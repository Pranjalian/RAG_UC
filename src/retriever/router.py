import json
import logging
from typing import Dict, Any, Optional

import groq
from groq import Groq

logger = logging.getLogger("pipeline.router")

ROUTER_PROMPT = """You are a metadata extraction assistant for a Mutual Fund FAQ bot.
Your job is to read the user's question and extract two specific metadata fields if they are mentioned.

The corpus only contains information about 9 specific HDFC mutual funds. 
Here are the valid fund IDs:
- "hdfc_small_cap" (HDFC Small Cap Fund)
- "hdfc_mid_cap" (HDFC Mid Cap Fund)
- "hdfc_flexi_cap" (HDFC Flexi Cap Fund / HDFC Equity Fund)
- "hdfc_multi_cap" (HDFC Multi Cap Fund)
- "hdfc_gold_etf" (HDFC Gold ETF Fund of Fund)
- "hdfc_large_mid_cap" (HDFC Large and Mid Cap Fund)
- "hdfc_nifty_50" (HDFC Nifty 50 Index Fund)
- "hdfc_large_cap" (HDFC Large Cap Fund)
- "hdfc_elss" (HDFC ELSS Tax Saver Fund)

Here are the valid section IDs:
- "overview" (NAV, AUM, expense ratio, risk, category, rating, benchmark, min SIP, launch date)
- "returns" (1D/1Y/3Y/5Y returns, category average)
- "holdings" (Top holdings table, companies, sectors, assets)
- "exit_load" (Exit load rules, stamp duty)
- "tax_info" (LTCG/STCG treatment)
- "fund_manager" (Manager name, tenure, education, experience)
- "amc_details" (AMC name, total AUM, incorporation date)

Rules:
1. Return ONLY a valid JSON object. Do not include markdown code blocks.
2. If the user mentions a specific fund, include its ID as "fund_id". Otherwise, omit "fund_id" or set it to null.
3. If the user asks about something that maps clearly to one of the 7 sections, include it as "section". Otherwise, omit "section" or set it to null.

Output JSON format:
{
    "fund_id": "hdfc_small_cap" | null,
    "section": "overview" | null
}
"""

class QueryRouter:
    def __init__(self, api_key: str, model: str = "openai/gpt-oss-120b"):
        """Initialize the router with the Groq client."""
        if not api_key:
            raise ValueError("Groq API key is required for the QueryRouter.")
        self.client = Groq(api_key=api_key)
        self.model = model

    def extract_filters(self, query: str) -> Dict[str, Any]:
        """
        Extract metadata filters from a user query using Groq.
        Returns a dictionary suitable for ChromaDB 'where' clause, e.g.
        {'fund_id': 'hdfc_small_cap', 'section': 'overview'}
        """
        try:
            # We use json_object response format to guarantee JSON
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ROUTER_PROMPT},
                    {"role": "user", "content": f"User question: {query}\n\nExtract the JSON metadata:"}
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
                max_tokens=100
            )
            
            raw_response = completion.choices[0].message.content
            parsed = json.loads(raw_response)
            
            filters = {}
            if parsed.get("fund_id"):
                filters["fund_id"] = parsed["fund_id"]
            if parsed.get("section"):
                filters["section"] = parsed["section"]
                
            if filters:
                logger.info(f"Query Router extracted filters: {filters}")
            else:
                logger.info("Query Router extracted no filters.")
                
            return filters
            
        except Exception as e:
            logger.error(f"Error in query routing: {e}. Falling back to no filters.")
            return {}
