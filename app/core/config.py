from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "ai-summarizer"
    description: str = (
        "AI summarization app offering full end-to-end audio summarization via ASR and TTS"
    )
    version: str = "0.1.0"
    max_chars: int = 20_000
    debug: bool = False

    # LLM settings
    llm_provider: str = "anthropic"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1024

    # OpenAI (for audio features)
    openai_api_key: str | None = None
    whisper_model: str = "whisper-1"
    tts_model: str = "tts-1"
    tts_voice: str = "alloy"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_enabled: bool = True
    cache_ttl: int = 86400  # 24 hours in seconds

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
