import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict

from src.normalizer.field_mappings import SECTION_MAPPINGS

logger = logging.getLogger(__name__)

@dataclass
class NormalizedFund:
    fund_id: str
    fund_name: str
    source_url: str
    last_scraped_at: str
    overview: Dict[str, Any]
    returns: Dict[str, Any]
    fund_managers: List[Dict[str, Any]]
    amc_details: Dict[str, Any]
    holdings: List[Dict[str, Any]]

class Normalizer:
    def __init__(self, config: dict):
        self.output_dir = config.get("output_dir", "data/normalized")
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_date(self, date_str: str) -> str:
        """
        Converts dates like "01-Jan-2013" to "2013-01-01".
        Leaves already formatted ISO dates or nulls alone.
        """
        if not date_str or not isinstance(date_str, str):
            return date_str
            
        try:
            # Example format: "01-Jan-2013"
            dt = datetime.strptime(date_str.strip(), "%d-%b-%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
        try:
            # Maybe it's already an ISO string like "2023-06-21T18:30:00.000Z"
            # Just keep it as is, or attempt to parse if needed.
            return date_str
        except Exception:
            return date_str

    def clean_float(self, val: Any) -> float:
        """
        Cleans percentage or currency strings and returns a float.
        Example: "0.75" -> 0.75, "1.05%" -> 1.05, "₹33,250 Cr" -> 33250.0
        """
        if val is None:
            return None
        if isinstance(val, (int, float)):
            return float(val)
        
        # String cleanup
        s = str(val).replace(",", "").replace("%", "").replace("₹", "").replace(" Cr", "").strip()
        try:
            return float(s)
        except ValueError:
            return val # Fallback to original if it's text like "Exit load of 1%..."

    def normalize_value(self, key: str, value: Any) -> Any:
        """Applies specific cleaning rules based on the field name."""
        if value is None:
            return None

        # Fields expected to be floats
        float_fields = {"expense_ratio", "aum", "min_sip_investment", "min_investment_amount", "nav"}
        if key in float_fields:
            return self.clean_float(value)
            
        # Fields expected to be dates
        date_fields = {"launch_date", "nav_date"}
        if key in date_fields:
            return self.clean_date(value)
            
        return value

    def normalize_fund(self, raw_data: dict) -> NormalizedFund:
        """
        Takes raw ScraperResult dictionary and transforms it into a NormalizedFund.
        """
        fund_id = raw_data.get("fund_id")
        fund_name = raw_data.get("fund_name")
        source_url = raw_data.get("source_url")
        last_scraped_at = raw_data.get("scraped_at")
        
        raw_sections = raw_data.get("raw_sections", {})
        
        normalized_data = {
            "overview": {},
            "returns": {},
            "fund_managers": [],
            "amc_details": {},
            "holdings": []
        }
        
        for section, keys in SECTION_MAPPINGS.items():
            if section in ["fund_managers", "amc_details", "holdings"]:
                # These might just map directly to lists or dicts
                for key in keys:
                    if key in raw_sections:
                        val = raw_sections[key]
                        if val is not None:
                            # Direct assignment for complex structures, we can refine inner keys if needed
                            if section == "fund_managers" and isinstance(val, list):
                                normalized_data[section].extend(val)
                            elif section == "holdings" and isinstance(val, list):
                                normalized_data[section].extend(val)
                            elif section == "amc_details" and isinstance(val, dict):
                                normalized_data[section].update(val)
            else:
                for key in keys:
                    if key in raw_sections:
                        raw_val = raw_sections[key]
                        cleaned_val = self.normalize_value(key, raw_val)
                        normalized_data[section][key] = cleaned_val

        return NormalizedFund(
            fund_id=fund_id,
            fund_name=fund_name,
            source_url=source_url,
            last_scraped_at=last_scraped_at,
            overview=normalized_data["overview"],
            returns=normalized_data["returns"],
            fund_managers=normalized_data["fund_managers"],
            amc_details=normalized_data["amc_details"],
            holdings=normalized_data["holdings"]
        )

    def persist_normalized(self, fund: NormalizedFund):
        """Save normalized fund to disk."""
        file_path = os.path.join(self.output_dir, f"{fund.fund_id}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(fund), f, indent=2, ensure_ascii=False)
            logger.debug(f"Persisted normalized data to {file_path}")
        except IOError as e:
            logger.error(f"Failed to persist normalized data for {fund.fund_id}: {str(e)}")
