from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes.transcribe import router as transcribe_router
from app.services.whisper_service import WhisperService
import os

whisper_service = WhisperService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the Whisper model once at startup
    whisper_service.load_model()
    yield
    # Cleanup on shutdown (optional)


app = FastAPI(
    title="Audio-to-Text API",
    description="Transcribe audio files using OpenAI Whisper (local)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allows your Lovable frontend to call this API
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router, prefix="/api/v1", tags=["Transcription"])


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "model_loaded": whisper_service.is_loaded(),
        "model_size": whisper_service.model_size,
    }