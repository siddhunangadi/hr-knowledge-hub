"""Pydantic request/response models for the API."""

from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response returned after a document has been ingested and indexed."""

    document_id: str
    filename: str
    chunks_created: int
    processing_time_ms: int
    status: str


class SearchRequest(BaseModel):
    """Request body for the hybrid retrieval search endpoint."""

    query: str
    top_k: int = 5
    debug: bool = False


class ChunkResponse(BaseModel):
    """A single retrieved chunk returned by the search endpoint."""

    chunk_id: str
    score: float
    filename: str
    page_number: Optional[int]
    text: str


class SearchResponse(BaseModel):
    """Response returned by the hybrid retrieval search endpoint."""

    query: str
    results: list[ChunkResponse]
    debug: Optional[dict] = None
