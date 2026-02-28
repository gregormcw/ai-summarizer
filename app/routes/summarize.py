import base64
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_audio_service, get_summarizer_service
from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.services.audio import AudioService
from app.services.summarizer import SummarizerService

router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("/")
async def summarize(
    request: SummarizeRequest,
    tts: bool = False,
    service: SummarizerService = Depends(get_summarizer_service),
    audio_service: AudioService = Depends(get_audio_service),
) -> SummaryResponse:
    summary_response = await service.summarize(request)

    if tts:
        audio_bytes = audio_service.text_to_speech(summary_response.summary)
        summary_response.audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return summary_response


@router.post("/stream")
async def summarize_stream(
    request: SummarizeRequest,
    service: SummarizerService = Depends(get_summarizer_service),
) -> StreamingResponse:
    async def event_generator():
        async for chunk in service.summarize_stream(request):
            yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
        yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
