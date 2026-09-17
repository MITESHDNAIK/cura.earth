from typing import Any, Dict

from fastapi import APIRouter, Body

from app.core.schema import EnvironmentalInput
from app.reasoning.conversation_service import conversation_service


router = APIRouter()


@router.post("/conversation")
async def conversation_endpoint(
    payload: EnvironmentalInput = Body(...)
) -> Dict[str, Any]:
    """
    Process a conversational environmental query.
    """

    session_id = payload.session_id or "default"
    query = payload.query or ""

    # ConversationService expects positional arguments.
    result = conversation_service.process_message(
        session_id,
        query,
    )

    return {
        "session_id": result.get("session_id", session_id),
        "requires_clarification": (
            result.get("status") == "needs_clarification"
        ),

        "profile": result.get("profile", {}),
        "environmental_profile": result.get("profile", {}),

        "interconnected_variables": result.get(
            "active_variables",
            [],
        ),

        "variable_connections": result.get(
            "variable_connections",
            [],
        ),

        "recommendations": result.get(
            "recommendations",
            [],
        ),

        "is_what_if": result.get(
            "is_what_if",
            False,
        ),

        "intervention": result.get(
            "intervention",
        ),

        "clarification_questions": result.get(
            "clarification",
            [],
        ),

        "system_notes": result.get(
            "message",
            "",
        ),
    }


@router.delete("/conversation/{session_id}")
async def reset_conversation(session_id: str) -> Dict[str, Any]:
    """
    Clear the stored conversation state for a session.
    """

    conversation_service.clear(session_id)

    return {
        "session_id": session_id,
        "cleared": True,
    }