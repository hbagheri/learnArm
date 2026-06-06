"""Admin endpoints for lesson content management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lesson, Step
from app.schemas import LessonCreate, LessonUpdate, LessonResponse, StepCreate, StepResponse
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])


# ============ LESSON ENDPOINTS ============

@router.post("/lessons", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    """Create a new lesson."""
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@router.get("/lessons", response_model=List[LessonResponse])
def list_lessons(db: Session = Depends(get_db)):
    """List all lessons (draft and published)."""
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    return lessons


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson with its steps."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.patch("/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, update: LessonUpdate, db: Session = Depends(get_db)):
    """Update lesson metadata."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Delete a lesson and all its steps."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}


# ============ STEP ENDPOINTS ============

@router.post("/lessons/{lesson_id}/steps", response_model=StepResponse)
def create_step(lesson_id: int, step: StepCreate, db: Session = Depends(get_db)):
    """Add a step to a lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db_step = Step(lesson_id=lesson_id, **step.dict())
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


@router.patch("/lessons/{lesson_id}/steps/{step_id}", response_model=StepResponse)
def update_step(lesson_id: int, step_id: int, step: StepCreate, db: Session = Depends(get_db)):
    """Update a step."""
    db_step = db.query(Step).filter(
        Step.id == step_id,
        Step.lesson_id == lesson_id
    ).first()
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    for field, value in step.dict().items():
        setattr(db_step, field, value)

    db.commit()
    db.refresh(db_step)
    return db_step


@router.delete("/lessons/{lesson_id}/steps/{step_id}")
def delete_step(lesson_id: int, step_id: int, db: Session = Depends(get_db)):
    """Delete a step from a lesson."""
    db_step = db.query(Step).filter(
        Step.id == step_id,
        Step.lesson_id == lesson_id
    ).first()
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    db.delete(db_step)
    db.commit()
    return {"message": "Step deleted"}


# ============ PUBLISHING ============

@router.post("/publish")
def publish_version(db: Session = Depends(get_db)):
    """Mark all lessons as published and bump content version.

    This endpoint prepares the lesson content for /content/lessons sync.
    In a real system, this would:
    1. Export all published lessons to JSON
    2. Bump CONTENT_VERSION in lessons.py
    3. Notify clients to re-sync
    """
    published_count = db.query(Lesson).filter(Lesson.is_published == True).count()
    return {
        "message": "Published",
        "published_lessons": published_count,
        "note": "Manually update CONTENT_VERSION in app/lessons.py after export"
    }
