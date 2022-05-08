from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DailyPlan(BaseModel):
    user_id: int
    book_id: int
    daily_goal: int
    is_submitted: bool = False
    progress: int = 0


class AddingDailyPlan(BaseModel):
    daily_goal: int


class EditingDailyPlan(BaseModel):
    daily_goal: Optional[int]


class DailyPlanEvaluation(BaseModel):
    evaluation_id: int
    date: datetime
    daily_goal: int
    daily_progress: int = 0
