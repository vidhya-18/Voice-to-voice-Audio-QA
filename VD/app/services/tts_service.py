from gtts import gTTS
import os
from pathlib import Path


class TTSService:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def text_to_speech(self, text: str, output_filename: str = "response.mp3") -> str:
        """
        Convert text to speech and save as audio file
        """
        try:
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Create speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            
            return output_path
        
        except Exception as e:
            raise Exception(f"Text-to-speech conversion failed: {str(e)}")