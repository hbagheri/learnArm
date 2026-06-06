# LearnArm Backend

FastAPI service providing TTS (Text-to-Speech), STT (Speech-to-Text), and pronunciation scoring for the LearnArm language-learning app.

## Features

- **TTS** — Armenian text → MP3 audio (Piper, hy_AM-gor-medium)
- **STT** — Audio recording → Armenian text (faster-whisper, small model, int8)
- **Pronunciation Scoring** — Compares user speech against target using Levenshtein distance
- **Content Versioning** — Versioned lesson packs (JSON)
- **Audio Caching** — Cache MP3s to reduce TTS calls

## API

### Health Check
```
GET /health
→ { "status": "ok", "models": {...} }
```

### Text-to-Speech
```
POST /tts
Body: { "text": "բարև", "voice": "hy_AM-gor-medium" }
→ audio/mpeg (MP3 bytes)
```

### Speech-to-Text + Scoring
```
POST /pronunciation-score
Multipart:
  - audio: m4a file
  - target: Armenian text (e.g., "բարև")
→ {
  "score": 0.85,
  "recognized": "բարեվ",
  "feedback": "خوب"  (Persian)
}
```

### Content Version
```
GET /content/version
→ { "version": 1, "updated_at": "2026-06-06T..." }
```

### Lesson Content
```
GET /content/lessons
→ {
  "version": 1,
  "lessons": [
    {
      "id": "lesson_1",
      "title": "الفبا — قسمت ۱",
      "steps": [
        { "type": "SHOW_LETTER", "itemKey": "letter:1", ... },
        ...
      ]
    }
  ]
}
```

## Setup

### Prerequisites
- Python 3.11+
- `pip install -r requirements.txt`

Models are downloaded at startup (first run takes ~10 minutes):
- Piper TTS model (~800 MB)
- faster-whisper model (~400 MB)

### Installation
```bash
pip install -r requirements.txt
```

### Running
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker
```bash
docker build -t learnarm-api .
docker run -p 8000:8000 learnarm-api
```

## Environment

- **PIPER_MODEL**: Piper model name (default: `hy_AM-gor-medium`)
- **WHISPER_MODEL**: faster-whisper model (default: `small`)
- **CACHE_DIR**: Audio cache directory (default: `./audio_cache`)

## Performance

- **TTS latency**: ~1–2 sec (CPU only, model cached)
- **STT latency**: ~2–5 sec (depending on audio length)
- **Score latency**: ~100 ms

## Structure

```
app/
  main.py      — FastAPI app + routes
  lessons.py   — Content (5 lessons, 112 steps)
requirements.txt
```

## License

Personal project. All rights reserved.
