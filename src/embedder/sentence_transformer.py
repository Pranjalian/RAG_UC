from typing import List
from sentence_transformers import SentenceTransformer
from .base import EmbedderInterface

class SentenceTransformerEmbedder(EmbedderInterface):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 32):
        self._model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size
        
    @property
    def model_name(self) -> str:
        return self._model_name
        
    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def embed_query(self, query: str) -> List[float]:
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, batch_size=self.batch_size, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]
