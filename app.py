"""Streamlit interface: search, answer and show sources."""
import streamlit as st

from ragdemo.answer import answer
from ragdemo.llm import make_hf_generate
from ragdemo.retrieve import Retriever

st.title("UK health guidance search")
st.caption("Demo on public guidance. Not medical advice.")


@st.cache_resource
def get_retriever() -> Retriever:
    return Retriever()


@st.cache_resource
def get_generate():
    """Hugging Face hosted model if HF_TOKEN is set, otherwise a stub that echoes the prompt."""
    try:
        return make_hf_generate()
    except RuntimeError:

        def stub(prompt: str) -> str:
            return "HF_TOKEN not set, so no LLM was called. Grounded prompt:\n\n" + prompt

        return stub


question = st.text_input("Ask a question about the guidance")
if question:
    hits = get_retriever().search(question, k=5)
    st.subheader("Answer")
    st.write(answer(question, hits, get_generate()))
    st.subheader("Sources")
    for i, h in enumerate(hits, start=1):
        with st.expander(f"[{i}] {h['source']} (score {h['score']:.2f})"):
            st.write(h["text"])
