# Evaluation

> Status: template. Update once the experiments are finished.

## Goal

_What is being measured and why (e.g. does retrieval find the right guidance page for a question?)._

## Evaluation set

- **File:** `eval/eval_questions.csv` (`question`, `expected_source`)
- **Number of questions:** _TODO_
- **How questions were written:** _TODO (e.g. paraphrased, not copied from the page text)_
- **Coverage:** _which pages/topics are covered_

## Metric

**Hit@k:** the share of questions whose expected source appears in the top-k retrieved chunks.
Run with `python -m ragdemo.evaluate`.

## Results

| Setup | Chunk size (words) | Overlap | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|---------|-----------------|-------|-------|-------|
| Baseline | 200 | 40 | all-MiniLM-L6-v2 | | | |
| Larger chunks | 400 | 80 | all-MiniLM-L6-v2 | | | |
| Different model | 200 | 40 | _TODO_ | | | |

## Answer quality (optional)

_Manual check of generated answers: are they grounded, are citations correct, does the model refuse when the sources lack the answer?_

| Question | Grounded? | Citations correct? | Notes |
|----------|-----------|--------------------|-------|
| | | | |

## Failure analysis

_Examples of questions that failed and why (wrong page, answer split across chunks, vocabulary mismatch, etc.)._

## Conclusions

_Which setup worked best, and what you would try next._
