from typing import Dict, Any, List
from .chunker import Chunk

def section_aware_chunking(fund_data: Dict[str, Any], changed_sections: List[str], config: Dict[str, Any]) -> List[Chunk]:
    """
    Chunking strategy that converts structured JSON sections into semantic Markdown templates.
    """
    chunks = []
    fund_id = fund_data["fund_id"]
    fund_name = fund_data["fund_name"]
    source_url = fund_data["source_url"]
    last_scraped_at = fund_data.get("last_scraped_at", "")
    
    # 1. Overview
    if "overview" in changed_sections and "overview" in fund_data:
        overview = fund_data["overview"]
        text = f"**Overview for {fund_name}**\n"
        for k, v in overview.items():
            if v is not None:
                text += f"- **{k.replace('_', ' ').title()}**: {v}\n"
        
        chunks.append(Chunk(
            chunk_id=f"{fund_id}::overview::0",
            fund_id=fund_id,
            fund_name=fund_name,
            section="overview",
            text=text.strip(),
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            chunk_index=0,
            strategy="section_aware"
        ))
        
    # 2. Returns
    if "returns" in changed_sections and "returns" in fund_data:
        returns = fund_data["returns"]
        text = f"**Returns for {fund_name}**\n\n"
        
        if "return_stats" in returns and returns["return_stats"]:
            stats = returns["return_stats"][0]
            text += "| Metric | Value |\n|---|---|\n"
            keys_to_include = ["return1y", "return3y", "return5y", "return10y", "mean_return", "sharpe_ratio", "beta", "alpha", "cat_return1y", "cat_return3y", "cat_return5y"]
            for k in keys_to_include:
                if k in stats and stats[k] is not None:
                    text += f"| {k} | {stats[k]} |\n"
        
        chunks.append(Chunk(
            chunk_id=f"{fund_id}::returns::0",
            fund_id=fund_id,
            fund_name=fund_name,
            section="returns",
            text=text.strip(),
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            chunk_index=0,
            strategy="section_aware"
        ))
        
    # 3. Fund Managers
    if "fund_managers" in changed_sections and "fund_managers" in fund_data:
        managers = fund_data["fund_managers"]
        text = f"**Fund Managers for {fund_name}**\n\n"
        for idx, mgr in enumerate(managers):
            name = mgr.get("person_name", "Unknown")
            edu = mgr.get("education", "")
            exp = mgr.get("experience", "")
            text += f"### {name}\n- **Education**: {edu}\n- **Experience**: {exp}\n\n"
            
        chunks.append(Chunk(
            chunk_id=f"{fund_id}::fund_managers::0",
            fund_id=fund_id,
            fund_name=fund_name,
            section="fund_managers",
            text=text.strip(),
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            chunk_index=0,
            strategy="section_aware"
        ))
        
    # 4. AMC Details
    if "amc_details" in changed_sections and "amc_details" in fund_data:
        amc = fund_data["amc_details"]
        text = f"**AMC Details for {fund_name}**\n"
        for k, v in amc.items():
            if v is not None and not k.startswith("vro_") and k != "more_description":
                # more_description often contains massive HTML dumps, skip it for chunk density
                text += f"- **{k.replace('_', ' ').title()}**: {v}\n"
                
        chunks.append(Chunk(
            chunk_id=f"{fund_id}::amc_details::0",
            fund_id=fund_id,
            fund_name=fund_name,
            section="amc_details",
            text=text.strip(),
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            chunk_index=0,
            strategy="section_aware"
        ))
        
    # 5. Holdings (Batched)
    if "holdings" in changed_sections and "holdings" in fund_data:
        holdings = fund_data["holdings"]
        batch_size = 25 # number of holdings per chunk
        
        for i in range(0, len(holdings), batch_size):
            batch = holdings[i:i+batch_size]
            chunk_idx = i // batch_size
            
            text = f"**Holdings for {fund_name} (Part {chunk_idx + 1})**\n\n"
            text += "| Company | Sector | Instrument | % Assets |\n|---|---|---|---|\n"
            for h in batch:
                name = h.get("company_name", "")
                sector = h.get("sector_name", "")
                instrument = h.get("instrument_name", "")
                pct = h.get("corpus_per", "")
                text += f"| {name} | {sector} | {instrument} | {pct}% |\n"
                
            chunks.append(Chunk(
                chunk_id=f"{fund_id}::holdings::{chunk_idx}",
                fund_id=fund_id,
                fund_name=fund_name,
                section="holdings",
                text=text.strip(),
                source_url=source_url,
                last_scraped_at=last_scraped_at,
                chunk_index=chunk_idx,
                strategy="section_aware"
            ))
            
    return chunks
