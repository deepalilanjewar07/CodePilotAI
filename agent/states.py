from pydantic import BaseModel, Field
from typing import Optional, List


class File(BaseModel):
    path: str
    purpose: str


class Plan(BaseModel):
    name: str
    description: str
    techstack: str
    features: List[str]
    files: List[File]


class ImplementationTask(BaseModel):
    filepath: str
    task_description: str


class TaskPlan(BaseModel):
    implementation_steps: List[ImplementationTask]


class CoderState(BaseModel):
    task_plan: TaskPlan
    current_step_idx: int = 0