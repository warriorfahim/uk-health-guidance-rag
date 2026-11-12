# Architecture

> Status: template. Update once the project is finished.

## Overview

_One paragraph: what the system does and who it is for._

## Pipeline

```
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
   │  answer.py   (grounded prompt with numbered sources → LLM)
   ▼
answer with citations  →  app.py (Streamlit UI)
```

## Components

| Module | Responsibility | Key decisions / notes |
|--------|----------------|-----------------------|
| `chunking.py` | Split text into overlapping chunks | _TODO_ |
| `ingest.py` | Read raw pages, write `chunks.jsonl` | _TODO_ |
| `index.py` | Embed chunks, build FAISS index | _TODO_ |
| `retrieve.py` | Semantic search over the index | _TODO_ |
| `answer.py` | Build grounded prompt, call LLM | _TODO_ |
| `evaluate.py` | Hit rate at k on the eval set | _TODO_ |
| `app.py` | Streamlit interface | _TODO_ |

## Data

- **Sources:** _which pages/sites, how many, licence (e.g. Open Government Licence)_
- **Cleaning:** _how pages were converted to plain text_
- **Chunk format:** `{"source", "chunk_id", "text"}`

## Models

- **Embedding model:** _final choice and why_
- **LLM:** _which model, local or API, and why_

## Design decisions and trade-offs

- _e.g. word-based vs token-based chunking_
- _e.g. flat FAISS index vs approximate index_
- _e.g. how the prompt enforces grounding and citations_

## Limitations and future work

- _TODO_
