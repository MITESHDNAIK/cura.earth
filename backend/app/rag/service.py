from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.rag.retriever import Retriever


class KnowledgeService:
    """
    High-level RAG knowledge service.

    Keeps retrieval behind a small, stable interface so API endpoints,
    recommendation logic, and ingestion code do not depend directly
    on ChromaDB internals.
    """

    def __init__(self) -> None:
        self.retriever = Retriever()

    def query(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge chunks.

        Returns normalized dictionaries so downstream code can safely
        consume the result regardless of the underlying vector-store format.
        """
        if not query or not query.strip():
            return []

        try:
            results = self.retriever.search(
                query=query,
                top_k=top_k,
                filters=filters,
            )
        except TypeError:
            # Backward compatibility with retrievers that don't accept
            # filters as a keyword argument.
            results = self.retriever.search(
                query=query,
                top_k=top_k,
            )

        if results is None:
            return []

        normalized: List[Dict[str, Any]] = []

        for item in results:
            if isinstance(item, dict):
                normalized.append(item)
            else:
                normalized.append(
                    {
                        "content": str(item),
                        "metadata": {},
                    }
                )

        return normalized


# Singleton used throughout the application.
knowledge_service = KnowledgeService()