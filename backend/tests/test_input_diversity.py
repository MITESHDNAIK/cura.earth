"""Manual/CI smoke suite for Cura.Earth input diversity.
Run: PYTHONPATH=. python tests/test_input_diversity.py
"""
from app.core.schema import EnvironmentalInput
from app.reasoning.engine import reasoning_engine
from app.recommendations.engine import recommendation_engine
from app.reasoning.extractor import extract_environmental_profile
from app.reasoning.conversation_service import ConversationService

CASES = [
    ("json_agro", {"soil":{"organic_carbon_pct":0.3},"climate":{"rainfall_category":"low"},"land_use":{"crop_type":"wheat","current_cover":"monoculture"}}, "Agroforestry / tree-crop integration"),
    ("json_cover", {"soil":{"organic_carbon_pct":0.5,"moisture_pct":8},"climate":{"rainfall_category":"low"},"land_use":{"tillage_practice":"conventional","crop_type":"maize"}}, "Cover cropping with reduced soil disturbance"),
    ("json_hedge", {"soil":{"organic_carbon_pct":2.0},"climate":{"rainfall_category":"high"},"land_use":{"habitat_fragmentation":"high","crop_diversity":"high"},"biodiversity":{"pollinator_status":"declining"}}, "Native flowering hedgerows / habitat corridors"),
    ("json_ph", {"soil":{"ph":4.8,"organic_carbon_pct":1.0},"climate":{"rainfall_category":"moderate"},"land_use":{"crop_type":"maize"}}, "Targeted soil pH management"),
    ("human", {"soil":{"organic_carbon_pct":1.5},"climate":{"rainfall_category":"high"},"land_use":{"crop_type":"rice"},"biodiversity":{"pollinator_status":"declining"}}, "Native flowering hedgerows / habitat corridors"),
]

TEXT_CASES = [
    ("text_agro", "Biodiversity is declining on my wheat farm. SOC 0.3%, rainfall is low, monoculture."),
    ("text_cover", "My soil moisture is 8%, the soil is degraded, and I use conventional tillage."),
    ("text_hedge", "Healthy soil but biodiversity declining. Pollinators have disappeared and the habitat is highly fragmented."),
    ("text_legume", "I grow wheat every year as a monoculture. Soil carbon is 0.6%."),
    ("text_ph", "My soil pH is 4.8, SOC is 1.0%, and rainfall is moderate. I grow maize."),
]

def check_env(env, label):
    active, connections = reasoning_engine.reason(env)
    recs = recommendation_engine.generate_recommendations(env, active, connections)
    return active, [r.action for r in recs]


def main():
    outputs = {}
    print("\nCURA.EARTH DIVERSITY TEST\n" + "="*32)
    for label, data, expected in CASES:
        env = EnvironmentalInput.model_validate({**data, "query": label, "session_id": label})
        active, recs = check_env(env, label)
        outputs[label] = recs
        ok = expected in recs
        print(f"{label:12} {'PASS' if ok else 'FAIL'} | active={len(active)} | {recs}")
        assert ok, f"{label}: expected {expected}, got {recs}"

    for label, text in TEXT_CASES:
        profile = extract_environmental_profile(text)
        env = EnvironmentalInput.model_validate({**profile, "query": text, "session_id": label})
        active, recs = check_env(env, label)
        outputs[label] = recs
        print(f"{label:12} OK   | active={len(active)} | {recs}")
        assert active or recs == [], f"{label}: extractor/reasoner crashed"

    # Memory isolation: different sessions must not inherit the previous profile.
    service = ConversationService()
    a = service.process_message("session-A", "SOC 0.3%, rainfall is low, wheat monoculture.")
    b = service.process_message("session-B", "My soil pH is 4.8, SOC is 1.2%, rainfall is moderate, and I grow maize.")
    assert "organic_carbon_pct" not in b["profile"].get("soil", {}) or b["profile"]["soil"]["organic_carbon_pct"] == 1.2
    assert b["profile"].get("climate", {}).get("rainfall_category") == "moderate"
    print("memory isolation PASS")

    unique = sorted({x for vals in outputs.values() for x in vals})
    print("\nUnique intervention outputs:", len(unique))
    print(" ->", " | ".join(unique))
    assert len(unique) >= 3, "Intervention diversity is too low"
    print("\nALL DIVERSITY CHECKS PASSED")

if __name__ == "__main__":
    main()
