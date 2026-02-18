import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.clients.llm import LLMClient, get_llm_client
from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.services.summarizer import SummarizerService


def get_summarizer_service(
    client: LLMClient = Depends(get_llm_client),
) -> SummarizerService:
    return SummarizerService(llm=client)


router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("/")
async def summarize(
    request: SummarizeRequest,
    service: SummarizerService = Depends(get_summarizer_service),
) -> SummaryResponse:
    return await service.summarize(request)


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
