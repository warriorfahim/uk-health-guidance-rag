# Answer check, run on 2026-11-17

Top 3 chunks per question. Backend: see LLM_BACKEND (default ollama). Sample seed: 0. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

The sources identify vulnerable close contacts as the group most needing protection from measles: immunosuppressed

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`

**Answer:**

Andes virus (ANDV) is treated as an airborne high consequence infectious disease in the UK because it can spread from person-to-person [1].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`

**Answer:**

The SFTS virus (SFTSV) was first isolated from human blood in 2009 in China [3].

Transmission:

- Tick bites are the usual route to humans, with the Asian long-horned tick (Haemaphysalis longicornis) as the primary vector [2]. Sheep, goats and other mammals may act as intermediate hosts, and animals including rodents, small mammals and yaks can be infected naturally; humans are accidental hosts when bitten by infected ticks [1][2].
- Human-to-human transmission is rare but documented, and requires close contact with an infected individual, their blood or other body fluids, or their immediate environment [1][2][3].
- Nosocomial transmission has been reported in emergency departments and intensive care units in China and South Korea, and transmission via percutaneous exposure such as a needle-stick injury has also been reported [1].
- Transmission via aerosol-generating procedures without sufficient respiratory protective equipment has been proposed as a possibility [1].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`

**Answer:**

ERROR from LLM: OpenRouter returned HTTP 429 (rate limited; try again shortly)

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`

**Answer:**

ERROR from LLM: OpenRouter returned HTTP 429 (rate limited; try again shortly)

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

ERROR from LLM: OpenRouter returned HTTP 429 (rate limited; try again shortly)

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 7. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered by any page; model should say sources don't contain the answer
- Retrieved: [1] `pertussis-clinical-and-public-health-management.txt`, [2] `pertussis-clinical-and-public-health-management.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

ERROR from LLM: OpenRouter returned HTTP 429 (rate limited; try again shortly)

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 8. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `plague-epidemiology-outbreaks-and-guidance.txt`

**Answer:**

I cannot answer this from the provided guidance. Source [2] covers measles case management and advice (isolating patients, excluding them from settings, protecting vulnerable contacts with MMR or HNIG), but it does not contain any statistics on the number of measles cases in England last year.

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 9. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine not covered
- Retrieved: [1] `pertussis-clinical-and-public-health-management.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

I cannot answer this question from the provided sources. The available sources cover pertussis (whooping cough) [1], diphtheria [2], and mosquito-borne diseases including dengue, Zika, and chikungunya [3]. None of them contain information about the flu vaccine or its safety for people with egg allergy.

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 10. What are the symptoms of dengue fever?

- Type: out-of-scope
- Note: Dengue only mentioned in passing
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

Symptoms of dengue can include fever, headache, muscle aches, joint pains, nausea and vomiting, and rash [1]. A high proportion of infections are asymptomatic, and disease is usually mild and self-limiting [1].

Severe disease, also known as dengue haemorrhagic fever / dengue shock syndrome, occurs in up to 5% of those who have symptoms [2].

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 11. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Not covered
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`

**Answer:**

The provided sources do not specifically address where to get a COVID-19 booster this winter.

The closest relevant information is in source [1], which states that for COVID-19, "the NHS will contact you if your records suggest you may be eligible for vaccination" [1]. However, this refers to COVID-19 vaccination eligibility generally and does not specify a location or service for getting a booster.

Note that source

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 12. Does Zika spread through sexual contact and for how long afterwards should couples use condoms?

- Type: out-of-scope
- Note: Partly covered; check whether the model overreaches
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`

**Answer:**

Yes, Zika can spread through sexual contact. Globally, cases of sexually transmitted Zika virus infection have been reported, with most cases involving male-to-female spread, though male-to-male and female-to-male transmission have also been reported as a very rare occurrence, and there is a potential risk of female-to-female transmission [3].

For couples planning pregnancy, the recommended duration of condom (barrier method) use depends on who travelled [2]:
- Both partners travelled: for 3 months after return or after last possible Zika virus exposure
- Male partner travelled only: for 3 months after return or after last possible Zika virus exposure
- Female partner travelled only: for 2 months after return or after last possible Zika virus exposure

These measures should be used even in the absence of symptoms while travelling [2].

For pregnant women and their sexual partners, barrier

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:
