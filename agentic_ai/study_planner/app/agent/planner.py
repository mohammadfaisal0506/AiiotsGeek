import json
import re
from app.llm.client import run_llm
from app.agent.resources import get_resource_for_subtopic


# ------------------------------------------
# JSON Extractor
# ------------------------------------------

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


# ------------------------------------------
# MAIN PLANNER
# ------------------------------------------

def plan_topics(goal: str, days: int, difficulty: str = "beginner"):

    prompt = f"""
You are an academic curriculum designer.

Create a structured study roadmap for:

Subject: {goal}
Difficulty: {difficulty}

STRICT RULES:
- Return ONLY valid JSON.
- No explanations.
- No markdown.
- No extra text.
- Include topic name, weight (0-1), and subtopics list.

FORMAT:

{{
  "topics": [
    {{
      "name": "Main Topic",
      "weight": 0.3,
      "subtopics": [
        "Subtopic 1",
        "Subtopic 2"
      ]
    }}
  ]
}}
"""

    max_attempts = 3

    for _ in range(max_attempts):

        raw = run_llm("llama3:8b", prompt)
        raw = raw.replace("```json", "").replace("```", "").strip()

        json_text = extract_json(raw)

        if not json_text:
            continue

        try:
            parsed = json.loads(json_text)
            break
        except:
            continue
    else:
        raise Exception("Failed to generate valid JSON.")

    topics = parsed.get("topics", [])

    if not topics:
        raise Exception("No topics generated.")

    final_topics = []

    for topic in topics:

        weight = topic.get("weight", 0.2)
        allocated_days = max(1, int(days * weight))

        subtopics_data = []

        for sub in topic.get("subtopics", []):

            subtopics_data.append({
                "name": sub,
                "resource": get_resource_for_subtopic(sub)
            })

        final_topics.append({
            "name": topic["name"],
            "days": allocated_days,
            "subtopics": subtopics_data
        })

    return {"topics": final_topics}
