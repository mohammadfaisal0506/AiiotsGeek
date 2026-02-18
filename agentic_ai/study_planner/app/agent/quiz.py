import json
import re
from app.llm.client import run_llm


# ==========================================
# SAFE JSON EXTRACTOR
# ==========================================

def extract_json_array(text: str):
    """
    Extract first JSON array from text.
    """
    match = re.search(r"\[\s*\{.*\}\s*\]", text, re.DOTALL)
    return match.group(0) if match else None


# ==========================================
# QUIZ VALIDATION
# ==========================================

def validate_quiz(data):

    if not isinstance(data, list) or len(data) != 5:
        return False

    for q in data:

        if not isinstance(q, dict):
            return False

        if "question" not in q or "options" not in q or "answer" not in q:
            return False

        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            return False

        # Ensure no duplicate options
        if len(set(q["options"])) != 4:
            return False

        # Ensure answer matches exactly one option
        if q["answer"] not in q["options"]:
            return False

    return True


# ==========================================
# QUIZ GENERATOR (ROBUST)
# ==========================================

def generate_quiz(topic: str, difficulty: str = "beginner"):

    prompt = f"""
You are a strict academic exam creator.

Generate EXACTLY 5 multiple choice questions.

Topic: {topic}
Difficulty: {difficulty}

STRICT RULES:
- Return ONLY JSON.
- No explanations.
- No markdown.
- No text outside JSON.
- Exactly 5 questions.
- Each question must have EXACTLY 4 options.
- "answer" must match exactly one option.
- No duplicate options.

FORMAT:

[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }}
]
"""

    max_attempts = 5

    for attempt in range(max_attempts):

        raw = run_llm("llama3:8b", prompt)

        # Clean markdown
        raw = raw.replace("```json", "").replace("```", "").strip()

        json_text = extract_json_array(raw)

        if not json_text:
            continue

        # Try loading JSON
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            # Attempt minor repair
            json_text = json_text.replace("\n", " ")
            try:
                data = json.loads(json_text)
            except:
                continue

        if validate_quiz(data):
            return data

    # -------------------------
    # SAFE FALLBACK
    # -------------------------

    return [
        {
            "question": f"Quiz generation failed for {topic}. Please retry.",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        }
    ]
