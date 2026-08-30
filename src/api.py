import re
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline import QueryPipeline
from src.config_loader import load_config
from src.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


# Initialize FastAPI
app = FastAPI(title="Mutual Fund RAG API")

# Allow requests from the Next.js frontend (e.g., localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
try:
    config = load_config("config/config.yaml")
    pipeline = QueryPipeline(config)
    logger.info("QueryPipeline initialized successfully for API.")
except Exception as e:
    logger.error(f"Failed to initialize QueryPipeline: {e}")
    pipeline = None

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[dict]

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline is not initialized")
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    try:
        # Get raw answer from pipeline
        raw_answer = pipeline.query(request.question)
        
        # Parse citations out of the answer string
        # Look for [Source: <url>, Data as of: <timestamp>]
        citation_pattern = r'\[Source:\s*(.*?),\s*Data as of:\s*(.*?)\]'
        
        citations = []
        for match in re.finditer(citation_pattern, raw_answer):
            url = match.group(1).strip()
            date = match.group(2).strip()
            # Only store unique citations to prevent UI bloat
            citation = {"url": url, "date": date}
            if citation not in citations:
                citations.append(citation)
                
        # Clean the answer text by removing the citation lines since the UI handles them
        clean_answer = re.sub(citation_pattern, '', raw_answer).strip()
        
        return ChatResponse(
            answer=clean_answer,
            citations=citations
        )
        
    except Exception as e:
        logger.error(f"Error during query processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
