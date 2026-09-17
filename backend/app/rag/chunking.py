import re
from typing import List, Tuple

class Chunker:
    """Utility for splitting text into overlapping semantic chunks while attaching metadata.

    The implementation uses a simple word‑based sliding window. For production use you may replace
    this with a more sophisticated tokenizer or semantic splitter.
    """

    def __init__(self, chunk_size_words: int = 200, overlap_words: int = 50):
        self.chunk_size_words = chunk_size_words
        self.overlap_words = overlap_words

    def chunk_text(self, text: str, metadata: dict) -> List[Tuple[str, dict]]:
        """Split *text* into overlapping chunks.

        Returns a list of ``(chunk_text, merged_metadata)`` tuples. ``merged_metadata`` is a copy of the
        provided ``metadata`` dictionary with an additional ``"chunk_index"`` field.
        """
        # Normalise whitespace and split into words.
        words = re.findall(r"\S+", text)
        if not words:
            return []
        chunks: List[Tuple[str, dict]] = []
        start = 0
        idx = 0
        while start < len(words):
            end = min(start + self.chunk_size_words, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunk_meta = dict(metadata)  # shallow copy
            chunk_meta["chunk_index"] = idx
            chunks.append((chunk_text, chunk_meta))
            # Advance by chunk_size - overlap
            if end == len(words):
                break
            start = end - self.overlap_words
            idx += 1
        return chunks
