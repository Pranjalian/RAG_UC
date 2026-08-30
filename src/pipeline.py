import dataclasses
from typing import Dict, Any

from src.scraper.scraper import Scraper
from src.normalizer.normalizer import Normalizer
from src.change_detector.detector import ChangeDetector
from src.chunker.chunker import create_chunker
from src.embedder import create_embedder
from src.vector_store import create_vector_store
from src.vector_store.base import VectorItem
from src.logger import setup_logger

class IngestionPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = setup_logger("pipeline", config)
        
        self.scraper = Scraper(config.get("scraper", {}))
        self.normalizer = Normalizer(config.get("normalizer", {}))
        self.detector = ChangeDetector(config.get("change_detector", {}))
        
        self.chunking_fn = create_chunker(config)
        self.embedder = create_embedder(config)
        self.vector_store = create_vector_store(config)
        
    def run(self):
        self.logger.info("Starting ingestion pipeline...")
        
        results = self.scraper.scrape_all()
        
        total_chunks_upserted = 0
        
        for res in results:
            if not res.success:
                self.logger.warning(f"Skipping {res.fund_name} due to scrape failure.")
                continue
                
            raw_data = dataclasses.asdict(res)
            normalized = self.normalizer.normalize_fund(raw_data)
            self.normalizer.persist_normalized(normalized)
            
            fund_dict = dataclasses.asdict(normalized)
            
            manifest, current_hashes = self.detector.detect_changes(normalized)
            
            changed_sections = [sec for sec, status in manifest.items() if status == "changed"]
            
            if not changed_sections:
                self.logger.info(f"[{res.fund_name}] No changes detected. Skipping chunking/embedding.")
                continue
                
            self.logger.info(f"[{res.fund_name}] Changed sections: {changed_sections}")
            
            # Chunking
            chunks = self.chunking_fn(fund_dict, changed_sections, self.config)
            self.logger.info(f"[{res.fund_name}] Created {len(chunks)} chunks.")
            
            if chunks:
                # Embedding
                texts = [chunk.text for chunk in chunks]
                self.logger.info(f"[{res.fund_name}] Generating embeddings for {len(texts)} chunks...")
                embeddings = self.embedder.embed(texts)
                
                # Upsert to Vector Store
                vector_items = []
                for i, chunk in enumerate(chunks):
                    metadata = dataclasses.asdict(chunk)
                    # Don't store the full text inside metadata if we also store it natively in the DB, 
                    # but Chroma supports metadatas, we'll keep minimal metadata.
                    metadata.pop("text", None)
                    metadata.pop("vector", None)
                    
                    vector_items.append(VectorItem(
                        id=chunk.chunk_id,
                        vector=embeddings[i],
                        metadata=metadata,
                        text=chunk.text
                    ))
                    
                self.vector_store.upsert(vector_items)
                total_chunks_upserted += len(vector_items)
                self.logger.info(f"[{res.fund_name}] Upserted {len(vector_items)} chunks to vector store.")
            
            # Save new hashes ONLY after successful upsert
            self.detector.save_hashes(normalized.fund_id, current_hashes)
            
        self.logger.info(f"Ingestion pipeline completed. Total chunks upserted: {total_chunks_upserted}")
        self.logger.info(f"Total items in vector store: {self.vector_store.count()}")

class QueryPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = setup_logger("pipeline.query", config)
        
        # Load components
        self.embedder = create_embedder(config)
        self.vector_store = create_vector_store(config)
        
        from src.retriever.retriever import Retriever
        self.retriever = Retriever(self.vector_store, self.embedder, config)
        
        from src.generator.generator import Generator
        import os
        api_key = os.getenv("GROQ_API_KEY")
        self.generator = Generator(api_key=api_key, config=config)

    def query(self, question: str) -> str:
        self.logger.info(f"Received query: {question}")
        
        # 1. Retrieve
        retrieved_chunks = self.retriever.retrieve(question)
        
        # 2. Generate
        answer = self.generator.generate(question, retrieved_chunks)
        
        return answer
