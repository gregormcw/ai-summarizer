from abc import ABC, abstractmethod
from typing import AsyncIterator

import anthropic

from app.core.config import get_settings


class LLMClient(ABC):
    @abstractmethod
    async def complete(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> str:
        pass

    @abstractmethod
    async def stream(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> AsyncIterator[str]:
        pass


class AnthropicClient(LLMClient):
    def __init__(self):
        settings = get_settings()
        self.model = settings.model
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def complete(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text

    async def stream(
        self, system_prompt: str, user_prompt: str, max_tokens: int
    ) -> AsyncIterator[str]:
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text


def get_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.llm_provider == "anthropic":
        return AnthropicClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
