"""
Tests for Multi-Metric Reasoning Engine
Ensures at least 3 environmental variables are analyzed together.
"""

from app.core.schema import EnvironmentalInput, SoilMetrics, ClimateMetrics, LandUseMetrics
from app.reasoning.engine import reasoning_engine


def test_reasoning_combines_minimum_three_variables():
    env_input = EnvironmentalInput(
        soil=SoilMetrics(organic_carbon_pct=0.3, ph=7.2),
        climate=ClimateMetrics(rainfall_category="low"),
        land_use=LandUseMetrics(crop_type="monoculture wheat")
    )
    
    active_vars, active_rules = reasoning_engine.reason(env_input)

    # Core challenge constraint: Must handle at least 3 environmental variables together
    assert len(active_vars) >= 3
    assert "soil_organic_carbon" in active_vars
    assert len(active_rules) > 0


def test_reasoning_detects_biophysical_interconnections():
    env_input = EnvironmentalInput(
        soil=SoilMetrics(organic_carbon_pct=0.4),
        climate=ClimateMetrics(rainfall_category="low"),
        land_use=LandUseMetrics(crop_type="monoculture wheat")
    )
    
    _, active_rules = reasoning_engine.reason(env_input)
    mechanisms = [r.mechanism for r in active_rules]
    
    # Verify non-trivial scientific reasoning mechanism presence
    assert any("microbial" in m.lower() or "water" in m.lower() for m in mechanisms)
