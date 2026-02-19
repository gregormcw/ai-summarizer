from typing import Literal, Union

from pydantic import BaseModel, Field


class StreamDelta(BaseModel):
    type: Literal["delta"] = "delta"
    path: str = Field(..., description="The path of the field being updated, e.g. 'summary', 'bullets[0]', 'actions[1]'.")
    value: str = Field(..., description="Text to append at that path.")


class StreamDone(BaseModel):
    type: Literal["done"] = "done"


class StreamError(BaseModel):
    type: Literal["error"] = "error"
    message: str


StreamEvent = Union[StreamDelta, StreamDone, StreamError]
