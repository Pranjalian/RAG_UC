import json
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class GrowwExtractor:
    """
    Extracts the core fund-fact data from a Groww mutual fund page.
    Instead of brittle text-parsing across heavily obfuscated CSS modules,
    this extractor targets the structured JSON payload embedded in the page's
    `__NEXT_DATA__` script tag, which contains all the required information.
    """

    @staticmethod
    def extract_fund_data(html_content: str) -> dict:
        """
        Parses the HTML and extracts the raw fund data, stripping out noise
        like global navigation, footer, and cross-fund comparison tables
        by directly selecting the core mutual fund data payload.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Target the Next.js data block using a CSS selector
        script_tag = soup.select_one('#__NEXT_DATA__')
        
        if not script_tag or not script_tag.string:
            logger.error("Could not find __NEXT_DATA__ script tag in HTML.")
            return {}
            
        try:
            data = json.loads(script_tag.string)
            # The exact path to the mutual fund data in Groww's Next.js structure
            mf_data = data.get('props', {}).get('pageProps', {}).get('mfServerSideData', {})
            
            # Noise Rejection: Instead of taking the whole payload which might contain
            # UI configuration, recommendations, or site-wide directories, we only
            # select the keys relevant to the mutual fund's facts.
            keys_to_extract = [
                'scheme_name', 'groww_rating', 'crisil_rating', 'category', 'sub_category',
                'description', 'benchmark_name', 'aum', 'expense_ratio', 'launch_date',
                'min_sip_investment', 'min_investment_amount', 'exit_load', 'stamp_duty',
                'nav', 'nav_date', 'return_stats', 'sip_return', 'simple_return',
                'fund_manager_details', 'amc_info', 'holdings'
            ]
            
            extracted_data = {}
            for key in keys_to_extract:
                if key in mf_data:
                    extracted_data[key] = mf_data[key]
                    
            return extracted_data
            
        except json.JSONDecodeError:
            logger.error("Failed to parse __NEXT_DATA__ JSON.")
            return {}
