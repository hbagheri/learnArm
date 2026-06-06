"""SQLAlchemy models for lesson content."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title_fa = Column(String, index=True)  # Persian title
    subtitle_fa = Column(String)
    module_key = Column(String)  # "alphabet", "greetings", "taxi", etc.
    order_index = Column(Integer)  # Sort order in lesson list
    est_minutes = Column(Integer, default=5)
    prerequisites = Column(String)  # JSON list of prerequisite lesson IDs
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    steps = relationship("Step", back_populates="lesson", cascade="all, delete-orphan")


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), index=True)
    order_index = Column(Integer)  # Order within lesson
    step_type = Column(String)  # "SHOW_LETTER", "QUIZ_LETTER", "SHOW_PHRASE", "QUIZ_PHRASE", "PRACTICE_PHRASE"
    item_key = Column(String)  # "letter:5", "phrase:13", etc.
    prompt_fa = Column(String, nullable=True)  # Persian instruction text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="steps")
