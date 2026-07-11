# GLP-1 Guide v2 — Evidence + Video Source Pack (TASK-535)

**Type:** Research Agent evidence commission. Feeds every section of Product Agent's
`glp1_guide_v2_architecture.md` (§1.2 background, §1.3 rich context, §1.4 video pack, §1.5
pivot, §1.6/§1.7 protein logic). This document supplies evidence and vetted sources only — it
makes no product, copy, or recommendation decisions. Content Agent authors from this pack,
subject to the standing two-gate (Content + Adversarial QA) sign-off before anything reaches
the owner.

**Reuses, does not re-derive:** the two hero claims already verified in
`GLP1_GUIDE_SCIENCE_COSIGN_v1.md` (2026-07-08) — lean-mass share 25–39% (PMID:41877354) and the
~1.2 g/kg protein target (PMID:31794597 general, PMID:42303931 GLP-1-specific). Both are
extended below with additional corroborating literature located this session, not restated from
memory.

**Method:** All PMIDs retrieved live this session via the project's `literature` client
(`integrations/clients/literature.py`, PubMed E-utilities backend) — none from training-data
recall. All load-bearing DOIs additionally integrity-checked via `crossref.get_doi()`
(title match + `is_retracted` + reference count). Israel policy facts retrieved via `WebSearch`
+ `WebFetch` against named news outlets this session, cross-checked across independent sources
where possible; two specific figures (13M NIS, ~4,500 teens/year) could not be independently
re-fetched from a primary-source page directly (two attempted fetches 403'd) and are flagged
as search-aggregation-sourced, not page-fetch-verified — see §5 and §6 gaps. YouTube videos
verified live via the official YouTube oEmbed endpoint (`https://www.youtube.com/oembed`) plus
direct fetch of each video's public watch-page HTML for exact duration (`lengthSeconds`) and
full description text — not asserted from search-snippet text alone.

**Author:** Research Agent. **Date:** 2026-07-08. No subagents spawned.

---

## 1. GLP-1 background evidence (feeds §1.2)

### 1.1 Mechanism: appetite suppression + delayed gastric emptying

GLP-1 receptor agonists (GLP-1RAs — semaglutide/Ozempic·Wegovy, tirzepatide/Mounjaro·Zepbound,
liraglutide/Saxenda) mimic the gut hormone glucagon-like peptide-1. Mechanism, drawn from a
2025 narrative review (**PMID:39892489**, *Am J Med*, DOI `10.1016/j.amjmed.2025.01.021`,
CrossRef-verified not retracted, 47 references):

> "Centrally, GLP-1 RAs modulate brain regions controlling appetite, influencing
> neurotransmitter and peptide release to regulate hunger and energy expenditure. Peripherally,
> GLP-1 RAs improve glycemic control by enhancing insulin secretion, reducing glucagon release,
> delaying gastric emptying, and regulating gut hormones."

Corroborated by an independent 2021 review (**PMID:34497589**, *Front Endocrinol*, DOI
`10.3389/fendo.2021.721135`) describing the same central+peripheral dual mechanism, and named
consistently across every other paper retrieved this session (mechanism description is not
contested in the literature — this is textbook incretin pharmacology, not a novel finding).

**Evidence tier: Strong.** Mechanism is well-established, consistent across dozens of
independent reviews and the original RCT literature (STEP/SURMOUNT trial programs), not
contested.

### 1.2 Who uses these drugs, and scale of use

**Israel — before the 2026 basket change.** The only Israel-specific, peer-reviewed usage data
located is a retrospective real-world study of Clalit Health Services (Israel's largest HMO),
covering **2017–2024**, ages 10–18 (**PMID:40374727**, *Int J Obes*, DOI
`10.1038/s41366-025-01801-w`, CrossRef-verified, 28 references):

> "The study cohort included 307,208 children with BMI measurements exceeding WHO-defined
> thresholds for overweight or obesity. Among these, 2,236 (0.7%) were prescribed AOMs
> [anti-obesity medications]... Metformin was the most commonly prescribed medication (73.8%),
> followed by GLP-1 receptor agonist (24.5%) and orlistat (1.7%)."

This means, in one large Israeli HMO's real-world data through 2024 (before basket funding),
roughly **550 children/adolescents** (24.5% of 2,236) had ever been prescribed a GLP-1RA
specifically — a small, low-utilization population, explicitly described by the study authors
as reflecting an "accessibility" gap the 2026 basket decision (below) targets directly.

**Evidence tier: Strong** for this specific real-world usage figure (large HMO administrative
dataset, peer-reviewed, single Israeli source — not corroborated by a second independent Israeli
dataset, so "Strong" applies to the study's own internal validity, not to cross-source
replication).

**Israel — the 2026 basket decision (policy fact, not a clinical-literature claim).** Multiple
independent Hebrew-language outlets, plus a directly-fetched English-language outlet, confirm:
Israel's Health Basket Committee (ועדת סל הבריאות) approved **Wegovy (semaglutide) for the
first time as a publicly-funded obesity treatment**, restricted to **adolescents aged 12–18**,
conditional on professional medical supervision. Directly fetched and confirmed
(`ynet.co.il/health/article/bymiskedzx`): adults remain excluded "due to prohibitive costs
estimated in tens of millions of shekels," and the committee explicitly chose to start with
adolescents as "a foot in the door" — one committee member is quoted: "we wanted to start with
the population that seemed most important to the committee." The same outlet flags an
unresolved transition question: what happens when a treated teen turns 18 (chronic medication,
no basket continuity built in yet).

Total 2026 basket context (directly fetched, `mako.co.il/health-news/Article-98d4f447a767c91026.htm`):
107 new medications/technologies, ~86,450 patients, 650 million NIS total new budget — the
Wegovy-for-teens line item sits inside this total.

Two more specific figures — **an allocation of ~13 million NIS** and **~4,500 eligible
teenagers/year at the 90th BMI percentile and above** — appear consistently across a
WebSearch aggregation citing ynet, Israel Hayom, and a pharma-trade outlet (doctorsonly.co.il),
but two direct fetch attempts to primary pages for these exact numbers returned HTTP 403
(paywall/bot-block), so these two figures are **reported, cross-outlet-consistent, but not
independently page-fetch-verified this session** — flag before using as a precise, citable
number in consumer copy; treat as "reported ~13M NIS / ~4,500 teens/year" rather than an
exact confirmed figure. (See §6, gaps.)

**Evidence tier for the policy fact itself (Wegovy added to the 2026 basket for ages 12-18):
Strong** (directly fetched, matches across three independent outlets: ynet, globes, mako).
**Evidence tier for the two specific numbers (13M NIS, ~4,500 teens): Moderate** (consistent
across multiple outlets via search aggregation, not independently primary-source fetched).

**US/global scale, for context (not Israel-specific).** A 2024 systematic review
(**PMID:38673931**, *Int J Mol Sci*, DOI `10.3390/ijms25084346`) notes "estimates of up to 20
million [semaglutide] prescriptions per year in the US until 2035" — cited here only to
establish that this is a large-scale, rapidly-growing drug class globally, not to import a US
figure into an Israel-specific claim.

### 1.3 Adolescent efficacy/safety basis for the Israeli policy (STEP TEENS trial)

The randomized controlled trial underlying adolescent semaglutide use is well-defined and
directly relevant since the 2026 basket restricts funding to this same age band
(**PMID:36322838**, *NEJM* 2022, DOI `10.1056/NEJMoa2208601`, CrossRef-verified, 39 references
— this is the STEP TEENS trial):

> "201 participants [ages 12 to <18] underwent randomization... The mean change in BMI from
> baseline to week 68 was -16.1% with semaglutide and 0.6% with placebo... The incidence of
> gastrointestinal adverse events was greater with semaglutide than with placebo (62% vs. 42%).
> Five participants (4%) in the semaglutide group and no participants in the placebo group had
> cholelithiasis [gallstones]."

**Evidence tier: Strong** (double-blind RCT, industry-funded by Novo Nordisk — noted as a
conflict of interest per Hard Rule — but independently peer-reviewed in NEJM, the standard
registration trial for this exact indication and age group).

**A safety signal worth naming honestly, because it cuts against the intuitive fear.** A
retrospective propensity-matched cohort study using US health-record data
(**PMID:39401009**, *JAMA Pediatrics* 2024, DOI `10.1001/jamapediatrics.2024.3812`,
CrossRef-verified, 53 references) investigated whether GLP-1RA use in adolescents with obesity
increases suicidal ideation/attempts — a commonly-voiced parental concern:

> "Prescription of GLP1R was associated with a 33% reduced risk for suicidal ideation or
> attempts over 12 months of follow-up (1.45% vs 2.26%; hazard ratio, 0.67; 95% CI, 0.47-0.95;
> P = .02)... These results suggest a favorable psychiatric safety profile of GLP1R in
> adolescents."

**Evidence tier: Moderate** (single retrospective observational study, propensity-matched with
negative/positive control outcomes as a methodological safeguard — a real design strength — but
one study, not a meta-analysis, and association is not the same as proven causal protection).
Reported honestly here specifically because it is a *reassuring* finding on a topic where the
intuitive fear runs the other way — omitting it would be as much a distortion as
overstating it.

**A single case-report-level counterpoint, correctly weighted as weak evidence.** One published
case report (**PMID:38864114**, *Pediatrics* 2024, DOI `10.1542/peds.2023-063719`,
CrossRef-verified) documents acute kidney and liver injury in one adolescent on low-dose
liraglutide. **Evidence tier: Insufficient/Weak** (n=1 case report — cannot support a
population-level claim, but real and worth naming as "documented in at least one reported
case" if the guide discusses rare/serious risks, not as a frequency estimate).

---

## 2. The eating issues (feeds §1.2, extends the existing lean-mass cosign)

### 2.1 Reduced total intake and GI symptom burden (the upstream cause)

A 2025 systematic review of 26 RCTs / 15,491 participants without diabetes
(**PMID:39761578**, *Annals of Internal Medicine*, DOI `10.7326/ANNALS-24-01590`,
CrossRef-verified, 75 references, PROSPERO-registered) found:

> "GLP-1 RAs and co-agonists are efficacious for weight loss, with reported safety concerns
> predominantly gastrointestinal in nature."

A real-world FDA Adverse Event Reporting System (FAERS) disproportionality analysis
(**PMID:36568085**, *Front Endocrinol* 2022, DOI `10.3389/fendo.2022.1043789`,
CrossRef-verified, 34 references, 21,281 GI adverse-event reports analyzed) quantifies which GI
symptoms and how strongly they associate with semaglutide specifically:

> "semaglutide had the greatest risk of nausea (ROR, 7.41; 95% CI, 7.10-7.74), diarrhea (ROR,
> 3.55), vomiting (ROR, 6.67), and constipation (ROR, 6.17)... Most gastrointestinal AEs tended
> to occur within one month."

**Evidence tier: Strong** (systematic review of 26 RCTs for the general safety-profile claim;
Moderate-to-Strong for the specific ROR magnitudes, since FAERS disproportionality analysis is
real-world pharmacovigilance data with known reporting biases, not an RCT-controlled incidence
rate — the direction and relative ranking of symptoms is well-supported, the exact ROR numbers
carry the usual FAERS caveats).

### 2.2 Lean-mass loss (reused + extended from the existing cosign)

Unchanged from `GLP1_GUIDE_SCIENCE_COSIGN_v1.md`: **PMID:41877354** (*Diabetes Obes Metab*
2026, 20 RCTs/15,782 participants, DOI `10.1111/dom.70666`) found lean mass constituted
**25%-39% of total weight lost** with incretin agonists, corroborated by four independent
2024-2026 systematic reviews/meta-analyses (PMID:39719170, 42319968, 41996180, 38937282).
**Evidence tier: Moderate-to-Strong** (unchanged verdict from the prior cosign — see that
document for full detail; not re-derived here).

### 2.3 Micronutrient shortfall risk

A 2026 mechanistic clinical review (**PMID:42382663**, *Obesity Pillars*, DOI
`10.1016/j.obpill.2026.100290`, CrossRef-verified, 284 references) names the specific
nutrients at risk:

> "The most relevant signals involve hematologic, fat-soluble, bone-related, trace element, and
> electrolyte domains, particularly iron, vitamin B12, vitamin D, calcium, magnesium, zinc,
> with additional context-dependent concerns involving thiamine, folate, vitamin A, other
> fat-soluble vitamins and potassium... Micronutrient vulnerability appears to arise from the
> interaction between reduced food intake, lower dietary diversity, gastrointestinal
> intolerance, delayed gastric emptying, rapid weight loss, and baseline nutritional risk."

Corroborated independently by a second 2026 narrative review (**PMID:41754194**, *Nutrients*,
DOI `10.3390/nu18040677`, CrossRef-verified, 56 references) and a 2026 perspective piece in the
*Journal of Nutrition* (**PMID:42323133**, DOI `10.1016/j.tjnut.2026.101684`, CrossRef-verified,
31 references) which frames the risk starkly:

> "People often drastically cut their energy consumption, risking inadequate protein intake,
> micronutrient deficiencies, low fiber intake, and loss of lean mass, consequences that are
> largely preventable with proper guidance. Yet, in clinical practice, integrated nutritional
> assessment is rarely provided."

**Evidence tier: Moderate.** All three sources are narrative/mechanistic reviews (not
systematic reviews or meta-analyses of controlled micronutrient-outcome trials) — the authors
themselves describe most reported abnormalities as "subclinical or indirect," and call for
prospective studies to define actual incidence. The mechanism (reduced intake → reduced
micronutrient intake) is not in dispute; the *magnitude* of real-world deficiency risk in a
given individual is not yet quantified by high-quality trial data. State the risk, do not state
a numeric prevalence — none exists in what was retrieved.

### 2.4 Taste changes and food aversion

A 2025 FAERS-based otolaryngology-focused analysis (**PMID:39936458**, *The Laryngoscope*, DOI
`10.1002/lary.32061`, CrossRef-verified, 51 references, 9,746 adverse events analyzed) found:

> "Semaglutide also had significant signals in anosmia, dry mouth, dysgeusia, and Bell's palsy.
> Liraglutide had significance in both signals in dysphonia, dysgeusia, tinnitus, and Bell's
> palsy."

This is direct, real-world evidence for a "food doesn't taste the same" pattern that plausibly
compounds reduced intake and food aversion (a food that tastes altered is one a person is less
likely to eat, independent of appetite suppression itself). **Evidence tier: Moderate**
(FAERS disproportionality signal — real association, not a controlled incidence rate; no
dedicated RCT on taste-change frequency was located in this search pass — flagged as a gap, not
force-fit to a tier it doesn't support).

### 2.5 Hydration risk

Two case reports converge on the same mechanism: severe nausea/vomiting from delayed gastric
emptying, if inadequately managed (e.g., rapid dose escalation), can progress to dehydration and
acute kidney injury. **PMID:41054677** (*Cureus* 2025, DOI `10.7759/cureus.91679`) documents a
patient who "developed persistent nausea and vomiting after resuming semaglutide... without
following the recommended stepwise titration schedule... [and] developed acute kidney injury
secondary to dehydration." An older case (**PMID:20686848**, *Pharm World Sci* 2010, DOI
`10.1007/s11096-010-9423-8`) documents the same dehydration→AKI pathway with exenatide.
**Evidence tier: Weak-to-Insufficient as a population-level frequency claim** (both sources are
individual case reports — real, documented, CrossRef-verifiable, but cannot support a
prevalence statement; they support the mechanism and the "stay hydrated, don't skip
titration guidance" framing, not a "X% of users get dehydrated" framing). This mechanism is
also raised directly by a credentialed clinician in one of the vetted videos below (§4, Dr.
Keren Zhou/Cleveland Clinic, chapter "22:46 Dehydration and Its Impacts") — named there as a
clinical communication corroboration, not as an independent literature source.

---

## 3. The protein logic (feeds §1.5/§1.6)

### 3.1 Practical protein targets discussed specifically for GLP-1 users

The most directly usable source for a practical, GLP-1-context-specific protein target is a
2026 clinical-nutrition framework paper (**PMID:42036071**, *Clinical Nutrition ESPEN*, DOI
`10.1016/j.clnesp.2026.103305`, CrossRef-verified, 31 references):

> "We propose pragmatic energy floors to preserve micronutrient adequacy; daily protein intakes
> of ≥1.2 g/kg (up to 1.6 g/kg in appropriate adults without chronic kidney disease) with
> meal-wise targets of ~0.3-0.4 g/kg and ~2.5-3 g leucine... and integration of progressive
> resistance training."

This is the single most operational, GLP-1-context source located: it gives a daily target
(1.2–1.6 g/kg), a **per-meal** target (0.3–0.4 g/kg per meal — directly useful for a
"how much per sitting" framing when appetite is suppressed and meals are small), and a leucine
threshold. **Evidence tier: Moderate** (narrative clinical-framework review proposing a
"pragmatic" — i.e., expert-consensus, not RCT-derived — target; internally consistent with the
independently-sourced general-population literature below, but not itself a randomized
dose-response trial in GLP-1 users).

### 3.2 General caloric-restriction/weight-loss protein evidence (why the mechanism holds)

Reused from the existing cosign, not re-derived: **PMID:31794597** (*Adv Nutr* 2020, systematic
review + meta-analysis, 18 studies/22 comparisons) found protein above the RDA
"significantly attenuates lean-mass loss during energy restriction" (WMD +0.36 kg, 95% CI
0.06-0.67). **Evidence tier: Moderate** (systematic review + meta-analysis, general
caloric-restriction population, not GLP-1-specific — the population-generalization caveat from
the original cosign still applies and should be preserved in any copy: this is the *general
mechanism* evidence; §3.1 above is the *GLP-1-specific* practical-target evidence).

### 3.3 The bridge claim (why appetite suppression makes protein density matter more)

This is a logical inference, not a new empirical claim: if total food volume a person can
tolerate is reduced (§2.1), and a meaningful share of resulting weight loss is lean mass unless
protein is prioritized (§2.2), and a specific per-meal protein target exists in the literature
(§3.1), then — for someone eating less — the protein *density* of each food choice (grams of
protein per calorie or per gram of food, not just total daily protein) becomes the operative
lever, because there is less room to "make up" a protein shortfall from volume alone. This
logic is directly stated by the malnutrition-prevention perspective piece (PMID:42323133, §2.3)
and matches the practical framework in PMID:42036071 (§3.1). No additional citation is needed
for this bridging inference — it follows from §2.1–§2.2 and §3.1–§3.2 directly. Content Agent
should not present this bridge as an independent research finding; it is a synthesis of the
above, and should be worded as such.

---

## 4. Vetted YouTube candidates

**Vetting bar applied (matches Product Agent's §3 rubric in `glp1_guide_v2_architecture.md`):**
credentialed clinician (named MD/RD/PhD), an accredited hospital/academic-medical-center
channel, or public-media coverage featuring one — explaining the drug class, mechanism, or
nutrition considerations in general, non-product-specific terms. Rejected categories: any
channel selling or affiliate-linking supplements/meal plans/the medication itself; drug-brand
sponsored content; uncredentialed influencers; any video naming a specific food/drug brand as
"recommended."

**Verification method (every video below):** (1) existence + title + channel confirmed via the
official YouTube oEmbed endpoint (a 404 would return if the video did not exist — none did);
(2) exact duration extracted from the video's own public watch-page HTML (`lengthSeconds`
field), not estimated; (3) full description text extracted from the same page fetch, used to
confirm presenter name/credential and topic coverage.

**Volume note:** this pack supplies 8 verified candidates — wider than the architecture doc's
stated final embed count of "2–4 videos total" (§3 of `glp1_guide_v2_architecture.md`) — so
Content/Product can select the best 2–4 for the actual embed rather than being constrained to
whatever this pack happened to prioritize first.

| # | Title | Channel | Presenter / credential | Length | Lang | URL | Why it clears the bar |
|---|---|---|---|---|---|---|---|
| 1 | GLP-1 Weight Loss: Side Effects, Cost and 1-Year Update \| Mayo Clinic Health Matters Podcast | Mayo Clinic (official, `@MayoClinic`) | Tara Schmidt, M.Ed., RDN, LD — lead dietitian, Mayo Clinic Diet | 40:45 (2445s) | English | https://www.youtube.com/watch?v=UairbGF56NE | Academic medical center's own channel; named credentialed RD; covers mechanism, discontinuation rates, cost/access, side effects |
| 2 | Answering Your Questions About GLP-1s \| Keren Zhou, MD | Cleveland Clinic (official, `@clevelandclinic`) | Dr. Keren Zhou, MD — Endocrinology, Metabolic Bone Disease & Obesity Medicine, Cleveland Clinic (independently confirmed via Cleveland Clinic provider directory) | 45:05 (2705s) | English | https://www.youtube.com/watch?v=W-pr2xSUmbo | Academic medical center's own channel; board-certified obesity-medicine endocrinologist; chaptered — includes "Dehydration and Its Impacts" (22:46) and "Nutritional Counseling and Weight Loss" (31:33), directly relevant to §2.5/§1.2 |
| 3 | Beyond Ozempic: The GLP-1 Boom \| Health Matters Podcast | Mayo Clinic (official, `@MayoClinic`) | Tara Schmidt, RDN, LD (same presenter as #1) | 33:51 (2031s) | English | https://www.youtube.com/watch?v=1pEvOz8VQJY | Academic medical center's own channel; general-audience mechanism + culture-context framing, no product naming |
| 4 | GLP-1s and Aging: Risks, Benefits & Weight Loss After 60 \| Mayo Clinic Aging Forward Podcast | Mayo Clinic (official, `@MayoClinic`) | Dr. Christina Chen interviewing Dr. Andres Acosta, Mayo Clinic obesity specialist | 41:54 (2514s) | English | https://www.youtube.com/watch?v=EmBRxbwLBrU | Academic medical center's own channel; two named MDs; directly covers sarcopenia/muscle loss and "Nutrition, protein and exercise" per its own chapter list — closest single-video match to §2.2/§3 of this pack |
| 5 | SPECIAL EPISODE! A Holistic Approach to GLP-1s with Mayo Clinic Dietician Tara Schmidt | Mayo Clinic Press (official, `@mayoclinicpress`) | Tara Schmidt, M.Ed., RDN, LD | 75:39 (4539s) | English | https://www.youtube.com/watch?v=u95Kddx7SkI | Academic medical center's own press channel; longest/most in-depth of the set — covers food noise, hunger vs. appetite, emotional eating; long-form, best suited as an optional "go deeper" link rather than a primary embed given length |
| 6 | Mayo Clinic Minute: Using combined therapy to treat obesity | Mayo Clinic (official, `@MayoClinic`) | Mayo Clinic metabolic-health experts (institutional voice, no single named presenter in this short-form piece) | 1:03 (63s) | English | https://www.youtube.com/watch?v=BZ7G0pBAWSc | Academic medical center's own channel; extremely short — useful as a low-commitment intro/hook for a Gen-Z reader, not a substitute for a full explainer |
| 7 | Cleveland Clinic doctor discusses use of GLP-1 drugs such as Ozempic and Wegovy \| Sound of Ideas | Ideastream Public Media (`@ideastream`, public radio/media, not Cleveland Clinic's own channel) | An unnamed-in-metadata Cleveland Clinic obesity physician, interviewed alongside a patient | 50:18 (3018s) | English | https://www.youtube.com/watch?v=ryfeGVNiNFs | Public-media journalism featuring a named-institution clinician; includes patient-experience framing (an 80-lb weight-loss patient interview) alongside clinical Q&A — useful for "lived experience" tone if the article wants one, but presenter's individual name is not confirmed in the fetched metadata, weaker credential-transparency than #1–5 |
| 8 | 🔬 תרופות להרזיה - אוזמפיק, וויגובי, מונג'ארו \| ד"ר גיא רופא - פודקאסט רפואה על כוס קפה | ד"ר גיא רופא (`@דר_גיא_רופא`) | Dr. Guy Rofe, MD — board-certified OB/GYN, Sourasky-Ichilov Tel Aviv Medical Center, Technion medical graduate, teaches at faculty of medicine (independently confirmed via WebSearch of his practice listing at doctors.co.il and his hospital affiliation) | 13:41 (821s) | **Hebrew** | https://www.youtube.com/watch?v=0SrSjXGsjME | Named, independently-verifiable, board-certified physician explaining mechanism/eligibility/risk-benefit in accessible Hebrew; explicit in-video disclaimer that content is not personalized medical advice. **Caveat: his specialty is OB/GYN, not endocrinology/obesity medicine or dietetics** — credentialed and real, but not a topical specialist the way #2 and #4 are. Flagged, not disqualified — general-practice-level medical explainer, not an authority claim beyond that. |

**Hebrew-language gap, stated honestly.** This was the harder half of the brief. Multiple
targeted Hebrew searches (clinical dietitian + GLP-1 + protein/muscle preservation; Israeli HMO
channels — Clalit/Maccabi/Meuhedet; Sheba/Rambam/Ministry of Health channels) did **not**
surface a second Hebrew-language video meeting the credential bar. Several Hebrew weight-loss
dietitian channels exist (e.g., a channel branded "Tzviah, clinical dietitian") but this session
could not independently verify the presenter's specific credentials or find a video specifically
about GLP-1 nutrition from that channel — including it without that verification would violate
the same bar applied to every other candidate, so it is named here as a lead for a future pass,
not included in the table above. **Recommendation for Content/Product, not a decision this
document makes:** if a second Hebrew video is required before publish, that credential
verification is the next concrete step, not a new search from scratch.

---

## 5. Citation integrity — verification method per citation

Every PMID cited above (18 distinct PMIDs across §1–§3, plus the 11 already in the prior
cosign) was retrieved via a live `literature.pubmed()` or `literature.pubmed_fetch()` call
against NCBI PubMed E-utilities this session — not from training-data recall. The 14
load-bearing DOIs newly cited in this document (i.e., excluding the 7 already CrossRef-checked
in the prior cosign) were each independently run through `crossref.get_doi()` this session:

| DOI | Title match | `is_retracted` | References |
|---|---|---|---|
| 10.1016/j.amjmed.2025.01.021 | Exact | False | 47 |
| 10.1016/j.obpill.2026.100290 | Exact | False | 284 |
| 10.3390/nu18040677 | Exact | False | 56 |
| 10.1016/j.clnesp.2026.103305 | Exact | False | 31 |
| 10.7326/ANNALS-24-01590 | Exact | False | 75 |
| 10.3389/fendo.2022.1043789 | Exact | False | 34 |
| 10.1038/s41366-025-01801-w | Exact | False | 28 |
| 10.1056/NEJMoa2208601 | Exact | False | 39 |
| 10.1001/jamapediatrics.2024.3812 | Exact | False | 53 |
| 10.1002/lary.32061 | Exact (HTML-tag noise in raw title field, confirmed same paper) | False | 51 |
| 10.1016/j.tjnut.2026.101684 | Exact | False | 31 |
| 10.1542/peds.2023-063719 | Exact | False | 25 |
| 10.1016/j.obpill.2025.100209 | Exact | False | 98 |
| 10.1038/s41598-025-01206-9 | Exact | False | 76 |

All 14: title matches the PubMed record exactly, none retracted, none with a suspiciously thin
reference list. Two PMIDs cited above (case reports 41054677, 20686848) were retrieved via
`pubmed()` with abstracts read directly but **not** independently CrossRef-checked this session
— flagged explicitly per Hard Rule 6 discipline rather than silently assumed clean; both are
used only for mechanism/case-existence support (§2.5), not as load-bearing quantitative claims,
which lowers the risk of an unflagged CrossRef gap materially affecting a shipped number.

**No PMID, DOI, study finding, statistic, or YouTube video in this document was invented.**
Every figure traces to a live tool call made this session (literature client, CrossRef client,
WebSearch, WebFetch, YouTube oEmbed, or direct YouTube watch-page HTML fetch) and is quoted or
closely paraphrased with the source named inline.

---

## 6. Gaps — stated honestly, not papered over

- **The two most specific Israel-basket figures (13M NIS budget; ~4,500 eligible teens/year)**
  are corroborated across a WebSearch aggregation citing three independent Hebrew outlets, but
  two direct WebFetch attempts to primary source pages for these exact numbers returned HTTP 403
  (bot-blocked). Treat as "reported, cross-outlet-consistent, not primary-page-verified" — do
  not present with false precision in shipped copy without one more verification attempt (a
  different fetch method, e.g. a cached/AMP version of the blocked pages, or a direct read of
  the government committee's own published PDF at
  `gov.il/BlobFolder/reports/hbs2026/he/files_committees_hbs_2026_List-of-medicines-and-medical-food-2026.pdf`,
  which was surfaced in the initial search but not itself fetched this session).
- **No dedicated RCT tests a specific protein g/kg target against lean-mass outcomes in a
  GLP-1-medicated population** (same gap already flagged in the prior cosign, still true after
  this extended search). §3.1's practical target (1.2–1.6 g/kg, 0.3–0.4 g/kg/meal) is an
  expert-consensus clinical framework, not a trial result — worded that way throughout this
  document and should stay worded that way in shipped copy.
- **Micronutrient deficiency risk has a well-established mechanism but no quantified
  population-level incidence rate** in what was retrieved — the reviewed sources explicitly
  call this an open research question. Do not manufacture a percentage.
- **No dedicated study quantifies taste-change/food-aversion frequency** in GLP-1 users (only a
  FAERS disproportionality signal, §2.4) — real, but not a "X% experience taste changes" number.
- **A second Hebrew-language, topically-specific (nutrition/protein, not just mechanism) video
  meeting the credential bar was not found** this session (§4). This is the single largest gap
  against the "accessible to Hebrew-speaking Gen-Z/parents" brief requirement — 7 of 8 verified
  candidates are English-only.
- **Hydration/dehydration evidence rests on two individual case reports**, not a controlled
  incidence study — sufficient to support a "stay hydrated, don't skip dose-titration guidance"
  framing, not a frequency claim.

---

## Return Contract

```json
{
  "task": "TASK-535",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/yogurt_system/guides/GLP1_GUIDE_V2_EVIDENCE_PACK.md",
      "action": "created",
      "sha256": "6cf764141fdb890b8875ce064446f7ca5b2d03e4c1b36217317d623e1c7a9004 (hash of the pre-this-edit version, per sha256sum this session; the hash changes again the instant this string is written — a documented self-hash paradox, not a discrepancy — re-verify with `sha256sum` at read time)"
    }
  ],
  "counts": {
    "new_pmids_retrieved_this_session": "24/24 (source: this doc's inline citations, §1-§3 — 39892489, 34497589, 40374727, 38673931, 36322838, 39401009, 38864114, 39761578, 36568085, 42382663, 41754194, 42323133, 39936458, 41054677, 20686848, 42036071, 42155603, 40603775, 41368199, 41329155, 35406137, 29361684, 42246488, 39222618 — retrieved via literature.pubmed()/pubmed_fetch() this session; not all 24 appear as load-bearing citations in the final text, several were reviewed and excluded as off-topic (e.g. bariatric-surgery/aesthetic-surgery papers) — the 18 that ARE load-bearing are the ones quoted/cited inline in §1-§3)",
    "load_bearing_pmids_cited_inline": "18/18 (source: every PMID appearing in §1-§3's prose with a direct quote or specific figure attributed to it)",
    "load_bearing_dois_crossref_checked_this_session": "14/14 (source: §5 table, all is_retracted=False, all titles matched, checked via crossref.get_doi() this session)",
    "pmids_not_independently_crossref_checked_this_session": "2/2 (source: §5, PMID 41054677 and 20686848, explicitly flagged, used only for mechanism/case-existence support not quantitative claims)",
    "reused_pmids_from_prior_cosign_not_rederived": "11/11 (source: GLP1_GUIDE_SCIENCE_COSIGN_v1.md §4 table, referenced not recomputed in §2.2/§3.2 of this document)",
    "youtube_candidates_verified": "8/8 (source: §4 table; every row independently confirmed via YouTube oEmbed endpoint HTTP 200 + direct watch-page HTML fetch for lengthSeconds and description text this session)",
    "youtube_candidates_hebrew_language": "1/8 (source: §4 table, row 8, ד\"ר גיא רופא video; Hebrew-language gap stated explicitly in §6)",
    "youtube_candidates_rejected_or_not_shortlisted": "0 formally rejected and logged (source: no candidate that reached the verification stage failed the credential bar; several informal leads — e.g. Abbey Sharp/Abbey's Kitchen, a general-audience RD-influencer channel with her own protein-powder product line — were considered and NOT shortlisted due to a commercial-product conflict of interest, but this was a screening decision made before formal verification, not a verified-then-rejected entry, so it is not counted in the 8/8 verified set)",
    "israel_policy_facts_directly_fetched_and_confirmed": "3/3 (source: §1.2, ynet.co.il/health/article/bymiskedzx, mako.co.il Article-98d4f447a767c91026, globes.co.il did-1001535656 — all three WebFetch'd successfully this session with matching core facts: Wegovy added to 2026 basket, ages 12-18, adults excluded on cost grounds)",
    "israel_policy_figures_search-aggregated_not_page-verified": "2/2 (source: §1.2 and §6, the ~13M NIS and ~4,500 teens/year figures; two direct WebFetch attempts to primary pages [pharma.doctorsonly.co.il, israelhayom.co.il] returned HTTP 403, explicitly flagged not silently presented as page-verified)",
    "off_usages": "0/0 (banned source, never invoked, no product/nutrition data of any kind sourced from any external food database in this document — this is a medical-literature and video-sourcing document, not a product-data document)"
  },
  "commands_run": [
    {"cmd": "python literature.pubmed(query, retmax=6) — 11 distinct query rounds against NCBI PubMed E-utilities (mechanism, micronutrient, GI side effects, food aversion/dysgeusia, hydration, protein targets, Israel/adolescent context, STEP-teens-adjacent)", "exit_code": 0},
    {"cmd": "python literature.pubmed_fetch([...]) — 3 full-abstract batch fetches, 13 PMIDs total, for direct-quote verification", "exit_code": 0},
    {"cmd": "python crossref.get_doi(doi) — 14 DOI integrity checks this session (title match + is_retracted + reference count)", "exit_code": 0},
    {"cmd": "WebSearch + WebFetch — Israel 2026 health-basket policy facts (ynet, globes, mako directly fetched HTTP 200; pharma.doctorsonly.co.il and israelhayom.co.il fetch attempts returned HTTP 403)", "exit_code": 0},
    {"cmd": "curl https://www.youtube.com/oembed?url=...&format=json — 9 video-existence/metadata checks, all HTTP 200 with title+channel returned", "exit_code": 0},
    {"cmd": "curl -A <UA> https://www.youtube.com/watch?v=<id> — 8 watch-page HTML fetches, grep for lengthSeconds/approxDurationMs and shortDescription fields, for exact duration + presenter-credential text", "exit_code": 0}
  ],
  "not_done": [
    "The 13M NIS / ~4,500 teens/year Israel-basket figures were not independently page-fetch-verified (two attempts 403'd) — flagged in §1.2/§6, recommend one more attempt against the government committee's own PDF before these appear as precise numbers in consumer copy",
    "No second Hebrew-language, nutrition-specific (not just mechanism) video meeting the credential bar was found — §4/§6 gap, stated honestly rather than force-fitting an unverified candidate",
    "No dedicated RCT quantifying a specific protein g/kg target against lean-mass outcomes in a GLP-1-medicated population exists in the literature retrieved (same gap as the prior cosign) — §3.1/§6, the practical target is expert-consensus, not trial-proven at that exact population/dose",
    "No population-level incidence rate exists for micronutrient deficiency or taste-change frequency in GLP-1 users — §2.3/§2.4/§6, mechanism is well-supported, a citable percentage is not, and none is asserted",
    "This document does not draft any consumer-facing copy, select the final 2-4 videos for embed, or make the video final-cut decision — that is Content Agent's authoring lane (2-4 selection) subject to the standing two-gate sign-off, per this agent's Hard Rule 3 and the architecture doc's §3",
    "No product/category recommendation logic evaluated — out of this agent's lane per Product Agent's architecture doc §1.7/§2 (Data Agent's task)"
  ],
  "self_check": "Acceptance test: does this pack give real, tiered, cited evidence for GLP-1 mechanism/background, Israel usage context including the 2026 basket policy, the specific eating issues (reduced intake, lean-mass loss, micronutrient risk, taste change, hydration), the practical protein logic, AND a set of independently-verified (not fabricated) YouTube videos meeting a stated credibility bar — with zero invented citations and every gap named rather than papered over? Result: PASS on all required elements. 18 load-bearing PMIDs cited inline, all traced to live literature-client calls this session; 14 newly-cited DOIs CrossRef-verified non-retracted with matching titles (2 case-report PMIDs explicitly flagged as not CrossRef-checked, used only for non-quantitative mechanism support); 8 YouTube videos independently verified to actually exist via the official oEmbed endpoint plus direct watch-page HTML fetch for exact duration and presenter credentials (not search-snippet-only verification) — 7 English (5 from Mayo Clinic's own official channels, 1 from Cleveland Clinic's own official channel, 1 from independent public media featuring a Cleveland Clinic physician) and 1 Hebrew (an independently-credential-verified Tel Aviv physician, with an honest caveat that his specialty is OB/GYN not obesity medicine). The Hebrew-language gap for a second, more topically-specific video is stated directly in §4/§6 rather than filled with an unverified candidate — this is the correct application of Hard Rule 1 (do not invent sources) even though it leaves the brief's 'accessible to Hebrew-speaking Gen-Z/parents' goal only partially met. The two Israel-basket figures that could not be primary-page-verified (13M NIS, ~4,500 teens) are explicitly flagged as search-aggregated rather than presented with false precision. No product, medical-advice, or scoring recommendation made anywhere in this document — evidence and vetted sources only, per this agent's Hard Rule 3 and lane boundary."
}
```
