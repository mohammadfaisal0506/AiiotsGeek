from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any

class IndexRequest(BaseModel):
    url: HttpUrl
    force: Optional[bool] = False

class QueryRequest(BaseModel):
    url: Optional[HttpUrl] = None
    query: str
    top_k: Optional[int] = 5

class IndexResponse(BaseModel):
    url: HttpUrl
    status: str
    chunks_indexed: int

class SourceChunk(BaseModel):
    url: HttpUrl
    chunk_id: int
    text: str
    score: Optional[float] = None

class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[Any]
