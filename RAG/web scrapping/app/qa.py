import os
from .utils import logger
OPENAI_KEY = os.getenv("OPENAI_API_KEY", None)

def assemble_prompt(query: str, docs: list):
    ctx_parts = []
    for i, d in enumerate(docs):
        ctx_parts.append(f"[{i+1}] Source: {d.get('url')} | Chunk: {d.get('chunk_id')}\n{d.get('text')}\n")
    context = "\n---\n".join(ctx_parts)
    prompt = f"""You are a helpful assistant. Use ONLY the provided context to answer the question below. Cite sources using the bracket numbers, e.g. [1].

Context:
{context}

Question:
{query}

Answer concisely and include bracketed references to the sources you used."""
    return prompt

def call_llm(prompt: str):
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                max_tokens=512,
                temperature=0.0
            )
            return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.warning(f"OpenAI call failed: {e}")
            return prompt
    logger.warning("OPENAI_API_KEY not set; returning prompt as fallback result.")
    return prompt
