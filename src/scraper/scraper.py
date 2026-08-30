import os
import json
import time
import logging
import requests
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Optional, List

from src.scraper.selectors import GrowwExtractor
from src.scraper.urls import FUND_URLS

logger = logging.getLogger(__name__)

@dataclass
class ScraperResult:
    fund_id: str
    fund_name: str
    source_url: str
    raw_sections: dict
    scraped_at: str
    success: bool
    error: Optional[str] = None

class Scraper:
    def __init__(self, config: dict):
        self.output_dir = config.get("output_dir", "data/rawdata")
        self.delay = config.get("request_delay_seconds", 2.5)
        self.timeout = config.get("request_timeout_seconds", 30)
        self.user_agent = config.get("user_agent", "MutualFundFAQBot/1.0")
        self.max_retries = config.get("max_retries", 2)
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.9"
        })

    def scrape_fund(self, fund_info: dict) -> ScraperResult:
        fund_id = fund_info["fund_id"]
        fund_name = fund_info["fund_name"]
        url = fund_info["url"]
        
        logger.info(f"Scraping fund: {fund_name} ({url})")
        
        extracted_data = {}
        success = False
        error_msg = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                extracted_data = GrowwExtractor.extract_fund_data(response.text)
                
                if extracted_data:
                    success = True
                    break
                else:
                    error_msg = "No data extracted from HTML (missing __NEXT_DATA__)."
            except requests.RequestException as e:
                error_msg = f"HTTP Error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed for {fund_name}: {error_msg}")
            
            if attempt < self.max_retries:
                time.sleep(self.delay)
                
        now_iso = datetime.now(timezone.utc).isoformat()
        
        result = ScraperResult(
            fund_id=fund_id,
            fund_name=fund_name,
            source_url=url,
            raw_sections=extracted_data,
            scraped_at=now_iso,
            success=success,
            error=error_msg if not success else None
        )
        
        # Persist to JSON
        self._persist_result(result)
        return result

    def _persist_result(self, result: ScraperResult):
        file_path = os.path.join(self.output_dir, f"{result.fund_id}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(result), f, indent=2, ensure_ascii=False)
            logger.debug(f"Persisted raw data to {file_path}")
        except IOError as e:
            logger.error(f"Failed to persist {result.fund_id}: {str(e)}")

    def scrape_all(self, urls: List[dict] = FUND_URLS) -> List[ScraperResult]:
        results = []
        for i, fund_info in enumerate(urls):
            result = self.scrape_fund(fund_info)
            results.append(result)
            
            # Respectful delay between requests
            if i < len(urls) - 1:
                time.sleep(self.delay)
                
        # Log summary
        success_count = sum(1 for r in results if r.success)
        logger.info(f"Scrape complete. {success_count}/{len(urls)} successful.")
        return results
