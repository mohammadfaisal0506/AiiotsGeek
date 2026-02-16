from .embeddings import embed_texts
from .vectorstore import VectorStore

vs = VectorStore()

def retrieve(query: str, top_k: int = 5, file: str = None):
    q_emb = embed_texts([query])[0]
    return vs.search(q_emb, top_k=top_k, file_filter=file)
