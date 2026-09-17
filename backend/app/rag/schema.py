"""
Pydantic models for the RAG Knowledge System.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class DocumentMetadata(BaseModel):
    source: str = Field(..., description="Original source identifier, e.g., filename or URL.")
    title: str = Field(..., description="Document title.")
    year: int = Field(..., description="Publication or creation year.")
    organization: str = Field(..., description="Organization responsible for the document.")
    topic: str = Field(..., description="Broad topic category.")
    environmental_metrics: List[str] = Field(..., description="List of environmental metric names covered.")
    intervention: str = Field(..., description="Proposed or described intervention.")
    url: Optional[str] = Field(None, description="Link to original document if available.")

class EvidenceChunk(BaseModel):
    chunk_id: str = Field(..., description="Unique identifier for the chunk.")
    doc_id: str = Field(..., description="Identifier of the parent document.")
    content: str = Field(..., description="Chunk text content.")
    metadata: DocumentMetadata = Field(..., description="Metadata inherited from the document.")
    relevance_score: Optional[float] = Field(None, description="Similarity score returned by retrieval.")

class RetrievalFilter(BaseModel):
    organization: Optional[str] = None
    topic: Optional[str] = None
    intervention: Optional[str] = None
    year: Optional[int] = None
