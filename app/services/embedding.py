import hashlib
import math
from typing import Iterable, List

from app.config import EMBEDDING_MODEL_NAME


class EmbeddingModel:
    """Creates vectors from text.

    Portfolio mode uses a Hugging Face sentence-transformer model.
    Fallback mode uses a simple hashing vector so beginners can run the demo
    before installing ML dependencies.
    """

    def __init__(self) -> None:
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            self.name = EMBEDDING_MODEL_NAME
        except Exception:
            self.name = "fallback-hashing-embedding"

    def encode(self, texts: Iterable[str]) -> List[List[float]]:
        text_list = list(texts)
        if self._model is not None:
            vectors = self._model.encode(text_list, normalize_embeddings=True)
            return vectors.tolist()
        return [_hashing_embedding(text) for text in text_list]


def _hashing_embedding(text: str, dimensions: int = 128) -> List[float]:
    vector = [0.0] * dimensions
    words = [word.lower() for word in text.replace("\n", " ").split()]

    for word in words:
        digest = hashlib.md5(word.encode("utf-8")).hexdigest()
        index = int(digest, 16) % dimensions
        vector[index] += 1.0

    length = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / length for value in vector]

