"""Streamlit frontend for HR Knowledge Hub — Phase 1: backend health check only."""

import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="HR Knowledge Hub", page_icon="📄")
st.title("HR Knowledge Hub")
st.caption("AI-powered Internal HR Knowledge Assistant (Hybrid RAG)")

st.subheader("Backend Connectivity Check")

if st.button("Check backend health"):
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        response.raise_for_status()
        st.success("Backend is reachable")
        st.json(response.json())
    except requests.RequestException as exc:
        st.error(f"Could not reach backend at {BACKEND_URL}: {exc}")
