from pydantic import BaseModel
from typing import Dict
from enum import Enum


class ProgressStatus(str, Enum):
    completed = "completed"
    partial = "partial"
    not_done = "not_done"


class GoalRequest(BaseModel):
    goal: str
    days: int


class ProgressUpdate(BaseModel):
    progress: Dict[str, ProgressStatus]
