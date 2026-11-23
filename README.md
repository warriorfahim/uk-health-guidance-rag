# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Done: the baseline retrieval run, chunk sizes of 100, 150 and 400 words, a second embedding model (bge-small-en-v1.5, now the default), a chunk-level check with hand-marked answer phrases for all 51 questions, the chunk-size runs repeated on all 51 with both models, and manual answer checks (Ollama and OpenRouter on the MiniLM baseline, plus Ollama on bge-retrieved chunks). Not done: the LLM answer check with other chunk sizes, and overlap and query-prefix tests.

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
results/       saved output of real runs: page-level retrieval (baseline, chunk sizes, bge), chunk-level checks, token-length check, embedding timing and answer-check reports
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
`eval/eval_questions.csv` holds 51 hand-written questions, each with the expected source file (all 32 pages have at least one). Raw page-level output: `results/retrieval_baseline.txt`, `results/retrieval_chunk100.txt`, `results/retrieval_chunk150.txt`, `results/retrieval_chunk400.txt` (all MiniLM), and `results/retrieval_bge_small.txt`, `results/retrieval_chunk100_bge.txt`, `results/retrieval_chunk150_bge.txt` and `results/retrieval_chunk400_bge.txt` (bge). Answers from two LLMs were also spot-checked by hand on 12 questions each, and the local model was re-run with bge-retrieved chunks (`results/answer_check_ollama_bge.md`); see `docs/evaluation.md`.

| Setup | Chunk size (words) | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|-----------------|-------|-------|-------|
| Baseline | 200 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Smaller chunks | 100 | all-MiniLM-L6-v2 | 0.92 | 0.98 | 1.00 |
| Smaller chunks | 150 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Larger chunks | 400 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Different model | 200 | bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 |
| Different model, smaller chunks | 100 | bge-small-en-v1.5 | 0.98 | 0.98 | 1.00 |
| Different model, smaller chunks | 150 | bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 |
| Different model, larger chunks | 400 | bge-small-en-v1.5 | 1.00 | 1.00 | 1.00 |

Overlap was 20% of the chunk size in every run (40, 20, 30 and 80 words). With 51 questions, one question is about 0.02, so the MiniLM chunk-size gains over the baseline are one or two questions and could be noise (bge's Hit@1 gain over MiniLM at 200 words is 4 questions). The baseline's 200-word chunks are often longer than MiniLM's 256-token input limit (55% of them); the 100- and 150-word chunks almost all fit. The 400-word chunks are mostly cut off by that limit (93% are over it) yet scored as well as the best smaller MiniLM setup, so page-level Hit@k does not show the cost of truncation, and it is not comparable across chunk sizes because the top 5 cover more text when chunks are larger. See `docs/evaluation.md`.

**Chunk-level check.** `python -m ragdemo.chunk_check` asks a stricter question: is the chunk that contains the answer in the top k? It uses a short phrase copied by hand from the answering sentence for each question (`eval/answer_spans.csv`). The chunk-size runs in the next table (all-MiniLM-L6-v2) were made when only the first 21 questions had a phrase, so they cover 21 questions; later runs cover all 51. Raw output for the 21-question runs: `results/chunk_check_baseline.txt`, `results/chunk_check_chunk100.txt`, `results/chunk_check_chunk150.txt` and `results/chunk_check_chunk400.txt`.

| Chunk size (words) | Chunks | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 |
|--------------------|--------|-------------|-------------|-------------|
| 100 | 651 | 0.43 | 0.71 | 0.86 |
| 150 | 436 | 0.57 | 0.71 | 0.86 |
| 200 (baseline) | 330 | 0.62 | 0.81 | 0.90 |
| 400 | 169 | 0.71 | 0.86 | 0.95 |

Same embedding model and 20% overlap throughout. One question is about 0.05 here, so the gaps are a few questions. The ranking at the small end is the reverse of page-level Hit@k: 100 and 150 words were slightly ahead of the baseline there and are behind it here. The measles-risk question (answer in chunk 0) was missed at every chunk size, and 400 words missed only that one. Larger chunks are an easier target and the top 5 cover more text, so this is still not a fully fair comparison.

**Chunk size on all 51 questions.** The chunk-size runs were repeated once every question had an answer phrase, for both embedding models (raw output: `results/chunk_check_all51_chunk100_minilm.txt`, `..._bge.txt`, and the same for 150 and 400; the 200-word rows are `results/chunk_check_all51_minilm.txt` and `..._bge.txt`). Each cell is Chunk-Hit@1 / @3 / @5, with the number of questions missed at k=5 in brackets.

| Chunk size (words) | Chunks | all-MiniLM-L6-v2 | bge-small-en-v1.5 |
|--------------------|--------|------------------|-------------------|
| 100 | 651 | 0.47 / 0.78 / 0.88 (6) | 0.57 / 0.76 / 0.88 (6) |
| 150 | 436 | 0.61 / 0.80 / 0.88 (6) | 0.63 / 0.88 / 0.90 (5) |
| 200 | 330 | 0.69 / 0.88 / 0.92 (4) | 0.65 / 0.90 / 0.96 (2) |
| 400 | 169 | 0.78 / 0.92 / 0.96 (2) | 0.84 / 0.96 / 1.00 (0) |

Larger chunks did better for both models, matching the 21-question result above. bge was ahead of MiniLM at every k at 150 and 400 words, and mixed at 100 and 200 words, though several gaps are one or two questions. bge with 400-word chunks is the best retrieval setup I tried: no questions missed at k=5, and Hit@1 1.00 at page level. Two cautions. A larger chunk is an easier target and the top 5 cover more text (about 2,000 words at 400 words per chunk, against about 500 at 100). And I have not tested the LLM with 400-word chunks, so the default stays at 200 words; switching would be a separate decision that needs an answer check. I did not measure how many 400-word chunks exceed bge's 512-token limit.

**Second embedding model.** `BAAI/bge-small-en-v1.5` (33.4M parameters, 384-dimensional, 512-token input limit, run without its optional query prefix) on the same 330 baseline chunks, none of which exceed its limit. Raw output: `results/retrieval_bge_small.txt` and `results/chunk_check_bge_small.txt`.

| Embedding model | Hit@1 | Hit@3 | Hit@5 | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 |
|-----------------|-------|-------|-------|-------------|-------------|-------------|
| all-MiniLM-L6-v2 (baseline) | 0.90 | 0.98 | 0.98 | 0.62 | 0.81 | 0.90 |
| bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 | 0.62 | 0.86 | 0.95 |

The table above is on the 21 questions that had a phrase at the time. bge missed no question at k=5 at page level, and the measles-risk chunk was found in its top 5 (it was not in MiniLM's top 5).

Once all 51 questions had a phrase (`results/chunk_check_all51_bge.txt`, `results/chunk_check_all51_minilm.txt`), the chunk-level result was mixed:

| Embedding model (51 questions, 200-word chunks) | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 | Missed at k=5 |
|-------------------------------------------------|-------------|-------------|-------------|---------------|
| all-MiniLM-L6-v2 | 0.69 | 0.88 | 0.92 | 4 |
| bge-small-en-v1.5 | 0.65 | 0.90 | 0.96 | 2 |

MiniLM was ahead at k=1 by 2 questions, and bge was ahead at k=3 and k=5 by 1 and 2 questions. MiniLM missed the diphtheria "wait for lab confirmation" question, the measles-risk question, the MMRV chickenpox question and the invasive Aedes south-east England question. bge missed the diphtheria question and the tick-borne encephalitis milk question. These gaps are one or two questions, so they are within noise, and the models differ in training and architecture as well as input length, so this does not show that truncation caused MiniLM's misses.

**Default model.** On 2026-11-23 the default became `BAAI/bge-small-en-v1.5` (`ragdemo.index.DEFAULT_MODEL`), so the Quick start, the app and `answer_check` now use it. The reasons: at page level it was ahead, mainly at k=1 (Hit@1 0.98 against 0.90, 4 questions; 1 question at k=3 and k=5), at chunk level on all 51 questions it was mixed (behind by 2 questions at k=1, ahead by 1 at k=3, which is the k the app uses, and by 2 at k=5), it answered 6 of 6 main-set questions correctly in the 12-question answer check against 4 of 6, and it reads 512 tokens, so none of the 200-word chunks are cut off. The costs: indexing the 330 chunks took about 98 s against 36 s, and embedding a question about 44 ms against 26 ms (`results/embedding_timing.txt`, CPU, rough). The evidence is thin and not uniformly in bge's favour (the gaps are one to four questions, one answer-check run, no query prefix), so this is a judgement that the demo can reverse cheaply, not a proven result. The chunk size stays at 200 words; the 100-, 150- and 400-word runs were repeated with bge (see the all-51 table above), but the LLM has not been tried with other chunk sizes.

If you change the default model you must rebuild `data/index.faiss` (`python -m ragdemo.index`); both models give 384-dimensional vectors, so a mismatch would not raise an error.

`index`, `evaluate` and `chunk_check` accept `--model` and `--index`, so either model can be run side by side. To repeat the MiniLM rows against a separate index file:
```bash
python -m ragdemo.index --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
python -m ragdemo.evaluate --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
python -m ragdemo.chunk_check --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
```
The bge rows were first produced with a short script before these options existed, and re-running with the options gave the same numbers. The options are for these three commands only; the app and `answer_check` always use the default.

## What I learned
- **Retrieval found the right page.** The baseline scored Hit@5 0.98 on 51 questions, and in a manual spot check both a local and a hosted LLM refused most out-of-scope questions clearly and did not invent facts. The local model blended flu and COVID guidance on one boundary question.
- **The main weakness is at chunk level.** For the measles-risk question the right page came back but not the chunk holding the answer, and Hit@k cannot see that. A chunk-level check with hand-marked answer phrases does see it: with MiniLM on all 51 questions Chunk-Hit@5 was 0.92 (4 misses, including this one), and on the first 21 questions that question was missed at every chunk size I tried.
- **Chunk size.** 100, 150 and 400 words all scored about the same as the 200-word baseline on page-level Hit@k (within one or two questions), even though 93% of the 400-word chunks exceed MiniLM's 256-token limit. The chunk-level check, on the first 21 questions I marked, separated them: larger chunks did better (Chunk-Hit@5 0.86 at 100 and 150 words, 0.90 at 200, 0.95 at 400). The same trend held when I repeated it on all 51 questions with both models (Chunk-Hit@5 0.88, 0.88, 0.92, 0.96 for MiniLM and 0.88, 0.90, 0.96, 1.00 for bge at 100, 150, 200 and 400 words), and bge with 400 words missed nothing at k=5. Larger chunks are an easier target and the LLM has not been tried with them, so I kept the default at 200 words.
- **Embedding model.** bge-small-en-v1.5 (512-token limit) scored higher than MiniLM at page level (Hit@1 0.98 against 0.90, no misses at k=5) but mixed at chunk level on all 51 questions (Chunk-Hit@1 0.65 against 0.69, Chunk-Hit@3 0.90 against 0.88, Chunk-Hit@5 0.96 against 0.92), and it found the measles-risk chunk. The two models differ in more than input length, so this does not show that truncation was the cause.
- **LLM answers.** The free OpenRouter model was more cautious but less dependable than local Ollama (one empty answer, two cut off). Re-running the same 12 questions with Ollama on bge-retrieved chunks, the measles-risk question was answered correctly and all 6 main-set answers were correct, against 4 of 6 before. The COVID booster question was still blended with flu guidance, and the scabies refusal falsely said the sources mention scabies testing. One run on 12 questions, so I read this as a sign, not proof.

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- Answer quality was judged by one person on 12 questions per model, with no scoring metric, so treat it as a spot check and not a benchmark.
- Only one other embedding model was tried (bge-small-en-v1.5), without its query prefix. Hit@k is page-level, and the larger-chunk advantage at chunk level is partly an easier target and untested with the LLM.
- The OpenRouter run used a free preview model with a 400-token cap, and an earlier run of it hit rate limits (HTTP 429).
- This is a demo built on public data. It is not medical advice.

## How this was built
I built this project with Claude Code (Anthropic's AI coding assistant) helping with implementation: much of the code, the tests and the first drafts of the docs were written with it, and I reviewed the changes and ran everything myself. The parts that need human judgement were done by me:
- **The evaluation set.** I wrote `eval/eval_questions.csv` (51 questions) and `eval/out_of_scope_questions.csv` by hand, so they stay independent of the system being tested.
- **The answer-quality check.** I read every answer from the two LLMs and marked it by hand against the source pages (see `docs/evaluation.md`). I did the same for the later run with bge-retrieved chunks.
- **The chunk-level answer phrases.** I wrote all 51 phrases in `eval/answer_spans.csv` myself, by copying a short phrase from the answering sentence on each page. Claude produced a set of candidate phrases for 30 of the questions as a suggestion, but I did not use them.
- **The results.** Every number in this README comes from a real run saved in `results/`. Nothing is estimated.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
