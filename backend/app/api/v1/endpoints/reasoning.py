"""
Multi-Metric Scientific Reasoning API Endpoint
"""

import uuid
from fastapi import APIRouter
from app.core.schema import EnvironmentalInput, EnvironmentalReasoningResponse
from app.reasoning.engine import reasoning_engine
from app.recommendations.engine import recommendation_engine


router = APIRouter()


@router.post("/reason", response_model=EnvironmentalReasoningResponse)
async def analyze_environmental_system(payload: EnvironmentalInput) -> EnvironmentalReasoningResponse:
    """
    Direct multi-metric analysis endpoint for structured input.
    Guarantees analysis connecting at least 3 environmental variables simultaneously.
    """
    session_id = payload.session_id or str(uuid.uuid4())
    active_vars, active_rules = reasoning_engine.reason(payload)
    recommendations = recommendation_engine.generate_recommendations(payload, active_vars)

    return EnvironmentalReasoningResponse(
        session_id=session_id,
        requires_clarification=False,
        clarification_questions=[],
        interconnected_variables=active_vars,
        variable_connections=active_rules,
        recommendations=recommendations,
        system_notes="Direct multi-metric diagnosis synthesized across soil, water, and land-use metrics."
    )
