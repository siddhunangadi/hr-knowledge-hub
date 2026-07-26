"""Stores documents and chunk text/metadata in Supabase Postgres."""

from supabase import Client, create_client

from app.config.settings import get_settings
from app.ingestion.chunker import Chunk


class DocumentRepositoryError(Exception):
    """Raised when a Supabase read or write fails."""


def _get_client() -> Client:
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def save_document(document_id: str, filename: str) -> None:
    """Insert a row for the uploaded document into the `documents` table."""
    try:
        _get_client().table("documents").insert(
            {"id": document_id, "filename": filename}
        ).execute()
    except Exception as exc:
        raise DocumentRepositoryError(f"Failed to save document: {exc}") from exc


def save_chunks(chunks: list[Chunk]) -> None:
    """Insert chunk text and metadata into the `document_chunks` table."""
    rows = [
        {
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "chunk_index": chunk.chunk_index,
            "page_number": chunk.page_number,
            "text": chunk.text,
        }
        for chunk in chunks
    ]
    try:
        _get_client().table("document_chunks").insert(rows).execute()
    except Exception as exc:
        raise DocumentRepositoryError(f"Failed to save chunks: {exc}") from exc
