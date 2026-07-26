"""Streamlit frontend for HR Knowledge Hub.

Talks to the FastAPI backend over HTTP only — no direct database or vector
store access, and no business logic here beyond formatting responses.
"""

from __future__ import annotations

import os
from datetime import datetime

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
SEARCH_MODES = ["hybrid", "semantic", "keyword"]

st.set_page_config(page_title="HR Knowledge Hub", page_icon="📄", layout="wide")

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []
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


def _post_json(path: str, payload: dict) -> dict | None:
    """POST JSON to the backend and return the parsed response, or None on error."""
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=60)
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


def render_sidebar() -> str:
    """Render the sidebar (branding, backend health, nav) and return the selected page."""
    with st.sidebar:
        st.title("📄 HR Knowledge Hub")
        st.caption("AI-powered Internal HR Knowledge Assistant using Hybrid RAG")
        st.divider()

        st.subheader("Backend status")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.ok:
                st.success(f"Connected — {BACKEND_URL}")
            else:
                st.error(f"Backend returned {response.status_code}")
        except requests.RequestException:
            st.error(f"Cannot reach backend at {BACKEND_URL}")

        st.divider()
        return st.radio(
            "Navigate",
            ["Dashboard", "Upload Documents", "Search & Chat", "Retrieval Inspector"],
        )


def render_dashboard() -> None:
    """Show document/chunk/vector counts and the list of documents indexed this session."""
    st.header("Dashboard")
    st.caption("Reflects documents uploaded during this Streamlit session.")

    documents = st.session_state.uploaded_documents
    total_chunks = sum(doc["chunks_created"] for doc in documents)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", len(documents))
    col2.metric("Chunks", total_chunks)
    col3.metric("Vectors", total_chunks)  # one Pinecone vector per chunk
    col4.metric("Last Upload", documents[-1]["filename"] if documents else "—")

    st.subheader("Indexed Documents")
    if not documents:
        st.info("No documents indexed yet — upload one on the **Upload Documents** page.")
    else:
        st.dataframe(documents, use_container_width=True, hide_index=True)


def render_upload() -> None:
    """Upload a PDF or DOCX file and show the indexing result."""
    st.header("Upload Documents")
    st.caption("Supported formats: PDF, DOCX. Maximum size: 5 MB.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

    if uploaded_file and st.button("Upload & Index", type="primary"):
        with st.spinner("Parsing, chunking, embedding, and indexing..."):
            result = _post_file("/api/documents/upload", uploaded_file)

        if result:
            st.success(f"Indexed **{result['filename']}** in {result['processing_time_ms']} ms")
            col1, col2 = st.columns(2)
            col1.metric("Chunks created", result["chunks_created"])
            col2.metric("Status", result["status"])

            st.session_state.uploaded_documents.append(
                {
                    "filename": result["filename"],
                    "chunks_created": result["chunks_created"],
                    "processing_time_ms": result["processing_time_ms"],
                    "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )


def render_search() -> None:
    """Ask a question, run retrieval + grounded generation, and show the answer."""
    st.header("Search & Chat")

    query = st.text_input("Ask a question about the uploaded HR documents")
    col1, col2 = st.columns([2, 1])
    search_mode = col1.selectbox("Search mode", SEARCH_MODES)
    top_k = col2.number_input("Top K", min_value=1, max_value=20, value=5)

    if st.button("Ask", type="primary") and query:
        with st.spinner("Retrieving context and generating an answer..."):
            result = _post_json(
                "/api/chat",
                {"query": query, "top_k": top_k, "search_mode": search_mode, "debug": True},
            )
        if result:
            # /api/chat doesn't echo the query back, so store it alongside
            # the result to keep "Question" accurate across reruns.
            st.session_state.last_chat_result = {**result, "query": query}

    result = st.session_state.last_chat_result
    if not result:
        st.info("Ask a question above to see a grounded answer with citations.")
        return

    st.subheader("Question")
    st.write(result["query"])

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Confidence")
    st.progress(result["confidence"] / 100, text=f"{result['confidence']}%")

    st.subheader("Source Documents")
    if result["citations"]:
        st.dataframe(result["citations"], use_container_width=True, hide_index=True)
    else:
        st.info("No sources — the answer wasn't grounded in the uploaded documents.")


def render_inspector() -> None:
    """Show dense, BM25, RRF, and reranked results from the most recent search."""
    st.header("Retrieval Inspector")
    st.caption("Intermediate results from each stage of the hybrid retrieval pipeline.")

    result = st.session_state.last_chat_result
    debug = result.get("debug") if result else None

    if not debug:
        st.info("Run a search on the **Search & Chat** page first to see pipeline internals.")
        return

    st.write(f"Search mode: **{debug['search_mode']}**")

    st.subheader("Dense Search Results (Pinecone)")
    st.dataframe(debug["dense_results"] or [{"info": "not used in this search mode"}])

    st.subheader("Keyword Search Results (BM25)")
    st.dataframe(debug["bm25_results"] or [{"info": "not used in this search mode"}])

    st.subheader("RRF Fused Results")
    st.dataframe(debug["rrf_results"] or [{"info": "not used in this search mode"}])

    st.subheader("Reranked Results (NVIDIA Reranker)")
    st.dataframe(debug["reranked_results"] or [{"info": "not used in this search mode"}])


page = render_sidebar()

if page == "Dashboard":
    render_dashboard()
elif page == "Upload Documents":
    render_upload()
elif page == "Search & Chat":
    render_search()
elif page == "Retrieval Inspector":
    render_inspector()
