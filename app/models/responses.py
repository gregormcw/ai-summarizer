from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    summary: str
    style: Literal["paragraph", "bullet", "tldr"]
    model: str
    prompt_length: int
    summary_length: int
    summary_ts: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The timestamp when the summary was generated.",
    )
    audio_base64: str | None = None


class StreamChunk(BaseModel):
    chunk: str
    done: bool = False
