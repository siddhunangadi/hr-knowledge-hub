"""Orchestrates grounded answer generation: retrieve -> prompt -> LLM -> answer + citations + confidence."""

import math

from app.generation.llm_client import llm_client
from app.generation.prompt_builder import NO_ANSWER_MESSAGE, build_prompt
from app.retrieval.retrieval_service import RankedChunk, search

# Below this confidence, we treat retrieval as "nothing relevant found" and
# skip the LLM call entirely rather than risk a hallucinated answer.
CONFIDENCE_THRESHOLD = 40


def _estimate_confidence(chunks: list[RankedChunk]) -> int:
    """Estimate answer confidence from retrieval scores, as a 0-100 percentage.

    Formula: average the retrieved chunks' scores, then squash that average
    through a sigmoid (1 / (1 + e^-x)) into a 0-1 range and scale to 0-100.
    A sigmoid is used because raw scores are unbounded and mean different
    things per search_mode (BM25 score, cosine similarity, or reranker
    logit) — this gives one consistent 0-100 scale regardless of which
    produced them.
    """
    if not chunks:
        return 0
    avg_score = sum(chunk.score for chunk in chunks) / len(chunks)
    probability = 1 / (1 + math.exp(-avg_score))
    return round(probability * 100)


def _build_citations(chunks: list[RankedChunk]) -> list[dict]:
    """Return {chunk_id, filename, page_number} for each retrieved chunk — no LLM involvement.

    chunk_id is included for internal debugging/retrieval inspection. The
    public Citation model only declares filename/page_number, so it's
    dropped automatically when the API layer builds the response — no
    similarity score, reranker score, or vector id is ever included.
    """
    return [
        {"chunk_id": chunk.chunk_id, "filename": chunk.filename, "page_number": chunk.page_number}
        for chunk in chunks
    ]


def generate_answer(query: str, top_k: int, search_mode: str, debug: bool) -> dict:
    """Retrieve chunks, ground the LLM's answer in them, and return answer + citations + confidence."""
    retrieval = search(query, top_k=top_k, search_mode=search_mode, debug=debug)
    chunks = retrieval["results"]
    confidence = _estimate_confidence(chunks)

    if not chunks or confidence < CONFIDENCE_THRESHOLD:
        response = {"answer": NO_ANSWER_MESSAGE, "confidence": confidence, "citations": []}
    else:
        prompt = build_prompt(query, chunks)
        answer = llm_client.generate(prompt)
        response = {
            "answer": answer,
            "confidence": confidence,
            "citations": _build_citations(chunks),
        }

    if debug:
        response["debug"] = retrieval.get("debug")
    return response
