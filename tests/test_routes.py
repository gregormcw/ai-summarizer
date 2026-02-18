from fastapi.testclient import TestClient

from app.clients.llm import get_llm_client
from app.main import app
from tests.test_summarizer import PROMPT, MockLLMClient

client = TestClient(app)
app.dependency_overrides[get_llm_client] = lambda: MockLLMClient()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200 and response.json()["status"] == "ok"


def test_summarize_success():
    response = client.post("/summarize/", json={"text": PROMPT, "style": "paragraph"})
    data = response.json()
    assert response.status_code == 200 and data["summary"] == "This is a test summary."


def test_summarize_rejects_short_text():
    response = client.post(
        "/summarize/",
        json={"text": "This text is below min length.", "style": "paragraph"},
    )
    assert response.status_code == 422


def test_summarize_rejects_invalid_style():
    response = client.post("/summarize/", json={"text": PROMPT, "style": "bananas"})
    assert response.status_code == 422
