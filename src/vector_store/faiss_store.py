import os
import faiss
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
from .base import VectorStoreInterface, VectorItem, SearchResult

class FaissStore(VectorStoreInterface):
    def __init__(self, index_dir: str, dimension: int = 384, index_type: str = "FlatIP"):
        self.index_dir = index_dir
        self.index_path = os.path.join(index_dir, "index.faiss")
        self.meta_path = os.path.join(index_dir, "metadata.pkl")
        self.dimension = dimension
        self.index_type = index_type
        self.id_to_idx = {}
        self.idx_to_meta = {}
        self.idx_to_text = {}
        self.current_idx = 0
        
        os.makedirs(index_dir, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'rb') as f:
                data = pickle.load(f)
                self.id_to_idx = data.get('id_to_idx', {})
                self.idx_to_meta = data.get('idx_to_meta', {})
                self.idx_to_text = data.get('idx_to_text', {})
                self.current_idx = data.get('current_idx', 0)
        else:
            if self.index_type == "FlatIP":
                self.index = faiss.IndexFlatIP(self.dimension)
            else:
                self.index = faiss.IndexFlatL2(self.dimension)

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump({
                'id_to_idx': self.id_to_idx,
                'idx_to_meta': self.idx_to_meta,
                'idx_to_text': self.idx_to_text,
                'current_idx': self.current_idx
            }, f)

    def upsert(self, items: List[VectorItem]) -> None:
        if not items:
            return
            
        vectors = []
        for item in items:
            idx = self.current_idx
            self.id_to_idx[item.id] = idx
            self.idx_to_meta[idx] = item.metadata
            self.idx_to_text[idx] = item.text
            
            vectors.append(item.vector)
            self.current_idx += 1
            
        vec_np = np.array(vectors, dtype=np.float32)
        if self.index_type == "FlatIP":
            faiss.normalize_L2(vec_np)
        
        self.index.add(vec_np)
        self._save()

    def search(self, query_vector: List[float], top_k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        if self.index.ntotal == 0:
            return []
            
        q_vec = np.array([query_vector], dtype=np.float32)
        if self.index_type == "FlatIP":
            faiss.normalize_L2(q_vec)
            
        # search a larger space if filtering to ensure we get top_k
        k_to_search = min(top_k * 5, self.index.ntotal)
        scores, indices = self.index.search(q_vec, k_to_search) 
        
        results = []
        for i, idx in enumerate(indices[0]):
            idx = int(idx)
            if idx == -1 or idx not in self.idx_to_meta:
                continue
                
            meta = self.idx_to_meta[idx]
            
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if meta.get(k) != v:
                        match = False
                        break
                if not match:
                    continue
                    
            item_id = None
            for i_id, i_idx in self.id_to_idx.items():
                if i_idx == idx:
                    item_id = i_id
                    break
                    
            results.append(SearchResult(
                id=item_id,
                score=float(scores[0][i]),
                metadata=meta,
                text=self.idx_to_text[idx]
            ))
            
            if len(results) >= top_k:
                break
                
        return results

    def delete(self, ids: List[str]) -> None:
        for item_id in ids:
            if item_id in self.id_to_idx:
                idx = self.id_to_idx[item_id]
                del self.id_to_idx[item_id]
                if idx in self.idx_to_meta:
                    del self.idx_to_meta[idx]
                if idx in self.idx_to_text:
                    del self.idx_to_text[idx]
        self._save()

    def count(self) -> int:
        return len(self.id_to_idx)
