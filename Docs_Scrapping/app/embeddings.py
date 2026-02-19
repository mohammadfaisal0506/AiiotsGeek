from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: List[str]) -> List[List[float]]:
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True
    ).tolist()

def embed_query(query: str) -> List[float]:
    return model.encode(
        [query],
        normalize_embeddings=True
    )[0].tolist()
