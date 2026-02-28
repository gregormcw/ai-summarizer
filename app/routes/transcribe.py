import base64
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.dependencies import get_audio_service, get_summarizer_service
from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.services.audio import AudioService
from app.services.summarizer import SummarizerService

MAX_SIZE = 25 * 1024 * 1024  # 25 MB OpenAI transcription limit
SUPPORTED_AUDIO_FORMATS = {".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"}
router = APIRouter(prefix="/transcribe", tags=["transcribe"])


@router.post("/", response_model=SummaryResponse)
async def transcribe_and_summarize(
    file: UploadFile = File(...),
    style: str = "paragraph",
    max_length: int = 200,
    tts: bool = False,
    audio_service: AudioService = Depends(get_audio_service),
    summarizer_service: SummarizerService = Depends(get_summarizer_service),
) -> SummaryResponse:
    audio_data = await file.read()
    if len(audio_data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 25 MB)")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{file_ext}'. Supported: {', '.join(SUPPORTED_AUDIO_FORMATS)}",
        )

    try:
        text = audio_service.transcribe(audio_data=audio_data, filename=file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    request = SummarizeRequest(
        text=text,
        max_length=max_length,
        style=style,
    )
    summary_response = await summarizer_service.summarize(request)

    if tts:
        audio_bytes = audio_service.text_to_speech(summary_response.summary)
        summary_response.audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return summary_response
