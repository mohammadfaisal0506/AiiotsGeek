from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
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

app = FastAPI(title="Production RAG Backend")

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

vs = VectorStore()

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx",
    ".xlsx", ".xls", ".csv",
    ".txt", ".md", ".json",
    ".html", ".htm",
    ".png", ".jpg", ".jpeg"
}


@app.get("/health")
def health():
    return {"status": "ok", "indexed_chunks": len(vs.metadata)}


@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    doc_id = str(uuid.uuid4())[:8]
    path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

    try:
        with open(path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(500, f"File save failed: {e}")

    try:
        filetype, raw_text = extract_text_from_file(path)
    except Exception as e:
        raise HTTPException(400, f"Extraction failed: {e}")

    text = clean_text(raw_text)

    if len(text) < 50:
        raise HTTPException(400, "No usable text extracted.")

    chunks = chunk_text(text)

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
    vs.add(embeddings, metadata)

    logger.info(f"Indexed {len(chunks)} chunks for {file.filename}")

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        chunks_indexed=len(chunks)
    )


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    results = retrieve(
        query=req.query,
        store=vs,
        top_k=req.top_k or 5,
        doc_ids=req.doc_ids
    )

    if not results:
        return QueryResponse(
            answer="No relevant content found.",
            source_chunks=[],
            metrics=None
        )

    prompt = assemble_prompt(req.query, results)

    try:
        answer = call_llm(prompt)
    except Exception as e:
        raise HTTPException(500, str(e))

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
