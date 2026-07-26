"""Hybrid retrieval search endpoint."""

import logging

from fastapi import APIRouter, HTTPException

from app.ingestion.embedder import EmbeddingError
from app.ingestion.vector_store import VectorStoreError
from app.models.schemas import ChunkResponse, SearchRequest, SearchResponse
from app.repositories.document_repository import DocumentRepositoryError
from app.retrieval.reranker import RerankError
from app.retrieval.retrieval_service import search

router = APIRouter(prefix="/api/retrieval")
logger = logging.getLogger(__name__)


@router.post("/search", response_model=SearchResponse)
def search_documents(request: SearchRequest) -> SearchResponse:
    """Run hybrid retrieval (dense + BM25 + RRF + rerank) for a query."""
    try:
        result = search(request.query, top_k=request.top_k, debug=request.debug)
    except EmbeddingError as exc:
        logger.exception("Query embedding failed")
        raise HTTPException(status_code=502, detail="Embedding service unavailable") from exc
    except VectorStoreError as exc:
        logger.exception("Pinecone search failed")
        raise HTTPException(status_code=502, detail="Vector search unavailable") from exc
    except RerankError as exc:
        logger.exception("Reranking failed")
        raise HTTPException(status_code=502, detail="Reranking service unavailable") from exc
    except DocumentRepositoryError as exc:
        logger.exception("Chunk lookup failed")
        raise HTTPException(status_code=502, detail="Document storage unavailable") from exc

    results = [
        ChunkResponse(
            chunk_id=chunk.chunk_id,
            score=chunk.score,
            filename=chunk.filename,
            page_number=chunk.page_number,
            text=chunk.text,
        )
        for chunk in result["results"]
    ]

    return SearchResponse(query=request.query, results=results, debug=result.get("debug"))
