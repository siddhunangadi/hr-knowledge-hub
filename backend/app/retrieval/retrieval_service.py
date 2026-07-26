"""Orchestrates hybrid retrieval: dense search + BM25 -> RRF -> rerank."""

from dataclasses import dataclass

from app.repositories.document_repository import fetch_chunks_by_ids
from app.retrieval.dense_search import search_dense
from app.retrieval.hybrid_search import reciprocal_rank_fusion
from app.retrieval.keyword_search import search_bm25
from app.retrieval.reranker import NVIDIARerankerClient

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


def search(query: str, top_k: int, debug: bool = False) -> dict:
    """Run the hybrid retrieval pipeline and return final (and optionally debug) results."""
    candidate_k = top_k * CANDIDATE_MULTIPLIER

    dense_results = search_dense(query, top_k=candidate_k)
    bm25_results = search_bm25(query, top_k=candidate_k)
    fused_results = reciprocal_rank_fusion(dense_results, bm25_results, top_k=candidate_k)

    fused_chunk_ids = [item["chunk_id"] for item in fused_results]
    chunks_by_id = fetch_chunks_by_ids(fused_chunk_ids)
    passages = [chunks_by_id[chunk_id]["text"] for chunk_id in fused_chunk_ids]

    reranked = NVIDIARerankerClient().rerank(query, passages)

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
