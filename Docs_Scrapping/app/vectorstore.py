# app/vectorstore.py
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadata):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5, doc_ids=None):
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]
            if doc_ids and meta["doc_id"] not in doc_ids:
                continue

            results.append(meta)

        return results
