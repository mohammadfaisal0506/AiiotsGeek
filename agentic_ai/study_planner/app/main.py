from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent.planner import plan_topics
from app.agent.reflector import adjust_plan
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
    plan = plan_topics(req.goal, req.days)

    state = {
        "goal": req.goal,
        "days": req.days,
        "plan": plan
    }

    save_state(state)
    return state


@app.post("/progress")
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
