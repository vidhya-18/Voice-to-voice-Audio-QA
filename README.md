# Voice-to-Voice Audio Q&A Assistant 🎙️

An interactive voice-based Q&A system that allows users to upload audio files, ask questions about the content through voice input, and receive voice responses. This project combines speech-to-text, natural language processing, and text-to-speech technologies to create a seamless voice interaction experience.

## Features 🌟

- **Audio File Processing**: Support for multiple audio formats (MP3, WAV, M4A, OGG, FLAC)
- **Voice-to-Voice Interaction**: Ask questions using voice and receive voice responses
- **Real-time Transcription**: View transcriptions of uploaded audio files
- **Interactive Q&A History**: Keep track of all questions and answers with playable responses
- **Modern Web Interface**: Built with Streamlit for a clean, responsive user experience

## Technology Stack 🛠️

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI/ML**:
  - Groq API for natural language processing
  - Whisper for Speech-to-Text conversion
  - gTTS (Google Text-to-Speech) for voice responses
- **Other Tools**:
  - Python 3.11+
  - Various audio processing libraries (pydub, soundfile)

## Prerequisites 📋

- Python 3.11 or higher
- Groq API key
- Git (for version control)

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/vidhya-18/Voice-to-voice-Audio-QA.git
   cd Voice-to-voice-Audio-QA
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_api_key_here
   ```

## Running the Application 🏃‍♂️

1. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. In a new terminal, start the Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open your browser and navigate to:
   - Frontend: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## Usage Guide 📖

1. **Upload Audio**:
   - Click the file uploader to select an audio file
   - Supported formats: MP3, WAV, M4A, OGG, FLAC
   - Click "Process Audio" to transcribe the content

2. **Ask Questions**:
   - Once audio is processed, use the microphone button to record your question
   - Click "Get Answer" to receive a voice response
   - View the question and answer in the Q&A History section

3. **View History**:
   - All Q&A interactions are saved in the session
   - Expand any Q&A pair to view details and replay audio responses
   - Use "Clear History" in the sidebar to reset

## Project Structure 📁

```
Voice-to-voice-Audio-QA/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── services/
│       ├── __init__.py
│       ├── qa_service.py
│       ├── transcription.py
│       └── tts_service.py
├── outputs/              # Generated audio responses
├── test_audio/          # Test audio files
├── uploads/             # Temporary upload directory
├── requirements.txt     # Project dependencies
├── streamlit_app.py     # Frontend application
└── README.md           # Project documentation
```

## Contributing 🤝

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License 📄

MIT License

## Contact 📧

- GitHub: [@vidhya-18](https://github.com/vidhya-18)

## Acknowledgments 🙏

- Groq API for providing the language model capabilities
- OpenAI's Whisper for speech recognition
- Google Text-to-Speech for voice synthesis
- Streamlit team for the amazing web framework