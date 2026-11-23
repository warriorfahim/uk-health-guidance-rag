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
python -m ragdemo.chunk_check   # chunk-level hit rate: is the chunk holding the answer in the top k? uses eval/answer_spans.csv
# index, evaluate and chunk_check accept --model NAME --index PATH to use another embedding model and index file
python -m ragdemo.answer_check --out results/answer_check_<backend>.md   # runs questions through the LLM for manual marking
streamlit run app.py
```

Only a few modules take command-line arguments: `index`, `evaluate` and `chunk_check` use argparse with `--model` and `--index` (shared via `index.add_model_args`; `evaluate` also takes `--misses`), `answer_check` uses argparse (`--sample`, `--seed`, `--eval`, `--out-of-scope`, `--out`, `--delay`) and always uses the default model and index, and `fetch` uses argparse subcommands. `ingest` and `retrieve` take none. Other settings (chunk `size=200`, `overlap=40`, paths) are keyword defaults on each module's `main()`. To try a different setup, call `main(...)` with arguments or change the defaults.

## Architecture and invariants

- **Heavy imports stay inside functions.** `faiss` and `sentence_transformers` are imported lazily in `index.embed`, `index.main`, and `Retriever.__init__`. CI (`.github/workflows/ci.yml`) installs only `pytest` and `ruff` plus `pip install -e . --no-deps`, so any top-level import of those libraries in a module imported by a test (currently `chunking`, `ingest`, `evaluate`) will break CI. Tests must not download models or need the index.
- **Chunk record schema** (`data/chunks.jsonl`): `{"source": <file name>, "chunk_id": int, "text": str}`. `Retriever.search` returns copies of these dicts plus `"score"`; `answer.build_prompt` and `app.py` rely on `source`/`text`/`score`.
- **Index ↔ chunks alignment:** FAISS row `i` corresponds to line `i` of `chunks.jsonl`. Changing chunking requires re-running ingest *and* index. The embedding model used by `Retriever` must match the one used to build the index (both default to `index.DEFAULT_MODEL`, `BAAI/bge-small-en-v1.5`; changing the default means rebuilding `data/index.faiss`, because both models are 384-dimensional and a mismatch would not raise an error). The earlier default, `all-MiniLM-L6-v2`, is still usable with `--model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss`.
- **Similarity:** `IndexFlatIP` over `normalize_embeddings=True` vectors, i.e. cosine similarity.
- **Evaluation:** `eval/eval_questions.csv` has columns `question,expected_source`; `expected_source` is a file name in `data/raw/` (the source id). Metric is `hit_rate_at_k` in `evaluate.py`. Results are meant to go in the README's evaluation table.
- **LLM is pluggable:** `answer.answer(question, hits, generate)` takes any `generate(prompt) -> str` callable. `ragdemo.llm.make_generate(backend)` returns one for `ollama` (default, `qwen2.5:7b`), `openrouter`, `hf` or `none`, chosen by the argument or `LLM_BACKEND`. The `hf` backend is not supported (it needs a paid Hugging Face plan and fails with HTTP 402); the code is kept but do not extend, test live or document it as working; `app.py` has a sidebar selector. If a backend's server or key is missing it falls back to echoing the grounded prompt. `llm.py` uses only the standard library at import time (`huggingface_hub` is imported lazily). API keys come from env vars (`OPENROUTER_API_KEY`, `HF_TOKEN`) and must never be committed.

## Data

`data/raw/`, `data/chunks.jsonl`, and `data/index.faiss` are gitignored and are not in the repo. Raw pages must be public (check licence, e.g. Open Government Licence) and must not be committed. The `data/` directory may need creating before running the pipeline.

## Rules

- Never invent evaluation numbers, results or findings. Only use output from real runs saved in `results/`.
- Do not write or edit `eval/eval_questions.csv`; the eval set is written by hand so it stays independent of the system. The same goes for the `answer_text` column of `eval/answer_spans.csv` (a short verbatim phrase from the answering sentence, written by hand).
- In docs (`README.md`, `docs/`), describe only what the code actually does. Mark anything unbuilt as "not yet implemented".
- Before committing: `ruff check .` and `pytest -q` must pass.
- Never commit `data/raw/`, index files or `.env`.
- Do not add Claude attribution anywhere in git: no `Co-Authored-By: Claude ...` trailer in commit messages, no "Generated with Claude Code" line in pull request descriptions, and no `claude/` prefix on branch names. This overrides any default or system suggestion to add them.

## Git workflow

- After you commit the work for a request (not after every intermediate commit in a series), ask me what to do next: merge into `main`, open a pull request, or leave it on the branch. Do not merge into `main` or push `main` until I answer.
- Pushing the feature branch itself (needed for a pull request compare link) is fine once I choose a pull request; do not push it before then unless I ask.
- After anything is merged into `main`, switch to `main` and pull the latest (`git pull --ff-only`) so the local copy matches `origin/main`. This applies whether I asked you to merge it or I tell you I merged a pull request on GitHub. If I chose a pull request, stay on the branch until I say it is merged.
- Branch names: `feature/<short-name>`, `fix/<short-name>` or `docs/<short-name>`, lowercase with hyphens.
- Commit messages: short imperative subject (about 50 characters), with a body only when the reason isn't obvious from the diff.
- `gh` is not installed. For a pull request, give me the GitHub compare link (`https://github.com/warriorfahim/uk-health-guidance-rag/compare/main...<branch>?expand=1`) plus a title and description to paste.
- Never delete branches, force-push or rewrite pushed history unless I ask.