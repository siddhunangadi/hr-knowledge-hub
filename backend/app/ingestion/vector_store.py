"""Pinecone vector store — writes chunk embeddings, reads them back by similarity."""

from pinecone import Pinecone

from app.config.settings import get_settings
from app.ingestion.chunker import Chunk


class VectorStoreError(Exception):
    """Raised when a Pinecone read or write fails."""


_index = None


def _get_index():
    """Return the Pinecone index, creating the connection once and reusing it."""
    global _index
    if _index is None:
        settings = get_settings()
        pc = Pinecone(api_key=settings.pinecone_api_key)
        _index = pc.Index(settings.pinecone_index_name)
    return _index


def index_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    """Upsert one Pinecone vector per chunk, keyed by chunk.chunk_id."""
    vectors = [
        {
            "id": chunk.chunk_id,
            "values": embedding,
            "metadata": {
                "document_id": chunk.document_id,
                "filename": chunk.filename,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number or 0,
            },
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    try:
        _get_index().upsert(vectors=vectors)
    except Exception as exc:
        raise VectorStoreError(f"Failed to upsert vectors to Pinecone: {exc}") from exc


def query_vectors(embedding: list[float], top_k: int) -> list[dict]:
    """Return the top_k closest chunks as {chunk_id, score} dicts."""
    try:
        result = _get_index().query(vector=embedding, top_k=top_k)
    except Exception as exc:
        raise VectorStoreError(f"Failed to query Pinecone: {exc}") from exc

    return [{"chunk_id": match["id"], "score": match["score"]} for match in result["matches"]]
