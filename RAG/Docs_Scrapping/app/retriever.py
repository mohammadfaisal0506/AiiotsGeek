from app.embeddings import embed_query

def retrieve(query: str, store, top_k=5, doc_ids=None):
    query_embedding = embed_query(query)

    results = store.search(
        query_embedding=query_embedding,
        top_k=top_k * 3,
        doc_ids=doc_ids
    )

    return results[:top_k]
