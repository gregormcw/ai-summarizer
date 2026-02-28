import base64

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.dependencies import (get_audio_service, get_file_parser,
                              get_summarizer_service)
from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.services.audio import AudioService
from app.services.file_parser import FileParser
from app.services.summarizer import SummarizerService

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", response_model=SummaryResponse)
async def upload_and_summarize(
    file: UploadFile = File(...),
    style: str = Form("paragraph"),
    max_length: int = Form(200),
    tts: bool = Form(False),
    parser: FileParser = Depends(get_file_parser),
    service: SummarizerService = Depends(get_summarizer_service),
    audio_service: AudioService = Depends(get_audio_service),
) -> SummaryResponse:
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    try:
        text = parser.parse_file(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    request = SummarizeRequest(text=text, max_length=max_length, style=style)
    summary_response = await service.summarize(request)

    if tts:
        audio_bytes = audio_service.text_to_speech(summary_response.summary)
        summary_response.audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return summary_response
