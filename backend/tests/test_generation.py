"""Tests for grounded answer generation: citation building and the no-answer fallback."""

from unittest.mock import patch

from app.retrieval.retrieval_service import RankedChunk

FAKE_CHUNK = RankedChunk(
    chunk_id="doc-0",
    score=6.0,
    filename="handbook.pdf",
    page_number=1,
    text="Employees are entitled to 20 days of paid leave per year.",
)


@patch("app.generation.generation_service.llm_client")
@patch("app.generation.generation_service.search")
def test_generate_answer_includes_citation(mock_search, mock_llm):
    from app.generation.generation_service import generate_answer

    mock_search.return_value = {"results": [FAKE_CHUNK]}
    mock_llm.generate.return_value = "Employees get 20 days of paid leave per year."

    result = generate_answer("How much leave?", top_k=1, search_mode="hybrid", debug=False)

    assert result["answer"] == "Employees get 20 days of paid leave per year."
    assert result["citations"] == [
        {"chunk_id": "doc-0", "filename": "handbook.pdf", "page_number": 1}
    ]


@patch("app.generation.generation_service.search")
def test_generate_answer_no_answer_fallback(mock_search):
    from app.generation.generation_service import generate_answer
    from app.generation.prompt_builder import NO_ANSWER_MESSAGE

    mock_search.return_value = {"results": []}

    result = generate_answer(
        "What is the capital of France?", top_k=3, search_mode="hybrid", debug=False
    )

    assert result["answer"] == NO_ANSWER_MESSAGE
    assert result["citations"] == []
    assert result["confidence"] == 0
