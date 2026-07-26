"""Builds the single prompt sent to the LLM for grounded answer generation."""

from app.retrieval.retrieval_service import RankedChunk

NO_ANSWER_MESSAGE = "I couldn't find enough information inside the uploaded HR documents."

SYSTEM_INSTRUCTIONS = f"""You are an HR knowledge assistant. Answer the question using ONLY the
context below, which comes from the company's own HR documents.

Rules:
- Answer only using the provided context. Never use outside knowledge.
- If the answer is not present in the context, respond with exactly this sentence:
  "{NO_ANSWER_MESSAGE}"
- Keep answers concise and professional.
- Do not invent facts that are not stated in the context."""


def _build_context(chunks: list[RankedChunk]) -> str:
    """Format retrieved chunks into one context block, one chunk per section."""
    sections = [
        f"Document: {chunk.filename} (page {chunk.page_number})\n{chunk.text}" for chunk in chunks
    ]
    return "\n\n".join(sections)


def build_prompt(question: str, chunks: list[RankedChunk]) -> str:
    """Build the full prompt: system instructions + context + question."""
    context = _build_context(chunks)
    return f"""{SYSTEM_INSTRUCTIONS}

Context:
{context}

Question: {question}"""
