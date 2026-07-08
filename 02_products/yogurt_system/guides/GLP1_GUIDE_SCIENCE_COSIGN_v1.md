# GLP-1 High-Protein Yogurt Guide — Hero Claims Evidence Verification v1 (TASK-504A / GATE-2 RT-2)

**Type:** Research Agent evidence verification — citation sourcing + evidence-tier
classification for two hero-section scientific claims. Not a co-sign of consumer copy,
not a build, not a scoring change.
**Status:** ISSUED. Answers Adversarial QA GATE-2 finding RT-2 (no on-disk evidence
citation for two hero sentences on a medication-adjacent guide; this topic was
previously BLOCKED on a different corpus partly for "a medication frame over-claiming
authority," so the evidence bar here is high).
**Input:** `02_products/yogurt_system/guides/glp1_dairy_guide_COPY_DRAFT_v1.json`
(`intro` field, read for exact phrasing only — not edited), the project's `literature`
client (`integrations/clients/literature.py`, PubMed E-utilities + Europe PMC backends)
and `crossref` client (`integrations/clients/crossref.py`, retraction/integrity check).
**Author:** Research Agent
**Date:** 2026-07-08

---

## 0. The two claims as currently written (verbatim, from the live draft)

Hebrew source (`glp1_dairy_guide_COPY_DRAFT_v1.json` line 15, `intro` field):

> "תרופות מדכאות תיאבון מסוג GLP-1 הפכו נפוצות בשנים האחרונות. מחקרים מתעדים שבין 25 ל-39
> אחוז מהמשקל שיורד בשימוש בהן הוא רקמת שריר. תיאבון מדוכא מקשה לאכול מספיק חלבון ביום,
> וצריכת חלבון של כ-1.2 גרם לכל קילוגרם ממשקל הגוף ומעלה קשורה בספרות המדעית לשימור מסת
> שריר."

English claims as briefed (confirmed to match the Hebrew above):

1. **"25 to 39 percent of weight lost while using GLP-1-class appetite-suppression
   medications is lean muscle tissue, not fat."**
2. **"Protein intake of approximately 1.2 g/kg body weight or more is associated in the
   scientific literature with lean muscle mass preservation."**

---

## 1. Claim 1 — "25 to 39 percent of weight lost is lean muscle tissue"

### 1.1 Verdict: DEFENSIBLE AS WRITTEN — a direct, near-exact primary source exists

This is the strongest possible outcome for a citation-verification pass: the "25 to 39
percent" figure is not an approximation or a force-fit — it is very likely the **actual
reported range from a specific, real, recent, high-quality meta-analysis**, retrieved
independently via the `literature` client (not supplied by the brief, not assumed):

> **PMID:41877354** — Lean Mass Changes With Incretin Therapy Versus Lifestyle
> Intervention: A Systematic Review and Meta-Analysis of Randomised Controlled Trials.
> *Diabetes, Obesity and Metabolism*, 2026. DOI: `10.1111/dom.70666`.
> **20 RCTs, 15,782 participants.** Semaglutide, tirzepatide, liraglutide, and lifestyle
> interventions, body composition measured by DXA or MRI, GRADE-assessed.
>
> Direct quote from the abstract (verified via PubMed efetch, not paraphrased):
> **"Lean mass constituted 25%-39% of total weight lost with incretin agonists:
> semaglutide (35.2% [95% CI: 31.5-38.9]), tirzepatide (25.4% [22.8-28.0]) and
> liraglutide (26.8% [23.1-30.5])."**

The claim's exact numeric band (25-39%) matches this paper's reported range almost
verbatim — the lower bound (25%) is tirzepatide's point estimate (25.4%), and the upper
bound (39%) sits at the top of semaglutide's 95% CI (38.9%, rounds to 39%). This is a
**2026 publication, 15,782 participants, GRADE-evaluated, three-drug breakdown** — one of
the largest and most current body-composition meta-analyses in this literature.

**Integrity check (CrossRef, `crossref.get_doi`):** DOI `10.1111/dom.70666` resolves,
title matches exactly, publisher Wiley, `is_retracted: False`, 49 references (not a thin
reference list), `cited_by_count: 5` (young paper, expected for a 2026 publication).
Confirmed real, not retracted, not a mismatched/fabricated identifier.

### 1.2 Corroborating evidence (independent triangulation, not just one paper)

The 25-39% range is not an isolated finding — three additional independent, real,
CrossRef-verified sources converge on the same order of magnitude:

| PMID | Study | Design | Finding |
|---|---|---|---|
| **39719170** | Effect of GLP-1RAs and co-agonists on body composition (*Metabolism*, 2025) | Systematic review + network meta-analysis, 22 RCTs, 2258 participants | Lean mass loss = MD -0.86 kg vs total weight MD -3.55 kg → **~25%** of total weight loss (authors' own framing: "approximately 25%") |
| **42319968** | GLP-1RA and SGLT2i effects on lean body mass (*Diabetes/Metab Res Rev*, 2026) | Systematic review + meta-analysis, 36 studies (21 GLP-1RA) | Lean mass = **28% (95% CI: 22%-34%)** of overall weight loss — CI band overlaps the 25-39% claim directly |
| **41996180** | Effect of Incretin-Based and Nonpharmacologic Weight Loss on Body Composition (*Annals of Internal Medicine*, 2026) | Systematic review, 35 primary studies | Uses **~25% as the prespecified field benchmark** for FFM/LST proportion, then finds actual trials **exceed this benchmark in ~2/3 of incretin-based interventions** — i.e., real-world figures commonly land *above* 25%, consistent with a range that extends up toward the high-30s |
| **38937282** | Changes in lean body mass with GLP-1-based therapies (*Diabetes Obes Metab*, 2024) | Narrative review | Explicitly flags heterogeneity: **some trials report 40-60%**, others **~15% or less** — confirms the true individual-study range is wider than any single point estimate, and that reported figures well above 39% also exist in the literature (a reason not to overstate precision, see §1.4) |

All four DOIs independently CrossRef-verified: `10.1016/j.metabol.2024.156113`,
`10.1002/dmrr.70194`, `10.7326/ANNALS-25-00478`, `10.1111/dom.15728` — none retracted, all
titles match, all real journal-article records.

### 1.3 Evidence tier: **Moderate-to-Strong**

Multiple independent, well-powered systematic reviews/meta-analyses (2025-2026,
combined n well over 18,000 participants across the corroborating set), consistent
direction, plausible and well-established mechanism (obligatory fat-free-mass loss
accompanies any substantial caloric-deficit-driven weight loss; GLP-1-induced anorexia
produces an unusually large and rapid deficit). Not "Strong" outright because: (a) study
designs are heterogeneous (RCT durations, populations — obesity vs T2D vs T1D vs PCOS —
and measurement methods DXA/MRI/BIA are pooled together in some of the corroborating
analyses), and (b) the primary source itself reports real per-drug variance (25.4% to
35.2%) rather than one converged number — meaning "25 to 39%" is honestly a **range of
drug-specific averages**, not a single tight estimate.

### 1.4 One caveat to carry forward, not a defect in the claim

The 25-39% figure describes the **proportion of total weight lost that is lean mass** —
not the proportion of a person's *starting* lean mass that disappears, and not the
change in lean-mass-as-percentage-of-remaining-body-weight (a different, sometimes
opposite-signed metric: PMID:42321502, a smaller 2026 systematic review of 7 studies/821
patients, found lean mass *as a share of total body weight* can rise slightly even as
absolute lean mass falls, because fat mass falls faster in proportion). **The draft
Hebrew copy already uses the correct framing** ("מהמשקל שיורד" = "of the weight that is
lost," matching the studies' own metric) — this is noted here only so a future editor
does not accidentally swap in the different, easily-confused metric.

Also worth naming: PMID:41877354 (the primary source) found lifestyle-only weight loss
produces a **comparable** proportional lean-mass loss (26.2%) to incretin therapy, and
that resistance training specifically (not incretin avoidance) is what meaningfully
improves the ratio (17.5%). This does not weaken the claim as written — the claim only
states what proportion is lean tissue, not that GLP-1 drugs are uniquely worse than any
weight loss method — but it is useful context if the guide's broader narrative ever
implies GLP-1-specific blame rather than a general caloric-deficit phenomenon.

---

## 2. Claim 2 — "~1.2 g/kg protein or more is associated with lean muscle mass preservation"

### 2.1 Verdict: DEFENSIBLE AS WRITTEN, with an honest scope note (extrapolated, not GLP-1-population-RCT-proven at this exact dose)

The claim is phrased carefully — "associated in the scientific literature" — and that
phrasing is accurate to what the evidence actually shows: **1.2 g/kg/day is a
real, widely-cited threshold in the general caloric-restriction/weight-loss protein
literature**, and it is **also the specific figure a GLP-1-focused review recommends**,
but I did not find a dedicated randomized dose-response trial that tested 1.2 g/kg/day
specifically *in GLP-1 users* and measured lean-mass outcomes. The claim does not assert
that such a trial exists (it says "the scientific literature," not "GLP-1 trials
specifically") — so no wording change is required, but the guide should not be extended
in future copy to imply GLP-1-population-specific RCT proof at this exact dose.

### 2.2 Evidence, general caloric-restriction/weight-loss literature (Moderate tier)

| PMID | Study | Design | Finding |
|---|---|---|---|
| **25926512** | The role of protein in weight loss and maintenance (*Am J Clin Nutr*, 2015, Leidy et al.) | Narrative review, widely cited (392 citations per CrossRef) | States that higher-protein weight-loss diets in the **1.2-1.6 g/kg/day** range show "greater weight loss, fat mass loss, and preservation of lean mass" than lower-protein energy-restriction diets across multiple meta-analyses of controlled feeding studies |
| **31794597** | Protein Intake Greater than the RDA... (*Advances in Nutrition*, 2020) | **Systematic review + meta-analysis**, 18 studies / 22 comparisons, ≥6-week RCTs in healthy adults | Protein intake above the RDA (0.8 g/kg) **significantly attenuates lean-mass loss during energy restriction**: WMD +0.36 kg (95% CI: 0.06-0.67), n=14 comparisons. This is the single best-controlled, most directly quantitative source for the general mechanism the claim describes |
| **30806592** | Optimal Protein Intake during Weight Loss Interventions in Older Adults with Obesity (*J Nutr Gerontol Geriatr*, 2019) | Review | States the 0.8 g/kg RDA "may be inadequate" for lean-mass preservation during structured weight loss; does not pin one exact replacement number but supports the above-RDA framing |
| **30629126** | Energy-Restricted, Higher Protein Meal Plan on Body Composition... Older Adults (*J Gerontol A*, 2019) | RCT, 96 older adults, DXA | Used a **1.2-1.5 g/kg/d** protein target; weight-loss group lost 87% of total mass as fat, with lean-mass loss not significantly different from the weight-stable control group — directionally supportive but shows protein alone (without resistance training) does not fully eliminate lean loss, a useful hedge against overstating the claim |

CrossRef-verified: `10.3945/ajcn.114.084038` (Leidy 2015) and `10.1093/advances/nmz106`
(2020 systematic review) both resolve, not retracted, titles match exactly.

### 2.3 Evidence specific to the GLP-1 context (Weak-to-Moderate — extrapolated, with one direct expert-recommendation source)

> **PMID:42303931** — GLP-1 Receptor Agonists for Obesity Management in Older Adults: A
> Scoping Review on the Risk of Sarcopenia and Sarcopenic Obesity. *Current Nutrition
> Reports*, 2026.
>
> Direct quote: **"Integrating GLP-1 RA therapy with tailored resistance exercise and
> caloric restriction with dietary counseling, including adequate protein intake
> (1.2-1.6 g/kg/day), may help preserve muscle mass and function in older adults."**

This is a genuine, real, GLP-1-specific source using the *exact same 1.2 g/kg floor* as
the claim — but it is a **scoping review** (a lower-rigor review type than a systematic
review or meta-analysis) making a **recommendation**, not reporting a **trial result**.
It is evidence that the 1.2 g/kg figure is the expert-consensus transplant of the
general weight-loss protein literature into the GLP-1 context — not evidence that a
GLP-1-population RCT has specifically validated 1.2 g/kg as sufficient or optimal in
GLP-1 users. PMID:41877354 (the same paper anchoring Claim 1) independently concludes
"muscle mass can be significantly preserved by integrating resistance training, adequate
protein intake, and body composition monitoring" but does not name a specific gram
figure in its abstract — directionally consistent, not independently quantitative for
this claim.

**No dedicated randomized dose-response trial testing a specific protein g/kg target
against lean-mass outcomes in a GLP-1-medicated population was found in this search
pass.** This is a real evidentiary gap, not a defect in the claim as phrased — the claim
correctly hedges to "the scientific literature" (general) rather than asserting
GLP-1-specific proof.

### 2.4 Evidence tier: **Moderate** (general weight-loss/caloric-restriction population), **Weak-to-Moderate** (GLP-1-specific — extrapolated + one scoping-review-level direct recommendation, no direct RCT)

---

## 3. Overall verdict on the two hero sentences

**Both sentences are defensible as currently phrased. No wording change is required.**
This is a stronger outcome than the task brief anticipated ("if the numbers need
adjustment, say so explicitly") — in this case they do not need adjustment, because a
direct, high-quality, recently published (2026) meta-analysis with the near-exact
reported range (25%-39%, drug-specific breakdown 25.4%-35.2%, CI extending to 38.9%) was
independently located and CrossRef-verified as real and non-retracted. The protein claim
is honestly scoped ("associated in the scientific literature," not "proven in GLP-1
trials") and that scoping matches what the evidence actually supports.

**Recommended action for whoever finalizes the guide's citation footnotes (Content
Agent / Product, not this document):** cite **PMID:41877354** as the primary source for
Claim 1, and **PMID:31794597** (general mechanism, systematic review + meta-analysis)
plus **PMID:42303931** (GLP-1-specific recommendation, scoping review) for Claim 2, with
the scope distinction preserved (general-population trial evidence vs. GLP-1-context
expert recommendation) if a footnote or "מקורות" section is added. This document does
not draft that footnote text — that is Content Agent's authoring lane, subject to the
standing two-gate sign-off.

---

## 4. Full citation list (ranked by relevance to the two claims; all PMIDs independently retrieved via `literature.pubmed`/`pubmed_fetch`, all DOIs CrossRef-verified not retracted)

| # | PMID | Citation | Tier for its claim | Verified real (CrossRef) |
|---|---|---|---|---|
| 1 | 41877354 | Lean Mass Changes With Incretin Therapy Versus Lifestyle Intervention: A Systematic Review and Meta-Analysis of RCTs. *Diabetes Obes Metab* 2026. DOI 10.1111/dom.70666 | **Primary source, Claim 1** | Yes — not retracted, 49 refs |
| 2 | 39719170 | Effect of GLP-1RAs and co-agonists on body composition: SR + network meta-analysis. *Metabolism* 2025. DOI 10.1016/j.metabol.2024.156113 | Corroborating, Claim 1 | Yes — not retracted, 74 refs |
| 3 | 42319968 | Effects of GLP-1RAs and SGLT2i on Lean Body Mass in Humans: SR + meta-analysis. *Diabetes Metab Res Rev* 2026. DOI 10.1002/dmrr.70194 | Corroborating, Claim 1 | Yes — not retracted, 78 refs |
| 4 | 41996180 | Effect of Incretin-Based and Nonpharmacologic Weight Loss on Body Composition: SR. *Ann Intern Med* 2026. DOI 10.7326/ANNALS-25-00478 | Corroborating, Claim 1 | Yes — not retracted, 140 refs |
| 5 | 38937282 | Changes in lean body mass with GLP-1-based therapies and mitigation strategies. *Diabetes Obes Metab* 2024. DOI 10.1111/dom.15728 | Heterogeneity context, Claim 1 | Yes — not retracted, 94 refs |
| 6 | 42321502 | GLP1-RA muscle health: SR + meta-analysis of RCTs. *Int J Obes* 2026 | Metric-distinction caveat, §1.4 | Not independently CrossRef-checked this pass — PMID/abstract retrieved via `literature.pubmed`, treat as corroborated-not-independently-verified until re-checked |
| 7 | 31794597 | Protein Intake Greater than the RDA... SR + meta-analysis. *Adv Nutr* 2020. DOI 10.1093/advances/nmz106 | **Primary quantitative source, Claim 2 (general)** | Yes — not retracted, 56 refs |
| 8 | 25926512 | The role of protein in weight loss and maintenance. *Am J Clin Nutr* 2015. DOI 10.3945/ajcn.114.084038 | Corroborating, Claim 2 (general) | Yes — not retracted, 94 refs |
| 9 | 42303931 | GLP-1RAs for Obesity Management in Older Adults: sarcopenia risk. Scoping review. *Curr Nutr Rep* 2026 | **GLP-1-specific source, Claim 2** | Not independently CrossRef-checked this pass — PMID/abstract retrieved via `literature.pubmed`, treat as corroborated-not-independently-verified until re-checked |
| 10 | 30806592 | Optimal Protein Intake during Weight Loss in Older Adults with Obesity. Review. *J Nutr Gerontol Geriatr* 2019 | Supporting context, Claim 2 | Not independently CrossRef-checked this pass |
| 11 | 30629126 | Energy-Restricted Higher Protein Meal Plan on Body Composition in Older Adults. RCT. *J Gerontol A* 2019 | Hedge/nuance, Claim 2 | Not independently CrossRef-checked this pass |

**No PMID in this document was invented.** Every PMID above was returned by a live
`pubmed_search`/`pubmed_fetch` call against NCBI E-utilities during this session, and
the six PMIDs marked "Yes" in the table were additionally cross-checked against CrossRef
by DOI (title match + `is_retracted: False` + non-trivial reference count) before being
treated as load-bearing for the primary verdict in §1 and §2.1-2.2. The five PMIDs not
yet independently CrossRef-checked are flagged explicitly rather than silently assumed
clean, per Hard Rule 6 discipline — they are corroborating/contextual, not the two
load-bearing primary sources (which are both CrossRef-verified: #1 and #7).

---

## 5. Constraints compliance

- No PMID, DOI, study finding, or figure invented anywhere in this document. Every
  number in §1-§2 traces to an abstract retrieved live via the `literature` client this
  session (not from training-data recall) and is quoted or closely paraphrased with the
  source named inline.
- No consumer copy drafted or edited. `glp1_dairy_guide_COPY_DRAFT_v1.json` was read
  only, never written to.
- No product recommendation made — this document verifies evidence and states a
  defensibility verdict; it does not decide whether/how the guide ships (that is
  Content Agent's authoring lane + the mandatory two-gate sign-off, and Product's launch
  call).
- Every claim carries an explicit evidence tier (Moderate-to-Strong for Claim 1;
  Moderate/Weak-to-Moderate split by population for Claim 2) per Hard Rule 2.
- Scope honesty preserved per Hard Rule 4/5: the GLP-1-specific vs.
  general-caloric-restriction evidentiary distinction for Claim 2 is stated explicitly,
  not blurred; no animal/in-vitro extrapolation occurs in either claim (all cited
  sources are human RCT-based systematic reviews/meta-analyses or reviews thereof).
- Open Food Facts not used, referenced, or considered anywhere in this document.
- No subagents spawned. All literature/CrossRef calls run directly via the project's
  own `integrations/clients/literature.py` and `integrations/clients/crossref.py`
  read-only clients.

---

## Return Contract

```json
{
  "task": "TASK-504A / GATE-2 RT-2",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/yogurt_system/guides/GLP1_GUIDE_SCIENCE_COSIGN_v1.md",
      "action": "created",
      "sha256": "NOTE: this file's own hash cannot be embedded without changing itself on next save; verify with `sha256sum 02_products/yogurt_system/guides/GLP1_GUIDE_SCIENCE_COSIGN_v1.md` at read time"
    }
  ],
  "counts": {
    "hero_claims_verified": "2/2 (source: this doc's headers, brief's two numbered claims, each given its own section 1 and 2 with a verdict)",
    "claims_defensible_as_written_no_reword_needed": "2/2 (source: this doc §1.1 and §2.1 verdicts, both DEFENSIBLE AS WRITTEN)",
    "load_bearing_pmids_crossref_integrity_checked": "6/6 (source: this doc §4 table, rows marked 'Yes' — 41877354, 39719170, 42319968, 41996180, 38937282, 31794597, 25926512 — actually 7 checked; denominator corrected: 7/7 CrossRef-checked DOIs, all is_retracted=False, all titles matched)",
    "corroborating_pmids_not_yet_crossref_checked": "3/3 (source: this doc §4 table rows marked 'Not independently CrossRef-checked this pass' — 42321502, 42303931, 30806592, 30629126 — actually 4; denominator corrected: 4/4, flagged explicitly not silently assumed clean)",
    "total_real_pmids_retrieved_this_session": "18 unique PMIDs returned across all pubmed_search/pubmed_fetch/europepmc calls this session (source: raw literature-client output captured during this session; 11 appear in this document's §4 citation table as directly load-bearing or corroborating, the remainder were reviewed and excluded as off-topic or duplicative)",
    "invented_or_unverifiable_citations": "0 (this document contains no PMID that was not returned by a live literature-client call this session)",
    "primary_source_exact_range_match_for_claim_1": "1/1 (PMID:41877354 reports '25%-39%' verbatim, matching the draft copy's stated range; source: §1.1 direct quote)",
    "scores_changed": "0/0 (no BSIP2/food-scoring file touched; this is a supplement/guide-context evidence document, not a food-scoring change)",
    "off_usages": "0/0 (banned source, never invoked)"
  },
  "commands_run": [
    "python literature.pubmed(...) — 5 query rounds against NCBI PubMed E-utilities (GLP-1/lean-mass queries, protein/lean-mass queries, targeted follow-up queries)",
    "python literature.europepmc(...) — 3 query rounds against Europe PMC (used to surface 2026 papers and confirm PMID 41877354's existence via title match before full pubmed_fetch)",
    "python literature.pubmed_fetch(['42319968','41877354','42303931']) — full-abstract fetch for the three highest-value candidate PMIDs",
    "python crossref.get_doi(...) — 7 DOI integrity checks (title match + is_retracted + reference count) against the load-bearing PMIDs"
  ],
  "not_done": [
    "4 corroborating/contextual PMIDs (42321502, 42303931, 30806592, 30629126) were retrieved via PubMed but not independently CrossRef-checked this pass — flagged explicitly in §4 rather than silently assumed clean; recommend a follow-up CrossRef pass before any of these four appear as a named inline citation in shipped consumer copy",
    "No full-text (only abstract-level) verification was performed for any paper — all figures in this document are drawn from PubMed-indexed abstracts, which is standard for a citation-defensibility pass but means table/figure-level precision (e.g. exact per-subgroup CIs beyond what the abstract states) has not been independently re-derived from full text",
    "No consumer-facing footnote or citation-display copy was drafted — §3 names which PMIDs Content Agent should cite and why, but authoring the actual footnote/source-line text is Content Agent's lane, still subject to the mandatory two-gate sign-off",
    "The guide draft JSON (glp1_dairy_guide_COPY_DRAFT_v1.json) was not edited — read-only, per task brief scope"
  ],
  "self_check": "Acceptance test: verify both hero claims against real, non-fabricated PMIDs; find the actual defensible range/figure rather than force-fitting to the pre-written numbers if the literature disagrees; produce a durable cosign record in the project's standard format with claim-exact-text, real PMIDs, study population/design, and an explicit as-written-defensible-or-needs-adjustment verdict; zero fabricated citations. Result: PASS, with a stronger-than-expected outcome. Claim 1's exact '25 to 39 percent' range was independently located as the near-verbatim reported finding of a real, CrossRef-verified 2026 meta-analysis (PMID:41877354, 20 RCTs, 15,782 participants) rather than needing to be force-fit or reworded — corroborated by three further independent 2025-2026 meta-analyses/systematic reviews. Claim 2's 1.2 g/kg figure is real and well-supported in the general caloric-restriction/weight-loss protein literature (systematic review + meta-analysis PMID:31794597, widely-cited review PMID:25926512) and is additionally the exact figure a GLP-1-specific scoping review (PMID:42303931) recommends as a countermeasure — but no GLP-1-population dose-response RCT at this specific threshold was found, so Claim 2 carries an honest scope caveat (general-literature-grounded, GLP-1-context extrapolated) rather than a wording change, which matches how the claim is actually phrased ('associated in the scientific literature,' not 'proven in GLP-1 trials'). Both verdicts: DEFENSIBLE AS WRITTEN, no reword required. All PMIDs traced to live literature-client calls this session; the 7 load-bearing DOIs additionally CrossRef-verified non-retracted with matching titles. No claim stated as established fact without an evidence tier. No animal/in-vitro data extrapolated to human outcomes without flagging. No safety signal omitted (none arose in this specific evidence set — this is an efficacy/mechanism verification, not a safety review). No product recommendation made; no consumer copy drafted; no scores touched; no OFF; no subagents."
}
```
