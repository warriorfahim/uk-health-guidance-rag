# Evaluation

> Status: baseline retrieval run and a manual answer spot check (Ollama and OpenRouter) are done. Chunk sizes of 100, 150 and 400 words have been run at page level (51 questions) and at chunk level (first on the 21 questions that had a hand-written answer phrase, then repeated on all 51 with both embedding models). A second embedding model (bge-small-en-v1.5) has also been run at both levels, and became the default on 2026-11-23 (reasons in `docs/architecture.md`). Rows below labelled "Baseline", "Smaller chunks" or "Larger chunks" were run with all-MiniLM-L6-v2, the earlier default; rows labelled "Different model" were run with bge-small-en-v1.5. Also done, all with bge: a test of bge's query prefix (off by default); manual answer checks with Ollama at 200 and 400 words and with OpenRouter at 200 and 400 words on 12 questions each; a larger 32 in-scope + 6 out-of-scope check with Ollama at 200 and 400 words (default chunk size stays at 200 words) and with OpenRouter at 200 words; an overlap test of 0, 20, 40 and 80 words (default stays at 40); and BM25 and hybrid search as an opt-in mode (not adopted as the default). Not done: the 32 + 6 question check with OpenRouter at 400 words.

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
| Different model, smaller chunks | 100 | 20 | bge-small-en-v1.5 | 0.98 | 0.98 | 1.00 |
| Different model, smaller chunks | 150 | 30 | bge-small-en-v1.5 | 0.98 | 1.00 | 1.00 |
| Different model, larger chunks | 400 | 80 | bge-small-en-v1.5 | 1.00 | 1.00 | 1.00 |

Raw output: `results/retrieval_baseline.txt`, `results/retrieval_chunk100.txt`, `results/retrieval_chunk150.txt` and `results/retrieval_chunk400.txt` (MiniLM), and `results/retrieval_bge_small.txt`, `results/retrieval_chunk100_bge.txt`, `results/retrieval_chunk150_bge.txt` and `results/retrieval_chunk400_bge.txt` (bge) (each header records the settings, chunk count and token lengths). Overlap was 20% of the chunk size in every run. The 100-, 150- and 400-word runs missed 0 of 51 questions at k=5, against 1 of 51 for the baseline. One question is about 0.02 of a score, so Hit@1 moving from 0.90 (46 questions) to 0.92 (47) and 0.94 (48) is a one- or two-question change and could be noise.

Token lengths under MiniLM's tokenizer, which reads at most 256 tokens per input: 183 of 330 baseline chunks (55%) are over the limit, against 11 of 436 (3%) for 150 words and 0 of 651 for 100 words. The smaller chunks therefore avoid most truncation, but chunk size changed in other ways too (more, shorter chunks), so this does not prove truncation was the cause. Hit@k is page-level, so these runs say nothing yet about whether the chunk holding the answer is retrieved (the measles-risk question).

The 400-word run is the opposite test: 158 of 169 chunks (93%) are over the 256-token limit (median 515 tokens, maximum 752), yet it scored 0.94, 0.98 and 1.00, as well as the best smaller setup. I expected a drop and did not get one, so page-level Hit@k does not show the cost of truncation. Hit@k is also not comparable across chunk sizes: the top 5 chunks cover about 2,000 words at 400 words per chunk, against about 500 at 100 words per chunk, which makes a page-level hit easier by itself.

**Different model:** `BAAI/bge-small-en-v1.5` (33.4M parameters, 384-dimensional, 512-token input limit) was run on the same 330 baseline chunks, none of which exceed its limit (0 of 330, against 183 of 330 for MiniLM's 256-token limit). It was used without its optional query instruction prefix here (the prefix is tested in the Query prefix section below). Raw output: `results/retrieval_bge_small.txt`. It missed 0 of 51 questions at k=5, including the MMRV chickenpox question the baseline missed, and Hit@1 rose from 0.90 (46 questions) to 0.98 (50). It differs from MiniLM in training data and architecture as well as input length, so this does not show that truncation caused the baseline's misses.

## Chunk-level check

**Metric:** Chunk-Hit@k, the share of questions where a chunk containing the answer is in the top k. Run with `python -m ragdemo.chunk_check`. For each question I copied a short phrase word for word from the answering sentence into `answer_text` in `eval/answer_spans.csv` (I wrote all 51 myself; Claude produced candidate phrases for 30 of them as a suggestion, which I did not use); a chunk counts as answering if its text contains the phrase (case, quotes and line breaks ignored), so the same file works for any chunk size. All 51 questions now have a phrase. The chunk-size runs below were made when only the first 21 did (the tool skips rows with no phrase), so they cover 21 questions; the all-51 runs are in the table after them. In every run every phrase was found in at least one chunk.

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
- Larger chunks scored higher at every k, the opposite of the small-chunk lead at page level. The 400-word chunks were mostly over MiniLM's 256-token limit and still scored best, so truncation did not stop retrieval here. Why is not tested.
- The measles-risk question (answering chunk is chunk 0 of the MMR catch-up page) was missed at every chunk size, and was the only miss at 400 words. This is the failure page-level Hit@k could not see.
- The MMRV chickenpox question (a Hit@k miss in the baseline) was also a chunk-level miss in the baseline, but not at 100, 150 or 400 words. The other misses were: at 100 words, the cold-weather temperature and tick-borne encephalitis milk questions; at 150 words, the MERS countries and cold-weather temperature questions.
- bge-small-en-v1.5 on the baseline chunks scored Chunk-Hit@1/3/5 of 0.62, 0.86 and 0.95. The measles-risk chunk was found, and the one miss was the tick-borne encephalitis milk question (right page, answering chunk 4 not in the top 5). Chunk-Hit@1 did not change; the gain is at k=3 and k=5 (one question each, so within noise on 21 questions).
- This is still not a fully fair comparison between sizes: a longer chunk is a bigger target for the phrase, and the top 5 cover more text. The check also does not test what the LLM does with longer chunks.
- The chunk-size runs cover only the first 21 questions I marked, which were not a random sample.

**All 51 questions, both models** (200-word chunks, overlap 40; `results/chunk_check_all51_minilm.txt`, `results/chunk_check_all51_bge.txt`):

| Embedding model | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 | Missed at k=5 |
|-----------------|-------------|-------------|-------------|---------------|
| all-MiniLM-L6-v2 | 0.69 (35) | 0.88 (45) | 0.92 (47) | 4 |
| bge-small-en-v1.5 | 0.65 (33) | 0.90 (46) | 0.96 (49) | 2 |

- The counts in brackets are questions out of 51. MiniLM is ahead at k=1 by 2 questions; bge is ahead at k=3 by 1 and at k=5 by 2. The result is mixed and within a couple of questions, so it does not show that either model is better at chunk level.
- MiniLM missed at k=5: the diphtheria "wait for lab confirmation" question, the measles-risk question, the MMRV chickenpox question and the invasive Aedes south-east England question. bge missed: the diphtheria question and the tick-borne encephalitis milk question. The diphtheria question (answering chunk 0) is missed by both.
- The earlier statement that bge was equal or better on every chunk-level measure came from the first 21 questions and does not hold on all 51: MiniLM is ahead at Chunk-Hit@1.

**Chunk size on all 51 questions, both models** (overlap 20% of size; raw output: `results/chunk_check_all51_chunk100_minilm.txt`, `..._bge.txt`, the same for 150 and 400, and the 200-word files above). Each cell is Chunk-Hit@1 / @3 / @5, with misses at k=5 out of 51 in brackets:

| Chunk size (words) | Chunks | all-MiniLM-L6-v2 | bge-small-en-v1.5 |
|--------------------|--------|------------------|-------------------|
| 100 | 651 | 0.47 / 0.78 / 0.88 (6) | 0.57 / 0.76 / 0.88 (6) |
| 150 | 436 | 0.61 / 0.80 / 0.88 (6) | 0.63 / 0.88 / 0.90 (5) |
| 200 | 330 | 0.69 / 0.88 / 0.92 (4) | 0.65 / 0.90 / 0.96 (2) |
| 400 | 169 | 0.78 / 0.92 / 0.96 (2) | 0.84 / 0.96 / 1.00 (0) |

Page-level Hit@1 / @3 / @5 for bge at the other sizes (`results/retrieval_chunk100_bge.txt`, `..._chunk150_bge.txt`, `..._chunk400_bge.txt`): 100 words 0.98 / 0.98 / 1.00, 150 words 0.98 / 1.00 / 1.00, 400 words 1.00 / 1.00 / 1.00. It missed no question at k=5 at any size.

- Larger chunks scored higher at every k for both models, and the 51-question result matches the 21-question trend (MiniLM Chunk-Hit@5 0.86 at 100 and 150, 0.90 at 200 and 0.95 at 400 on the first 21; 0.88, 0.88, 0.92, 0.96 on all 51).
- bge was ahead of MiniLM at every k at 150 and 400 words. At 100 words it was ahead at k=1 (0.57 against 0.47), behind at k=3 (0.76 against 0.78) and level at k=5. At 200 words the result was mixed. Several of these gaps are one or two questions.
- bge with 400-word chunks is the strongest setup tried: no misses at k=5, Chunk-Hit@1 0.84 and page-level Hit@1 1.00. MiniLM with 400-word chunks missed the measles-risk and invasive Aedes questions.
- The 100-word runs missed the most (6 of 51 for both models). At 100 words bge missed the anthrax forms, UKHSA research centre, diphtheria lab confirmation, hantavirus death rates, tick-borne encephalitis milk and invasive Aedes questions.
- Cautions: a larger chunk is an easier target and the top 5 cover more text (about 2,000 words at 400 words per chunk, against about 500 at 100). A retrieval gain does not by itself show better answers; the LLM was run with 400-word chunks on 12 questions each with Ollama and OpenRouter, and on 32 in-scope and 6 out-of-scope questions with Ollama only (see Answer quality and Default chunk size: result below). I did not measure how many 400-word chunks exceed bge's 512-token limit (with MiniLM's tokenizer 93% exceed 256 and the median is 515 tokens). The default chunk size therefore stays at 200 words.

## Query prefix (bge)

bge's authors suggest putting `Represent this sentence for searching relevant passages: ` in front of short search questions, with the documents indexed without it. `--query-prefix` on `evaluate`, `chunk_check` and `answer_check` does this at search time, so the index needs no rebuild. The same bge index and chunks as the runs above, all 51 questions, run on 2026-11-24:

| Chunks | Page Hit@1 / 3 / 5 | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 | Missed at k=5 (chunk level) |
|--------|--------------------|-------------|-------------|-------------|-----------------------------|
| 200 words, no prefix (`results/chunk_check_all51_bge.txt`) | 0.98 / 1.00 / 1.00 | 0.65 | 0.90 | 0.96 | 2 |
| 200 words, prefix (`results/chunk_check_all51_bge_prefix.txt`) | 0.98 / 1.00 / 1.00 | 0.65 | 0.94 | 0.96 | 2 |
| 400 words, no prefix (`results/chunk_check_all51_chunk400_bge.txt`) | 1.00 / 1.00 / 1.00 | 0.84 | 0.96 | 1.00 | 0 |
| 400 words, prefix (`results/chunk_check_all51_chunk400_bge_prefix.txt`) | 1.00 / 1.00 / 1.00 | 0.88 | 0.96 | 1.00 | 0 |

- The prefix gained 2 questions at one k in each setup: Chunk-Hit@3 at 200 words (0.90 to 0.94) and Chunk-Hit@1 at 400 words (0.84 to 0.88). Nothing got worse, and page level did not change (`results/retrieval_bge_prefix.txt`, `results/retrieval_chunk400_bge_prefix.txt`).
- The two questions still missed at k=5 with 200-word chunks are the same with and without the prefix (diphtheria lab confirmation, and tick-borne encephalitis from unpasteurised milk).
- Two questions out of 51 is within noise, so this is a possible small gain and not a proven one. I did not test the prefix with the LLM, and it is off by default.

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
- Measles risk: now correct (people aged 30 and under who did not have 2 MMR doses). This is the question that was wrong with MiniLM, where the answering chunk 0 was not in the top 8 (and not in the top 5 in the chunk-level check). With bge it was in the top 5 (`results/chunk_check_bge_small.txt`), and the answer is correct, so it reached the LLM.
- Care-home outbreak: now includes the 5-day window that the MiniLM answer left out, but drops the "linked by spread" caveat that the MiniLM answer had. (SFTS was the same in substance with both: tick bite and close-contact human-to-human spread.)
- Out-of-scope: 4 of 6 refused cleanly. The COVID booster question gave the same blend as before: it applies the flu route (occupational health, pharmacy, GP) to COVID. The scabies question was refused but said the sources discuss "scabies testing procedures", and scabies appears in none of the 32 pages, so that clause is a false statement about the sources.
- This is one run per setup on 12 questions with one marker. The difference in retrieval is the likely reason for the improvement, but LLM output also varies between runs, and this was not repeated.

**Ollama with bge and 400-word chunks, same 12 questions** (`results/answer_check_ollama_bge_400.md`, run on 2026-11-24): the same questions, seed, model and bge retrieval as the previous run, but the corpus was re-chunked at 400 words (overlap 80, 169 chunks), so each prompt held three chunks of about 400 words (6,100 to 8,400 characters, inside Ollama's 4096-token context). I marked the answers by hand against the page text in `data/raw/`.
- All 6 main-set answers were correct (the same as with 200-word bge chunks, against 4 of 6 with MiniLM). The diphtheria answer was marked "partly" grounded: it adds "This increases the risk of diphtheria in this population", which the page does not state, and leaves out the co-infection point.
- Care-home outbreak: it has the "linked by spread" caveat but leaves out the 5-day onset window (the 200-word bge answer had the window but not the caveat, and MiniLM had the caveat but not the window). It says "residents", where the page says "people in your setting".
- Out-of-scope: 5 of 6 were refused cleanly. The COVID booster question no longer applied the flu booking route to COVID, which both earlier runs did, and it correctly said the NHS will contact people who may be eligible. It still did not say that no locations are given, so the "where" was left unanswered, and I marked it partial. The scabies refusal did not repeat the false "scabies testing" claim from the 200-word bge run.
- Overall, 400-word chunks with bge gave answers at least as good as the 200-word runs on these 12 questions, with small gains on two out-of-scope questions (COVID booster, scabies), a small loss on the diphtheria answer, and a swap on the care-home answer (a different one of its two parts is kept). This is one run on 12 questions with one marker and is not repeated, so it does not show that 400 words is better, only that it did not hurt.

**OpenRouter with bge, 200 words, same 12 questions** (`results/answer_check_openrouter_bge.md`, run on 2026-11-24): the same questions and seed, `baidu/ernie-5.5-flash-preview:free`, and the top 3 chunks from the bge index over the default 200-word chunks. The reply cap was raised from 400 to 1,500 tokens (`--max-tokens 1500`), and the report now records each reply's finish reason and token counts. I marked the answers by hand against the page text in `data/raw/`.
- All 12 replies finished normally (finish reason `stop`), so there were no empty or cut-off answers, against one empty and two cut-off in the first OpenRouter run. Reasoning tokens count towards the cap: they ranged from 40 to 426 per reply, and the longest reply (the care-home question) used 517 tokens in total, which is over the old 400-token cap. That fits the earlier suspicion that the cap caused the cut-offs, but this run does not prove it.
- All 6 main-set answers were correct. Measles risk was right (the first OpenRouter run said the sources did not identify the group), and the care-home answer had both the 5-day window and the "linked by spread" caveat. The diphtheria answer was marked "partly" grounded: it says such wounds are "common in this population" and that large lesions "require" treatment, where the page says poor skin integrity is often seen and large lesions need prompt assessment for antitoxin treatment. The SFTS answer gave more detail than was asked, all of it on the page.
- All 6 out-of-scope questions were refused cleanly, with no outside facts. On the COVID booster question it said no location is given, gave only the NHS-contact line, and said the flu booking route does not apply to COVID-19; neither Ollama bge run did both of these. The scabies refusal did not repeat the false "scabies testing" claim from the 200-word Ollama bge run.
- This run changed two things from the first OpenRouter run at once: the embedding model (which changes the chunks retrieved) and the reply cap. It does not show which of them helped. One run on 12 questions with one marker, not repeated.

**OpenRouter with bge, 400 words, same 12 questions** (`results/answer_check_openrouter_bge_400.md`, run on 2026-11-24): the same setup as the previous OpenRouter run (same model, questions, seed, bge retrieval and 1,500-token cap), but over 400-word chunks (overlap 80, 169 chunks), so chunk size is the only change. I marked the answers by hand against the page text in `data/raw/`. All 12 replies finished normally (finish reason `stop`). Prompts were 1,262 to 1,754 tokens, against 731 to 970 at 200 words.

| Question | OpenRouter, 200 words | OpenRouter, 400 words |
|----------|-----------------------|-----------------------|
| Measles risk | Correct | Correct |
| Care-home outbreak | Correct (5-day window and caveat) | Correct (5-day window, caveat and the single confirmed flu case) |
| Diphtheria skin wounds | Correct, "partly" grounded (two stretches) | Correct, "partly" grounded (its own inferences about infection control; leaves out co-infection) |
| Other refusals (paracetamol, measles cases, flu vaccine and egg allergy, HPV) | Clean | Clean, except the egg-allergy refusal says the sources cover Zika vaccines, and the page says there are no licensed Zika vaccines |
| COVID booster (out of scope) | Says no location is given and the flu route does not apply | Says the same, then adds signposting (household help, Age UK) that does not answer the question |
| Scabies (out of scope) | Clean | Clean |
| Main set fully correct | 6 of 6 | 6 of 6 |
| Out-of-scope refused | 6 of 6 | 6 of 6 |

- The counts are the same at both sizes, and the differences are small and mixed. At 400 words there was one false statement about the sources (Zika vaccines) and extra signposting on the COVID booster question; the one addition that was correct was the single confirmed flu case on the care-home question.
- Replies were longer at 400 words in places. The diphtheria answer used 1,084 completion tokens (927 of them reasoning), against 370 at 200 words, which is far over the old 400-token cap but inside 1,500. I did not run it at 400 tokens.
- One run per setup on 12 questions with one marker, not repeated, so it does not show that either size is better.

**Three runs side by side** (same 12 questions, seed, Ollama model and top 3 chunks; the first run used MiniLM retrieval, the other two bge; `results/answer_check_ollama.md`, `results/answer_check_ollama_bge.md`, `results/answer_check_ollama_bge_400.md`). The questions where the runs differ:

| Question | MiniLM, 200 words | bge, 200 words | bge, 400 words |
|----------|-------------------|----------------|----------------|
| Measles risk | Wrong (answering chunk not retrieved) | Correct | Correct |
| Care-home outbreak | Partly (has the "linked by spread" caveat, no 5-day window) | Correct (5-day window, no caveat) | Correct (caveat, no 5-day window) |
| Diphtheria skin wounds | Correct | Correct | Correct, but one sentence not on the page (marked "partly" grounded) |
| COVID booster (out of scope) | Partly refused; applied the flu route | Not refused; applied the flu route | Partial; no flu route, but did not say locations are not given |
| Scabies (out of scope) | Clean refusal | Refusal that falsely said the sources discuss scabies testing | Clean refusal |
| Main set fully correct | 4 of 6 | 6 of 6 | 6 of 6 |
| Out-of-scope refused cleanly | 5 of 6 | 4 of 6 | 5 of 6 |

The gap between MiniLM and bge on the main set comes from the model, since MiniLM was not run at 400 words. The two bge runs isolate chunk size, and there 400 words did not hurt. One run per setup, 12 questions, one marker.

**OpenRouter with bge, same 32 + 6 questions** (`results/answer_check_openrouter_bge_32.md`, run on 2026-11-25; the two Ollama columns come from the runs described under "Default chunk size: decision rule" and "result" below): the same questions and seed as the two Ollama 32-question reports, with the free OpenRouter model, 200-word chunks and a 1,500-token cap. I marked the answers by hand against the page text in `data/raw/`. All 38 replies finished with reason `stop` (the longest used 599 completion tokens).

| | Ollama, 200 words | Ollama, 400 words | OpenRouter, 200 words |
|---|---|---|---|
| In-scope answers marked correct (of 32) | 31 | 30 (2 partly) | 31 |
| Out-of-scope refused cleanly (of 6) | 4 | 5 | 6 |

OpenRouter had 1 in-scope answer marked wrong (the cold-weather temperature question, which says no temperature is given although the page gives prolonged periods below 2 degrees C as an example; Ollama at 200 words was marked wrong on the same question), and one marked only partly grounded (the plague question: it gave only the respiratory route and applied the page's close-contact point about pneumonic plague patients to infected cats). All 32 citations were marked as pointing to the right source. On the out-of-scope questions it refused all 6, including the COVID booster question that neither Ollama run refused (it said no location is given and that the booking options in the source apply to flu). Its answers were often longer than needed (the Zika, diphtheria skin wound and SFTS answers in particular), which I marked down in notes but not as errors. This is one run per backend with one marker, so it shows the OpenRouter model was at least as good as Ollama here, not that it is better.

## Default chunk size: decision rule

Written on 2026-11-24, before the 32-question runs (`results/answer_check_ollama_bge_32.md` at 200 words and `results/answer_check_ollama_bge_400_32.md` at 400 words) were read or marked. Both use Ollama (`qwen2.5:7b`), bge retrieval, seed 0 and the top 3 chunks, over 32 in-scope questions (one per page, because `answer_check` picks at most one question per source page, so `--sample 51` gives 32) and the 6 out-of-scope questions. I mark the answers by hand.

- Switch the default to 400-word chunks only if the 400-word run has at least 3 more in-scope answers marked correct than the 200-word run (out of 32), and no more out-of-scope questions that were not refused cleanly (out of 6; a question counts as not refused cleanly if I mark it as not saying the sources lack the answer, or as adding facts from outside the sources).
- Otherwise the default stays at 200 words, and this section records the result.

## Default chunk size: result

Marked by hand on 2026-11-25 (`results/answer_check_ollama_bge_32.md` at 200 words, `results/answer_check_ollama_bge_400_32.md` at 400 words). Counts:

| | 200 words | 400 words |
|---|---|---|
| In-scope answers marked correct (of 32) | 31 | 30 (2 marked partly) |
| Out-of-scope refused cleanly (of 6) | 4 | 5 |

The 400-word run had 1 fewer correct in-scope answer, not the 3 more the rule requires, so the default stays at 200 words. Differences were small and mixed. At 200 words, the temperature question (cold-weather risk) was marked wrong because the answer said the page gives no temperature although it gives prolonged periods below 2 degrees C as an example. At 400 words the same question was marked partly, since the answer said no exact temperature was given and then quoted the 2 degrees C example. The Zika-in-pregnancy question was marked partly at 400 words because it opened with advice on delaying pregnancy that does not suit someone who may already be pregnant. On the out-of-scope questions, the COVID booster question was not refused at either size (the 200-word answer applied the flu booking route, the 400-word one gave advice for managerial and patient-facing staff), and the scabies question was refused at 200 words with a false claim that the sources discuss scabies testing, but cleanly at 400 words. A one-question difference on one run with one marker is within noise, so this shows no benefit from 400-word chunks with Ollama and no harm either.

## Chunk overlap: decision rule

Written on 2026-11-25, before any overlap run. The chunk size stays at 200 words, with bge-small-en-v1.5, no query prefix, and the same 51 questions. I will build one chunks file and index per overlap (0, 20 and 80 words; `python -m ragdemo.ingest --size 200 --overlap N --out data/chunks_ovN.jsonl`, then `python -m ragdemo.index --chunks ... --index data/index_ovN.faiss`), and run `evaluate` and `chunk_check` on each. The current setting, overlap 40 (330 chunks, `results/retrieval_bge_small.txt` and `results/chunk_check_all51_bge.txt`: Chunk-Hit@3 0.90, which is 46 of 51), is the control and is re-run with the same code for the comparison.

- Change the default overlap only if one setting gets Chunk-Hit@3 at least 3 questions higher than overlap 40 (so 49 or more of 51), and its page-level Hit@3 is not lower. A question whose answer phrase is found in no chunk counts as a miss, so a setting cannot win by dropping hard questions.
- Otherwise the default stays at 40, and the result is recorded here.
- Chunk-Hit@3 is the deciding number because the app sends the top 3 chunks to the LLM. Other k values and the chunk counts are reported but do not decide.

## Chunk overlap: result

Run on 2026-11-25 under the rule above (200-word chunks, bge-small-en-v1.5, no query prefix, 51 questions; raw output in `results/retrieval_overlap{0,20,40,80}_bge.txt` and `results/chunk_check_all51_overlap{0,20,40,80}_bge.txt`):

| Overlap | Chunks | Hit@1 / @3 / @5 | Chunk-Hit@1 / @3 / @5 | Answer phrase in no chunk | Chunk-Hit@3 as a count |
|---|---|---|---|---|---|
| 0 | 271 | 0.98 / 1.00 / 1.00 | 0.67 / 0.94 / 0.98 (of 49 checked) | 2 | 46 of 51 (misses counted) |
| 20 | 297 | 1.00 / 1.00 / 1.00 | 0.65 / 0.90 / 1.00 | 0 | 46 of 51 |
| 40 (control, current default) | 330 | 0.98 / 1.00 / 1.00 | 0.65 / 0.90 / 0.96 | 0 | 46 of 51 |
| 80 | 421 | 0.94 / 1.00 / 1.00 | 0.63 / 0.90 / 0.94 | 0 | 46 of 51 |

No setting reached the 49 of 51 the rule requires, so the default overlap stays at 40. At Chunk-Hit@3, the number that decides, all four settings are the same. The differences are at other k: overlap 20 was slightly ahead at k=5 (1.00 against 0.96, two questions: the diphtheria lab-confirmation question and the tick-borne encephalitis milk question) and at page-level Hit@1 (1.00 against 0.98, one question), and was not worse on any metric. That is one to two questions out of 51, chosen after comparing four settings on six metrics, so I treat it as a candidate and not a finding, and I did not change the rule after seeing it. Overlap 0 left the answer phrase in no chunk for 2 of 51 questions (both on the Zika page, where the phrase falls across a chunk boundary), which is the case overlap protects against. Overlap 80 was the weakest at k=1 and k=5.

Overlap does not change the prompt size: the chunk length stays near 200 words and the app sends the top 3. Measured over the 51 questions, the mean prompt was 4,219 characters at overlap 20 and 4,228 at overlap 40. Overlap 20 only gives about 10% fewer chunks to embed and store (297 against 330).

## Hybrid search: decision rule

Written on 2026-11-25, before any hybrid code or run. Hybrid search here means: score every chunk with BM25 (keyword match; k1 1.5, b 0.75; text lower-cased and split into word tokens with the regular expression `\w+`; no stop-word list or stemming), take the top 20 chunks from BM25 and the top 20 from the dense (bge) search, and merge the two lists with reciprocal rank fusion (score is the sum of 1 / (60 + rank) over the lists a chunk appears in), returning the top k. These settings are fixed now and will not be tuned, so there is one hybrid setup and not a search over many. The comparison uses 200-word chunks with overlap 40, bge-small-en-v1.5, no query prefix and the same 51 questions as `evaluate` and `chunk_check`. The control is dense-only retrieval re-run with the same code (expected: page Hit@3 1.00 and Chunk-Hit@3 46 of 51, as in `results/chunk_check_all51_overlap40_bge.txt`). BM25 on its own is also run for reference and does not decide anything.

- Make hybrid the default only if its Chunk-Hit@3 is at least 3 questions higher than the control (49 or more of 51; the app sends the top 3 chunks to the LLM), and neither its page-level Hit@3 nor its Chunk-Hit@1 is lower than the control's.
- Otherwise hybrid stays an option that is off by default, and the result is recorded here either way.
- If hybrid wins by this rule, the next step is the 32 + 6 question answer check with Ollama, which is not part of this rule.

## Hybrid search: result

Run on 2026-11-25 under the rule above (200-word chunks, overlap 40, bge-small-en-v1.5, no query prefix, 51 questions; raw output in `results/retrieval_hybrid_{dense,bm25,hybrid}.txt` and `results/chunk_check_all51_hybrid_{dense,bm25,hybrid}.txt`). The dense control reproduced the earlier overlap-40 numbers exactly.

| Mode | Hit@1 / @3 / @5 (page) | Chunk-Hit@1 | Chunk-Hit@3 | Chunk-Hit@5 | Answering chunk missed at k=5 |
|---|---|---|---|---|---|
| Dense only (control) | 0.98 / 1.00 / 1.00 | 0.65 (33 of 51) | 0.90 (46 of 51) | 0.96 | 2 |
| BM25 only (reference) | 0.88 / 1.00 / 1.00 | 0.69 (35 of 51) | 0.94 (48 of 51) | 0.96 | 2 |
| Hybrid | 1.00 / 1.00 / 1.00 | 0.86 (44 of 51) | 0.92 (47 of 51) | 0.96 | 2 |

The rule required Chunk-Hit@3 of at least 49 of 51 for hybrid, and it got 47 (one question above the control), so hybrid stays an option that is off by default (`--mode hybrid`) and the app is unchanged. Page-level Hit@3 and Chunk-Hit@1 were not lower, so those conditions were met. The clear difference is at k=1: hybrid had the answering chunk first for 11 more questions than dense (44 against 33 of 51). The app sends the top 3 chunks, and by k=3 the gap is 1 question, so I read this as a better ordering but not a better answer set for the LLM. At k=5 all three modes are at 0.96. BM25 alone scored higher than hybrid at k=3 (48 of 51). The eval questions were written by hand while reading the pages, so they share wording with the pages, which favours keyword matching; a question set written by someone who had not read the pages could give a different picture, and I did not test one. This is a single run on one question set, with the hybrid settings fixed beforehand and not tuned. Implementation detail not in the rule: each distinct query word counts once in the BM25 score. The scores shown by the app for hybrid would be fused rank scores, not cosine similarities, which is another reason it is not wired into the app.

## Failure analysis

Baseline run (`results/retrieval_baseline.txt`): 1 of 51 questions missed at k=5. The question about the combined measles, mumps, rubella and chickenpox jab from 2026 expected `universal-varicella-vaccination-programme-in-england.txt`, but 4 of the top 5 chunks came from `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` and one from `pertussis-clinical-and-public-health-management.txt`. The reason has not been investigated.

**Answer-quality finding: right page retrieved, wrong chunk (measles risk question).** In the manual answer check (`results/answer_check_ollama.md`, `results/answer_check_openrouter.md`), the question "Who is most at risk of catching measles at the moment?" was a Hit@k success, because the expected page `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` was retrieved. Both models still answered it wrongly. They named vulnerable close contacts (immunosuppressed people, pregnant women, children under 1), which the page says to protect, instead of people aged 30 and under who did not have 2 MMR doses, which the page gives as the group most at risk. The sentence that answers the question is only in chunk 0 of that page. Retrieval for this question returned chunks 2, 5, 6, 7 and 4 of the page in ranks 1 to 5, and chunk 0 was not in the top 8. The LLM therefore never saw the answer, so this is a retrieval failure, not a generation failure. Likely cause (not tested): chunk 0 is a 200-word introduction on several topics, so the sentence is a small part of its embedding. Chunks 5 and 6 also overlap heavily, so two of the three chunks sent to the LLM (k=3) were near-duplicates. Hit@k is measured at page level and cannot see this kind of failure. No change has been made to chunking or k, because a change tuned to one question could hurt others.

## Conclusions

Retrieval found the right page within the top 5 for 50 of 51 questions (Hit@1 0.90, Hit@3 and Hit@5 0.98). The one miss was the MMRV chickenpox question, whose page was crowded out by the MMR catch-up page. Hit@k is measured at page level and hides a second kind of failure: for the measles-risk question the right page was retrieved but the chunk holding the answer was not, so one model answered wrongly and the other correctly said the sources did not say.

In the manual spot check, both LLMs stayed within the sources and refused most out-of-scope questions cleanly. The one exception was the COVID booster boundary question, where Ollama blended flu and COVID guidance (the OpenRouter call for that question failed). Ollama (`qwen2.5:7b`) was concise and completed all 12 questions but answered the measles question confidently and wrongly. The OpenRouter free model was more careful but less reliable in its first run (one empty answer, two cut-off answers, 400-token cap). A later run with bge retrieval and a 1,500-token cap finished all 12 questions normally, with all 6 main-set answers and all 6 refusals marked correct, but it changed two things at once and was a single run. On the larger 32 in-scope and 6 out-of-scope check at 200 words, OpenRouter had 31 of 32 in-scope answers correct and refused all 6 out-of-scope questions cleanly, against 31 and 4 for Ollama (30 and 5 at 400 words); one run each, one marker, so it shows OpenRouter was at least as good here, not better. The OpenRouter 32 + 6 check at 400 words was not run. With one reviewer and these sample sizes, these are observations, not measured accuracy.

Chunk sizes of 100, 150 and 400 words all matched or slightly beat the baseline at every k and found the baseline's one miss, but the gains are one or two questions out of 51, and the heavily truncated 400-word chunks scored as well as the best smaller setup. Page-level Hit@k therefore does not separate these setups. Changing the embedding model helped more than changing chunk size at page level: bge-small-en-v1.5 scored Hit@1/3/5 of 0.98, 1.00 and 1.00, with no misses. A chunk-level check on 21 hand-marked questions did separate them (see above): Chunk-Hit@5 rose with chunk size, from 0.86 at 100 and 150 words to 0.95 at 400, and the measles-risk chunk was missed at every size. With phrases for all 51 questions, the two embedding models were compared at chunk level: bge was behind by 2 questions at k=1 and ahead by 1 at k=3 and 2 at k=5, a mixed result within noise. Repeated on all 51 questions with both models, larger chunks again did better at chunk level, and bge with 400-word chunks missed nothing at k=5. The two LLM answer checks with 400-word chunks and bge (Ollama and OpenRouter, 12 questions each) gave answers at least as good as the 200-word runs with Ollama and about the same with OpenRouter (6 of 6 main-set answers and 6 of 6 refusals at both sizes, with small slips in both directions), so they show no clear gain from larger chunks. The larger Ollama check (32 in-scope and 6 out-of-scope questions) then followed the decision rule above: 31 correct at 200 words against 30 at 400, and 4 against 5 clean refusals, so the default stays at 200 words. I then tested overlap (0, 20, 40 and 80 words) under a rule written first: no setting beat overlap 40 at Chunk-Hit@3, so it stays at 40 (overlap 20 was slightly ahead at k=5 only; see Chunk overlap: result). bge's query prefix was tried and gave a small chunk-level gain (2 questions at one k, within noise; see Query prefix above), so it stays off by default. Last, I added BM25 and hybrid (BM25 + dense, reciprocal rank fusion) search as an opt-in mode under a rule written first: hybrid put the answering chunk first for many more questions (Chunk-Hit@1 44 against 33 of 51) but reached only 47 of 51 at Chunk-Hit@3 where the rule needed 49 (dense scored 46), so dense stays the default (see Hybrid search: result).
