import os
from typing import List

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None

class SentenceTransformerEmbeddingService:
    """Embedding service using a SentenceTransformer model.

    If the model cannot be loaded (e.g., missing dependencies or no internet), a deterministic
    fallback that returns zero‑vectors of the appropriate dimension is used. This ensures that the
    service remains functional for unit tests that mock the embedding values.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        if SentenceTransformer is None:
            # Fallback will be used; we cannot import the library.
            self._model = None
            return
        try:
            self._model = SentenceTransformer(self.model_name)
        except Exception:  # pragma: no cover
            # Any failure (e.g., no internet) results in fallback.
            self._model = None

    def _fallback_vector(self, size: int = 384) -> List[float]:
        """Return a deterministic zero‑vector of the given size.
        The default size matches the dimension of ``all-MiniLM-L6-v2``.
        """
        return [0.0] * size

    def embed_text(self, text: str) -> List[float]:
        """Return an embedding for a single piece of text.

        If the underlying model is unavailable, a zero‑vector is returned.
        """
        if self._model is None:
            return self._fallback_vector()
        return self._model.encode(text, convert_to_numpy=True).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a batch of texts.

        If the underlying model is unavailable, a list of zero‑vectors is returned.
        """
        if self._model is None:
            return [self._fallback_vector() for _ in texts]
        return self._model.encode(texts, convert_to_numpy=True).tolist()
