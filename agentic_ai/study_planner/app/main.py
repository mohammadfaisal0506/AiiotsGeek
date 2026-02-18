from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent.planner import plan_topics
from app.agent.reflector import adjust_plan
from app.agent.quiz import generate_quiz
from app.memory.state import load_state, save_state
from app.schemas import GoalRequest, ProgressUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/goal")
def set_goal(req: GoalRequest):
    plan = plan_topics(req.goal, req.days, req.difficulty)

    state = {
        "goal": req.goal,
        "days": req.days,
        "difficulty": req.difficulty,
        "plan": plan
    }

    save_state(state)
    return state


@app.post("/progress")

def update_progress(update: ProgressUpdate):

    state = load_state()

    if "progress" not in state:
        state["progress"] = {}

    state["progress"][update.topic] = {
        "subtopics": update.subtopic_status,
        "quiz_score": update.quiz_score
    }

    save_state(state)

    return {"message": "Progress updated"}

def update_progress(req: ProgressUpdate):
    state = load_state()

    if "plan" not in state:
        return {"error": "No active study plan"}

    updated_plan = adjust_plan(state["plan"], req.progress)

    state["plan"] = updated_plan
    state["progress"] = req.progress

    save_state(state)

    return {
        "message": "Plan updated successfully",
        "updated_plan": updated_plan
    }

@app.post("/quiz")
def quiz_endpoint(data: dict):
    topic = data["topic"]
    difficulty = data.get("difficulty", "beginner")
    return generate_quiz(topic, difficulty)
