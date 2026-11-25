# Answer check, run on 2026-11-25

Top 3 chunks per question. Backend: ollama (qwen2.5:7b). Sample seed: 0. Replies are capped at 400 tokens, so long answers may be cut off. If an answer starts with 'No LLM available', the backend was not running and this is only the grounded prompt.

Retrieval: model BAAI/bge-small-en-v1.5, chunks data/chunks_400.jsonl, index data/index_400.faiss.

Setup: bge-small-en-v1.5 retrieval over 400-word chunks (overlap 80, 169 chunks); Ollama `qwen2.5:7b`, reply cap 400 tokens. 32 in-scope questions (one per source page, from `--sample 51`) and the 6 out-of-scope questions, seed 0, the same questions in both reports.

Marking: marked by the author against the page text in `data/raw/`.

### 1. Who is most at risk of catching measles at the moment?

- Type: in-scope
- Expected source: `mmr-catchup-programme-diagnosis-case-management-and-advice.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

People aged 30 and under who did not receive 2 doses of MMR vaccine as children are most at risk of catching measles now. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page: aged 30 and under without 2 MMR doses.

### 2. Which hantavirus is treated as an airborne high consequence infection in the UK because it can pass between people?

- Type: in-scope
- Expected source: `hantaviruses.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hantaviruses.txt`, [2] `hantaviruses.txt`, [3] `hantaviruses.txt`

**Answer:**

The Andes virus (ANDV) is treated as an airborne high consequence infection in the UK because it can pass between people. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 3. Where was the SFTS virus first found and how does it spread?

- Type: in-scope
- Expected source: `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt` (retrieved in top 3: yes)
- Retrieved: [1] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [2] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`, [3] `hantaviruses.txt`

**Answer:**

The SFTS virus was first isolated from human blood in 2009 in China [1]. It is primarily spread to humans through the bite of a tick carrying the SFTSV, with sheep, goats, and other mammals serving as intermediate hosts [1, 2]. Human-to-human transmission can occur through close contact with an infected individual, their blood or other body fluids, or their immediate environment, including nosocomial transmission in healthcare settings [1, 2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page, except that it states sheep, goats and other mammals are intermediate hosts where the page says they may be.

### 4. When did the UK last have a case of polio caught within the country?

- Type: in-scope
- Expected source: `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

The UK last had a case of polio caught within the country in 1984 [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 5. How many sick residents in a care home count as a respiratory outbreak that I need to report?

- Type: in-scope
- Expected source: `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt` (retrieved in top 3: yes)
- Retrieved: [1] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [2] `report-an-outbreak-of-acute-respiratory-infection-in-an-adult-social-care-settin.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

You need to report 2 or more residents with symptoms of an acute respiratory infection (ARI) that started within 5 days of each other as an outbreak [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Has the 5-day window. Says 'residents' where the page says people in the setting, and leaves out the 'linked by spread' caveat.

### 6. Why are chronic skin wounds in people who have recently arrived in the UK relevant to diphtheria?

- Type: in-scope
- Expected source: `diphtheria-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `diphtheria-migrant-health-guide.txt`, [2] `diphtheria-migrant-health-guide.txt`, [3] `diphtheria-migrant-health-guide.txt`

**Answer:**

Chronic skin wounds in people who have recently arrived in the UK are relevant to diphtheria because *C. diphtheriae* has been found to colonize or infect long-standing wounds, and there is often co-infection with other organisms such as Group A Streptococcus or Staphylococcus aureus [1]. This is particularly relevant for migrants who have experienced long journeys prior to reaching the UK and often have poor skin integrity, making them more susceptible to such infections [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Main point correct, including co-infection. Adds that poor skin integrity makes migrants more susceptible, which the page does not state.

### 7. Which ticks are the main carriers of Crimean-Congo haemorrhagic fever and are they established in Britain?

- Type: in-scope
- Expected source: `crimean-congo-haemorrhagic-fever-origins-reservoirs-transmission-and-guidelines.txt` (retrieved in top 3: yes)
- Retrieved: [1] `crimean-congo-haemorrhagic-fever-origins-reservoirs-transmission-and-guidelines.txt`, [2] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`

**Answer:**

The main carriers of Crimean-Congo haemorrhagic fever (CCHF) are Hyalomma ticks, particularly H. marginatum and H. lusitanicum. However, these ticks are not established in the United Kingdom (UK) [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Hyalomma ticks, with no established populations in the UK, as the page says.

### 8. Can whooping cough be diagnosed without a laboratory test?

- Type: in-scope
- Expected source: `pertussis-clinical-and-public-health-management.txt` (retrieved in top 3: yes)
- Retrieved: [1] `pertussis-clinical-and-public-health-management.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

Yes, whooping cough can be diagnosed on clinical grounds without the need for laboratory confirmation [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 9. Which anthrax outbreak affected drug users in the UK around 2009 to 2012?

- Type: in-scope
- Expected source: `anthrax-guidance-for-testing.txt` (retrieved in top 3: yes)
- Retrieved: [1] `anthrax-guidance-for-testing.txt`, [2] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [3] `anthrax-guidance-for-testing.txt`

**Answer:**

The anthrax outbreak affecting drug users in the UK around 2009 to 2012 was injectional anthrax associated with the use of contaminated heroin [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 10. Why is south-east England considered a place where invasive Aedes mosquitoes could survive?

- Type: in-scope
- Expected source: `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

South-east England is considered a place where invasive Aedes mosquitoes could survive due to its warm climate, which is suitable for these mosquitoes. This is supported by the statement from Source [2] which notes, "Temperatures in the south-east of England are high enough for these mosquitoes to survive, and with climate change the areas of suitability will increase, bringing with them the risk of disease transmission within the UK." [2]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Gives the page's reason: temperatures are high enough for the mosquitoes to survive.

### 11. Can chikungunya be confused with dengue when a patient has fever and sore joints?

- Type: in-scope
- Expected source: `chikungunya.txt` (retrieved in top 3: yes)
- Retrieved: [1] `chikungunya.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `chikungunya.txt`

**Answer:**

Yes, chikungunya can be confused with dengue when a patient has fever and sore joints. Both diseases are transmitted by mosquitoes and can present with similar symptoms such as fever and joint pain [1]. Given the overlap in symptoms, chikungunya can often be misdiagnosed as other viral illnesses, including dengue fever, in areas where these infections also occur [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 12. What survey is the main source of data on infections among people who inject drugs?

- Type: in-scope
- Expected source: `people-who-inject-drugs-infection-risks-guidance-and-data.txt` (retrieved in top 3: yes)
- Retrieved: [1] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [2] `people-who-inject-drugs-infection-risks-guidance-and-data.txt`, [3] `universal-varicella-vaccination-programme-in-england.txt`

**Answer:**

The main source of data on infections among people who inject drugs is the Unlinked Anonymous Monitoring (UAM) Survey. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 13. Which animal spreads Lassa fever to people?

- Type: in-scope
- Expected source: `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt` (retrieved in top 3: yes)
- Retrieved: [1] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`, [2] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`, [3] `lassa-fever-origins-reservoirs-transmission-and-guidelines.txt`

**Answer:**

The Lassa fever virus is spread to people by wild rodents, specifically the Mastomys natalensis. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 14. I have just come back from a country with Zika and I might be pregnant. What should I do?

- Type: in-scope
- Expected source: `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt` (retrieved in top 3: yes)
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`

**Answer:**

You should avoid becoming pregnant for two months after your return if you travelled alone, or for three months if you travelled with your male partner or if your male partner travelled alone [1]. Use of effective contraception AND barrier methods (condoms) is advised during these time periods to prevent pregnancy-related harms and to prevent the spread of infection through sexual contact [1]. Additionally, you should inform your midwife of your travel and avoid unprotected sex with anyone who has been to a country at risk of Zika virus transmission for the remainder of your pregnancy [1]. If you have any symptoms suggestive of Zika virus infection, such as a fever, rash, or flu-like illness, you should discuss this with a healthcare professional without delay [1].

- Correct? (yes/no/partly): partly
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Opens with advice on delaying pregnancy, which is for women planning a pregnancy, not someone who may already be pregnant. The midwife and symptom advice is correct.

### 15. Has anyone caught West Nile virus in the UK, and has it been found in British mosquitoes?

- Type: in-scope
- Expected source: `national-contingency-plan-for-west-nile-virus-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `national-contingency-plan-for-west-nile-virus-in-england.txt`, [2] `national-contingency-plan-for-west-nile-virus-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

As of the time of publication, no human cases of West Nile virus (WNV) have been acquired in the UK [2]. However, fragments of WNV genetic material have been detected in UK mosquitoes in samples from 2023 [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 16. Which animals are the natural hosts of Nipah virus?

- Type: in-scope
- Expected source: `nipah-virus-epidemiology-outbreaks-and-guidance.txt` (retrieved in top 3: yes)
- Retrieved: [1] `nipah-virus-epidemiology-outbreaks-and-guidance.txt`, [2] `nipah-virus-epidemiology-outbreaks-and-guidance.txt`, [3] `hantaviruses.txt`

**Answer:**

The natural reservoir of Nipah virus (NiV) is bats, particularly fruit bats of the Pteropus genus. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 17. Is there a vaccine or antiviral drug for Oropouche fever?

- Type: in-scope
- Expected source: `oropouche-virus-disease.txt` (retrieved in top 3: yes)
- Retrieved: [1] `oropouche-virus-disease.txt`, [2] `oropouche-virus-disease.txt`, [3] `severe-fever-with-thrombocytopaenia-syndrome-sfts-epidemiology-outbreaks-and-gui.txt`

**Answer:**

Currently, there is no specific vaccine or antiviral treatment for Oropouche fever. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 18. At what temperature does cold weather start to count as a health risk for vulnerable patients?

- Type: in-scope
- Expected source: `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt` (retrieved in top 3: yes)
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

The guidance does not specify an exact temperature at which cold weather starts to count as a health risk for vulnerable patients. However, it mentions that adverse cold weather can put people at greater risk of ill-health and even death, primarily because it increases the probability of complications from existing diseases and the risk of injury due to falls [2]. The guidance suggests that actions to protect people should be taken when the temperature drops, such as prolonged periods below 2°C, or a sudden drop in temperature [2].

- Correct? (yes/no/partly): partly
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Says no exact temperature is given, then gives the page's example of prolonged periods below 2°C.

### 19. Can a pet cat pass plague to a person?

- Type: in-scope
- Expected source: `plague-epidemiology-outbreaks-and-guidance.txt` (retrieved in top 3: yes)
- Retrieved: [1] `plague-epidemiology-outbreaks-and-guidance.txt`, [2] `plague-epidemiology-outbreaks-and-guidance.txt`, [3] `plague-epidemiology-outbreaks-and-guidance.txt`

**Answer:**

Yes, a pet cat can pass plague to a person. This can occur via fleas, scratches, or bites if the cat has acquired the infection from interactions with wild rodents [2]. Additionally, there is mention of humans being infected via the respiratory secretions of infected cats, though this is not a common route of transmission [2].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): partly
- Citations point to the right source? (yes/no): yes
- Notes: Correct routes. Adds that the respiratory route is not common, which the page does not state.

### 20. How often do sexual health clinics in England have to send their data to UKHSA for the national STI surveillance system?

- Type: in-scope
- Expected source: `gumcad-sti-surveillance-system.txt` (retrieved in top 3: yes)
- Retrieved: [1] `gumcad-sti-surveillance-system.txt`, [2] `gumcad-sti-surveillance-system.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

Sexual health clinics in England have to send their data to UKHSA quarterly for the national STI surveillance system [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 21. How many people in the world are living with long-term hepatitis C and which region has the most?

- Type: in-scope
- Expected source: `hepatitis-c-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hepatitis-c-migrant-health-guide.txt`, [2] `hepatitis-b-migrant-health-guide.txt`, [3] `hepatitis-c-migrant-health-guide.txt`

**Answer:**

The World Health Organization estimates that 50 million people are living with chronic hepatitis C globally [1]. The Eastern Mediterranean Region has the highest burden of disease with 12 million people estimated to be living with chronic infection [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 22. What scheme should companies register with if their staff work in areas affected by Ebola or Marburg?

- Type: in-scope
- Expected source: `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt` (retrieved in top 3: yes)
- Retrieved: [1] `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt`, [2] `ebola-and-marburg-haemorrhagic-fevers-outbreaks-and-case-locations.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

Companies should register with the UK Health Security Agency (UKHSA) returning workers scheme if their staff work in areas affected by Ebola or Marburg [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 23. At what ages do children get the combined measles, mumps, rubella and chickenpox jab from 2026?

- Type: in-scope
- Expected source: `universal-varicella-vaccination-programme-in-england.txt` (retrieved in top 3: yes)
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

From January 2026, children in England will receive the combined measles, mumps, rubella and varicella (MMRV) vaccine as a 2-dose schedule at 12 months and 18 months of age. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 24. Which age groups and health conditions make meningococcal disease more likely?

- Type: in-scope
- Expected source: `meningococcal-disease-background-information.txt` (retrieved in top 3: yes)
- Retrieved: [1] `meningococcal-disease-background-information.txt`, [2] `meningococcal-disease-background-information.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

Meningococcal disease is more common in the following age groups and health conditions:

- Babies and young children [1]
- Teenagers and young adults [1]
- Older adults [1]
- People with a weak immune system – for example, due to HIV or chemotherapy [1]

These factors increase the likelihood of contracting meningococcal disease.

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Lists the groups on the page.

### 25. How long before a trip should someone visiting relatives abroad ask for travel health advice?

- Type: in-scope
- Expected source: `travel-to-visit-friends-and-relatives-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [2] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [3] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`

**Answer:**

People who travel to visit friends and relatives (VFR travellers) should ideally seek travel health advice at least 6 to 8 weeks prior to their planned departure [1]. However, it's noted that it's never too late to advise them about a planned trip [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 26. Does a new arrival need proof of address or immigration status to register with a GP and get vaccinated?

- Type: in-scope
- Expected source: `immunisation-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `immunisation-migrant-health-guide.txt`, [2] `travel-to-visit-friends-and-relatives-migrant-health-guide.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

No, individuals do not need to provide proof of identity, address, or of immigration status in order to register with a GP practice to access immunisations [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 27. Can you catch tick-borne encephalitis from unpasteurised milk products?

- Type: in-scope
- Expected source: `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt` (retrieved in top 3: yes)
- Retrieved: [1] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [2] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`, [3] `tick-borne-encephalitis-epidemiology-diagnosis-and-prevention.txt`

**Answer:**

Yes, infection with TBEV can occur through consumption of infected unpasteurised dairy products [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Yes, through unpasteurised dairy products, as the page says.

### 28. Which laboratories must report notifiable organisms and who do they report to?

- Type: in-scope
- Expected source: `notifiable-organisms-and-how-to-report-them.txt` (retrieved in top 3: yes)
- Retrieved: [1] `notifiable-organisms-and-how-to-report-them.txt`, [2] `notifiable-organisms-and-how-to-report-them.txt`, [3] `nipah-virus-epidemiology-outbreaks-and-guidance.txt`

**Answer:**

All laboratories in England with a primary diagnostic role must report a confirmed notifiable organism to the UK Health Security Agency (UKHSA, previously Public Health England) [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 29. Which country has reported the majority of MERS cases since 2012?

- Type: in-scope
- Expected source: `mers-cov-background-information.txt` (retrieved in top 3: yes)
- Retrieved: [1] `mers-cov-background-information.txt`, [2] `mers-cov-background-information.txt`, [3] `mers-cov-background-information.txt`

**Answer:**

The Kingdom of Saudi Arabia has reported the majority of MERS cases since 2012, with approximately 84% of human cases reported there. [1] [2] [3]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 30. What extra care does a newborn need if the mother is living with hepatitis B?

- Type: in-scope
- Expected source: `hepatitis-b-migrant-health-guide.txt` (retrieved in top 3: yes)
- Retrieved: [1] `hepatitis-b-migrant-health-guide.txt`, [2] `hepatitis-b-migrant-health-guide.txt`, [3] `hepatitis-b-migrant-health-guide.txt`

**Answer:**

Babies born to mothers living with hepatitis B should receive appropriate care, including vaccinations at birth and at 4 weeks of age (in addition to the routine immunisation schedule), and testing at 12–18 months of age [1].

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 31. Which UKHSA research centre works on new treatments and vaccines for drug-resistant infections?

- Type: in-scope
- Expected source: `antimicrobial-resistance-amr.txt` (retrieved in top 3: yes)
- Retrieved: [1] `antimicrobial-resistance-amr.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

The Vaccine Development and Evaluation Centre (VDEC) works on new treatments and vaccines for drug-resistant infections. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 32. A woman had a live vaccine before she knew she was pregnant. Who should the GP tell?

- Type: in-scope
- Expected source: `vaccination-in-pregnancy-vip.txt` (retrieved in top 3: yes)
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `vaccination-in-pregnancy-vip.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`

**Answer:**

The GP should notify UKHSA if a woman has had a live vaccine before realizing she was pregnant. This can be done by completing the Notification form for vaccines administered in pregnancy (VIP) and returning it by email or post, or through the online form provided. [1]

- Correct? (yes/no/partly): yes
- Grounded in the sources? (yes/no): yes
- Citations point to the right source? (yes/no): yes
- Notes: Matches the page.

### 33. What is the recommended adult dose of paracetamol?

- Type: out-of-scope
- Note: Not covered: paracetamol is mentioned once (Zika symptom relief) with no dose; model should say sources don't contain the answer
- Retrieved: [1] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `hepatitis-c-migrant-health-guide.txt`

**Answer:**

I cannot answer from the provided guidance. The sources given are related to MMR vaccination, measles infection control, and hepatitis C management and do not contain information about the recommended adult dose of paracetamol.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 34. How many people caught measles in England last year?

- Type: out-of-scope
- Note: Case numbers not in these pages
- Retrieved: [1] `universal-varicella-vaccination-programme-in-england.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`

**Answer:**

I cannot answer from the provided guidance. The sources do not contain specific information about the number of people who caught measles in England last year.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 35. Is the flu vaccine safe for people with egg allergy?

- Type: out-of-scope
- Note: Flu vaccine safety not covered
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`, [3] `national-contingency-plan-for-invasive-aedes-mosquitoes-in-england.txt`

**Answer:**

The provided sources do not contain information about the safety of the flu vaccine for people with egg allergy. Therefore, I cannot answer this question based on the given guidance. [1]

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 36. What are the side effects of the HPV vaccine?

- Type: out-of-scope
- Note: HPV not mentioned in any page
- Retrieved: [1] `vaccination-in-pregnancy-vip.txt`, [2] `poliomyelitis-and-post-polio-syndrome-migrant-health-guide.txt`, [3] `universal-varicella-vaccination-programme-in-england.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources do not contain information about the side effects of the HPV vaccine.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.

### 37. Where can I get a COVID-19 booster this winter?

- Type: out-of-scope
- Note: Boundary case: pages only say the NHS contacts people who may be eligible; no locations given
- Retrieved: [1] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [2] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`, [3] `supporting-vulnerable-people-before-and-during-cold-weather-for-healthcare-profe.txt`

**Answer:**

For those working in managerial or patient-facing roles, if you are eligible, you can get a COVID-19 booster vaccination as a preventive measure to reduce the risk of respiratory infections during winter. The NHS will contact you if your records suggest you may be eligible for vaccination. [1]

- Said the sources do not contain the answer? (yes/no): no
- Added facts from outside the sources? (yes/no): no
- Notes: Does not say that no location is given. Gives the advice for managerial and patient-facing staff and the NHS contact line, so the 'where' is unanswered. No flu route.

### 38. How long should someone with scabies stay off work?

- Type: out-of-scope
- Note: Scabies not mentioned in any page
- Retrieved: [1] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`, [2] `mmr-catchup-programme-diagnosis-case-management-and-advice.txt`, [3] `health-advice-for-women-returning-from-areas-with-a-risk-of-zika-virus.txt`

**Answer:**

I cannot answer from the provided guidance. The given sources discuss Zika virus prevention, measles management, and MMR vaccination, but do not contain information about scabies or work restrictions related to it.

- Said the sources do not contain the answer? (yes/no): yes
- Added facts from outside the sources? (yes/no): no
- Notes: Clean refusal.
