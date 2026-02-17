from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunks_indexed: int

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    doc_ids: Optional[List[str]] = None
    reference_answer: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[dict]
    metrics: Optional[Dict[str, Any]] = None 