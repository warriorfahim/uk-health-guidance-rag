# Answer check, run on 2026-11-24

Top 3 chunks per question. Backend: openrouter (baidu/ernie-5.5-flash-preview:free). Sample seed: 0. Replies are capped at 1500 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

Setup: bge-small-en-v1.5 retrieval over 400-word chunks (overlap 80, 169 chunks); reply cap 1,500 tokens. Same 12 questions as the other answer checks.

Marking: marked by the author against the page text in `data/raw/`.

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 1490, completion 109, reasoning 54

**Answer:**

People aged 30 and under who did not receive 2 doses of MMR vaccine as children are most at risk of catching measles now [1]. By contrast, measles is very unlikely in people who are fully immunised or who have had measles in the past [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page: aged 30 and under without 2 MMR doses.

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`
- Finish reason: stop
- Tokens: prompt 1493, completion 113, reasoning 70

**Answer:**

Andes virus (ANDV) is the hantavirus classified as an airborne high consequence infectious disease (HCID) in the UK, because it has shown potential to spread from person-to-person [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Andes virus (ANDV), as the page states.

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `hantaviruses.txt`
- Finish reason: stop
- Tokens: prompt 1754, completion 418, reasoning 177

**Answer:**

The SFTS virus (SFTSV) was first isolated from human blood in 2009 in China [1].

Spread:
- It is a tick-borne zoonosis, with infections usually passing to humans through the bite of a tick carrying SFTSV [1]. The primary vector is the Asian long-horned tick, *Haemaphysalis longicornis* [1].
- Sheep, goats and other mammals may serve as intermediate hosts, and many animals (rodents, small mammals, yaks) can be naturally infected; humans are accidental hosts when bitten by infected ticks [1][2].
- Most human infections occur in people exposed to ticks in rural mountainous areas of Central and Eastern China [1].
- Rare human-to-human transmission is clearly documented and requires close contact with an infected individual, their blood or other body fluids, or their immediate environment [1][2].
- Nosocomial transmission has been reported in emergency departments and intensive care units in China and South Korea, and transmission via percutaneous exposure such as a needle-stick injury has also been reported [1][2].
- Transmission via aerosol-generating procedures without sufficient respiratory protective equipment has been proposed [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: 2009, China, tick bite and rare human-to-human spread. More detail than asked, all found on the page.

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 1636, completion 78, reasoning 48

**Answer:**

The UK's last case of domestically acquired polio infection was in 1984 [1]. All cases since then have been acquired abroad [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: 1984, as the page states.

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`
- Finish reason: stop
- Tokens: prompt 1262, completion 197, reasoning 69

**Answer:**

Two or more people in your setting with symptoms that started within 5 days of each other counts as a new outbreak of acute respiratory infection (ARI) [1]. ARIs include COVID-19, flu, RSV and other respiratory infections [1].

Two caveats:
- You only report 2 or more cases as an outbreak if they could be linked by spread within your setting; if the infection could not have been spread there, do not report it as an outbreak — but if in doubt, report it [1][2].
- Separately, a single confirmed case of flu in your setting should also be reported [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Has the 5-day window, the 'linked by spread' caveat and the single confirmed flu case.

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 1656, completion 1084, reasoning 927

**Answer:**

Chronic skin wounds are relevant because many migrants have experienced long journeys and often have poor skin integrity, and *C. diphtheriae* can colonise or infect long-standing wounds [1]. Diphtheria may present with skin lesions, and cutaneous diphtheria can appear as chronic non-healing sores or shallow ulcers [1][2]. Most cases diagnosed in England had arrived very recently and were considered to have acquired infection during their journey, making recent arrivals a relevant group for cutaneous diphtheria assessment [2]. Cutaneous lesions or infected secretions can transmit *C. diphtheriae* by direct contact, so wounds and lesions may be important for infection control [2]. If diphtheria is suspected, skin swabs of wounds and lesions should be collected [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Main point correct. Adds its own inferences about infection control and assessment of recent arrivals. Leaves out co-infection with other organisms.

### 7. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `hepatitis-c-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 1440, completion 127, reasoning 77

**Answer:**

I cannot answer this from the provided guidance. The sources cover the MMR catch-up programme and vaccination advice [1][2] and hepatitis C testing, treatment, and prevention [3], but none of them contain information about paracetamol dosing.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 8. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 1648, completion 234, reasoning 81

**Answer:**

I cannot answer this from the provided sources.

None of the three sources report measles case numbers for England. Source [3] covers clinical guidance for the MMR catch-up programme — checking vaccination history, confirming diagnosis via oral fluid testing, and managing cases and contacts — but contains no incidence or case-count data [3]. Source [1] describes varicella (chickenpox) surveillance plans, noting that varicella became notifiable in April 2025 and that case data will come from NOIDS notifications, but gives no figures [1]. Source [2] does contain case counts, but for locally acquired dengue in mainland France, Italy and Spain (579 between 2010 and publication; 304 in 2024), not measles in England [2].

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal; the dengue and varicella details it mentions are on the pages.

### 9. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 1683, completion 229, reasoning 148

**Answer:**

I cannot answer this question from the provided guidance. None of the sources discuss the flu vaccine or egg allergy. The sources cover inadvertent vaccination in pregnancy for MMR, MMRV, chickenpox, and shingles vaccines [1], and vaccines for dengue, chikungunya, and Zika virus in the context of invasive Aedes mosquitoes [2][3], but none address influenza vaccination or egg allergy.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Refusal. Its summary mentions vaccines for Zika virus, but the page says there are no licensed Zika vaccines.

### 10. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `universal-varicella-vaccination-programme-in-england.txt`
- Finish reason: stop
- Tokens: prompt 1618, completion 180, reasoning 107

**Answer:**

I cannot answer this from the provided guidance. None of the sources discuss the HPV vaccine or its side effects. The sources cover inadvertent vaccination in pregnancy for MMR, MMRV, chickenpox, and shingles vaccines [1], poliomyelitis and post-polio syndrome [2], and the universal varicella (chickenpox) vaccination programme in England [3].

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 11. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`
- Finish reason: stop
- Tokens: prompt 1515, completion 461, reasoning 258

**Answer:**

The sources don't mention COVID-19 boosters specifically, so I can only partially answer.

For COVID-19 vaccination, the guidance says the NHS will contact you if your records suggest you may be eligible for vaccination [1]. It does not give a booking route or location for COVID-19 jabs.

The booking channels it does list — your employer's occupational health service, a pharmacy, or your GP — are given for flu vaccination, and only "provided that you are eligible" [1]. Healthcare professionals in managerial or patient-facing roles are advised to get vaccinated against COVID-19 and/or flu as a preventive measure [1][2], and to offer COVID-19 and/or flu vaccinations to all those eligible [2].

For further signposting, the guidance points to the NHS England information on how to stay well in winter, the GOV.UK page on help for households, and Age UK (0800 169 6565, quoting 'WINTER') [1][2].

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Says no COVID booking route or location is given and that the booking channels are for flu. Then adds signposting (household help, Age UK) that does not answer the question.

### 12. How long should someone with scabies stay off work?

- Type: out-of-scope
- Note: Scabies not mentioned in any page
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`
- Finish reason: stop
- Tokens: prompt 1523, completion 142, reasoning 88

**Answer:**

I cannot answer this from the provided guidance. The sources cover Zika virus advice for returning travelers [1][3] and measles/MMR case management [2], but none of them mention scabies or guidance on how long someone with scabies should stay off work.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.
