from fastapi.testclient import TestClient

from app.clients.llm import get_llm_client
from app.main import app
from tests.test_summarizer import MockLLMClient

client = TestClient(app)
app.dependency_overrides[get_llm_client] = lambda: MockLLMClient()

SAMPLE_TEXT = b"This is sample text content with more than fifty characters for testing the upload endpoint."


def test_upload_txt_file():
    """Test successful upload and summarization of TXT file."""
    response = client.post(
        "/upload/",
        files={"file": ("text.txt", SAMPLE_TEXT, "text/plain")},
        data={"style": "paragraph", "max_length": 100},
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["style"] == "paragraph"


def test_upload_file_too_large():
    """Test that files over 10MB are rejected."""
    large_content = b"x" * (11 * 1024 * 1024)  # 11 MB
    response = client.post(
        "/upload/", files={"file": ("large.txt", large_content, "text/plain")}
    )
    assert response.status_code == 413


def test_upload_unsupported_file_type():
    """Test that unsupported file types return 400."""
    response = client.post(
        "/upload/", files={"file": ("test.mp3", b"content", "audio/mpeg")}
    )
    assert response.status_code == 400


def test_upload_empty_file():
    """Test that empty files return 400."""
    response = client.post("/upload/", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 400
