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

Run on 2026-11-17 with local Ollama (`qwen2.5:7b`), top 3 chunks per question, using `python -m ragdemo.answer_check` (report: `results/answer_check_ollama.md`). Six questions were sampled from the main set (seed 0) and six come from `eval/out_of_scope_questions.csv`. Verdicts were checked by hand against the source page text. A matching OpenRouter run (`results/answer_check_openrouter.md`) is incomplete: 4 of 12 answers failed with HTTP 429 (rate limited), and it was run with the earlier version of the out-of-scope set.

| Question | Grounded? | Citations correct? | Notes |
|----------|-----------|--------------------|-------|
| Who is most at risk of catching measles at the moment? | Yes | Yes (right page) | **Wrong answer.** Named vulnerable contacts (immunosuppressed, pregnant, under 1) instead of people aged 30 and under who missed 2 MMR doses. The answering sentence is only in chunk 0 of the page, which was not in the top 8 retrieved chunks, so the model never saw it. |
| Which hantavirus is treated as an airborne HCID in the UK? | Yes | Yes | Correct (Andes virus). |
| Where was the SFTS virus first found and how does it spread? | Yes | Yes | Correct (China, 2009; tick bites). Dropped that human-to-human spread is rare. |
| When did the UK last have a locally acquired polio case? | Yes | Yes | Correct (1984). |
| How many sick care-home residents count as a reportable respiratory outbreak? | Yes | Yes | Partly correct. Gave "2 or more… if linked by spread" but left out the 5-day window for symptom onset. |
| Why are chronic skin wounds in new arrivals relevant to diphtheria? | Yes | Yes | Correct. |
| What is the recommended adult dose of paracetamol? (out of scope) | Yes | n/a | Correct refusal; no outside facts. |
| How many people caught measles in England last year? (out of scope) | Yes | n/a | Correct refusal; noted the page covers case management but has no incidence data. |
| Is the flu vaccine safe for people with egg allergy? (out of scope) | Yes | n/a | Correct refusal. |
| What are the side effects of the HPV vaccine? (out of scope) | Yes | n/a | Correct refusal; named the unrelated pages it was given. |
| Where can I get a COVID-19 booster this winter? (out of scope, boundary) | Partly | Partly | Right page cited, but applied the flu-vaccine route (occupational health, pharmacy, GP) to COVID. The page only says the NHS contacts people who may be eligible. It admitted locations are not given, but did not clearly refuse. |
| How long should someone with scabies stay off work? (out of scope) | Yes | n/a | Correct refusal. |

Summary: 4 of the 6 main-set answers were fully correct, 1 was partly correct and 1 was wrong. Of the 6 out-of-scope questions, 5 were refused cleanly and 1 was a partial blend. No answer invented facts outside the sources.

## Failure analysis

Baseline run (`results/retrieval_baseline.txt`): 1 of 51 questions missed at k=5. The question about the combined measles, mumps, rubella and chickenpox jab from 2026 expected `universal-varicella-vaccination-programme-in-england.txt`, but 4 of the top 5 chunks came from `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` and one from `pertussis-clinical-and-public-health-management.txt`. The reason has not been investigated.

**Answer-quality finding: right page retrieved, wrong chunk (measles risk question).** In the manual answer check (`results/answer_check_ollama.md`, `results/answer_check_openrouter.md`), the question "Who is most at risk of catching measles at the moment?" was a Hit@k success, because the expected page `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` was retrieved. Both models still answered it wrongly. They named vulnerable close contacts (immunosuppressed people, pregnant women, children under 1), which the page says to protect, instead of people aged 30 and under who did not have 2 MMR doses, which the page gives as the group most at risk. The sentence that answers the question is only in chunk 0 of that page. Retrieval for this question returned chunks 2, 5, 6, 7 and 4 of the page in ranks 1 to 5, and chunk 0 was not in the top 8. The LLM therefore never saw the answer, so this is a retrieval failure, not a generation failure. Likely cause (not tested): chunk 0 is a 200-word introduction on several topics, so the sentence is a small part of its embedding. Chunks 5 and 6 also overlap heavily, so two of the three chunks sent to the LLM (k=3) were near-duplicates. Hit@k is measured at page level and cannot see this kind of failure. No change has been made to chunking or k, because a change tuned to one question could hurt others.

## Conclusions

_Which setup worked best, and what you would try next._
