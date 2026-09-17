"""
Tests for What-If Ecology Simulator
"""

from app.simulator.ecology_sim import ecology_simulator
from app.core.schema import SimulationPerturbation


def test_ecology_simulation_timeframe():
    response = ecology_simulator.simulate(
        scenario_key="semi_arid_monoculture_agroforestry",
        timeframe_years=5
    )

    assert response.timeframe_years == 5
    assert len(response.yearly_projections) == 5
    
    # Year 5 SOC should be strictly greater than baseline SOC
    baseline_soc = response.baseline_metrics["soil_organic_carbon"]
    year5_soc = response.yearly_projections[-1].projected_metrics["soil_organic_carbon"]
    assert year5_soc > baseline_soc


def test_simulation_perturbation_influence():
    # Run with positive perturbation on SOC
    perturbations = [SimulationPerturbation(variable_name="soil_organic_carbon", delta_percentage=20.0)]
    resp_perturbed = ecology_simulator.simulate(
        scenario_key="semi_arid_monoculture_agroforestry",
        timeframe_years=3,
        perturbations=perturbations
    )
    
    resp_normal = ecology_simulator.simulate(
        scenario_key="semi_arid_monoculture_agroforestry",
        timeframe_years=3
    )

    perturbed_y3 = resp_perturbed.yearly_projections[-1].projected_metrics["soil_organic_carbon"]
    normal_y3 = resp_normal.yearly_projections[-1].projected_metrics["soil_organic_carbon"]

    assert perturbed_y3 > normal_y3
