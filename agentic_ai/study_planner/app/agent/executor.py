from app.llm import run_llm
def generate_tasks(topic: str):
    prompt = f"""
Generate concrete study tasks for topic:
{topic}

Include:
- Videos
- Reading
- Practice problems
"""
    return run_llm("mistral:7b", prompt)