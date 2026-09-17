"""
Clarification Trigger & Missing Parameter Detector
"""

from typing import List, Tuple
from app.core.schema import EnvironmentalInput, ClarificationQuestion


class ClarificationManager:
    """
    Evaluates ecological input completeness and generates targeted follow-up questions
    when insufficient variables are provided for multi-metric scientific reasoning.
    """

    @staticmethod
    def evaluate_completeness(env_input: EnvironmentalInput) -> Tuple[bool, List[ClarificationQuestion]]:
        """
        Determines if the minimum variable requirement (at least 3 environmental variables)
        is met to perform multi-metric ecological reasoning.
        """
        questions: List[ClarificationQuestion] = []

        has_soil = (
            env_input.soil is not None and 
            (env_input.soil.organic_carbon_pct is not None or env_input.soil.ph is not None)
        )
        has_climate = (
            env_input.climate is not None and 
            (env_input.climate.rainfall_category is not None or env_input.climate.annual_rainfall_mm is not None)
        )
        has_land_use = (
            env_input.land_use is not None and 
            (env_input.land_use.crop_type is not None or env_input.land_use.current_cover is not None)
        )

        # Build clarification questions for missing dimensions
        if not has_soil:
            questions.append(
                ClarificationQuestion(
                    field_key="soil.organic_carbon_pct",
                    prompt_text="Can you provide the soil organic carbon % or current soil health status?",
                    recommended_options=["Low (< 0.5%)", "Moderate (0.5% - 1.5%)", "Healthy (> 1.5%)"]
                )
            )

        if not has_climate:
            questions.append(
                ClarificationQuestion(
                    field_key="climate.rainfall_category",
                    prompt_text="What is the rainfall pattern or regional climate condition?",
                    recommended_options=["Semi-arid / Low (< 400mm)", "Moderate (400-800mm)", "High (> 800mm)"]
                )
            )

        if not has_land_use:
            questions.append(
                ClarificationQuestion(
                    field_key="land_use.crop_type",
                    prompt_text="What is the current land use or cropping pattern?",
                    recommended_options=["Monoculture cereal", "Degraded pasture", "Intensive horticulture", "Fallow"]
                )
            )

        # If more than 1 dimension is missing, clarification is required before proceeding
        requires_clarification = len(questions) > 1
        return requires_clarification, questions


clarification_manager = ClarificationManager()
