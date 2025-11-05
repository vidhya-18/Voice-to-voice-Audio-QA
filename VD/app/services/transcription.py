import os
from groq import Groq
from pathlib import Path


class TranscriptionService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using Groq's Whisper API
        """
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(Path(audio_file_path).name, file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                    language="en",
                    temperature=0.0
                )
            return transcription
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_question(self, question_audio_path: str) -> str:
        """
        Transcribe user's question audio
        """
        return self.transcribe_audio(question_audio_path)