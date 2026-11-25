"""Streamlit interface: search, answer and show sources."""
import os

import streamlit as st

from ragdemo.answer import answer
from ragdemo.llm import BACKENDS, make_generate
from ragdemo.retrieve import Retriever

st.title("UK health guidance search")
st.caption("Demo on public guidance. Not medical advice.")

default_backend = os.environ.get("LLM_BACKEND", "ollama").lower()
backend = st.sidebar.selectbox(
    "LLM backend",
    BACKENDS,
    index=BACKENDS.index(default_backend) if default_backend in BACKENDS else 0,
    help="ollama runs locally. openrouter and hf send the question and passages to a third party.",
)


@st.cache_resource
def get_retriever() -> Retriever:
    return Retriever()


question = st.text_input("Ask a question about the guidance")
if question:
    hits = get_retriever().search(question, k=3)
    st.subheader("Answer")
    try:
        cap = 1500 if backend == "openrouter" else 400  # OpenRouter reasoning tokens count towards the cap; all 24 checked replies finished at 1500
        st.write(answer(question, hits, make_generate(backend, max_tokens=cap)))
    except Exception as exc:  # noqa: BLE001 - show any backend failure in the UI
        st.error(f"Could not get an answer from the LLM: {exc}")
    st.subheader("Sources")
    for i, h in enumerate(hits, start=1):
        with st.expander(f"[{i}] {h['source']} (score {h['score']:.2f})"):
            st.write(h["text"])
