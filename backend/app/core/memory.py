"""
Conversational Memory & State Tracking for Multi-Turn Ecological Sessions
"""

from typing import Dict, List, Optional
from app.core.schema import EnvironmentalInput, ChatMessage


class SessionState:
    """
    Maintains ecological parameters and chat history accumulated across turns.
    """
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[ChatMessage] = []
        self.current_state: EnvironmentalInput = EnvironmentalInput()

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        self.messages.append(ChatMessage(role=role, content=content, metadata=metadata))

    def update_environmental_state(self, new_input: EnvironmentalInput):
        """
        Merges new environmental variables into the persistent session state.
        """
        # Merge Soil
        if new_input.soil:
            if new_input.soil.organic_carbon_pct is not None:
                self.current_state.soil.organic_carbon_pct = new_input.soil.organic_carbon_pct
            if new_input.soil.ph is not None:
                self.current_state.soil.ph = new_input.soil.ph
            if new_input.soil.moisture_pct is not None:
                self.current_state.soil.moisture_pct = new_input.soil.moisture_pct
            if new_input.soil.texture is not None:
                self.current_state.soil.texture = new_input.soil.texture

        # Merge Climate
        if new_input.climate:
            if new_input.climate.rainfall_category is not None:
                self.current_state.climate.rainfall_category = new_input.climate.rainfall_category
            if new_input.climate.annual_rainfall_mm is not None:
                self.current_state.climate.annual_rainfall_mm = new_input.climate.annual_rainfall_mm
            if new_input.climate.temperature_celsius is not None:
                self.current_state.climate.temperature_celsius = new_input.climate.temperature_celsius

        # Merge Land Use
        if new_input.land_use:
            if new_input.land_use.crop_type is not None:
                self.current_state.land_use.crop_type = new_input.land_use.crop_type
            if new_input.land_use.current_cover is not None:
                self.current_state.land_use.current_cover = new_input.land_use.current_cover
            if new_input.land_use.tillage_practice is not None:
                self.current_state.land_use.tillage_practice = new_input.land_use.tillage_practice

        # Merge Spatial
        if new_input.spatial:
            if new_input.spatial.region is not None:
                self.current_state.spatial.region = new_input.spatial.region
            if new_input.spatial.latitude is not None:
                self.current_state.spatial.latitude = new_input.spatial.latitude
            if new_input.spatial.longitude is not None:
                self.current_state.spatial.longitude = new_input.spatial.longitude


class MemoryStore:
    """
    In-memory registry of conversational sessions.
    """
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create_session(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)
        return self._sessions[session_id]

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]


session_memory = MemoryStore()
