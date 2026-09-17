from typing import Optional, Dict, List, Any
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.schema import (
    SimulationResponse,
    SimulationPerturbation,
    YearlyMetricProjection,
)

from app.simulator.ecology_sim import ecology_simulator


router = APIRouter()


class SimulationRequest(BaseModel):
    scenario_key: str = "semi_arid_monoculture_agroforestry"
    timeframe_years: int = 5
    custom_baseline: Optional[Dict[str, float]] = None
    perturbations: Optional[List[SimulationPerturbation]] = None
    intervention: Optional[str] = None


@router.post(
    "/simulate",
    response_model=SimulationResponse
)
async def run_ecological_simulation(
    payload: SimulationRequest
) -> SimulationResponse:

    result = ecology_simulator.simulate(
        scenario_key=payload.scenario_key,
        timeframe_years=payload.timeframe_years,
        custom_baseline=payload.custom_baseline,
        perturbations=payload.perturbations,
        intervention=payload.intervention,
    )

    # Convert the new simulator format back into the
    # existing API response schema expected by the frontend.

    yearly_projections = []

    for item in result["trajectory"]:

        yearly_projections.append(
            YearlyMetricProjection(
                year=item["year"],
                projected_metrics=item["metrics"],
                ecological_state=(
                    "Ecosystem Regenerating & Stabilized"
                    if item["metrics"].get(
                        "soil_organic_carbon",
                        0
                    ) > 1.2
                    else (
                        "Transitional Recovery"
                        if item["metrics"].get(
                            "soil_organic_carbon",
                            0
                        ) > 0.6
                        else "Early Stage Bio-Remediation"
                    )
                ),
            )
        )

    return SimulationResponse(
        scenario_name=result["scenario_name"],
        timeframe_years=result["timeframe_years"],
        baseline_metrics=result["baseline"],
        perturbations_applied=(
            payload.perturbations or []
        ),
        yearly_projections=yearly_projections,
        cascade_summary=" ".join(
            result["cascade_summary"]
        ),
        confidence_level=result["confidence_level"],
    )