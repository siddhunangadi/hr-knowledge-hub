"""Extracts raw text from uploaded PDF and DOCX files."""

import io

import docx
import fitz  # PyMuPDF


class DocumentParsingError(Exception):
    """Raised when a document's text cannot be extracted."""


def parse_pdf(file_bytes: bytes) -> list[str]:
    """Return a list of page texts extracted from a PDF."""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
            return [page.get_text() for page in pdf]
    except Exception as exc:
        raise DocumentParsingError(f"Failed to parse PDF: {exc}") from exc


def parse_docx(file_bytes: bytes) -> list[str]:
    """Return the DOCX text as a single page (DOCX has no page concept)."""
    try:
        document = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        return [text]
    except Exception as exc:
        raise DocumentParsingError(f"Failed to parse DOCX: {exc}") from exc
