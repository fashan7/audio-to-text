# 🎙️ Audio-to-Text API

A local, privacy-friendly audio transcription API built with **FastAPI** and **OpenAI Whisper**.  
No cloud API keys needed — everything runs on your machine.

---

## 🚀 Quick Start

### 0. Prerequisites — Install `ffmpeg`

`ffmpeg` is required for all audio and video processing. Install it for your OS:

**macOS**
```bash
brew install ffmpeg
```

**Linux (Debian / Ubuntu)**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Linux (Fedora / RHEL)**
```bash
sudo dnf install ffmpeg
```

**Windows**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download the installer from https://ffmpeg.org/download.html
```

Verify the install:
```bash
ffmpeg -version
```

### 1. Clone & set up environment

```bash
git clone <your-repo-url>
cd audio-to-text

python -m venv .venv
source venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env as needed (model size, allowed origins, etc.)
```

### 3. Run the server

```bash
python run.py
```

The API will be available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Check server & model status |
| `POST` | `/api/v1/transcribe` | Upload audio and get transcription |
| `GET`  | `/api/v1/formats` | List supported audio formats |

### POST `/api/v1/transcribe`

**Form data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `File` | ✅ | Audio file to transcribe |
| `language` | `string` | ❌ | Language code (e.g. `en`, `fr`). Auto-detected if omitted. |

**Example response:**
```json
{
  "success": true,
  "filename": "meeting.mp3",
  "transcription": {
    "text": "Hello, this is a test transcription.",
    "language": "en",
    "duration": 3.42,
    "segments": [
      { "id": 0, "start": 0.0, "end": 3.42, "text": "Hello, this is a test transcription." }
    ]
  }
}
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL_SIZE` | `base` | Whisper model size: `tiny`, `base`, `small`, `medium`, `large` |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | CORS origins for frontend (comma-separated) |
| `MAX_FILE_SIZE_MB` | `50` | Max upload size in MB |

### Model Size Guide

| Size | Speed | Accuracy | RAM needed |
|------|-------|----------|------------|
| `tiny` | ⚡⚡⚡⚡ | ⭐⭐ | ~1 GB |
| `base` | ⚡⚡⚡ | ⭐⭐⭐ | ~1 GB |
| `small` | ⚡⚡ | ⭐⭐⭐⭐ | ~2 GB |
| `medium` | ⚡ | ⭐⭐⭐⭐⭐ | ~5 GB |
| `large` | 🐢 | ⭐⭐⭐⭐⭐ | ~10 GB |

---

## 🎨 Frontend (Lovable)

This API is built to connect with a Lovable-generated UI.  
When your Lovable app is deployed:

1. Add its URL to `ALLOWED_ORIGINS` in your `.env`
2. The UI posts to `POST /api/v1/transcribe` with `multipart/form-data`

---

## 📁 Project Structure

```
audio-to-text/
├── app/
│   ├── main.py                  # FastAPI app, CORS, startup
│   ├── routes/
│   │   └── transcribe.py        # Upload & transcription endpoints
│   ├── services/
│   │   └── whisper_service.py   # Whisper model loading & transcription
│   └── utils/                   # (reserved for helpers)
├── uploads/                     # Temp uploads (gitignored)
├── .env.example                 # Environment template
├── .gitignore
├── requirements.txt
├── run.py                       # Server entry point
└── README.md
```

---

## 🛡️ Supported Formats

| Type | Formats |
|------|---------|
| 🎵 Audio | `mp3` · `wav` · `m4a` · `ogg` · `flac` · `aac` · `wma` |
| 🎬 Video | `mp4` · `webm` · `mov` · `avi` · `mkv` · `wmv` |

> **Note:** `ffmpeg` is required for all formats (see Prerequisites above).  
> Whisper extracts the audio track from video files automatically — no manual conversion needed.

---

## 📝 License

MIT