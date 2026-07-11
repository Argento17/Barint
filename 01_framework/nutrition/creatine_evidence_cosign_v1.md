# Creatine Evidence Base — Nutrition Co-Sign v1 (TASK-492C / TASK-492B)

**Type:** Nutrition Agent co-sign — vetted evidence base + scoring/annotation approach.
**Status:** ISSUED. This document is the corrected spine the comparison page (492C) and
blog (492B) build from. It does not write consumer copy and does not build the page.
**Input:** `03_operations/reports/research/creatine_evidence_verification_v1.md` (Research
verification, RETURNED) — every correction it flags is baked into this document.
**Scores affected:** None. This is a new supplement-comparison page + a food-page
annotation lane (per `functional_dose_ingredient_ruling_v1.md`), not a BSIP2 change.
**Author:** Nutrition Agent
**Date:** 2026-07-03

---

## 0. What changed from the raw research pack (do not re-introduce these)

The two source PDFs and the owner's pasted synthesis are themselves AI-generated
secondary literature reviews (confirmed by Research: ChatGPT headers, bracket-citation
artifacts, `[cite: N]` placeholders). Four corrections are load-bearing and are applied
throughout this document, not just noted:

1. **Hypertrophy/lean-mass meta-analysis = 12 studies, +1.14 kg LBM (95% CI 0.69–1.59),
   PMID:39074168.** The "35 studies" figure is unsupported by the actual abstract and is
   dropped entirely.
2. **No 2021 ISSN creatine update exists.** The only verified 2021 ISSN position stand
   (PMID:34503527) is about sodium bicarbonate, mentioning creatine only in passing.
   The sole citable ISSN authority is the **2017 position stand, PMID:28615996 only**
   — and its PubMed-supplied DOI (`10.1016/S0278-5919(05)70173-3`) is wrong (resolves to
   an unrelated 1999 paper). **Cite by PMID, never by that DOI.**
3. **Dairy-matrix stability is qualitative only.** No specific retention percentage
   (56–60%/35 weeks, <5% heat loss, 10% at 4°C, 12–21% in 3 days, up to 90% in 45 days)
   is confirmed against primary full text. The real, verified paper (Uzzan et al. 2007,
   PMID:17995798, *J Food Sci*) is cited for the qualitative fact only.
4. **Tnuva GO = creatine is false and OUT entirely.** Direct Shufersal scrape
   (2026-07-03) shows Tnuva's only live GO SKU is **GO Collagen Iced Coffee**
   (collagen 1.48%, barcode 7290116935607) — no creatine. The dairy creatine that
   genuinely exists on-shelf is **Yoplait GO (יופלה גו)**, 2 SKUs, **both undisclosed
   dose** (one shows a 0.6% formulation figure with no serving size to convert; one
   shows no figure at all).

---

## 1. Vetted evidence base by claim

Evidence-tier definitions per Hard Rule 6: **Strong** (multiple independent, well-powered
meta-analyses/RCTs, consistent direction) / **Moderate** (real effect, narrower or
population-specific evidence, or mechanistic markers only) / **Weak** (directionally
suggestive, small/heterogeneous/contested evidence) / **Insufficient** (no credible
studied endpoint matching the claim).

| # | Claim | Tier | Confidence | Key citation(s) | Consumer-safe one-line framing | Safe to state confidently? |
|---|---|---|---|---|---|---|
| 1 | Strength & power with resistance training | **Strong** | VERIFIED-primary | PMID:28615996 (ISSN 2017); PMID:39519498, 37432300, 39074168, 34836013, 24576864 | "One of the best-replicated effects in sports-nutrition research: creatine plus resistance training increases strength beyond training alone." | Yes |
| 2 | Lean mass with resistance training | **Strong** | VERIFIED-primary | PMID:39074168 — **+1.14 kg LBM (95% CI 0.69–1.59), 12 studies** | "A 2024 meta-analysis of 12 studies found an average lean-mass gain of about 1.1 kg beyond training alone." | Yes — with the corrected number (12 studies, not 35) |
| 3 | High-intensity/repeated-sprint performance | **Moderate-to-Strong** | corroborated | ISSN 2017 position stand | "Supports repeated short, high-intensity efforts (sprints, HIIT-style intervals) — a well-established but less individually-quantified benefit than strength." | Yes, hedged to "supports" rather than a specific number (no dedicated meta-analysis PMID pulled yet) |
| 4 | Recovery — biochemical markers (CK/LDH) | **Moderate** | corroborated (Jiao et al. 2021, not independently re-verified) | cited both PDFs | "May reduce blood markers of muscle-damage stress after hard training." | Hedge — do not claim faster recovery, only marker change |
| 5 | Recovery — functional return to performance | **Weak** | corroborated (Santos et al. 2022 "paradoxical effect," not independently re-verified) | cited PDF #1 | Do not publish a standalone recovery-speed claim. | No — must not conflate with #4 |
| 6 | Cognitive — sleep-deprived / vegetarian / older / low-baseline populations | **Moderate** | corroborated | EFSA 2024 critique + both PDFs | "In specific groups — the sleep-deprived, vegetarians, older adults — some studies show a cognitive benefit." | Hedge — population-specific only, never generalize |
| 7 | Cognitive — general healthy omnivorous adults | **Weak/Insufficient** | corroborated | Same EFSA 2024 critique | Do not claim a general cognitive benefit. | No |
| 8 | Fat loss / fat burning | **Insufficient** | VERIFIED-primary, matches dossier | dossier `claims[1]`, both PDFs agree | "No credible evidence creatine directly burns fat; body-composition change reflects lean-mass gain from training, not fat loss." | State the null clearly — this is a FAIL anchor, not a hedge |
| 9 | "Energy" (acute stimulant-style effect) | **Insufficient** | corroborated | both PDFs reject this framing | Do not use "energy" framing at all. | No |
| 10 | Anti-aging / sarcopenia support (with training) | **Weak-to-Moderate** | corroborated | both PDFs, training-dependent | "May help preserve muscle mass in older adults, but only alongside resistance training — not a passive anti-aging effect." | Hedge heavily; always attach the training-dependent qualifier |
| 11 | Mood / adjunctive depression support | **Weak** | corroborated (2025 BJN GRADE meta-analysis, "very low certainty," SMD -0.34, substantial publication bias — not independently re-verified this pass) | cited PDF #1 | Do not publish a mood-benefit claim without the safety flag attached (see §2). | No — insufficient to state as a benefit; if mentioned at all, must carry the bipolar caution in the same breath |
| 12 | Effective dose — maintenance | **3–5 g/day**, floor ~3 g/day | VERIFIED-primary (matches dossier) | ISSN 2017; dossier `effective_dose` | "The studied effective range is 3–5 g per day, taken consistently." | Yes |
| 13 | Effective dose — loading | ~20 g/day (4×5g) for 5–7 days, optional | corroborated | ISSN 2017 | "A loading phase speeds saturation but isn't required — 3–5 g/day daily gets you to the same place, just slower." | Yes |
| 14 | Form — monohydrate preferred, no alternative superior | **Strong** consensus | VERIFIED-primary | dossier `forms`; both PDFs, multiple named head-to-head trials | "Monohydrate is the form virtually all the evidence was generated on. HCl, buffered/'alkaline,' and other premium forms have no human evidence of superiority." | Yes |
| 15 | Safety — no established UL | corroborated (not primary-source-verified against ODS page text) | corroborated | 3 independent kidney-function meta-analyses (PMID:31375416, 41199218, 42035842) | "No upper limit has been established; studies up to 30 g/day for 5 years found no dose-dependent harm." | Yes, using the hedged framing (decades-of-study), not a direct "NIH says" attribution until the ODS page itself is fetched (see ship-gate §5) |
| 16 | Safety — kidney "myth" (creatinine rise ≠ renal damage in healthy kidneys) | **Strong** | corroborated | same 3 meta-analyses + FDA CAERS (203 reports, no dominant renal-harm signal) | "A common myth: creatine doesn't damage healthy kidneys. It raises a lab marker (creatinine) that's often mistaken for kidney harm, but this is well-studied and not the same thing." | Yes |
| 17 | Safety — contraindication, pre-existing renal impairment | **Established caution** | corroborated | both PDFs, standard clinical caution | "If you have existing kidney disease, talk to a doctor before use." | Yes, as a caution note, not a health claim |
| 18 | Safety — bipolar disorder / manic-switch risk | **New finding, safety flag** | corroborated (both PDFs independently) | see §2 | See §2 for the exact safety statement. | Yes, as a defensible caution — required whenever mood/depression framing (#11) appears |
| 19 | Dairy-matrix stability — qualitative | Real, qualitatively supported | corroborated, paper verified real (PMID:17995798) | Uzzan/Nechrebeki/Labuza 2007, *J Food Sci* | "Creatine is chemically unstable in liquid dairy matrices over time, especially with heat and low pH — a genuine, documented food-science formulation challenge." | Yes, qualitative only — no percentage |
| 20 | Dairy-matrix stability — quantitative | **Unverified precision** | unverified | patent WO2015078835A1 (grey lit, not peer-reviewed); PDF-quoted percentages not confirmed against primary text | Do not publish any number. | No — hard block until full-text Uzzan + patent tables are pulled |

---

## 2. New claim areas beyond the dossier — rulings

The dossier (`creatine_monohydrate.yaml`) currently has 2 ratified claims (strength/lean
mass = Strong; fat loss = Insufficient). Research surfaced 4 candidate additions. Ruling
on each:

### 2.1 Cognitive effects — USABLE, split-tier, editorial-only for now
**Ruling: usable in consumer copy, but only as two separate, population-qualified
statements (rows 6–7 above), never a single unqualified "creatine improves cognition"
line.** The EFSA 2024 statistical-correction critique (a genuine methodological finding
re-analyzing prior positive meta-analyses) is exactly the kind of nuance Bari's "no
health claims, evidence-tier honesty" posture exists to carry. **Recommend dossier
addition:** a new `claims` entry, tier split by population (Moderate for
sleep-deprived/vegetarian/older/low-baseline; Weak/Insufficient for general healthy
adults), pending formal PMID pull for the EFSA critique and the specific sleep-deprivation
RCTs Research cites but has not independently re-verified this pass.

### 2.2 Recovery — USABLE, but split and hedged, with the "paradoxical effect" caveat kept
**Ruling: the biochemical-marker claim (row 4, Moderate) is usable with a "marker" hedge;
the functional-recovery-speed claim (row 5, Weak) is NOT usable as a standalone benefit
statement.** Do not let copy compress these into one "creatine speeds recovery" line —
that is precisely the compression error Research caught in the owner synthesis
(§1 of the verification report: synthesis flattened PDF #2's "weak/mixed" framing into a
flat "Moderate"). If recovery is mentioned at all, it must carry the marker-vs-function
distinction inline. **Recommend dossier addition:** a `claims` entry for recovery,
tier "Moderate (biochemical markers) / Weak (functional return)" as one combined,
explicitly two-part entry — not two separate claims that could be cherry-picked apart in
future copy.

### 2.3 Dairy/liquid-matrix stability — KB-lane, not a claims addition
**Ruling: this is not an efficacy or safety claim — it's a food-science formulation fact
that matters for the functional-dose annotation lane** (per
`functional_dose_ingredient_ruling_v1.md` §3), not the dossier's `claims` list. Recommend
it live as a qualitative flag on the dossier (e.g., a `matrix_stability_note` field) or
in the Nutrition Reference KB, not as a scored/tiered claim — there is no consumer
"benefit" being claimed here, only a transparency-relevant formulation fact ("does the
labeled dose survive to point-of-sale in this format"). Firewall preserved: this never
moves a score.

### 2.4 Bipolar/mood contraindication — ACT NOW, required safety statement
**Ruling: this is a real, defensible safety flag and must be added to the dossier's
`safety.risky_flags` (currently `[]`).** Both source PDFs independently report a
documented risk of manic/hypomanic switching in bipolar patients using creatine
adjunctively for mood/depression. This is consistent with standard psychiatric-pharmacology
caution (any agent that can shift mood/energy state carries this class of risk in bipolar
disorder) and is corroborative rather than a single-study outlier claim.

**Recommended dossier addition** (Nutrition ruling, Product does not need to co-sign a
safety-flag addition — this is not a scoring-rule change, it is a `risky_flags` populate,
analogous to how `safety.upper_limit_UL` already documents a null value with a source):

```yaml
safety:
  risky_flags:
    - flag: "bipolar_disorder_mood_use_caution"
      context: "adjunctive use for mood/depression support in individuals with bipolar disorder"
      rationale: "Documented risk of manic/hypomanic switch; general caution in psychiatric-pharmacology practice, corroborated independently by both source reviews"
      verification_status: "candidate — recommend Research Agent PMID pull before this ships as a cited fact"
      scope: "does not apply to standard strength/lean-mass use in the general population; specific to mood/depression-use context in bipolar individuals"
```

**Defensible consumer-safe safety statement (usable now, hedged appropriately):**
> "If you have bipolar disorder, talk to a doctor before using creatine for mood support —
> there's a documented risk it can trigger manic or hypomanic episodes in this context."

This statement is scoped narrowly (bipolar + mood-use context, not general strength use),
is a caution rather than a health claim, and matches Hard Rule 5 (Bari doesn't advise on
health outcomes, but a safety caution attached to a claim area we're choosing to publish
is standard practice, consistent with row 17's kidney-caution framing). **This statement
must appear anywhere mood/depression framing (§1 row 11) is used at all** — the two are
not separable in copy.

---

## 3. Comparison-page approach (492C) — magnesium golden-standard model

Confirms the magnesium page's ranking lens generalizes to creatine with domain-specific
substitutions. **This moves NO published score.** It defines a new supplement-comparison
page (parallel structure to the magnesium page) plus the food-page annotation lane
already ruled on in `functional_dose_ingredient_ruling_v1.md`. Nothing here touches
BSIP2, `score_engine.py`, `constants.py`, or any category's published grade.

### 3.1 Ranking lens (four pillars, per the magnesium precedent)

1. **Dose adequacy** — per SIE §2.2 band structure, applied to creatine's dossier
   `effective_dose` (min_effective 3.0 g/day, typical 5.0 g/day):
   - ≥ 3 g/day of a named form → in-range, no dose penalty
   - 1.5–3 g/day → sub-therapeutic, graded by proximity (SIE's existing 50–84 band)
   - < 1.5 g/day → fairy-dust band (SIE's existing 0–34 band)
   - Loading-phase products (~20 g/day, 5–7 days) are a separate protocol, not scored
     against the maintenance floor — annotate as "loading" not "underdosed."
2. **Form** — monohydrate = evidence-based default (row 14, Strong consensus).
   Alternative forms (HCl, buffered/"alkaline," ethyl ester, citrate/malate) are not
   superior — the dossier's existing `poor` framing ("evidence-orphaned for a premium
   claim," not "chemically bad") is the correct consumer framing; do not imply the
   alternative forms are unsafe or lower-quality, only that they carry no evidenced
   advantage over the cheaper, better-studied monohydrate.
3. **Third-party testing** — NSF Certified for Sport / Informed-Sport certification is
   a genuine differentiator for the specific "will this trigger a doping test" and
   "is this what the label says" use case. This is a **verifiable, binary, label/cert-page
   fact** (not a scientific-evidence-tier question) — confirm per-product before ship,
   same discipline as any other product fact.
4. **Price-value** — cost per effective daily dose (price ÷ servings-at-3-5g), the same
   normalization the magnesium page uses. Every price is a point-in-time e-commerce fact
   and must be directly re-verified before shipping (see ship-gate §5).

### 3.2 Functional-dose annotation lane (for any dairy/food creatine that surfaces)

Per `functional_dose_ingredient_ruling_v1.md` §3.2, reused here without modification:

| Computed daily dose | Annotation verdict |
|---|---|
| ≥ 3 g/day | "Meaningful dose" |
| 1.5–3 g/day | "Partial dose" |
| < 1.5 g/day | "Decorative amount" |
| Undisclosed / blended | "Amount not disclosed" |

Applied to the actual scraped data (`functional_dairy_shelf_scrape_v1.md`): **both
Yoplait GO SKUs land in "Amount not disclosed"** — one shows only a 0.6% formulation
figure with no serving size to convert to mg/day (missing-data discard rule forbids
assuming a bottle size), one shows no figure at all. This is a real, publishable
transparency-gap finding — a stronger and more honest story than a fabricated dose
verdict would be. **No score changes; this is annotation only, exactly as the ruling
specifies.**

### 3.3 Scope correction inherited from Research (confirmed, not re-litigated here)

Tnuva GO does not belong in the comparison-page framing — it has no creatine SKU on the
live shelf. If 492C includes a dairy-creatine angle at all, it must be built around the
two Yoplait GO SKUs and the disclosure-gap finding, not a "Tnuva GO" brand-specific frame.
This Nutrition co-sign affirms Research's Spec-Conflict flag; final scope call is
Product's per the standing division of labor, but the evidence base in this document
does not support any Tnuva-creatine framing under any circumstances.

---

## 4. Dose-honesty criteria for creatine products

Applies to both the pure-supplement comparison shelf (492C) and any dairy/food product
carrying a creatine claim.

**Honest label (passes dose-honesty check):**
- States creatine **by name** (not buried in a "performance blend" or "matrix")
- States an **exact gram figure per serving** (not a %, not a range with no anchor)
- That figure is **≥ 3 g/day** at the labeled serving frequency (or is explicitly and
  correctly framed as a loading-phase product, ~20 g/day for 5–7 days)
- Form is disclosed (monohydrate is the evidence-based default; if an alternative form is
  used, that's a formulation choice, not itself a dishonesty flag — but see §3.2 form
  framing)

**Fairy-dusting (fails dose-honesty check):**
- Dose < 3 g/day of a named form, presented without qualification as if it were a
  full effective dose
- Creatine named on the label/front-of-pack but **hidden inside a proprietary blend**
  with no per-active gram figure (SIE §2.4's "blend-hiding cap" — Dose Adequacy becomes
  unknowable, not just low)
- A percentage-of-formulation figure given **with no serving size**, making the daily
  dose uncomputable (this is the exact pattern found in both Yoplait GO SKUs — flagged
  as "undisclosed," not assumed low or high)
- "Contains creatine" marketing language with **zero quantification anywhere on the
  label**, as found in one of the two Yoplait GO SKUs

This criteria set is arithmetic against the dossier's own already-ratified
`min_effective` (3.0 g/day) — it does not invent a new number.

---

## 5. Ship-gate list — must be DIRECTLY re-verified before appearing in consumer copy

Everything below is either flagged "approximate" by the source research itself, or is a
correction this document makes that has not yet been re-confirmed against a live source.
None of it may appear in blog or comparison-page copy until re-verified.

1. **Every benchmark/comparison product's dose, price, and certification claim** —
   the worldwide benchmark product table in the research pack (Thorne, Momentous,
   Optimum Nutrition, Myprotein, Bulk Nutrients, Super Effect, Alfa, etc.) was explicitly
   flagged by Research as "approximate," not independently re-verified against live
   retailer/brand pages. This includes the two Israeli products named (Super Effect,
   Alfa). **Requires a live retail-price + label-photo check, not a literature lookup.**
2. **NIH ODS's exact no-UL statement** — corroborated indirectly via 3 kidney-function
   meta-analyses, but the ODS fact-sheet page itself
   (`ods.od.nih.gov/factsheets/Creatine-HealthProfessional/`) was not directly fetched.
   Fetch before any "NIH says no UL" direct-attribution sentence ships; until then, use
   the hedged framing in row 15 (§1).
3. **The 2017 ISSN paper's correct DOI** — do not publish
   `10.1016/S0278-5919(05)70173-3` anywhere (confirmed via CrossRef to resolve to an
   unrelated 1999 paper). Cite by PMID (28615996) only, or independently confirm the
   correct DOI (candidate: `10.1186/s12970-017-0173-z`, the standard JISSN 2017 DOI
   pattern, not yet independently confirmed for this specific paper) before publishing
   any DOI at all.
4. **Recovery citations (Jiao et al. 2021; Santos et al. 2022 "paradoxical effect")** —
   both carried over from the PDFs, not independently re-verified by Research this pass.
   Verify PMIDs before these appear as cited facts (rows 4–5).
5. **2025 BJN mood/depression GRADE meta-analysis** — cited internally-consistently by
   PDF #1 (SMD -0.34, "very low certainty," publication bias noted) but not
   independently re-verified. Verify PMID before row 11 ships with a specific effect size.
6. **The EFSA 2024 cognitive statistical-critique citation and the specific
   sleep-deprivation RCTs** — both PDFs cite these consistently but Research did not
   independently re-pull the PMIDs this pass. Verify before rows 6–7 cite a specific
   paper (the tier-level claim — Moderate in specific populations, Weak generally — is
   corroborated enough to state; a specific citation is not yet nailed down).
7. **Second-retailer cross-check on the Tnuva GO / Yoplait GO finding** — only Shufersal
   was successfully scraped; Victory is bot-walled, Yochananof's search endpoint wasn't
   mapped. The "0 Tnuva creatine SKUs, 2 Yoplait undisclosed-dose SKUs" finding is
   single-retailer. Recommend a second clean retailer pass (or an owner real-world
   sighting) before the disclosure-gap headline is presented as a market-wide finding
   rather than a Shufersal-shelf finding specifically.
8. **Bipolar-contraindication PMID** — the safety flag itself (§2.4) is defensible to
   ship as a general caution statement now (it is standard, corroborated
   psychiatric-pharmacology caution, independently reported by both source reviews), but
   Research should still pull the specific supporting PMID(s) before the statement is
   framed as citing a specific study rather than general clinical caution.

**Nothing in §1's rows 1, 2, 8, 9, 12, 13, 14, 16 requires further re-verification before
shipping** — those are VERIFIED-primary or corroborated-and-internally-consistent with
independently re-checked PMIDs (per Research's verification pass) and carry no unresolved
number.

---

## 6. Constraints compliance

- No product data, ingredient list, or nutrition value invented. All product facts
  (Yoplait GO 0.6% figure, Tnuva GO collagen SKU, barcodes) are carried over verbatim
  from the direct-scrape report, not re-derived or estimated here.
- No PMID/DOI invented — every identifier in §1 and §5 traces to Research's independent
  verification pass or is explicitly flagged as "not independently re-verified this
  pass," carried at that same confidence level here, not upgraded.
- Open Food Facts not used, referenced, or considered.
- No published score changed; no BSIP2/`score_engine.py`/`constants.py` file touched.
- No consumer copy drafted — every framing line in §1/§2/§4 is a *permitted line*, not
  finished copy; Content Agent authorship + two-gate sign-off (Content + Adversarial QA)
  is still required before anything reaches the owner, per the standing hard rule.
- No subagents spawned.

---

## Return Contract

```json
{
  "task": "TASK-492C / TASK-492B",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "01_framework/nutrition/creatine_evidence_cosign_v1.md", "action": "created", "sha256": "SELF_REFERENTIAL_SEE_NOTE: embedding this file's own hash inside itself changes the hash on write, so no single value is stable; verify with `sha256sum 01_framework/nutrition/creatine_evidence_cosign_v1.md` at read time instead of trusting this field"}
  ],
  "counts": {
    "claims_vetted_with_tier_and_framing": "20/20 (source: Research verification report §5 table, 20 rows, cross-referenced 1:1 in this doc's §1)",
    "load_bearing_corrections_baked_in": "4/4 (source: Research verification report §7 consolidated list — study-count fix, 2021-ISSN-update removal, Tnuva GO removal, dairy-percentage removal — all 4 applied in §0 and threaded through §1/§3)",
    "new_claim_areas_ruled_on": "4/4 (source: Research verification report §3 escalation list — cognitive, recovery, dairy-stability, bipolar — each given a usable/not-usable ruling in this doc's §2.1-2.4)",
    "dossier_pmids_carried_without_change": "5/5 (source: creatine_monohydrate.yaml claims[0].citations, re-verified clean per Research §2e, unchanged here)",
    "ship_gate_items": "8/8 (source: this doc's §5, each item traces to a specific 'not independently re-verified' or 'approximate' flag in the Research verification report's own §7 and counts block)",
    "scores_changed": "0/0 (no BSIP2 file touched; confirmed in §3 preamble and §6)",
    "off_usages": "0/0 (banned source, never invoked, confirmed in §6)"
  },
  "commands_run": [],
  "not_done": [
    "No dossier YAML file actually edited — this document RECOMMENDS the risky_flags addition (§2.4) and two new claims entries (§2.1, §2.2) as specific, ready-to-apply YAML/tier text, but per the task brief ('recommend, do NOT edit') the actual edit to creatine_monohydrate.yaml is left for a separate, explicit follow-up action",
    "PMIDs for Jiao et al. 2021, Santos et al. 2022, the 2025 BJN mood meta-analysis, the EFSA 2024 cognitive critique, and the bipolar-contraindication source were not independently re-pulled in this pass — carried at Research's 'corroborated, not independently re-verified' confidence level, listed explicitly in ship-gate items 4-6 and 8",
    "No live retail-price/certification re-check performed on any benchmark product (Thorne, Momentous, ON, Myprotein, Bulk Nutrients, Super Effect, Alfa) — flagged as ship-gate item 1, requires a separate live-retail pass",
    "NIH ODS fact-sheet page not directly fetched — flagged as ship-gate item 2",
    "Second-retailer cross-check (Yochananof/Rami-Levy) for the Tnuva/Yoplait GO finding not performed — flagged as ship-gate item 7, inherited gap from the prior scrape report",
    "No consumer copy drafted for either 492B or 492C — out of this document's scope per task brief"
  ],
  "self_check": "Acceptance test: produce a vetted evidence base (tiered, framed per-claim), rule on 4 new claim areas including the bipolar safety flag with a defensible statement, define the 492C ranking lens confirming no score movement, define dose-honesty criteria, and produce a ship-gate list of everything requiring direct re-verification -- all corrections from the verification report baked in, no invented data, no OFF, no subagents. Result: PASS. Section 1 delivers all 20 claims from the Research verification table with an added consumer-safe framing column and a confident/hedge flag per claim. Section 2 rules on all 4 new claim areas (cognitive=usable split-tier, recovery=usable split with functional-claim block, dairy-stability=KB-lane not a claims addition, bipolar=act-now with a specific defensible safety statement and ready-to-apply YAML). Section 3 defines the 4-pillar ranking lens (dose/form/third-party-testing/price-value) plus the functional-dose annotation lane reused verbatim from the standing ruling, explicitly confirms zero BSIP2/score exposure, and reapplies the actual scraped Yoplait GO data through the annotation bands (both land 'amount not disclosed'). Section 4 gives binary honest-vs-fairy-dust criteria anchored to the dossier's existing ratified 3.0 g/day min_effective. Section 5 consolidates 8 concrete ship-gate items, each traceable to a specific unresolved flag in the Research report. All 4 load-bearing corrections (12-not-35 studies, no-2021-update, no dairy percentages, no Tnuva-creatine) are threaded through every relevant row rather than only stated once. No dossier file edited (recommendation only, per task brief). No product/PMID/DOI data invented anywhere in this document."
}
```
