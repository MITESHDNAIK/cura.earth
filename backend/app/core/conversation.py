from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class ConversationState:
    conversation_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    environmental_profile: Dict[str, Any] = field(default_factory=dict)
    intervention: str | None = None

class ConversationMemory:
    def __init__(self):
        self._sessions: Dict[str, ConversationState] = {}
    def get_or_create(self, conversation_id: str) -> ConversationState:
        if conversation_id not in self._sessions:
            self._sessions[conversation_id] = ConversationState(conversation_id=conversation_id)
        return self._sessions[conversation_id]
    def get(self, conversation_id: str):
        return self._sessions.get(conversation_id)
    def clear(self, conversation_id: str):
        self._sessions.pop(conversation_id, None)
