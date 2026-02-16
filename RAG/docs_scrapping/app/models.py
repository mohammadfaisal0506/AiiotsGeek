from pydantic import BaseModel
from typing import List, Optional


class UploadResponse(BaseModel):
    file_name: str
    status: str = "uploaded"
    message: Optional[str] = None


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
