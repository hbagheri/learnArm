"""Versioned course content (lessons + extra phrases) for the LearnArm app.

Bump CONTENT_VERSION whenever the payload below changes — the client uses it
to detect whether to re-sync.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lesson

router = APIRouter(prefix="/content", tags=["content"])

CONTENT_VERSION = 1

# Extra phrases beyond the bootstrap assets/seed/phrases.json shipped with the
# APK. Client merges these into its local phrases table on sync.
EXTRA_PHRASES = [
    # Taxi-specific
    {"id": 51, "orderIndex": 51, "category": "taxi",
     "armenian": "Տաքսի՛", "transliteration": "taqsi",
     "persian": "تاکسی!", "note": "صدا کردن"},
    {"id": 52, "orderIndex": 52, "category": "taxi",
     "armenian": "Որտե՞ղ է կանգառը", "transliteration": "vortegh e kangary",
     "persian": "ایستگاه کجاست؟", "note": None},
    {"id": 53, "orderIndex": 53, "category": "taxi",
     "armenian": "Տարեք ինձ ...", "transliteration": "tarek indz ...",
     "persian": "منو ببر به ...", "note": "بعدش مقصد بگو"},
    {"id": 54, "orderIndex": 54, "category": "taxi",
     "armenian": "Որքա՞ն կարժենա", "transliteration": "vorqan karzhena",
     "persian": "چقدر می‌شه؟", "note": "قیمت کرایه"},
    {"id": 55, "orderIndex": 55, "category": "taxi",
     "armenian": "Կանգնեցրեք, խնդրեմ", "transliteration": "kangnetseq, khndrem",
     "persian": "نگه دارید لطفاً", "note": None},
    {"id": 56, "orderIndex": 56, "category": "taxi",
     "armenian": "Այստեղ լավ է", "transliteration": "ayst'egh lav e",
     "persian": "همین‌جا خوبه", "note": "برای پیاده شدن"},
    {"id": 57, "orderIndex": 57, "category": "taxi",
     "armenian": "Մանր փող չունեմ", "transliteration": "manr p'ogh ch'unem",
     "persian": "پول خرد ندارم", "note": None},
]


def _show_letters(start: int, end: int):
    return [
        {"orderIndex": i - start + 1, "type": "SHOW_LETTER",
         "itemKey": f"letter:{i}", "promptFa": None}
        for i in range(start, end + 1)
    ]


def _quiz_letters(start: int, end: int, base_order: int):
    return [
        {"orderIndex": base_order + (i - start),
         "type": "QUIZ_LETTER", "itemKey": f"letter:{i}",
         "promptFa": "این حرف چه صدایی داره؟"}
        for i in range(start, end + 1)
    ]


def _alphabet_lesson(lesson_id: int, order: int, start: int, end: int,
                     title: str, prereqs):
    show = _show_letters(start, end)
    quiz = _quiz_letters(start, end, base_order=len(show) + 1)
    return {
        "id": lesson_id,
        "orderIndex": order,
        "moduleKey": "alphabet",
        "titleFa": title,
        "subtitleFa": f"حرف‌های {start} تا {end}",
        "estMinutes": 6,
        "prerequisiteIds": prereqs,
        "steps": show + quiz,
    }


def _greetings_lesson():
    show_ids = [1, 2, 4, 5, 6, 7, 8, 13, 16, 18, 21, 22]
    quiz_ids = [1, 4, 7, 13, 18]
    practice_ids = [1, 13]
    steps = []
    for i, pid in enumerate(show_ids, start=1):
        steps.append({"orderIndex": i, "type": "SHOW_PHRASE",
                      "itemKey": f"phrase:{pid}", "promptFa": None})
    n = len(steps)
    for j, pid in enumerate(quiz_ids, start=1):
        steps.append({"orderIndex": n + j, "type": "QUIZ_PHRASE",
                      "itemKey": f"phrase:{pid}",
                      "promptFa": "این عبارت یعنی چی؟"})
    n = len(steps)
    for k, pid in enumerate(practice_ids, start=1):
        steps.append({"orderIndex": n + k, "type": "PRACTICE_PHRASE",
                      "itemKey": f"phrase:{pid}",
                      "promptFa": "این عبارت را با صدای بلند بگو"})
    return {
        "id": 4,
        "orderIndex": 4,
        "moduleKey": "greetings",
        "titleFa": "سلام و احوال‌پرسی",
        "subtitleFa": "اولین حرف‌های روزمره",
        "estMinutes": 8,
        "prerequisiteIds": [3],
        "steps": steps,
    }


def _taxi_lesson():
    show_ids = [47, 49, 51, 52, 53, 54, 55, 56, 57]
    quiz_ids = [51, 53, 54, 55]
    practice_ids = [52, 54]
    steps = []
    for i, pid in enumerate(show_ids, start=1):
        steps.append({"orderIndex": i, "type": "SHOW_PHRASE",
                      "itemKey": f"phrase:{pid}", "promptFa": None})
    n = len(steps)
    for j, pid in enumerate(quiz_ids, start=1):
        steps.append({"orderIndex": n + j, "type": "QUIZ_PHRASE",
                      "itemKey": f"phrase:{pid}",
                      "promptFa": "این عبارت یعنی چی؟"})
    n = len(steps)
    for k, pid in enumerate(practice_ids, start=1):
        steps.append({"orderIndex": n + k, "type": "PRACTICE_PHRASE",
                      "itemKey": f"phrase:{pid}",
                      "promptFa": "این عبارت را با صدای بلند بگو"})
    return {
        "id": 5,
        "orderIndex": 5,
        "moduleKey": "taxi",
        "titleFa": "تاکسی گرفتن",
        "subtitleFa": "جابه‌جایی شهری",
        "estMinutes": 10,
        "prerequisiteIds": [4],
        "steps": steps,
    }


LESSONS = [
    _alphabet_lesson(1, 1, 1, 13, "الفبا — بخش ۱", []),
    _alphabet_lesson(2, 2, 14, 26, "الفبا — بخش ۲", [1]),
    _alphabet_lesson(3, 3, 27, 39, "الفبا — بخش ۳", [2]),
    _greetings_lesson(),
    _taxi_lesson(),
]


def _lesson_to_dict(lesson: Lesson) -> dict:
    """Convert database lesson model to API response format."""
    return {
        "id": lesson.id,
        "orderIndex": lesson.order_index,
        "moduleKey": lesson.module_key,
        "titleFa": lesson.title_fa,
        "subtitleFa": lesson.subtitle_fa,
        "estMinutes": lesson.est_minutes,
        "prerequisiteIds": [],  # TODO: parse from prerequisites JSON
        "steps": [
            {
                "orderIndex": step.order_index,
                "type": step.step_type,
                "itemKey": step.item_key,
                "promptFa": step.prompt_fa,
            }
            for step in sorted(lesson.steps, key=lambda s: s.order_index)
        ],
    }


@router.get("/lessons")
def get_lessons(db: Session = Depends(get_db)):
    """Get all lessons (from database if available, fallback to hardcoded)."""
    db_lessons = db.query(Lesson).filter(Lesson.is_published == True).order_by(Lesson.order_index).all()

    if db_lessons:
        lessons = [_lesson_to_dict(lesson) for lesson in db_lessons]
    else:
        lessons = LESSONS

    return {
        "version": CONTENT_VERSION,
        "extraPhrases": EXTRA_PHRASES,
        "lessons": lessons,
    }


@router.get("/version")
def get_version():
    return {"version": CONTENT_VERSION}
