from typing import Dict, Any
from .base import VectorStoreInterface

def create_vector_store(config: Dict[str, Any]) -> VectorStoreInterface:
    provider = config.get("vector_store", {}).get("provider", "chroma")
    
    if provider == "chroma":
        from .chroma_store import ChromaStore
        persist_dir = config.get("vector_store", {}).get("chroma", {}).get("persist_dir", "vector_db/chroma")
        collection_name = config.get("vector_store", {}).get("chroma", {}).get("collection_name", "mutual_funds")
        return ChromaStore(persist_dir=persist_dir, collection_name=collection_name)
    elif provider == "faiss":
        from .faiss_store import FaissStore
        index_dir = config.get("vector_store", {}).get("faiss", {}).get("index_dir", "vector_db/faiss")
        index_type = config.get("vector_store", {}).get("faiss", {}).get("index_type", "FlatIP")
        # Ensure we read the dimension correctly based on the configured embedder
        emb_provider = config.get("embedder", {}).get("provider", "gemini")
        dimension = 768 # Gemini default
        if emb_provider == "sentence_transformer":
            dimension = 384 # all-MiniLM-L6-v2 default
        return FaissStore(index_dir=index_dir, dimension=dimension, index_type=index_type)
    else:
        raise ValueError(f"Unknown vector store provider: {provider}")
