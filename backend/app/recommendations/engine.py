"""Condition-aware ecological recommendation engine for Cura.Earth.

Key rule:
- A populated parameter is an OBSERVATION, not automatically a STRESS.
- Recommendations are generated only when a meaningful ecological stress signal
  is detected.
- Intervention scores are driven by those stress signals, then strengthened by
  multi-metric coverage and known ecological relationships.
"""

from __future__ import annotations

from typing import Any, Dict, List

from app.core.schema import (
    EnvironmentalInput,
    RecommendationItem,
    VariableInterconnection,
)
from app.reasoning.intervention_engine import intervention_engine
from app.recommendations.evidence_linker import evidence_linker


class RecommendationEngine:
    """Select interventions from actual environmental stressors."""

    # ---------------------------------------------------------
    # STRESS SIGNAL EXTRACTION
    # ---------------------------------------------------------

    def _signals(self, e: EnvironmentalInput) -> set[str]:
        signals: set[str] = set()

        soil = e.soil
        climate = e.climate
        land = e.land_use
        bio = getattr(e, "biodiversity", None)
        human = getattr(e, "human_impact", None)
        query = (e.query or "").lower()

        # ---------------- SOIL ----------------
        if soil:
            soc = soil.organic_carbon_pct
            moisture = soil.moisture_pct
            ph = soil.ph

            if soc is not None:
                if soc < 1.0:
                    signals.add("low_soc")
                elif soc >= 1.5:
                    signals.add("healthy_soc")

            # IMPORTANT: only low moisture is a stress.
            if moisture is not None:
                if moisture <= 15:
                    signals.add("very_low_moisture")
                elif moisture >= 30:
                    signals.add("water_adequate")

            # IMPORTANT: normal pH produces NO pH intervention signal.
            if ph is not None:
                if ph < 5.5:
                    signals.add("acidic_soil")
                elif ph > 8.2:
                    signals.add("alkaline_soil")

            soil_health = getattr(soil, "soil_health", None)
            if soil_health == "degraded":
                signals.add("degraded_soil")
            elif soil_health == "healthy":
                signals.add("healthy_soil")

        # ---------------- CLIMATE ----------------
        if climate:
            rainfall = climate.rainfall_category
            annual_mm = climate.annual_rainfall_mm

            if rainfall in {"very_low", "low"}:
                signals.add("low_rainfall")
            elif rainfall in {"high", "very_high"}:
                signals.add("rainfall_adequate")

            if rainfall == "very_low":
                signals.add("very_low_rainfall")

            if annual_mm is not None:
                if annual_mm < 500:
                    signals.add("low_rainfall")
                elif annual_mm >= 800:
                    signals.add("rainfall_adequate")

                if annual_mm < 300:
                    signals.add("very_low_rainfall")

        # ---------------- LAND USE ----------------
        if land:
            management = " ".join(
                filter(
                    None,
                    [
                        getattr(land, "management", None),
                        getattr(land, "current_cover", None),
                        getattr(land, "tillage_practice", None),
                    ],
                )
            ).lower()

            diversity = getattr(land, "crop_diversity", None)

            if diversity == "low" or any(
                phrase in management
                for phrase in ("monoculture", "single crop")
            ):
                signals.add("monoculture")

            if diversity == "high" or "intercropping" in management:
                signals.add("already_diverse")

            if getattr(land, "habitat_fragmentation", None) == "high":
                signals.add("high_fragmentation")

            if getattr(land, "tillage_practice", None) == "conventional":
                signals.add("conventional_tillage")

        # ---------------- BIODIVERSITY ----------------
        if bio:
            if getattr(bio, "status", None) == "declining":
                signals.add("biodiversity_decline")
            if getattr(bio, "pollinator_status", None) == "declining":
                signals.add("pollinator_decline")

        # ---------------- HUMAN IMPACT ----------------
        if human:
            if getattr(human, "pollution", False):
                signals.add("high_pollution")
            if getattr(human, "deforestation", False):
                signals.add("habitat_loss")
            if getattr(human, "disturbance", False):
                signals.add("human_disturbance")

        # ---------------- NATURAL LANGUAGE ----------------
        if any(
            phrase in query
            for phrase in (
                "biodiversity is declining",
                "biodiversity declining",
                "wildlife declining",
                "species declining",
            )
        ):
            signals.add("biodiversity_decline")

        if any(
            phrase in query
            for phrase in (
                "pollinator",
                "pollinators",
                "bees disappearing",
                "pollinator decline",
            )
        ):
            signals.add("pollinator_decline")

        if any(
            phrase in query
            for phrase in (
                "fragmented habitat",
                "habitat fragmentation",
                "high fragmentation",
            )
        ):
            signals.add("high_fragmentation")

        if any(
            phrase in query
            for phrase in (
                "poor soil",
                "degraded soil",
                "soil degradation",
                "degraded land",
            )
        ):
            signals.add("degraded_soil")

        if any(
            phrase in query
            for phrase in (
                "dry soil",
                "soil is dry",
                "soil stays dry",
                "low moisture",
                "poor water retention",
                "water retention",
                "water stress",
                "drought stress",
            )
        ):
            signals.add("very_low_moisture")

        if any(
            phrase in query
            for phrase in (
                "low rainfall",
                "very low rainfall",
                "low rain",
                "very low rain",
                "low precipitation",
            )
        ):
            signals.add("low_rainfall")

        if any(
            phrase in query
            for phrase in (
                "monoculture",
                "single crop",
                "same crop every year",
            )
        ):
            signals.add("monoculture")

        if any(
            phrase in query
            for phrase in (
                "acidic soil",
                "acid soil",
                "low soil ph",
            )
        ):
            signals.add("acidic_soil")

        if any(
            phrase in query
            for phrase in (
                "alkaline soil",
                "high soil ph",
            )
        ):
            signals.add("alkaline_soil")

        if any(
            phrase in query
            for phrase in (
                "pollution",
                "polluted",
                "pesticides",
                "pesticide pressure",
                "pesticide use",
                "chemical runoff",
                "chemical pollution",
            )
        ):
            signals.add("high_pollution")

        if any(
            phrase in query
            for phrase in (
                "water contamination",
                "contaminated water",
            )
        ):
            signals.add("water_contamination")

        if any(
            phrase in query
            for phrase in (
                "habitat loss",
                "deforestation",
                "forest loss",
            )
        ):
            signals.add("habitat_loss")

        return signals

    # ---------------------------------------------------------
    # CONDITION -> INTERVENTION SCORING
    # ---------------------------------------------------------

    def _score(
        self,
        candidate: dict,
        signals: set[str],
        active_vars: List[str],
        connections: List[VariableInterconnection],
    ) -> tuple[float, List[str]]:

        key = candidate["key"]
        matched: set[str] = set()

        # Candidate-specific ecological triggers.
        trigger_map = {
            "agroforestry": {
                "low_soc": 4,
                "low_rainfall": 4,
                "very_low_rainfall": 2,
                "monoculture": 3,
                "high_fragmentation": 2,
                "biodiversity_decline": 2,
            },
            "legume_intercropping": {
                "low_soc": 4,
                "monoculture": 4,
            },
            "cover_cropping": {
                "low_soc": 3,
                "very_low_moisture": 5,
                "degraded_soil": 4,
                "conventional_tillage": 3,
            },
            "water_retention_management": {
                "very_low_moisture": 6,
                "very_low_rainfall": 5,
                "low_rainfall": 3,
            },
            "soil_water_retention": {
                "very_low_moisture": 6,
                "very_low_rainfall": 5,
                "low_rainfall": 3,
            },
            "soil_ph_management": {
                "acidic_soil": 8,
                "alkaline_soil": 8,
            },
            "pesticide_reduction": {
                "high_pollution": 8,
                "pollinator_decline": 3,
            },
            "riparian_buffers": {
                "high_pollution": 5,
                "water_contamination": 8,
            },
            "native_hedgerows": {
                "pollinator_decline": 7,
                "high_fragmentation": 7,
                "biodiversity_decline": 4,
            },
            "habitat_restoration": {
                "habitat_loss": 8,
                "high_fragmentation": 7,
                "biodiversity_decline": 4,
            },
            "native_habitat_restoration": {
                "habitat_loss": 8,
                "high_fragmentation": 7,
                "biodiversity_decline": 4,
            },
        }

        triggers = trigger_map.get(key, {})

        for signal, points in triggers.items():
            if signal in signals:
                matched.add(signal)

        # Unknown/custom interventions can still use their declared strengths.
        if not triggers:
            matched |= (
                set(candidate.get("strengths", []))
                & signals
            )

        # If this intervention has no actual stressor match, do NOT recommend it.
        if not matched:
            return 0.0, []

        score = sum(triggers.get(signal, 5) for signal in matched)

        # Multi-metric coverage is useful, but never enough by itself.
        overlap_count = len(
            set(candidate.get("overlap", []))
            & set(active_vars)
        )
        score += min(overlap_count, 3) * 0.75

        # Relationship support is a secondary tie-breaker.
        relationship_count = len(
            [
                connection
                for connection in connections
                if (
                    connection.source_metric in candidate.get("affects", [])
                    or connection.target_metric in candidate.get("affects", [])
                )
            ]
        )
        score += min(relationship_count, 4) * 0.35

        # Already-diverse farms should not be pushed toward intercropping.
        if key == "legume_intercropping" and "already_diverse" in signals:
            score -= 5

        # Agroforestry is deliberately not allowed to dominate every profile.
        if key == "agroforestry":
            if (
                "healthy_soc" in signals
                and "rainfall_adequate" in signals
                and "high_fragmentation" not in signals
                and "monoculture" not in signals
            ):
                score -= 6

        return max(score, 0.0), sorted(matched)

    # ---------------------------------------------------------
    # MAIN GENERATION
    # ---------------------------------------------------------

    def generate_recommendations(
        self,
        env_input: EnvironmentalInput,
        active_vars: List[str],
        connections: List[VariableInterconnection] | None = None,
    ) -> List[RecommendationItem]:

        connections = connections or []
        signals = self._signals(env_input)

        # No stress = no forced intervention.
        meaningful_stress = {
            "low_soc",
            "very_low_moisture",
            "low_rainfall",
            "very_low_rainfall",
            "acidic_soil",
            "alkaline_soil",
            "degraded_soil",
            "monoculture",
            "high_fragmentation",
            "biodiversity_decline",
            "pollinator_decline",
            "high_pollution",
            "water_contamination",
            "habitat_loss",
            "conventional_tillage",
        }

        if not signals.intersection(meaningful_stress):
            return []

        candidates = intervention_engine.get_applicable(
            set(active_vars)
        )

        if not candidates:
            return []

        scored: List[Dict[str, Any]] = []

        for candidate in candidates:
            score, matched = self._score(
                candidate,
                signals,
                active_vars,
                connections,
            )

            if score <= 0:
                continue

            try:
                evidence = evidence_linker.get_evidence_for_intervention(
                    candidate["key"]
                )
            except Exception:
                evidence = []

            scored.append(
                {
                    "candidate": candidate,
                    "score": score,
                    "matched": matched,
                    "evidence": evidence,
                }
            )

        scored.sort(
            key=lambda item: (
                item["score"],
                len(item["matched"]),
                len(item["evidence"]),
            ),
            reverse=True,
        )

        if not scored:
            return []

        # Keep recommendations genuinely different.
        selected: List[Dict[str, Any]] = []
        covered_metrics: set[str] = set()

        for item in scored:
            candidate = item["candidate"]
            affected = set(candidate.get("overlap", []))

            if not selected:
                selected.append(item)
                covered_metrics.update(affected)
                continue

            # Do not fill the UI with near-duplicates.
            new_metrics = affected - covered_metrics

            if new_metrics or len(selected) < 2:
                selected.append(item)
                covered_metrics.update(affected)

            if len(selected) >= 3:
                break

        recommendations: List[RecommendationItem] = []

        for item in selected:
            candidate = item["candidate"]
            matched = item["matched"]
            evidence = item["evidence"]

            impacted = self._impact_metrics(
                candidate,
                signals,
            )

            recommendations.append(
                RecommendationItem(
                    action=candidate["name"],
                    scientific_reasoning=self._reasoning(
                        candidate,
                        signals,
                        matched,
                        impacted,
                    ),
                    impacted_metrics=impacted,
                    measurable_improvements=self._measurement(
                        candidate["key"]
                    ),
                    time_horizon=candidate.get(
                        "time_horizon",
                        "medium_term",
                    ),
                    confidence_level=self._confidence(
                        matched,
                        evidence,
                        active_vars,
                    ),
                    evidence=evidence,
                )
            )

        return recommendations

    def recommend(
        self,
        env_input: EnvironmentalInput,
    ) -> List[RecommendationItem]:

        from app.reasoning.engine import reasoning_engine

        active, connections = reasoning_engine.reason(env_input)

        return self.generate_recommendations(
            env_input,
            active,
            connections,
        )

    # ---------------------------------------------------------
    # IMPACT METRICS
    # ---------------------------------------------------------

    def _impact_metrics(
        self,
        candidate: dict,
        signals: set[str],
    ) -> List[str]:

        preferred: List[str] = []

        for metric in candidate.get("affects", []):
            if (
                metric == "soil_moisture"
                and "very_low_moisture" in signals
            ):
                preferred.append(metric)

            elif (
                metric == "soil_ph"
                and (
                    "acidic_soil" in signals
                    or "alkaline_soil" in signals
                )
            ):
                preferred.append(metric)

            elif (
                metric == "habitat_fragmentation_index"
                and "high_fragmentation" in signals
            ):
                preferred.append(metric)

            elif (
                metric == "biodiversity"
                and (
                    "biodiversity_decline" in signals
                    or "pollinator_decline" in signals
                )
            ):
                preferred.append(metric)

            elif metric in {
                "soil_organic_carbon",
                "water_availability",
                "crop_diversity",
            } and metric in candidate.get("overlap", []):
                preferred.append(metric)

        return preferred or list(candidate.get("overlap", []))

    # ---------------------------------------------------------
    # EXPLANATION
    # ---------------------------------------------------------

    def _reasoning(
        self,
        candidate: dict,
        signals: set[str],
        matched: List[str],
        impacted: List[str],
    ) -> str:

        signal_text = (
            ", ".join(matched)
            if matched
            else "the observed multi-metric profile"
        )

        return (
            f"{candidate['name']} is selected because the profile "
            f"contains the specific stress signals: {signal_text}. "
            f"The intervention targets {', '.join(impacted)} "
            f"through its ecological mechanism. It was not selected "
            f"merely because the parameter was provided; the parameter "
            f"had to indicate a meaningful environmental stress."
        )

    # ---------------------------------------------------------
    # MEASUREMENT
    # ---------------------------------------------------------

    def _measurement(self, key: str) -> str:

        statements = {
            "agroforestry":
                "Track SOC, infiltration/water retention, crop diversity "
                "and habitat indicators annually; use the simulator only "
                "as an illustrative trajectory until locally calibrated.",

            "legume_intercropping":
                "Track SOC, crop diversity, yield stability and soil "
                "nutrient indicators across 2–3 growing seasons; response "
                "is site- and species-dependent.",

            "cover_cropping":
                "Track soil moisture, SOC, erosion/ground cover and "
                "microbial indicators across successive seasons; magnitude "
                "depends on species, climate and management.",

            "native_hedgerows":
                "Track flowering-season pollinator observations, native "
                "plant establishment and habitat connectivity over "
                "1–3 seasons.",

            "water_retention_management":
                "Track root-zone moisture, infiltration and runoff after "
                "rainfall events over the next growing season.",

            "soil_water_retention":
                "Track root-zone moisture, infiltration and runoff after "
                "rainfall events over the next growing season.",

            "soil_ph_management":
                "Repeat soil pH and nutrient-availability testing after "
                "the appropriate amendment interval; target crop-specific "
                "pH rather than a universal value.",

            "pesticide_reduction":
                "Track pesticide use intensity, non-target observations "
                "and water-quality indicators across growing seasons.",

            "habitat_restoration":
                "Track native vegetation establishment, habitat connectivity "
                "and species/pollinator observations over 1–3 years.",

            "native_habitat_restoration":
                "Track native vegetation establishment, habitat connectivity "
                "and species/pollinator observations over 1–3 years.",

            "riparian_buffers":
                "Track runoff, water-quality indicators and aquatic/terrestrial "
                "habitat observations across seasons.",
        }

        return statements.get(
            key,
            "Monitor the directly affected environmental metrics "
            "before and after implementation.",
        )

    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------

    def _confidence(
        self,
        matched: List[str],
        evidence: List,
        active_vars: List[str],
    ) -> str:

        if (
            len(matched) >= 2
            and evidence
            and len(active_vars) >= 3
        ):
            return "high"

        if matched or evidence:
            return "medium"

        return "low"


recommendation_engine = RecommendationEngine()
