"""Deterministic, auditable multi-metric ecological reasoning."""

from typing import List, Tuple
from app.core.schema import EnvironmentalInput, VariableInterconnection
from app.reasoning.rules import ECOLOGICAL_RULES
from app.reasoning.relationship_engine import relationship_engine


class MultiMetricReasoningEngine:
    def __init__(self):
        self.rules = ECOLOGICAL_RULES

    def extract_active_variables(self, env_input: EnvironmentalInput) -> List[str]:
        active: List[str] = []
        soil = env_input.soil
        climate = env_input.climate
        land = env_input.land_use
        bio = getattr(env_input, "biodiversity", None)
        human = getattr(env_input, "human_impact", None)
        query = (env_input.query or "").lower()

        if soil:
            if soil.organic_carbon_pct is not None: active.append("soil_organic_carbon")
            if soil.ph is not None: active.append("soil_ph")
            if soil.moisture_pct is not None: active.append("soil_moisture")
            if soil.soil_health is not None: active.append("soil_health")
            if soil.organic_carbon_pct is not None and soil.organic_carbon_pct < 1.0 and "soil_health" not in active:
                active.append("soil_health")
            if soil.moisture_pct is not None and soil.moisture_pct < 15:
                active.append("water_availability")

        if climate:
            if climate.rainfall_category or climate.annual_rainfall_mm is not None: active.append("water_availability")
            if climate.temperature_celsius is not None: active.append("climate")

        if land:
            if land.crop_type or land.current_cover or land.crop_diversity or land.management: active.append("crop_diversity")
            if land.habitat_fragmentation: active.append("habitat_fragmentation_index")

        if bio:
            if bio.status or bio.pollinator_status or bio.species_richness is not None: active.append("biodiversity")

        if human and (human.pollution or human.deforestation or human.disturbance):
            active.append("human_impact")

        # Natural-language signals. These add only what the user actually describes.
        if any(x in query for x in ["biodiversity", "species decline", "species are declining", "pollinator", "bees", "birds disappearing", "wildlife declining"]):
            active.append("biodiversity")
        if any(x in query for x in ["dry", "drought", "low rainfall", "very low rainfall", "water stress", "water shortage", "arid", "semi-arid", "semi arid"]):
            active.append("water_availability")
        if any(x in query for x in ["monoculture", "single crop", "one crop", "same crop every year", "crop diversity is low", "diverse crops"]):
            active.append("crop_diversity")
        if any(x in query for x in ["fragmented habitat", "habitat fragmentation", "high fragmentation", "hedgerow", "habitat corridor"]):
            active.append("habitat_fragmentation_index")
        if any(x in query for x in ["poor soil", "degraded soil", "soil degradation", "soil is degraded", "soil health is poor"]):
            active.append("soil_health")

        return list(dict.fromkeys(active))

    def reason(self, env_input: EnvironmentalInput) -> Tuple[List[str], List[VariableInterconnection]]:
        active = self.extract_active_variables(env_input)
        if len(active) < 3:
            return active, []

        connections: List[VariableInterconnection] = []
        for rule in self.rules:
            if rule.source_metric in active or rule.target_metric in active:
                connections.append(rule)

        for rel in relationship_engine.related_relationships(active):
            src, dst = rel.get("from"), rel.get("to")
            if not src or not dst or (src not in active and dst not in active):
                continue
            kind = {
                "supports": "synergy", "enhances": "synergy", "positive_feedback": "positive_feedback",
                "reduces": "tradeoff", "degrades": "tradeoff", "tradeoff": "tradeoff", "mitigation": "mitigation"
            }.get(rel.get("type", "synergy"), "synergy")
            if any(c.source_metric == src and c.target_metric == dst for c in connections):
                continue
            connections.append(VariableInterconnection(
                source_metric=src, target_metric=dst, relationship_type=kind,
                mechanism=rel.get("mechanism", "Structured ecological relationship from the knowledge base.")
            ))
        return active, connections


reasoning_engine = MultiMetricReasoningEngine()
