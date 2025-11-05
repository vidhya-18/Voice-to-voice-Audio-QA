from groq import Groq


class QAService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.audio_context = None
    
    def set_audio_context(self, transcription: str):
        """
        Store the transcription of uploaded audio as context
        """
        self.audio_context = transcription
    
    def answer_question(self, question: str) -> str:
        """
        Answer user's question based on audio context using Groq
        """
        if not self.audio_context:
            return "Please upload an audio file first."
        
        try:
            prompt = f"""You are a helpful assistant that answers questions about audio content.

Audio Content:
{self.audio_context}

User Question: {question}

Please provide a clear, concise answer based on the audio content above. If the question cannot be answered from the audio content, politely say so."""

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions about audio transcriptions accurately and concisely."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            
            return chat_completion.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Question answering failed: {str(e)}")