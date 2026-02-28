from fastapi import Depends

from app.clients.llm import LLMClient, get_llm_client
from app.services.audio import AudioService
from app.services.cache import CacheService
from app.services.file_parser import FileParser
from app.services.summarizer import SummarizerService


def get_cache_service() -> CacheService:
    return CacheService()


def get_audio_service() -> AudioService:
    return AudioService()


def get_file_parser() -> FileParser:
    return FileParser()


def get_summarizer_service(
    client: LLMClient = Depends(get_llm_client),
    cache: CacheService = Depends(get_cache_service),
) -> SummarizerService:
    return SummarizerService(llm=client, cache=cache)
