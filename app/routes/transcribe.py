from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from app.services.whisper_service import SUPPORTED_FORMATS
from app.dependencies import whisper_service
from typing import Optional
import os

router = APIRouter()

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 50))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio or video file to transcribe"),
    language: Optional[str] = Form(
        None,
        description="Optional language code (e.g. 'en', 'fr'). Auto-detected if omitted.",
    ),
):
    suffix = os.path.splitext(file.filename or "")[-1].lower()
    if suffix not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{suffix}'. Accepted: {', '.join(SUPPORTED_FORMATS)}",
        )

    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = whisper_service.transcribe(
            file_bytes=file_bytes,
            filename=file.filename or "audio.mp3",
            language=language or None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    return JSONResponse(content={
        "success": True,
        "filename": file.filename,
        "transcription": result,
    })


@router.get("/formats")
def supported_formats():
    return {"supported_formats": sorted(SUPPORTED_FORMATS)}