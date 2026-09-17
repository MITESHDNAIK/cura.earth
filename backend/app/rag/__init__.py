"""
Cura.Earth RAG package.

Imports are intentionally kept lightweight here to avoid circular
dependencies during FastAPI startup.
"""

from .retriever import Retriever, retriever
from .service import KnowledgeService, knowledge_service

__all__ = [
    "Retriever",
    "retriever",
    "KnowledgeService",
    "knowledge_service",
]