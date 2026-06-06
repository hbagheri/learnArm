"""Learning curriculum - levels, phases, and progression."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["curriculum"])


class Phase(BaseModel):
    id: int
    title: str
    description: str
    type: str  # "learning" or "exam"
    isCompleted: bool = False
    score: Optional[int] = None


class Level(BaseModel):
    id: int
    title: str
    titleFa: str
    description: str
    phases: List[Phase]
    isUnlocked: bool


# ============ CURRICULUM DATA ============

CURRICULUM = [
    Level(
        id=1,
        title="الفبا",
        titleFa="Letters - الفبای ارمنی",
        description="یادگیری ۳۹ حرف ارمنی",
        isUnlocked=True,
        phases=[
            Phase(
                id=1,
                title="شناسایی حروف",
                description="تشخیص حروف و صدای آن‌ها - نیاز: ۱۰۰%",
                type="learning",
            ),
            Phase(
                id=2,
                title="تکرار حروف",
                description="تمرین تلفظ درست حروف - نیاز: ۸۲%",
                type="learning",
            ),
            Phase(
                id=3,
                title="حروف در واژه‌ها",
                description="حرف در شروع، وسط و انتهای واژه - نیاز: ۱۰۰%",
                type="learning",
            ),
            Phase(
                id=4,
                title="امتحان حروف",
                description="۴ مرحله: تلفظ، تطابق، شنیدن، واژه",
                type="exam",
            ),
        ],
    ),
    Level(
        id=2,
        title="واژگان",
        titleFa="Vocabulary - کلمات",
        description="یادگیری ۲۰-۳۰ واژه از هر سطح",
        isUnlocked=False,
        phases=[
            Phase(
                id=5,
                title="معرفی واژه‌ها",
                description="واژه‌های جدید و تلفظ آن‌ها",
                type="learning",
            ),
            Phase(
                id=6,
                title="تمرین تلفظ واژه",
                description="تکرار واژه‌ها - نیاز: ۹۰%",
                type="learning",
            ),
            Phase(
                id=7,
                title="امتحان واژگان",
                description="خوندن واژه بدون کمک صوتی - نیاز: ۹۰%",
                type="exam",
            ),
        ],
    ),
    Level(
        id=3,
        title="جملات",
        titleFa="Sentences - جملات",
        description="یادگیری جملاتی و ساختار آن‌ها",
        isUnlocked=False,
        phases=[
            Phase(
                id=8,
                title="مفاهیم جملاتی",
                description="فعل، فاعل، مفعول، قید",
                type="learning",
            ),
            Phase(
                id=9,
                title="خوندن و تلفظ جملات",
                description="تمرین خوندن جملات",
                type="learning",
            ),
            Phase(
                id=10,
                title="امتحان جملات",
                description="ترجمه فارسی → ارمنی",
                type="exam",
            ),
        ],
    ),
    Level(
        id=4,
        title="رسانه‌ها",
        titleFa="Media - فیلم و خبر",
        description="فیلم‌ها و اخبار به ارمنی",
        isUnlocked=False,
        phases=[
            Phase(
                id=11,
                title="تماشای فیلم",
                description="تماشای فیلم و نوشتن چیزی که شنیدی",
                type="learning",
            ),
            Phase(
                id=12,
                title="خبر و ترجمه",
                description="خواندن خبر و ترجمه به فارسی",
                type="learning",
            ),
        ],
    ),
]


# ============ ENDPOINTS ============

@router.get("/levels", response_model=List[Level])
def get_levels():
    """Get all learning levels."""
    return CURRICULUM


@router.get("/levels/{level_id}", response_model=Level)
def get_level(level_id: int):
    """Get a specific level with its phases."""
    level = next((l for l in CURRICULUM if l.id == level_id), None)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level


@router.get("/levels/{level_id}/phases", response_model=List[Phase])
def get_level_phases(level_id: int):
    """Get phases for a specific level."""
    level = next((l for l in CURRICULUM if l.id == level_id), None)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level.phases


@router.get("/phases/{phase_id}", response_model=Phase)
def get_phase(phase_id: int):
    """Get a specific phase."""
    for level in CURRICULUM:
        phase = next((p for p in level.phases if p.id == phase_id), None)
        if phase:
            return phase
    raise HTTPException(status_code=404, detail="Phase not found")
