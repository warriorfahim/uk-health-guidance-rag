# Answer check, run on 2026-11-24

Top 3 chunks per question. Backend: openrouter (baidu/ernie-5.5-flash-preview:free). Sample seed: 0. Replies are capped at 1500 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

Setup: bge-small-en-v1.5 retrieval over the default 200-word chunks; reply cap raised to 1,500 tokens. Same 12 questions as the other answer checks.

Marking: marked by the author against the page text in `data/raw/`.

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 820, completion 109, reasoning 54

**Answer:**

People aged 30 and under who did not receive 2 doses of MMR vaccine as children are most at risk of catching measles now [2]. By contrast, measles is very unlikely in people who are fully immunised or who have had measles in the past [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page: aged 30 and under without 2 MMR doses.

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`
- Finish reason: stop
- Tokens: prompt 895, completion 129, reasoning 91

**Answer:**

Andes virus (ANDV) is classified as an airborne high consequence infectious disease (HCID) in the UK because it has shown potential to spread from person-to-person [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Andes virus (ANDV), as the page states.

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`
- Finish reason: stop
- Tokens: prompt 970, completion 392, reasoning 173

**Answer:**

The SFTS virus (SFTSV) was first isolated from human blood in 2009 in China [1].

Transmission:
- It is a tick-borne zoonosis, with infections usually passing to humans through the bite of a tick carrying SFTSV [1][2]. The primary vector is the Asian long-horned tick, *Haemaphysalis longicornis* [2].
- Sheep, goats and other mammals may serve as intermediate hosts, and many animals (rodents, small mammals, yaks) can be infected naturally; humans are accidental hosts when bitten by infected ticks [2].
- Rare human-to-human transmission is clearly documented and requires close contact with an infected individual, their blood or other body fluids, or their immediate environment [1][2].
- Nosocomial transmission has occurred in emergency departments and intensive care units in China and South Korea, and transmission via percutaneous exposure (e.g. needle-stick injury) has been reported [3]. Aerosol-generating procedures without sufficient respiratory protective equipment have been proposed as a possible route [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: 2009, China, tick bite; also covers rare human-to-human spread. More detail than asked, all found on the page.

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 892, completion 72, reasoning 40

**Answer:**

The UK's last case of domestically acquired polio infection was in 1984 [1][2]. All cases since then have been acquired abroad [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: 1984, as the page states.

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`
- Finish reason: stop
- Tokens: prompt 814, completion 517, reasoning 426

**Answer:**

You need to report a respiratory outbreak when there are **2 or more people in the setting with symptoms that started within 5 days of each other** [1].

This counts as an outbreak only if the cases **could be linked by spread within your setting** [2][3]. If the infection could not have been spread in your setting, you should not report it as an outbreak; if in doubt, report it as an outbreak [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Has both the 5-day window and the 'linked by spread' caveat.

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 874, completion 370, reasoning 128

**Answer:**

Chronic (long-standing) wounds matter because *C. diphtheriae* has been found to colonise or infect them, and many migrants arrive after long journeys with poor skin integrity, making such wounds common in this population [1]. These wounds are often co-infected with other organisms such as Group A Streptococcus or *Staphylococcus aureus* [1].

This is clinically relevant for several reasons:

- Cutaneous diphtheria is a recognised presentation, and the most common presentation in the 2022+ outbreak among migrants arriving by small boats was cutaneous, though respiratory cases including classical membranous disease also occurred [1][3].
- Transmission can occur by direct contact with cutaneous lesions or infected secretions, not only by droplet spread [2].
- Testing should include skin swabs of wounds and lesions where present, alongside nose and throat swabs, taken before antibiotics are started [2].
- Suspected cases with large cutaneous lesions (greater than 2 cubic centimetres) fall within the group requiring treatment in line with national guidance [2].
- All cases, respiratory and cutaneous, are notifiable on clinical suspicion, so a suspected case warrants contacting the local UKHSA health protection team [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Main point correct, including co-infection. Two stretches: the page does not say such wounds are 'common in this population' (it says poor skin integrity is often seen), and it says large cutaneous lesions need prompt assessment for antitoxin treatment, not that they require treatment. Longer than needed.

### 7. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 842, completion 129, reasoning 74

**Answer:**

I cannot answer this from the provided guidance. The sources discuss the MMR catch-up programme, measles vaccination schedules, travel vaccination advice, and infection control measures [1][2][3], but none of them contain any information about paracetamol or its recommended adult dose.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 8. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 920, completion 128, reasoning 69

**Answer:**

I cannot answer this from the provided guidance. The sources cover diphtheria epidemiology and vaccination status of new arrivals [1], and invasive Aedes mosquito surveillance with dengue, chikungunya, and Zika data [2][3] — none of them report measles case numbers for England.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 9. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 934, completion 200, reasoning 116

**Answer:**

I cannot answer this question from the provided guidance. None of the sources discuss the flu vaccine or egg allergy. The sources cover chikungunya virus serology and Aedes albopictus mosquito suitability [1], inadvertent vaccination in pregnancy for MMR, MMRV, chickenpox, and shingles vaccines [2], and dengue and chikungunya vaccines [3], but none address influenza vaccination or egg allergies.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 10. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `vaccination-in-pregnancy-vip.txt`
- Finish reason: stop
- Tokens: prompt 879, completion 146, reasoning 85

**Answer:**

I cannot answer this question from the provided sources. The sources cover the varicella vaccination programme in England [1] and inadvertent vaccination in pregnancy (covering MMR, MMRV, chickenpox, and shingles vaccines) [2][3]. None of them mention the HPV vaccine or its side effects.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 11. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `vaccination-in-pregnancy-vip.txt`
- Finish reason: stop
- Tokens: prompt 731, completion 374, reasoning 276

**Answer:**

The provided sources do not specifically address where to get a COVID-19 booster. The closest relevant information is that for COVID-19, the NHS will contact you if your records suggest you may be eligible for vaccination [1]. However, the sources do not specify a location or method for obtaining a COVID-19 booster specifically.

Note that the guidance about booking through your employer's occupational health service, a pharmacy, or your GP applies to flu vaccination, not COVID-19 [1].

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Says no location is given, gives only the NHS contact line, and says the flu booking route does not apply to COVID-19.

### 12. How long should someone with scabies stay off work?

- Type: out-of-scope
- Note: Scabies not mentioned in any page
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 791, completion 156, reasoning 64

**Answer:**

I cannot answer this from the provided guidance. The sources cover measles/MMR case management and advice [1][3] and Zika virus advice for returning travellers [2]; none of them mention scabies or exclusion periods for work with scabies.

The only work/school exclusion guidance present relates to measles — avoiding contact with others and staying away from school or nursery for 4 days after rash onset [1] — which does not apply to scabies.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal. Calls the measles school or nursery exclusion 'work/school', but says it does not apply to scabies.
