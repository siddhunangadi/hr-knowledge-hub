"""Streamlit frontend for HR Knowledge Hub.

Talks to the FastAPI backend over HTTP only — no direct database or vector
store access, and no business logic here beyond formatting responses.
"""

from __future__ import annotations

import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DEFAULT_SEARCH_MODE = "hybrid"
DEFAULT_TOP_K = 8

st.set_page_config(page_title="HR Knowledge Hub", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1080px;}
    h1, h2, h3 {font-weight: 600; letter-spacing: -0.01em;}
    [data-testid="stMetricValue"] {font-weight: 600; font-size: 1.75rem;}
    [data-testid="stMetricLabel"] {color: #6B7280;}
    div[data-testid="stStatusWidget"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}

    .status-row {display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem;}
    .status-dot {width: 8px; height: 8px; border-radius: 999px; flex-shrink: 0;}
    .status-dot.ok {background: #12B76A;}
    .status-dot.err {background: #F04438;}

    div[role="radiogroup"] {gap: 0.25rem; justify-content: center;}
    div[role="radiogroup"] label {
        border-radius: 8px; padding: 0.35rem 0.75rem; margin-right: 0.25rem;
    }

    .chip {display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.25rem 0.65rem;
           border-radius: 999px; font-size: 0.85rem; font-weight: 500;}
    .chip.high {background: #ECFDF3; color: #027A48;}
    .chip.medium {background: #FFFAEB; color: #B54708;}
    .chip.low {background: #FEF3F2; color: #B42318;}
    .answer-block {font-size: 1.02rem; line-height: 1.6;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "last_chat_result" not in st.session_state:
    st.session_state.last_chat_result = None


def _error_detail(exc: requests.RequestException) -> str:
    """Extract the FastAPI error detail from a failed request, falling back to the exception text."""
    if exc.response is not None:
        try:
            return exc.response.json().get("detail", exc.response.text)
        except ValueError:
            return exc.response.text
    return str(exc)


def _get_json(path: str) -> dict | list | None:
    """GET from the backend and return the parsed response, or None on error."""
    try:
        response = requests.get(f"{BACKEND_URL}{path}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Request to {path} failed: {_error_detail(exc)}")
        return None


def _post_json(path: str, payload: dict, timeout: int = 60) -> dict | None:
    """POST JSON to the backend and return the parsed response, or None on error."""
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Request to {path} failed: {_error_detail(exc)}")
        return None


def _post_file(path: str, file) -> dict | None:
    """POST an uploaded file to the backend and return the parsed response, or None on error."""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{BACKEND_URL}{path}", files=files, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Upload failed: {_error_detail(exc)}")
        return None


def _render_table(rows: list[dict], columns: dict[str, str], empty_message: str) -> None:
    """Render a list of dicts as a table with friendly column names, or a placeholder message."""
    if not rows:
        st.caption(empty_message)
        return
    renamed = [{columns.get(key, key): value for key, value in row.items()} for row in rows]
    st.dataframe(renamed, use_container_width=True, hide_index=True)


def render_topbar() -> str:
    """Render the topbar (branding, backend health, nav) and return the selected page."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        connected = response.ok
        label = "Connected" if connected else f"Backend returned {response.status_code}"
    except requests.RequestException:
        connected = False
        label = "Cannot reach backend"

    st.markdown(
        f'<div class="status-row" style="justify-content: flex-end;">'
        f'<span class="status-dot {"ok" if connected else "err"}"></span>{label}</div>'
        '<div style="text-align: center;">'
        '<h1 style="margin-bottom: 0;">HR Knowledge Hub</h1>'
        '<div style="color: #6B7280;">AI-powered internal HR assistant · Hybrid RAG</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        ["Dashboard", "Upload Documents", "Search & Chat", "Retrieval Inspector"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.divider()
    return page


def render_dashboard() -> None:
    """Show document/chunk/vector counts, fetched fresh from GET /api/documents."""
    st.header("Dashboard")

    documents = _get_json("/api/documents") or []

    st.metric("Documents", len(documents))

    st.divider()
    st.subheader("Indexed Documents")
    if not documents:
        st.caption("No documents indexed yet — upload one on the **Upload Documents** page.")
    else:
        _render_table(
            documents,
            columns={
                "document_id": "Document ID",
                "filename": "Filename",
                "chunks_created": "Chunks",
                "uploaded_at": "Uploaded At",
            },
            empty_message="",
        )


def render_upload() -> None:
    """Upload a PDF or DOCX file and show the indexing result."""
    st.header("Upload Documents")
    st.caption("Supported formats: PDF, DOCX · Maximum size: 5 MB")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

    if uploaded_file and st.button("Upload & Index", type="primary"):
        with st.spinner(f"Parsing, chunking, embedding, and indexing {uploaded_file.name}..."):
            result = _post_file("/api/documents/upload", uploaded_file)

        if result:
            st.success(
                f"Indexed **{result['filename']}** in {result['processing_time_ms']} ms — "
                "see the **Dashboard** for the updated document list."
            )
            col1, col2 = st.columns(2)
            col1.metric("Chunks Created", result["chunks_created"])
            col2.metric("Status", result["status"])


def _confidence_chip(confidence: int) -> str:
    """Return an inline HTML chip for a confidence score: high (green), medium (amber), low (red)."""
    if confidence >= 70:
        tier, label = "high", "High confidence"
    elif confidence >= 40:
        tier, label = "medium", "Medium confidence"
    else:
        tier, label = "low", "Low confidence"
    return f'<span class="chip {tier}">{label} · {confidence}%</span>'


def render_search() -> None:
    """Ask a question, run retrieval + grounded generation, and show the answer."""
    st.header("Search & Chat")

    query = st.text_input("Ask a question about the uploaded HR documents")

    if st.button("Ask", type="primary") and query:
        with st.spinner("Retrieving context and generating an answer..."):
            # Longer than the default POST timeout: the LLM call alone can
            # take up to 90s (see llm_client.py), on top of retrieval time.
            result = _post_json(
                "/api/chat",
                {"query": query, "top_k": DEFAULT_TOP_K, "search_mode": DEFAULT_SEARCH_MODE, "debug": True},
                timeout=120,
            )
        if result:
            # /api/chat doesn't echo the query back, so store it alongside
            # the result to keep "Question" accurate across reruns.
            st.session_state.last_chat_result = {**result, "query": query}

    result = st.session_state.last_chat_result
    if not result:
        st.caption("Ask a question above to see a grounded answer with citations.")
        return

    st.divider()

    st.caption(result["query"])
    st.markdown(f'<div class="answer-block">{result["answer"]}</div>', unsafe_allow_html=True)
    st.markdown(_confidence_chip(result["confidence"]), unsafe_allow_html=True)

    st.write("")
    st.subheader("Sources")
    _render_table(
        result["citations"],
        columns={"filename": "Filename", "page_number": "Page"},
        empty_message="No sources — the answer wasn't grounded in the uploaded documents.",
    )


def render_inspector() -> None:
    """Show dense, BM25, RRF, and reranked results from the most recent search."""
    st.header("Retrieval Inspector")
    st.caption("Intermediate results from each stage of the hybrid retrieval pipeline.")

    result = st.session_state.last_chat_result
    debug = result.get("debug") if result else None

    if not debug:
        st.caption("Run a search on the **Search & Chat** page first to see pipeline internals.")
        return

    st.caption(f"Search mode: **{debug['search_mode']}**")

    score_columns = {"chunk_id": "Chunk ID", "score": "Score"}
    not_used = "Not used in this search mode."

    dense_tab, bm25_tab, rrf_tab, reranked_tab = st.tabs(
        ["Dense (Pinecone)", "Keyword (BM25)", "Rank Fusion", "Reranker"]
    )
    with dense_tab:
        _render_table(debug["dense_results"], score_columns, not_used)
    with bm25_tab:
        _render_table(debug["bm25_results"], score_columns, not_used)
    with rrf_tab:
        _render_table(debug["rrf_results"], score_columns, not_used)
    with reranked_tab:
        _render_table(
            debug["reranked_results"], {"index": "Passage Index", "score": "Score"}, not_used
        )


page = render_topbar()

if page == "Dashboard":
    render_dashboard()
elif page == "Upload Documents":
    render_upload()
elif page == "Search & Chat":
    render_search()
elif page == "Retrieval Inspector":
    render_inspector()
