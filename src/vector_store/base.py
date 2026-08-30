from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Protocol

@dataclass
class VectorItem:
    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    text: str

@dataclass
class SearchResult:
    id: str
    score: float
    metadata: Dict[str, Any]
    text: str

class VectorStoreInterface(Protocol):
    def upsert(self, items: List[VectorItem]) -> None:
        """Insert or update items in the vector store."""
        ...

    def search(self, query_vector: List[float], top_k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search the vector store for nearest neighbors."""
        ...

    def delete(self, ids: List[str]) -> None:
        """Delete items by ID."""
        ...

    def count(self) -> int:
        """Return the number of items in the store."""
        ...
