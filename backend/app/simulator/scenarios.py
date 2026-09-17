"""
Predefined Ecological Benchmark Scenarios for Cura.Earth What-If Simulation.

These scenarios are modelled benchmarks for comparative simulation.
They are not field measurements or guaranteed real-world predictions.
"""

from typing import Dict, Any


BENCHMARK_SCENARIOS: Dict[str, Dict[str, Any]] = {

    "semi_arid_monoculture_agroforestry": {

        "title": "Semi-Arid Monoculture to Silvo-Arable Agroforestry",

        "description": (
            "Low-SOC wheat monoculture in a semi-arid environment. "
            "The scenario models ecological recovery under different "
            "land-management interventions."
        ),

        "baseline": {
            # Soil
            "soil_organic_carbon": 0.35,

            # Water
            "water_retention_capacity": 65.0,

            # Biological indicators
            "microbial_diversity_index": 1.4,
            "pollinator_richness": 4.0,

            # Landscape
            "habitat_fragmentation_index": 0.85,

            # Derived ecological state variables
            "water_availability": 0.35,
            "biodiversity": 0.32,

            # Monoculture baseline
            "crop_diversity": 0.10,
        },

        "annual_rate_multipliers": {
            "soil_organic_carbon": 0.08,
            "water_retention_capacity": 0.06,
            "microbial_diversity_index": 0.12,
            "pollinator_richness": 0.15,
            "habitat_fragmentation_index": -0.09,

            # Derived metrics are calculated through ecological cascades.
            "water_availability": 0.0,
            "biodiversity": 0.0,
            "crop_diversity": 0.0,
        },
    },

    "regenerative_riparian_buffer": {

        "title": "Riparian Buffer & Hedgerow Restoration",

        "description": (
            "Agricultural landscape with degraded field margins where "
            "native vegetation and riparian buffers are restored."
        ),

        "baseline": {
            "soil_organic_carbon": 0.60,
            "water_retention_capacity": 90.0,
            "microbial_diversity_index": 2.1,
            "pollinator_richness": 7.0,
            "habitat_fragmentation_index": 0.70,

            "water_availability": 0.62,
            "biodiversity": 0.58,
            "crop_diversity": 0.30,
        },

        "annual_rate_multipliers": {
            "soil_organic_carbon": 0.05,
            "water_retention_capacity": 0.09,
            "microbial_diversity_index": 0.08,
            "pollinator_richness": 0.22,
            "habitat_fragmentation_index": -0.15,

            "water_availability": 0.0,
            "biodiversity": 0.0,
            "crop_diversity": 0.0,
        },
    },
}