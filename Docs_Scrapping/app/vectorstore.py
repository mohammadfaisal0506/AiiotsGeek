import faiss
import numpy as np
import json
import os

class VectorStore:
    def __init__(self, dim=384, path="data/index"):
        self.dim = dim
        self.path = path
        self.index_file = os.path.join(path, "faiss.index")
        self.meta_file = os.path.join(path, "metadata.json")

        os.makedirs(path, exist_ok=True)

        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatIP(dim)
            self.metadata = []

    def add(self, embeddings, metadata):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)
        self.save()

    def search(self, query_embedding, top_k=5, doc_ids=None):
        q = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(q, top_k)

        results = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]
            if doc_ids and meta["doc_id"] not in doc_ids:
                continue

            results.append(meta)

        return results

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "w") as f:
            json.dump(self.metadata, f)
