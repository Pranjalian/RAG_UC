import json
from typing import Dict, Any, List
from .chunker import Chunk

def fixed_size_chunking(fund_data: Dict[str, Any], changed_sections: List[str], config: Dict[str, Any]) -> List[Chunk]:
    """
    Alternative chunking strategy that dumps the JSON to a string and splits it by fixed sizes.
    """
    chunk_size = config.get("chunker", {}).get("fixed_size", {}).get("chunk_size", 500)
    chunk_overlap = config.get("chunker", {}).get("fixed_size", {}).get("chunk_overlap", 50)
    
    fund_id = fund_data["fund_id"]
    fund_name = fund_data["fund_name"]
    source_url = fund_data["source_url"]
    last_scraped_at = fund_data.get("last_scraped_at", "")
    
    # We only process changed sections
    data_to_chunk = {k: v for k, v in fund_data.items() if k in changed_sections}
    if not data_to_chunk:
        return []
        
    full_text = json.dumps(data_to_chunk, indent=2)
    chunks = []
    
    start = 0
    chunk_idx = 0
    while start < len(full_text):
        end = start + chunk_size
        text_chunk = full_text[start:end]
        
        chunks.append(Chunk(
            chunk_id=f"{fund_id}::fixed::{chunk_idx}",
            fund_id=fund_id,
            fund_name=fund_name,
            section="all",
            text=text_chunk,
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            chunk_index=chunk_idx,
            strategy="fixed_size"
        ))
        
        start += chunk_size - chunk_overlap
        chunk_idx += 1
        
    return chunks
