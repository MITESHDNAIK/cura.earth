from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

import chromadb

from app.config import settings


class VectorStore:
    """
    Persistent ChromaDB wrapper used by Cura.Earth RAG.

    Provides a stable interface for:
    - adding documents
    - querying documents
    - deleting documents
    - counting indexed chunks
    """

    COLLECTION_NAME = "curaearth_knowledge"

    def __init__(self) -> None:
        persist_directory = PathLike(settings.CHROMA_PERSIST_DIRECTORY)

        try:
            self.client = chromadb.PersistentClient(
                path=str(persist_directory)
            )
        except Exception:
            # Safe fallback for environments where the configured
            # persistence directory cannot be created/accessed.
            self.client = chromadb.EphemeralClient()

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    # ---------------------------------------------------------
    # ADD DOCUMENTS
    # ---------------------------------------------------------

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        """
        Add document chunks to ChromaDB.

        Chroma requires explicit IDs. We generate deterministic
        SHA256 IDs when IDs are not supplied.
        """

        if not documents:
            return

        if metadatas is None:
            metadatas = [{} for _ in documents]

        if len(metadatas) != len(documents):
            raise ValueError(
                "documents and metadatas must have the same length"
            )

        if ids is None:
            ids = [
                hashlib.sha256(
                    document.encode("utf-8")
                ).hexdigest()
                for document in documents
            ]

        if len(ids) != len(documents):
            raise ValueError(
                "documents and ids must have the same length"
            )

        # Chroma metadata values must be primitive types.
        clean_metadatas = [
            self._clean_metadata(metadata)
            for metadata in metadatas
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=clean_metadatas,
        )

    # ---------------------------------------------------------
    # QUERY
    # ---------------------------------------------------------

    def query(
        self,
        query_embeddings: Optional[List[List[float]]] = None,
        query_texts: Optional[List[str]] = None,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Query the Chroma collection using either embeddings
        or raw text.
        """

        kwargs: Dict[str, Any] = {
            "n_results": n_results,
        }

        if query_embeddings is not None:
            kwargs["query_embeddings"] = query_embeddings

        elif query_texts is not None:
            kwargs["query_texts"] = query_texts

        else:
            raise ValueError(
                "Either query_embeddings or query_texts must be provided"
            )

        if where:
            kwargs["where"] = where

        return self.collection.query(**kwargs)

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:

        kwargs: Dict[str, Any] = {}

        if ids:
            kwargs["ids"] = ids

        if where:
            kwargs["where"] = where

        if limit is not None:
            kwargs["limit"] = limit

        return self.collection.get(**kwargs)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
    ) -> None:

        kwargs: Dict[str, Any] = {}

        if ids:
            kwargs["ids"] = ids

        if where:
            kwargs["where"] = where

        if kwargs:
            self.collection.delete(**kwargs)

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    def count(self) -> int:
        return self.collection.count()

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Delete and recreate the Cura.Earth knowledge collection.
        """

        try:
            self.client.delete_collection(
                name=self.COLLECTION_NAME
            )
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    # ---------------------------------------------------------
    # METADATA CLEANING
    # ---------------------------------------------------------

    @staticmethod
    def _clean_metadata(
        metadata: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:

        if not metadata:
            return {}

        cleaned: Dict[str, Any] = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(value, (str, int, float, bool)):
                cleaned[str(key)] = value

            else:
                cleaned[str(key)] = str(value)

        return cleaned


# -------------------------------------------------------------
# PATH HELPER
# -------------------------------------------------------------

class PathLike:
    """
    Small helper so the configured Chroma directory is safely
    converted into a Path and created when necessary.
    """

    def __init__(self, value: Any):
        from pathlib import Path

        self.path = Path(str(value))
        self.path.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        return str(self.path)