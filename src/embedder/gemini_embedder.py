import os
import google.generativeai as genai
from typing import List
from .base import EmbedderInterface

class GeminiEmbedder(EmbedderInterface):
    def __init__(self, model: str = "models/gemini-embedding-2", batch_size: int = 32):
        self._model_name = model if model.startswith("models/") else f"models/{model}"
        self.batch_size = batch_size
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        genai.configure(api_key=api_key)
        
    @property
    def model_name(self) -> str:
        return self._model_name
        
    @property
    def dimension(self) -> int:
        return 768  # text-embedding-004 dimension

    def embed(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i+self.batch_size]
            
            # Using specific task type for document embedding
            result = genai.embed_content(
                model=self._model_name,
                content=batch,
                task_type="retrieval_document"
            )
            all_embeddings.extend(result["embedding"])
            
        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        result = genai.embed_content(
            model=self._model_name,
            content=query,
            task_type="retrieval_query"
        )
        return result["embedding"]
