"""Pydantic schemas for API request/response validation."""

from typing import Optional, List
from pydantic import BaseModel


class StepCreate(BaseModel):
    order_index: int
    step_type: str  # SHOW_LETTER, QUIZ_LETTER, SHOW_PHRASE, QUIZ_PHRASE, PRACTICE_PHRASE
    item_key: str  # letter:5, phrase:13, etc.
    prompt_fa: Optional[str] = None


class StepResponse(StepCreate):
    id: int
    lesson_id: int

    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    title_fa: str
    subtitle_fa: str
    module_key: str
    order_index: int
    est_minutes: int = 5
    prerequisites: str = "[]"  # JSON string


class LessonUpdate(BaseModel):
    title_fa: Optional[str] = None
    subtitle_fa: Optional[str] = None
    module_key: Optional[str] = None
    order_index: Optional[int] = None
    est_minutes: Optional[int] = None
    prerequisites: Optional[str] = None
    is_published: Optional[bool] = None


class LessonResponse(LessonCreate):
    id: int
    is_published: bool
    steps: List[StepResponse] = []

    class Config:
        from_attributes = True
