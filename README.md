# UK Health Guidance RAG Demo

A small semantic search and retrieval-augmented question answering (RAG) demo over public UK health guidance.
It retrieves the most relevant passages for a question, answers using only those passages, and shows the sources.

> Status: work in progress. Fill in the evaluation table below once you have run the experiments.

## What it does
1. Loads public guidance pages (plain text) and splits them into overlapping chunks.
2. Embeds the chunks with an open-source sentence-transformers model and stores them in a FAISS index.
3. Retrieves the top-k chunks for a query (semantic search).
4. Builds a prompt that asks an LLM to answer using only the retrieved text and to cite its sources.
5. Evaluates retrieval on a hand-written question set (hit rate at k).

## Project layout
```
src/ragdemo/   chunking, ingest, index, retrieve, answer, evaluate
app.py         Streamlit interface
tests/         unit tests (run in CI, no model downloads needed)
data/raw/      put cleaned .txt guidance pages here (not committed)
eval/          eval_questions.csv: question, expected_source
.github/       CI workflow (tests and lint on every push)
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .

# 1. Put cleaned .txt pages in data/raw/ (one file per page; the file name is the source id)
python -m ragdemo.ingest            # writes data/chunks.jsonl
python -m ragdemo.index             # writes data/index.faiss
python -m ragdemo.evaluate          # prints hit rate at k = 1, 3, 5
streamlit run app.py
```

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
