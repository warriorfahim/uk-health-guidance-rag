# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small semantic-search + RAG demo over public UK health guidance: `.txt` pages → word-based overlapping chunks → sentence-transformers embeddings in a FAISS index → top-k retrieval → grounded, cited LLM prompt. Package is `ragdemo` (src layout, `src/ragdemo/`), with a Streamlit UI in `app.py`. It is a demo on public data, not medical advice.

## Environment

- Python 3.12 (local 3.12.10; CI uses `"3.12"`; `.python-version` contains `3.12`).
- Use the virtual environment in `.venv/`. Do not suggest syntax or packages that need Python 3.13+.

## Commands

```bash
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .

ruff check .                                   # lint (line-length 100)
pytest -q                                      # all tests
pytest tests/test_chunking.py::test_chunks_overlap   # single test

# Pipeline (run from repo root; all paths are relative to CWD)
python -m ragdemo.ingest     # data/raw/*.txt -> data/chunks.jsonl
python -m ragdemo.index      # data/chunks.jsonl -> data/index.faiss
python -m ragdemo.evaluate   # prints Hit@1/3/5 using eval/eval_questions.csv
python -m ragdemo.evaluate --misses   # also lists questions whose source was not in the top 5
streamlit run app.py
```

The pipeline modules have no CLI argument parsing (apart from the single `--misses` flag on `evaluate`); settings (chunk `size=200`, `overlap=40`, model, paths) are keyword defaults on each module's `main()`. To try a different setup, call `main(...)` with arguments or change the defaults.

## Architecture and invariants

- **Heavy imports stay inside functions.** `faiss` and `sentence_transformers` are imported lazily in `index.embed`, `index.main`, and `Retriever.__init__`. CI (`.github/workflows/ci.yml`) installs only `pytest` and `ruff` plus `pip install -e . --no-deps`, so any top-level import of those libraries in a tested module (`chunking`, `ingest`, `evaluate`) will break CI. Tests must not download models or need the index.
- **Chunk record schema** (`data/chunks.jsonl`): `{"source": <file name>, "chunk_id": int, "text": str}`. `Retriever.search` returns copies of these dicts plus `"score"`; `answer.build_prompt` and `app.py` rely on `source`/`text`/`score`.
- **Index ↔ chunks alignment:** FAISS row `i` corresponds to line `i` of `chunks.jsonl`. Changing chunking requires re-running ingest *and* index. The embedding model used by `Retriever` must match the one used to build the index (both default to `index.DEFAULT_MODEL`, `all-MiniLM-L6-v2`).
- **Similarity:** `IndexFlatIP` over `normalize_embeddings=True` vectors, i.e. cosine similarity.
- **Evaluation:** `eval/eval_questions.csv` has columns `question,expected_source`; `expected_source` is a file name in `data/raw/` (the source id). Metric is `hit_rate_at_k` in `evaluate.py`. Results are meant to go in the README's evaluation table.
- **LLM is pluggable:** `answer.answer(question, hits, generate)` takes any `generate(prompt) -> str` callable. `ragdemo.llm.make_generate(backend)` returns one for `ollama` (default, `qwen2.5:7b`), `openrouter`, `hf` or `none`, chosen by the argument or `LLM_BACKEND`; `app.py` has a sidebar selector. If a backend's server or key is missing it falls back to echoing the grounded prompt. `llm.py` uses only the standard library at import time (`huggingface_hub` is imported lazily). API keys come from env vars (`OPENROUTER_API_KEY`, `HF_TOKEN`) and must never be committed.

## Data

`data/raw/`, `data/chunks.jsonl`, and `data/index.faiss` are gitignored and are not in the repo. Raw pages must be public (check licence, e.g. Open Government Licence) and must not be committed. The `data/` directory may need creating before running the pipeline.

## Rules

- Never invent evaluation numbers, results or findings. Only use output from real runs saved in `results/`.
- Do not write or edit `eval/eval_questions.csv`; the eval set is written by hand so it stays independent of the system.
- In docs (`README.md`, `docs/`), describe only what the code actually does. Mark anything unbuilt as "not yet implemented".
- Before committing: `ruff check .` and `pytest -q` must pass.
- Never commit `data/raw/`, index files or `.env`.