"""Splits page texts into overlapping chunks with metadata."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


@dataclass
class Chunk:
    """A single chunk of document text with its metadata."""

    text: str
    document_id: str
    filename: str
    chunk_index: int
    page_number: int | None


def chunk_pages(pages: list[str], document_id: str, filename: str) -> list[Chunk]:
    """Split page texts into Chunk objects, preserving page numbers.

    DOCX files have no native page concept, so the parser returns a single
    "page" and every chunk is tagged page_number=1.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    chunks: list[Chunk] = []
    for page_number, page_text in enumerate(pages, start=1):
        for piece in splitter.split_text(page_text):
            chunks.append(
                Chunk(
                    text=piece,
                    document_id=document_id,
                    filename=filename,
                    chunk_index=len(chunks),
                    page_number=page_number,
                )
            )
    return chunks
