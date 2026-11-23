# Evaluation

> Status: baseline retrieval run and a manual answer spot check (Ollama and OpenRouter) are done. Chunk sizes of 100, 150 and 400 words have been run at page level and at chunk level (21 questions). A second embedding model (bge-small-en-v1.5) has also been run at both levels.

## Goal

Two things are checked. Retrieval is measured: does it find the right guidance page for a question (Hit@k, below). Answer quality is only spot-checked by hand: are the LLM's answers grounded in the retrieved text, do they cite the right source, and does the model refuse when the sources lack the answer.

## Evaluation set

- **File:** `eval/eval_questions.csv` (`question`, `expected_source`)
- **Number of questions:** 51
- **How questions were written:** paraphrased from the page content, not copied from it, with one expected source per question (no topic that two pages both cover). They were written before the retriever was run, so the set was not tuned to the system, and mix plain-language and professional wording.
- **Coverage:** all 32 pages in `data/raw/` have at least one question; no page has more than 2.

## Metric

**Hit@k:** the share of questions whose expected source appears in the top-k retrieved chunks.
Run with `python -m ragdemo.evaluate` (add `--misses` to list questions that failed at k=5).

## Results

| Setup | Chunk size (words) | Overlap | Embedding model | Hit@1 | Hit@3 | Hit@5 |
|-------|--------------------|---------|-----------------|-------|-------|-------|
| Baseline | 200 | 40 | all-MiniLM-L6-v2 | 0.90 | 0.98 | 0.98 |
| Smaller chunks | 100 | 20 | all-MiniLM-L6-v2 | 0.92 | 0.98 | 1.00 |
| Smaller chunks | 150 | 30 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Larger chunks | 400 | 80 | all-MiniLM-L6-v2 | 0.94 | 0.98 | 1.00 |
| Different model | 200 | 40 | bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 |

Raw output: `results/retrieval_baseline.txt`, `results/retrieval_chunk100.txt`, `results/retrieval_chunk150.txt` and `results/retrieval_chunk400.txt` (each header records the settings, chunk count and token lengths). Overlap was 20% of the chunk size in every run. The 100-, 150- and 400-word runs missed 0 of 51 questions at k=5, against 1 of 51 for the baseline. One question is about 0.02 of a score, so Hit@1 moving from 0.90 (46 questions) to 0.92 (47) and 0.94 (48) is a one- or two-question change and could be noise.

Token lengths under the embedding model's tokenizer, which reads at most 256 tokens per input: 183 of 330 baseline chunks (55%) are over the limit, against 11 of 436 (3%) for 150 words and 0 of 651 for 100 words. The smaller chunks therefore avoid most truncation, but chunk size changed in other ways too (more, shorter chunks), so this does not prove truncation was the cause. Hit@k is page-level, so these runs say nothing yet about whether the chunk holding the answer is retrieved (the measles-risk question).

The 400-word run is the opposite test: 158 of 169 chunks (93%) are over the 256-token limit (median 515 tokens, maximum 752), yet it scored 0.94, 0.98 and 1.00, as well as the best smaller setup. I expected a drop and did not get one, so page-level Hit@k does not show the cost of truncation. Hit@k is also not comparable across chunk sizes: the top 5 chunks cover about 2,000 words at 400 words per chunk, against about 500 at 100 words per chunk, which makes a page-level hit easier by itself.

**Different model:** `BAAI/bge-small-en-v1.5` (33.4M parameters, 384-dimensional, 512-token input limit) was run on the same 330 baseline chunks, none of which exceed its limit (0 of 330, against 183 of 330 for MiniLM's 256-token limit). It was used without its optional query instruction prefix. Raw output: `results/retrieval_bge_small.txt`. It missed 0 of 51 questions at k=5, including the MMRV chickenpox question the baseline missed, and Hit@1 rose from 0.90 (46 questions) to 0.98 (50). It differs from MiniLM in training data and architecture as well as input length, so this does not show that truncation caused the baseline's misses.

## Chunk-level check

**Metric:** Chunk-Hit@k, the share of questions where a chunk containing the answer is in the top k. Run with `python -m ragdemo.chunk_check`. For each question I copied a short phrase word for word from the answering sentence into `answer_text` in `eval/answer_spans.csv`; a chunk counts as answering if its text contains the phrase (case, quotes and line breaks ignored), so the same file works for any chunk size. 21 of the 51 questions are marked so far; the tool skips the rest. In every run all 21 phrases were found in at least one chunk.

| Setup | Chunk size (words) | Overlap | Chunks | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 | Missed at k=5 |
|-------|--------------------|---------|--------|-------------|-------------|-------------|---------------|
| Smaller chunks | 100 | 20 | 651 | 0.43 | 0.71 | 0.86 | 3 |
| Smaller chunks | 150 | 30 | 436 | 0.57 | 0.71 | 0.86 | 3 |
| Baseline | 200 | 40 | 330 | 0.62 | 0.81 | 0.90 | 2 |
| Larger chunks | 400 | 80 | 169 | 0.71 | 0.86 | 0.95 | 1 |
| Different model (bge-small-en-v1.5) | 200 | 40 | 330 | 0.62 | 0.86 | 0.95 | 1 |

Raw output: `results/chunk_check_bge_small.txt` for the different-model row, and `results/chunk_check_baseline.txt`, `results/chunk_check_chunk100.txt`, `results/chunk_check_chunk150.txt`, `results/chunk_check_chunk400.txt`.

What the runs show:
- One question is about 0.05, so the gap between 100 and 150 words at Hit@1 (0.43 against 0.57) is 3 questions. The pattern is more informative than any single number.
- Larger chunks scored higher at every k, the opposite of the small-chunk lead at page level. The 400-word chunks were mostly over the embedding model's 256-token limit and still scored best, so truncation did not stop retrieval here. Why is not tested.
- The measles-risk question (answering chunk is chunk 0 of the MMR catch-up page) was missed at every chunk size, and was the only miss at 400 words. This is the failure page-level Hit@k could not see.
- The MMRV chickenpox question (a Hit@k miss in the baseline) was also a chunk-level miss in the baseline, but not at 100, 150 or 400 words. The other misses were: at 100 words, the cold-weather temperature and tick-borne encephalitis milk questions; at 150 words, the MERS countries and cold-weather temperature questions.
- bge-small-en-v1.5 on the baseline chunks scored Chunk-Hit@1/3/5 of 0.62, 0.86 and 0.95. The measles-risk chunk was found, and the one miss was the tick-borne encephalitis milk question (right page, answering chunk 4 not in the top 5). Chunk-Hit@1 did not change; the gain is at k=3 and k=5 (one question each, so within noise on 21 questions).
- This is still not a fully fair comparison between sizes: a longer chunk is a bigger target for the phrase, and the top 5 cover more text. The check also does not test what the LLM does with longer chunks.
- The 21 questions are the ones I chose to mark, not a random sample.

## Answer quality

This is a small qualitative check, not a benchmark. No scoring metric was computed, and counts are given with their sample size because 6 + 6 questions are too few for reliable percentages. Run on 2026-11-17 using `python -m ragdemo.answer_check`: top 3 chunks per question, six questions sampled from the main set (seed 0) and six from `eval/out_of_scope_questions.csv`. Verdicts were checked by hand against the source page text. Ollama (`qwen2.5:7b`) is in the table below (report: `results/answer_check_ollama.md`). The OpenRouter run (`results/answer_check_openrouter.md`) used the same 12 questions and is summarised after the table.

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

**OpenRouter (`baidu/ernie-5.5-flash-preview:free`), same 12 questions:** 10 answers were correct or correctly refused, 1 was an honest non-answer and 1 failed.
- Measles risk: said the sources do not identify the at-risk group, where Ollama answered confidently and wrongly. Given what retrieval supplied, this is the better behaviour.
- Care-home outbreak: complete (5-day window, "linked by spread" caveat, single confirmed flu case), where Ollama left out the 5-day window.
- COVID booster: failed with "empty answer". The measles-risk and SFTS answers were cut off mid-sentence. The 400-token cap may be the cause (not confirmed).
- All five clear out-of-scope questions were refused cleanly.

**Ollama with bge-retrieved chunks, same 12 questions** (`results/answer_check_ollama_bge.md`, run on 2026-11-23): the same questions, seed and `qwen2.5:7b`, but the top 3 chunks came from the bge-small-en-v1.5 index instead of MiniLM. The answers were marked by hand against the page text in `data/raw/`, as for the two reports above.
- All 6 main-set answers were correct and grounded, against 4 of 6 correct with MiniLM-retrieved chunks.
- Measles risk: now correct (people aged 30 and under who did not have 2 MMR doses). This is the question that was wrong with MiniLM, where the answering chunk 0 ranked 9th. With bge it ranked 2nd, so it reached the LLM.
- Care-home outbreak: now includes the 5-day window. SFTS: now includes the close-contact route for human-to-human spread. Both were left out with MiniLM. The care-home answer still omits the "linked by spread" caveat.
- Out-of-scope: 4 of 6 refused cleanly. The COVID booster question gave the same blend as before: it applies the flu route (occupational health, pharmacy, GP) to COVID. The scabies question was refused but said the sources discuss "scabies testing procedures", and scabies appears in none of the 32 pages, so that clause is a false statement about the sources.
- This is one run per setup on 12 questions with one marker. The difference in retrieval is the likely reason for the improvement, but LLM output also varies between runs, and this was not repeated.

## Failure analysis

Baseline run (`results/retrieval_baseline.txt`): 1 of 51 questions missed at k=5. The question about the combined measles, mumps, rubella and chickenpox jab from 2026 expected `universal-varicella-vaccination-programme-in-england.txt`, but 4 of the top 5 chunks came from `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` and one from `pertussis-clinical-and-public-health-management.txt`. The reason has not been investigated.

**Answer-quality finding: right page retrieved, wrong chunk (measles risk question).** In the manual answer check (`results/answer_check_ollama.md`, `results/answer_check_openrouter.md`), the question "Who is most at risk of catching measles at the moment?" was a Hit@k success, because the expected page `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` was retrieved. Both models still answered it wrongly. They named vulnerable close contacts (immunosuppressed people, pregnant women, children under 1), which the page says to protect, instead of people aged 30 and under who did not have 2 MMR doses, which the page gives as the group most at risk. The sentence that answers the question is only in chunk 0 of that page. Retrieval for this question returned chunks 2, 5, 6, 7 and 4 of the page in ranks 1 to 5, and chunk 0 was not in the top 8. The LLM therefore never saw the answer, so this is a retrieval failure, not a generation failure. Likely cause (not tested): chunk 0 is a 200-word introduction on several topics, so the sentence is a small part of its embedding. Chunks 5 and 6 also overlap heavily, so two of the three chunks sent to the LLM (k=3) were near-duplicates. Hit@k is measured at page level and cannot see this kind of failure. No change has been made to chunking or k, because a change tuned to one question could hurt others.

## Conclusions

Retrieval found the right page within the top 5 for 50 of 51 questions (Hit@1 0.90, Hit@3 and Hit@5 0.98). The one miss was the MMRV chickenpox question, whose page was crowded out by the MMR catch-up page. Hit@k is measured at page level and hides a second kind of failure: for the measles-risk question the right page was retrieved but the chunk holding the answer was not, so one model answered wrongly and the other correctly said the sources did not say.

In the manual spot check, both LLMs stayed within the sources and refused most out-of-scope questions cleanly. The one exception was the COVID booster boundary question, where Ollama blended flu and COVID guidance (the OpenRouter call for that question failed). Ollama (`qwen2.5:7b`) was concise and completed all 12 questions but answered the measles question confidently and wrongly. The OpenRouter free model was more careful but less reliable (one empty answer, two cut-off answers). With only 12 questions per model and one reviewer, these are observations, not measured accuracy.

Chunk sizes of 100, 150 and 400 words all matched or slightly beat the baseline at every k and found the baseline's one miss, but the gains are one or two questions out of 51, and the heavily truncated 400-word chunks scored as well as the best smaller setup. Page-level Hit@k therefore does not separate these setups. Changing the embedding model helped more than changing chunk size at page level: bge-small-en-v1.5 scored Hit@1/3/5 of 0.98, 1.00 and 1.00, with no misses. A chunk-level check on 21 hand-marked questions did separate them (see above): Chunk-Hit@5 rose with chunk size, from 0.86 at 100 and 150 words to 0.95 at 400, and the measles-risk chunk was missed at every size. Next steps: mark the remaining 30 questions in `eval/answer_spans.csv`, then test overlap, bge's query prefix, and bge with other chunk sizes using the chunk-level check.
