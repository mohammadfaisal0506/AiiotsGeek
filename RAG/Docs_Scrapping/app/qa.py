import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def assemble_prompt(query: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[{c['filename']} | {c.get('page', 'N/A')}]\n{c['text']}"
        for c in chunks if c.get("text")
    )

    return f"""
You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not present, say "Answer not found in document."

Context:
{context}

Question:
{query}

Answer:
"""

def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["response"].strip()
