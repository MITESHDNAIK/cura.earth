"""
Tests for Evidence-Backed Recommendation Engine
Validates scientific citations, measurable improvement estimates, and required fields.
"""

from app.core.schema import EnvironmentalInput, SoilMetrics, ClimateMetrics, LandUseMetrics
from app.recommendations.engine import recommendation_engine


def test_recommendations_contain_mandatory_scientific_evidence():
    env_input = EnvironmentalInput(
        soil=SoilMetrics(organic_carbon_pct=0.3),
        climate=ClimateMetrics(rainfall_category="low"),
        land_use=LandUseMetrics(crop_type="monoculture wheat")
    )
    
    recs = recommendation_engine.generate_recommendations(env_input, ["soil_organic_carbon", "water_retention_capacity", "crop_diversity"])
    
    assert len(recs) > 0
    top_rec = recs[0]

    # Mandatory output quality criteria from challenge document:
    # 1. What to do (action)
    assert len(top_rec.action) > 10
    # 2. Why it works (scientific reasoning)
    assert len(top_rec.scientific_reasoning) > 20
    # 3. Which environmental metric improves (impacted_metrics)
    assert len(top_rec.impacted_metrics) >= 2
    # 4. Measurable improvement estimates
    assert "%" in top_rec.measurable_improvements or "year" in top_rec.measurable_improvements
    # 5. Reference to a study/report/model (FAO/IPCC/etc.)
    assert len(top_rec.evidence) > 0
    sources = [e.source_organization for e in top_rec.evidence]
    assert any("FAO" in s or "IPCC" in s or "IPBES" in s for s in sources)
