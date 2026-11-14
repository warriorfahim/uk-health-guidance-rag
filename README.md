# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Fill in the evaluation table below once you have run the experiments.

## What it does
1. Downloads public GOV.UK guidance pages as plain text (optional helper), then splits them into overlapping chunks.
2. Embeds the chunks with an open-source sentence-transformers model and stores them in a FAISS index.
3. Retrieves the top-k chunks for a query (semantic search).
4. Builds a prompt that asks an LLM to answer using only the retrieved text and to cite its sources. The Streamlit app sends it to a model hosted by Hugging Face when `HF_TOKEN` is set.
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
`ragdemo.llm.make_hf_generate()` returns a `generate(prompt) -> str` function that calls a model hosted by Hugging Face (Inference Providers) through `huggingface_hub`. `app.py` uses it automatically when a token is set:
```powershell
$env:HF_TOKEN = "hf_..."          # free access token from huggingface.co/settings/tokens
$env:HF_MODEL = "Qwen/Qwen2.5-7B-Instruct"   # optional; this is the default
streamlit run app.py
```
Without `HF_TOKEN`, the app still runs and shows the grounded prompt instead of an answer. Free usage is rate limited, and which models are available can change; if the default fails, set `HF_MODEL` to another instruct model. Retrieved text is sent to Hugging Face's servers. Retrieval evaluation (`ragdemo.evaluate`) does not use the LLM, and answer quality is not yet evaluated.

## Evaluation
`eval/eval_questions.csv` holds 20 to 30 questions with the expected source file.
Compare a few setups and record the results here.

| Setup | Chunk size (words) | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|-----------------|-------|-------|-------|
| Baseline | 200 | all-MiniLM-L6-v2 | | | |
| Larger chunks | 400 | all-MiniLM-L6-v2 | | | |
| Different model | 200 | (second model) | | | |

## What I learned
(Add 3 to 5 sentences: what worked, what failed, what you would change.)

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- This is a demo built on public data. It is not medical advice.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
