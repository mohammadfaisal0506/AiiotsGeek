import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


def assemble_prompt(query: str, chunks: list[dict]) -> str:
    context_blocks = []

    for c in chunks:
        filename = c.get("filename", "unknown")
        location = (
            c.get("page")
            or c.get("slide")
            or c.get("paragraph")
            or c.get("chunk_id")
            or "N/A"
        )
        text = c.get("text", "")

        if not text.strip():
            continue

        context_blocks.append(
            f"[{filename} | {location}]\n{text}"
        )

    context = "\n\n".join(context_blocks)

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
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        return response.json()["response"].strip()

    except Exception as e:
        return f"Local LLM error: {str(e)}"
