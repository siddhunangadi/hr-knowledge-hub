"""Pydantic request/response models for the API."""

from typing import Literal, Optional

from pydantic import BaseModel

SearchMode = Literal["semantic", "keyword", "hybrid"]


class UploadResponse(BaseModel):
    """Response returned after a document has been ingested and indexed."""

    document_id: str
    filename: str
    chunks_created: int
    processing_time_ms: int
    status: str


class DocumentSummary(BaseModel):
    """One row of the document list returned by GET /api/documents."""

    document_id: str
    filename: str
    uploaded_at: str
    chunks_created: int


class SearchRequest(BaseModel):
    """Request body for the hybrid retrieval search endpoint."""

    query: str
    top_k: int = 8
    search_mode: SearchMode = "hybrid"
    debug: bool = False


class ChunkResponse(BaseModel):
    """A single retrieved chunk returned by the search endpoint."""

    chunk_id: str
    score: float
    filename: str
    page_number: Optional[int]
    text: str


class RankedResult(BaseModel):
    """A chunk id and score from one stage of the retrieval pipeline."""

    chunk_id: str
    score: float


class RerankedResult(BaseModel):
    """A reranked candidate, identified by its position in the passage list sent to the reranker."""

    index: int
    score: float


class RetrievalDebugInfo(BaseModel):
    """Intermediate results from each retrieval stage — for inspection, not for clients to act on."""

    search_mode: SearchMode
    dense_results: list[RankedResult] = []
    bm25_results: list[RankedResult] = []
    rrf_results: list[RankedResult] = []
    reranked_results: list[RerankedResult] = []


class SearchResponse(BaseModel):
    """Response returned by the hybrid retrieval search endpoint."""

    query: str
    results: list[ChunkResponse]
    debug: Optional[RetrievalDebugInfo] = None


class Citation(BaseModel):
    """Where an answer's supporting text came from — filename and page only."""

    filename: str
    page_number: Optional[int]


class ChatResponse(BaseModel):
    """Response returned by the grounded answer generation endpoint."""

    answer: str
    confidence: int
    citations: list[Citation]
    debug: Optional[RetrievalDebugInfo] = None
