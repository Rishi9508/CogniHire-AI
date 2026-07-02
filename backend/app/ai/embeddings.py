"""Embedding engine using SentenceTransformers all-MiniLM-L6-v2 (384-dim).

The model is loaded once at application startup and reused for all
encode operations. Embeddings are L2-normalized for direct cosine
similarity via dot product.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union


class EmbeddingEngine:
    """Wraps SentenceTransformer to produce 384-dim normalized embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, text: Union[str, List[str]]) -> np.ndarray:
        """Encode text(s) into normalized embedding vector(s).

        Args:
            text: A single string or list of strings.

        Returns:
            numpy array of shape (dim,) for single input or (n, dim) for list.
        """
        if isinstance(text, str):
            text = [text]
            single = True
        else:
            single = False

        embeddings = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        if single:
            return embeddings[0]
        return embeddings

    @staticmethod
    def to_bytes(embedding: np.ndarray) -> bytes:
        """Serialize a numpy embedding to bytes for BLOB storage."""
        return embedding.astype(np.float32).tobytes()

    @staticmethod
    def from_bytes(data: bytes, dimension: int = 384) -> np.ndarray:
        """Deserialize bytes back to a numpy embedding."""
        return np.frombuffer(data, dtype=np.float32).copy()

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two L2-normalized vectors.

        Since vectors are already normalized, this is just the dot product.
        """
        score = float(np.dot(a, b))
        return max(0.0, min(1.0, score))
