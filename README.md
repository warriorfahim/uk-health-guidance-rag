# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Done: the baseline retrieval run, chunk sizes of 100, 150 and 400 words, a second embedding model (bge-small-en-v1.5), a chunk-level check on 21 hand-marked questions, and manual answer checks (Ollama and OpenRouter on the baseline, plus Ollama on bge-retrieved chunks). The app still uses `all-MiniLM-L6-v2`; bge was only an experiment. Not done: marking the other 30 questions for the chunk-level check, and choosing a default embedding model.

## What it does
1. Downloads public GOV.UK guidance pages as plain text (optional helper), then splits them into overlapping chunks.
2. Embeds the chunks with an open-source sentence-transformers model and stores them in a FAISS index.
3. Retrieves the top-k chunks for a query (semantic search).
4. Builds a prompt that asks an LLM to answer using only the retrieved text and to cite its sources. The Streamlit app sends it to a local Ollama model by default (`qwen2.5:7b`), or to OpenRouter if you pick it (see "Connecting an LLM"). A Hugging Face backend is still in the code but is not supported.
5. Evaluates retrieval on a hand-written question set (hit rate at k).
6. Runs a chunk-level check: for questions where a short answer phrase was copied by hand from the page, it tests whether the chunk containing that phrase is in the top k.
7. Runs a manual answer check: a sample of questions goes through retrieval and the LLM, and a report is written for you to mark by hand.

## Project layout
```
src/ragdemo/   fetch, chunking, ingest, index, retrieve, answer, llm, evaluate, chunk_check, answer_check
app.py         Streamlit interface
tests/         unit tests (run in CI, no model downloads needed)
data/raw/      cleaned .txt guidance pages (not committed; `fetch` can create these)
eval/          eval_questions.csv (question, expected_source), out_of_scope_questions.csv (question, note) and answer_spans.csv (hand-written answer phrases for the chunk-level check)
results/       saved output of real runs: page-level retrieval (baseline, chunk sizes, bge), chunk-level checks, token-length check and answer-check reports
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
python -m ragdemo.chunk_check       # is the chunk holding the answer in the top k? (uses eval/answer_spans.csv)
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
`eval/eval_questions.csv` holds 51 hand-written questions, each with the expected source file (all 32 pages have at least one). Raw page-level output: `results/retrieval_baseline.txt`, `results/retrieval_chunk100.txt`, `results/retrieval_chunk150.txt`, `results/retrieval_chunk400.txt` and `results/retrieval_bge_small.txt`. Answers from two LLMs were also spot-checked by hand on 12 questions each, and the local model was re-run with bge-retrieved chunks (`results/answer_check_ollama_bge.md`); see `docs/evaluation.md`.

| Setup | Chunk size (words) | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|-----------------|-------|-------|-------|
| Baseline | 200 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Smaller chunks | 100 | all-MiniLM-L6-v2 | 0.92 | 0.98 | 1.00 |
| Smaller chunks | 150 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Larger chunks | 400 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Different model | 200 | bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 |

Overlap was 20% of the chunk size in every run (40, 20, 30 and 80 words). With 51 questions, one question is about 0.02, so the gains over the baseline are one or two questions and could be noise. The baseline's 200-word chunks are often longer than the embedding model's 256-token input limit (55% of them); the 100- and 150-word chunks almost all fit. The 400-word chunks are mostly cut off by that limit (93% are over it) yet scored as well as the best smaller setup, so page-level Hit@k does not show the cost of truncation, and it is not comparable across chunk sizes because the top 5 cover more text when chunks are larger. See `docs/evaluation.md`.

**Chunk-level check.** `python -m ragdemo.chunk_check` asks a stricter question: is the chunk that contains the answer in the top k? It uses a short phrase I copied by hand from the answering sentence for 21 of the 51 questions (`eval/answer_spans.csv`), so it covers fewer questions than the table above and the two are not comparable. Raw output: `results/chunk_check_baseline.txt`, `results/chunk_check_chunk100.txt`, `results/chunk_check_chunk150.txt` and `results/chunk_check_chunk400.txt`.

| Chunk size (words) | Chunks | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 |
|--------------------|--------|-------------|-------------|-------------|
| 100 | 651 | 0.43 | 0.71 | 0.86 |
| 150 | 436 | 0.57 | 0.71 | 0.86 |
| 200 (baseline) | 330 | 0.62 | 0.81 | 0.90 |
| 400 | 169 | 0.71 | 0.86 | 0.95 |

Same embedding model and 20% overlap throughout. One question is about 0.05 here, so the gaps are a few questions. The ranking at the small end is the reverse of page-level Hit@k: 100 and 150 words were slightly ahead of the baseline there and are behind it here. The measles-risk question (answer in chunk 0) was missed at every chunk size, and 400 words missed only that one. Larger chunks are an easier target and the top 5 cover more text, so this is still not a fully fair comparison.

**Second embedding model.** `BAAI/bge-small-en-v1.5` (33.4M parameters, 384-dimensional, 512-token input limit, run without its optional query prefix) on the same 330 baseline chunks, none of which exceed its limit. Raw output: `results/retrieval_bge_small.txt` and `results/chunk_check_bge_small.txt`.

| Embedding model | Hit@1 | Hit@3 | Hit@5 | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 |
|-----------------|-------|-------|-------|-------------|-------------|-------------|
| all-MiniLM-L6-v2 (baseline) | 0.90 | 0.98 | 0.98 | 0.62 | 0.81 | 0.90 |
| bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 | 0.62 | 0.86 | 0.95 |

Page-level Hit@k is on 51 questions, Chunk-Hit@k on the 21 hand-marked ones. bge missed no question at k=5 at page level, and the measles-risk chunk was found in its top 5 (it was not in MiniLM's top 5). Its one chunk-level miss was the tick-borne encephalitis milk question. The models differ in training and architecture as well as input length, so this does not show that truncation caused the baseline's misses.

The app and the Quick start still use `all-MiniLM-L6-v2`, set as the default in `ragdemo.index`. To repeat the bge rows (same chunks, separate index file so the baseline index is untouched):
```bash
python -m ragdemo.index --model BAAI/bge-small-en-v1.5 --index data/index_bge.faiss
python -m ragdemo.evaluate --model BAAI/bge-small-en-v1.5 --index data/index_bge.faiss
python -m ragdemo.chunk_check --model BAAI/bge-small-en-v1.5 --index data/index_bge.faiss
```
The original bge runs were made with a short script before these options existed; re-running with the options gave the same numbers. The `--model` and `--index` options are for these three commands only. The app and `answer_check` still use the default model and index.

## What I learned
- **Retrieval found the right page.** The baseline scored Hit@5 0.98 on 51 questions, and in a manual spot check both a local and a hosted LLM refused most out-of-scope questions clearly and did not invent facts. The local model blended flu and COVID guidance on one boundary question.
- **The main weakness is at chunk level.** For the measles-risk question the right page came back but not the chunk holding the answer, and Hit@k cannot see that. A chunk-level check on 21 hand-marked questions does see it: Chunk-Hit@5 was 0.90 at the baseline, and that question was missed at every chunk size I tried.
- **Chunk size.** 100, 150 and 400 words all scored about the same as the 200-word baseline on page-level Hit@k (within one or two questions), even though 93% of the 400-word chunks exceed the embedding model's 256-token limit. The chunk-level check separated them: larger chunks did better (Chunk-Hit@5 0.86 at 100 and 150 words, 0.90 at 200, 0.95 at 400). That is on only 21 questions and larger chunks are an easier target, so I would not pick 400 words from this alone.
- **Embedding model.** bge-small-en-v1.5 (512-token limit) scored higher than MiniLM at page level (Hit@1 0.98 against 0.90, no misses at k=5) and a little higher at chunk level (Chunk-Hit@5 0.95 against 0.90), and it found the measles-risk chunk. The two models differ in more than input length, so this does not show that truncation was the cause.
- **LLM answers.** The free OpenRouter model was more cautious but less dependable than local Ollama (one empty answer, two cut off). Re-running the same 12 questions with Ollama on bge-retrieved chunks, the measles-risk question was answered correctly and all 6 main-set answers were correct, against 4 of 6 before. The COVID booster question was still blended with flu guidance, and the scabies refusal falsely said the sources mention scabies testing. One run on 12 questions, so I read this as a sign, not proof.

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- Answer quality was judged by one person on 12 questions per model, with no scoring metric, so treat it as a spot check and not a benchmark.
- Only one other embedding model was tried (bge-small-en-v1.5), once, without its query prefix. Hit@k is page-level, and the chunk-level check covers only 21 of the 51 questions. I chose which 21 to mark, so they are not a random sample.- The OpenRouter run used a free preview model with a 400-token cap, and an earlier run of it hit rate limits (HTTP 429).
- This is a demo built on public data. It is not medical advice.

## How this was built
I built this project with Claude Code (Anthropic's AI coding assistant) helping with implementation: much of the code, the tests and the first drafts of the docs were written with it, and I reviewed the changes and ran everything myself. The parts that need human judgement were done by me:
- **The evaluation set.** I wrote `eval/eval_questions.csv` (51 questions) and `eval/out_of_scope_questions.csv` by hand, so they stay independent of the system being tested.
- **The answer-quality check.** I read every answer from the two LLMs and marked it by hand against the source pages (see `docs/evaluation.md`). I did the same for the later run with bge-retrieved chunks.
- **The results.** Every number in this README comes from a real run saved in `results/`. Nothing is estimated.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
