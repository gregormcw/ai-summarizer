from typing import Literal

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="The text to summarize.")
    max_length: int = Field(
        default=200,
        ge=50,
        le=1000,
        description="The maximum length of the summary in characters.",
    )
    style: Literal["paragraph", "bullet", "tldr"] = Field(
        default="paragraph", description="The style of the summary."
    )
