from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.retriever import Retriever


router = APIRouter()

# Create one retriever instance for the endpoint.
retriever = Retriever()


class KnowledgeQueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    metric_filter: Optional[str] = None


@router.post("/query")
async def query_knowledge(payload: KnowledgeQueryRequest) -> Dict[str, Any]:
    """
    Search the Cura.Earth environmental knowledge base.

    The actual Retriever API is:
        search(query, top_k=5, filters=None)
    """

    query = payload.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Knowledge query cannot be empty.",
        )

    # Build filters only when the frontend sends a metric filter.
    filters = None

    if payload.metric_filter:
        filters = {
            "metric": payload.metric_filter
        }

    try:
        results = retriever.search(
            query=query,
            top_k=payload.top_k,
            filters=filters,
        )

        # Retriever.search() is documented by the actual class
        # to return List[Dict[str, Any]].
        if results is None:
            results = []

        if not isinstance(results, list):
            results = list(results)

        return {
            "query": query,
            "top_k": payload.top_k,
            "results": results,
            "count": len(results),
        }

    except Exception as exc:
        print("KNOWLEDGE SEARCH ERROR:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail=f"Knowledge search failed: {str(exc)}",
        )