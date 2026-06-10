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


class WordPair(BaseModel):
    id: int
    armenian: str
    persian: str
    transliteration: Optional[str] = None


class Letter(BaseModel):
    id: int
    orderIndex: int
    upper: str
    lower: str
    name: str
    nameLatin: str
    pronunciationFa: str
    ipa: str
    exampleArmenian: str
    exampleLatin: str
    exampleFa: str
    audioAsset: Optional[str] = None


class BatchWord(BaseModel):
    armenian: str
    transliteration: str
    persian: str


class LetterBatch(BaseModel):
    index: int
    round: int
    letterIds: List[int]
    targetWord: BatchWord
    readableWords: List[BatchWord]


class LetterCurriculum(BaseModel):
    batches: List[LetterBatch]
    periodicReviewBatches: List[int]
    passThresholdPercent: int = 100   # min % correct to pass a batch test or periodic review
    hintTimeoutMs: int = 8000          # ms until the correct-letter hint shows on a question


VOCABULARY: List[WordPair] = [
    # Core greetings & courtesy
    WordPair(id=101, armenian="Բարև", persian="سلام", transliteration="barev"),
    WordPair(id=102, armenian="Շնորհակալություն", persian="ممنون", transliteration="shnorhakalut'yun"),
    WordPair(id=103, armenian="Խնդրեմ", persian="خواهش می‌کنم", transliteration="khndrem"),
    WordPair(id=104, armenian="Այո", persian="بله", transliteration="ayo"),
    WordPair(id=105, armenian="Ոչ", persian="نه", transliteration="voch"),
    # Food & drink
    WordPair(id=106, armenian="Ջուր", persian="آب", transliteration="jur"),
    WordPair(id=107, armenian="Հաց", persian="نان", transliteration="hats"),
    WordPair(id=108, armenian="Կաթ", persian="شیر", transliteration="kat"),
    WordPair(id=109, armenian="Թեյ", persian="چای", transliteration="tey"),
    WordPair(id=110, armenian="Սուրճ", persian="قهوه", transliteration="surch"),
    # Home & family
    WordPair(id=111, armenian="Տուն", persian="خانه", transliteration="tun"),
    WordPair(id=112, armenian="Մայր", persian="مادر", transliteration="mayr"),
    WordPair(id=113, armenian="Հայր", persian="پدر", transliteration="hayr"),
    WordPair(id=114, armenian="Ընկեր", persian="دوست", transliteration="ənker"),
    WordPair(id=115, armenian="Երեխա", persian="کودک", transliteration="yerekha"),
    # Time
    WordPair(id=116, armenian="Օր", persian="روز", transliteration="or"),
    WordPair(id=117, armenian="Գիշեր", persian="شب", transliteration="gisher"),
    WordPair(id=118, armenian="Առավոտ", persian="صبح", transliteration="aravot"),
    WordPair(id=119, armenian="Երեկո", persian="عصر", transliteration="yereko"),
    # City essentials
    WordPair(id=120, armenian="Քաղաք", persian="شهر", transliteration="qaghaq"),
    WordPair(id=121, armenian="Փող", persian="پول", transliteration="pogh"),
    WordPair(id=122, armenian="Խանութ", persian="مغازه", transliteration="khanut"),
    WordPair(id=123, armenian="Դեղատուն", persian="داروخانه", transliteration="deghatun"),
    WordPair(id=124, armenian="Ճանապարհ", persian="راه", transliteration="janaparh"),
    WordPair(id=125, armenian="Մեքենա", persian="ماشین", transliteration="meqena"),
]


SENTENCES: List[WordPair] = [
    # Question patterns
    WordPair(id=201, armenian="Որտե՞ղ է", persian="کجاست", transliteration="vortegh e"),
    WordPair(id=202, armenian="Որքա՞ն արժե", persian="چقدر است", transliteration="vorqan arzhe"),
    WordPair(id=203, armenian="Անունդ ի՞նչ է", persian="اسمت چیست", transliteration="anund inch e"),
    WordPair(id=204, armenian="Ինչպե՞ս ես", persian="چطوری", transliteration="inchpes es"),
    WordPair(id=205, armenian="Ե՞րբ", persian="کِی", transliteration="erb"),
    # Daily greetings
    WordPair(id=206, armenian="Բարի լույս", persian="صبح بخیر", transliteration="bari luys"),
    WordPair(id=207, armenian="Բարի օր", persian="روز بخیر", transliteration="bari or"),
    WordPair(id=208, armenian="Բարի գիշեր", persian="شب بخیر", transliteration="bari gisher"),
    WordPair(id=209, armenian="Ցտեսություն", persian="خداحافظ", transliteration="tstesutyun"),
    # Useful phrases
    WordPair(id=210, armenian="Չեմ հասկանում", persian="نمی‌فهمم", transliteration="chem haskanum"),
    WordPair(id=211, armenian="Կարո՞ղ եմ", persian="می‌توانم؟", transliteration="karogh em"),
    WordPair(id=212, armenian="Շատ լավ", persian="خیلی خوب", transliteration="shat lav"),
    WordPair(id=213, armenian="Շատ թանկ է", persian="خیلی گران است", transliteration="shat tank e"),
    WordPair(id=214, armenian="Ներողություն", persian="ببخشید", transliteration="neroghutyun"),
    WordPair(id=215, armenian="Ես չգիտեմ", persian="نمی‌دانم", transliteration="es chgitem"),
    WordPair(id=216, armenian="Հաճելի է", persian="خوشحالم", transliteration="hacheli e"),
    WordPair(id=217, armenian="Օգնեք", persian="کمکم کنید", transliteration="ognek"),
    WordPair(id=218, armenian="Ուր ես", persian="کجایی", transliteration="ur es"),
]


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


# ============ LEVEL 1 LETTER CURRICULUM ============
#
# Letter-batch sequence for Level 1, Mayreni-primer-style: ordered so each
# batch unlocks a real "target word" (mama → mayr → arev → barev → ...).
# Words intentionally repeat across batches for reinforcement.
# letterIds reference the 1..39 ids in app/src/main/assets/seed/alphabet.json.

LETTER_CURRICULUM = LetterCurriculum(
    periodicReviewBatches=[4, 8],
    passThresholdPercent=100,
    hintTimeoutMs=8000,
    batches=[
        LetterBatch(
            index=1, round=1,
            letterIds=[1, 20, 22, 11],  # Ա, Մ, Ն, Ի
            targetWord=BatchWord(armenian="մամա", transliteration="mama", persian="ماما"),
            readableWords=[
                BatchWord(armenian="մամա", transliteration="mama", persian="ماما"),
                BatchWord(armenian="նա", transliteration="na", persian="او"),
                BatchWord(armenian="մի", transliteration="mi", persian="یک / نکن"),
                BatchWord(armenian="ինա", transliteration="ina", persian="Ina (نام)"),
                BatchWord(armenian="ման", transliteration="man", persian="جستجو"),
            ],
        ),
        LetterBatch(
            index=2, round=1,
            letterIds=[5, 32, 21, 29],  # Ե, Ր, Յ, Ս
            targetWord=BatchWord(armenian="մայր", transliteration="mayr", persian="مادر"),
            readableWords=[
                BatchWord(armenian="մայր", transliteration="mayr", persian="مادر"),
                BatchWord(armenian="ես", transliteration="yes", persian="من"),
                BatchWord(armenian="սեր", transliteration="ser", persian="عشق"),
                BatchWord(armenian="սա", transliteration="sa", persian="این"),
                BatchWord(armenian="յար", transliteration="yar", persian="یار"),
                BatchWord(armenian="մամա", transliteration="mama", persian="ماما"),
                BatchWord(armenian="նա", transliteration="na", persian="او"),
            ],
        ),
        LetterBatch(
            index=3, round=1,
            letterIds=[16, 39, 31, 24],  # Հ, և, Տ, Ո
            targetWord=BatchWord(armenian="արև", transliteration="arev", persian="خورشید"),
            readableWords=[
                BatchWord(armenian="արև", transliteration="arev", persian="خورشید"),
                BatchWord(armenian="հայր", transliteration="hayr", persian="پدر"),
                BatchWord(armenian="հայ", transliteration="hay", persian="ارمنی"),
                BatchWord(armenian="հիմա", transliteration="hima", persian="الآن"),
                BatchWord(armenian="տես", transliteration="tes", persian="ببین"),
                BatchWord(armenian="սիրտ", transliteration="sirt", persian="قلب"),
                BatchWord(armenian="հա", transliteration="ha", persian="آره"),
                BatchWord(armenian="մայր", transliteration="mayr", persian="مادر"),
                BatchWord(armenian="սեր", transliteration="ser", persian="عشق"),
                BatchWord(armenian="ես", transliteration="yes", persian="من"),
            ],
        ),
        LetterBatch(
            index=4, round=1,
            letterIds=[34, 2, 15, 12],  # Ու, Բ, Կ, Լ
            targetWord=BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
            readableWords=[
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="տուն", transliteration="tun", persian="خانه"),
                BatchWord(armenian="բարի", transliteration="bari", persian="خوب / مهربان"),
                BatchWord(armenian="կամ", transliteration="kam", persian="هستم"),
                BatchWord(armenian="լույս", transliteration="luys", persian="نور"),
                BatchWord(armenian="կարմիր", transliteration="karmir", persian="قرمز"),
                BatchWord(armenian="մատ", transliteration="mat", persian="انگشت"),
                BatchWord(armenian="արև", transliteration="arev", persian="خورشید"),
                BatchWord(armenian="մայր", transliteration="mayr", persian="مادر"),
                BatchWord(armenian="հայր", transliteration="hayr", persian="پدر"),
            ],
        ),
        LetterBatch(
            index=5, round=2,
            letterIds=[26, 23, 25, 30],  # Պ, Շ, Չ, Վ
            targetWord=BatchWord(armenian="չորս", transliteration="chors", persian="چهار"),
            readableWords=[
                BatchWord(armenian="չորս", transliteration="chors", persian="چهار"),
                BatchWord(armenian="շուն", transliteration="shun", persian="سگ"),
                BatchWord(armenian="վարդ", transliteration="vard", persian="گل سرخ"),
                BatchWord(armenian="պապա", transliteration="papa", persian="بابا"),
                BatchWord(armenian="շատ", transliteration="shat", persian="خیلی"),
                BatchWord(armenian="վար", transliteration="var", persian="راندن"),
                BatchWord(armenian="պատ", transliteration="pat", persian="دیوار"),
                BatchWord(armenian="ապա", transliteration="apa", persian="پس"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="տուն", transliteration="tun", persian="خانه"),
            ],
        ),
        LetterBatch(
            index=6, round=2,
            letterIds=[4, 9, 18, 17],  # Դ, Թ, Ղ, Ձ
            targetWord=BatchWord(armenian="դուռ", transliteration="dur", persian="در"),
            readableWords=[
                BatchWord(armenian="դուռ", transliteration="dur", persian="در"),
                BatchWord(armenian="ձուկ", transliteration="dzuk", persian="ماهی"),
                BatchWord(armenian="դաս", transliteration="das", persian="درس"),
                BatchWord(armenian="դեմ", transliteration="dem", persian="مقابل"),
                BatchWord(armenian="թաթ", transliteration="tat", persian="پنجه"),
                BatchWord(armenian="թագ", transliteration="tag", persian="تاج"),
                BatchWord(armenian="ղեկ", transliteration="ghek", persian="سکّان"),
                BatchWord(armenian="մարդ", transliteration="mard", persian="انسان / مرد"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="տուն", transliteration="tun", persian="خانه"),
            ],
        ),
        LetterBatch(
            index=7, round=2,
            letterIds=[33, 27, 13, 28],  # Ց, Ջ, Խ, Ռ
            targetWord=BatchWord(armenian="ջուր", transliteration="jur", persian="آب"),
            readableWords=[
                BatchWord(armenian="ջուր", transliteration="jur", persian="آب"),
                BatchWord(armenian="ցավ", transliteration="tsav", persian="درد"),
                BatchWord(armenian="ցուրտ", transliteration="tsurt", persian="سرد"),
                BatchWord(armenian="խաղ", transliteration="khagh", persian="بازی"),
                BatchWord(armenian="ռադիո", transliteration="radio", persian="رادیو"),
                BatchWord(armenian="դուռ", transliteration="dur", persian="در"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
            ],
        ),
        LetterBatch(
            index=8, round=2,
            letterIds=[7, 8, 36, 37],  # Է, Ը, Ք, Օ
            targetWord=BatchWord(armenian="է", transliteration="e", persian="هست (فعل ربطی)"),
            readableWords=[
                BatchWord(armenian="է", transliteration="e", persian="هست"),
                BatchWord(armenian="օր", transliteration="or", persian="روز"),
                BatchWord(armenian="ընկեր", transliteration="ynker", persian="دوست"),
                BatchWord(armenian="քամի", transliteration="kami", persian="باد"),
                BatchWord(armenian="քեռի", transliteration="keri", persian="دایی"),
                BatchWord(armenian="քաղաք", transliteration="kaghak", persian="شهر"),
                BatchWord(armenian="էջ", transliteration="ej", persian="صفحه"),
                BatchWord(armenian="խոսք", transliteration="khosk", persian="سخن"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="ջուր", transliteration="jur", persian="آب"),
            ],
        ),
        LetterBatch(
            index=9, round=3,
            letterIds=[3, 10, 14, 19],  # Գ, Ժ, Ծ, Ճ
            targetWord=BatchWord(armenian="գիրք", transliteration="girk", persian="کتاب"),
            readableWords=[
                BatchWord(armenian="գիրք", transliteration="girk", persian="کتاب"),
                BatchWord(armenian="ծառ", transliteration="tsar", persian="درخت"),
                BatchWord(armenian="ճանապարհ", transliteration="chanaparh", persian="راه"),
                BatchWord(armenian="ժամ", transliteration="zham", persian="ساعت / زمان"),
                BatchWord(armenian="գարուն", transliteration="garun", persian="بهار"),
                BatchWord(armenian="ծով", transliteration="tsov", persian="دریا"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="ընկեր", transliteration="ynker", persian="دوست"),
            ],
        ),
        LetterBatch(
            index=10, round=3,
            letterIds=[6, 35, 38],  # Զ, Փ, Ֆ
            targetWord=BatchWord(armenian="փող", transliteration="pogh", persian="پول"),
            readableWords=[
                BatchWord(armenian="փող", transliteration="pogh", persian="پول"),
                BatchWord(armenian="ֆիլմ", transliteration="film", persian="فیلم"),
                BatchWord(armenian="զատիկ", transliteration="zatik", persian="کفش‌دوزک"),
                BatchWord(armenian="բարև", transliteration="barev", persian="سلام"),
                BatchWord(armenian="տուն", transliteration="tun", persian="خانه"),
                BatchWord(armenian="ջուր", transliteration="jur", persian="آب"),
                BatchWord(armenian="ընկեր", transliteration="ynker", persian="دوست"),
            ],
        ),
    ],
)


LETTERS: List[Letter] = [
    Letter(id=1,  orderIndex=1,  upper="Ա",  lower="ա",  name="այբ",   nameLatin="ayb",   pronunciationFa="آ",                       ipa="/a/",    exampleArmenian="արև",          exampleLatin="arev",       exampleFa="خورشید"),
    Letter(id=2,  orderIndex=2,  upper="Բ",  lower="բ",  name="բեն",   nameLatin="ben",   pronunciationFa="ب",                       ipa="/b/",    exampleArmenian="բարև",         exampleLatin="barev",      exampleFa="سلام"),
    Letter(id=3,  orderIndex=3,  upper="Գ",  lower="գ",  name="գիմ",   nameLatin="gim",   pronunciationFa="گ",                       ipa="/g/",    exampleArmenian="գիրք",         exampleLatin="girk",       exampleFa="کتاب"),
    Letter(id=4,  orderIndex=4,  upper="Դ",  lower="դ",  name="դա",    nameLatin="da",    pronunciationFa="د",                       ipa="/d/",    exampleArmenian="դուռ",         exampleLatin="dur",        exampleFa="در"),
    Letter(id=5,  orderIndex=5,  upper="Ե",  lower="ե",  name="եչ",    nameLatin="yech",  pronunciationFa="یه (اول کلمه) / اِ",        ipa="/jɛ/",   exampleArmenian="երկու",        exampleLatin="yerku",      exampleFa="دو"),
    Letter(id=6,  orderIndex=6,  upper="Զ",  lower="զ",  name="զա",    nameLatin="za",    pronunciationFa="ز",                       ipa="/z/",    exampleArmenian="զատիկ",        exampleLatin="zatik",      exampleFa="گل سرخی / کفش‌دوزک"),
    Letter(id=7,  orderIndex=7,  upper="Է",  lower="է",  name="է",     nameLatin="eh",    pronunciationFa="اِ",                      ipa="/ɛ/",    exampleArmenian="էջ",           exampleLatin="ej",         exampleFa="صفحه"),
    Letter(id=8,  orderIndex=8,  upper="Ը",  lower="ը",  name="ըթ",    nameLatin="et",    pronunciationFa="ـِ کوتاه (schwa)",          ipa="/ə/",    exampleArmenian="ընկեր",        exampleLatin="ynker",      exampleFa="دوست"),
    Letter(id=9,  orderIndex=9,  upper="Թ",  lower="թ",  name="թո",    nameLatin="to",    pronunciationFa="ت (پرتنش)",               ipa="/tʰ/",   exampleArmenian="թագ",          exampleLatin="tag",        exampleFa="تاج"),
    Letter(id=10, orderIndex=10, upper="Ժ",  lower="ժ",  name="ժե",    nameLatin="zhe",   pronunciationFa="ژ",                       ipa="/ʒ/",    exampleArmenian="ժամ",          exampleLatin="zham",       exampleFa="ساعت"),
    Letter(id=11, orderIndex=11, upper="Ի",  lower="ի",  name="ինի",   nameLatin="ini",   pronunciationFa="ای",                      ipa="/i/",    exampleArmenian="ինը",          exampleLatin="iny",        exampleFa="نُه"),
    Letter(id=12, orderIndex=12, upper="Լ",  lower="լ",  name="լյուն", nameLatin="liwn",  pronunciationFa="ل",                       ipa="/l/",    exampleArmenian="լույս",        exampleLatin="luys",       exampleFa="نور"),
    Letter(id=13, orderIndex=13, upper="Խ",  lower="խ",  name="խե",    nameLatin="kheh",  pronunciationFa="خ",                       ipa="/x/",    exampleArmenian="խաղող",        exampleLatin="khaghogh",   exampleFa="انگور"),
    Letter(id=14, orderIndex=14, upper="Ծ",  lower="ծ",  name="ծա",    nameLatin="tsa",   pronunciationFa="تْس (ساده)",               ipa="/ts/",   exampleArmenian="ծառ",          exampleLatin="tsar",       exampleFa="درخت"),
    Letter(id=15, orderIndex=15, upper="Կ",  lower="կ",  name="կեն",   nameLatin="ken",   pronunciationFa="ک (ساده)",                ipa="/k/",    exampleArmenian="կատու",        exampleLatin="katu",       exampleFa="گربه"),
    Letter(id=16, orderIndex=16, upper="Հ",  lower="հ",  name="հո",    nameLatin="ho",    pronunciationFa="ه",                       ipa="/h/",    exampleArmenian="հայր",         exampleLatin="hayr",       exampleFa="پدر"),
    Letter(id=17, orderIndex=17, upper="Ձ",  lower="ձ",  name="ձա",    nameLatin="dza",   pronunciationFa="دْز",                      ipa="/dz/",   exampleArmenian="ձուկ",         exampleLatin="dzuk",       exampleFa="ماهی"),
    Letter(id=18, orderIndex=18, upper="Ղ",  lower="ղ",  name="ղատ",   nameLatin="ghat",  pronunciationFa="غ",                       ipa="/ɣ/",    exampleArmenian="ղեկ",          exampleLatin="ghek",       exampleFa="سکّان"),
    Letter(id=19, orderIndex=19, upper="Ճ",  lower="ճ",  name="ճե",    nameLatin="cheh",  pronunciationFa="چ (ساده)",                ipa="/tʃ/",   exampleArmenian="ճանապարհ",     exampleLatin="chanaparh",  exampleFa="راه"),
    Letter(id=20, orderIndex=20, upper="Մ",  lower="մ",  name="մեն",   nameLatin="men",   pronunciationFa="م",                       ipa="/m/",    exampleArmenian="մայր",         exampleLatin="mayr",       exampleFa="مادر"),
    Letter(id=21, orderIndex=21, upper="Յ",  lower="յ",  name="հի",    nameLatin="hi",    pronunciationFa="ی",                       ipa="/j/",    exampleArmenian="յոթ",          exampleLatin="yot",        exampleFa="هفت"),
    Letter(id=22, orderIndex=22, upper="Ն",  lower="ն",  name="նու",   nameLatin="nu",    pronunciationFa="ن",                       ipa="/n/",    exampleArmenian="նարինջ",       exampleLatin="narinj",     exampleFa="پرتقال"),
    Letter(id=23, orderIndex=23, upper="Շ",  lower="շ",  name="շա",    nameLatin="sha",   pronunciationFa="ش",                       ipa="/ʃ/",    exampleArmenian="շուն",         exampleLatin="shun",       exampleFa="سگ"),
    Letter(id=24, orderIndex=24, upper="Ո",  lower="ո",  name="ո",     nameLatin="vo",    pronunciationFa="وُ (اول کلمه «وُ»)",       ipa="/vɔ/",   exampleArmenian="ոսկի",         exampleLatin="voski",      exampleFa="طلا"),
    Letter(id=25, orderIndex=25, upper="Չ",  lower="չ",  name="չա",    nameLatin="cha",   pronunciationFa="چ (پرتنش)",               ipa="/tʃʰ/",  exampleArmenian="չորս",         exampleLatin="chors",      exampleFa="چهار"),
    Letter(id=26, orderIndex=26, upper="Պ",  lower="պ",  name="պե",    nameLatin="peh",   pronunciationFa="پ (ساده)",                ipa="/p/",    exampleArmenian="պատ",          exampleLatin="pat",        exampleFa="دیوار"),
    Letter(id=27, orderIndex=27, upper="Ջ",  lower="ջ",  name="ջե",    nameLatin="jheh",  pronunciationFa="ج",                       ipa="/dʒ/",   exampleArmenian="ջուր",         exampleLatin="jur",        exampleFa="آب"),
    Letter(id=28, orderIndex=28, upper="Ռ",  lower="ռ",  name="ռա",    nameLatin="ra",    pronunciationFa="ر (غلت‌دار، قوی)",         ipa="/r/",    exampleArmenian="ռադիո",        exampleLatin="radio",      exampleFa="رادیو"),
    Letter(id=29, orderIndex=29, upper="Ս",  lower="ս",  name="սե",    nameLatin="se",    pronunciationFa="س",                       ipa="/s/",    exampleArmenian="սեր",          exampleLatin="ser",        exampleFa="عشق"),
    Letter(id=30, orderIndex=30, upper="Վ",  lower="վ",  name="վև",    nameLatin="vew",   pronunciationFa="و (مثل v)",               ipa="/v/",    exampleArmenian="վարդ",         exampleLatin="vard",       exampleFa="گل سرخ"),
    Letter(id=31, orderIndex=31, upper="Տ",  lower="տ",  name="տյուն", nameLatin="tiwn",  pronunciationFa="ت (ساده)",                ipa="/t/",    exampleArmenian="տուն",         exampleLatin="tun",        exampleFa="خانه"),
    Letter(id=32, orderIndex=32, upper="Ր",  lower="ր",  name="րե",    nameLatin="reh",   pronunciationFa="ر (سبک، تقه‌ای)",          ipa="/ɾ/",    exampleArmenian="մարդ",         exampleLatin="mard",       exampleFa="انسان / مرد"),
    Letter(id=33, orderIndex=33, upper="Ց",  lower="ց",  name="ցո",    nameLatin="tso",   pronunciationFa="تْس (پرتنش)",              ipa="/tsʰ/",  exampleArmenian="ցուրտ",        exampleLatin="tsurt",      exampleFa="سرد"),
    Letter(id=34, orderIndex=34, upper="Ու", lower="ու", name="ու",    nameLatin="u",     pronunciationFa="او",                      ipa="/u/",    exampleArmenian="ուտել",        exampleLatin="utel",       exampleFa="خوردن"),
    Letter(id=35, orderIndex=35, upper="Փ",  lower="փ",  name="փյուր", nameLatin="piwr",  pronunciationFa="پ (پرتنش)",               ipa="/pʰ/",   exampleArmenian="փող",          exampleLatin="pogh",       exampleFa="پول"),
    Letter(id=36, orderIndex=36, upper="Ք",  lower="ք",  name="քե",    nameLatin="keh",   pronunciationFa="ک (پرتنش)",               ipa="/kʰ/",   exampleArmenian="քաղաք",        exampleLatin="kaghak",     exampleFa="شهر"),
    Letter(id=37, orderIndex=37, upper="Օ",  lower="օ",  name="օ",     nameLatin="oh",    pronunciationFa="اُ",                      ipa="/o/",    exampleArmenian="օր",           exampleLatin="or",         exampleFa="روز"),
    Letter(id=38, orderIndex=38, upper="Ֆ",  lower="ֆ",  name="ֆե",    nameLatin="feh",   pronunciationFa="ف",                       ipa="/f/",    exampleArmenian="ֆիլմ",         exampleLatin="film",       exampleFa="فیلم"),
    Letter(id=39, orderIndex=39, upper="ԵՒ", lower="և",  name="և",     nameLatin="ev",    pronunciationFa="اِو (= «و» ربط)",          ipa="/ev/",   exampleArmenian="հայր և մայր",  exampleLatin="hayr ev mayr",exampleFa="پدر و مادر"),
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


@router.get("/vocabulary", response_model=List[WordPair])
def get_vocabulary():
    """Get the vocabulary word pairs for the matching game."""
    return VOCABULARY


@router.get("/sentences", response_model=List[WordPair])
def get_sentences():
    """Get short sentence pairs for the sentence matching game."""
    return SENTENCES


@router.get("/letter-curriculum", response_model=LetterCurriculum)
def get_letter_curriculum():
    """Level 1 letter-batch sequence with target words, readable words, and review batches."""
    return LETTER_CURRICULUM


@router.get("/letters", response_model=List[Letter])
def get_letters():
    """All 39 Armenian letters with name, pronunciation, IPA, and example word."""
    return LETTERS
