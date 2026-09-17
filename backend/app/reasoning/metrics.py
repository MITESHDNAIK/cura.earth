"""
Ecological Metric Definitions & Threshold Baselines
"""

from typing import Dict, Any


METRIC_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "soil_organic_carbon": {
        "unit": "%",
        "description": "Concentration of organic carbon in topsoil (0-30cm)",
        "thresholds": {
            "severely_depleted": (0.0, 0.4),
            "depleted": (0.4, 0.8),
            "moderate": (0.8, 1.5),
            "healthy": (1.5, 3.0),
            "rich": (3.0, 10.0)
        }
    },
    "soil_ph": {
        "unit": "pH",
        "description": "Soil acidity/alkalinity level",
        "thresholds": {
            "acidic": (0.0, 6.0),
            "neutral_optimal": (6.0, 7.5),
            "alkaline": (7.5, 14.0)
        }
    },
    "microbial_diversity_index": {
        "unit": "Shannon Index (H')",
        "description": "Soil fungal and bacterial taxonomic diversity",
        "thresholds": {
            "poor": (0.0, 2.0),
            "moderate": (2.0, 3.5),
            "high": (3.5, 5.0)
        }
    },
    "water_retention_capacity": {
        "unit": "mm/m",
        "description": "Plant available water capacity in root zone",
        "thresholds": {
            "low": (0.0, 80.0),
            "medium": (80.0, 150.0),
            "high": (150.0, 250.0)
        }
    },
    "habitat_fragmentation_index": {
        "unit": "Index (0-1)",
        "description": "Degree of patch isolation and edge density",
        "thresholds": {
            "continuous": (0.0, 0.25),
            "moderate_fragmentation": (0.25, 0.6),
            "severe_fragmentation": (0.6, 1.0)
        }
    },
    "pollinator_richness": {
        "unit": "Species / hectare",
        "description": "Native bee, hoverfly, and lepidoptera richness",
        "thresholds": {
            "depleted": (0, 5),
            "moderate": (5, 15),
            "thriving": (15, 50)
        }
    }
}
