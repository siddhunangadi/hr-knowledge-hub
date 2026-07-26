"""Keyword retrieval: a small BM25 implementation over chunk text in Supabase."""

import math
from collections import Counter

from app.repositories.document_repository import fetch_all_chunks

BM25_K1 = 1.5
BM25_B = 0.75


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def search_bm25(query: str, top_k: int) -> list[dict]:
    """Score every stored chunk against the query using BM25, return the top_k."""
    chunks = fetch_all_chunks()
    if not chunks:
        return []

    tokenized_docs = [_tokenize(chunk["text"]) for chunk in chunks]
    doc_lengths = [len(doc) for doc in tokenized_docs]
    avg_doc_length = sum(doc_lengths) / len(doc_lengths)
    num_docs = len(tokenized_docs)

    document_frequency = Counter()
    for doc in tokenized_docs:
        document_frequency.update(set(doc))

    query_terms = _tokenize(query)
    scores = []
    for chunk, doc, doc_length in zip(chunks, tokenized_docs, doc_lengths):
        term_frequency = Counter(doc)
        score = 0.0
        for term in query_terms:
            if term not in term_frequency:
                continue
            df = document_frequency[term]
            idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1)
            freq = term_frequency[term]
            norm = 1 - BM25_B + BM25_B * doc_length / avg_doc_length
            score += idf * (freq * (BM25_K1 + 1)) / (freq + BM25_K1 * norm)
        if score > 0:
            scores.append({"chunk_id": chunk["chunk_id"], "score": score})

    scores.sort(key=lambda item: item["score"], reverse=True)
    return scores[:top_k]
