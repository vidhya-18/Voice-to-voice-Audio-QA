import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Voice Audio Q&A",
    page_icon="🎙️",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'audio_uploaded' not in st.session_state:
    st.session_state.audio_uploaded = False
if 'transcription' not in st.session_state:
    st.session_state.transcription = ""
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

# Header
st.markdown('<div class="main-header">🎙️ Voice Audio Q&A Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload audio, ask questions via voice, get voice responses!</div>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Step 1: Upload Audio File")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Upload the audio file you want to ask questions about"
    )
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format=f'audio/{uploaded_file.type.split("/")[1]}')
        
        if st.button("🚀 Process Audio", type="primary", use_container_width=True):
            with st.spinner("Transcribing audio..."):
                try:
                    # Send file to API
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{API_URL}/upload-audio/", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.audio_uploaded = True
                        st.session_state.transcription = data['transcription']
                        st.success("✅ Audio processed successfully!")
                    else:
                        st.error(f"Error: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                    st.info("Make sure FastAPI server is running on http://localhost:8000")
    
    # Display transcription
    if st.session_state.audio_uploaded:
        st.subheader("📝 Audio Transcription")
        with st.expander("View transcription", expanded=False):
            st.text_area(
                "Transcription",
                value=st.session_state.transcription,
                height=200,
                disabled=True
            )

with col2:
    st.header("🎤 Step 2: Ask Questions")
    
    if not st.session_state.audio_uploaded:
        st.info("👈 Please upload and process an audio file first")
    else:
        st.success("✅ Ready to answer questions!")
        
        # Audio recorder
        st.subheader("Record your question:")
        audio_bytes = audio_recorder(
            pause_threshold=2.0,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("🤔 Get Answer", type="primary", use_container_width=True):
                with st.spinner("Processing your question..."):
                    try:
                        # Save audio bytes to file
                        temp_file = "temp_question.wav"
                        with open(temp_file, "wb") as f:
                            f.write(audio_bytes)
                        
                        # Send to API
                        with open(temp_file, "rb") as f:
                            files = {"file": (temp_file, f, "audio/wav")}
                            response = requests.post(f"{API_URL}/ask-question/", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Add to history
                            st.session_state.qa_history.append({
                                'question': data['question'],
                                'answer': data['answer'],
                                'audio_file': data['audio_file']
                            })
                            
                            # Clean up temp file
                            os.remove(temp_file)
                            
                            st.success("✅ Answer ready!")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Q&A History
if st.session_state.qa_history:
    st.header("💬 Q&A History")
    
    for i, qa in enumerate(reversed(st.session_state.qa_history)):
        with st.expander(f"Q{len(st.session_state.qa_history) - i}: {qa['question'][:100]}..."):
            st.markdown(f"**Question:** {qa['question']}")
            st.markdown(f"**Answer:** {qa['answer']}")
            
            # Play response audio
            filename = os.path.basename(qa['audio_file'])
            try:
                audio_response = requests.get(f"{API_URL}/download-response/{filename}")
                if audio_response.status_code == 200:
                    st.audio(audio_response.content, format="audio/mp3")
            except:
                st.warning("Audio response not available")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.markdown("""
    1. **Upload Audio**: Upload an audio file (MP3, WAV, etc.)
    2. **Process**: Click 'Process Audio' to transcribe
    3. **Ask Questions**: Record your voice question
    4. **Get Answer**: Receive voice response
    
    ---
    
    **Features:**
    - 🎙️ Voice-to-Voice interaction
    - 🤖 AI-powered Q&A
    - 📝 Audio transcription
    - 🔊 Text-to-Speech responses
    """)
    
    if st.button("🔄 Clear History", use_container_width=True):
        st.session_state.qa_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("- Groq API")
    st.markdown("- Whisper (Speech-to-Text)")
    st.markdown("- gTTS (Text-to-Speech)")