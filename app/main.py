import hashlib
import os
import subprocess
import tempfile
import time
import wave
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from faster_whisper import WhisperModel
from piper import PiperVoice
from rapidfuzz.distance import Levenshtein

from app.lessons import router as lessons_router
from app.admin import router as admin_router
from app.curriculum import router as curriculum_router
from app.database import init_db

MODEL_DIR = Path(os.getenv("MODEL_DIR", "/app/models"))
PIPER_MODEL_PATH = MODEL_DIR / "hy_AM-gor-medium.onnx"
PIPER_VOICE_ID = "hy_AM-gor-medium"
CACHE_DIR = Path(os.getenv("AUDIO_CACHE_DIR", "/app/audio_cache"))
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
WHISPER_DOWNLOAD_ROOT = os.getenv("WHISPER_DOWNLOAD_ROOT", "/app/whisper_cache")

CACHE_DIR.mkdir(parents=True, exist_ok=True)

piper_voice = PiperVoice.load(str(PIPER_MODEL_PATH))
whisper_model = WhisperModel(
    WHISPER_MODEL_NAME,
    device="cpu",
    compute_type=WHISPER_COMPUTE_TYPE,
    download_root=WHISPER_DOWNLOAD_ROOT,
)

app = FastAPI(title="learnarm-api", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(lessons_router)
app.include_router(admin_router)
app.include_router(curriculum_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "models": {
            "tts": f"piper:{PIPER_VOICE_ID}",
            "stt": f"faster-whisper:{WHISPER_MODEL_NAME}:{WHISPER_COMPUTE_TYPE}",
        },
    }


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    voice: str = "hy-default"


def _cache_key(text: str, voice: str) -> str:
    return hashlib.sha256(f"{voice}::{text}".encode("utf-8")).hexdigest()


def _wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-qscale:a", "4",
            str(mp3_path),
        ],
        check=True,
        capture_output=True,
    )


def _synthesize_to_mp3(text: str, mp3_path: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = Path(tmp.name)
    try:
        with wave.open(str(wav_path), "wb") as wav_file:
            # Tuning for clarity on hy_AM-gor-medium, which renders initial labial
            # consonants (m / b / p) muddly at default settings:
            #   length_scale > 1.0 = slower speech, sharper consonants
            #   noise_scale < default (~0.667) = more consistent voice
            #   noise_w < default (~0.8) = less duration jitter
            piper_voice.synthesize(
                text,
                wav_file,
                length_scale=1.2,
                noise_scale=0.5,
                noise_w=0.7,
            )
        _wav_to_mp3(wav_path, mp3_path)
    finally:
        wav_path.unlink(missing_ok=True)


@app.post("/tts")
def tts(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "text is empty after strip")
    key = _cache_key(text, req.voice)
    mp3_path = CACHE_DIR / f"{key}.mp3"
    if not mp3_path.exists():
        try:
            _synthesize_to_mp3(text, mp3_path)
        except subprocess.CalledProcessError as e:
            raise HTTPException(500, f"ffmpeg failed: {e.stderr.decode(errors='ignore')[:200]}")
    return Response(
        content=mp3_path.read_bytes(),
        media_type="audio/mpeg",
        headers={"X-Cache-Key": key},
    )


def _save_upload(upload: UploadFile, suffix: str = ".wav") -> Path:
    inferred = Path(upload.filename or "audio").suffix or suffix
    with tempfile.NamedTemporaryFile(suffix=inferred, delete=False) as tmp:
        tmp.write(upload.file.read())
        return Path(tmp.name)


@app.post("/stt")
async def stt(audio: UploadFile = File(...), language: str = Form(default="hy")):
    t0 = time.time()
    audio_path = _save_upload(audio)
    try:
        segments, info = whisper_model.transcribe(
            str(audio_path),
            language=language or None,
            beam_size=5,
            vad_filter=False,
        )
        text = "".join(s.text for s in segments).strip()
        if info.duration:
            duration_ms = int(info.duration * 1000)
        else:
            duration_ms = int((time.time() - t0) * 1000)
        return {
            "text": text,
            "language": info.language or language,
            "duration_ms": duration_ms,
        }
    finally:
        audio_path.unlink(missing_ok=True)


def _normalize_armenian(s: str) -> str:
    s = s.strip().lower()
    return "".join(c for c in s if "԰" <= c <= "֏")


def _feedback(score: float) -> str:
    if score >= 0.95:
        return "عالی"
    if score >= 0.80:
        return "خوب"
    if score >= 0.60:
        return "نزدیک"
    return "دوباره"


@app.post("/pronunciation-score")
async def pronunciation_score(
    audio: UploadFile = File(...),
    target: str = Form(...),
):
    audio_path = _save_upload(audio)
    try:
        segments, _ = whisper_model.transcribe(
            str(audio_path),
            language="hy",
            beam_size=5,
            vad_filter=False,
        )
        recognized_raw = "".join(s.text for s in segments).strip()
        t_norm = _normalize_armenian(target)
        r_norm = _normalize_armenian(recognized_raw)
        if not t_norm or not r_norm:
            score = 0.0
        else:
            dist = Levenshtein.distance(t_norm, r_norm)
            score = max(0.0, 1.0 - dist / max(len(t_norm), len(r_norm)))
        return {
            "target": target,
            "recognized": recognized_raw,
            "score": round(score, 2),
            "feedback": _feedback(score),
        }
    finally:
        audio_path.unlink(missing_ok=True)
