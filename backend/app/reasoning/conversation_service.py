from typing import Any, Dict, Optional

from app.core.conversation import ConversationMemory
from app.core.schema import EnvironmentalInput
from app.reasoning.extractor import extract_environmental_profile
from app.reasoning.completeness import check_completeness
from app.reasoning.engine import reasoning_engine
from app.recommendations.engine import recommendation_engine


class ConversationService:
    """
    Stateful multi-turn environmental analysis.

    Each conversation_id owns an isolated environmental profile.
    Information from one conversation is never intentionally merged
    into another conversation.
    """

    def __init__(self):
        self.memory = ConversationMemory()

    # ============================================================
    # PROFILE MERGING
    # ============================================================

    @staticmethod
    def _deep_merge(
        existing: Dict[str, Any],
        incoming: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = dict(existing or {})

        for key, value in (incoming or {}).items():

            if value is None or value == "":
                continue

            if (
                isinstance(value, dict)
                and isinstance(result.get(key), dict)
            ):
                result[key] = ConversationService._deep_merge(
                    result[key],
                    value,
                )

            else:
                result[key] = value

        return result

    # ============================================================
    # EXTRACTION
    # ============================================================

    def _extract(self, message: str) -> Dict[str, Any]:

        data = extract_environmental_profile(message)

        if hasattr(data, "model_dump"):
            data = data.model_dump(exclude_none=True)

        return data if isinstance(data, dict) else {}

    # ============================================================
    # ENVIRONMENTAL INPUT
    # ============================================================

    @staticmethod
    def _to_environmental_input(
        profile: Dict[str, Any],
        session_id: str,
        query: str,
    ) -> EnvironmentalInput:

        payload = {
            "session_id": session_id,
            "query": query,
            **profile,
        }

        return EnvironmentalInput.model_validate(payload)

    # ============================================================
    # MAIN CONVERSATION FLOW
    # ============================================================

    def process_message(
        self,
        conversation_id: str,
        message: str,
    ) -> Dict[str, Any]:

        conversation_id = str(conversation_id or "default")
        message = (message or "").strip()

        state = self.memory.get_or_create(conversation_id)

        # Store user message
        state.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        # Extract only information explicitly present in this message.
        extracted = self._extract(message)

        # Merge it into the persistent profile for THIS conversation.
        state.environmental_profile = self._deep_merge(
            state.environmental_profile,
            extracted,
        )

        profile = state.environmental_profile

        # --------------------------------------------------------
        # Completeness
        # --------------------------------------------------------

        completeness = check_completeness(
            query=message,
            profile=profile,
        )

        is_what_if = completeness.get(
            "is_what_if",
            False,
        )

        intervention = self._extract_intervention(message)

        if intervention:
            state.intervention = intervention

        # --------------------------------------------------------
        # Clarification
        # --------------------------------------------------------

        if completeness.get("requires_clarification", False):

            return {
                "session_id": conversation_id,
                "status": "needs_clarification",

                # IMPORTANT:
                # Return the accumulated profile so the frontend
                # always knows the backend's actual state.
                "profile": profile,

                "active_variables": [],
                "variable_connections": [],
                "recommendations": [],

                "is_what_if": is_what_if,
                "intervention": state.intervention,

                "clarification": self._clarification_list(
                    completeness.get("clarification")
                ),

                "message": completeness.get(
                    "clarification",
                    "More environmental context is required.",
                ),
            }

        # --------------------------------------------------------
        # Scientific reasoning
        # --------------------------------------------------------

        env = self._to_environmental_input(
            profile,
            conversation_id,
            message,
        )

        active, connections = reasoning_engine.reason(env)

        recommendations = (
            recommendation_engine.generate_recommendations(
                env,
                active,
                connections,
            )
        )

        return {
            "session_id": conversation_id,
            "status": (
                "what_if_ready"
                if is_what_if
                else "ready_for_reasoning"
            ),

            # Backend source of truth
            "profile": profile,

            "active_variables": active,
            "variable_connections": connections,
            "recommendations": recommendations,

            "is_what_if": is_what_if,
            "intervention": state.intervention,

            "clarification": [],

            "message": (
                "Environmental system understood. Multi-metric "
                "reasoning and context-specific recommendations "
                "completed."
            ),
        }

    # ============================================================
    # CLARIFICATION
    # ============================================================

    @staticmethod
    def _clarification_list(
        text: Optional[str],
    ):

        if not text:
            return []

        return [
            {
                "field_key": "environmental_context",
                "prompt_text": text,
                "recommended_options": None,
            }
        ]

    # ============================================================
    # INTERVENTION DETECTION
    # ============================================================

    @staticmethod
    def _extract_intervention(
        message: str,
    ) -> Optional[str]:

        q = (message or "").lower()

        mappings = {
            "agroforestry": [
                "agroforestry",
                "trees between crops",
                "tree crop integration",
                "integrate trees",
                "introduce trees",
            ],

            "legume_intercropping": [
                "legume intercropping",
                "legume intercrop",
                "intercrop legumes",
                "intercropping",
                "legumes between",
            ],

            "cover_cropping": [
                "cover crop",
                "cover cropping",
                "cover crops",
            ],

            "native_hedgerows": [
                "hedgerow",
                "native hedgerow",
                "habitat corridor",
                "flowering corridor",
            ],
        }

        for key, phrases in mappings.items():

            if any(
                phrase in q
                for phrase in phrases
            ):
                return key

        return None

    # ============================================================
    # CLEAR SESSION
    # ============================================================

    def clear(
        self,
        conversation_id: str,
    ):
        self.memory.clear(conversation_id)


# Singleton used by the API.
conversation_service = ConversationService()