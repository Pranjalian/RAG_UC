import logging
import time
from typing import List, Dict, Any, Optional

import groq
from groq import Groq

from src.vector_store.base import SearchResult
from src.generator.prompts import SYSTEM_PROMPT, format_context

logger = logging.getLogger("pipeline.generator")

class Generator:
    def __init__(self, api_key: str, config: Dict[str, Any]):
        if not api_key:
            raise ValueError("Groq API key is required for the Generator.")
            
        self.client = Groq(api_key=api_key)
        
        gen_cfg = config.get("generator", {})
        self.model = gen_cfg.get("model", "openai/gpt-oss-120b")
        self.temperature = gen_cfg.get("temperature", 0.0)
        
        # We will hardcode some retry logic for Rate Limits
        self.max_retries = 3
        self.base_backoff = 2  # seconds

    def generate(self, query: str, retrieved_chunks: List[SearchResult]) -> str:
        """
        Generate an answer to the query based on the retrieved chunks.
        """
        # 1. Early exit if no context is found (save LLM call & cost)
        if not retrieved_chunks:
            logger.info("No chunks retrieved. Returning 'not found' directly.")
            return "This information is not available in the indexed pages."
            
        # 2. Format context
        context_str = format_context(retrieved_chunks)
        system_message = SYSTEM_PROMPT.format(context=context_str)
        
        # 3. Call LLM with Retry logic
        for attempt in range(self.max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": query}
                    ],
                    temperature=self.temperature
                )
                
                answer = completion.choices[0].message.content
                return answer
                
            except groq.RateLimitError as e:
                logger.warning(f"RateLimitError from Groq (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    sleep_time = self.base_backoff ** (attempt + 1)
                    logger.info(f"Sleeping for {sleep_time} seconds before retry...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Max retries reached for RateLimitError.")
                    return "Error: Unable to generate an answer at this time due to rate limits."
            except Exception as e:
                logger.error(f"Unexpected error during generation: {e}")
                return "Error: An unexpected error occurred while generating the answer."
                
        return "Error: Unable to generate an answer."
