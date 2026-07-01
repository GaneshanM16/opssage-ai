import math
from dataclasses import dataclass
from typing import List

from app.services.document_loader import Document


@dataclass
class SearchResult:
    document: Document
    score: float


class VectorStore:
    """Stores document vectors and returns the closest documents."""

    def __init__(self, documents: List[Document], vectors: List[List[float]]) -> None:
        self.documents = documents
        self.vectors = vectors
        self._faiss_index = None

        try:
            import faiss
            import numpy as np

            matrix = np.array(vectors, dtype="float32")
            index = faiss.IndexFlatIP(matrix.shape[1])
            index.add(matrix)
            self._faiss_index = index
        except Exception:
            self._faiss_index = None

    def search(self, query_vector: List[float], top_k: int) -> List[SearchResult]:
        if not self.documents:
            return []

        if self._faiss_index is not None:
            return self._search_with_faiss(query_vector, top_k)

        scored = [
            SearchResult(document=document, score=_cosine_similarity(query_vector, vector))
            for document, vector in zip(self.documents, self.vectors)
        ]
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

    def _search_with_faiss(self, query_vector: List[float], top_k: int) -> List[SearchResult]:
        import numpy as np

        query = np.array([query_vector], dtype="float32")
        scores, indexes = self._faiss_index.search(query, top_k)
        results: List[SearchResult] = []

        for score, index in zip(scores[0], indexes[0]):
            if index == -1:
                continue
            results.append(
                SearchResult(document=self.documents[int(index)], score=float(score))
            )

        return results


def _cosine_similarity(left: List[float], right: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(left, right))
    left_length = math.sqrt(sum(a * a for a in left)) or 1.0
    right_length = math.sqrt(sum(b * b for b in right)) or 1.0
    return dot_product / (left_length * right_length)

