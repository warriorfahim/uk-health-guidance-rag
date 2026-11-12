"""Streamlit interface: search, answer and show sources."""
import streamlit as st

from ragdemo.answer import answer
from ragdemo.retrieve import Retriever

st.title("UK health guidance search")
st.caption("Demo on public guidance. Not medical advice.")


@st.cache_resource
def get_retriever() -> Retriever:
    return Retriever()


def generate(prompt: str) -> str:
    # TODO: plug in your LLM here (local open model or API). Until then, show the grounded prompt.
    return "LLM not connected yet. Grounded prompt that would be sent:\n\n" + prompt


question = st.text_input("Ask a question about the guidance")
if question:
    hits = get_retriever().search(question, k=5)
    st.subheader("Answer")
    st.write(answer(question, hits, generate))
    st.subheader("Sources")
    for i, h in enumerate(hits, start=1):
        with st.expander(f"[{i}] {h['source']} (score {h['score']:.2f})"):
            st.write(h["text"])
