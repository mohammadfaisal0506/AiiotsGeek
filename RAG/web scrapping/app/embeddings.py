import os
from .utils import logger
OPENAI_KEY = os.getenv("OPENAI_API_KEY", None)

def embed_texts(texts: list):
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            res = openai.Embedding.create(model="text-embedding-3-large", input=texts)
            return [d['embedding'] for d in res['data']]
        except Exception as e:
            logger.warning(f"OpenAI embeddings failed: {e}. Falling back to sentence-transformers.")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return [v.tolist() for v in vectors]
