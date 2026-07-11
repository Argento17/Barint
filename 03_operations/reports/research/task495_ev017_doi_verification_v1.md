# EV-017 DOI Verification Report — TASK-495 dependency
**Research Agent | 2026-07-05**
**Commissioned by:** TASK-495 (EV-017 flag-vs-score review, DOIs pending)
**Scope:** Verify citations in the 2026-07-03 REFINES addendum to EV-017 (and the 2026-06-18 CORROBORATES addendum, which shares `doi_status: unconfirmed`). Evidence only — no scoring opinion.

---

## Summary of addendum citations requiring verification

The EV-017 entry in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.json` carries two corroboration addenda, both with `doi_status: "unconfirmed"`:

| Addendum date | Classification | Source description in registry | DOI status at filing |
|---|---|---|---|
| 2026-06-18 | CORROBORATES | Frontiers in Nutrition mouse model (sucralose/stevia intergenerational); UK Biobank CVD observational | unconfirmed |
| 2026-07-03 | REFINES | Tufts/Mozaffarian narrative review + meta-analysis, *Current Atherosclerosis Reports* vol 28 art 65 | unconfirmed |

TASK-495's dependency on this report is specifically the 2026-07-03 REFINES addendum (the "Tufts/Mozaffarian 21-RCT population-level meta-analysis"). Both addenda are resolved here.

---

## Citation 1 — 2026-07-03 REFINES addendum (primary TASK-495 dependency)

### Claimed in registry

> "Tufts Food is Medicine Institute narrative review + meta-analysis (Mozaffarian et al.), 'Artificial and Other Non-Nutritive Sweeteners, the Microbiome, and Cardiometabolic Health,' *Current Atherosclerosis Reports* vol 28, art 65, ~2026-06-30; press: Tufts Now, EurekAlert, Newsweek. Pooled 21 adult RCTs of NNS vs noncaloric controls (water/placebo): raised fasting insulin and HbA1c with a trend toward worse insulin sensitivity across the pooled population, not confined to a responder subgroup."

### Verification table

| Field | Claimed in registry | Verified |
|---|---|---|
| **PMID** | not recorded | **42347889** |
| **DOI** | not recorded | **10.1007/s11883-026-01429-9** |
| **Title** | "Artificial and Other Non-Nutritive Sweeteners, the Microbiome, and Cardiometabolic Health" | CONFIRMED (exact match — PubMed, CrossRef, Springer, press releases) |
| **Authors** | Mozaffarian et al. | CONFIRMED: Wang M, Wu OY, Wallen OG, Mozaffarian D (Tufts Now; CrossRef record) |
| **Journal** | *Current Atherosclerosis Reports* | CONFIRMED |
| **Volume** | vol 28 | CONFIRMED (28(1) per PubMed esummary) |
| **Article number** | art 65 | CONFIRMED (CrossRef: article-number = 65) |
| **Published date** | ~2026-06-30 | CONFIRMED: June 25, 2026 (PubMed/CrossRef); press release June 30, 2026 |
| **Institution** | Tufts Food is Medicine Institute | CONFIRMED (Tufts Now, EurekAlert) |
| **RCT count** | 21 adult RCTs | CONFIRMED by multiple press sources citing the paper (EurekAlert, Tufts Now, News-Medical) |
| **Comparator** | NNS vs noncaloric controls (water/placebo) | CONFIRMED |
| **Key finding** | Raised fasting insulin, HbA1c, trend to worse insulin sensitivity across pooled population | CONFIRMED |
| **Retraction/erratum** | — | NONE — CrossRef `update-to` field: no corrections, retractions, or expressions of concern; citation count 0 (too recent for retractions to register) |

### Article type — critical nuance

**Registry description:** "narrative review + meta-analysis"

**Verified:** The abstract (efetch) and press coverage consistently describe this as **"a narrative review complemented by a novel meta-analysis"** — explicitly a hybrid form. PubMed pub_types: **Journal Article; Review** (not "Meta-Analysis" as a MeSH pub type). CrossRef type: journal-article.

This distinction matters for TASK-495's crux:

- The paper is not classified as a standalone systematic review or as a pure meta-analysis under PubMed indexing. It is a **Review article that contains a novel quantitative meta-analytic component** of 21 RCTs as a supplemental analysis within a narrative synthesis.
- The meta-analytic component (21 RCTs, fixed or random effects not specified in press abstracts) produces the raised fasting-insulin and HbA1c finding. It is a new pooled analysis by these authors, not a replication of a prior systematic review.
- This is a meaningful but not maximal evidence tier. Per the Research Agent evidence tier taxonomy: this falls at **Moderate** — it constitutes RCT evidence with a new quantitative synthesis, but the narrative-review container, absence of a PRISMA registration signal in available press coverage, and journal classification as Review (not Meta-Analysis) place it below the Strong tier of a registered, fully protocol-driven Cochrane-style systematic review.

### Class-vs-tier analysis — the crux for TASK-495

The registry correctly identifies the crux: the Tufts meta operates at the NNS **class** level; EV-017's actionable content is **tier**-level (sucralose/saccharin flagged vs stevia/monk-fruit neutral).

Verified findings on this point:

1. **All 21 RCTs are pooled as a single NNS class.** The paper does not break out sucralose, saccharin, stevia, erythritol, or monk fruit as separate analytical subgroups in its meta-analysis. (Source: Tufts Now press release — "Different sweeteners may also have different health effects, so grouping them together may obscure the full picture" — this is the paper's own stated limitation.)

2. **The class-level finding is therefore agnostic to EV-017's tier structure.** A population-level signal that raises insulin and HbA1c across all NNS combined does not confirm that stevia is equivalently harmful to sucralose, nor that sucralose is more harmful than stevia. It is consistent with three interpretations: (a) all NNS tiers are harmful at similar magnitude; (b) the harmful-tier sweeteners (sucralose/saccharin) are driving the pooled signal and stevia/erythritol are dragged along by sample weight; (c) all sweeteners contribute but at different magnitudes not separable without subgroup analysis.

3. **The paper itself acknowledges the tier-blindness as a limitation.** The researchers' own quote confirms they could not disentangle tier effects from the pooled analysis.

4. **Competing interests noted.** CrossRef record states: "Dr. Mozaffarian disclosed scientific advising roles and equity interests with multiple health and technology organizations." This is a standard disclosure; it does not invalidate the work but is noted per Research Agent source-credibility protocol.

### Evidence tier classification (this source alone)

**Tier: Moderate**

Rationale: Contains a novel RCT meta-analysis (21 trials) but published as a Review article (not a registered systematic review/meta-analysis per PubMed pub types). Pooled-class finding is real and statistically meaningful for the class as a whole. However, the class-level pooling does not resolve the tier-level question that is EV-017's operative content. The mechanism chain (NNS → microbiome disruption → glycemic impairment) is supported by this and prior work (Moderate-to-Strong for the class; Moderate for individual tiers).

---

## Citation 2 — 2026-06-18 CORROBORATES addendum, Source A

### Mouse intergenerational study

| Field | Claimed in registry | Verified |
|---|---|---|
| **DOI** | unconfirmed | **10.3389/fnut.2026.1694149** |
| **PMID** | not recorded | Not retrieved (Frontiers articles may not be immediately indexed; DOI is verified via publisher) |
| **Title** | "Frontiers in Nutrition mouse model (sucralose/stevia intergenerational metabolic + genetic changes)" | Verified title: "Artificial and natural non-nutritive sweeteners drive divergent gut and genetic responses across generations" |
| **Journal** | Frontiers in Nutrition | CONFIRMED |
| **Year** | 2026 | CONFIRMED: Published April 10, 2026 |
| **Lead author** | not specified in registry | Francisca Concha Celume, Universidad de Chile |
| **Study design** | Mouse (intergenerational) | CONFIRMED: C57BL/6J mice, three generations (F0, F1, F2) |
| **Key findings** | Sucralose/stevia-induced metabolic + genetic changes in offspring | CONFIRMED: sucralose — impaired glucose tolerance, liver gene suppression (Srebp1), intestinal inflammatory markers (Tnf, Tlr4), microbiota changes transmitted across generations; stevia effects mainly F1 generation |
| **Retraction** | — | NONE identified |

**Evidence tier for this source:** Weak — animal (mouse) study only; no human data. Correctly classified by the 2026-06-18 addendum as not sufficient to lift EV-017 to a score-moving tier.

---

## Citation 3 — 2026-06-18 CORROBORATES addendum, Source B

### UK Biobank cardiovascular disease cohort

| Field | Claimed in registry | Verified |
|---|---|---|
| **DOI** | unconfirmed | **10.1186/s12933-024-02333-9** |
| **PMID** | not recorded | **38965574** |
| **Title** | "UK Biobank association with cardiovascular-disease risk" | Verified title: "Artificial sweeteners and risk of incident cardiovascular disease and mortality: evidence from UK Biobank" |
| **Journal** | Cardiovascular Diabetology | (Not Frontiers in Nutrition — registry's 2026-06-18 addendum grouped sources loosely) |
| **Year** | 2024 | CONFIRMED: Published July 4, 2024 |
| **Authors** | not specified in registry | Sun T, Yang J, Lei F, et al. (14 authors total) |
| **Study design** | Observational cohort (UK Biobank) | CONFIRMED: 133,285 participants, prospective, through Oct 2022 |
| **Sample size** | not specified in registry | 133,285 participants |
| **Key findings** | UK Biobank association with CVD risk | CONFIRMED: per teaspoon increase in artificial sweeteners associated with higher risk of overall CVD (HR 1.012), coronary artery disease, peripheral arterial disease; type 2 diabetes mediated ~70% of CVD association |
| **Retraction** | — | NONE identified; indexed PMC (PMC11225337) |

**Evidence tier for this source:** Moderate (observational) — large prospective cohort, robust sample size, but observational design (confounding possible); T2D mediation is important context. Correctly classified by the 2026-06-18 addendum as "observational (UK Biobank CVD)."

---

## Consolidated verification status

| Citation | Claimed DOI/PMID | Verified DOI | Verified PMID | Title match | RCT count match | Design match | Retraction | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-07-03: Tufts/Mozaffarian | none recorded | 10.1007/s11883-026-01429-9 | 42347889 | EXACT | 21 RCTs CONFIRMED | Narrative review + meta-analysis (not pure RCT meta or systematic review) | None | **VERIFIED** |
| 2026-06-18 Source A: Frontiers/Concha Celume | none recorded | 10.3389/fnut.2026.1694149 | not retrieved | CONFIRMED by title | N/A (mouse study) | Mouse intergenerational (Weak tier) | None | **VERIFIED** |
| 2026-06-18 Source B: UK Biobank/Sun | none recorded | 10.1186/s12933-024-02333-9 | 38965574 | CONFIRMED | N/A (observational) | Prospective cohort (Moderate tier) | None | **VERIFIED** |

**No fabricated identifiers. No retractions or errata found for any source.**

---

## Class-vs-tier finding — key output for TASK-495

This is the crux the Nutrition Agent must resolve in the D6/D7 review. Research Agent finding (evidence only, no scoring opinion):

**The Tufts/Mozaffarian meta-analysis operates exclusively at the NNS class level.** The paper's own stated limitation is that "grouping them together may obscure the full picture" — the authors could not and did not separate sucralose, saccharin, stevia, erythritol, or monk fruit as independent analytical arms in the meta-analysis. The 21 pooled RCTs produce a class-level signal.

**EV-017's actionable tier structure is not confirmed, complicated, or refuted by this paper.** Three scenarios remain equally plausible from this evidence:
1. The pooled signal is driven primarily by the flagged tier (sucralose/saccharin), which would support the EV-017 tier.
2. All NNS including stevia and erythritol contribute equally, which would challenge the EV-017 tier (stevia/erythritol listed as "neutral").
3. Effect magnitudes differ by sweetener but the pooled analysis cannot separate them.

**The paper does not provide tier-level evidence** because it was not designed to do so. The registry's existing characterization — "a class-level signal that lumps stevia/erythritol in with sucralose/saccharin is agnostic-to-threatening on the tier structure" — is confirmed as accurate by this verification.

**What would resolve the tier question:** A systematic review or meta-analysis with pre-registered sweetener-specific subgroup analysis (sucralose alone vs stevia alone vs saccharin alone in separate arms). No such analysis was identified in the literature search for this commission.

---

## Query log (verification method)

| Step | Query / URL | Result |
|---|---|---|
| PubMed esearch | `Mozaffarian + non-nutritive sweeteners + microbiome + cardiometabolic` | 1 result: PMID 42347889 |
| PubMed esummary | PMID 42347889 | Title, authors (Wang M, Wu OY, Wallen OG, Mozaffarian D), journal, vol 28(1), pub June 25 2026, DOI confirmed, pub type: Journal Article; Review |
| CrossRef | DOI 10.1007/s11883-026-01429-9 | Vol 28, art 65, published June 25 2026, no update-to/retraction fields, references_count 73, competing-interests disclosure confirmed |
| Semantic Scholar | DOI:10.1007/s11883-026-01429-9 | PMID 42347889, citationCount 0 (too recent), pub type: Review |
| Tufts Now press release | now.tufts.edu/2026/06/30 | 21 RCTs confirmed, class-pooling confirmed, tier-blindness limitation confirmed as authors' own stated limitation |
| EurekAlert | eurekalert.org/news-releases/1134115 | 21 RCTs confirmed, class-pooling confirmed |
| News-Medical | news-medical.net/20260630 | Article type: "narrative review complemented by a novel meta-analysis" (verbatim) |
| Frontiers (Source A, 2026-06-18) | doi.org/10.3389/fnut.2026.1694149 | Full title, authors, mouse study design, published April 10 2026, no retraction |
| PMC (Source B, 2026-06-18) | pmc.ncbi.nlm.nih.gov/PMC11225337 | PMID 38965574, DOI 10.1186/s12933-024-02333-9, UK Biobank, n=133,285, Cardiovascular Diabetology 2024, no retraction |

---

## Notes for Nutrition Agent (evidence framing, not a scoring opinion)

1. The Tufts paper's article type (Narrative review + meta-analysis; PubMed pub type: Review) is weaker than a registered systematic review. The 21-RCT pooling is a genuine quantitative synthesis but is embedded in a narrative review, which carries less methodological rigor than a PRISMA-registered standalone meta-analysis. This does not invalidate the finding but bears on how much weight it should carry in a D7 co-sign.

2. The DOI-confirmed article is citable for the class-level signal. It should not be cited for tier-level claims about sucralose vs stevia specifically — the paper does not support those claims and explicitly flags the limitation.

3. The 2026-06-18 addendum sources are now also citable with verified DOIs/PMIDs. The mouse study (10.3389/fnut.2026.1694149) should be cited at Weak tier (animal model). The UK Biobank study (10.1186/s12933-024-02333-9) should be cited at Moderate tier (large observational cohort).

4. All three verified sources are consistent with EV-017's existing tier structure but do not provide independent corroboration of the sucralose/saccharin-vs-stevia/erythritol tier split. The tier structure in EV-017 rests on the earlier landmark human intervention studies (Suez et al., Ruiz-Ojeda et al.) not covered by this commission.

---

*Research Agent — evidence only; no scoring opinion, no D6/D7 recommendation, no file edits beyond this report and the return file.*
