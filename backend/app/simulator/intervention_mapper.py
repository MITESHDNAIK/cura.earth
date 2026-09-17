"""
Cura.Earth intervention-specific ecological effects.

The values below are transparent model assumptions used to create
comparative What-If scenarios.

They represent directional model coefficients, NOT guaranteed
field measurements or universal ecological outcomes.
"""

from typing import Dict


INTERVENTION_EFFECTS: Dict[str, Dict[str, float]] = {

    "agroforestry": {
        "soil_organic_carbon": 0.060,
        "water_retention_capacity": 0.045,
        "microbial_diversity_index": 0.055,
        "pollinator_richness": 0.070,
        "habitat_fragmentation_index": -0.060,

        "water_availability": 0.050,
        "biodiversity": 0.070,
        "crop_diversity": 0.040,
    },

    "legume_intercropping": {
        "soil_organic_carbon": 0.055,
        "water_retention_capacity": 0.030,
        "microbial_diversity_index": 0.070,
        "pollinator_richness": 0.045,
        "habitat_fragmentation_index": -0.015,

        "water_availability": 0.035,
        "biodiversity": 0.050,
        "crop_diversity": 0.080,
    },

    "cover_cropping": {
        "soil_organic_carbon": 0.050,
        "water_retention_capacity": 0.060,
        "microbial_diversity_index": 0.060,
        "pollinator_richness": 0.035,
        "habitat_fragmentation_index": -0.010,

        "water_availability": 0.065,
        "biodiversity": 0.040,
        "crop_diversity": 0.025,
    },

    "native_hedgerows": {
        "soil_organic_carbon": 0.020,
        "water_retention_capacity": 0.025,
        "microbial_diversity_index": 0.030,
        "pollinator_richness": 0.085,
        "habitat_fragmentation_index": -0.080,

        "water_availability": 0.030,
        "biodiversity": 0.085,
        "crop_diversity": 0.020,
    },
}


INTERVENTION_NAMES = {

    "agroforestry":
        "Agroforestry / tree-crop integration",

    "legume_intercropping":
        "Legume-based intercropping",

    "cover_cropping":
        "Cover cropping with reduced soil disturbance",

    "native_hedgerows":
        "Native flowering hedgerows / habitat corridors",
}


def normalize_intervention_key(intervention: str) -> str:

    value = (intervention or "").strip().lower()

    aliases = {
        "agroforestry":
            "agroforestry",

        "agroforestry / tree-crop integration":
            "agroforestry",

        "tree-crop integration":
            "agroforestry",

        "silvo-arable agroforestry":
            "agroforestry",

        "legume intercropping":
            "legume_intercropping",

        "legume-based intercropping":
            "legume_intercropping",

        "intercropping":
            "legume_intercropping",

        "cover cropping":
            "cover_cropping",

        "cover crop":
            "cover_cropping",

        "cover crops":
            "cover_cropping",

        "native hedgerows":
            "native_hedgerows",

        "hedgerows":
            "native_hedgerows",

        "native flowering hedgerows":
            "native_hedgerows",

        "habitat corridors":
            "native_hedgerows",
    }

    return aliases.get(value, value)


def get_intervention_effects(intervention: str) -> Dict[str, float]:

    key = normalize_intervention_key(intervention)

    return INTERVENTION_EFFECTS.get(key, {})


def get_intervention_name(intervention: str) -> str:

    key = normalize_intervention_key(intervention)

    return INTERVENTION_NAMES.get(
        key,
        intervention or "No intervention"
    )