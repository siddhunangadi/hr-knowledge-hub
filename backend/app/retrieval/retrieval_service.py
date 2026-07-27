"""Orchestrates retrieval: semantic (dense only), keyword (BM25 only), or hybrid (both + RRF + rerank)."""

from dataclasses import dataclass

from app.repositories.document_repository import fetch_chunks_by_ids
from app.retrieval.dense_search import search_dense
from app.retrieval.hybrid_search import reciprocal_rank_fusion
from app.retrieval.keyword_search import search_bm25
from app.retrieval.reranker import reranker_client

# Fetch a wider candidate pool than top_k so RRF and the reranker have
# enough chunks to actually reorder.
CANDIDATE_MULTIPLIER = 4


@dataclass
class RankedChunk:
    """A single retrieved chunk, ready to return from the API."""

    chunk_id: str
    score: float
    filename: str
    page_number: int
    text: str


def _hydrate(ranked_results: list[dict], top_k: int) -> list[RankedChunk]:
    """Attach filename/page_number/text from Supabase to {chunk_id, score} results.

    Skips any chunk_id Pinecone/BM25 returned that has no matching Supabase
    row — the two stores aren't written transactionally, so they can drift.
    """
    top_results = ranked_results[:top_k]
    chunks_by_id = fetch_chunks_by_ids([item["chunk_id"] for item in top_results])
    return [
        RankedChunk(
            chunk_id=item["chunk_id"],
            score=item["score"],
            filename=chunks_by_id[item["chunk_id"]]["filename"],
            page_number=chunks_by_id[item["chunk_id"]]["page_number"],
            text=chunks_by_id[item["chunk_id"]]["text"],
        )
        for item in top_results
        if item["chunk_id"] in chunks_by_id
    ]


def _search_semantic(query: str, top_k: int, debug: bool) -> dict:
    """Dense (Pinecone) search only — no BM25, no reranker."""
    dense_results = search_dense(query, top_k=top_k)
    response = {"results": _hydrate(dense_results, top_k)}
    if debug:
        response["debug"] = {"dense_results": dense_results}
    return response


def _search_keyword(query: str, top_k: int, debug: bool) -> dict:
    """BM25 search only — no dense search, no reranker."""
    bm25_results = search_bm25(query, top_k=top_k)
    response = {"results": _hydrate(bm25_results, top_k)}
    if debug:
        response["debug"] = {"bm25_results": bm25_results}
    return response


def _search_hybrid(query: str, top_k: int, debug: bool) -> dict:
    """Dense + BM25 -> Reciprocal Rank Fusion -> NVIDIA reranker."""
    candidate_k = top_k * CANDIDATE_MULTIPLIER

    dense_results = search_dense(query, top_k=candidate_k)
    bm25_results = search_bm25(query, top_k=candidate_k)
    fused_results = reciprocal_rank_fusion(dense_results, bm25_results, top_k=candidate_k)

    fused_chunk_ids = [item["chunk_id"] for item in fused_results]
    chunks_by_id = fetch_chunks_by_ids(fused_chunk_ids)
    # Drop any chunk_id missing from Supabase before building passages, so
    # the reranker's later index-based lookup stays aligned.
    fused_chunk_ids = [cid for cid in fused_chunk_ids if cid in chunks_by_id]
    passages = [chunks_by_id[chunk_id]["text"] for chunk_id in fused_chunk_ids]

    reranked = reranker_client.rerank(query, passages)

    results = []
    for item in reranked[:top_k]:
        chunk_id = fused_chunk_ids[item["index"]]
        chunk = chunks_by_id[chunk_id]
        results.append(
            RankedChunk(
                chunk_id=chunk_id,
                score=item["score"],
                filename=chunk["filename"],
                page_number=chunk["page_number"],
                text=chunk["text"],
            )
        )

    response = {"results": results}
    if debug:
        response["debug"] = {
            "dense_results": dense_results,
            "bm25_results": bm25_results,
            "rrf_results": fused_results,
            "reranked_results": reranked,
        }
    return response


def search(query: str, top_k: int, search_mode: str = "hybrid", debug: bool = False) -> dict:
    """Run retrieval in the requested mode and return final (and optionally debug) results."""
    if search_mode == "semantic":
        response = _search_semantic(query, top_k, debug)
    elif search_mode == "keyword":
        response = _search_keyword(query, top_k, debug)
    else:
        response = _search_hybrid(query, top_k, debug)

    if debug:
        response["debug"]["search_mode"] = search_mode
    return response
