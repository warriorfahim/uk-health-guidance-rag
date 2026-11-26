"""FastAPI service. Run with: uvicorn ragdemo.api:app"""
import logging
import os
import time
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from .llm import make_generate
from .retrieve import Retriever
from .service import ask

logger = logging.getLogger("uvicorn.error")


class AskRequest(BaseModel):
    question: str = Field(max_length=500)
    k: int = Field(default=3, ge=1, le=10)

    @field_validator("question")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value


class Source(BaseModel):
    ref: int
    source: str
    chunk_id: int
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str | None
    llm_used: bool
    sources: list[Source]


def default_generate():
    """LLM chosen by the server's LLM_BACKEND setting; callers of the API cannot change it."""
    backend = os.environ.get("LLM_BACKEND", "ollama").lower()
    return make_generate(backend, max_tokens=1500 if backend == "openrouter" else 400)


def create_app(retriever_factory=Retriever, generate_factory=default_generate) -> FastAPI:
    """Build the app. Tests pass fakes so that no model, index or LLM is needed."""
    app = FastAPI(title="UK health guidance RAG demo", description="Not medical advice.")
    get_retriever = lru_cache(maxsize=1)(retriever_factory)  # load once, on the first question

    @app.get("/health")
    def health() -> dict:
        """The process is up. This does not check the index or the LLM."""
        return {"status": "ok"}

    @app.post("/ask", response_model=AskResponse)
    def ask_question(request: AskRequest) -> dict:
        start = time.perf_counter()
        try:
            retriever = get_retriever()
        except Exception as exc:
            logger.exception("could not load the retriever")
            raise HTTPException(503, "Search index is not available") from exc
        try:
            result = ask(request.question, retriever, generate_factory(), k=request.k)
        except Exception as exc:
            logger.exception("could not answer")
            raise HTTPException(502, "Could not get an answer") from exc
        # The question text is deliberately not logged.
        logger.info("ask k=%d llm_used=%s seconds=%.2f",
                    request.k, result["llm_used"], time.perf_counter() - start)
        return result

    return app


app = create_app()
