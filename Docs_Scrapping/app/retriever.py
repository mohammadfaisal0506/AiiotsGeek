# app/retriever.py
from app.embeddings import embed_texts

def retrieve(query, store, top_k=5, doc_ids=None):
    query_emb = embed_texts([query])[0]

   
    scores, indices = store.index.search(
        query_emb.reshape(1, -1), top_k * 3
    )

    results = []
    for idx in indices[0]:
        if idx == -1:
            continue

        meta = store.metadata[idx]

       
        if doc_ids and meta["doc_id"] not in doc_ids:
            continue

        results.append(meta)

        if len(results) >= top_k:
            break

    return results
