# Website RAG Backend

## Overview
A Python backend RAG (Retrieval-Augmented Generation) starter:
- Scrape webpages (Playwright + trafilatura fallback)
- Clean and chunk text (LangChain splitter)
- Embeddings (OpenAI or sentence-transformers fallback)
- FAISS vector store with metadata
- FastAPI endpoints to index and query with LLM answers and citations

## Quickstart (local)
1. Copy env: `cp .env.example .env` and edit.
2. Install deps: `pip install -r requirements.txt`
3. Install Playwright browsers: `python -m playwright install`
4. Run: `uvicorn app.main:app --reload`

## Using Docker
`docker compose up --build`

## Endpoints
- POST /index  -> { "url": "https://example.com" }
- POST /query  -> { "url": "https://example.com", "query": "What is pricing?" }
