from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class Chunk:
    chunk_id: str
    fund_id: str
    fund_name: str
    section: str
    text: str
    source_url: str
    last_scraped_at: str
    chunk_index: int
    strategy: str

def create_chunker(config: Dict[str, Any]):
    strategy = config.get("chunker", {}).get("strategy", "section_aware")
    if strategy == "section_aware":
        from .section_aware import section_aware_chunking
        return section_aware_chunking
    elif strategy == "fixed_size":
        from .fixed_size import fixed_size_chunking
        return fixed_size_chunking
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
