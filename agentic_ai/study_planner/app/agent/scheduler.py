from app.llm.client import run_llm

def create_daily_plan(topic: str, day: int):
    prompt = f"""
Create a daily study plan for:

Topic: {topic}
Day: {day}

Include:
- Study tasks
- Practice
- Revision
"""
    return run_llm("mistral:7b", prompt)