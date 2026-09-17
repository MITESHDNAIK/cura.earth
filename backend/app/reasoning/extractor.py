"""
Natural-language environmental information extractor.

This is intentionally lightweight and deterministic.

It converts normal user language into the structured environmental
profile consumed by Cura.Earth's reasoning engine.
"""

from __future__ import annotations

import re
from typing import Any, Dict


class EnvironmentalExtractor:
    def extract(self, text: str) -> Dict[str, Any]:
        text = (text or "").strip()

        profile: Dict[str, Any] = {
            "soil": {},
            "climate": {},
            "land_use": {},
            "spatial": {},
            "biodiversity": {},
            "human_impact": {},
            "what_if": {},
        }

        if not text:
            return profile

        lower = text.lower()

        self._extract_soil(lower, profile)
        self._extract_climate(lower, profile)
        self._extract_land_use(lower, profile)
        self._extract_biodiversity(lower, profile)
        self._extract_human_impact(lower, profile)
        self._extract_spatial(lower, profile)
        self._extract_intervention(lower, profile)

        return {
            key: value
            for key, value in profile.items()
            if value
        }

    # ============================================================
    # SOIL
    # ============================================================

    def _extract_soil(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        soc_patterns = [
            r"(?:soil\s+organic\s+carbon|soil\s+carbon|organic\s+carbon|soc)"
            r"\s*(?:is|=|around|about|approximately|of)?\s*"
            r"(\d+(?:\.\d+)?)\s*(?:%|percent)",

            r"(?:soil\s+organic\s+carbon|soil\s+carbon|organic\s+carbon|soc)"
            r"\s*:\s*(\d+(?:\.\d+)?)\s*(?:%|percent)",
        ]

        for pattern in soc_patterns:
            match = re.search(pattern, text, re.I)

            if match:
                profile["soil"]["organic_carbon_pct"] = float(
                    match.group(1)
                )
                break

        # pH
        ph_match = re.search(
            r"(?:soil\s+)?pH\s*(?:is|=|around|about|of)?\s*"
            r"(\d+(?:\.\d+)?)",
            text,
            re.I,
        )

        if ph_match:
            profile["soil"]["ph"] = float(ph_match.group(1))

        # Moisture
        moisture_match = re.search(
            r"(?:soil\s+)?moisture\s*(?:is|=|around|about|of)?\s*"
            r"(\d+(?:\.\d+)?)\s*(?:%|percent)",
            text,
            re.I,
        )

        if moisture_match:
            profile["soil"]["moisture_pct"] = float(
                moisture_match.group(1)
            )

        # Qualitative soil condition
        if any(
            phrase in text
            for phrase in [
                "poor soil",
                "soil is poor",
                "soil has degraded",
                "degraded soil",
                "soil degradation",
                "soil is degraded",
                "soil health is poor",
                "fertility has declined",
                "low soil health",
                "poor soil health",
            ]
        ):
            profile["soil"]["soil_health"] = "degraded"

        if any(
            phrase in text
            for phrase in [
                "healthy soil",
                "soil is healthy",
                "good soil",
                "good soil health",
                "healthy soil health",
            ]
        ):
            profile["soil"]["soil_health"] = "healthy"

    # ============================================================
    # CLIMATE / WATER
    # ============================================================

    def _extract_climate(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        # Numerical rainfall amount
        rainfall_match = re.search(
            r"(?:annual\s+)?rainfall\s*(?:is|=|around|about|of)?\s*"
            r"(\d+(?:\.\d+)?)\s*(?:mm|millimetres|millimeters)",
            text,
            re.I,
        )

        if rainfall_match:
            profile["climate"]["annual_rainfall_mm"] = float(
                rainfall_match.group(1)
            )

        # --------------------------------------------------------
        # Qualitative rainfall
        # --------------------------------------------------------
        # Check most specific categories first.
        # This prevents "very low" from being classified simply as "low".
        if any(
            phrase in text
            for phrase in [
                "very low rainfall",
                "rainfall is very low",
                "rainfall: very low",
                "very low rain",
                "rain is very low",
            ]
        ):
            profile["climate"]["rainfall_category"] = "very_low"

        elif any(
            phrase in text
            for phrase in [
                "very high rainfall",
                "rainfall is very high",
                "rainfall: very high",
                "very high rain",
                "rain is very high",
            ]
        ):
            profile["climate"]["rainfall_category"] = "very_high"

        elif any(
            phrase in text
            for phrase in [
                "moderate rainfall",
                "rainfall is moderate",
                "rainfall: moderate",
                "moderate rain",
                "rain is moderate",
            ]
        ):
            profile["climate"]["rainfall_category"] = "moderate"

        elif any(
            phrase in text
            for phrase in [
                "low rainfall",
                "rainfall is low",
                "rainfall: low",
                "little rainfall",
                "low rain",
                "rain is low",
                "dry climate",
                "dry region",
                "water stress",
                "water shortage",
                "drought",
                "drought-prone",
                "drought prone",
                "rainfall: little",
                "rainfall: dry",
            ]
        ):
            profile["climate"]["rainfall_category"] = "low"

        elif any(
            phrase in text
            for phrase in [
                "high rainfall",
                "rainfall is high",
                "rainfall: high",
                "heavy rainfall",
                "high rain",
                "rain is high",
                "very rainy",
                "wet climate",
                "rainfall: wet",
            ]
        ):
            profile["climate"]["rainfall_category"] = "high"

        # Temperature
        temperature_match = re.search(
            r"(?:temperature|temp)\s*(?:is|=|around|about|of)?\s*"
            r"(-?\d+(?:\.\d+)?)\s*(?:°?\s*c|celsius)",
            text,
            re.I,
        )

        if temperature_match:
            profile["climate"]["temperature_celsius"] = float(
                temperature_match.group(1)
            )

        # Aridity
        aridity_match = re.search(
            r"(?:aridity\s+index|aridity)\s*(?:is|=|around|about|of)?\s*"
            r"(\d+(?:\.\d+)?)",
            text,
            re.I,
        )

        if aridity_match:
            profile["climate"]["aridity_index"] = float(
                aridity_match.group(1)
            )

    # ============================================================
    # LAND USE
    # ============================================================

    def _extract_land_use(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        crops = [
            "wheat",
            "rice",
            "maize",
            "corn",
            "soybean",
            "cotton",
            "sugarcane",
            "millet",
            "sorghum",
            "barley",
        ]

        for crop in crops:
            if re.search(
                rf"\b{re.escape(crop)}\b",
                text,
                re.I,
            ):
                profile["land_use"]["crop_type"] = crop
                break

        if any(
            phrase in text
            for phrase in [
                "monoculture",
                "single crop",
                "one crop",
                "same crop every year",
                "grow the same crop every year",
                "growing wheat every year",
                "wheat every year",
            ]
        ):
            profile["land_use"]["management"] = "monoculture"
            profile["land_use"]["crop_diversity"] = "low"

        if any(
            phrase in text
            for phrase in [
                "intercropping",
                "intercrop",
                "mixed cropping",
                "mixed crops",
            ]
        ):
            profile["land_use"]["management"] = "intercropping"
            profile["land_use"]["crop_diversity"] = "high"

        if "agroforestry" in text:
            profile["land_use"]["management"] = "agroforestry"
            profile["land_use"]["crop_diversity"] = "high"

        if any(
            phrase in text
            for phrase in [
                "crop diversity is low",
                "low crop diversity",
                "low diversity of crops",
            ]
        ):
            profile["land_use"]["crop_diversity"] = "low"

        if any(
            phrase in text
            for phrase in [
                "crop diversity is high",
                "high crop diversity",
                "diverse crops",
            ]
        ):
            profile["land_use"]["crop_diversity"] = "high"

        if any(
            phrase in text
            for phrase in [
                "conventional tillage",
                "conventional farming",
                "intensive tillage",
            ]
        ):
            profile["land_use"]["tillage_practice"] = "conventional"

        if any(
            phrase in text
            for phrase in [
                "reduced tillage",
                "minimum tillage",
                "no till",
                "no-till",
            ]
        ):
            profile["land_use"]["tillage_practice"] = "reduced"

        if any(
            phrase in text
            for phrase in [
                "fragmented habitat",
                "habitat fragmentation",
                "high fragmentation",
                "highly fragmented",
                "fields are fragmented",
            ]
        ):
            profile["land_use"]["habitat_fragmentation"] = "high"

    # ============================================================
    # BIODIVERSITY
    # ============================================================

    def _extract_biodiversity(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        if any(
            phrase in text
            for phrase in [
                "biodiversity is declining",
                "biodiversity decline",
                "biodiversity declining",
                "biodiversity is decreasing",
                "biodiversity has declined",
                "less biodiversity",
                "loss of biodiversity",
                "declining biodiversity",
                "decreasing biodiversity",
            ]
        ):
            profile["biodiversity"]["status"] = "declining"

        if any(
            phrase in text
            for phrase in [
                "pollinators are declining",
                "pollinator decline",
                "fewer pollinators",
                "pollinators disappearing",
                "pollinators have disappeared",
                "pollinators disappeared",
            ]
        ):
            profile["biodiversity"]["pollinator_status"] = "declining"

        if any(
            phrase in text
            for phrase in [
                "species are declining",
                "species decline",
                "species disappearing",
                "wildlife is declining",
                "wildlife decline",
            ]
        ):
            profile["biodiversity"]["species_status"] = "declining"

    # ============================================================
    # HUMAN IMPACT
    # ============================================================

    def _extract_human_impact(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        # Pollution / pesticide pressure
        if any(
            phrase in text
            for phrase in [
                "pollution",
                "polluted",
                "chemical pollution",
                "pesticide pollution",
                "pesticides",
                "pesticide use",
                "pesticide usage",
                "use pesticides",
                "using pesticides",
                "heavy pesticide use",
                "heavily use pesticides",
                "pesticides heavily",
                "chemical inputs",
                "agrochemical use",
                "agrochemicals",
            ]
        ):
            profile["human_impact"]["pollution"] = True

        # Deforestation
        if any(
            phrase in text
            for phrase in [
                "deforestation",
                "forest loss",
                "trees have been removed",
                "trees removed",
                "forest has been cleared",
                "forest clearing",
            ]
        ):
            profile["human_impact"]["deforestation"] = True

        # Land-use / habitat change
        if any(
            phrase in text
            for phrase in [
                "habitat loss",
                "land conversion",
                "land converted",
                "natural habitat removed",
                "habitat destroyed",
                "habitat destruction",
            ]
        ):
            profile["human_impact"]["land_use_change"] = True

    # ============================================================
    # SPATIAL
    # ============================================================

    def _extract_spatial(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        regions = [
            "semi-arid",
            "semi arid",
            "arid",
            "tropical",
            "temperate",
            "coastal",
            "forest",
            "grassland",
            "wetland",
        ]

        for region in regions:
            if region in text:
                profile["spatial"]["region"] = region
                break

    # ============================================================
    # WHAT-IF INTERVENTION
    # ============================================================

    def _extract_intervention(
        self,
        text: str,
        profile: Dict[str, Any],
    ) -> None:

        interventions = {
            "agroforestry": [
                "agroforestry",
                "trees between crops",
                "trees among crops",
                "integrate trees",
                "introduce trees",
                "tree crop integration",
            ],
            "legume_intercropping": [
                "legume intercropping",
                "legume intercrop",
                "intercrop legumes",
                "plant legumes between",
            ],
            "cover_cropping": [
                "cover cropping",
                "cover crop",
                "cover crops",
            ],
            "native_hedgerows": [
                "hedgerow",
                "hedgerows",
                "habitat corridor",
                "native flowering plants",
                "flowering corridor",
            ],
        }

        for key, phrases in interventions.items():
            if any(phrase in text for phrase in phrases):
                profile["what_if"]["intervention"] = key
                break


# Singleton used by the application.
extractor = EnvironmentalExtractor()


def extract_environmental_profile(text: str) -> Dict[str, Any]:
    return extractor.extract(text)