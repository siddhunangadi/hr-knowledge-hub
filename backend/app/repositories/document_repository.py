"""Stores documents and chunk text/metadata in Supabase Postgres."""

from functools import lru_cache

from supabase import Client, create_client

from app.config.settings import get_settings
from app.ingestion.chunker import Chunk


class DocumentRepositoryError(Exception):
    """Raised when a Supabase read or write fails."""


@lru_cache
def _get_client() -> Client:
    """Return the Supabase client, creating the connection once and reusing it."""
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
            "chunk_id": chunk.chunk_id,
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


def fetch_all_chunks() -> list[dict]:
    """Return chunk_id and text for every stored chunk — used by BM25 search."""
    try:
        response = _get_client().table("document_chunks").select("chunk_id, text").execute()
    except Exception as exc:
        raise DocumentRepositoryError(f"Failed to fetch chunks: {exc}") from exc
    return response.data


def fetch_chunks_by_ids(chunk_ids: list[str]) -> dict[str, dict]:
    """Return {chunk_id: {filename, page_number, text}} for the given chunk ids."""
    if not chunk_ids:
        return {}
    try:
        response = (
            _get_client()
            .table("document_chunks")
            .select("chunk_id, filename, page_number, text")
            .in_("chunk_id", chunk_ids)
            .execute()
        )
    except Exception as exc:
        raise DocumentRepositoryError(f"Failed to fetch chunks by id: {exc}") from exc
    return {row["chunk_id"]: row for row in response.data}
