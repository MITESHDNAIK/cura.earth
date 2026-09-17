import json
import os
from typing import Dict, List, Any

# Path to the metrics JSON (relative to this file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")

class ProfileBuilder:
    """Builds a validated environmental profile from raw metric values.

    The input ``raw_profile`` should be a dict mapping variable names (e.g., ``soil_health``) to
    a dict of metric values. Only metrics defined in ``metrics.json`` are accepted; unknown
    entries are ignored. Missing metrics are omitted from the resulting profile.
    """

    def __init__(self):
        self.metric_definitions = self._load_metrics()

    def _load_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def build(self, raw_profile: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Validate and return a clean profile.

        Returns a dict of the form ``{variable: {metric: value, ...}, ...}`` containing only
        metrics present in the definition file.
        """
        clean_profile: Dict[str, Dict[str, Any]] = {}
        for variable, metrics in raw_profile.items():
            if variable not in self.metric_definitions:
                continue  # unknown variable
            defined_metrics = {m["metric"] for m in self.metric_definitions[variable]}
            filtered = {k: v for k, v in metrics.items() if k in defined_metrics}
            if filtered:
                clean_profile[variable] = filtered
        return clean_profile
