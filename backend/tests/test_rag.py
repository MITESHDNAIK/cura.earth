"""
Tests for Knowledge Retrieval Layer (RAG)
"""

from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store
from app.rag.retriever import retriever


def test_embedding_generation():
    text = "Legume cover crops fix atmospheric nitrogen"
    emb = embedding_service.get_embedding(text)
    assert isinstance(emb, list)
    assert len(emb) == embedding_service.dimension


def test_vector_store_indexing_and_retrieval():
    test_content = "Soil organic carbon increases significantly under conservation tillage and agroforestry."
    emb = embedding_service.get_embedding(test_content)
    
    vector_store.add_document(
        doc_id="doc_test_1",
        content=test_content,
        metadata={"source": "FAO", "year": 2022},
        embedding=emb
    )

    results = retriever.retrieve("soil organic carbon and tillage", top_k=1)
    assert len(results) > 0
    assert results[0]["metadata"]["source"] == "FAO"
