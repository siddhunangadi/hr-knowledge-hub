"""Stores chunk embeddings and metadata in Pinecone."""

from pinecone import Pinecone

from app.config.settings import get_settings
from app.ingestion.chunker import Chunk


class IndexingError(Exception):
    """Raised when writing vectors to Pinecone fails."""


def index_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    """Upsert one Pinecone vector per chunk, keyed by `{document_id}-{chunk_index}`."""
    settings = get_settings()
    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)

    vectors = [
        {
            "id": f"{chunk.document_id}-{chunk.chunk_index}",
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
        index.upsert(vectors=vectors)
    except Exception as exc:
        raise IndexingError(f"Failed to upsert vectors to Pinecone: {exc}") from exc
