"""Merges dense and BM25 results using Reciprocal Rank Fusion (RRF)."""

RRF_K = 60


def reciprocal_rank_fusion(
    dense_results: list[dict], bm25_results: list[dict], top_k: int
) -> list[dict]:
    """Combine two ranked chunk lists into one fused ranking.

    Each input is a list of {chunk_id, score} sorted best-first. RRF ignores
    the raw scores and only uses each chunk's rank, so dense (cosine) and
    BM25 (unbounded) scores don't need to be on the same scale.
    """
    fused_scores: dict[str, float] = {}

    for rank, result in enumerate(dense_results, start=1):
        chunk_id = result["chunk_id"]
        fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + 1 / (RRF_K + rank)

    for rank, result in enumerate(bm25_results, start=1):
        chunk_id = result["chunk_id"]
        fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + 1 / (RRF_K + rank)

    ranked = sorted(fused_scores.items(), key=lambda item: item[1], reverse=True)
    return [{"chunk_id": chunk_id, "score": score} for chunk_id, score in ranked[:top_k]]
