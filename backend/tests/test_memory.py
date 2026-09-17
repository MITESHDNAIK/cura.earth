"""
Tests for Conversational Memory and Clarification Tracking
"""

from app.core.schema import EnvironmentalInput, SoilMetrics, ClimateMetrics, LandUseMetrics
from app.core.memory import session_memory
from app.core.clarification import clarification_manager


def test_session_state_accumulation():
    session_id = "test-session-123"
    session = session_memory.get_or_create_session(session_id)

    # Turn 1: User specifies soil metric only
    turn1_input = EnvironmentalInput(soil=SoilMetrics(organic_carbon_pct=0.4))
    session.update_environmental_state(turn1_input)
    assert session.current_state.soil.organic_carbon_pct == 0.4
    assert session.current_state.climate.rainfall_category is None

    # Clarification should be triggered because climate and land use are missing
    requires_clarification, questions = clarification_manager.evaluate_completeness(session.current_state)
    assert requires_clarification is True

    # Turn 2: User provides climate and crop
    turn2_input = EnvironmentalInput(
        climate=ClimateMetrics(rainfall_category="low"),
        land_use=LandUseMetrics(crop_type="wheat")
    )
    session.update_environmental_state(turn2_input)

    # State now contains variables from both turns
    assert session.current_state.soil.organic_carbon_pct == 0.4
    assert session.current_state.climate.rainfall_category == "low"
    assert session.current_state.land_use.crop_type == "wheat"

    # Now sufficient variables exist
    requires_clarification_turn2, _ = clarification_manager.evaluate_completeness(session.current_state)
    assert requires_clarification_turn2 is False
