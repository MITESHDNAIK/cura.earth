from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class SoilMetrics(BaseModel):
    organic_carbon_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    ph: Optional[float] = Field(None, ge=0.0, le=14.0)
    moisture_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    texture: Optional[str] = None
    soil_health: Optional[Literal["healthy", "degraded"]] = None


class ClimateMetrics(BaseModel):
    rainfall_category: Optional[Literal["very_low", "low", "moderate", "high", "very_high"]] = None
    annual_rainfall_mm: Optional[float] = Field(None, ge=0.0)
    temperature_celsius: Optional[float] = None
    aridity_index: Optional[float] = None


class LandUseMetrics(BaseModel):
    current_cover: Optional[str] = None
    crop_type: Optional[str] = None
    tillage_practice: Optional[str] = None
    habitat_fragmentation: Optional[Literal["low", "medium", "high"]] = None
    management: Optional[str] = None
    crop_diversity: Optional[Literal["low", "medium", "high"]] = None


class BiodiversityMetrics(BaseModel):
    status: Optional[Literal["declining", "stable", "improving", "healthy"]] = None
    pollinator_status: Optional[Literal["declining", "stable", "improving", "healthy"]] = None
    species_richness: Optional[float] = None
    species_status: Optional[Literal["declining", "stable", "improving", "healthy"]] = None


class HumanImpactMetrics(BaseModel):
    pollution: Optional[bool] = None
    deforestation: Optional[bool] = None
    disturbance: Optional[bool] = None
    land_use_change: Optional[bool] = None


class SpatialContext(BaseModel):
    region: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    ecoregion_id: Optional[str] = None


class EnvironmentalInput(BaseModel):
    query: Optional[str] = None
    soil: Optional[SoilMetrics] = Field(default_factory=SoilMetrics)
    climate: Optional[ClimateMetrics] = Field(default_factory=ClimateMetrics)
    land_use: Optional[LandUseMetrics] = Field(default_factory=LandUseMetrics)
    biodiversity: Optional[BiodiversityMetrics] = Field(default_factory=BiodiversityMetrics)
    human_impact: Optional[HumanImpactMetrics] = Field(default_factory=HumanImpactMetrics)
    spatial: Optional[SpatialContext] = Field(default_factory=SpatialContext)
    session_id: Optional[str] = None


class ClarificationQuestion(BaseModel):
    field_key: str
    prompt_text: str
    recommended_options: Optional[List[str]] = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ScientificEvidence(BaseModel):
    title: str
    source_organization: str
    year: int
    url_or_doi: Optional[str] = None
    finding_summary: str


class VariableInterconnection(BaseModel):
    source_metric: str
    target_metric: str
    relationship_type: Literal["positive_feedback", "synergy", "tradeoff", "mitigation"]
    mechanism: str


class RecommendationItem(BaseModel):
    action: str
    scientific_reasoning: str
    impacted_metrics: List[str]
    measurable_improvements: str
    time_horizon: Literal["short_term", "medium_term", "long_term"]
    confidence_level: Literal["low", "medium", "high"]
    evidence: List[ScientificEvidence] = Field(default_factory=list)


class EnvironmentalReasoningResponse(BaseModel):
    session_id: str
    requires_clarification: bool = False
    clarification_questions: List[ClarificationQuestion] = Field(default_factory=list)
    interconnected_variables: List[str] = Field(default_factory=list)
    variable_connections: List[VariableInterconnection] = Field(default_factory=list)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    system_notes: Optional[str] = None


class SimulationPerturbation(BaseModel):
    variable_name: str
    delta_percentage: float


class YearlyMetricProjection(BaseModel):
    year: int
    projected_metrics: Dict[str, float]
    ecological_state: str


class SimulationResponse(BaseModel):
    scenario_name: str
    timeframe_years: int
    baseline_metrics: Dict[str, float]
    perturbations_applied: List[SimulationPerturbation]
    yearly_projections: List[YearlyMetricProjection]
    cascade_summary: str
    confidence_level: str
