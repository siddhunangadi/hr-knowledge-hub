"""Tests for upload validation — the only pure logic in the ingestion pipeline."""

import pytest

from app.ingestion.ingestion_service import (
    FileTooLargeError,
    UnsupportedFileTypeError,
    validate_upload,
)


def test_validate_upload_accepts_pdf():
    assert validate_upload("handbook.pdf", "application/pdf", 1000) == "pdf"


def test_validate_upload_accepts_docx():
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert validate_upload("handbook.docx", content_type, 1000) == "docx"


def test_validate_upload_rejects_unsupported_type():
    with pytest.raises(UnsupportedFileTypeError):
        validate_upload("notes.txt", "text/plain", 1000)


def test_validate_upload_rejects_oversized_file():
    five_mb_plus_one = 5 * 1024 * 1024 + 1
    with pytest.raises(FileTooLargeError):
        validate_upload("handbook.pdf", "application/pdf", five_mb_plus_one)
