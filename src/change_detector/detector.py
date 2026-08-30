import os
import json
import hashlib
import logging
from typing import Dict, Any, Tuple
from src.normalizer.normalizer import NormalizedFund

logger = logging.getLogger(__name__)

class ChangeDetector:
    def __init__(self, config: dict):
        self.hashes_dir = config.get("hashes_dir", "data/hashes")
        os.makedirs(self.hashes_dir, exist_ok=True)

    def hash_section(self, section_data: Any) -> str:
        """
        Creates a SHA-256 hash of a dictionary or list, ensuring stable sorting.
        """
        if section_data is None:
            return ""
            
        # Sort keys to ensure stable output for identical data
        encoded_data = json.dumps(section_data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return hashlib.sha256(encoded_data).hexdigest()

    def load_previous_hashes(self, fund_id: str) -> Dict[str, str]:
        """
        Loads the previously saved hashes for a given fund.
        Returns an empty dict if the file does not exist.
        """
        file_path = os.path.join(self.hashes_dir, f"{fund_id}.json")
        if not os.path.exists(file_path):
            return {}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load previous hashes for {fund_id}: {e}")
            return {}

    def save_hashes(self, fund_id: str, current_hashes: Dict[str, str]):
        """
        Saves the current hashes to disk.
        """
        file_path = os.path.join(self.hashes_dir, f"{fund_id}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_hashes, f, indent=2)
            logger.debug(f"Saved hashes for {fund_id}")
        except Exception as e:
            logger.error(f"Failed to save hashes for {fund_id}: {e}")

    def detect_changes(self, fund: NormalizedFund) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Compares the current fund sections against previously saved hashes.
        Returns:
            manifest: A dict mapping section names to "changed" or "unchanged".
            current_hashes: The newly computed hashes for all sections.
        """
        previous_hashes = self.load_previous_hashes(fund.fund_id)
        current_hashes = {}
        manifest = {}
        
        # We only check the primary sections inside NormalizedFund
        sections = {
            "overview": fund.overview,
            "returns": fund.returns,
            "fund_managers": fund.fund_managers,
            "amc_details": fund.amc_details,
            "holdings": fund.holdings
        }
        
        for section_name, section_data in sections.items():
            new_hash = self.hash_section(section_data)
            current_hashes[section_name] = new_hash
            
            old_hash = previous_hashes.get(section_name)
            
            if old_hash is None or old_hash != new_hash:
                manifest[section_name] = "changed"
            else:
                manifest[section_name] = "unchanged"
                
        return manifest, current_hashes
