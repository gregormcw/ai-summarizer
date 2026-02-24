from io import BytesIO
from pathlib import Path
from typing import Callable

import fitz  # PyMuPDF
from docx import Document


class FileParser:
    """Extract text from uploaded files."""

    def __init__(self):
        self.extensions: dict[str, Callable[[bytes], str]] = {
            ".pdf": self._parse_pdf,
            ".docx": self._parse_docx,
            ".txt": self._parse_txt,
        }

    def parse_file(self, file_content: bytes, filename: str) -> str:
        """Detect file type and extract text."""
        file_path: Path = Path(filename)
        extension: str = file_path.suffix.lower()

        if not file_content:
            raise ValueError(f"{filename} is empty - nothing to summarize.")

        if extension in self.extensions:
            return self.extensions[extension](file_content)
        else:
            supported: str = ", ".join(self.extensions.keys())
            raise ValueError(
                f"Unsupported file type: '{extension}'. Supported types: {supported}"
            )

    def _parse_pdf(self, content: bytes) -> str:
        text: list[str] = []
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text.append(page.get_text())
        return "\n".join(text)

    def _parse_docx(self, content: bytes) -> str:
        text: list[str] = []
        doc: Document = Document(BytesIO(content))
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text)

    def _parse_txt(self, content: bytes) -> str:
        return content.decode("utf-8", errors="replace")
