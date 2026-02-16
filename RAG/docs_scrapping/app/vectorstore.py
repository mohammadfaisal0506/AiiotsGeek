import os, pickle
import numpy as np
import faiss
from .utils import FAISS_INDEX_FILE, METADATA_STORE_FILE, logger

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        self._load()

    def _load(self):
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(METADATA_STORE_FILE):
            try:
                self.index = faiss.read_index(FAISS_INDEX_FILE)
                with open(METADATA_STORE_FILE, "rb") as f:
                    self.metadata = pickle.load(f)
                logger.info("Loaded FAISS index and metadata")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}")
                self.index = None
                self.metadata = []

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_FILE)
        with open(METADATA_STORE_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def add(self, embeddings: list, metadatas: list):
        vecs = np.array(embeddings).astype('float32')
        if vecs.ndim == 1:
            vecs = vecs.reshape(1, -1)
        dim = vecs.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(vecs)
        self.metadata.extend(metadatas)
        self._save()

    def search(self, query_embedding, top_k=5, file_filter: str = None):
        if self.index is None:
            raise ValueError("Vector index empty. Index files first.")
        q = np.array([query_embedding]).astype('float32')
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            md = self.metadata[idx].copy()
            if file_filter and md.get("filename") != file_filter:
                continue
            md.update({"score": float(dist), "index": int(idx)})
            results.append(md)
        return results
