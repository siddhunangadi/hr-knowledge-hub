"""Orchestrates the document ingestion pipeline: parse -> chunk -> embed -> store."""

import time
import uuid
from dataclasses import dataclass

from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import NVIDIAEmbeddingClient
from app.ingestion.parser import parse_docx, parse_pdf
from app.ingestion.vector_store import index_chunks
from app.repositories.document_repository import save_chunks, save_document

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
SUPPORTED_CONTENT_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}


class UnsupportedFileTypeError(Exception):
    """Raised when the uploaded file is not a PDF or DOCX."""


class FileTooLargeError(Exception):
    """Raised when the uploaded file exceeds the size limit."""


@dataclass
class IngestionResult:
    """Summary returned after a document has been indexed."""

    document_id: str
    filename: str
    chunks_created: int
    processing_time_ms: int
    status: str


def validate_upload(filename: str, content_type: str, file_size: int) -> str:
    """Validate file type and size, returning the detected file kind ("pdf"/"docx")."""
    if content_type not in SUPPORTED_CONTENT_TYPES:
        raise UnsupportedFileTypeError(f"Unsupported file type: {content_type}")
    if file_size > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(f"File exceeds maximum size of {MAX_FILE_SIZE_BYTES} bytes")
    return SUPPORTED_CONTENT_TYPES[content_type]


def ingest_document(filename: str, content_type: str, file_bytes: bytes) -> IngestionResult:
    """Run the full ingestion pipeline for one uploaded file."""
    start_time = time.perf_counter()

    file_kind = validate_upload(filename, content_type, len(file_bytes))

    pages = parse_pdf(file_bytes) if file_kind == "pdf" else parse_docx(file_bytes)

    document_id = str(uuid.uuid4())
    chunks = chunk_pages(pages, document_id=document_id, filename=filename)

    embeddings = NVIDIAEmbeddingClient().embed([chunk.text for chunk in chunks])

    save_document(document_id, filename)
    save_chunks(chunks)
    index_chunks(chunks, embeddings)

    processing_time_ms = int((time.perf_counter() - start_time) * 1000)

    return IngestionResult(
        document_id=document_id,
        filename=filename,
        chunks_created=len(chunks),
        processing_time_ms=processing_time_ms,
        status="indexed",
    )
