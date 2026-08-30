import os
import chromadb
from typing import List, Dict, Any, Optional
from chromadb.config import Settings
from .base import VectorStoreInterface, VectorItem, SearchResult

class ChromaStore(VectorStoreInterface):
    def __init__(self, persist_dir: str = "vector_db/chroma", collection_name: str = "mutual_funds"):
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, items: List[VectorItem]) -> None:
        if not items:
            return
            
        ids = [item.id for item in items]
        embeddings = [item.vector for item in items]
        metadatas = [item.metadata for item in items]
        documents = [item.text for item in items]
        
        # Chroma handles both insert and update with `upsert`
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def search(self, query_vector: List[float], top_k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        kwargs = {
            "query_embeddings": [query_vector],
            "n_results": top_k,
            "include": ["metadatas", "documents", "distances"]
        }
        
        if filter_metadata:
            kwargs["where"] = filter_metadata
            
        results = self.collection.query(**kwargs)
        
        search_results = []
        if results["ids"] and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                # Chroma returns distance, we want similarity score (1 - distance for cosine)
                # Note: Exact interpretation depends on space (cosine space in Chroma is cosine distance)
                distance = results["distances"][0][i]
                score = 1.0 - distance
                
                search_results.append(SearchResult(
                    id=results["ids"][0][i],
                    score=score,
                    metadata=results["metadatas"][0][i] or {},
                    text=results["documents"][0][i] or ""
                ))
                
        return search_results

    def delete(self, ids: List[str]) -> None:
        if not ids:
            return
        self.collection.delete(ids=ids)

    def count(self) -> int:
        return self.collection.count()
