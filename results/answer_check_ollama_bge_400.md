# Answer check, run on 2026-11-24

Top 3 chunks per question. Backend: ollama (qwen2.5:7b). Sample seed: 0. Replies are capped at 400 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

Setup: bge-small-en-v1.5 retrieval over 400-word chunks (overlap 80, 169 chunks), so each prompt holds three 400-word chunks (prompts were 6,100 to 8,400 characters, well inside Ollama's 4096-token context). The same 12 questions as `results/answer_check_ollama.md` (MiniLM, 200-word chunks) and `results/answer_check_ollama_bge.md` (bge, 200-word chunks).

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

People aged 30 and under who did not receive 2 doses of MMR vaccine as children are most at risk of catching measles now. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page: people aged 30 and under who did not receive 2 MMR doses. All three retrieved chunks are from the MMR page, so the answering sentence reached the model with 400-word chunks too.

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`

**Answer:**

Andes virus (ANDV) is treated as an airborne high consequence infection in the UK because it can pass between people. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Andes virus (ANDV) is the airborne HCID, as the page says.

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `hantaviruses.txt`

**Answer:**

The SFTS virus was first isolated from human blood in 2009 in China [1]. It is primarily spread to humans through the bite of a tick carrying the SFTSV, with sheep, goats, and other mammals serving as intermediate hosts [1, 2]. Human-to-human transmission can occur through close contact with an infected individual, their blood or other body fluids, or their immediate environment, including nosocomial transmission in healthcare settings [1, 2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: First isolated from human blood in 2009 in China; tick bite; sheep and goats as intermediate hosts; human-to-human by close contact, including nosocomial spread. All on the page. Minor: the page says sheep and goats 'may serve' as intermediate hosts and the answer states it as fact. Chunk numbering of [1]/[2] not checked. The third retrieved chunk (hantaviruses) was not cited.

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

The UK last had a case of polio caught within the country in 1984 [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Page: last domestically acquired polio case was in 1984. The third retrieved chunk (diphtheria) was not cited.

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

You need to report 2 or more residents with symptoms of a respiratory infection as an outbreak if these infections could be linked by spread within your setting [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: '2 or more' matches the page and the caveat that the cases must be linkable by spread within the setting is included. Leaves out the 5-day onset window ('symptoms that started within 5 days of each other'). Says 'residents'; the page says 'people in your setting'.

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

Chronic skin wounds in people who have recently arrived in the UK are relevant to diphtheria because *C. diphtheriae* has been found to colonize or infect long-standing wounds, and many migrants have poor skin integrity due to long journeys prior to reaching the UK [1]. This increases the risk of diphtheria in this population.

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Core matches the page: C. diphtheriae colonises or infects long-standing wounds, and migrants often have poor skin integrity after long journeys. Leaves out the co-infection with Group A Streptococcus or Staphylococcus aureus. The last sentence ('This increases the risk of diphtheria in this population') is an inference, not stated on the page.

### 7. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `hepatitis-c-migrant-health-guide.txt`

**Answer:**

I cannot answer from the provided guidance. The sources given are related to MMR vaccination, measles infection control, and hepatitis C management and do not contain information about the recommended adult dose of paracetamol.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refuses correctly and describes the retrieved pages (MMR, measles, hepatitis C) accurately. No dose given.

### 8. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

I cannot answer from the provided guidance. The sources do not contain specific information on the number of people who caught measles in England last year.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refuses correctly; no figure given.

### 9. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

The provided sources do not contain information about the safety of the flu vaccine for people with egg allergy. Therefore, I cannot answer this question based on the given guidance. [1]

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refuses correctly. Attaches a citation [1] (vaccination in pregnancy page) to a refusal, which supports nothing.

### 10. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `universal-varicella-vaccination-programme-in-england.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources do not contain information about the side effects of the HPV vaccine.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refuses correctly.

### 11. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

For those working in managerial or patient-facing roles, if you are eligible, you can get vaccinated against COVID-19 as a preventive measure to reduce the risk of respiratory infections during winter. The NHS will contact you if your records suggest you may be eligible for vaccination. [1]

- Said the sources do not contain the answer? (yes/no): no
- Added facts from outside the sources? (yes/no): no
- Notes: Partial. Unlike the 200-word bge run, it does not apply the flu booking route (occupational health, pharmacy, GP) to COVID-19, and it correctly says the NHS will contact you if your records suggest you may be eligible. But it does not say that no booster locations are given, so the 'where' is left unanswered, and it frames the reply around managerial and patient-facing staff, which the question did not ask about.

### 12. How long should someone with scabies stay off work?

- Type: out-of-scope
- Note: Scabies not mentioned in any page
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources discuss Zika virus prevention, measles management, and MMR vaccination, but do not contain information about scabies or work restrictions related to it.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refuses correctly and describes the retrieved pages (Zika, measles, MMR) accurately. The 200-word bge run wrongly said the sources discuss scabies testing; this one does not.
