import json
from pathlib import Path
from typing import List, Dict, Set


class InterventionEngine:
    """Condition-aware intervention catalogue and candidate generator."""

    def __init__(self, interventions_path: str | Path = None):
        path = interventions_path or Path(__file__).parent / "data" / "interventions.json"
        self.interventions_path = Path(path)
        with open(self.interventions_path, "r", encoding="utf-8") as f:
            self.interventions: Dict[str, Dict] = json.load(f)

    def get_applicable(self, target_vars: Set[str]) -> List[Dict]:
        candidates = []
        for key, data in self.interventions.items():
            overlap = set(data.get("affects", [])) & set(target_vars)
            if overlap:
                candidates.append({
                    "key": key,
                    "name": data.get("name", key.replace("_", " ").title()),
                    "affects": list(data.get("affects", [])),
                    "overlap": sorted(overlap),
                    "impact_factor": float(data.get("impact_factor", 0.0)),
                    "time_horizon": data.get("time_horizon", "medium_term"),
                    "description": data.get("description", ""),
                    "strengths": data.get("strengths", []),
                    "avoid_when": data.get("avoid_when", []),
                    "priority": int(data.get("priority", 3)),
                })
        return candidates

    def top_intervention(self, target_vars: Set[str]) -> Dict | None:
        candidates = self.get_applicable(target_vars)
        return max(candidates, key=lambda x: x["impact_factor"]) if candidates else None


intervention_engine = InterventionEngine()
