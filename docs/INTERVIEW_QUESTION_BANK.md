# HR Knowledge Hub — Internal Interview Question Bank

Target roles: Fresher GenAI Engineer / AI Developer / Backend AI (KPMG, HCLTech, Deloitte, EY, PwC, Capgemini, Infosys, Accenture)
Purpose: expose whether the candidate genuinely engineered this repository, calibrated to strong-fresher expectations.

---

## 1. Resume Walkthrough

**Purpose:** Establish baseline ownership before drilling into code.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★★

1. Walk me through this project in two minutes — what does it do, end to end? ★★★★★
2. What was your role — did you build this solo? ★★★★★
3. Of everything in this repo, which single file would you say you understand best, and why that one? ★★★★☆
4. What was the hardest bug you hit while building this? ★★★★★
5. If I asked you to rebuild the retrieval pipeline from scratch right now with no reference, what would you get wrong first? ★★★☆☆
6. What's one design decision in this repo you'd defend even if I pushed back hard? ★★★☆☆

---

## 2. Project Overview

**Purpose:** Confirm the candidate can describe the system's shape without reciting docs.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★★★

1. What are the four pipeline stages this system runs on document upload? (`ingestion_service.py:48`) ★★★★★
2. What are the three search modes, and what's actually different between them under the hood? (`retrieval_service.py:108`) ★★★★★
3. Why does `/api/chat` call retrieval internally instead of the frontend calling `/api/retrieval/search` first and `/api/chat` second? ★★★☆☆
4. Where does the Streamlit frontend get its data — direct DB access or HTTP? Why does that matter? (`streamlit_app.py:1-5`) ★★★★☆
5. Name every external service this system depends on to answer a single question. What happens to the answer if each one is down, one at a time? ★★★★☆

---

## 3. Business Problem

**Purpose:** Test whether the candidate can connect code to a real use case.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★★☆

1. What business problem does this solve for an HR department specifically? ★★★★★
2. Why can't employees just use ChatGPT for this instead? ★★★★★
3. Why does the system refuse to answer instead of guessing when a document doesn't contain the answer? (`prompt_builder.py:5-16`) ★★★★☆
4. Who is the end user of the Streamlit app — an HR admin, an employee, or both? Does the UI design reflect that? ★★★☆☆
5. What would happen, business-wise, if this gave a confidently wrong answer about a leave policy? ★★★★☆

---

## 4. Business Value

**Purpose:** Push beyond "it's RAG" into measurable value framing.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. How would you measure whether this tool is actually saving HR time, if you had to put a number on it? ★★★☆☆
2. What's the cost per query, roughly — which API calls does one question trigger, and which of those cost money? ★★★★☆
3. Why is citation display (`filename`, `page_number`) a business requirement, not just a nice-to-have? (`schemas.py:80-85`) ★★★★☆
4. If a consulting firm like Deloitte deployed this for a client, what would need to change before go-live? (see §51, §57) ★★★☆☆

---

## 5. Repository Structure

**Purpose:** Confirm familiarity with the physical layout.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★★☆

1. Why is the codebase split into `backend/` and `frontend/` as top-level directories instead of one flat `app/`? ★★★★☆
2. What lives in `app/repositories/` versus `app/ingestion/` versus `app/retrieval/` — draw the boundary. ★★★★☆
3. Why is there no `services/` folder even though each subpackage has a `*_service.py`? ★★☆☆☆
4. Why does `frontend/` sit outside `backend/app/` entirely rather than as a subpackage? ★★★☆☆

---

## 6. Code Organization

**Purpose:** Test whether module boundaries reflect actual understanding, not copy-paste.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. `embedder.py`, `llm_client.py`, and `reranker.py` are all "thin wrapper" clients with near-identical structure (`__init__`, one public method, module-level shared instance). Why not merge them into one `NVIDIAClient` base class? ★★★★☆
   - Follow-up: What would you lose if you did merge them? ★★★☆☆
   - Follow-up: Is this duplication or is it three genuinely different responsibilities? ★★★☆☆
2. Every client module ends with a module-level singleton comment ("Shared instance so ... reuses one client instead of creating a new one"). Why not just instantiate inside each function that needs it? ★★★★☆
3. Why does `vector_store.py` live under `ingestion/` when it's also used by `retrieval/dense_search.py`? ★★★☆☆
4. `retrieval_service.py` imports from `dense_search`, `hybrid_search`, `keyword_search`, and `reranker` — but `document_repository.py` for hydration. Why is chunk *storage* a repository but chunk *retrieval-scoring* a set of separate modules? ★★★☆☆

---

## 7. Python

**Purpose:** Verify baseline language fluency as used in this codebase (not academic Python trivia).
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★★

1. What does `@lru_cache` do on `get_settings()`, `_get_index()`, and `_get_client()`? Why use it here instead of a global variable set at import time? (`settings.py:57`, `vector_store.py:20`, `document_repository.py:16`) ★★★★★
2. What's the difference between the module-level `embedding_client = NVIDIAEmbeddingClient()` singleton pattern (`embedder.py:45`) and the `@lru_cache`-wrapped factory function pattern (`vector_store.py:20-25`)? Why does this repo use both? ★★★★☆
3. What does `@dataclass` buy you in `Chunk` and `IngestionResult` over a plain class or a dict? (`chunker.py:13`, `ingestion_service.py:28`) ★★★★☆
4. Explain the `chunk_id` property on `Chunk` — why compute it instead of storing it as a field? (`chunker.py:23-26`) ★★★☆☆
5. `TOKEN_PATTERN = re.compile(r"[a-z0-9]+")` is compiled once at module import. Why not compile it inside `_tokenize()`? (`keyword_search.py:14`) ★★★☆☆
6. What does `from __future__ import annotations` do, and why is it in `chunker.py` and `streamlit_app.py` but not, say, `main.py`? ★★☆☆☆
7. Walk through `list[dict[str, dict]]`-style type hints used across the repo (e.g. `fetch_chunks_by_ids` return type). Are these enforced at runtime? ★★★☆☆

---

## 8. OOP

**Purpose:** Fresher-appropriate OOP reasoning grounded in the three client classes and one dataclass.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★☆

1. `NVIDIAEmbeddingClient`, `NVIDIARerankerClient`, `NVIDIALLMClient` — none of them inherit from a common base class despite sharing a shape. Is that a missed abstraction or a deliberate choice? Argue both sides. ★★★★☆
2. Why is `RankedChunk` a dataclass but the retrieval functions (`search_dense`, `search_bm25`) return plain `list[dict]` instead? Why the inconsistency? (`retrieval_service.py:16-24` vs `dense_search.py:7-10`) ★★★★☆
3. What's the point of custom exception classes like `EmbeddingError`, `VectorStoreError`, `RerankError`, `LLMError` when they all just wrap and re-raise? Why not one `ExternalServiceError`? ★★★★☆
4. There's no class at all for the retrieval or generation "service" — just module-level functions. When would you introduce a class instead of a module of functions? ★★★☆☆

---

## 9. FastAPI

**Purpose:** Confirm the candidate can explain the framework mechanics actually used.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Walk through what happens, line by line, when a POST hits `/api/chat`. (`chat.py:19-53`) ★★★★★
2. What does `response_model=ChatResponse` actually do for you — what happens if `generate_answer()` returns a dict missing a required field? ★★★★☆
3. Why does every router use `APIRouter(prefix=...)` instead of hardcoding the full path on every route? (`chat.py:15`, `documents.py:18`) ★★★☆☆
4. `upload_document` is `async def` but every other endpoint is a plain `def`. Why the difference? (`documents.py:35` vs `documents.py:23`) ★★★★☆
5. How does FastAPI turn a raised `HTTPException(status_code=502, detail=...)` into an actual HTTP response? ★★★★☆
6. Where is dependency injection (FastAPI's `Depends()`) used in this codebase? If nowhere, why not, given the codebase's stated production drift issue with binding? ★★★☆☆

---

## 10. API Design

**Purpose:** Ownership questions on endpoint shape and contract choices.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Why is `/api/chat` a separate endpoint from `/api/retrieval/search` instead of one endpoint with a "generate answer" flag? (`chat.py:15`, `retrieval.py:14`) ★★★★☆
2. Why does `SearchRequest` default `top_k=8` and `search_mode="hybrid"`? Who decided 8, and what breaks if it were 3 or 50? (`schemas.py:33-34`) ★★★★☆
3. `POST /api/documents/upload` returns 400 for unsupported type/size but 422 for parsing failure. Why two different status codes for what both feel like "bad file"? (`documents.py:45-48`) ★★★★☆
4. Why is there no `DELETE /api/documents/{id}` endpoint? (documented as a known limitation in CHANGELOG) What would it need to touch — just Supabase, or Pinecone too? ★★★★☆
5. `GET /api/documents` has no pagination. At what document count does that become a real problem, and where exactly does it break — the endpoint, the query, or the Streamlit table render? ★★★☆☆
6. Why does `debug: bool` live in the request body (`SearchRequest.debug`) instead of being a query parameter like `?debug=true`? ★★☆☆☆

---

## 11. Dependency Injection

**Purpose:** This repo does NOT use a DI framework — probe whether the candidate notices and can reason about it.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★☆☆☆

1. FastAPI has a first-class `Depends()` system. This repo doesn't use it anywhere — how are dependencies (settings, clients) actually wired instead? ★★★★☆
2. If you wanted to unit test `chat()` in `chat.py` with a fake `generate_answer`, how would you do it given there's no DI? What did the test suite actually do instead? (`test_api.py:16` — `@patch`) ★★★★☆
3. What's the tradeoff of `@patch("app.api.documents.ingest_document")`-style testing versus constructor-injected dependencies? ★★★☆☆
4. Would introducing `Depends()` for the Supabase/Pinecone clients make this codebase better or just bigger? ★★★☆☆

---

## 12. Configuration

**Purpose:** Test understanding of the single `Settings` class.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★☆

1. Walk through how `_ENV_FILE` is resolved. Why `Path(__file__).resolve().parent.parent.parent.parent` instead of a relative path like `"../../.env"`? (`settings.py:12`) ★★★★☆
2. Why is the comment on line 8-11 saying it's "harmless if missing" important — what happens in Docker if `.env` genuinely doesn't exist? ★★★★☆
3. What does `extra="ignore"` do in `SettingsConfigDict`, and why would you want it here? (`settings.py:18`) ★★★☆☆
4. Every setting has a default (`= ""` or a real URL) even the API keys. What happens at runtime if `nvidia_llm_api_key` is left as `""` and a chat request comes in? Trace it. ★★★★☆
5. Why is `get_settings()` wrapped in `@lru_cache` — what would go wrong (or just get slower) without it? ★★★★☆

---

## 13. Environment Variables

**Purpose:** Confirm the candidate actually configured deployment, not just local dev.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★★☆

1. Compare `.env.example`, `docker-compose.yml`'s `env_file: .env`, and `render.yaml`'s `envVars` list — why three different mechanisms for the same variables? ★★★★☆
2. What does `sync: false` mean for `NVIDIA_EMBEDDING_API_KEY` in `render.yaml:22-23`? Why is it set for the API keys but not for `PINECONE_INDEX_NAME`? ★★★★☆
3. `CORS_ORIGINS` defaults to `["*"]` in both `.env.example` and `render.yaml`. What's the actual risk of that in this specific deployment (single-user demo) versus a real HR system with employee data? ★★★★☆
4. Why does `render.yaml` set `BACKEND_URL=http://localhost:8000` when the Streamlit `streamlit_app.py` reads `BACKEND_URL` via `os.getenv` — walk through whether that value is even correct given the container's process layout. ★★★☆☆

---

## 14. Logging

**Purpose:** Fresher-level logging hygiene.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★☆☆

1. Why does `setup_logging()` get called once in `main.py:14`, at import/startup time, rather than per-request? (`main.py:13-14`, `logging_config.py:6-11`) ★★★☆☆
2. Every API layer uses `logger.exception(...)` before raising `HTTPException`. What does `logger.exception` capture that `logger.error` wouldn't? (`chat.py:30`) ★★★★☆
3. Why log at the API layer instead of inside `generate_answer()` or `ingest_document()` where the actual failure happens? ★★★★☆
4. There's no request-ID or correlation-ID in the log format. Why might that matter once this handles concurrent users? (`logging_config.py:10`) ★★☆☆☆
5. `log_level` is `INFO` by default in both `.env.example` and `render.yaml`. What would you miss in production debugging that `DEBUG` would show? ★★☆☆☆

---

## 15. Exception Handling

**Purpose:** Deep-dive the layered exception strategy — a genuinely well-thought-out part of the repo.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Every external-service module defines its own exception (`EmbeddingError`, `VectorStoreError`, `RerankError`, `LLMError`, `DocumentRepositoryError`). Why not one shared `ExternalServiceError` raised everywhere? ★★★★★
2. In `chat.py`, five different exceptions map to five different log messages but the *same* 502 status code. If they all return 502 anyway, what's the value of catching them separately? ★★★★☆
3. `ingestion_service.py` doesn't catch any exceptions itself — it lets `EmbeddingError`, `VectorStoreError`, `DocumentParsingError` propagate up to `documents.py`. Why put the try/except at the API layer instead of the service layer? ★★★★☆
4. Every custom exception wraps the original with `raise X(...) from exc`. What does `from exc` actually preserve, and why does it matter for debugging a 502 in production logs? (`embedder.py:37`) ★★★★☆
5. What happens today if Supabase's `save_document()` succeeds but `save_chunks()` then fails? (`ingestion_service.py:65-66`) Is the system left in a consistent state? ★★★★★
   - Follow-up: The code comment says Pinecone is written before Supabase "so a retry starts clean" (`ingestion_service.py:61-64`) — does that reasoning also protect against a Supabase-only partial failure? ★★★★☆
   - Follow-up: How would you fix this without adding a full transaction system? ★★★☆☆

---

## 16. Validation

**Purpose:** Test understanding of where validation lives and why.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★☆

1. `validate_upload()` checks content-type against a fixed dict and file size against a constant. Why is this the "only pure logic in the ingestion pipeline" per the test file's own docstring? (`test_ingestion.py:1`) ★★★★☆
2. Why check `content_type not in SUPPORTED_CONTENT_TYPES` rather than checking the filename extension? What's the security/reliability tradeoff? (`ingestion_service.py:41`) ★★★★☆
3. `content_type` comes from the client (`file.content_type`) — can a malicious or careless client just lie about it? What actually stops a `.exe` renamed to `.pdf` with a spoofed content-type from getting this far? ★★★★☆
4. Pydantic validates `SearchRequest` shape automatically. What does Pydantic *not* validate here — e.g. is `top_k=-5` or `top_k=100000` rejected? Trace what happens if it isn't. ★★★★☆
5. Why is `MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024` checked in application code (`ingestion_service.py:13,43`) instead of, say, a FastAPI/Starlette upload-size limit or an nginx config? ★★★☆☆

---

## 17. Data Models

**Purpose:** Pydantic schema design reasoning.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. `Citation` only exposes `filename` and `page_number` — no score, no chunk_id. Why hide those from the public API when `_build_citations()` internally keeps `chunk_id`? (`schemas.py:80-85`, `generation_service.py:49-59`) ★★★★★
2. `RankedResult` and `RerankedResult` are nearly identical (`chunk_id`/`score` vs `index`/`score`). Why two separate models instead of one? ★★★☆☆
3. `RetrievalDebugInfo` defaults every list field to `[]`. What would break in the Streamlit inspector page if these defaulted to `None` instead? (`schemas.py:66-69`, `streamlit_app.py:256-263`) ★★★★☆
4. Why is `page_number: Optional[int]` on `ChunkResponse` and `Citation` but not on `RankedChunk`'s dataclass equivalent (`retrieval_service.py:23` uses plain `int`)? Is that inconsistency intentional? ★★★☆☆
5. `SearchMode = Literal["semantic", "keyword", "hybrid"]` — what happens if a client sends `search_mode: "fuzzy"`? Where does that get rejected? (`schemas.py:7`) ★★★★☆

---

## 18. Document Processing

**Purpose:** PDF/DOCX parsing decisions.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Why PyMuPDF (`fitz`) for PDFs instead of `PyPDF2` or `pdfplumber`? What would you check before picking one? ★★★★☆
2. `parse_docx()` joins all paragraphs into one page (`parser.py:22-27`) — why does DOCX have "no page concept" but PDF does? What real-world consequence does that have for citations on a DOCX source? ★★★★☆
3. `parse_pdf` returns `list[str]`, one entry per page — this becomes the unit that `chunk_pages` iterates over for `page_number`. What happens to page numbers for a scanned/image-only PDF where `page.get_text()` returns empty strings? ★★★★☆
4. Both parsers wrap all failures in a single broad `except Exception` and re-raise as `DocumentParsingError`. What's the risk of catching `Exception` this broadly? ★★★☆☆
5. What happens if a legitimate DOCX file is renamed to `.pdf` and uploaded — where does it fail, and with what error? Trace it through `validate_upload` → `parse_pdf`. ★★★★☆

---

## 19. Chunking

**Purpose:** Core RAG mechanics — must be second nature.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. What splitter is used, and why `RecursiveCharacterTextSplitter` specifically rather than a fixed-length character splitter? (`chunker.py:7,35-37`) ★★★★★
2. Why chunk per-page (looping over `pages`) rather than joining all pages into one string and chunking that? (`chunker.py:40-41`) ★★★★☆
3. `chunk_index` is assigned as `len(chunks)` — a running counter across the *whole document*, not per page. Why not reset it per page? (`chunker.py:47`) ★★★☆☆
4. What information would you lose about a chunk if you didn't track `page_number` at all? ★★★★☆

---

## 20. Chunk Size Decisions

**Purpose:** Probe whether 500 was a real decision or a copied default.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★★

1. `CHUNK_SIZE = 500` — why 500 characters and not 300, or 1000? How did you land on this number? (`chunker.py:9`) ★★★★★
2. If you doubled `CHUNK_SIZE` to 1000, what would you expect to happen to: retrieval precision, LLM context length per query, embedding cost per document, and answer quality on a question whose answer spans two paragraphs? ★★★★☆
3. Would you use a different chunk size for a 2-page leave policy PDF versus a 200-page employee handbook? Why or why not? ★★★★☆
4. This chunk size is measured in characters, not tokens. Why does that distinction matter when the embedding model has a token limit, not a character limit? ★★★☆☆
5. How would chunk size need to change for legal contracts (dense, clause-based) versus expense-report tables (structured, low prose density)? ★★★☆☆

---

## 21. Chunk Overlap Decisions

**Purpose:** Same rigor as chunk size, applied to overlap.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. `CHUNK_OVERLAP = 50` is 10% of `CHUNK_SIZE`. Is that ratio a coincidence or deliberate? (`chunker.py:10`) ★★★★☆
2. What specific retrieval failure does overlap prevent — walk through a concrete sentence that straddles a chunk boundary. ★★★★★
3. What's the cost of overlap — in storage, in embedding calls, in Pinecone index size? (`chunker.py:9-10`, `embedder.py:18`) ★★★★☆
4. If overlap were 0, what would you expect to observe in the Retrieval Inspector page on a real query? ★★★☆☆
5. Is there a point where increasing overlap stops helping and starts hurting (redundant near-duplicate chunks competing in the reranker)? ★★★☆☆

---

## 22. Embedding Model Decisions

**Purpose:** NVIDIA NIM embedding choice reasoning.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Why `nvidia/nv-embedqa-e5-v5` specifically — what does "e5" and "qa" in the name tell you about what it's optimized for? (`settings.py:29`) ★★★☆☆
2. `embed()` takes an `input_type` param that's `"passage"` for ingestion and `"query"` for search (`embedder.py:18-23`). Why does the same model need to know which side of the pair it's embedding? What breaks if you always pass `"passage"`? ★★★★★
3. Why NVIDIA NIM hosted embeddings instead of running a local `sentence-transformers` model? What's the tradeoff in latency, cost, and infra complexity? ★★★★☆
4. If the embedding model were swapped for a different one with a different vector dimension, what else in this system would need to change? (Hint: Pinecone index config.) ★★★★☆
5. What happens to previously-indexed vectors in Pinecone if you swap embedding models without re-ingesting every document? ★★★★☆

---

## 23. Vector Database Decisions

**Purpose:** Pinecone usage patterns.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Walk through `index_chunks()` — why batch upserts at 100 vectors instead of sending everything in one call? (`vector_store.py:15-17,46-47`) ★★★★★
2. The comment says Pinecone rejects requests over 4MB and 100 vectors "keeps each request well under that limit regardless of document size" — is that actually true regardless of embedding dimension? What if the embedding model produced 4096-dim vectors instead of ~1024? ★★★★☆
3. Why store `document_id`, `filename`, `chunk_index`, `page_number` as Pinecone metadata (`vector_store.py:34-39`) when the same data is *also* stored in Supabase (`document_repository.py:33-49`)? Isn't that duplication? ★★★★★
4. `query_vectors()` doesn't pass a `filter` to `.query()` — every search hits the entire index regardless of which document the user cares about. What would you need to add to scope a search to one document? ★★★☆☆
5. `page_number or 0` in the metadata dict (`vector_store.py:38`) — what case is this defending against, and why is `0` a safe sentinel here? ★★★☆☆

---

## 24. Pinecone Decisions

**Purpose:** Deep dive specifically on the chosen vector DB (separate from generic vector DB questions above).
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★☆

1. Why Pinecone specifically? ★★★★★
   - Follow-up: Why not pgvector, given you're already running Postgres via Supabase? ★★★★★
   - Follow-up: Suppose Pinecone has an outage right now. What breaks first — upload, search, or chat? Trace the exception path. (`vector_store.py:11-25`, `chat.py:32-34`) ★★★★☆
   - Follow-up: What compromises would you make to keep the system partially functional during a Pinecone outage? (e.g., degrade to keyword-only mode) ★★★☆☆
2. `_get_index()` is `@lru_cache`d with no arguments — meaning one process gets exactly one Pinecone connection for its lifetime. What happens if the API key rotates while the process is running? ★★★☆☆
3. This system uses one Pinecone index (`hr-knowledge-hub`) for everything. What would multi-tenant isolation (per-company documents) require — separate indexes, or namespaces within one index? ★★★★☆

---

## 25. Alternative Technologies

**Purpose:** Test breadth beyond what was chosen.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. Why Supabase for chunk text storage instead of storing it directly as Pinecone metadata (Pinecone does support metadata text)? ★★★★☆
2. Why NVIDIA NIM for the LLM instead of OpenAI, Anthropic, or a self-hosted model? ★★★★☆
3. Why FastAPI instead of Flask or Django for the backend? ★★★☆☆
4. Why Streamlit instead of a React/Next.js frontend, given the backend is already a clean REST API? ★★★★☆
5. Why write BM25 by hand (`keyword_search.py`) instead of using `rank_bm25` or Elasticsearch? ★★★★★

---

## 26. Retrieval Pipeline

**Purpose:** End-to-end pipeline tracing.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Trace a hybrid-mode query end to end: what function calls happen in what order, from `search()` to the final `RankedChunk` list? (`retrieval_service.py:66-105`) ★★★★★
2. Why does `_search_hybrid` fetch `candidate_k = top_k * CANDIDATE_MULTIPLIER` chunks from dense and BM25 but only return `top_k` at the end? (`retrieval_service.py:68,84`) ★★★★★
3. Why is `_hydrate()` a separate function used only by semantic and keyword modes, while hybrid mode has its own inline hydration logic (`chunks_by_id = fetch_chunks_by_ids(...)`)? Isn't that duplicated logic? (`retrieval_service.py:27-45` vs `74-79`) ★★★★☆
4. What does the comment "Skips any chunk_id ... that has no matching Supabase row" mean in practice — under what real conditions would Pinecone and Supabase drift? (`retrieval_service.py:31-32`) ★★★★★

---

## 27. Dense Retrieval

**Purpose:** Simplest pipeline path — confirm fundamentals.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy
**Interview Frequency:** ★★★★☆

1. `search_dense` is 10 lines. Walk through exactly what happens on each line. (`dense_search.py`) ★★★★☆
2. Why `input_type="query"` here but `input_type="passage"` in `embedder.embed()` calls during ingestion? ★★★★★
3. Semantic mode alone (no BM25, no rerank) — when would you recommend a user pick this mode over hybrid? ★★★☆☆

---

## 28. BM25

**Purpose:** The hand-rolled implementation is a strong ownership signal — probe hard here.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. Explain the BM25 formula as implemented here, term by term — what do `idf`, `freq`, `norm` each represent? (`keyword_search.py:38-48`) ★★★★★
2. Why `BM25_K1 = 1.5` and `BM25_B = 0.75`? Where do these numbers come from — did you derive them or are they the standard defaults? (`keyword_search.py:9-10`) ★★★★☆
3. What does `BM25_B` control — walk through what happens to scoring for a very long chunk versus a very short one as `B` moves from 0 to 1. ★★★★☆
4. `search_bm25()` calls `fetch_all_chunks()` and recomputes document frequency **on every single search request** — no persisted index. What's the performance ceiling of this approach, and at what document count does it become a real problem? (`keyword_search.py:23,32-34`) ★★★★★
5. Why regex-tokenize with `[a-z0-9]+` instead of `str.split()`? What real query would break with a naive split? (`keyword_search.py:12-14`) ★★★★☆
6. There's no stemming or stopword removal here. What's the practical effect of that on a query like "what is the policy for leaves"? ★★★☆☆
7. If a chunk scores 0 for every query term, it's excluded entirely (`if score > 0`) rather than included with score 0 (`keyword_search.py:49`). Why does that matter for how many total chunks the fusion step downstream actually sees? ★★★☆☆

---

## 29. Hybrid Search

**Purpose:** Confirm understanding of why hybrid exists and how it's assembled.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. What specific weakness of dense-only search does BM25 cover, and vice versa? Give a concrete HR-document example for each. ★★★★★
2. Hybrid mode runs dense, BM25, RRF, *and* a reranker — four stages. Why not stop at RRF and skip the reranker call (saving one API round-trip)? ★★★★☆
3. What's the latency cost of hybrid mode versus semantic-only, in terms of number of network calls? Count them. (`retrieval_service.py:66-81`) ★★★★☆

---

## 30. Reciprocal Rank Fusion

**Purpose:** RRF mechanics and rationale.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Explain RRF's formula: `1 / (RRF_K + rank)`. Why use rank instead of the raw scores? (`hybrid_search.py:9-13,19,23`) ★★★★★
2. Why `RRF_K = 60`? What happens to the fused ranking if `RRF_K` were 1 instead of 60? ★★★★☆
3. A chunk that appears in *both* dense and BM25 results gets its scores summed (`fused_scores[chunk_id] = fused_scores.get(...) + ...`, lines 19 and 23). What does that mean semantically — why should appearing in both lists boost a chunk? (`hybrid_search.py:15-23`) ★★★★★
4. Why is RRF necessary at all — why not just normalize the dense cosine scores and BM25 scores onto the same 0-1 scale and sum those directly? ★★★★☆

---

## 31. Candidate Multiplier

**Purpose:** A specific, named constant — good ownership probe.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. `CANDIDATE_MULTIPLIER = 4` — why 4 and not 2 or 10? (`retrieval_service.py:13`) ★★★★★
2. The comment says this gives RRF and the reranker "enough chunks to actually reorder." What would happen with a multiplier of 1 — would RRF even do anything meaningful? ★★★★☆
3. What's the cost of a higher multiplier — trace it through BM25's full-corpus rescan, Supabase hydration, and reranker API payload size. (`keyword_search.py:23`, `retrieval_service.py:75-81`) ★★★★☆
4. If `top_k=8` and `CANDIDATE_MULTIPLIER=4`, how many passages get sent to the NVIDIA reranker per hybrid query? ★★★☆☆

---

## 32. Top-K

**Purpose:** Default value reasoning.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★☆

1. `top_k: int = 8` default in `SearchRequest` — why 8? What tradeoff does a higher top_k create for the LLM prompt in `_build_context()`? (`schemas.py:33`, `prompt_builder.py:19-24`) ★★★★☆
2. The Streamlit frontend hardcodes `DEFAULT_TOP_K = 8` again separately (`streamlit_app.py:16`) rather than reading it from the backend. Why is that a maintenance risk? ★★★☆☆
3. What happens to LLM cost and latency if a user could set `top_k=100`? Is there any server-side cap? ★★★★☆

---

## 33. Reranker

**Purpose:** NVIDIA reranker integration specifics.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Walk through `rerank()` — why does it return `index` referring to position in the input `passages` list rather than a chunk_id? (`reranker.py:18-22,38-39`) ★★★★☆
2. In `_search_hybrid`, after reranking, the code does `fused_chunk_ids[item["index"]]` to map back to a real chunk_id (`retrieval_service.py:85`). What would happen if `fused_chunk_ids` and the `passages` list sent to the reranker ever got out of sync? ★★★★★
3. Why is the field named `logit` in the raw API response but exposed as `score` in this codebase's return value? (`reranker.py:38`) Does that renaming lose any information downstream? ★★★☆☆
4. The reranker is only used in hybrid mode, not semantic or keyword mode. Why not always rerank, even for semantic-only search? ★★★★☆

---

## 34. Prompt Engineering

**Purpose:** System prompt design.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Walk through every rule in `SYSTEM_INSTRUCTIONS` and explain what failure mode each one is defending against. (`prompt_builder.py:7-16`) ★★★★★
2. Why does the no-answer sentence get embedded *verbatim* into the system prompt via an f-string (`f"""...{NO_ANSWER_MESSAGE}..."""`) rather than just describing the behavior in words? (`prompt_builder.py:5,12-13`) ★★★★☆
3. The last rule handles "multiple retrieved documents contain different or conflicting information" by preferring the highest-ranked chunk (`prompt_builder.py:16`). What real HR scenario would trigger this — think about policy versions. ★★★★★
4. Why include the document filename and page number in each context section (`_build_context`) rather than just the raw text? (`prompt_builder.py:19-24`) ★★★★☆
5. `temperature=0.2` in the LLM call, not `0`. Why not exactly 0 for a system that needs deterministic, grounded answers? (`llm_client.py:27`) ★★★★☆

---

## 35. Grounding

**Purpose:** Core RAG safety mechanism.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. What is "grounding" in this system, concretely — point to the exact code/prompt line that enforces it. (`prompt_builder.py:10-11`) ★★★★★
2. Is grounding enforced by the LLM's judgment alone, or is there any code-level check that the answer text actually appears in the retrieved context? What does that imply about trust in the model? (`generation_service.py:63-89`) ★★★★★
3. What happens if the LLM ignores the system prompt and answers from outside knowledge anyway — is there any downstream guardrail that would catch that? ★★★★☆

---

## 36. Hallucination Prevention

**Purpose:** Distinguish this from grounding — the no-answer fallback and citation logic.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. Two separate mechanisms prevent hallucination here: the prompt rule, and the empty-chunks fallback in `generate_answer()`. Explain both, and explain why you need the second one even with the first. (`prompt_builder.py:12-13`, `generation_service.py:76-77`) ★★★★★
2. Why does `generate_answer` skip calling the LLM entirely when `chunks` is empty, rather than always calling the LLM and trusting it to say "I don't know"? (`generation_service.py:76-77`) ★★★★☆
3. What's the difference between "no chunks retrieved" and "chunks retrieved but LLM says NO_ANSWER_MESSAGE anyway"? Does the code distinguish these two cases? (`generation_service.py:76-85`) ★★★★☆
4. Citations are explicitly emptied when the answer equals `NO_ANSWER_MESSAGE` (`generation_service.py:81-84`). What UX problem would showing citations alongside "I don't know" create? ★★★★☆

---

## 37. Citation Generation

**Purpose:** How sources are surfaced to the user.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. `_build_citations()` builds citations from the *retrieved chunks*, not from parsing the LLM's answer text. What does that mean if the LLM only actually used 2 of the 8 retrieved chunks to write its answer — will all 8 still show as citations? (`generation_service.py:49-60`) ★★★★★
2. The CHANGELOG explicitly lists "Citations aren't deduplicated when multiple retrieved chunks land on the same page" as a known limitation. Why would that happen given `CHUNK_OVERLAP`? How would you fix it — where in the code? ★★★★☆
3. Why does `_build_citations` keep `chunk_id` internally but the public `Citation` schema drops it? Trace exactly where that field gets dropped. (`generation_service.py:49-59`, `schemas.py:80-85`, `chat.py:45`) ★★★★☆

---

## 38. Confidence Calculation

**Purpose:** The most mathematically involved piece of business logic in the repo — probe deeply.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. Walk through `_estimate_confidence()` end to end: what's `center`, what's `spread`, and what does the sigmoid do at the end? (`generation_service.py:20-46`) ★★★★★
2. Why does each search mode (hybrid/semantic/keyword) need its own `center`/`spread` calibration instead of one formula for all three? (`generation_service.py:10-24`) ★★★★★
3. The code comment admits the calibration values are "a rough calibration from real examples ... not derived analytically." What does that actually mean you did to arrive at `-3.0`/`2.0` for hybrid? Walk me through how you'd have actually done that calibration. ★★★★★
4. Why use *only* the top chunk's score rather than averaging across all returned chunks? The comment gives a reason (`generation_service.py:35-38`) — do you agree with it, or can you construct a query where averaging would give a better confidence estimate? ★★★★☆
5. Confidence is explicitly "informational only — it does not gate whether the LLM is called" (`generation_service.py:66-70`). Why not use a low confidence score to skip the LLM call and save money, the way the empty-chunks case does? ★★★★★
6. What happens to confidence if you swap the reranker model for a different one with a completely different logit range? Would the current calibration silently start producing wrong percentages? ★★★★☆
7. The Streamlit UI buckets confidence into three tiers at 70% and 40% (`streamlit_app.py:186-191`). Are those thresholds arbitrary or tied to the calibration math above? ★★★☆☆

---

## 39. Response Generation

**Purpose:** Full generation flow, one level up from confidence specifically.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Trace `generate_answer()` top to bottom — what's computed, in what order, and what's returned in each branch (empty chunks vs. real chunks)? (`generation_service.py:63-89`) ★★★★★
2. Why is `debug` threaded all the way from the API request through `search()`, `generate_answer()`, into the response — what's it for, and who consumes it? (`chat.py:20-27`, `generation_service.py:63,87-88`) ★★★★☆
3. Why 70B instead of the 8B model for generation — what specific failure mode was observed with 8B? (`settings.py:41-46`) ★★★★★
   - Follow-up: The comment says the 8B model failed on "indirect / inferential questions" even with the correct chunk in context, and answered correctly once rephrased as a direct question. What does that tell you about the difference between a retrieval problem and a reasoning problem? ★★★★☆
   - Follow-up: How would you go about detecting/reproducing that kind of failure systematically instead of anecdotally? ★★★☆☆

---

## 40. Performance

**Purpose:** Latency reasoning across the stack.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. For a single hybrid-mode `/api/chat` call, list every network round-trip that happens, in order, and estimate which one dominates latency. ★★★★★
2. `search_bm25()` rescans and rescoring *every* stored chunk on every query (`keyword_search.py:23,27-48`) — no caching, no persisted inverted index. At what corpus size does this start to hurt, and what would you replace it with first? ★★★★☆
3. Why is the LLM call given a 90-second timeout while embedding/rerank get 30 seconds? (`llm_client.py:29-32` vs `embedder.py:33`, `reranker.py:32`) ★★★★☆
4. The Streamlit `_post_json` call for chat uses `timeout=120` — comment explains it accounts for the 90s LLM timeout plus retrieval time (`streamlit_app.py:203-209`). Is 120 enough headroom, or is it cutting it close? ★★★☆☆

---

## 41. Scalability

**Purpose:** Where does this design fall over at scale.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★☆

1. This is explicitly a "portfolio scale" project per the CHANGELOG. Name the three things that would break first under real load, in order. ★★★★★
2. BM25 recomputing over the full corpus per-query is the most obvious scaling bottleneck. What's the actual algorithmic complexity of `search_bm25()` per call, in terms of corpus size and document length? ★★★★☆
3. `render.yaml` runs the app on the `free` plan with a single instance running both uvicorn *and* Streamlit in one container via a shell `&`. What happens under concurrent traffic — does Render autoscale this, and if it did, what would go wrong? (`render.yaml:2-10`) ★★★★☆
4. What's the concurrency model of `search_bm25()` under multiple simultaneous requests — is there any shared mutable state that could race? ★★★☆☆

---

## 42. Security

**Purpose:** Baseline security awareness for a document-handling system.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. There's no authentication anywhere in this API. What's the actual blast radius if this were deployed with real employee HR documents instead of demo data? (CHANGELOG "Known Limitations") ★★★★★
2. `CORS_ORIGINS = ["*"]` combined with `allow_credentials=True` in `main.py:18-24` — is that combination actually valid per the CORS spec, and if not, what does the browser do about it? ★★★★☆
3. API keys for NVIDIA, Pinecone, and Supabase are all loaded via `Settings` with empty-string defaults (`settings.py:27,32,39,49,53-54`). What happens if `.env` is accidentally committed to git? Check: is it gitignored? ★★★★★
4. Uploaded file bytes go straight into `fitz.open(stream=file_bytes, ...)` and `docx.Document(io.BytesIO(file_bytes))` — what's the risk profile of parsing untrusted binary files with these libraries? ★★★☆☆
5. Why bind uvicorn to `127.0.0.1` inside the Dockerfile (`Dockerfile:14`) but the comment in memory notes `render.yaml` binds `0.0.0.0` — what's the actual exposure difference, and which one is currently live? ★★★★☆

---

## 43. Docker

**Purpose:** Deployment container mechanics — an area with a real, documented bug.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★☆

1. Walk through the Dockerfile's `CMD` line — why background the uvicorn process with `&` instead of running two separate containers? (`Dockerfile:14`) ★★★★★
2. What happens if uvicorn crashes 5 seconds after container start — does Docker or Render notice, given Streamlit (the foregrounded process) is what's actually being monitored? ★★★★★
3. `EXPOSE 8501` — why 8501 and not 8000, given the backend is also running inside this container? (`Dockerfile:12`) ★★★★☆
4. uvicorn binds to `127.0.0.1` in the Dockerfile's CMD (`--host 127.0.0.1`) — why localhost-only, and how does Streamlit still reach it? Where does Streamlit get the backend URL from inside this container? (`Dockerfile:14`, `streamlit_app.py:14`) ★★★★★
5. There's no multi-stage build and no `.dockerignore` reference visible — what's being copied into the image that doesn't need to be? (`Dockerfile:8-10`) ★★★☆☆

---

## 44. Deployment

**Purpose:** Render-specific configuration and drift.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★★

1. `render.yaml`'s `startCommand` binds uvicorn to `0.0.0.0:8000` (`render.yaml:9`) but the Dockerfile's `CMD` binds it to `127.0.0.1:8000` (`Dockerfile:14`). Which one actually runs when deployed to Render — does Render use the Dockerfile or `render.yaml`'s `startCommand`? ★★★★★
   - Follow-up: If both configs are present and disagree, which wins, and is that a bug you'd want to fix before calling this "production ready"? ★★★★★
2. Why does `render.yaml` use `runtime: python` with an explicit `buildCommand`/`startCommand` rather than `runtime: docker` pointing at the `Dockerfile`, when a Dockerfile clearly exists? ★★★★☆
3. `render.yaml` runs on `plan: free`. What are the real operational consequences of the free plan for a RAG app specifically (cold starts, no persistent disk, sleep after inactivity)? ★★★★☆
4. Why does `$PORT` get used for Streamlit's port in `render.yaml` (`--server.port $PORT`) but a hardcoded `8000` for uvicorn? What does Render's platform actually require here? (`render.yaml:9-10`) ★★★★☆
5. `docker-compose.yml` runs backend and frontend as two *separate* containers/services, but the production Dockerfile colocates them in one. Why the divergence between local dev and production topology? (`docker-compose.yml:1-26` vs `Dockerfile`) ★★★★★

---

## 45. Testing

**Purpose:** Testing philosophy and coverage boundaries.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium
**Interview Frequency:** ★★★★★

1. `test_ingestion.py`'s docstring says it covers "the only pure logic in the ingestion pipeline." What does that imply is *not* tested about ingestion, and why not? (`test_ingestion.py:1`) ★★★★★
2. `test_api.py`'s docstring explicitly says it verifies "HTTP wiring, not the underlying logic (already covered in ...)". Why draw that boundary — what would be redundant about testing business logic again at the API layer? (`test_api.py:1-3`) ★★★★★
3. There's no test file for `chunker.py`, `parser.py`, `embedder.py`, `llm_client.py`, or `reranker.py` directly. Is that a gap, or intentional given they're thin external-API wrappers? ★★★★☆
4. There's no test for `_estimate_confidence()` — arguably the most complex pure-math function in the repo. Why might that be the single most important missing test in this suite? ★★★★★

---

## 46. pytest

**Purpose:** pytest mechanics as actually used.
**Expected Fresher Depth:** Must Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★★☆

1. What does `pytest.ini` configure for this project, and why does it matter where `pytest` is run from? ★★★☆☆
2. `test_validate_upload_rejects_oversized_file` uses `pytest.raises(FileTooLargeError)` — walk through what that context manager actually asserts. (`test_ingestion.py:26-29`) ★★★★☆
3. Why are the imports inside each test function (`from app.retrieval.retrieval_service import search`) rather than at the top of the test file, in `test_retrieval.py` and `test_generation.py`? ★★★☆☆

---

## 47. Mocking

**Purpose:** The most technically interesting testing detail in the repo — patch-location correctness.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. `test_retrieval.py` patches `app.retrieval.retrieval_service.search_dense`, not `app.retrieval.dense_search.search_dense`. Why does the patch target have to be where the name is *used*, not where it's *defined*? (`test_retrieval.py:16-18`) ★★★★★
2. If you patched `app.retrieval.dense_search.search_dense` instead in that same test, would it fail, silently do nothing, or pass for the wrong reason? Explain exactly what happens under the hood. ★★★★★
3. `test_api.py` patches at the *controller* layer (`app.api.documents.ingest_document`, `app.api.retrieval.search`) while `test_retrieval.py` patches at the *service* layer (`search_dense`, `search_bm25`, `reranker_client`). Why the different patch depths between these two test files? (`test_api.py:16,43`, `test_retrieval.py:16-53`) ★★★★★
4. `test_search_hybrid_mode` patches four things at once (`mock_dense, mock_bm25, mock_fetch, mock_reranker`). Why mock `reranker_client` as a whole object rather than just its `.rerank()` method? (`test_retrieval.py:43-47`) ★★★☆☆
5. None of these tests touch a real Pinecone index, Supabase table, or NVIDIA API. What's the risk of a fully-mocked test suite — could all these tests pass while the real integration is completely broken? ★★★★★

---

## 48. CI/CD

**Purpose:** Explicitly absent — probe awareness of the gap.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Easy → Medium
**Interview Frequency:** ★★★☆☆

1. The CHANGELOG states "No CI/CD — tests are run manually with pytest." What's the risk of that, concretely, for this repo's Render auto-deploy setup? ★★★★☆
2. If you had to add one GitHub Actions workflow right now, what would it run, and at what trigger (push, PR, merge to main)? ★★★★☆
3. Render deploys straight from a git push per the earlier deployment history in this project. What's the danger of auto-deploying without a test gate in front of it? ★★★★☆

---

## 49. Debugging

**Purpose:** Live investigation reasoning, not memorized answers.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. **Search quality drops after a new document is uploaded.** Where do you start looking — chunking, embedding, or the reranker? What would you check first in the Retrieval Inspector? ★★★★★
2. **Wrong citations appear on an otherwise-correct answer.** Given citations come from retrieved chunks, not answer-text parsing (§37), what's the most likely cause — a bad chunk boundary, an overlap duplicate, or a reranker misfire? ★★★★★
3. **Users receive empty answers (`NO_ANSWER_MESSAGE`) for questions that should be answerable.** Walk your investigation: is it a chunking gap, an embedding mismatch, or a chunk that scored below what the reranker's `top_k` cutoff kept? ★★★★★
4. **The embedding service starts timing out intermittently.** `embedder.py` has a 30s timeout with no retry logic. What's the user-facing symptom, and what status code do they see? (`embedder.py:33-37`, `chat.py:29-31`) ★★★★☆
5. **Pinecone has an outage.** Trace the failure from `_get_index()` through to the HTTP response the Streamlit user sees. (`vector_store.py:44-49`, `retrieval.py:31-33`) ★★★★★
6. **A large PDF upload fails.** Is it more likely to fail at `validate_upload` (size check), `parse_pdf` (PyMuPDF memory), or `index_chunks` (batch upsert)? How would you narrow it down with logs alone? ★★★★☆
7. **The container crashes shortly after start on Render.** Given the Dockerfile backgrounds uvicorn with `&`, what's a plausible failure mode where the container appears "up" but is actually broken? ★★★★★
8. **Memory grows steadily over hours of uptime.** `search_bm25()` rebuilds tokenized docs and counters from scratch on every call rather than caching — is that a leak, or just wasted CPU? Where would you actually look for a real leak in this codebase? ★★★☆☆
9. **Retrieval is fine but the whole `/api/chat` response is slow.** Given the LLM has a 90s timeout, how do you tell from logs alone whether the slowness is retrieval-side or generation-side? ★★★★☆
10. **A request times out with no error logged.** What single Streamlit-side timeout value would you check first, and why? (`streamlit_app.py:205-209`) ★★★☆☆

---

## 50. Failure Scenarios

**Purpose:** Systemic failure reasoning across service boundaries.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★☆

1. Supabase and Pinecone are never written to inside a single transaction. Construct a realistic sequence of events that leaves them out of sync, beyond the one already described in `ingestion_service.py`'s comment. ★★★★★
2. What happens if `save_document()` succeeds but `save_chunks()` fails midway through a large batch — is `document_chunks` left with a partial set of rows for that document, and what does that do to BM25 and dashboard chunk counts? (`document_repository.py:23-49`) ★★★★☆
3. If the NVIDIA reranker API changes its response schema (e.g. renames `logit` to `score`), where does this code break, and how loudly? (`reranker.py:38`) ★★★☆☆
4. What happens if two users upload the same document simultaneously — any duplicate detection? ★★★☆☆

---

## 51. Production Readiness

**Purpose:** Direct confrontation with the CHANGELOG's own "Known Limitations" section.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★★

1. The CHANGELOG lists five known limitations. Pick the one you'd fix first before letting a real HR team use this, and justify the ordering. ★★★★★
2. What would "delete a document" actually require touching — Pinecone vectors, Supabase rows, or both? Sketch the endpoint. ★★★★☆
3. Is this system currently safe to point at documents containing PII (SSNs, salaries, medical info)? What's missing, specifically? ★★★★★
4. If you had one week to harden this for a pilot with 50 real users, what's your priority list? ★★★★☆

---

## 52. Monitoring

**Purpose:** Observability gaps.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. There's no metrics/tracing library anywhere in `requirements.txt`. If a query is slow, how would you find out *which stage* was slow right now, with only the existing `logging_config.py`? ★★★★☆
2. What would you add first — structured logging (JSON), a request-ID, or an APM tool — and why that order for this specific codebase's size? ★★★☆☆
3. `/health` just returns a static `{"status": "healthy"}` (`health.py:8-11`) — it doesn't actually check Pinecone, Supabase, or NVIDIA connectivity. Is that a real gap for a Render health check? ★★★★☆

---

## 53. Code Review

**Purpose:** Direct code-review-style challenges to real lines.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★☆

1. Why is this class (`NVIDIALLMClient`) responsible for both building the HTTP request *and* parsing the response, instead of splitting those? Is that a smell here, or fine at this size? ★★★☆☆
2. Why was the `_hydrate()` abstraction introduced for semantic/keyword mode but not reused in hybrid mode (§26.3)? Would you push back on that in review? ★★★★☆
3. Why is `DocumentRepositoryError` required as a dependency of `retrieval_service.py`, `generation_service.py`, and every API router — is that appropriate coupling, or should storage errors be translated earlier? ★★★☆☆
4. Why does `_search_hybrid` duplicate the "drop missing chunk_ids" filtering logic that `_hydrate` already does (§26.3)? What would you say in a PR comment about this? ★★★★☆
5. Why this threshold — the 70/40 split for confidence chips in the Streamlit UI (`streamlit_app.py:186-191`)? Would you request a change to tie it directly to the backend calibration constants? ★★★☆☆
6. Why this default — `top_k: int = 8` duplicated in both `schemas.py` and `streamlit_app.py`? Would you flag that as a DRY violation in review? ★★★★☆

---

## 54. Refactoring

**Purpose:** Concrete "what would you change" prompts.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. If asked to refactor the three NVIDIA client classes into one, what would the shared base class's interface look like? What would each subclass still need to override? ★★★★☆
2. Refactor `_search_hybrid` and `_hydrate` to share the missing-chunk-id filtering logic without changing behavior. ★★★★☆
3. The confidence calibration dict (`_CONFIDENCE_CALIBRATION`) is hardcoded in `generation_service.py`. Would you move it to `Settings`? Why or why not? ★★★☆☆

---

## 55. Tradeoffs

**Purpose:** Cross-cutting tradeoff synthesis.
**Expected Fresher Depth:** Must Know
**Difficulty:** Medium → Hard
**Interview Frequency:** ★★★★★

1. Hand-rolled BM25 vs. a library: what did you gain, what did you give up? ★★★★★
2. Storing chunk text in both Supabase and (implicitly, via re-fetch) nowhere in Pinecone metadata — single source of truth vs. two systems that can drift. Which would you pick again, knowing what you know now? ★★★★☆
3. Two containers colocated in one Dockerfile process (`&`) vs. two separate services. What did colocating save you, and what did it cost in reliability? ★★★★★
4. Confidence as informational-only vs. confidence as a gate that blocks low-quality answers. Which is safer for an HR use case? ★★★★☆

---

## 56. Future Improvements

**Purpose:** Forward-looking design instinct.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. What's the single highest-leverage improvement you'd make to retrieval quality specifically? ★★★★☆
2. If you had to add authentication, would you do it at the FastAPI layer, an API gateway, or Render's own access control? ★★★☆☆
3. Would you replace the hand-rolled BM25 with a persisted inverted index (e.g. via Postgres full-text search in Supabase, since it's already there) before scaling document count? ★★★★☆

---

## 57. Cost Optimization

**Purpose:** Awareness of what actually costs money in this architecture.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. Which parts of a single `/api/chat` request cost money (external API calls), and which are free (BM25, RRF)? ★★★★★
2. `CANDIDATE_MULTIPLIER = 4` directly multiplies reranker payload size and therefore reranker cost. If reranker cost became a concern, what's the cheapest lever to pull without hurting quality much? ★★★★☆
3. Every ingested chunk gets one embedding API call in a single batched request (`embedder.embed([chunk.text for chunk in chunks])`, `ingestion_service.py:59`). Is batching here actually reducing API cost, or just reducing round-trips? ★★★☆☆

---

## 58. Real-world Deployment

**Purpose:** Consulting-firm-flavored deployment scenarios.
**Expected Fresher Depth:** Good to Know
**Difficulty:** Medium
**Interview Frequency:** ★★★☆☆

1. How would a bank's HR department's requirements differ from this demo's — think document sensitivity and audit trail. ★★★★☆
2. How would an insurance company use a tool like this for policy documents, and what would need to change about the citation format for their compliance team? ★★★☆☆
3. How would you deploy this for a client with strict data-residency requirements (documents can't leave a specific region)? What in this stack (NVIDIA NIM, Pinecone, Supabase) would you need to check for regional hosting? ★★★☆☆

---

## 59. Ownership Verification

**Purpose:** The core anti-cheating category — see Top 25 below for the sharpest cuts.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. What problem forced you to add the `input_type` parameter to `embed()` — did you discover it, or was it there from a tutorial? (`embedder.py:18-23`) ★★★★★
2. The 70B vs 8B model comment is very specific about an observed failure mode. Describe the actual failing query you tested that led to that comment. (`settings.py:41-46`) ★★★★★
3. Why does the Dockerfile bind uvicorn to `127.0.0.1` — walk me through the exact incident that caused you to change it from `0.0.0.0`. (recall: earlier deploy history shows this was a live debugging session) ★★★★★
4. The confidence calibration values are explicitly "not derived analytically." Show me — right now — how you'd recalibrate `spread` for semantic mode if confidence scores started clustering near 100% for mediocre matches. ★★★★★
5. What would you redesign today, now that the system has been live? Be specific about one thing you'd genuinely do differently. ★★★★☆

---

## 60. Resume Verification

**Purpose:** Final gate — does the resume claim match the depth just demonstrated.
**Expected Fresher Depth:** Must Know
**Difficulty:** Hard
**Interview Frequency:** ★★★★★

1. If your resume says "built a hybrid RAG system with RRF and reranking," defend every one of those three terms using this repo's actual code, not textbook definitions. ★★★★★
2. If your resume claims "production deployment," reconcile that claim with the CHANGELOG's own "Known Limitations" section — no auth, no CI/CD, no pagination. ★★★★★
3. What percentage of this repo's design decisions could you defend cold, without looking at the code right now? ★★★★☆

---

# FINAL STUDY PRIORITIES

## Top 50 Most Likely Interview Questions

1. Walk me through this project in two minutes — what does it do, end to end?
2. What are the four pipeline stages this system runs on document upload?
3. What are the three search modes, and what's actually different between them under the hood?
4. Why does the system refuse to answer instead of guessing when a document doesn't contain the answer?
5. What does `@lru_cache` do on `get_settings()`, `_get_index()`, and `_get_client()`?
6. What's the point of custom exception classes like `EmbeddingError`, `VectorStoreError`, `RerankError`, `LLMError`?
7. Walk through what happens, line by line, when a POST hits `/api/chat`.
8. Why is `/api/chat` a separate endpoint from `/api/retrieval/search`?
9. `POST /api/documents/upload` returns 400 vs 422 for different failures — why?
10. Walk through how `_ENV_FILE` is resolved in `settings.py`.
11. What happens at runtime if `nvidia_llm_api_key` is left as `""` and a chat request comes in?
12. Compare `.env.example`, `docker-compose.yml`, and `render.yaml` for env var handling — why three mechanisms?
13. `CORS_ORIGINS` defaults to `["*"]` — what's the actual risk here?
14. Every API layer uses `logger.exception(...)` — what does that capture that `logger.error` wouldn't?
15. What happens today if Supabase's `save_document()` succeeds but `save_chunks()` fails?
16. Why is the try/except at the API layer instead of inside the service functions?
17. `validate_upload()` checks content-type from the client — can that be spoofed?
18. `Citation` only exposes `filename` and `page_number` — why hide chunk_id and score?
19. Why `RecursiveCharacterTextSplitter` specifically?
20. `CHUNK_SIZE = 500` — why 500 and not 300 or 1000?
21. `CHUNK_OVERLAP = 50` — walk through a concrete sentence that straddles a chunk boundary.
22. Why does `embed()` need an `input_type` param — what breaks if you always pass "passage"?
23. Walk through `index_chunks()` — why batch upserts at 100?
24. Why store chunk metadata in both Pinecone AND Supabase — isn't that duplication?
25. Why Pinecone specifically? Why not pgvector, given Supabase is already Postgres?
26. Why write BM25 by hand instead of using a library?
27. Explain the BM25 formula term by term — what do `idf`, `freq`, `norm` represent?
28. `search_bm25()` recomputes over the full corpus on every request — what's the performance ceiling?
29. What specific weakness of dense-only search does BM25 cover, and vice versa?
30. Explain RRF's formula — why rank instead of raw scores?
31. Why `RRF_K = 60`?
32. `CANDIDATE_MULTIPLIER = 4` — why 4?
33. Walk through `rerank()` — why does it return `index` instead of chunk_id, and what would happen if the passage list and chunk_id list got out of sync?
34. Walk through every rule in `SYSTEM_INSTRUCTIONS` and what failure mode each defends against.
35. What is "grounding" concretely — point to the exact enforcing code.
36. Two mechanisms prevent hallucination here — explain both and why you need both.
37. `_build_citations()` builds from retrieved chunks, not the LLM's answer text — what does that imply?
38. Walk through `_estimate_confidence()` end to end.
39. Why does each search mode need its own calibration constants?
40. Why use only the top chunk's score for confidence, not an average?
41. Confidence "does not gate whether the LLM is called" — why not use it to skip the LLM and save cost?
42. Why 70B instead of 8B for generation — what specific failure mode was observed?
43. `test_ingestion.py` covers "the only pure logic in the ingestion pipeline" — what does that imply isn't tested?
44. Why does `test_retrieval.py` patch `app.retrieval.retrieval_service.search_dense` and not `app.retrieval.dense_search.search_dense`?
45. Why do `test_api.py` and `test_retrieval.py` patch at different layers?
46. `render.yaml`'s startCommand binds uvicorn to `0.0.0.0` but the Dockerfile binds to `127.0.0.1` — which one actually runs, and is that a bug?
47. Walk through the Dockerfile's `CMD` — why background uvicorn with `&` instead of two containers?
48. Debugging: users receive empty `NO_ANSWER_MESSAGE` for answerable questions — where do you look first?
49. There's no authentication anywhere — what's the blast radius if deployed with real employee data?
50. What would you redesign today, now that the system has been live?

## Top 25 Ownership Questions

1. What problem forced you to add the `input_type` parameter to `embed()`?
2. Describe the actual failing query that led to the 70B-vs-8B model comment in `settings.py`.
3. Walk me through the exact incident behind binding uvicorn to `127.0.0.1` in the Dockerfile.
4. Show me, right now, how you'd recalibrate the confidence `spread` for a search mode if it started misbehaving.
5. `CANDIDATE_MULTIPLIER = 4` — how did you actually determine this, not what does the comment say?
6. Why is `RRF_K = 60` — is that the textbook default you copied, or did you tune it against this corpus?
7. Explain the exact bug that would occur if the reranker's `passages` list and `fused_chunk_ids` list ever desynced — has that ever actually happened to you?
8. What's the real reason Pinecone is written before Supabase in `ingest_document()` — trace the failure case that reasoning protects against, and the one it doesn't.
9. Why does `chunk_id` combine `document_id` and `chunk_index` with a hyphen — what would break if a `document_id` itself ever contained a hyphen? Did you consider that?
10. Walk through what you observed in the Retrieval Inspector that told you hybrid mode was working correctly the first time.
11. Why does the Streamlit frontend duplicate `DEFAULT_TOP_K = 8` instead of fetching it from the backend — was this a deliberate choice or an oversight you're seeing for the first time?
12. What's the actual reason `_hydrate()` isn't reused inside `_search_hybrid` — time pressure, or a real technical constraint?
13. Why does `validate_upload` trust `content_type` from the client rather than sniffing file magic bytes — did you consider the spoofing risk, and reject a fix, or not think about it?
14. `render.yaml` and `Dockerfile` disagree on the host binding — which one is actually live on Render right now, and how would you check?
15. What would you change about the BM25 implementation if a real user reported irrelevant keyword-search results tomorrow?
16. Why does the LLM get `temperature=0.2` instead of `0` — what did you observe at `0` that changed your mind, if anything?
17. What's the single most surprising thing you learned building the confidence calibration numbers?
18. If I removed the reranker call from hybrid mode right now, what would you predict happens to answer quality — and why do you believe that, specifically?
19. Why is there no test for `_estimate_confidence()` — was that a conscious tradeoff or a gap you're noticing now?
20. Walk through what actually happens if two documents are uploaded with the exact same filename.
21. What made you choose `page_number or 0` as the Pinecone metadata sentinel instead of `None` or `-1`?
22. Why does `SYSTEM_INSTRUCTIONS` explicitly address "conflicting information across documents" — what real scenario prompted that specific rule?
23. Explain, without looking, what `fitz` actually is and why PyMuPDF was chosen over alternatives.
24. If your Pinecone index were deleted right now, what's your actual recovery plan given Supabase still has the chunk text?
25. What's one part of this system you now think is over-engineered, and one part you think is under-engineered?

## Top 10 Make-or-Break Questions

1. Walk through `_estimate_confidence()` end to end, including why each search mode needs separate calibration constants.
2. Why does `test_retrieval.py` patch `app.retrieval.retrieval_service.search_dense` rather than `app.retrieval.dense_search.search_dense` — and what would happen if you patched the wrong one?
3. `render.yaml` binds uvicorn to `0.0.0.0` while the Dockerfile binds to `127.0.0.1` — which one is actually live, and why does that discrepancy exist?
4. Explain the BM25 formula term by term, and justify `BM25_K1 = 1.5` / `BM25_B = 0.75`.
5. What happens today if Supabase's `save_document()` succeeds but `save_chunks()` fails — and how would you fix it without a full transaction system?
6. Why 70B instead of 8B for the LLM — describe the specific failure mode observed, and how you'd verify that claim if I doubted it.
7. Two mechanisms prevent hallucination in this system — name both, explain why you need both, and which one is actually load-bearing.
8. Trace a hybrid-mode query end to end, including exactly how many network calls it makes and where each one can fail.
9. There's no authentication anywhere in this system — what's the honest answer about whether this is "production ready," reconciled against the resume claim?
10. What would you redesign today, and why — give one concrete answer, not a general "I'd add more tests."
