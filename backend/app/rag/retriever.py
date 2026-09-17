from typing import Any, Dict, List, Optional

from app.rag.vector_store import VectorStore


class Retriever:
    """
    Cura.Earth semantic retrieval layer.

    Public API:
        search(query, top_k=5, filters=None)
    """

    def __init__(self):
        self.vector_store = VectorStore()

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base using Chroma's query_texts interface.
        """

        if not query or not query.strip():
            return []

        query = query.strip()

        # Convert optional application filters to Chroma `where`.
        where = None

        if filters:
            valid_filters = {
                key: value
                for key, value in filters.items()
                if value is not None and value != ""
            }

            if valid_filters:
                if len(valid_filters) == 1:
                    key, value = next(iter(valid_filters.items()))
                    where = {key: value}
                else:
                    where = {
                        "$and": [
                            {key: value}
                            for key, value in valid_filters.items()
                        ]
                    }

        # IMPORTANT:
        # Your actual VectorStore API is:
        #
        # query(
        #     query_embeddings=None,
        #     query_texts=None,
        #     n_results=5,
        #     where=None
        # )
        #
        # Therefore we MUST use query_texts here.

        raw_results = self.vector_store.query(
            query_texts=[query],
            n_results=top_k,
            where=where,
        )

        if not raw_results:
            return []

        documents = raw_results.get("documents") or []
        metadatas = raw_results.get("metadatas") or []
        distances = raw_results.get("distances") or []
        ids = raw_results.get("ids") or []

        # Chroma returns nested arrays for a batch query.
        if documents and isinstance(documents[0], list):
            documents = documents[0]

        if metadatas and isinstance(metadatas[0], list):
            metadatas = metadatas[0]

        if distances and isinstance(distances[0], list):
            distances = distances[0]

        if ids and isinstance(ids[0], list):
            ids = ids[0]

        results: List[Dict[str, Any]] = []

        for index, document in enumerate(documents):
            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            document_id = (
                ids[index]
                if index < len(ids)
                else None
            )

            # Convert distance to a simple relevance score.
            # Chroma distance is lower = more similar.
            score = None

            if isinstance(distance, (int, float)):
                score = 1.0 / (1.0 + float(distance))

            results.append(
                {
                    "id": document_id,
                    "doc_id": document_id,
                    "content": document,
                    "document": document,
                    "metadata": metadata or {},
                    "distance": distance,
                    "score": score,
                }
            )

        return results


# Backwards compatibility:
# app/rag/__init__.py currently imports both Retriever and retriever.
retriever = Retriever()