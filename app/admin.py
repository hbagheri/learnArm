"""Admin endpoints for lesson content management."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import Lesson, Step
from app.schemas import LessonCreate, LessonUpdate, LessonResponse, StepCreate, StepResponse
from typing import List

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

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


# ============ WEB UI ROUTES ============

@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard with overview."""
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    lesson_count = len(lessons)
    step_count = sum(len(lesson.steps) for lesson in lessons)
    published_count = db.query(Lesson).filter(Lesson.is_published == True).count()
    draft_count = lesson_count - published_count
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "lesson_count": lesson_count,
        "step_count": step_count,
        "published_count": published_count,
        "draft_count": draft_count,
        "recent_lessons": lessons,
    })


@router.get("/lessons")
def list_lessons_ui(request: Request, db: Session = Depends(get_db)):
    """Display lessons list page."""
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    return templates.TemplateResponse("lessons.html", {
        "request": request,
        "lessons": lessons,
    })


@router.get("/lessons/new")
def new_lesson_form(request: Request):
    """Show form for creating new lesson."""
    return templates.TemplateResponse("lesson_form.html", {
        "request": request,
        "lesson": None,
    })


@router.post("/lessons/new")
async def create_lesson_ui(request: Request, db: Session = Depends(get_db)):
    """Create lesson from form submission."""
    form = await request.form()
    lesson = Lesson(
        title_fa=form.get("title_fa"),
        subtitle_fa=form.get("subtitle_fa"),
        module_key=form.get("module_key"),
        order_index=int(form.get("order_index", 0)),
        est_minutes=int(form.get("est_minutes", 5)),
        is_published=bool(form.get("is_published")),
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return RedirectResponse(url=f"/admin/lessons/{lesson.id}", status_code=303)


@router.get("/lessons/{lesson_id}")
def edit_lesson_form(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    """Show form for editing lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return templates.TemplateResponse("lesson_form.html", {
        "request": request,
        "lesson": lesson,
    })


@router.post("/lessons/{lesson_id}")
async def update_lesson_ui(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    """Update lesson from form submission."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    form = await request.form()
    lesson.title_fa = form.get("title_fa")
    lesson.subtitle_fa = form.get("subtitle_fa")
    lesson.module_key = form.get("module_key")
    lesson.order_index = int(form.get("order_index", 0))
    lesson.est_minutes = int(form.get("est_minutes", 5))
    lesson.is_published = bool(form.get("is_published"))

    db.commit()
    db.refresh(lesson)
    return RedirectResponse(url=f"/admin/lessons/{lesson.id}", status_code=303)


@router.get("/lessons/{lesson_id}/delete")
def delete_lesson_ui(lesson_id: int, db: Session = Depends(get_db)):
    """Delete lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()
    return RedirectResponse(url="/admin/lessons", status_code=303)


@router.get("/lessons/{lesson_id}/steps/new")
def new_step_form(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    """Show form for adding step to lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return templates.TemplateResponse("step_form.html", {
        "request": request,
        "lesson": lesson,
        "step": None,
    })


@router.post("/lessons/{lesson_id}/steps/new")
async def create_step_ui(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    """Create step from form submission."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    form = await request.form()
    step = Step(
        lesson_id=lesson_id,
        order_index=int(form.get("order_index", 0)),
        step_type=form.get("step_type"),
        item_key=form.get("item_key"),
        prompt_fa=form.get("prompt_fa") or None,
    )
    db.add(step)
    db.commit()
    db.refresh(step)
    return RedirectResponse(url=f"/admin/lessons/{lesson_id}", status_code=303)


@router.get("/lessons/{lesson_id}/steps/{step_id}/edit")
def edit_step_form(lesson_id: int, step_id: int, request: Request, db: Session = Depends(get_db)):
    """Show form for editing step."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    step = db.query(Step).filter(
        Step.id == step_id,
        Step.lesson_id == lesson_id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    return templates.TemplateResponse("step_form.html", {
        "request": request,
        "lesson": lesson,
        "step": step,
    })


@router.post("/lessons/{lesson_id}/steps/{step_id}/edit")
async def update_step_ui(lesson_id: int, step_id: int, request: Request, db: Session = Depends(get_db)):
    """Update step from form submission."""
    step = db.query(Step).filter(
        Step.id == step_id,
        Step.lesson_id == lesson_id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    form = await request.form()
    step.order_index = int(form.get("order_index", 0))
    step.step_type = form.get("step_type")
    step.item_key = form.get("item_key")
    step.prompt_fa = form.get("prompt_fa") or None

    db.commit()
    db.refresh(step)
    return RedirectResponse(url=f"/admin/lessons/{lesson_id}", status_code=303)


@router.get("/lessons/{lesson_id}/steps/{step_id}/delete")
def delete_step_ui(lesson_id: int, step_id: int, db: Session = Depends(get_db)):
    """Delete step."""
    step = db.query(Step).filter(
        Step.id == step_id,
        Step.lesson_id == lesson_id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    db.delete(step)
    db.commit()
    return RedirectResponse(url=f"/admin/lessons/{lesson_id}", status_code=303)
