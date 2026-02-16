import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def run_llm(model: str, prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"LLM error: {response.text}")

        return response.json().get("response", "")

    except Exception as e:
        raise Exception(f"LLM connection failed: {str(e)}")
