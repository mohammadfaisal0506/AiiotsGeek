import os
import pickle
import numpy as np
import faiss
from .utils import logger

DATA_DIR = os.getenv("DATA_DIR", "./data")
FAISS_INDEX_FILE = os.getenv("FAISS_INDEX_FILE", os.path.join(DATA_DIR, "faiss.index"))
METADATA_FILE = os.getenv("METADATA_STORE_FILE", os.path.join(DATA_DIR, "metadata.pkl"))

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        self._load()

    def _load(self):
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(METADATA_FILE):
            try:
                self.index = faiss.read_index(FAISS_INDEX_FILE)
                with open(METADATA_FILE, "rb") as f:
                    self.metadata = pickle.load(f)
                logger.info("Loaded FAISS index and metadata")
            except Exception as e:
                logger.warning(f"Failed loading index: {e}. Creating new.")
                self.index = None
                self.metadata = []
        else:
            self.index = None
            self.metadata = []

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_FILE)
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def add(self, embeddings: list, metadatas: list):
        vecs = np.array(embeddings).astype('float32')
        dim = vecs.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(vecs)
        self.metadata.extend(metadatas)
        self._save()

    def search(self, query_embedding, top_k=5):
        q = np.array([query_embedding]).astype('float32')
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            md = self.metadata[idx].copy()
            md["score"] = float(dist)
            md["index"] = int(idx)
            results.append(md)
        return results
