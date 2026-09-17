"""
Conversational Intelligence API Endpoint
"""

import uuid
from fastapi import APIRouter
from app.core.schema import EnvironmentalInput, EnvironmentalReasoningResponse
from app.core.memory import session_memory
from app.core.clarification import clarification_manager
from app.reasoning.engine import reasoning_engine
from app.recommendations.engine import recommendation_engine


router = APIRouter()


@router.post("/chat", response_model=EnvironmentalReasoningResponse)
async def chat_interaction(payload: EnvironmentalInput) -> EnvironmentalReasoningResponse:
    """
    Handles multi-turn conversational query, tracks environmental variables in memory,
    and asks clarifying questions if incomplete inputs prevent 3-variable reasoning.
    """
    session_id = payload.session_id or str(uuid.uuid4())
    session = session_memory.get_or_create_session(session_id)

    # Record user message & update state
    if payload.query:
        session.add_message("user", payload.query)
    session.update_environmental_state(payload)

    # Check completeness
    requires_clarification, questions = clarification_manager.evaluate_completeness(session.current_state)

    if requires_clarification:
        return EnvironmentalReasoningResponse(
            session_id=session_id,
            requires_clarification=True,
            clarification_questions=questions,
            interconnected_variables=[],
            variable_connections=[],
            recommendations=[],
            system_notes="Insufficient variables provided. Proactive clarification required before generating scientific diagnosis."
        )

    # If complete, execute multi-metric reasoning and evidence recommendations
    active_vars, active_rules = reasoning_engine.reason(session.current_state)
    recommendations = recommendation_engine.generate_recommendations(session.current_state, active_vars)

    return EnvironmentalReasoningResponse(
        session_id=session_id,
        requires_clarification=False,
        clarification_questions=[],
        interconnected_variables=active_vars,
        variable_connections=active_rules,
        recommendations=recommendations,
        system_notes="Multi-metric scientific reasoning completed successfully."
    )
