from typing import AsyncIterator

from app.clients.llm import LLMClient
from app.models.requests import SummarizeRequest
from app.services.summarizer import SummarizerService


class MockLLMClient(LLMClient):
    async def complete(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> str:
        return "This is a test summary."

    async def stream(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> AsyncIterator[str]:
        yield "This is a test summary."


class MockCacheService:
    """Mock cache that always returns None (cache miss)."""
    
    def get(self, text: str, style: str, max_length: int):
        return None  # Always cache miss for testing
    
    def set(self, text: str, style: str, max_length: int, summary_data: dict):
        pass  # Do nothing


PROMPT: str = (
    "The 2024-2025 season was Liverpool Football Club's 133rd season in their history and their 63rd "
    "consecutive season in the top flight of English football. In addition to the domestic league, the club "
    "also participated in the FA Cup, the EFL Cup, and the UEFA Champions League. This was Liverpool's first "
    "season under new head coach Arne Slot, who was announced as Jürgen Klopp's successor on 20 May 2024."
)

MAX_LENGTH = 200

mock_client = MockLLMClient()
mock_style = "paragraph"


async def test_summarize_returns_summary():
    request = SummarizeRequest(
        text=PROMPT,
        max_length=MAX_LENGTH,
        style=mock_style,
    )
    mock_cache = MockCacheService()
    service = SummarizerService(llm=mock_client, cache=mock_cache)
    summary = await service.summarize(request)
    assert isinstance(summary.summary, str) and summary.summary != ""


async def test_summarize_correct_style():
    request = SummarizeRequest(
        text=PROMPT,
        max_length=MAX_LENGTH,
        style=mock_style,
    )
    mock_cache = MockCacheService()
    service = SummarizerService(llm=mock_client, cache=mock_cache)
    summary = await service.summarize(request)
    assert summary.style == mock_style


async def test_summarize_word_counts():
    request = SummarizeRequest(
        text=PROMPT,
        max_length=MAX_LENGTH,
        style=mock_style,
    )
    mock_cache = MockCacheService()
    service = SummarizerService(llm=mock_client, cache=mock_cache)
    summary = await service.summarize(request)
    assert summary.prompt_length > 0 and summary.summary_length > 0
