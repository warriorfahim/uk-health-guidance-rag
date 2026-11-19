# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. The baseline retrieval run and a manual answer check are done. The 400-word chunk and second-model rows of the evaluation table are not yet run.

## What it does
1. Downloads public GOV.UK guidance pages as plain text (optional helper), then splits them into overlapping chunks.
2. Embeds the chunks with an open-source sentence-transformers model and stores them in a FAISS index.
3. Retrieves the top-k chunks for a query (semantic search).
4. Builds a prompt that asks an LLM to answer using only the retrieved text and to cite its sources. The Streamlit app sends it to a local Ollama model by default (`qwen2.5:7b`), or to OpenRouter if you pick it (see "Connecting an LLM"). A Hugging Face backend is still in the code but is not supported.
5. Evaluates retrieval on a hand-written question set (hit rate at k).
6. Runs a manual answer check: a sample of questions goes through retrieval and the LLM, and a report is written for you to mark by hand.

## Project layout
```
src/ragdemo/   fetch, chunking, ingest, index, retrieve, answer, llm, evaluate, answer_check
app.py         Streamlit interface
tests/         unit tests (run in CI, no model downloads needed)
data/raw/      cleaned .txt guidance pages (not committed; `fetch` can create these)
eval/          eval_questions.csv (question, expected_source) and out_of_scope_questions.csv (question, note)
results/       saved output of real runs: retrieval baseline and answer-check reports
docs/          architecture.md and evaluation.md
.github/       CI workflow (tests and lint on every push)
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .

# 1. Get pages into data/raw/ (one .txt per page; the file name is the source id).
#    Either add your own, or download public GOV.UK pages with fetch (see below):
python -m ragdemo.fetch discover    # writes candidate paths to data/sources.txt
#    edit data/sources.txt: keep the pages you want, delete the rest
python -m ragdemo.fetch fetch       # writes data/raw/<slug>.txt and data/raw/manifest.csv
python -m ragdemo.ingest            # writes data/chunks.jsonl
python -m ragdemo.index             # writes data/index.faiss
python -m ragdemo.evaluate          # prints hit rate at k = 1, 3, 5
python -m ragdemo.evaluate --misses # also lists questions whose source was not in the top 5
python -m ragdemo.answer_check --out results/answer_check_ollama.md   # needs an LLM backend (see below)
streamlit run app.py
```

## Fetching data
`ragdemo.fetch` uses only the standard library and two free GOV.UK APIs (no key needed):
- `discover` searches the Search API (default: UK Health Security Agency `detailed_guide` pages) and writes candidate paths to `data/sources.txt`. Options: `--org`, `--doc-type` (repeatable), `--query`, `--count`, `--out`.
- `fetch` downloads each path left in `data/sources.txt` from the Content API, converts the HTML to plain text, and saves `data/raw/<slug>.txt` plus `data/raw/manifest.csv` (source, title, url, updated, licence). Options: `--sources`, `--raw-dir`.

Pages with fewer than 100 words (for example PDF-only or collection pages) and failed requests are skipped and listed at the end. Requests are throttled to stay well under the API rate limit. The manifest records the licence as OGL v3.0; check each page's own licence before relying on it.

## Connecting an LLM
`app.py` retrieves the top 3 chunks and sends one grounded prompt (replies capped at 400 tokens) to an LLM chosen by `LLM_BACKEND`:

**Local Ollama (default).** Runs `qwen2.5:7b` on your machine, so no data leaves it and there are no API costs.
```powershell
# install Ollama from ollama.com, then:
ollama pull qwen2.5:7b
streamlit run app.py
```
Override with `OLLAMA_MODEL` or `OLLAMA_URL` (default `http://localhost:11434`). Answers on CPU can take a while.

**Hugging Face Inference Providers (not supported).** The `hf` backend (`LLM_BACKEND=hf` with `HF_TOKEN`, default model `meta-llama/Llama-3.1-8B-Instruct`, override with `HF_MODEL`) is still in the code but is not used or maintained. It needs a paid Hugging Face subscription, and without one calls fail with HTTP 402 Payment Required. It was not part of the answer check.

**OpenRouter (optional).** `$env:LLM_BACKEND = "openrouter"` plus `$env:OPENROUTER_API_KEY = "sk-or-..."`; the model defaults to `baidu/ernie-5.5-flash-preview:free` (override with `OPENROUTER_MODEL`; check the current ID on openrouter.ai/models, as free preview models change). Free models can be rate limited (HTTP 429), and retrieved text is sent to OpenRouter and its model provider.

The app's sidebar has an "LLM backend" selector, so you can switch between Ollama, OpenRouter, Hugging Face (not supported) or none (grounded prompt only) without restarting; `LLM_BACKEND` sets the initial choice.

If no LLM is usable (Ollama not running, or `hf`/`openrouter` selected without its key), the app automatically falls back to showing the grounded prompt instead of an answer; `LLM_BACKEND=none` forces this. If a call to a working backend fails, the app shows the error. Retrieved sources are always listed. Retrieval evaluation (`ragdemo.evaluate`) does not use the LLM. Answer quality was checked by hand on a small sample (see `docs/evaluation.md`).

## Evaluation
`eval/eval_questions.csv` holds 51 hand-written questions, each with the expected source file (all 32 pages have at least one). Raw output: `results/retrieval_baseline.txt`, `results/retrieval_chunk100.txt` and `results/retrieval_chunk150.txt`. The 400-word and second-model setups have not been run yet. Answers from two LLMs were also spot-checked by hand on 12 questions each; see `docs/evaluation.md`.
Compare a few setups and record the results here.

| Setup | Chunk size (words) | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|-----------------|-------|-------|-------|
| Baseline | 200 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Smaller chunks | 100 | all-MiniLM-L6-v2 | 0.92 | 0.98 | 1.00 |
| Smaller chunks | 150 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Larger chunks | 400 | all-MiniLM-L6-v2 | not yet run | not yet run | not yet run |
| Different model | 200 | (second model) | not yet run | not yet run | not yet run |

Overlap was 20% of the chunk size in every run (40, 20 and 30 words). With 51 questions, one question is about 0.02, so the 100- and 150-word gains are one or two questions and could be noise. The baseline's 200-word chunks are often longer than the embedding model's 256-token input limit (55% of them); the 100- and 150-word chunks almost all fit. See `docs/evaluation.md`.

## What I learned
Retrieval worked well on this corpus (Hit@5 0.98 on 51 questions), and in a manual spot check both a local and a hosted LLM refused most out-of-scope questions clearly and did not invent facts, although the local model blended flu and COVID guidance on one boundary question. The main weakness is at chunk level: for one question the right page came back but not the chunk holding the answer, and Hit@k cannot see that. I would add a chunk-level check and then test chunk size and overlap on all 51 questions, rather than tuning on a single failure. The free OpenRouter model was more cautious but less dependable than local Ollama (one empty answer, two cut off).

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- Answer quality was judged by one person on 12 questions per model, with no scoring metric, so treat it as a spot check and not a benchmark.
- 400-word chunks and a second embedding model were not evaluated.
- The OpenRouter run used a free preview model with a 400-token cap, and an earlier run of it hit rate limits (HTTP 429).
- This is a demo built on public data. It is not medical advice.

## How this was built
I built this project with Claude Code (Anthropic's AI coding assistant) helping with implementation: much of the code, the tests and the first drafts of the docs were written with it, and I reviewed the changes and ran everything myself. The parts that need human judgement were done by me:
- **The evaluation set.** I wrote `eval/eval_questions.csv` (51 questions) and `eval/out_of_scope_questions.csv` by hand, so they stay independent of the system being tested.
- **The answer-quality check.** I read every answer from the two LLMs and marked it by hand against the source pages (see `docs/evaluation.md`).
- **The results.** Every number in this README comes from a real run saved in `results/`. Nothing is estimated.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
