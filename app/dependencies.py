from app.services.whisper_service import WhisperService

# Single shared instance used by both main.py and routes
whisper_service = WhisperService()