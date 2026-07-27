"""Tests for the FastAPI endpoints — verifying HTTP wiring, not the underlying
logic (already covered in test_ingestion.py, test_retrieval.py, test_generation.py).
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.ingestion.ingestion_service import IngestionResult
from app.main import app
from app.retrieval.retrieval_service import RankedChunk

client = TestClient(app)


@patch("app.api.documents.ingest_document")
def test_upload_endpoint_returns_indexing_summary(mock_ingest):
    mock_ingest.return_value = IngestionResult(
        document_id="doc-1",
        filename="handbook.pdf",
        chunks_created=3,
        processing_time_ms=120,
        status="indexed",
    )

    response = client.post(
        "/api/documents/upload",
        files={"file": ("handbook.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["chunks_created"] == 3


def test_upload_endpoint_rejects_unsupported_file():
    response = client.post(
        "/api/documents/upload",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


@patch("app.api.retrieval.search")
def test_retrieval_endpoint_returns_results(mock_search):
    mock_search.return_value = {
        "results": [
            RankedChunk(
                chunk_id="doc-0", score=0.9, filename="handbook.pdf", page_number=1, text="..."
            )
        ]
    }

    response = client.post(
        "/api/retrieval/search",
        json={"query": "paid leave", "top_k": 1, "search_mode": "semantic"},
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["filename"] == "handbook.pdf"
