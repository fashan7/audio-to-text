# 🎙️ player2text

A local, privacy-friendly audio & video transcription API built with **FastAPI** and **faster-whisper**.  
No cloud API keys needed — everything runs on your machine.

---

## ✨ Features

- 🎬 **Audio & video support** — mp3, mp4, mov, avi, mkv, wav, and more
- ⚡ **Auto-compression** — videos are stripped to audio and downsampled to 16kHz before transcription (a 300MB video becomes ~5MB)
- 🌍 **Auto language detection** — or specify a language manually
- 🕐 **Timestamped segments** — full transcript broken into timed chunks
- 🔒 **100% local** — no data leaves your machine

---

## 🚀 Quick Start

### 0. Prerequisites

Install `ffmpeg` — required for audio extraction and compression:

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
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

Verify:
```bash
ffmpeg -version
```

### 1. Clone & set up environment

```bash
git clone <your-repo-url>
cd player2text

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env as needed
```

### 3. Run the server

```bash
python run.py
```

API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Server & model status |
| `POST` | `/api/v1/transcribe` | Upload audio/video → get transcription |
| `GET`  | `/api/v1/formats` | List supported formats |

### POST `/api/v1/transcribe`

**Form data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `File` | ✅ | Audio or video file |
| `language` | `string` | ❌ | Language code e.g. `en`, `fr`. Auto-detected if omitted. |

**Example response:**
```json
{
  "success": true,
  "filename": "meeting.mp4",
  "transcription": {
    "text": "Hello and welcome to the project...",
    "language": "en",
    "duration": 462.74,
    "segments": [
      { "id": 1, "start": 0.0, "end": 9.5, "text": "Hello and welcome to the project." }
    ]
  }
}
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL_SIZE` | `base` | Model size: `tiny`, `base`, `small`, `medium`, `large` |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | CORS origins (comma-separated) |
| `MAX_FILE_SIZE_MB` | `50` | Max upload size in MB |

### Model Size Guide

| Size | Speed | Accuracy | RAM |
|------|-------|----------|-----|
| `tiny` | ⚡⚡⚡⚡ | ⭐⭐ | ~1 GB |
| `base` | ⚡⚡⚡ | ⭐⭐⭐ | ~1 GB |
| `small` | ⚡⚡ | ⭐⭐⭐⭐ | ~2 GB |
| `medium` | ⚡ | ⭐⭐⭐⭐⭐ | ~5 GB |
| `large` | 🐢 | ⭐⭐⭐⭐⭐ | ~10 GB |

---

## 🔄 How Auto-Compression Works

Before transcription, every uploaded file is passed through ffmpeg:

```
Upload (300MB .mp4) → ffmpeg extract audio → 16kHz mono .wav (~5MB) → Whisper
```

- **`-vn`** strips the video stream entirely
- **`-ar 16000`** downsamples to 16kHz (Whisper's native rate)
- **`-ac 1`** converts to mono

This makes transcription dramatically faster without any loss in accuracy.

---

## 📁 Project Structure

```
player2text/
├── app/
│   ├── main.py                  # FastAPI app, CORS, startup
│   ├── dependencies.py          # Shared whisper_service instance
│   ├── routes/
│   │   └── transcribe.py        # Upload & transcription endpoints
│   ├── services/
│   │   └── whisper_service.py   # Compression + Whisper transcription
│   └── utils/                   # Reserved for helpers
├── uploads/                     # Temp uploads (gitignored)
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## 🛡️ Supported Formats

| Type | Formats |
|------|---------|
| 🎵 Audio | `mp3` · `wav` · `m4a` · `ogg` · `flac` · `aac` · `wma` |
| 🎬 Video | `mp4` · `webm` · `mov` · `avi` · `mkv` · `wmv` |

---

## 📝 License

MIT