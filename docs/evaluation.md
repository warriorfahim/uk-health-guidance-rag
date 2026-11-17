# Evaluation

> Status: baseline run done; the larger-chunks and different-model setups are not yet run.

## Goal

_What is being measured and why (e.g. does retrieval find the right guidance page for a question?)._

## Evaluation set

- **File:** `eval/eval_questions.csv` (`question`, `expected_source`)
- **Number of questions:** 51
- **How questions were written:** _TODO (e.g. paraphrased, not copied from the page text)_
- **Coverage:** all 32 pages in `data/raw/` have at least one question; no page has more than 2.

## Metric

**Hit@k:** the share of questions whose expected source appears in the top-k retrieved chunks.
Run with `python -m ragdemo.evaluate` (add `--misses` to list questions that failed at k=5).

## Results

| Setup | Chunk size (words) | Overlap | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|---------|-----------------|-------|-------|-------|
| Baseline | 200 | 40 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Larger chunks | 400 | 80 | all-MiniLM-L6-v2 | | | |
| Different model | 200 | 40 | _TODO_ | | | |

## Answer quality (optional)

_Manual check of generated answers: are they grounded, are citations correct, does the model refuse when the sources lack the answer?_

| Question | Grounded? | Citations correct? | Notes |
|----------|-----------|--------------------|-------|
| | | | |

## Failure analysis

Baseline run (`results/retrieval_baseline.txt`): 1 of 51 questions missed at k=5. The question about the combined measles, mumps, rubella and chickenpox jab from 2026 expected `universal-varicella-vaccination-programme-in-england.txt`, but 4 of the top 5 chunks came from `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` and one from `pertussis-clinical-and-public-health-management.txt`. The reason has not been investigated.

## Conclusions

_Which setup worked best, and what you would try next._
