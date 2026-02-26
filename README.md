# AI Summarizer

A production-ready REST API for AI-powered text summarization, built with FastAPI and Anthropic's Claude API. Features clean architecture with dependency injection, comprehensive test coverage, and streaming support.

## Features

- **Three summarization styles**: `paragraph`, `bullet`, `tldr`
- **Multiple input methods**: Direct text input or file upload (PDF, DOCX, TXT)
- **Streaming support**: Server-Sent Events (SSE) for real-time token delivery
- **Input validation**: Pydantic schemas with automatic error responses
- **Provider-agnostic architecture**: Swap LLM providers without touching business logic
- **Comprehensive tests**: 15/15 passing tests with mocked API calls
- **Auto-generated docs**: Interactive API documentation at `/docs`

## Architecture
```
app/
├── core/          # Configuration and logging
├── routes/        # HTTP layer (FastAPI routers)
├── services/      # Business logic
├── clients/       # LLM provider adapters
├── models/        # Pydantic request/response schemas
└── prompts/       # Prompt templates (versioned as code)
```

**Design principle**: Each layer has one responsibility. Routes handle HTTP, services contain logic, clients abstract external APIs. This makes the codebase testable, maintainable, and extensible.

## Quick Start

### Prerequisites

- Python 3.12+ ([download here](https://www.python.org/downloads/))
- Anthropic API key ([get one here](https://console.anthropic.com))

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/gregormcw/ai-summarizer.git
cd ai-summarizer
```

**2. Create and activate a virtual environment:**
```bash
python -m venv .venv
```

Activate it:
- **macOS/Linux**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`

You should see `(.venv)` in your terminal prompt.

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**5. Run the server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Alternative: Using conda

If you prefer conda:
```bash
conda create -n ai-summarizer python=3.12
conda activate ai-summarizer
pip install -r requirements.txt
```

## Using the Web Interface

A user-friendly web interface is available at `http://localhost:8000/static/index.html` when the server is running.

**Features:**
- **Text input** - Paste text directly into the textarea
- **File upload** - Upload PDF, DOCX, or TXT files (supports drag-and-drop)
- **Style selection** - Choose paragraph, bullet points, or TL;DR format
- **Real-time results** - See your summary with metadata (word counts, model used)

The interface calls the same API endpoints documented at `/docs`.

## Usage

### Standard Summarization
```bash
curl -X POST http://localhost:8000/summarize/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "style": "paragraph",
    "max_length": 150
  }'
```

**Response:**
```json
{
  "summary": "A concise summary of your text.",
  "style": "paragraph",
  "model": "claude-3-5-sonnet-20241022",
  "prompt_length": 245,
  "summary_length": 28,
  "summary_ts": "2026-02-18T10:30:00Z"
}
```

### File Upload

Upload PDF, DOCX, or TXT files for summarization:
```bash
curl -X POST http://localhost:8000/upload/ \
  -F "file=@document.pdf" \
  -F "style=bullet" \
  -F "max_length=200"
```

**Supported file types:**
- PDF (`.pdf`) - Extracted via PyMuPDF
- Word Documents (`.docx`) - Extracted via python-docx
- Text files (`.txt`) - Direct UTF-8 decoding

**File size limit:** 10MB maximum

**Response:** Same format as standard summarization endpoint

### Streaming Summarization
```bash
curl -X POST http://localhost:8000/summarize/stream \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "style": "bullet"
  }'
```

Receives tokens progressively as Server-Sent Events.

### Caching

Redis caching is enabled by default to reduce API costs and improve response times.

**How it works:**
- Identical requests (same text, style, and max_length) return cached results
- Cache entries expire after 24 hours (configurable via `CACHE_TTL`)
- Cache hits are logged for monitoring

**Requirements:**
- Redis server running locally (install via `brew install redis` on macOS)
- Start Redis: `brew services start redis`

**Configuration:**
Add to your `.env` file:
```bash
REDIS_ENABLED=true
CACHE_TTL=86400  # 24 hours in seconds
```

**Disable caching** (for development/testing):
```bash
REDIS_ENABLED=false
```

### Summarization Styles

| Style | Description | Use Case |
|-------|-------------|----------|
| `paragraph` | Concise prose summary | Reports, articles |
| `bullet` | Key points as bullets | Meeting notes, action items |
| `tldr` | 1-2 sentence summary | Quick overviews |

## Testing

Run the full test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

## Development

### Code Formatting

This project uses Black, isort, and flake8:
```bash
black app/ tests/
isort app/ tests/
flake8 app/ tests/ --max-line-length=120
```

### Project Structure

- **`core/config.py`**: Centralized configuration using Pydantic Settings
- **`clients/llm.py`**: Abstract `LLMClient` with concrete `AnthropicClient` implementation
- **`services/summarizer.py`**: Core summarization logic, decoupled from HTTP and LLM concerns
- **`routes/summarize.py`**: FastAPI endpoints with dependency injection
- **`prompts/`**: Prompt templates stored as files, versioned alongside code

## Design Decisions

### Why separate the client layer?

The `LLMClient` abstraction means swapping from Anthropic to OpenAI requires changes only in `clients/llm.py`. The service layer, routes, and tests remain unchanged.

### Why store prompts as files?

Prompts are source code. Storing them as `.txt` files means they can be versioned, reviewed, and iterated independently of application logic.

### Why use dependency injection?

FastAPI's `Depends()` pattern makes the codebase testable. Tests inject mock clients instead of hitting real APIs, making them fast and deterministic.

### Why streaming?

Modern AI tools stream tokens as they're generated. The `/stream` endpoint provides this UX without blocking the main `/summarize` endpoint for non-streaming use cases.

## Roadmap

- [x] File upload support for PDF, DOCX, TXT
- [x] Redis caching to avoid re-summarizing identical text
- [x] Simple HTML frontend for non-API usage
- [ ] ASR/STT input for audio summarization
- [ ] TTS output for accessibility

## Environment Troubleshooting

### Common Issues

**Module not found despite installation**

If you see `ModuleNotFoundError` after installing packages, ensure your virtual environment is activated:
```bash
which python  # Should point to .venv/bin/python
python --version  # Should show 3.12+
```

If not activated, run:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

**Tests not finding pytest**

Make sure pytest is installed in your active environment:
```bash
pip install pytest pytest-asyncio
```

**API key errors**

Verify your `.env` file exists and contains a valid `ANTHROPIC_API_KEY`.

## Contributing

This is a portfolio project, but suggestions are welcome. Open an issue or submit a pull request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Anthropic Claude](https://www.anthropic.com/) - AI language model
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [pytest](https://docs.pytest.org/) - Testing framework
