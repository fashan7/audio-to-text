from faster_whisper import WhisperModel
import os
import tempfile
import subprocess
from typing import Optional


SUPPORTED_FORMATS = {
    # Audio formats
    ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma",
    # Video formats
    ".mp4", ".webm", ".mov", ".avi", ".mkv", ".wmv",
}

DEFAULT_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")


def _compress_to_audio(input_path: str) -> str:
    """
    Use ffmpeg to extract and compress audio from any audio/video file.
    Output: 16kHz mono WAV — exactly what Whisper expects internally.
    This reduces a 300MB video to ~5MB audio in seconds.
    """
    output_path = input_path + "_compressed.wav"
    cmd = [
        "ffmpeg",
        "-y",                    # overwrite output if exists
        "-i", input_path,        # input file
        "-vn",                   # drop video stream entirely
        "-acodec", "pcm_s16le",  # uncompressed PCM (fastest for Whisper to decode)
        "-ar", "16000",          # 16kHz sample rate (Whisper's native rate)
        "-ac", "1",              # mono channel
        "-loglevel", "error",    # suppress ffmpeg noise in logs
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg compression failed: {result.stderr}")
    return output_path


class WhisperService:
    def __init__(self):
        self.model = None
        self.model_size = DEFAULT_MODEL_SIZE

    def load_model(self):
        print(f"[Whisper] Loading model: {self.model_size} ...")
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
            raise RuntimeError("Whisper model is not loaded.")

        suffix = os.path.splitext(filename)[-1].lower()
        if suffix not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format '{suffix}'. "
                f"Supported: {', '.join(SUPPORTED_FORMATS)}"
            )

        # Write uploaded file to a temp file
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        compressed_path = None
        try:
            # Auto-compress: extract & downsample audio before transcription
            print(f"[Whisper] Compressing '{filename}' ({len(file_bytes) / 1_000_000:.1f} MB)...")
            compressed_path = _compress_to_audio(tmp_path)
            compressed_size = os.path.getsize(compressed_path)
            print(f"[Whisper] Compressed to {compressed_size / 1_000_000:.1f} MB — starting transcription...")

            options = {}
            if language:
                options["language"] = language

            segments_gen, info = self.model.transcribe(compressed_path, **options)

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

            print(f"[Whisper] Transcription complete. Language: {info.language}, Duration: {info.duration:.1f}s")

            return {
                "text": " ".join(full_text_parts),
                "language": info.language,
                "duration": round(info.duration, 2),
                "segments": segments,
            }
        finally:
            # Always clean up both temp files
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            if compressed_path and os.path.exists(compressed_path):
                os.unlink(compressed_path)