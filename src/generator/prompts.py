SYSTEM_PROMPT = """You are a helpful, expert financial assistant for HDFC Mutual Funds. 
Your goal is to answer the user's questions based strictly on the provided context chunks.

CRITICAL RULES:
1. **Answer ONLY from context**: You must base your entire answer only on the provided context. Do not use outside knowledge. 
2. **Not found fallback**: If the answer is not present in the context, you MUST respond exactly with: "This information is not available in the indexed pages." Do not attempt to guess or hallucinate.
3. **No Financial Advice**: Never provide personalized investment advice. You are only providing factual information about the mutual funds based on the text.
4. **Citations**: For every claim you make, you must cite the source. At the very end of your answer, list the sources used in this exact format:
   [Source: <url>, Data as of: <timestamp>]
   (You will find the <url> and <timestamp> in the chunk metadata provided below).
5. **Conciseness**: Keep your answers clear, concise, and structured (use bullet points if helpful).

CONTEXT:
{context}
"""

def format_context(retrieved_chunks) -> str:
    """
    Format a list of SearchResult chunks into a context string for the prompt.
    """
    if not retrieved_chunks:
        return ""
        
    formatted_chunks = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        # Extract metadata
        url = chunk.metadata.get("source_url", "Unknown URL")
        timestamp = chunk.metadata.get("last_scraped_at", "Unknown Time")
        
        chunk_text = f"--- Chunk {i} ---\n"
        chunk_text += f"Metadata: URL={url}, Timestamp={timestamp}\n"
        chunk_text += f"Content:\n{chunk.text}\n"
        formatted_chunks.append(chunk_text)
        
    return "\n".join(formatted_chunks)
