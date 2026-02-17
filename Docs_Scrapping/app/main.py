from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Optional
import os
import uuid

from app.models import UploadResponse, QueryRequest, QueryResponse
from app.extractor import extract_text_from_file
from app.cleaner import clean_text
from app.chunker import chunk_text
from app.embeddings import embed_texts
from app.vectorstore import VectorStore
from app.retriever import retrieve
from app.qa import assemble_prompt, call_llm
from app.utils import DATA_DIR, logger
from app.metrics import evaluate_answer

# ------------------------------
# APP SETUP
# ------------------------------

app = FastAPI(title="RAG Backend (Docs Scrapping)")

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

vs = VectorStore()

# ------------------------------
# UPLOAD ENDPOINT
# ------------------------------

@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    """
    Upload a document, index it, and return a unique document ID.
    """

    doc_id = str(uuid.uuid4())[:8]
    safe_name = f"{doc_id}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, safe_name)

    # Save file
    try:
        with open(path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Extract text
    try:
        filetype, text = extract_text_from_file(path)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))

    # Clean text
    text = clean_text(text)
    if not text or len(text) < 20:
        raise HTTPException(status_code=400, detail="No usable text found")

    # Chunk text
    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks created")

    # Prepare embeddings + metadata
    texts = []
    metadata = []

    for i, chunk in enumerate(chunks):
        texts.append(chunk)
        metadata.append({
            "doc_id": doc_id,
            "filename": file.filename,
            "chunk_id": i,
            "text": chunk,
            "page": i + 1
        })

    embeddings = embed_texts(texts)

    # Store in vector DB
    vs.add(embeddings=embeddings, metadata=metadata)

    return UploadResponse(
    doc_id=doc_id,
    filename=file.filename,
    chunks_indexed=len(chunks)
)


    

# ------------------------------
# QUERY ENDPOINT
# ------------------------------

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):

    results = retrieve(
        query=req.query,
        top_k=req.top_k or 5,
        doc_ids=req.doc_ids,
        store=vs
    )

    if not results:
        return QueryResponse(
            answer="No relevant content found.",
            source_chunks=[],
            metrics=None
        )

    prompt = assemble_prompt(req.query, results)
    answer = call_llm(prompt)

    metrics = None
    if req.reference_answer:
        metrics = evaluate_answer(
            reference=req.reference_answer,
            prediction=answer
        )

    return QueryResponse(
        answer=answer,
        source_chunks=results,
        metrics=metrics
    )