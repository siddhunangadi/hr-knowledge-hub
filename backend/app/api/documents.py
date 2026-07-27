"""Document upload endpoint."""

import logging

from fastapi import APIRouter, HTTPException, UploadFile

from app.ingestion.embedder import EmbeddingError
from app.ingestion.ingestion_service import (
    FileTooLargeError,
    UnsupportedFileTypeError,
    ingest_document,
)
from app.ingestion.parser import DocumentParsingError
from app.ingestion.vector_store import VectorStoreError
from app.models.schemas import DocumentSummary, UploadResponse
from app.repositories.document_repository import DocumentRepositoryError, list_documents

router = APIRouter(prefix="/api/documents")
logger = logging.getLogger(__name__)


@router.get("", response_model=list[DocumentSummary])
def get_documents() -> list[DocumentSummary]:
    """Return every uploaded document, for the Streamlit dashboard to display."""
    try:
        documents = list_documents()
    except DocumentRepositoryError as exc:
        logger.exception("Failed to list documents")
        raise HTTPException(status_code=502, detail="Document storage unavailable") from exc

    return [DocumentSummary(**doc) for doc in documents]


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile) -> UploadResponse:
    """Validate, parse, chunk, embed, and index an uploaded PDF or DOCX file."""
    file_bytes = await file.read()

    try:
        result = ingest_document(
            filename=file.filename or "unknown",
            content_type=file.content_type or "",
            file_bytes=file_bytes,
        )
    except (UnsupportedFileTypeError, FileTooLargeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except DocumentParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except EmbeddingError as exc:
        logger.exception("Embedding generation failed")
        raise HTTPException(status_code=502, detail="Embedding service unavailable") from exc
    except (VectorStoreError, DocumentRepositoryError) as exc:
        logger.exception("Document storage failed")
        raise HTTPException(status_code=502, detail="Document storage unavailable") from exc

    return UploadResponse(
        document_id=result.document_id,
        filename=result.filename,
        chunks_created=result.chunks_created,
        processing_time_ms=result.processing_time_ms,
        status=result.status,
    )
