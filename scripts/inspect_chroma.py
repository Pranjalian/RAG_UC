import sys
import os

# Add project root to PYTHONPATH so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config_loader import load_config
from src.vector_store import create_vector_store

def main():
    print("Loading configuration...")
    config = load_config()
    
    print("Connecting to Vector Store (ChromaDB)...")
    store = create_vector_store(config)
    
    # Check total count
    count = store.count()
    print(f"\n[SUCCESS] Total items in ChromaDB: {count}")
    
    if count == 0:
        print("The database is empty. Did you run `python src/main.py ingest`?")
        return
        
    print("\n--- Inspecting first 3 chunks from ChromaDB ---")
    
    # We can peek at the data by querying the collection directly since our interface 
    # abstracts it, but the underlying object is a chromadb collection.
    if hasattr(store, "collection"):
        results = store.collection.peek(limit=3)
        
        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])
        documents = results.get("documents", [])
        
        for i in range(len(ids)):
            print(f"\n[{i+1}] ID: {ids[i]}")
            print(f"Metadata: {metadatas[i]}")
            
            doc_preview = documents[i][:200].replace('\n', ' ')
            if len(documents[i]) > 200:
                doc_preview += "..."
            print(f"Document Preview: {doc_preview}")
            
    print("\n" + "-"*50)
    print("To view specific funds, we need to do a semantic search, which requires generating an embedding first.")

if __name__ == "__main__":
    main()
