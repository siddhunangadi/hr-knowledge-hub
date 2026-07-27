"""Dense retrieval: embed the query, search Pinecone for similar chunks."""

from app.ingestion.embedder import embedding_client
from app.ingestion.vector_store import query_vectors


def search_dense(query: str, top_k: int) -> list[dict]:
    """Return the top_k closest chunks as {chunk_id, score} dicts."""
    embedding = embedding_client.embed([query], input_type="query")[0]
    return query_vectors(embedding, top_k=top_k)
