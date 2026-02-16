from fastapi import FastAPI, HTTPException
from .models import IndexRequest, IndexResponse, QueryRequest, QueryResponse
from .scraper import fetch_html, sanitize_url
from .cleaner import html_to_text
from .chunker import chunk_text
from .embeddings import embed_texts
from .vectorstore import VectorStore
from .retriever import retrieve
from .qa import assemble_prompt, call_llm
from .utils import logger

app = FastAPI(title="Website RAG Backend")
vs = VectorStore()

@app.post("/index", response_model=IndexResponse)
def index_url(req: IndexRequest):
    try:
        
        url = sanitize_url(str(req.url))

        html = fetch_html(url)
        text = html_to_text(html)
        chunks = chunk_text(text)

        metadatas = []
        texts = []
        for i, c in enumerate(chunks):
            meta = {
                "url": url,     
                "chunk_id": i,
                "text": c[:2000]
            }
            metadatas.append(meta)
            texts.append(c)

        embs = embed_texts(texts)
        vs.add(embeddings=embs, metadatas=metadatas)

        return IndexResponse(url=url, status="indexed", chunks_indexed=len(chunks))

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):

    if not req.query:
        raise HTTPException(status_code=400, detail="query is required")

    raw_results = retrieve(req.query, top_k=req.top_k or 5)

   
    if req.url:
        urlstr = sanitize_url(str(req.url)) 
        filtered = [r for r in raw_results if r.get("url") == urlstr]

        docs = filtered[: req.top_k or 5] if filtered else raw_results[: req.top_k or 5]
    else:
        docs = raw_results[: req.top_k or 5]

    doc_payload = []
    for r in docs:
        doc_payload.append({
            "url": r.get("url"),
            "chunk_id": r.get("chunk_id"),
            "text": r.get("text")
        })

    prompt = assemble_prompt(req.query, doc_payload)
    answer = call_llm(prompt)

    return QueryResponse(answer=answer, source_chunks=doc_payload)
