# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Done: the baseline retrieval run, chunk sizes of 100, 150 and 400 words, a second embedding model (bge-small-en-v1.5, now the default), a test of bge's query prefix, a chunk-level check with hand-marked answer phrases for all 51 questions, the chunk-size runs repeated on all 51 with both models, and manual answer checks (Ollama and OpenRouter on the MiniLM baseline, plus Ollama on bge-retrieved chunks at 200 and at 400 words). Also done: a 32-question Ollama answer check at 200 and 400 words (default stays at 200 words) and an overlap test of 0, 20, 40 and 80 words (default stays at 40). Also done: the same 32 + 6 question check with OpenRouter. Also done: BM25 and hybrid search as an opt-in mode, compared on all 51 questions (not adopted as the default). Not done: an OpenRouter check at 400 words.

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
src/ragdemo/   fetch, chunking, ingest, index, retrieve, answer, llm, service, api, evaluate, chunk_check, answer_check
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

## API and Docker
The Docker image has not been built or tested yet.

A FastAPI service gives the same retrieval and grounded answer over HTTP. Build the data first (`ragdemo.ingest`, then `ragdemo.index`).
```powershell
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
uvicorn ragdemo.api:app          # interactive docs at http://127.0.0.1:8000/docs
```
`GET /health` says the process is up. `POST /ask` takes `{"question": "...", "k": 3}` and returns `answer`, `llm_used` and the numbered `sources`. If no LLM is usable, `answer` is null and the sources are still returned. The server's `LLM_BACKEND` setting chooses the LLM.

With Docker (the image does not contain the data, so mount it):
```powershell
docker build -t uk-health-rag .
docker run --rm -p 127.0.0.1:8000:8000 -v "${PWD}/data:/app/data:ro" -e OLLAMA_URL=http://host.docker.internal:11434 uk-health-rag
```
The service has no authentication or rate limiting, so keep it on your own machine until those are added.

## Fetching data
`ragdemo.fetch` uses only the standard library and two free GOV.UK APIs (no key needed):
- `discover` searches the Search API (default: UK Health Security Agency `detailed_guide` pages) and writes candidate paths to `data/sources.txt`. Options: `--org`, `--doc-type` (repeatable), `--query`, `--count`, `--out`.
- `fetch` downloads each path left in `data/sources.txt` from the Content API, converts the HTML to plain text, and saves `data/raw/<slug>.txt` plus `data/raw/manifest.csv` (source, title, url, updated, licence). Options: `--sources`, `--raw-dir`.

Pages with fewer than 100 words (for example PDF-only or collection pages) and failed requests are skipped and listed at the end. Requests are throttled to stay well under the API rate limit. The manifest records the licence as OGL v3.0; check each page's own licence before relying on it.

## Connecting an LLM
`app.py` retrieves the top 3 chunks and sends one grounded prompt (replies capped at 400 tokens, or 1,500 with OpenRouter) to an LLM chosen by `LLM_BACKEND`:

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

Larger chunks did better for both models, matching the 21-question result above. bge was ahead of MiniLM at every k at 150 and 400 words, and mixed at 100 and 200 words, though several gaps are one or two questions. bge with 400-word chunks is the best retrieval setup I tried: no questions missed at k=5, and Hit@1 1.00 at page level. Two cautions. A larger chunk is an easier target and the top 5 cover more text (about 2,000 words at 400 words per chunk, against about 500 at 100). I did run the LLM with 400-word chunks twice (Ollama and OpenRouter, 12 questions each, see "What I learned"), and the answers were about as good as at 200 words, not clearly better, and that is a small check, so the default stays at 200 words for now and changing it is a separate decision. I did not measure how many 400-word chunks exceed bge's 512-token limit.

**Second embedding model.** `BAAI/bge-small-en-v1.5` (33.4M parameters, 384-dimensional, 512-token input limit, run here without its optional query prefix, which is tested separately below) on the same 330 baseline chunks, none of which exceed its limit. Raw output: `results/retrieval_bge_small.txt` and `results/chunk_check_bge_small.txt`.

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

**Default model.** On 2026-11-23 the default became `BAAI/bge-small-en-v1.5` (`ragdemo.index.DEFAULT_MODEL`), so the Quick start, the app and `answer_check` now use it. The reasons: at page level it was ahead, mainly at k=1 (Hit@1 0.98 against 0.90, 4 questions; 1 question at k=3 and k=5), at chunk level on all 51 questions it was mixed (behind by 2 questions at k=1, ahead by 1 at k=3, which is the k the app uses, and by 2 at k=5), it answered 6 of 6 main-set questions correctly in the 12-question answer check against 4 of 6, and it reads 512 tokens, so none of the 200-word chunks are cut off. The costs: indexing the 330 chunks took about 98 s against 36 s, and embedding a question about 44 ms against 26 ms (`results/embedding_timing.txt`, CPU, rough). The evidence is thin and not uniformly in bge's favour (the gaps are one to four questions, one answer-check run, and the default runs without bge's query prefix), so this is a judgement that the demo can reverse cheaply, not a proven result. The chunk size stays at 200 words; the 100-, 150- and 400-word runs were repeated with bge (see the all-51 table above), but the LLM was tried with other chunk sizes only at 400 words (Ollama and OpenRouter, 12 questions each).

If you change the default model you must rebuild `data/index.faiss` (`python -m ragdemo.index`); both models give 384-dimensional vectors, so a mismatch would not raise an error.

`index`, `evaluate`, `chunk_check` and `answer_check` accept `--model`, `--chunks` and `--index`, so either model or chunk size can be run side by side; all but `index` also accept `--query-prefix`. To repeat the MiniLM rows against a separate index file:
```bash
python -m ragdemo.index --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
python -m ragdemo.evaluate --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
python -m ragdemo.chunk_check --model sentence-transformers/all-MiniLM-L6-v2 --index data/index_minilm.faiss
```
The bge rows were first produced with a short script before these options existed, and re-running with the options gave the same numbers. The app always uses the default model, chunks and index, with no query prefix.

**Query prefix.** bge's authors suggest putting an instruction in front of short search questions (`Represent this sentence for searching relevant passages: `), with the documents indexed as they are. `--query-prefix` does this at search time, so the index needs no rebuild. Run on all 51 questions with bge (no prefix against prefix; raw output in `results/`):

| Chunks | Page Hit@1 / 3 / 5 | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 |
|--------|--------------------|-------------|-------------|-------------|
| 200 words, no prefix | 0.98 / 1.00 / 1.00 | 0.65 | 0.90 | 0.96 |
| 200 words, prefix | 0.98 / 1.00 / 1.00 | 0.65 | 0.94 | 0.96 |
| 400 words, no prefix | 1.00 / 1.00 / 1.00 | 0.84 | 0.96 | 1.00 |
| 400 words, prefix | 1.00 / 1.00 / 1.00 | 0.88 | 0.96 | 1.00 |

The prefix gained 2 questions at one k in each setup (Chunk-Hit@3 at 200 words, Chunk-Hit@1 at 400 words), changed nothing at page level and lost nothing, and the same 2 questions are still missed at k=5 with 200-word chunks. Two questions out of 51 is within noise, so this is a possible small gain, not a proven one. It is off by default, and I did not test it with the LLM. Raw output: `results/retrieval_bge_prefix.txt`, `results/chunk_check_all51_bge_prefix.txt`, `results/retrieval_chunk400_bge_prefix.txt` and `results/chunk_check_all51_chunk400_bge_prefix.txt`.

**Answer quality (manual spot check).** `python -m ragdemo.answer_check` sends 12 questions (6 sampled from the main set, 6 out of scope) through retrieval and a local LLM (`qwen2.5:7b` via Ollama), and I marked each answer by hand against the page text. The three runs used the same questions, seed, model and top 3 chunks; only the retrieval setup changed. Rows where they differ:

| Question | MiniLM, 200 words | bge, 200 words | bge, 400 words |
|----------|-------------------|----------------|----------------|
| Measles risk | Wrong (answering chunk not retrieved) | Correct | Correct |
| Care-home outbreak | Partly (has the "linked by spread" caveat, no 5-day window) | Correct (5-day window, no caveat) | Correct (caveat, no 5-day window) |
| Diphtheria skin wounds | Correct | Correct | Correct, but one sentence not on the page (marked "partly" grounded) |
| COVID booster (out of scope) | Partly refused; applied the flu route | Not refused; applied the flu route | Partial; no flu route, but did not say locations are not given |
| Scabies (out of scope) | Clean refusal | Refusal that falsely said the sources discuss scabies testing | Clean refusal |
| Main set fully correct | 4 of 6 | 6 of 6 | 6 of 6 |
| Out-of-scope refused cleanly | 5 of 6 | 4 of 6 | 5 of 6 |

With bge retrieval the measles-risk question is answered correctly at both chunk sizes, which MiniLM got wrong. The 400-word run was at least as good as the 200-word bge run, not clearly better. This is one run per setup, 12 questions and one marker, so it is a spot check and not a benchmark. Per-question notes are in `docs/evaluation.md`; raw reports are `results/answer_check_ollama.md`, `results/answer_check_ollama_bge.md` and `results/answer_check_ollama_bge_400.md`.

I also ran the same 12 questions through OpenRouter (free `baidu/ernie-5.5-flash-preview`) with bge retrieval and a 1,500-token reply cap, over 200-word chunks (`results/answer_check_openrouter_bge.md`) and over 400-word chunks (`results/answer_check_openrouter_bge_400.md`). The counts were the same at both sizes (6 of 6 main-set answers, 6 of 6 refusals), with small slips in both directions, so with OpenRouter too 400 words showed no clear gain. All 24 replies finished normally, and in both runs one main-set answer (diphtheria) was marked only partly grounded. The first OpenRouter run (MiniLM retrieval, 400-token cap) had one empty and two cut-off answers. That run changed the embedding model and the cap at once, so it does not show which helped, and it is one run on 12 questions. With 32 in-scope and 6 out-of-scope questions at 200 words (`results/answer_check_openrouter_bge_32.md`, the same questions as the Ollama 32-question runs), OpenRouter had 31 of 32 in-scope answers correct and refused all 6 out-of-scope questions cleanly, against 31 and 4 for Ollama at 200 words and 30 and 5 at 400 words. One run each, one marker.

**Chunk overlap.** With 200-word chunks and bge, I compared overlaps of 0, 20, 40 (the default) and 80 words on all 51 questions, under a rule written first (change only if Chunk-Hit@3 rises by at least 3 questions; raw output `results/*overlap*_bge.txt`):

| Overlap | Chunks | Hit@3 | Chunk-Hit@3 | Chunk-Hit@5 |
|---|---|---|---|---|
| 0 | 271 | 1.00 | 46 of 51 (2 answer phrases fall across a chunk boundary) | 0.98 of 49 checked |
| 20 | 297 | 1.00 | 46 of 51 | 1.00 |
| 40 (default) | 330 | 1.00 | 46 of 51 | 0.96 |
| 80 | 421 | 1.00 | 46 of 51 | 0.94 |

All four settings tie at k=3, so the default stays at 40. Overlap 20 was ahead at k=5 by two questions and not worse anywhere, which I record as a candidate and not a result. It does not change the prompt size (mean 4,219 against 4,228 characters), only the number of chunks. Details are in `docs/evaluation.md`.

**Hybrid search.** I added BM25 keyword search and a hybrid of BM25 and dense search (reciprocal rank fusion), off by default (`--mode bm25|hybrid` on `evaluate`, `chunk_check` and `answer_check`). The settings and the adoption rule were fixed before the run. On all 51 questions at 200 words, hybrid put the answering chunk first for many more questions than dense (Chunk-Hit@1 44 against 33 of 51) but was only one question ahead at k=3 (47 against 46 of 51, 49 needed), so dense stays the default. BM25 alone scored 48 at k=3, probably helped by questions that share wording with the pages. One run, one question set; details and raw output in `docs/evaluation.md` and `results/*hybrid*`.

## What I learned
- **Retrieval found the right page.** The baseline scored Hit@5 0.98 on 51 questions, and in a manual spot check both a local and a hosted LLM refused most out-of-scope questions clearly and did not invent facts. The local model blended flu and COVID guidance on one boundary question.
- **The main weakness is at chunk level.** For the measles-risk question the right page came back but not the chunk holding the answer, and Hit@k cannot see that. A chunk-level check with hand-marked answer phrases does see it: with MiniLM on all 51 questions Chunk-Hit@5 was 0.92 (4 misses, including this one), and on the first 21 questions that question was missed at every chunk size I tried.
- **Chunk size.** 100, 150 and 400 words all scored about the same as the 200-word baseline on page-level Hit@k (within one or two questions), even though 93% of the 400-word chunks exceed MiniLM's 256-token limit. The chunk-level check, on the first 21 questions I marked, separated them: larger chunks did better (Chunk-Hit@5 0.86 at 100 and 150 words, 0.90 at 200, 0.95 at 400). The same trend held when I repeated it on all 51 questions with both models (Chunk-Hit@5 0.88, 0.88, 0.92, 0.96 for MiniLM and 0.88, 0.90, 0.96, 1.00 for bge at 100, 150, 200 and 400 words), and bge with 400 words missed nothing at k=5. Larger chunks are an easier target and the LLM checks with 400-word chunks were single runs on 12 questions each, so I kept the default at 200 words. I then set a rule in advance (400 words only if at least 3 more of 32 in-scope answers were correct, with no more unclean out-of-scope refusals) and ran Ollama on 32 in-scope and 6 out-of-scope questions at both sizes: 31 correct at 200 words against 30 at 400, and 4 against 5 clean refusals out of 6, so the default stays at 200 words (`results/answer_check_ollama_bge_32.md`, `results/answer_check_ollama_bge_400_32.md`; one run each, one marker).
- **Embedding model.** bge-small-en-v1.5 (512-token limit) scored higher than MiniLM at page level (Hit@1 0.98 against 0.90, no misses at k=5) but mixed at chunk level on all 51 questions (Chunk-Hit@1 0.65 against 0.69, Chunk-Hit@3 0.90 against 0.88, Chunk-Hit@5 0.96 against 0.92), and it found the measles-risk chunk. The two models differ in more than input length, so this does not show that truncation was the cause.
- **Query prefix.** bge's recommended query prefix gave a small chunk-level gain (Chunk-Hit@3 0.90 to 0.94 at 200 words, Chunk-Hit@1 0.84 to 0.88 at 400 words, 2 questions each) and no change at page level, with no losses. That is within noise on 51 questions, so it stays off by default.
- **LLM answers.** The free OpenRouter model was more cautious but less dependable than local Ollama in its first run (one empty answer, two cut off). Re-running the same 12 questions with Ollama on bge-retrieved chunks, the measles-risk question was answered correctly and all 6 main-set answers were correct, against 4 of 6 before. The COVID booster question was still blended with flu guidance, and the scabies refusal falsely said the sources mention scabies testing. One run on 12 questions, so I read this as a sign, not proof. With bge retrieval over 400-word chunks (three chunks of about 400 words per prompt), the same 12 questions gave 6 of 6 main-set answers correct again, 5 of 6 out-of-scope questions refused cleanly, and no flu-route blend on the COVID booster question (it still did not say that locations are not given). It left out the 5-day window on the care-home question and added an unsupported "increases the risk" sentence to the diphtheria answer, so it was at least as good as the 200-word runs but not clearly better (`results/answer_check_ollama_bge_400.md`).

## Limitations
- Answers are only as good as the retrieved passages. The model is told to say when the sources do not contain the answer.
- Answer quality was judged by one person on 12 questions per model, with no scoring metric, so treat it as a spot check and not a benchmark.
- Only one other embedding model was tried (bge-small-en-v1.5), and its query prefix changed little (2 questions at one k, within noise). Hit@k is page-level, and the larger-chunk advantage at chunk level is partly an easier target and checked with the LLM only at 400 words, on 12 questions per backend.
- The OpenRouter runs used a free preview model. The first had a 400-token cap, and an earlier attempt hit rate limits (HTTP 429); the later run used a 1,500-token cap.
- This is a demo built on public data. It is not medical advice.

## How this was built
I built this project with Claude Code (Anthropic's AI coding assistant) helping with implementation: much of the code, the tests and the first drafts of the docs were written with it, and I reviewed the changes and ran everything myself. The parts that need human judgement were done by me:
- **The evaluation set.** I wrote `eval/eval_questions.csv` (51 questions) and `eval/out_of_scope_questions.csv` by hand, so they stay independent of the system being tested.
- **The answer-quality check.** I read every answer from the two LLMs and marked it by hand against the source pages (see `docs/evaluation.md`). I did the same for the later run with bge-retrieved chunks.
- **The chunk-level answer phrases.** I wrote all 51 phrases in `eval/answer_spans.csv` myself, by copying a short phrase from the answering sentence on each page. Claude produced a set of candidate phrases for 30 of the questions as a suggestion, but I did not use them.
- **The results.** Every number in this README comes from a real run saved in `results/`. Nothing is estimated.

## Data
Use public pages only, and check the licence (many GOV.UK pages are under the Open Government Licence). Do not commit raw data.
