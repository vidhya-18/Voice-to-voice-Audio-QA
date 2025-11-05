from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import uuid
from typing import Dict

from app.services.transcription import TranscriptionService
from app.services.qa_service import QAService
from app.services.tts_service import TTSService

# Global storage for audio context (in production, use Redis or database)
audio_context_storage: Dict[str, str] = {}

# Load environment variables
load_dotenv()

app = FastAPI(title="Voice Audio Q&A API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Initialize services (will be created on startup)
transcription_service = None
qa_service = None
tts_service = None

@app.on_event("startup")
async def startup_event():
    global transcription_service, qa_service, tts_service
    transcription_service = TranscriptionService(GROQ_API_KEY)
    qa_service = QAService(GROQ_API_KEY)
    tts_service = TTSService()


@app.get("/")
async def root():
    return {"message": "Voice Audio Q&A API is running"}


@app.get("/check-context/")
async def check_context():
    """
    Check if audio context exists for the session
    """
    session_id = "default_session"
    has_context = session_id in audio_context_storage
    context_preview = ""
    
    if has_context:
        context_preview = audio_context_storage[session_id][:200] + "..."
    
    return {
        "has_context": has_context,
        "session_id": session_id,
        "context_preview": context_preview
    }


@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file and transcribe it
    """
    try:
        # Validate file type
        allowed_extensions = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe audio
        transcription = transcription_service.transcribe_audio(file_path)
        
        # Store in global context with a session key
        session_id = "default_session"  # You can make this dynamic per user
        audio_context_storage[session_id] = transcription
        
        return {
            "success": True,
            "file_id": file_id,
            "session_id": session_id,
            "transcription": transcription,
            "message": "Audio uploaded and transcribed successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask-question/")
async def ask_question(file: UploadFile = File(...)):
    """
    Upload voice question and get voice response
    """
    try:
        # Check if audio context exists
        session_id = "default_session"
        if session_id not in audio_context_storage:
            raise HTTPException(
                status_code=400,
                detail="No audio context found. Please upload an audio file first."
            )
        
        # Save question audio
        question_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix.lower()
        question_path = os.path.join(UPLOAD_DIR, f"question_{question_id}{file_extension}")
        
        with open(question_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe question
        question_text = transcription_service.transcribe_question(question_path)
        
        # Set the context for QA service
        qa_service.set_audio_context(audio_context_storage[session_id])
        
        # Get answer from QA service
        answer_text = qa_service.answer_question(question_text)
        
        # Convert answer to speech
        response_audio_path = tts_service.text_to_speech(
            answer_text,
            f"response_{question_id}.mp3"
        )
        
        # Clean up question file
        os.remove(question_path)
        
        return {
            "success": True,
            "question": question_text,
            "answer": answer_text,
            "audio_file": response_audio_path
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download-response/{filename}")
async def download_response(filename: str):
    """
    Download the generated response audio
    """
    file_path = os.path.join("outputs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)