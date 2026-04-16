from faster_whisper import WhisperModel
import os
import tempfile
from typing import Optional


SUPPORTED_FORMATS = {
    # Audio formats
    ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma",
    # Video formats (Whisper extracts the audio track via ffmpeg)
    ".mp4", ".webm", ".mov", ".avi", ".mkv", ".wmv",
}

# Available sizes: tiny, base, small, medium, large
DEFAULT_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")


class WhisperService:
    def __init__(self):
        self.model = None
        self.model_size = DEFAULT_MODEL_SIZE

    def load_model(self):
        """Load the faster-whisper model into memory. Called once at app startup."""
        print(f"[Whisper] Loading model: {self.model_size} ...")
        # device="cpu", compute_type="int8" works on any Mac/Linux/Windows, no GPU needed
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        print(f"[Whisper] Model '{self.model_size}' loaded successfully.")

    def is_loaded(self) -> bool:
        return self.model is not None

    def transcribe(
        self,
        file_bytes: bytes,
        filename: str,
        language: Optional[str] = None,
    ) -> dict:
        if not self.is_loaded():
            raise RuntimeError("Whisper model is not loaded. Call load_model() first.")

        suffix = os.path.splitext(filename)[-1].lower()
        if suffix not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format '{suffix}'. "
                f"Supported: {', '.join(SUPPORTED_FORMATS)}"
            )

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            options = {}
            if language:
                options["language"] = language

            segments_gen, info = self.model.transcribe(tmp_path, **options)

            segments = []
            full_text_parts = []
            for seg in segments_gen:
                segments.append({
                    "id": seg.id,
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip(),
                })
                full_text_parts.append(seg.text.strip())

            return {
                "text": " ".join(full_text_parts),
                "language": info.language,
                "duration": round(info.duration, 2),
                "segments": segments,
            }
        finally:
            os.unlink(tmp_path)