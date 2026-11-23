# Answer check, run on 2026-11-23

Top 3 chunks per question. Backend: ollama (qwen2.5:7b). Sample seed: 0. Replies are capped at 400 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

People aged 30 and under who did not receive 2 doses of MMR vaccine as children are most at risk of catching measles now. [2]

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`

**Answer:**

Andes virus (ANDV) is treated as an airborne high consequence infection in the UK because it can pass between people [2].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`

**Answer:**

The SFTS virus was first isolated from human blood in 2009 in China [1]. Infections usually pass to humans by the bite of a tick carrying SFTSV [2]. Human-to-human transmission requires close contact with an infected individual, their blood or other body fluids, or their immediate environment [2].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`

**Answer:**

The UK last had a case of polio caught within the country in 1984 [1, 2].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`

**Answer:**

You need to report 2 or more people in your setting with symptoms that started within 5 days of each other as an outbreak of acute respiratory infection (ARI) [2].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

Chronic skin wounds in people who have recently arrived in the UK are relevant to diphtheria because *C. diphtheriae* has been found to colonize or infect long-standing wounds, and there is often co-infection with other organisms such as Group A Streptococcus or Staphylococcus aureus [1].

- Correct? (yes/no/partly):
- Grounded in the sources? (yes/no):
- Citations point to the right source? (yes/no):
- Notes:

### 7. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

I cannot answer from the provided guidance. The sources focus on MMR vaccination recommendations and infection control measures but do not provide information on adult paracetamol doses.

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 8. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

I cannot answer from the provided guidance as none of the sources mention measles cases in England. The sources discuss diphtheria cases, invasive mosquitoes, and general surveillance practices but do not provide information on measles cases. [1] [2] [3]

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 9. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

The provided sources do not contain information about the safety of the flu vaccine for people with egg allergy. Therefore, I cannot answer the question based on the given guidance. [1] [2] [3]

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 10. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `vaccination-in-pregnancy-vip.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources do not contain information about the side effects of the HPV vaccine.

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 11. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `vaccination-in-pregnancy-vip.txt`

**Answer:**

You can get a COVID-19 booster this winter by checking whether you are eligible for vaccination and booking an appointment with your employer's occupational health service, your pharmacy, or your GP. The NHS will contact you if your records suggest you may be eligible for vaccination. [1]

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:

### 12. How long should someone with scabies stay off work?

- Type: out-of-scope
- Note: Scabies not mentioned in any page
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources discuss measles, Zika virus, and scabies testing procedures but do not provide information on how long someone with scabies should stay off work.

- Said the sources do not contain the answer? (yes/no):
- Added facts from outside the sources? (yes/no):
- Notes:
