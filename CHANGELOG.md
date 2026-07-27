# Changelog

## v1.0.0

### Added
- Document ingestion: PDF/DOCX upload, parsing, chunking, embedding, and indexing into Pinecone + Supabase.
- Hybrid retrieval: dense search (Pinecone), a hand-written BM25 implementation, Reciprocal Rank Fusion, and NVIDIA reranking — selectable via `semantic` / `keyword` / `hybrid` modes.
- Grounded answer generation with an NVIDIA LLM, confidence scoring, citations, and an explicit no-answer fallback.
- `GET /api/documents` — lists every indexed document with its chunk count, for the dashboard.
- Streamlit UI: Dashboard, Upload, Search & Chat, and Retrieval Inspector pages.
- A pytest suite covering ingestion validation, all three search modes, citation/no-answer generation, and the upload/retrieval API endpoints (external services mocked).

### Changed
- Dashboard now reads from `GET /api/documents` instead of Streamlit session state, so the document list persists across page refreshes.

### Known Limitations
- No document delete/update endpoints — documents can be uploaded but not removed via the API.
- No pagination, filtering, or sorting on `GET /api/documents` — fine at portfolio scale, would need addressing for a large document set.
- Citations aren't deduplicated when multiple retrieved chunks land on the same page.
- No authentication — this is a single-user local/demo project, not a multi-tenant system.
- No CI/CD — tests are run manually with `pytest`.
