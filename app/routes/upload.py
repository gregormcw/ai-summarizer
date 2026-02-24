from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.models.requests import SummarizeRequest
from app.models.responses import SummaryResponse
from app.routes.summarize import get_summarizer_service
from app.services.file_parser import FileParser
from app.services.summarizer import SummarizerService

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
router = APIRouter(prefix="/upload", tags=["upload"])


def get_file_parser() -> FileParser:
    return FileParser()


@router.post("/", response_model=SummaryResponse)
async def upload_and_summarize(
    file: UploadFile = File(...),
    style: str = "paragraph",
    max_length: int = 200,
    parser: FileParser = Depends(get_file_parser),
    service: SummarizerService = Depends(get_summarizer_service),
) -> SummaryResponse:
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    try:
        text = parser.parse_file(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    request = SummarizeRequest(text=text, max_length=max_length, style=style)
    return await service.summarize(request)
