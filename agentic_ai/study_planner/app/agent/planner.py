from app.llm.client import run_llm
from app.agent.resources import get_resources


# ==============================
# SIMPLE TEXT STRUCTURE PARSER
# ==============================

def parse_topics(text: str):
    """
    Expected format from LLM:

    Topic 1:
    - Subtopic A
    - Subtopic B

    Topic 2:
    - Subtopic C
    - Subtopic D
    """

    topics = []
    current_topic = None

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Detect main topic (ends with :)
        if line.endswith(":"):
            if current_topic:
                topics.append(current_topic)

            current_topic = {
                "name": line[:-1].strip(),
                "subtopics": []
            }

        # Detect subtopic
        elif line.startswith("-") and current_topic:
            subtopic = line.replace("-", "").strip()
            current_topic["subtopics"].append(subtopic)

    if current_topic:
        topics.append(current_topic)

    return topics


# ==============================
# MAIN GENERAL STUDY PLANNER
# ==============================

def plan_topics(goal: str, days: int):

    print("\n===== DEBUG: GENERAL PLANNER START =====")
    print("Goal:", goal)
    print("Days:", days)

    prompt = f"""
Create a structured study plan for: {goal}

FORMAT STRICTLY LIKE THIS:

Main Topic 1:
- Subtopic A
- Subtopic B

Main Topic 2:
- Subtopic C
- Subtopic D

Do NOT include explanations.
Do NOT include numbering.
Only use the exact format above.
"""

    raw_response = run_llm("llama3:8b", prompt)

    print("\n===== DEBUG: RAW LLM RESPONSE =====")
    print(raw_response)

    parsed_topics = parse_topics(raw_response)

    print("\n===== DEBUG: PARSED STRUCTURE =====")
    print(parsed_topics)

    if not parsed_topics:
        raise Exception("Failed to parse topics from LLM response")

    days_per_topic = max(1, days // len(parsed_topics))

    final_topics = []

    for topic in parsed_topics:
        topic_data = {
            "name": topic["name"],
            "days": days_per_topic,
            "resources": get_resources(topic["name"]),
            "subtopics": []
        }

        for sub in topic["subtopics"]:
            topic_data["subtopics"].append({
                "name": sub,
                "resources": get_resources(sub)
            })

        final_topics.append(topic_data)

    print("===== DEBUG: GENERAL PLANNER END =====\n")

    return {"topics": final_topics}
