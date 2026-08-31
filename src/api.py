import re
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from src.pipeline import QueryPipeline, IngestionPipeline
from src.config_loader import load_config
from src.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


# Initialize FastAPI
app = FastAPI(title="Mutual Fund RAG API")

# Dynamic CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "").strip()
allow_origins = [frontend_url] if frontend_url and frontend_url != "*" else ["*"]

# Allow requests from the Next.js frontend (e.g., localhost:3000 or Vercel domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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
        # Sanitize internal server errors to avoid leaking stack traces
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing your request.")

def run_ingestion_background():
    """Background task to run the ingestion pipeline."""
    try:
        logger.info("Starting background ingestion pipeline...")
        ingestion_pipeline = IngestionPipeline(config)
        ingestion_pipeline.run()
        logger.info("Background ingestion pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Background ingestion failed: {e}")

@app.post("/api/ingest")
async def ingest_endpoint(background_tasks: BackgroundTasks, authorization: str = Header(None)):
    """Trigger the ingestion pipeline in the background."""
    admin_token = os.getenv("ADMIN_TOKEN")
    
    if not admin_token:
        logger.error("ADMIN_TOKEN is not configured in the environment.")
        raise HTTPException(status_code=500, detail="Server configuration error.")
        
    expected_header = f"Bearer {admin_token}"
    if authorization != expected_header:
        logger.warning("Unauthorized attempt to trigger ingestion.")
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    background_tasks.add_task(run_ingestion_background)
    return {"message": "Ingestion pipeline started in the background. Check server logs for progress."}
