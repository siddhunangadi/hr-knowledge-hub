"""Tests for retrieval_service's three search modes.

External calls (NVIDIA, Pinecone, Supabase) are mocked; the actual dispatch
and result-assembly logic in retrieval_service.py runs for real.
"""

from unittest.mock import patch

FAKE_CHUNK = {
    "filename": "handbook.pdf",
    "page_number": 1,
    "text": "Employees are entitled to 20 days of paid leave per year.",
}


@patch("app.retrieval.retrieval_service.fetch_chunks_by_ids")
@patch("app.retrieval.retrieval_service.search_dense")
def test_search_semantic_mode(mock_dense, mock_fetch):
    from app.retrieval.retrieval_service import search

    mock_dense.return_value = [{"chunk_id": "doc-0", "score": 0.9}]
    mock_fetch.return_value = {"doc-0": FAKE_CHUNK}

    result = search("How much paid leave do I get?", top_k=1, search_mode="semantic")

    assert len(result["results"]) == 1
    assert result["results"][0].filename == "handbook.pdf"


@patch("app.retrieval.retrieval_service.fetch_chunks_by_ids")
@patch("app.retrieval.retrieval_service.search_bm25")
def test_search_keyword_mode(mock_bm25, mock_fetch):
    from app.retrieval.retrieval_service import search

    mock_bm25.return_value = [{"chunk_id": "doc-0", "score": 3.2}]
    mock_fetch.return_value = {"doc-0": FAKE_CHUNK}

    result = search("paid leave", top_k=1, search_mode="keyword")

    assert result["results"][0].chunk_id == "doc-0"


@patch("app.retrieval.retrieval_service.reranker_client")
@patch("app.retrieval.retrieval_service.fetch_chunks_by_ids")
@patch("app.retrieval.retrieval_service.search_bm25")
@patch("app.retrieval.retrieval_service.search_dense")
def test_search_hybrid_mode(mock_dense, mock_bm25, mock_fetch, mock_reranker):
    from app.retrieval.retrieval_service import search

    mock_dense.return_value = [{"chunk_id": "doc-0", "score": 0.9}]
    mock_bm25.return_value = [{"chunk_id": "doc-0", "score": 3.2}]
    mock_fetch.return_value = {"doc-0": FAKE_CHUNK}
    mock_reranker.rerank.return_value = [{"index": 0, "score": 5.0}]

    result = search("paid leave", top_k=1, search_mode="hybrid")

    # Hybrid mode's final score comes from the reranker, not dense/BM25.
    assert result["results"][0].score == 5.0
