from typing import Dict, Any
from .base import EmbedderInterface

def create_embedder(config: Dict[str, Any]) -> EmbedderInterface:
    provider = config.get("embedder", {}).get("provider", "gemini")
    
    if provider == "gemini":
        from .gemini_embedder import GeminiEmbedder
        model = config.get("embedder", {}).get("gemini", {}).get("model", "gemini-embedding-2")
        batch_size = config.get("embedder", {}).get("gemini", {}).get("batch_size", 32)
        return GeminiEmbedder(model=model, batch_size=batch_size)
    else:
        raise ValueError(f"Unknown embedder provider: {provider}")
