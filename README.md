# Mutual Fund FAQ Assistant - RAG Pipeline

This project is a local, single-user Retrieval-Augmented Generation (RAG) pipeline designed for answering factual questions about a specific set of 9 Mutual Funds on Groww.

## Project Structure

- `docs/`: Project documentation (Architecture, Implementation Plan).
- `src/`: Python source code for the pipeline components.
- `config/`: Central configuration file `config.yaml`.
- `data/`: Local storage for raw HTML, normalized JSON, hashes, and logs.
- `vector_db/`: Local vector database storage (Chroma / FAISS).
- `experiments/`: Evaluation results and comparison reports.

## Quickstart

1. **Activate the virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the CLI**:
   The primary entry point is `src/main.py`.
   ```bash
   python src/main.py --help
   ```

## Available Commands
- `python src/main.py scrape`: Runs the scraper only.
- `python src/main.py ingest`: Runs the full ingestion pipeline (scrape -> embed -> store).
- `python src/main.py query "Your question"`: Query the pipeline for an answer.
- `python src/main.py query --interactive`: Start an interactive REPL loop.
- `python src/main.py schedule --start`: Start the recurring scheduler for updates.
- `python src/main.py evaluate`: Run evaluation test suite.

For more details on the architecture and implementation, see the `docs/` folder.
