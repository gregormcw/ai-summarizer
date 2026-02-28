import io

from openai import OpenAI

from app.core.config import get_settings


class AudioService:
    """Handle audio transcription and text-to-speech."""

    def __init__(self):
        # Initialize OpenAI client with API key
        # Store model settings
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.whisper_model = settings.whisper_model
        self.tts_model = settings.tts_model
        self.tts_voice = settings.tts_voice

    def transcribe(self, audio_data: bytes, filename: str) -> str:
        """Transcribe audio to text using Whisper."""
        audio_buffer = io.BytesIO(audio_data)
        audio_buffer.name = filename

        transcription = self.client.audio.transcriptions.create(
            file=audio_buffer,
            model=self.whisper_model,
        )
        return transcription.text

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech audio"""
        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.tts_voice,
            input=text,
            instructions="Speak in a cheerful and positive tone.",
        )
        return response.content
