from typing import List
from app.core.schema import VariableInterconnection

ECOLOGICAL_RULES: List[VariableInterconnection] = [
    VariableInterconnection(source_metric="soil_organic_carbon", target_metric="water_availability", relationship_type="positive_feedback", mechanism="Higher soil organic carbon can improve aggregation and water-holding capacity, with magnitude depending on soil and climate."),
    VariableInterconnection(source_metric="crop_diversity", target_metric="soil_organic_carbon", relationship_type="synergy", mechanism="Diverse crops provide varied root inputs and residue pathways that can contribute to soil organic matter."),
    VariableInterconnection(source_metric="soil_organic_carbon", target_metric="biodiversity", relationship_type="synergy", mechanism="Organic carbon supports soil biological functioning and habitat for soil organisms."),
    VariableInterconnection(source_metric="water_availability", target_metric="biodiversity", relationship_type="synergy", mechanism="Water availability constrains plant productivity and species persistence, especially during dry periods."),
    VariableInterconnection(source_metric="habitat_fragmentation_index", target_metric="biodiversity", relationship_type="tradeoff", mechanism="Greater habitat fragmentation can reduce connectivity and movement between habitat patches."),
    VariableInterconnection(source_metric="soil_ph", target_metric="biodiversity", relationship_type="synergy", mechanism="Strongly unsuitable pH can constrain plant nutrient availability and the composition of soil biological communities."),
    VariableInterconnection(source_metric="human_impact", target_metric="biodiversity", relationship_type="tradeoff", mechanism="High human disturbance can reduce habitat quality and ecological connectivity."),
]
