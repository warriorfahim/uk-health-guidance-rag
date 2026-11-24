# Architecture

> Status: the pipeline, components and data sections describe what the code does today. The design reasons for chunking and the index were drafted from the code and results, not recorded at the time; the author should confirm them.

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
| `index.py` | Embed chunks, build FAISS index | `BAAI/bge-small-en-v1.5` embeddings by default (`--model` / `--index` to change), normalised, in an `IndexFlatIP` (cosine similarity). |
| `retrieve.py` | Semantic search over the index | Embeds the query with the same model; returns copies of the chunk records plus a `score`. |
| `answer.py` | Build the grounded prompt | Numbered sources `[1] (file) text`, and rules to use only the sources, cite them, and say when they do not contain the answer. |
| `llm.py` | LLM backends as `generate(prompt) -> str` | `ollama` (default), `openrouter`, `hf` (not supported) and `none`; falls back to echoing the prompt when a backend is unusable. |
| `evaluate.py` | Hit@k on the retrieval eval set | Page-level metric. `--misses` lists failed questions. |
| `chunk_check.py` | Chunk-level hit rate | A chunk counts as answering if it contains the hand-written phrase in `eval/answer_spans.csv`; questions with no phrase are skipped. |
| `answer_check.py` | Manual answer-quality report | Runs sampled in-scope and out-of-scope questions through retrieval (top 3) and the LLM, and writes a report to mark by hand. |
| `app.py` | Streamlit interface | Retrieves the top 3 chunks, shows the answer and the sources, and has a sidebar backend selector. |

## Data

- **Sources:** 32 GOV.UK guidance pages, curated by hand from the candidates that `fetch discover` writes to `data/sources.txt` (its default search is UK Health Security Agency `detailed_guide` pages). Content is Crown copyright under the Open Government Licence v3.0 unless a page states otherwise (the manifest records OGL v3.0; check each page's own licence).
- **Cleaning:** `fetch.py` takes the page body from the Content API and converts the HTML to plain text. It ignores `script`, `style`, `nav` and `footer` content and starts a new line at block tags such as paragraphs, list items and headings.
- **Chunk format:** `{"source", "chunk_id", "text"}`. The current baseline has 330 chunks from the 32 pages.
- **Not committed:** `data/raw/`, `data/chunks.jsonl` and `data/index.faiss` are gitignored. FAISS row `i` must correspond to line `i` of `chunks.jsonl`, so changing the chunking requires re-running ingest and index.

## Models

- **Embedding model:** `BAAI/bge-small-en-v1.5` (33.4 million parameters, 384-dimensional vectors, 512-token input limit), used both to build the index and to embed queries. It became the default on 2026-11-23; the model before that was `sentence-transformers/all-MiniLM-L6-v2` (22.7 million parameters, 256-token limit), which the baseline and chunk-size results used. Why bge:
  - It is open source and runs locally on a CPU, so no text leaves the machine, in line with the local-first LLM choice.
  - At page level it was ahead: Hit@1/3/5 0.98, 1.00, 1.00 against 0.90, 0.98, 0.98 (`results/retrieval_bge_small.txt`).
  - At chunk level on all 51 questions the result was mixed: Chunk-Hit@1/3/5 0.65, 0.90, 0.96 against 0.69, 0.88, 0.92 for MiniLM (`results/chunk_check_all51_bge.txt`, `results/chunk_check_all51_minilm.txt`). bge was behind by 2 questions at k=1 and ahead by 1 at k=3 (the k the app uses) and 2 at k=5, with 2 misses at k=5 against 4.
  - In the 12-question answer check it answered 6 of 6 main-set questions correctly against 4 of 6 (`results/answer_check_ollama_bge.md`), from one run.
  - The gaps are one to four questions, so this is a judgement from small differences that do not all point the same way, not a proven result.
  - Its 512-token limit means none of the 330 baseline chunks (200 words) are cut off. The model differs from MiniLM in more than input length, so this does not prove truncation was the cause of MiniLM's misses.
  - Cost: it is slower on CPU. Indexing the 330 chunks took about 98 s against 36 s, and embedding a question about 44 ms against 26 ms (`results/embedding_timing.txt`, one machine, rough). That is acceptable for a demo of this size.
  - Not tried: bge's recommended query instruction prefix. bge was also run at 100, 150 and 400 words (page-level and chunk-level results in `docs/evaluation.md`).
  - MiniLM caveat (for the earlier results): it reads at most 256 tokens per input and ignores the rest. 183 of the 330 baseline chunks (55%) are longer than that (median 259 tokens, maximum 409; `results/embedding_token_check.txt`), so for those chunks the last part of the text is not reflected in the embedding. With 100-word chunks none are over the limit (0 of 651) and with 150-word chunks 11 of 436 (3%); 400-word chunks are cut off much more (158 of 169, 93%), yet they scored as well on page-level Hit@k (see `docs/evaluation.md`), so that metric does not show the cost of truncation.
- **LLM:** The default LLM backend is local Ollama (qwen2.5:7b), chosen so that questions and retrieved text never leave the machine and there are no API costs or rate limits. OpenRouter is an optional backend, selected in the sidebar. It is used with a free open-source model, which may be rate-limited. It sends the question and retrieved text to a third party, with no guarantee the models are hosted in the UK. A Hugging Face backend is still in the code but is not supported: it requires a paid subscription, and calls without one fail with HTTP 402.

## Design decisions and trade-offs

What the code does, and why. The reasons for chunking and the index were drafted by Claude from the code and the saved results, not recorded when the choices were made:

- **Word-based chunking** (not token-based): chunks are counted in whitespace-separated words (`text.split()`). Reason: it needs no tokenizer, so the same chunks work with any embedding model and the chunk size is easy to reason about (the chunk-size experiments used 100, 150, 200 and 400 words). Trade-off: words are not tokens. Under MiniLM's tokenizer a 200-word chunk has a median of 259 tokens, so 55% exceed its 256-token limit (`results/embedding_token_check.txt`), and the chunk size that fits a model's limit depends on the model. Splitting on whitespace also drops the pages' line breaks, so the chunk text is flattened to one paragraph.
- **Flat FAISS index** (`IndexFlatIP`, exact search) instead of an approximate index: with 330 chunks it is fast enough. Reason: exact search compares the query with every chunk, so the results are never an approximation, and there is nothing to train or tune. Trade-off: the cost grows linearly with the number of chunks, so a much larger corpus (tens of thousands of chunks or more) would need an approximate index. Search time was not measured here.
- **Grounding in the prompt:** the prompt tells the model to answer only from the numbered sources, cite them like [1], and say when it cannot answer. This is enforced by the instruction alone; nothing checks the output, so the manual answer check is how it was assessed (see `docs/evaluation.md`).
- **Pluggable LLM:** `answer.answer` takes any `generate(prompt) -> str` callable, so backends can be swapped without changing retrieval or the prompt.
- **Lazy heavy imports:** `faiss` and `sentence_transformers` are imported inside functions so the unit tests and CI run without them and without downloading models.

## Limitations and future work

- Answers are only as good as the retrieved passages. Hit@k is measured at page level, so it cannot see a case where the right page is retrieved but not the chunk holding the answer (the measles-risk question in `docs/evaluation.md`).
- Retrieval baseline: Hit@1 0.90, Hit@3 0.98, Hit@5 0.98 on 51 questions (`results/retrieval_baseline.txt`). Other chunk sizes scored the same or slightly higher (100 words: 0.92, 0.98, 1.00; 150 words: 0.94, 0.98, 1.00; 400 words: 0.94, 0.98, 1.00; see `docs/evaluation.md`). A second embedding model, `BAAI/bge-small-en-v1.5` (512-token limit), scored 0.98, 1.00, 1.00 on the baseline chunks (`results/retrieval_bge_small.txt`); it is now the default embedding model (see Models above). The MiniLM rows above are the baseline and chunk-size runs; bge was also run at 100, 150 and 400 words (page-level Hit@1 0.98, 0.98 and 1.00, with no misses at k=5; see `docs/evaluation.md`).
- 55% of the baseline chunks exceed MiniLM's 256-token limit, so their later text does not influence retrieval. The measles-risk answer sentence sits at about words 102 to 120 of chunk 0 in the 200-word chunks, inside that limit, so truncation is unlikely to explain that miss. Shorter chunks and a model with a longer input limit (bge-small-en-v1.5) both did as well or better, but neither isolates truncation as the cause of other misses.
- Answer quality was judged by one person on 12 questions per model, so it is a spot check, not a benchmark.
- Grounding relies on the prompt alone; there is no automatic check that an answer is supported by the sources or that its citations are correct.
- A chunk-level check (`chunk_check.py`, `eval/answer_spans.csv`) exists and all 51 questions now have a hand-written answer phrase. Across chunk sizes it gives Chunk-Hit@5 of 0.88, 0.88, 0.92 and 0.96 (MiniLM) and 0.88, 0.90, 0.96 and 1.00 (bge) at 100, 150, 200 and 400 words, so larger chunks retrieve the answering chunk more often, partly because they are an easier target; see `docs/evaluation.md`.
- Future work: repeat the LLM answer check with 400-word chunks on more than 12 questions (one 12-question run was at least as good as 200 words; the default stays at 200 words until then), and test overlap and bge's query prefix.
