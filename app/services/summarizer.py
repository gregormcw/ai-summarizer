from datetime import datetime, timezone
from typing import AsyncGenerator, Optional

from app.clients.llm import LLMClient
from app.core.config import get_settings
from app.core.logging import logger
from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.prompts.loader import build_user_prompt, load_system_prompt
from app.services.cache import CacheService


class SummarizerService:
    def __init__(self, llm: LLMClient, cache: CacheService):
        self.llm = llm
        self.cache = cache
        settings = get_settings()
        self.max_tokens = settings.max_tokens
        self.model = settings.model

    async def summarize(self, summarize_request: SummarizeRequest) -> SummaryResponse:
        cached_summary: Optional[dict] = self.cache.get(
            text=summarize_request.text,
            style=summarize_request.style,
            max_length=summarize_request.max_length,
        )

        if cached_summary:
            logger.info("Cache hit - returning cached summary.")
            return SummaryResponse(**cached_summary)

        logger.info("Cache miss.")
        system_prompt = load_system_prompt()
        user_prompt = build_user_prompt(
            text=summarize_request.text,
            style=summarize_request.style,
            max_length=summarize_request.max_length,
        )

        summary = await self.llm.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=self.max_tokens,
        )

        response_data = {
            "summary": summary,
            "style": summarize_request.style,
            "model": self.model,
            "prompt_length": len(summarize_request.text.split()),
            "summary_length": len(summary.split()),
        }

        self.cache.set(
            text=summarize_request.text,
            style=summarize_request.style,
            max_length=summarize_request.max_length,
            summary_data=response_data,
        )

        return SummaryResponse(**response_data, summary_ts=datetime.now(timezone.utc))

    async def summarize_stream(
        self, summarize_request: SummarizeRequest
    ) -> AsyncGenerator[str, None]:
        system_prompt = load_system_prompt()
        user_prompt = build_user_prompt(
            text=summarize_request.text,
            style=summarize_request.style,
            max_length=summarize_request.max_length,
        )
        async for text in self.llm.stream(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=self.max_tokens,
        ):
            yield text
