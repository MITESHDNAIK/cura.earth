import json
import os
from pathlib import Path
from typing import List, Dict, Set

class RelationshipEngine:
    """Load structured environmental knowledge and expose relationship queries.

    The knowledge file (environmental_knowledge.json) follows the schema:
    ```json
    {
      "entities": ["soil_health", "land_use", ...],
      "relationships": [
        {"from": "soil_health", "to": "biodiversity", "type": "supports", "evidence": ["chunk_001"]},
        ...
      ]
    }
    ```
    This engine builds a mapping of each entity to the set of directly related entities
    based on the ``relationships`` list.
    """

    def __init__(self, knowledge_path: str | Path = None):
        if knowledge_path is None:
            knowledge_path = Path(__file__).parent / "data" / "environmental_knowledge.json"
        self.knowledge_path = Path(knowledge_path)
        self._load_knowledge()
        self._build_index()

    def _load_knowledge(self) -> None:
        if not self.knowledge_path.is_file():
            raise FileNotFoundError(f"Environmental knowledge file not found: {self.knowledge_path}")
        with open(self.knowledge_path, "r", encoding="utf-8") as f:
            self.raw = json.load(f)

    def _build_index(self) -> None:
        """Create a dict ``entity -> set(related_entities)`` from the raw relationships."""
        self.index: Dict[str, Set[str]] = {entity: set() for entity in self.raw.get("entities", [])}
        for rel in self.raw.get("relationships", []):
            src = rel.get("from")
            dst = rel.get("to")
            if src and dst:
                self.index.setdefault(src, set()).add(dst)
                self.index.setdefault(dst, set()).add(src)  # treat as undirected for convenience

    def get_related(self, var: str) -> Set[str]:
        """Return directly related variables for ``var`` (empty set if unknown)."""
        return self.index.get(var, set())

    def combine_relationships(self, variables: List[str]) -> Set[str]:
        """Union of the supplied variables and all their direct neighbours."""
        combined: Set[str] = set(variables)
        for v in variables:
            combined.update(self.get_related(v))
        return combined

    def validate_three_factor(self, variables: List[str]) -> bool:
        """Return ``True`` if at least three distinct variables are present."""
        return len(set(variables)) >= 3

    def related_relationships(self, variables: List[str]) -> List[Dict]:
        """Return the list of relationship dicts that involve any of the supplied variables.
        This is used to fetch supporting evidence IDs.
        """
        rels = []
        for rel in self.raw.get("relationships", []):
            if rel.get("from") in variables or rel.get("to") in variables:
                rels.append(rel)
        return rels

# Export a singleton for convenient import elsewhere
relationship_engine = RelationshipEngine()
