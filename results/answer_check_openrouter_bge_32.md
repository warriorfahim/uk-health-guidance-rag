# Answer check, run on 2026-11-25

Top 3 chunks per question. Backend: openrouter (baidu/ernie-5.5-flash-preview:free). Sample seed: 0. Replies are capped at 1500 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

Retrieval: model BAAI/bge-small-en-v1.5, chunks data/chunks.jsonl, index data/index.faiss.

Setup: bge-small-en-v1.5 retrieval over 200-word chunks (330 chunks); OpenRouter free `baidu/ernie-5.5-flash-preview:free`, reply cap 1,500 tokens, 10 s delay between questions. 32 in-scope questions (one per source page, from `--sample 51`) and the 6 out-of-scope questions, seed 0, the same questions as the two Ollama 32-question reports.

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
- Notes: Matches the page.

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
- Notes: Matches the page.

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`
- Finish reason: stop
- Tokens: prompt 970, completion 351, reasoning 147

**Answer:**

The SFTS virus (SFTSV) was first isolated from human blood in 2009 in China [1].

Spread:
- SFTS is a tick-borne zoonosis, with rare cases of human-to-human transmission clearly documented [1].
- Infections usually pass to humans through the bite of a tick carrying SFTSV; the primary vector is the Asian long-horned tick, *Haemaphysalis longicornis* [2]. Sheep, goats and other mammals may serve as intermediate hosts, and humans are accidental hosts when bitten by infected ticks [2].
- Human-to-human transmission requires close contact with an infected individual, their blood or other body fluids, or their immediate environment [2].
- Nosocomial transmission has been reported in emergency departments and intensive care units in China and South Korea, and transmission via percutaneous exposure (for example, needle-stick injury) has also been reported [3]. Transmission via aerosol-generating procedures without sufficient respiratory protective equipment has been proposed [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page; more detail than asked.

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 892, completion 80, reasoning 47

**Answer:**

The last case of domestically acquired polio infection in the UK was in 1984 [1][2]. All cases since then have been acquired abroad [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`
- Finish reason: stop
- Tokens: prompt 814, completion 212, reasoning 82

**Answer:**

Two or more people in your setting with symptoms that started within 5 days of each other counts as a new outbreak of acute respiratory infection (ARI) that you should report [1].

Two caveats:
- The cases must be ones that could plausibly be linked by spread within your setting. If the infection could not have been spread there, you should not report it as an outbreak — but if in doubt, report it anyway [2][3].
- Separately, a single confirmed case of flu in your setting should also be reported [1].

You should not wait for test results before reporting; report as soon as possible [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Has the 5-day window, the 'linked by spread' caveat and the single confirmed flu case.

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 874, completion 371, reasoning 148

**Answer:**

Chronic (long-standing) wounds matter because *C. diphtheriae* can colonise or infect them, and many migrants arrive with poor skin integrity after long journeys, so these wounds are a plausible site of infection [1]. Cutaneous diphtheria was in fact the most common presentation in the 2022 outbreak among migrants arriving by small boats, though classical respiratory cases with a membrane also occurred [3].

This has practical consequences:
- Transmission can occur by direct contact with cutaneous lesions or infected secretions, not only by droplet spread [2].
- Wounds and lesions should be swabbed, along with nose and throat swabs, for all clinically suspected cases before antibiotics are started [2].
- Suspected cases with respiratory symptoms and/or large cutaneous lesions (greater than 2 cubic centimetres) fall within the treatment guidance [2].
- Long-standing wounds often involve co-infection with other organisms such as Group A Streptococcus or *Staphylococcus aureus* [1].
- All cases, respiratory and cutaneous, are notifiable on clinical suspicion to the local UKHSA health protection team [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Main point correct, including co-infection. Much longer than needed.

### 7. Which ticks are the main carriers of Crimean-Congo haemorrhagic fever and are they established in Britain?

- Type: in-scope
- Expected source: `crimean-congo-haemorrhagic-fever-origins-reservoirs-transmission-and-guidelines.txt` (retrieved in top 3: yes)
- Retrieved: [1] `crimean-congo-haemorrhagic-fever-origins-reservoirs-transmission-and-guidelines.txt`, [2] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [3] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`
- Finish reason: stop
- Tokens: prompt 942, completion 147, reasoning 84

**Answer:**

The principal vectors of Crimean-Congo haemorrhagic fever virus (CCHFV) are Hyalomma ticks [1]. They are not established in Britain: there are no identified established populations of Hyalomma ticks in the United Kingdom, and CCHF itself is not present in the UK [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 8. Can whooping cough be diagnosed without a laboratory test?

- Type: in-scope
- Expected source: `pertussis-clinical-and-public-health-management.txt` (retrieved in top 3: yes)
- Retrieved: [1] `pertussis-clinical-and-public-health-management.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 900, completion 213, reasoning 49

**Answer:**

Yes. Whooping cough (pertussis) is a notifiable disease in England and Wales, and a diagnosis may be made on clinical grounds without the need for laboratory confirmation [1].

Laboratory methods are available and can add confirmation — isolation of *B. pertussis* by culture confirms diagnoses, though culture lacks sensitivity, and since 2001 PCR and serological testing have been available, increasing case ascertainment (particularly serology in adults) [1]. Oral fluid testing has been available since 2013 for children aged 5 to 16 years not confirmed by other laboratory methods [1]. Note that the WHO definition of classic (severe) pertussis does include culture confirmation, alongside at least 21 days of cough illness with paroxysms, associated whoops or post-tussis vomiting [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Correct; adds more detail on laboratory methods than asked.

### 9. Which anthrax outbreak affected drug users in the UK around 2009 to 2012?

- Type: in-scope
- Expected source: `anthrax-guidance-for-testing.txt` (retrieved in top 3: yes)
- Retrieved: [1] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [2] `anthrax-guidance-for-testing.txt`, [3] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`
- Finish reason: stop
- Tokens: prompt 872, completion 97, reasoning 63

**Answer:**

The most significant UK outbreak in humans was injectional anthrax, occurring from 2009 to 2012 and associated with the use of contaminated heroin [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 10. Why is south-east England considered a place where invasive Aedes mosquitoes could survive?

- Type: in-scope
- Expected source: `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 891, completion 158, reasoning 81

**Answer:**

Temperatures in the south-east of England are high enough for invasive Aedes mosquitoes to survive [3]. Some areas of England are already considered suitable for the survival of Aedes albopictus [2], and with climate change the areas of suitability are expected to increase — including parts of Wales, the English Midlands and North West England — further raising the risk [2][3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Gives the page's reason: temperatures are high enough for the mosquitoes to survive.

### 11. Can chikungunya be confused with dengue when a patient has fever and sore joints?

- Type: in-scope
- Expected source: `chikungunya.txt` (retrieved in top 3: yes)
- Retrieved: [1] `chikungunya.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 948, completion 226, reasoning 141

**Answer:**

Yes. Chikungunya can often be misdiagnosed as other viral illnesses such as dengue fever in areas where these infections also occur [1]. This confusion is plausible because chikungunya is characterised by a sudden onset of fever usually accompanied by joint pain (arthralgia) [1], and both dengue and chikungunya infections can cause fever, muscle aches, joint pains and a rash [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 12. What survey is the main source of data on infections among people who inject drugs?

- Type: in-scope
- Expected source: `people-who-inject-drugs-infection-risks-guidance-and-data.txt` (retrieved in top 3: yes)
- Retrieved: [1] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [2] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [3] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`
- Finish reason: stop
- Tokens: prompt 832, completion 130, reasoning 60

**Answer:**

The Unlinked Anonymous Monitoring (UAM) Survey of PWID is the main source of information on the extent of infections and risks in this population [2]. It is a multi-site survey that is a collaboration between UKHSA and over 60 specialist agencies that work with PWID across England, Wales and Northern Ireland [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 13. Which animal spreads Lassa fever to people?

- Type: in-scope
- Expected source: `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt` (retrieved in top 3: yes)
- Retrieved: [1] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`, [2] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`, [3] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`
- Finish reason: stop
- Tokens: prompt 874, completion 109, reasoning 88

**Answer:**

Wild rodents, specifically *Mastomys natalensis*, spread Lassa fever to people [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 14. I have just come back from a country with Zika and I might be pregnant. What should I do?

- Type: in-scope
- Expected source: `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt` (retrieved in top 3: yes)
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`
- Finish reason: stop
- Tokens: prompt 818, completion 599, reasoning 266

**Answer:**

Based on the guidance:

**If you have no symptoms** (no fever, rash or flu-like illness within two weeks of leaving the risk country), you do not need to be tested for Zika virus infection [1]. You should:
- Inform your midwife of your travel [1]
- Avoid unprotected sex with anyone who has been to a country at risk of Zika transmission for the remainder of your pregnancy [1][3]
- Be vigilant with mosquito bite prevention [1][3]

**If you do have symptoms** — fever, rash or flu-like illness — discuss this with a healthcare professional without delay, and tell them you have recently returned from an area at risk of Zika [1]. Symptoms can resemble dengue, chikungunya, malaria, and some non-travel-related infections seen in pregnancy, so assessment matters [1].

**On the pregnancy question itself:** the guidance advises that any woman concerned after travel to a Zika area should discuss it with a healthcare professional such as a doctor or midwife, and notes the guidance is supporting information only and does not replace a face-to-face consultation [2]. If you are not yet pregnant but trying to conceive, the guidance advises avoiding pregnancy for two months after your return date if only you travelled, or three months if you travelled with your male partner or he travelled alone, using effective contraception plus barrier methods (condoms) during that period [3].

The sources do not specifically address what to do when pregnancy status is uncertain (i.e. a possible but unconfirmed pregnancy), so I cannot answer that part from the provided guidance beyond the general advice to consult a doctor or midwife [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Covers symptoms, midwife, sexual precautions and bite prevention, and says the sources do not address an unconfirmed pregnancy. Long.

### 15. Has anyone caught West Nile virus in the UK, and has it been found in British mosquitoes?

- Type: in-scope
- Expected source: `national-contingency-plan-for-west-nile-virus-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `national-contingency-plan-for-west-nile-virus-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 903, completion 169, reasoning 124

**Answer:**

According to the sources, at the time of publication there have been no human cases of West Nile virus acquired in the UK [1]. However, there have been detections of WNV in mosquitoes in the UK [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 16. Which animals are the natural hosts of Nipah virus?

- Type: in-scope
- Expected source: `nipah-virus-epidemiology-outbreaks-and-guidance.txt` (retrieved in top 3: yes)
- Retrieved: [1] `nipah-virus-epidemiology-outbreaks-and-guidance.txt`, [2] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [3] `nipah-virus-epidemiology-outbreaks-and-guidance.txt`
- Finish reason: stop
- Tokens: prompt 928, completion 179, reasoning 75

**Answer:**

Bats are the natural reservoir of Nipah virus, particularly fruit bats of the Pteropus genus [1]. NiV has been isolated from the urine of bats in Malaysia, and antibodies against NiV have been detected in 23 species of bat across Asia, Ghana and Madagascar [1][3].

Pigs are not natural hosts but were the intermediate source in the 1998 Malaysian outbreak, where bat-derived NiV spread to pigs and then to humans exposed to infected pigs' urine and respiratory secretions [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 17. Is there a vaccine or antiviral drug for Oropouche fever?

- Type: in-scope
- Expected source: `oropouche-virus-disease.txt` (retrieved in top 3: yes)
- Retrieved: [1] `oropouche-virus-disease.txt`, [2] `oropouche-virus-disease.txt`, [3] `oropouche-virus-disease.txt`
- Finish reason: stop
- Tokens: prompt 821, completion 174, reasoning 130

**Answer:**

No. There is currently no specific vaccine or antiviral treatment for Oropouche fever [1]. Management is supportive, using antipyretics, painkillers, and maintenance of fluid balance [1][3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 18. At what temperature does cold weather start to count as a health risk for vulnerable patients?

- Type: in-scope
- Expected source: `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt` (retrieved in top 3: yes)
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`
- Finish reason: stop
- Tokens: prompt 849, completion 265, reasoning 104

**Answer:**

The provided sources do not state an outdoor or ambient temperature threshold at which cold weather becomes a health risk. The only temperature figure given is the clinical definition of hypothermia: a core body temperature of less than 35°C [1][2]. That is a measure of a patient's body temperature, not an environmental trigger point.

The sources instead frame risk by population rather than by temperature — older people (65 and over), people with cardiovascular or respiratory conditions, people with mental health conditions, people with learning and/or physical disabilities, young children under 5, pregnant women, people on a low income, and people sleeping rough [1]. They also note that preparation should be planned year-round with plans agreed and distributed before 1 November each year [2], but no specific temperature trigger is provided.

- Correct? (yes/no/partly): no
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Wrong for the question: says there is no temperature threshold, but the page gives prolonged periods below 2°C as an example. That passage was probably not retrieved; the 35°C hypothermia figure is correct.

### 19. Can a pet cat pass plague to a person?

- Type: in-scope
- Expected source: `plague-epidemiology-outbreaks-and-guidance.txt` (retrieved in top 3: yes)
- Retrieved: [1] `plague-epidemiology-outbreaks-and-guidance.txt`, [2] `plague-epidemiology-outbreaks-and-guidance.txt`, [3] `plague-epidemiology-outbreaks-and-guidance.txt`
- Finish reason: stop
- Tokens: prompt 683, completion 81, reasoning 45

**Answer:**

Yes. Humans have been infected via the respiratory secretions of infected cats [1]. This route involves inhaling infectious respiratory particles, which generally requires close and prolonged contact [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Yes, but gives only the respiratory route and leaves out fleas, scratches and bites. Applies the page's 'close and prolonged contact' point about people with pneumonic plague to infected cats.

### 20. How often do sexual health clinics in England have to send their data to UKHSA for the national STI surveillance system?

- Type: in-scope
- Expected source: `gumcad-sti-surveillance-system.txt` (retrieved in top 3: yes)
- Retrieved: [1] `gumcad-sti-surveillance-system.txt`, [2] `gumcad-sti-surveillance-system.txt`, [3] `gumcad-sti-surveillance-system.txt`
- Finish reason: stop
- Tokens: prompt 830, completion 116, reasoning 74

**Answer:**

Sexual health services (SHSs) in England must report their GUMCAD data to UKHSA quarterly [3]. The data is then published quarterly as provisional data and annually as official statistics [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 21. How many people in the world are living with long-term hepatitis C and which region has the most?

- Type: in-scope
- Expected source: `hepatitis-c-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hepatitis-c-migrant-health-guide.txt`, [2] `hepatitis-c-migrant-health-guide.txt`, [3] `hepatitis-b-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 842, completion 169, reasoning 116

**Answer:**

According to the World Health Organization, an estimated 50 million people are living with chronic hepatitis C globally [2]. The region with the highest burden of disease is the Eastern Mediterranean Region, with 12 million people estimated to be living with chronic infection [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 22. What scheme should companies register with if their staff work in areas affected by Ebola or Marburg?

- Type: in-scope
- Expected source: `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt` (retrieved in top 3: yes)
- Retrieved: [1] `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt`
- Finish reason: stop
- Tokens: prompt 856, completion 90, reasoning 69

**Answer:**

Companies should register with the UK Health Security Agency (UKHSA) returning workers scheme [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 23. At what ages do children get the combined measles, mumps, rubella and chickenpox jab from 2026?

- Type: in-scope
- Expected source: `universal-varicella-vaccination-programme-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `pertussis-clinical-and-public-health-management.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 875, completion 107, reasoning 51

**Answer:**

From January 2026, eligible children in England will be offered the combined MMRV (measles, mumps, rubella and varicella/chickenpox) vaccine as a 2-dose schedule, routinely at 12 months and 18 months of age [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 24. Which age groups and health conditions make meningococcal disease more likely?

- Type: in-scope
- Expected source: `meningococcal-disease-background-information.txt` (retrieved in top 3: yes)
- Retrieved: [1] `meningococcal-disease-background-information.txt`, [2] `meningococcal-disease-background-information.txt`, [3] `meningococcal-disease-background-information.txt`
- Finish reason: stop
- Tokens: prompt 869, completion 199, reasoning 119

**Answer:**

Meningococcal disease is more common in [2]:

- babies and young children
- teenagers and young adults
- older adults
- people with a weak immune system — for example, due to HIV or chemotherapy

Anyone can catch it, but these groups are at higher risk [2]. Separately, sharing drinks or straws can increase the risk of passing on the bacteria [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 25. How long before a trip should someone visiting relatives abroad ask for travel health advice?

- Type: in-scope
- Expected source: `travel-to-visit-friends-and-relatives-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [2] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [3] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 836, completion 103, reasoning 61

**Answer:**

At least 6 to 8 weeks before their planned departure [1][2]. That said, the guidance also notes it is never too late to advise someone about a planned trip [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 26. Does a new arrival need proof of address or immigration status to register with a GP and get vaccinated?

- Type: in-scope
- Expected source: `immunisation-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `immunisation-migrant-health-guide.txt`, [2] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [3] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`
- Finish reason: stop
- Tokens: prompt 846, completion 92, reasoning 32

**Answer:**

No. Individuals do not need to provide proof of identity, address, or immigration status in order to register with a GP practice to access immunisations [1]. This also applies to asylum seekers, refugees, homeless patients, or overseas visitors, whether lawfully in the UK or not [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 27. Can you catch tick-borne encephalitis from unpasteurised milk products?

- Type: in-scope
- Expected source: `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt` (retrieved in top 3: yes)
- Retrieved: [1] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [2] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [3] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`
- Finish reason: stop
- Tokens: prompt 801, completion 81, reasoning 45

**Answer:**

Yes. Although TBE is usually transmitted to humans through the bite of an infected tick, infection can also occur through consumption of infected unpasteurised dairy products [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 28. Which laboratories must report notifiable organisms and who do they report to?

- Type: in-scope
- Expected source: `notifiable-organisms-and-how-to-report-them.txt` (retrieved in top 3: yes)
- Retrieved: [1] `notifiable-organisms-and-how-to-report-them.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `plague-epidemiology-outbreaks-and-guidance.txt`
- Finish reason: stop
- Tokens: prompt 948, completion 126, reasoning 95

**Answer:**

All laboratories in England with a primary diagnostic role must report a confirmed notifiable organism to the UK Health Security Agency (UKHSA) [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 29. Which country has reported the majority of MERS cases since 2012?

- Type: in-scope
- Expected source: `mers-cov-background-information.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mers-cov-background-information.txt`, [2] `mers-cov-background-information.txt`, [3] `mers-cov-background-information.txt`
- Finish reason: stop
- Tokens: prompt 879, completion 283, reasoning 249

**Answer:**

The Kingdom of Saudi Arabia has reported the majority of MERS cases since 2012, with approximately 84% of human cases reported by that country [3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 30. What extra care does a newborn need if the mother is living with hepatitis B?

- Type: in-scope
- Expected source: `hepatitis-b-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hepatitis-b-migrant-health-guide.txt`, [2] `hepatitis-b-migrant-health-guide.txt`, [3] `hepatitis-b-migrant-health-guide.txt`
- Finish reason: stop
- Tokens: prompt 832, completion 177, reasoning 101

**Answer:**

Babies born to mothers living with hepatitis B need vaccinations at birth and again at 4 weeks of age, in addition to the routine immunisation schedule, plus testing at 12–18 months of age [2]. More broadly, hepatitis B vaccine should be offered to all individuals at risk of infection, which explicitly includes infants born to mothers living with hepatitis B [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 31. Which UKHSA research centre works on new treatments and vaccines for drug-resistant infections?

- Type: in-scope
- Expected source: `antimicrobial-resistance-amr.txt` (retrieved in top 3: yes)
- Retrieved: [1] `antimicrobial-resistance-amr.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `antimicrobial-resistance-amr.txt`
- Finish reason: stop
- Tokens: prompt 881, completion 240, reasoning 183

**Answer:**

The Vaccine Development and Evaluation Centre (VDEC) works on new treatments and vaccines for drug-resistant infections [1]. VDEC facilitates the development and evaluation of new vaccines and therapeutics and has expertise in antimicrobial resistance, including novel antimicrobials and vaccines for AMR [1][3].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 32. A woman had a live vaccine before she knew she was pregnant. Who should the GP tell?

- Type: in-scope
- Expected source: `vaccination-in-pregnancy-vip.txt` (retrieved in top 3: yes)
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `vaccination-in-pregnancy-vip.txt`
- Finish reason: stop
- Tokens: prompt 905, completion 284, reasoning 91

**Answer:**

The GP should notify UKHSA (the UK Health Security Agency), which runs UK-wide surveillance on the safety of vaccines given in pregnancy [1][2]. This applies to MMR, MMRV, chickenpox or shingles vaccine inadvertently administered during pregnancy or shortly before conception — i.e. cases where the woman would not have been aware she was pregnant at the time [1][2].

Notification can be made either by completing the Notification form for vaccines administered in pregnancy (VIP) and returning it by email or post, or by completing the notification form online [1][2].

Consent does not need to be obtained, though it is recommended that the surveillance be discussed with the patient by the health professional reporting the case [3]. Follow-up is normally undertaken with the GP practice the woman is registered with [1]. The woman can also be reassured that there are no known risks from these vaccines at any stage of pregnancy or shortly before conception [1][2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 33. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`
- Finish reason: stop
- Tokens: prompt 842, completion 136, reasoning 79

**Answer:**

I cannot answer this from the provided guidance. The sources discuss the MMR catch-up programme, measles vaccination schedules, travel to outbreak areas, and infection control in clinics [1][2][3], but none of them contain any information about paracetamol or its recommended adult dose.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 34. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 920, completion 137, reasoning 81

**Answer:**

I cannot answer this question from the provided guidance. None of the sources mention measles or measles case numbers in England. The sources cover diphtheria [1] and invasive Aedes mosquitoes with associated diseases like dengue, chikungunya, and Zika [2][3].

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 35. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`
- Finish reason: stop
- Tokens: prompt 934, completion 197, reasoning 117

**Answer:**

I cannot answer this question from the provided sources. None of the sources discuss the flu vaccine or egg allergy. The sources cover chikungunya virus serology and Aedes albopictus suitability [1], inadvertent vaccination in pregnancy (MMR, chickenpox, shingles) [2], and dengue and chikungunya vaccines [3], but none address influenza vaccination or egg allergy.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 36. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `vaccination-in-pregnancy-vip.txt`
- Finish reason: stop
- Tokens: prompt 879, completion 168, reasoning 110

**Answer:**

I cannot answer this question from the provided guidance. The sources discuss the varicella vaccination programme [1] and inadvertent vaccination in pregnancy for MMR, MMRV, chickenpox, and shingles vaccines [2][3], but none of them mention the HPV vaccine or its side effects.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 37. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `vaccination-in-pregnancy-vip.txt`
- Finish reason: stop
- Tokens: prompt 731, completion 348, reasoning 235

**Answer:**

The provided sources do not specify where to get a COVID-19 booster this winter. Source [1] only states that for COVID-19, the NHS will contact you if your records suggest you may be eligible for vaccination [1]. It does not give a location or booking method for the COVID-19 booster specifically.

Note that the pharmacy, GP, or occupational health service booking options mentioned in [1] apply to flu vaccination, not the COVID-19 booster [1].

I cannot answer where to get a COVID-19 booster from the provided guidance.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Says no location or booking method is given, and that the booking options are for flu.

### 38. How long should someone with scabies stay off work?

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
