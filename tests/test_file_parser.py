import pytest

from app.services.file_parser import FileParser

# Sample test data
SAMPLE_TXT = b"This is sample text content with more than fifty characters for testing the file parser functionality."


def test_parse_txt_file():
    """Test parsing a valid TXT file."""
    parser = FileParser()
    result = parser.parse_file(SAMPLE_TXT, "test.txt")
    assert isinstance(result, str)
    assert "sample text" in result


def test_parse_empty_file():
    """Test that empty files raise ValueError."""
    parser = FileParser()
    with pytest.raises(ValueError, match="empty"):
        parser.parse_file(b"", "empty.txt")


def test_parse_unsupported_extension():
    """Test that unsupported file types raise ValueError."""
    parser = FileParser()
    with pytest.raises(ValueError, match="Unsupported file type"):
        parser.parse_file(b"content", "test.mp3")


def test_parse_case_insensitive_extension():
    """Test that file extensions are case-insensitive."""
    parser = FileParser()
    result = parser.parse_file(SAMPLE_TXT, "test.TXT")
    assert isinstance(result, str)
