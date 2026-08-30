import logging
from typing import List, Dict, Any, Optional

from src.vector_store.base import VectorStoreInterface, SearchResult
from src.embedder.base import EmbedderInterface
from src.retriever.router import QueryRouter

logger = logging.getLogger("pipeline.retriever")

class Retriever:
    def __init__(
        self,
        vector_store: VectorStoreInterface,
        embedder: EmbedderInterface,
        config: Dict[str, Any]
    ):
        """
        Initialize the retriever.
        """
        self.vector_store = vector_store
        self.embedder = embedder
        
        retriever_cfg = config.get("retriever", {})
        self.top_k = retriever_cfg.get("top_k", 2)
        self.similarity_threshold = retriever_cfg.get("similarity_threshold", 0.65)
        
        self_query_cfg = retriever_cfg.get("self_query", {})
        self.self_query_enabled = self_query_cfg.get("enabled", False)
        
        self.router = None
        if self.self_query_enabled:
            import os
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                model = self_query_cfg.get("model", "openai/gpt-oss-120b")
                self.router = QueryRouter(api_key=api_key, model=model)
                logger.info(f"Self-Query routing enabled using model: {model}")
            else:
                logger.warning("GROQ_API_KEY not found in environment, disabling self-query routing.")

    def retrieve(self, query: str) -> List[SearchResult]:
        """
        Retrieve chunks relevant to the query.
        """
        # 1. Extract metadata filters via LLM router (if enabled)
        filters = {}
        if self.router:
            logger.info("Extracting metadata filters via Query Router...")
            filters = self.router.extract_filters(query)
            
        # 2. Embed the query string
        logger.info(f"Embedding query: '{query}'")
        query_vector = self.embedder.embed_query(query)
        
        # 3. Search the vector store with the filters
        # Support for passing 'where' filters to the vector store interface
        logger.info(f"Searching vector store (top_k={self.top_k}, threshold={self.similarity_threshold})...")
        
        search_args = {
            "query_vector": query_vector,
            "top_k": self.top_k
        }
        # Only add filters if not empty
        if filters:
            if len(filters) == 1:
                search_args["filter_metadata"] = filters
            else:
                # Chroma requires $and for multiple conditions
                search_args["filter_metadata"] = {"$and": [{k: v} for k, v in filters.items()]}
            
        raw_results = self.vector_store.search(**search_args)
        
        # 4. Apply threshold filtering
        results = [res for res in raw_results if res.score >= self.similarity_threshold]
        
        if len(results) < len(raw_results):
            logger.info(f"Filtered {len(raw_results) - len(results)} chunks below threshold {self.similarity_threshold}")
            
        logger.info(f"Retrieved {len(results)} chunks above the similarity threshold.")
        return results
