# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Fill in the evaluation table below once you have run the experiments.

## What it does
1. Downloads public GOV.UK guidance pages as plain text (optional helper), then splits them into overlapping chunks.
2. Embeds the chunks with an open-source sentence-transformers model and stores them in a FAISS index.
3. Retrieves the top-k chunks for a query (semantic search).
4. Builds a prompt that asks an LLM to answer using only the retrieved text and to cite its sources. The Streamlit app sends it to a local Ollama model by default (`qwen2.5:7b`), or to OpenRouter or Hugging Face if you pick one of those (see "Connecting an LLM").
5. Evaluates retrieval on a hand-written question set (hit rate at k).

## Project layout
```
src/ragdemo/   fetch, chunking, ingest, index, retrieve, answer, llm, evaluate
app.py         Streamlit interface
tests/         unit tests (run in CI, no model downloads needed)
data/raw/      cleaned .txt guidance pages (not committed; `fetch` can create these)
eval/          eval_questions.csv: question, expected_source
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

**Hugging Face Inference Providers (optional).** `$env:LLM_BACKEND = "hf"` plus `$env:HF_TOKEN = "hf_..."`; the model defaults to `meta-llama/Llama-3.1-8B-Instruct` (override with `HF_MODEL`). This is a paid per-use service (the free allowance is small and calls can fail with 402 Payment Required), and retrieved text is sent to Hugging Face's servers.

**OpenRouter (optional).** `$env:LLM_BACKEND = "openrouter"` plus `$env:OPENROUTER_API_KEY = "sk-or-..."`; the model defaults to `baidu/ernie-5.5-flash-preview:free` (override with `OPENROUTER_MODEL`; check the current ID on openrouter.ai/models, as free preview models change). Free models can be rate limited (HTTP 429), and retrieved text is sent to OpenRouter and its model provider.

The app's sidebar has an "LLM backend" selector, so you can switch between Ollama and OpenRouter without restarting; `LLM_BACKEND` sets the initial choice.

If no LLM is usable (Ollama not running, or `hf`/`openrouter` selected without its key), the app automatically falls back to showing the grounded prompt instead of an answer; `LLM_BACKEND=none` forces this. If a call to a working backend fails, the app shows the error. Retrieved sources are always listed. Retrieval evaluation (`ragdemo.evaluate`) does not use the LLM. Answer quality was checked by hand on a small sample (see `docs/evaluation.md`).

## Evaluation
`eval/eval_questions.csv` holds 51 hand-written questions, each with the expected source file (all 32 pages have at least one). Raw output: `results/retrieval_baseline.txt`. Only the baseline has been run so far. Answers from two LLMs were also spot-checked by hand on 12 questions each; see `docs/evaluation.md`.
Compare a few setups and record the results here.

| Setup | Chunk size (words) | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|-----------------|-------|-------|-------|
| Baseline | 200 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Larger chunks | 400 | all-MiniLM-L6-v2 | | | |
| Different model | 200 | (second model) | | | |

## What I learned
Retrieval worked well on this corpus (Hit@5 0.98 on 51 questions), and in a manual spot check both a local and a hosted LLM refused out-of-scope questions instead of inventing facts. The main weakness is at chunk level: for one question the right page came back but not the chunk holding the answer, and Hit@k cannot see that. I would add a chunk-level check and then test chunk size and overlap on all 51 questions, rather than tuning on a single failure. The free OpenRouter model was more cautious but less dependable than local Ollama (one empty answer, two cut off).

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- Answer quality was judged by one person on 12 questions per model, with no scoring metric, so treat it as a spot check and not a benchmark.
- Larger chunks and a second embedding model were not evaluated.
- The OpenRouter run used a free preview model with a 400-token cap, and an earlier run of it hit rate limits (HTTP 429).
- This is a demo built on public data. It is not medical advice.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
