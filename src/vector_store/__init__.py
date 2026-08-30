from typing import Dict, Any
from .base import VectorStoreInterface

def create_vector_store(config: Dict[str, Any]) -> VectorStoreInterface:
    provider = config.get("vector_store", {}).get("provider", "chroma")
    
    if provider == "chroma":
        from .chroma_store import ChromaStore
        persist_dir = config.get("vector_store", {}).get("chroma", {}).get("persist_dir", "vector_db/chroma")
        collection_name = config.get("vector_store", {}).get("chroma", {}).get("collection_name", "mutual_funds")
        return ChromaStore(persist_dir=persist_dir, collection_name=collection_name)
    else:
        raise ValueError(f"Unknown vector store provider: {provider}")
