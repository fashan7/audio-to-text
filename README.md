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

You need **Python 3.11** and **ffmpeg** installed before running this project.

---

#### Python 3.11

> ⚠️ Python 3.12+ may work but **Python 3.14 will not** — ML packages (torch, whisper) don't support it yet. Python 3.11 is recommended.

**macOS** (via pyenv — recommended)
```bash
brew install pyenv
pyenv install 3.11.9
pyenv local 3.11.9       # sets Python 3.11 for this project folder only
```

Add pyenv to your shell if you haven't already:
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

**Linux**
```bash
sudo apt install python3.11 python3.11-venv   # Debian/Ubuntu
sudo dnf install python3.11                    # Fedora/RHEL
```

**Windows**
Download Python 3.11 directly from [python.org/downloads](https://www.python.org/downloads/)

---

#### ffmpeg

Required for audio extraction and compression from video files.

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
# Or download from https://ffmpeg.org/download.html and add to PATH
```

Verify both are installed:
```bash
python --version   # should show 3.11.x
ffmpeg -version    # should show ffmpeg version info
```

### 1. Clone & set up environment

```bash
git clone <your-repo-url>
cd player2text

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Upgrade build tools first — skipping this causes install failures
pip install --upgrade pip setuptools wheel

pip install -r requirements.txt
```

> 💡 **Troubleshooting installs:** If you see `No module named 'pkg_resources'`, run `pip install --upgrade pip setuptools wheel` and retry.

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