"""Grounded answer generation endpoint — retrieve, then answer using only that context."""

import logging

from fastapi import APIRouter, HTTPException

from app.generation.generation_service import generate_answer
from app.generation.llm_client import LLMError
from app.ingestion.embedder import EmbeddingError
from app.ingestion.vector_store import VectorStoreError
from app.models.schemas import ChatResponse, Citation, RetrievalDebugInfo, SearchRequest
from app.repositories.document_repository import DocumentRepositoryError
from app.retrieval.reranker import RerankError

router = APIRouter(prefix="/api/chat")
logger = logging.getLogger(__name__)


@router.post("", response_model=ChatResponse)
def chat(request: SearchRequest) -> ChatResponse:
    """Retrieve relevant chunks and generate a grounded answer with citations."""
    try:
        result = generate_answer(
            request.query,
            top_k=request.top_k,
            search_mode=request.search_mode,
            debug=request.debug,
        )
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
    except LLMError as exc:
        logger.exception("Answer generation failed")
        raise HTTPException(status_code=502, detail="Generation service unavailable") from exc

    citations = [Citation(**citation) for citation in result["citations"]]
    debug = RetrievalDebugInfo(**result["debug"]) if result.get("debug") else None

    return ChatResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        citations=citations,
        debug=debug,
    )
