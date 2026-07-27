"""Orchestrates grounded answer generation: retrieve -> prompt -> LLM -> answer + citations + confidence."""

import math

from app.generation.llm_client import llm_client
from app.generation.prompt_builder import NO_ANSWER_MESSAGE, build_prompt
from app.retrieval.retrieval_service import RankedChunk, search


# Each search_mode's chunk.score comes from a different scale: reranker
# logits (hybrid), cosine similarity (semantic), or raw BM25 (keyword).
# Centering the sigmoid at 0 for all three badly miscalibrates confidence,
# since e.g. a genuinely correct hybrid-mode match often scores around -2 to
# -3, not near 0. CENTER is the score treated as "50% confidence" per mode,
# and SPREAD controls how quickly confidence moves away from 50% as the
# score moves away from CENTER. Values below are a rough calibration from
# real examples observed against actual documents, not derived analytically
# — if a different reranker/embedding model is swapped in later, recheck
# these against a few real queries.
_CONFIDENCE_CALIBRATION = {
    "hybrid": {"center": -3.0, "spread": 2.0},
    "semantic": {"center": 0.35, "spread": 0.15},
    "keyword": {"center": 5.0, "spread": 5.0},
}


def _estimate_confidence(chunks: list[RankedChunk], search_mode: str) -> int:
    """Estimate answer confidence from the top chunk's score, as a 0-100 percentage.

    Formula: take the top-ranked chunk's score (chunks are already sorted
    best-first), recenter and scale it per search_mode using
    _CONFIDENCE_CALIBRATION, then squash through a sigmoid (1 / (1 + e^-x))
    into 0-100.

    Only the top chunk's score is used, not an average across all returned
    chunks: the answer is grounded primarily in the single best match, and
    averaging in weaker lower-ranked chunks would understate confidence in
    an otherwise strong top result.
    """
    if not chunks:
        return 0
    calibration = _CONFIDENCE_CALIBRATION[search_mode]
    top_score = chunks[0].score
    normalized = (top_score - calibration["center"]) / calibration["spread"]
    probability = 1 / (1 + math.exp(-normalized))
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
    """Retrieve chunks, ground the LLM's answer in them, and return answer + citations + confidence.

    Confidence is informational only — it does not gate whether the LLM is
    called. The prompt's own grounding rule ("if the answer isn't in the
    context, say so") is the actual safety net against hallucination; a low
    reranker score on the top chunk doesn't necessarily mean the chunk is
    wrong, so the LLM is trusted to make that call itself.
    """
    retrieval = search(query, top_k=top_k, search_mode=search_mode, debug=debug)
    chunks = retrieval["results"]
    confidence = _estimate_confidence(chunks, search_mode)

    if not chunks:
        response = {"answer": NO_ANSWER_MESSAGE, "confidence": confidence, "citations": []}
    else:
        prompt = build_prompt(query, chunks)
        answer = llm_client.generate(prompt)
        # No citations when the LLM itself decided the context didn't answer
        # the question — showing "sources" next to a "not found" message
        # would be self-contradictory.
        citations = [] if answer == NO_ANSWER_MESSAGE else _build_citations(chunks)
        response = {"answer": answer, "confidence": confidence, "citations": citations}

    if debug:
        response["debug"] = retrieval.get("debug")
    return response
