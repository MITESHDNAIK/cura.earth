from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from app.rag.vector_store import VectorStore


class DocumentIngestionPipeline:
    """
    Cura.Earth knowledge-document ingestion pipeline.

    Handles:
    - Markdown/text documents
    - Optional YAML-style frontmatter
    - Safe local chunking
    - Vector-store insertion

    This module intentionally does not import app.rag.chunking so that
    startup is not coupled to a particular chunking implementation.
    """

    def __init__(self) -> None:
        self.vector_store = VectorStore()

    # ------------------------------------------------------------------
    # FRONTMATTER
    # ------------------------------------------------------------------

    def parse_frontmatter(
        self,
        file_content: str,
    ) -> Tuple[Dict[str, str], str]:
        """
        Parse optional YAML-style frontmatter.

        Example:

        ---
        title: Agroforestry and Soil Carbon
        organization: FAO
        topic: soil_health
        year: 2025
        ---

        Document content...
        """

        content = file_content.strip()

        if not content.startswith("---"):
            return {}, content

        lines = content.splitlines()

        closing_index = None

        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            return {}, content

        metadata: Dict[str, str] = {}

        for line in lines[1:closing_index]:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            # Remove optional quotes.
            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in {"'", '"'}
            ):
                value = value[1:-1]

            if key:
                metadata[key] = value

        body = "\n".join(
            lines[closing_index + 1 :]
        ).strip()

        return metadata, body

    # ------------------------------------------------------------------
    # CHUNKING
    # ------------------------------------------------------------------

    def chunk_document(
        self,
        text: str,
        chunk_size: int = 1200,
        overlap: int = 200,
    ) -> List[str]:
        """
        Simple deterministic text chunker.

        We keep this implementation inside ingestion.py to avoid
        depending on the exact API of chunking.py.
        """

        text = text.strip()

        if not text:
            return []

        if overlap >= chunk_size:
            overlap = max(0, chunk_size // 5)

        chunks: List[str] = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(
                start + chunk_size,
                text_length,
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = max(
                start + 1,
                end - overlap,
            )

        return chunks

    # ------------------------------------------------------------------
    # SINGLE DOCUMENT
    # ------------------------------------------------------------------

    def ingest_document(
        self,
        file_path: str | Path,
    ) -> int:
        """
        Read and ingest one document.

        Returns:
            Number of chunks inserted.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Knowledge document not found: {path}"
            )

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        metadata, body = self.parse_frontmatter(content)

        if not body:
            return 0

        # --------------------------------------------------------------
        # Fallback metadata
        # --------------------------------------------------------------

        metadata.setdefault(
            "source_file",
            path.name,
        )

        metadata.setdefault(
            "title",
            path.stem.replace("_", " "),
        )

        chunks = self.chunk_document(body)

        if not chunks:
            return 0

        documents: List[str] = []
        metadatas: List[Dict[str, str]] = []

        for index, chunk in enumerate(chunks):

            chunk_metadata = dict(metadata)

            chunk_metadata["chunk_index"] = str(index)

            documents.append(chunk)
            metadatas.append(chunk_metadata)

        # --------------------------------------------------------------
        # Vector store
        # --------------------------------------------------------------

        self.vector_store.add_documents(
            documents=documents,
            metadatas=metadatas,
        )

        return len(documents)

    # ------------------------------------------------------------------
    # DIRECTORY
    # ------------------------------------------------------------------

    def ingest_directory(
        self,
        directory: str | Path,
    ) -> int:
        """
        Ingest every .md and .txt document in a directory.
        """

        directory_path = Path(directory)

        if not directory_path.exists():
            raise FileNotFoundError(
                f"Knowledge directory not found: "
                f"{directory_path}"
            )

        files = sorted(
            [
                *directory_path.glob("*.md"),
                *directory_path.glob("*.txt"),
            ]
        )

        total_chunks = 0

        for file_path in files:

            try:

                count = self.ingest_document(
                    file_path
                )

                total_chunks += count

                print(
                    f"Indexed {file_path.name}: "
                    f"{count} chunks"
                )

            except Exception as exc:

                print(
                    f"Warning: failed to ingest "
                    f"{file_path.name}: {exc}"
                )

        return total_chunks


# ----------------------------------------------------------------------
# APPLICATION SINGLETON
# ----------------------------------------------------------------------

ingestion_pipeline = DocumentIngestionPipeline()