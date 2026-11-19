# Architecture

> Status: the pipeline, components and data sections describe what the code does today. Items marked "to add" are design reasons that only the author can state.

## Overview

A small demo of semantic search and retrieval-augmented question answering over 32 public UK Health Security Agency guidance pages from GOV.UK. A question is embedded, the most similar chunks of guidance are retrieved from a FAISS index, and an LLM is asked to answer using only those chunks and to cite them as numbered sources. It is a learning and portfolio project on public data, not medical advice.

## Pipeline

```
fetch.py (optional)  GOV.UK Search + Content APIs → data/sources.txt → data/raw/*.txt + manifest.csv
   │
data/raw/*.txt
   │  ingest.py   (chunking.py: word-based chunks with overlap)
   ▼
data/chunks.jsonl
   │  index.py    (sentence-transformers embeddings → FAISS)
   ▼
data/index.faiss
   │  retrieve.py (embed query, top-k cosine similarity)
   ▼
top-k chunks
   │  answer.py   (grounded prompt with numbered sources)
   │  llm.py      (generate(prompt) → text: Ollama, OpenRouter, or echo fallback)
   ▼
answer with citations  →  app.py (Streamlit UI)
```

## Components

| Module | Responsibility | Key decisions / notes |
|--------|----------------|-----------------------|
| `fetch.py` | Find GOV.UK pages (`discover`) and download them as plain text (`fetch`) | Standard library only. Pages under 100 words and failed requests are skipped. Writes `data/raw/manifest.csv` (source, title, url, updated, licence). |
| `chunking.py` | Split text into overlapping chunks | Word-based: default 200 words with 40 overlap, split on whitespace. |
| `ingest.py` | Read raw pages, write `chunks.jsonl` | One record per chunk: `source` (file name), `chunk_id`, `text`. Pages are read in sorted order. |
| `index.py` | Embed chunks, build FAISS index | `all-MiniLM-L6-v2` embeddings, normalised, in an `IndexFlatIP` (cosine similarity). |
| `retrieve.py` | Semantic search over the index | Embeds the query with the same model; returns copies of the chunk records plus a `score`. |
| `answer.py` | Build the grounded prompt | Numbered sources `[1] (file) text`, and rules to use only the sources, cite them, and say when they do not contain the answer. |
| `llm.py` | LLM backends as `generate(prompt) -> str` | `ollama` (default), `openrouter`, `hf` (not supported) and `none`; falls back to echoing the prompt when a backend is unusable. |
| `evaluate.py` | Hit@k on the retrieval eval set | Page-level metric. `--misses` lists failed questions. |
| `answer_check.py` | Manual answer-quality report | Runs sampled in-scope and out-of-scope questions through retrieval (top 3) and the LLM, and writes a report to mark by hand. |
| `app.py` | Streamlit interface | Retrieves the top 3 chunks, shows the answer and the sources, and has a sidebar backend selector. |

## Data

- **Sources:** 32 GOV.UK guidance pages, curated by hand from the candidates that `fetch discover` writes to `data/sources.txt` (its default search is UK Health Security Agency `detailed_guide` pages). Content is Crown copyright under the Open Government Licence v3.0 unless a page states otherwise (the manifest records OGL v3.0; check each page's own licence).
- **Cleaning:** `fetch.py` takes the page body from the Content API and converts the HTML to plain text. It ignores `script`, `style`, `nav` and `footer` content and starts a new line at block tags such as paragraphs, list items and headings.
- **Chunk format:** `{"source", "chunk_id", "text"}`. The current baseline has 330 chunks from the 32 pages.
- **Not committed:** `data/raw/`, `data/chunks.jsonl` and `data/index.faiss` are gitignored. FAISS row `i` must correspond to line `i` of `chunks.jsonl`, so changing the chunking requires re-running ingest and index.

## Models

- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (22.7 million parameters, 384-dimensional vectors), used both to build the index and to embed queries. Why it fits this project:
  - It is open source and runs locally on a CPU, so no text leaves the machine, in line with the local-first LLM choice.
  - It is small and fast, which suits 330 chunks and a laptop.
  - It is the standard example model in the sentence-transformers documentation, so it is a sensible, well-known baseline.
  - It scored Hit@5 0.98 on the 51-question set (`results/retrieval_baseline.txt`).
  - Caveat: it reads at most 256 tokens per input and ignores the rest. 183 of the 330 baseline chunks (55%) are longer than that (median 259 tokens, maximum 409; `results/embedding_token_check.txt`), so for those chunks the last part of the text is not reflected in the embedding. Shorter chunks (the 100-word scenario) would fit; 400-word chunks would be cut off much more. This has not been tested.
- **LLM:** The default LLM backend is local Ollama (qwen2.5:7b), chosen so that questions and retrieved text never leave the machine and there are no API costs or rate limits. OpenRouter is an optional backend, selected in the sidebar. It is used with a free open-source model, which may be rate-limited. It sends the question and retrieved text to a third party, with no guarantee the models are hosted in the UK. A Hugging Face backend is still in the code but is not supported: it requires a paid subscription, and calls without one fail with HTTP 402.

## Design decisions and trade-offs

What the code does, with the reasons still to add:

- **Word-based chunking** (not token-based): chunks are counted in whitespace-separated words. Reason and trade-off: to add.
- **Flat FAISS index** (`IndexFlatIP`, exact search) instead of an approximate index: with 330 chunks it is fast enough. Reason and trade-off: to add.
- **Grounding in the prompt:** the prompt tells the model to answer only from the numbered sources, cite them like [1], and say when it cannot answer. This is enforced by the instruction alone; nothing checks the output, so the manual answer check is how it was assessed (see `docs/evaluation.md`).
- **Pluggable LLM:** `answer.answer` takes any `generate(prompt) -> str` callable, so backends can be swapped without changing retrieval or the prompt.
- **Lazy heavy imports:** `faiss` and `sentence_transformers` are imported inside functions so the unit tests and CI run without them and without downloading models.

## Limitations and future work

- Answers are only as good as the retrieved passages. Hit@k is measured at page level, so it cannot see a case where the right page is retrieved but not the chunk holding the answer (the measles-risk question in `docs/evaluation.md`).
- Retrieval baseline: Hit@1 0.90, Hit@3 0.98, Hit@5 0.98 on 51 questions (`results/retrieval_baseline.txt`). Larger chunks (400 words) and a second embedding model are not yet run.
- 55% of the baseline chunks exceed the embedding model's 256-token limit, so their later text does not influence retrieval. This may relate to the measles-risk miss, but that is not tested. Options to try: shorter chunks, or a model with a longer input limit.
- Answer quality was judged by one person on 12 questions per model, so it is a spot check, not a benchmark.
- Grounding relies on the prompt alone; there is no automatic check that an answer is supported by the sources or that its citations are correct.
- Future work: a chunk-level retrieval check (is the answering chunk in the top k?), then testing chunk size and overlap on all 51 questions.
