from typing import List, Protocol

class EmbedderInterface(Protocol):
    @property
    def model_name(self) -> str:
        ...
        
    @property
    def dimension(self) -> int:
        ...

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text chunks."""
        ...

    def embed_query(self, query: str) -> List[float]:
        """Embed a single search query."""
        ...
