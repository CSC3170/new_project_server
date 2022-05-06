from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DailyPlan(BaseModel):
    user_id: int
    book_id: int
    daily_goal: int
    progress: int = 0


class DailyPlanEvaluation(BaseModel):
    date: datetime
    daily_goal: int
    daily_progress: int


class AddingDailyPlan(BaseModel):
    daily_goal: int


class EditingDailyPlan(BaseModel):
    daily_goal: Optional[int]
