from pydantic import BaseModel
from typing import Dict, Optional
from enum import Enum


class ProgressStatus(str, Enum):
    completed = "completed"
    partial = "partial"
    not_done = "not_done"


class GoalRequest(BaseModel):
    goal: str
    days: int
    difficulty: str


class ProgressUpdate(BaseModel):
    topic: str
    subtopic_status: Dict[str, ProgressStatus]
    quiz_score: Optional[int] = 0