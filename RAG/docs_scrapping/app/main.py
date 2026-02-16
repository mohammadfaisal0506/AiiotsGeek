from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from app.models import UploadResponse, QueryRequest, QueryResponse
from .extractor import extract_text_from_file
from .cleaner import clean_text
from .chunker import chunk_text
from .embeddings import embed_texts
from .vectorstore import VectorStore
from .retriever import retrieve
from .qa import assemble_prompt, call_llm
from .utils import DATA_DIR, logger
import os, shutil, uuid

app=FastAPI(title="PDF & Docs RAG Backend")
vs = VectorStore()

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload", response_model=UploadResponse)
async def upload_and_index(file: UploadFile = File(...)):
    # Save file
    fname = file.filename
    uid = str(uuid.uuid4())[:8]
    safe_name = f"{uid}_{fname}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract
    try:
        filetype, text = extract_text_from_file(path)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))

    text = clean_text(text)
    if not text or len(text) < 20:
        raise HTTPException(status_code=400, detail="No extractable text found.")

    chunks = chunk_text(text)
    metadatas = []
    texts = []
    for i, c in enumerate(chunks):
        md = {"filename": safe_name, "chunk_id": i, "text": c[:2000]}
        metadatas.append(md)
        texts.append(c)

    embs = embed_texts(texts)
    vs.add(embeddings=embs, metadatas=metadatas)

    return UploadResponse(filename=safe_name, status="indexed", chunks_indexed=len(chunks))

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.query:
        raise HTTPException(status_code=400, detail="query is required")

    raw_results = retrieve(req.query, top_k=req.top_k or 5, file=req.file)
    if not raw_results:
        return QueryResponse(answer="No relevant content found.", source_chunks=[])

    doc_payload = []
    for r in raw_results:
        doc_payload.append({"filename": r.get("filename"), "chunk_id": r.get("chunk_id"), "text": r.get("text")})

    prompt = assemble_prompt(req.query, doc_payload)
    answer = call_llm(prompt)
    return QueryResponse(answer=answer, source_chunks=doc_payload)

@app.get("/files")
def list_files():
    return {"files": os.listdir(UPLOAD_DIR)}

@app.get("/")
def health():
    return {"status": "ok"}
