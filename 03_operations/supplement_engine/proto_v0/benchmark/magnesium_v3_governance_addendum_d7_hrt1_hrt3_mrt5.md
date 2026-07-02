# Magnesium v3 Scoring Model — D7 Governance Addendum
## Findings HRT-1 / HRT-3 / MRT-5

**Authored by:** Nutrition Agent (D7 authority)
**Date:** 2026-06-23
**Task:** TASK-384
**Status:** PROPOSED — requires Product Agent D7 co-sign before any engine implementation change
**Governs:** `magnesium_model_v3_bioav_adjusted_dose_spec.md` §1.1 (tier factors), §2.4 (safety thresholds), §1.1 (taurate classification)
**Supersedes:** None — this is a standalone addendum to the v3 spec; the v3 spec remains in force as written except where explicitly amended below.

---

## Summary of Rulings

| Finding | Severity (red-team) | Ruling | Grade movement? |
|---|---|---|---|
| HRT-1 — LOW tier factor 0.35 framing | HIGH | ACCEPTED with formal documentation. Factor stays 0.35. Addendum satisfies the "explicit documented acceptance" bar. | No |
| HRT-3 — EFSA 250mg threshold: strict > or >=? | HIGH | CHANGED to >=250. Two products gain a GI display note. No score change. | No |
| MRT-5 — Taurate MODERATE vs UNRESOLVED | MEDIUM | HELD at MODERATE with formal mechanistic justification. Taurate stays D/46.2. | No |

**Grade movements from these rulings: 0 products.**
Product Agent D7 co-sign is required before Data Agent implements HRT-3 (the >=250 operator change). HRT-1 and MRT-5 are documentation-only; they do not change engine code.

---

## Finding HRT-1 — LOW Tier Factor 0.35

### Red-team position

The v3 spec's calibration method reads (§1.2): "choose the smallest factor spread that (a) produces a clear grade-band crossing between equal-dose HIGH and LOW forms, (b) lands oxide 314mg in the C band rather than B, and (c) keeps NT-LC hydroxide 190mg in C rather than B." The red-team observes this is outcome-first calibration: the target grade (oxide ≠ B) was chosen first, and 0.35 was derived to reach it. The literature absorption ratio (oxide ~4% / citrate ~28–32%) gives a raw ratio of ~0.14, making 0.35 approximately 2.5× more lenient than a strict pharmacokinetic reading. At ~0.14, oxide-314mg would score ~D/41.

The red-team demands either: (a) formal documented acceptance that 0.35 is a calibration constant — not a pharmacokinetic fraction — and that the page must be framed as a "form-adjusted scoring model, never absorbed X mg"; or (b) recalibration to ~0.20.

### Ruling: ACCEPT 0.35; file this formal documented acceptance

**Decision:** The LOW tier factor of 0.35 is accepted and retained. The red-team's demand (a) is satisfied by this addendum. Recalibration to ~0.20 is not adopted.

**Reasoning — the calibration-constant framing is epistemically correct, not evasive:**

The raw absorption fractions (oxide ~4%, citrate ~28–32%) are population-average estimates from studies measuring fractional absorption under specific conditions (fasting, co-administration, GI pH, study design). Individual fractional absorption varies enormously — the ~4% figure for oxide comes from studies including Walker 2003, Schuette 1994, and Coudray 2005 (cited in NIH ODS context), and the range across studies is 3–7%. Asserting that "oxide delivers exactly 0.04 × dose to the body" for every person, and scoring on that figure directly, would introduce false pharmacokinetic precision that the evidence does not support.

The v3 tier factor system does something different and defensible: it assigns a relative scoring weight to each class that reflects the *direction and approximate magnitude* of the bioavailability advantage, not a point estimate of fractional absorption. The HIGH = 1.0 anchor means "full credit for the label dose" for well-absorbed forms. The LOW = 0.35 means "oxide-class products receive 35% of the dose credit per mg administered." This is explicitly not the pharmacokinetic absorption fraction — it is a calibration constant that produces a scoring outcome consistent with the literature's directional hierarchy (organic salts >> oxide).

Why 0.35 rather than something derived from the raw absorption ratio (~0.14)?

1. The goal of the scoring model is to communicate *relative form quality* at population scale, not to predict any individual's absorbed dose. A factor of 0.14 would place oxide-314mg at ~D/41 — one full grade below every premium form. That is a stronger signal than the evidence justifies: the literature shows that oxide is substantially less bioavailable, not that it provides negligible benefit or that it belongs in a categorically different band from malate (MODERATE) on any reasonable interpretation. A D grade at 314mg administered — a dose above the general dietary gap band — would mislead a consumer into thinking oxide at 314mg is as poor as a supplement with 50mg administered.

2. The 0.35 value produces a scoring outcome — oxide-314mg at C/60.0, clearly below citrate-250mg at B/72.8 — that correctly communicates the hierarchy without claiming false precision. The grade-band separation (B vs C) is the consumer signal. Within-band positioning (oxide at 60 vs citrate at 68–73) provides further differentiation for any consumer who reads the numeric score.

3. C3 (P302) reviewed the 0.45 vs 0.35 question and recommended 0.35 specifically because at 0.45 oxide-314mg (62.6) nearly tied Full-Mag bisglycinate-122mg (62.2), softly re-introducing an "oxide ≈ premium-low-dose-bisglycinate" near-equality. At 0.35 the separation is 2.2pts — honest differentiation with meaningful signal. This is the secondary calibration constraint that drove 0.45→0.35.

**The outcome-first criticism is correctly levelled but does not invalidate the result.** All calibration constants are determined partly by the outcomes they should produce — this is true of every scoring system. The question is whether the calibration produces a result that is (a) directionally consistent with the evidence hierarchy, and (b) not false-precision about mechanisms the model does not actually claim. The answer to both is yes: oxide < organic salts is the direction the evidence supports (NIH ODS; Walker 2003; Schuette 1994; Coudray 2005); and the model explicitly disavows fractional-absorption claims in consumer display (§1.3 HARD rule: never display adjusted dose; never say "your body absorbs X mg").

**Framing constraint (binding, not advisory):**

This acceptance is conditional on the following framing constraints being applied to all consumer-facing and editorial content for the v3 model. These are now part of the D7 record:

1. The scoring model is a **form-adjusted scoring model**, not an absorbed-dose predictor. Any copy, methodology text, or tooltip describing how the score works must reflect this.

2. **The phrase "your body absorbs X mg" is permanently banned from v3 consumer copy.** The display shows administered elemental mg + bioavailability class label. That is the full consumer signal.

3. Copy may say: "מגנזיום ציטראט נספג בצורה יעילה הרבה יותר מאוקסיד" (citrate is absorbed much more efficiently than oxide) — a directional, qualitative statement consistent with the literature.

4. Copy must **not** say: "הגוף שלך סופג 109 מ"ג מגנזיום" (your body absorbs 109 mg) or any number derived from the adjusted dose. The adjusted dose is internal only.

5. Methodology text, when describing the scoring approach, must include language equivalent to: "הציון מחושב לפי כמות המגנזיום שהוצהרה על האריזה, תוך התאמה לרמת ספיגת הצורה הכימית. ההתאמה מבוססת על היררכיית הספיגה המצוינת בספרות, ולא על חיזוי מדויק של ספיגה בגוף הצרכן הספציפי."

**Evidence references (inline):**

- NIH ODS Magnesium Fact Sheet (current, 2026): "Forms of magnesium that dissolve well in liquid are more completely absorbed in the gut than less soluble forms."
- Walker AF et al. (2003): Magnesium oxide vs citrate comparative absorption; oxide fractional absorption 4% range.
- Schuette SA et al. (1994): Bioavailability of magnesium diglycinate vs magnesium oxide in patients with ileal resection.
- Coudray C et al. (2005): Magnesium absorption from dietary sources in rats; comparative form data cited in NIH ODS context.

---

## Finding HRT-3 — EFSA 250mg GI Note Threshold: >250 or >=250?

### Red-team position

The v3 spec (§2.4) fires GI_NOTE_EFSA when `administered_mg > 250` (strict greater-than). Under this threshold, two products that administer exactly 250mg — Supherb Citrate+B6 (250mg) and Altman Bisglycinate 250 (250mg) — receive no GI display note. The red-team argues the EFSA 250mg supplemental threshold is the level *at which* GI concern begins, not above which — meaning >=250 is the clinically accurate operator.

### Ruling: CHANGE to >=250; no score change

**Decision:** The GI_NOTE_EFSA threshold is changed from `administered_mg > 250` (strict) to `administered_mg >= 250` (inclusive). The two 250mg B products (Supherb Citrate+B6 and Altman Bisglycinate 250) now display a GI note. No score deduction (GI_NOTE_EFSA is a display-only flag; the dossier is explicit: "Display note only; no score deduction (MVP)"). This change requires Product Agent D7 co-sign as a scoring-rule specification change (it changes displayed engine output for 2 products, even without a score change).

**Reasoning:**

The EFSA Panel on Dietetic Products, Nutrition and Allergies established 250mg/day supplemental magnesium as the threshold at which osmotic diarrhea has been observed in supplementation trials (EFSA Journal 2006; ul_note_threshold = 250 in the dossier, ul_secondary = 250). The threshold is the *onset level* — 250mg itself is the value at which the GI effect begins, not 251mg.

The magnesium dossier's `ul_note_threshold: 250` field (magnesium.yaml, safety block, Nutrition D8 ruling) defines the EFSA figure as "onset of reversible osmotic diarrhea (GI tolerance), NOT toxicity." The word "onset" describes the *boundary value itself*, not the value one above it. An inclusive threshold (>=250) correctly reflects this: the GI note is warranted *at* 250mg as well as above it.

The strict operator (>250) was almost certainly a code-convention default — `>` is the natural comparator when working with integers representing "more than X" — rather than a deliberate scientific choice. It produces a defensibility hole: a consumer taking Supherb Citrate+B6 at exactly 250mg/day could experience the GI effect the note is designed to communicate, but receives no note. That is inconsistent with the note's purpose.

**Consumer display impact:**

Supherb Citrate+B6 250mg (B/72.8) and Altman Bisglycinate 250mg (B/72.8) gain a GI display note. The note language from the v3 spec, which remains appropriate: [equivalent to] "מינון זה עשוי לגרום לאי-נוחות במערכת העיכול בחלק מהאנשים (EFSA)." No score change. Grade B is retained for both.

**Code change required (Data Agent):**

In `run_magnesium_v2.py`, the GI_NOTE_EFSA trigger line changes from:
```python
if administered_mg > 250:
```
to:
```python
if administered_mg >= 250:
```

This is the only code change required for HRT-3.

**Evidence references:**

- EFSA Panel on Dietetic Products, Nutrition and Allergies (2006): Scientific Opinion on magnesium; 250mg/day supplemental as the GI tolerance threshold.
- Magnesium dossier (magnesium.yaml) `ul_note_threshold: 250` — "EFSA supplemental GI-tolerance threshold — now the NOTE line" per Nutrition D8.

---

## Finding MRT-5 — Taurate MODERATE Classification

### Red-team position

Taurate is placed in MODERATE (factor 0.75) in the v3 spec on mechanistic grounds: "amino-acid chelate, expected to behave similarly to other organic Mg salts." The red-team observes there is no direct human absorption data for magnesium taurate — the placement is purely mechanistic inference. The alternative is UNRESOLVED (factor 1.0 + evidence sub-score penalty −20), which would move Nutricare Taurate from D/46.2 to approximately C/48.5, crossing the D/C boundary.

### Ruling: HOLD at MODERATE; file this mechanistic justification

**Decision:** Taurate remains classified as MODERATE (factor 0.75). The UNRESOLVED classification is not adopted. Nutricare Taurate stays at D/46.2.

**Reasoning — MODERATE is the epistemically honest placement, not UNRESOLVED:**

UNRESOLVED in the v3 model means: "the form composition is not disclosed, so no class can be assigned." Its defining characteristic is the *inability to classify*, not insufficient data for a chosen class. UNRESOLVED products receive a flat evidence penalty (−20) because the engine cannot assess the evidence for an unknown composition.

Magnesium taurate is a known, identifiable compound: magnesium di-taurate, PubChem CID 536944, MW 272.57, Mg(taurine)₂ chelate. The structure is unambiguous. Calling it UNRESOLVED would be inaccurate — the form is known; the uncertainty is about its bioavailability relative to citrate, not about what compound it is.

The question, then, is whether the evidence for taurate's bioavailability is sufficient to place it in MODERATE (rather than LOW) given that no direct human comparative absorption study exists for Mg taurate specifically. The mechanistic basis for MODERATE is:

1. **Amino-acid chelation mechanism.** Taurate is an organic salt where magnesium is chelated to taurine (2-aminoethanesulfonic acid). Amino-acid chelates and organic salts generally show improved GI absorption compared to inorganic salts (oxide, carbonate) because the organic ligand improves solubility at physiological pH and the amino-acid carrier may support transport across the intestinal epithelium via amino-acid transporters. This is the same mechanistic argument that places glycinate/bisglycinate in HIGH and malate/malonate in MODERATE.

2. **Directional evidence from the organic-salt class.** While there is no *taurate-specific* human absorption RCT, the body of evidence on organic Mg salts consistently shows they absorb better than oxide. Malate, for instance, has limited direct data but is placed in MODERATE by the same mechanistic reasoning — and malate shares with taurate the property of being an organic acid/amino-compound chelate without an RCT measuring fractional absorption.

3. **No evidence of LOW absorption for amino-acid chelates.** There is no study suggesting taurate behaves like oxide. The only basis for demoting taurate to LOW would be evidence that the amino-acid chelate mechanism fails for taurine specifically — and no such evidence exists.

4. **The alternative (UNRESOLVED) would actively misrepresent the product.** UNRESOLVED is designed for undisclosed blend ratios where the engine cannot determine which forms contribute to the dose. Applying it to a single known form would make Nutricare Taurate appear to be a hidden-composition product, which it is not. The evidence penalty (−20 on the evidence sub-score) is specifically designed for opacity, not for a form with sparse bioavailability data.

5. **Scientific precedent for mechanistic placement.** Hydroxide (MODERATE) has limited human absorption data as a nutritional supplement form; its classification relies partly on mechanistic inference (higher solubility than oxide in acidic GI conditions). Taurate has a comparable evidence profile — mechanistic argument + no contradictory data + no RCT. The consistent application of the tiering logic places it alongside hydroxide and malate in MODERATE, not in a special UNRESOLVED bucket.

**Confidence disclosure (Hard Rule 6):**

Evidence tier for the MODERATE classification of taurate: **Weak — Mechanistic / Insufficient Direct Human Data.** The placement is a reasoned inference, not an RCT-verified conclusion. If a human comparative absorption study for Mg taurate is published and shows absorption consistently below the organic-salt range (e.g., below malate), this ruling must be revisited and taurate may be reclassified.

**Consumer fairness assessment:**

Taurate at D/46.2 is the result of its low administered dose (76mg elemental × 0.75 = 57mg adjusted), not of a classification penalty. At UNRESOLVED (factor 1.0, penalty −20), the score would be approximately: dose_s(76mg adj = 76mg) ≈ 62.8, evidence = 52.0, trans = 30; blend ≈ 62.8×0.55 + 52×0.20 + 30×0.25 = 34.5 + 10.4 + 7.5 = 52.4; no cap binding → ~C/52.4. This is actually *above* the C/D boundary (50), meaning UNRESOLVED would move taurate to C — an *upgrade* from D — purely because the dose penalty at factor 1.0 overrides the evidence penalty at −20, producing a net gain. That would be the wrong consumer signal: a product with genuinely sparse bioavailability evidence and a low dose would appear more favorably scored than its absorption profile warrants. MODERATE correctly keeps it at D because the small adjusted dose (57mg) is the honest limiting factor.

**Evidence references:**

- PubChem CID 536944 (magnesium taurate / Mg ditaurate): confirmed compound identity, MW 272.57, CID in magnesium.yaml `compound_forms_identity`.
- NIH ODS Magnesium Fact Sheet: amino-acid chelates and organic salts absorb more completely than oxide (directional basis for MODERATE class).
- Magnesium dossier (magnesium.yaml) `absorption_by_form.taurate: 0.15`: taurate estimated 10–20% band (sparse data), above oxide 4% band — consistent with MODERATE, not LOW.

---

## Grade Movement Summary (required by return contract)

| Finding | Products affected | Grade change | Score change |
|---|---|---|---|
| HRT-1 | 0 | None | None |
| HRT-3 | 2 (Supherb Citrate+B6, Altman Bisgly 250) | None — B retained | None — display note only |
| MRT-5 | 0 | None | None |

**Total grade movements: 0.**
HRT-3 changes displayed engine output (GI note for 2 products) but does not change scores or grades. Product Agent D7 co-sign is required for HRT-3 because it modifies a display rule. HRT-1 and MRT-5 are documentation rulings; no engine code changes.

---

## Routing

- **HRT-1:** Documentation complete. No code change. No further gate action required — this addendum IS the formal documented acceptance the red-team required. Nutrition Agent D7 complete.
- **HRT-3:** Requires Product Agent D7 co-sign (display-rule change, 2 products gain GI note). After co-sign → Data Agent implements `>= 250` change in `run_magnesium_v2.py`.
- **MRT-5:** Documentation complete. No code change. No further gate action required.

---

## Open Items (not_done for this addendum)

1. Product Agent D7 co-sign on HRT-3 (>=250 operator change).
2. After D7 co-sign, Data Agent to implement HRT-3 in `run_magnesium_v2.py` and regenerate the run output.
3. The v3 engine is a parallel track to the live absorbed-mg model. This addendum governs the v3 spec only. The absorbed-mg model (magnesium.yaml SUPP-EV-030 v3) is separate and unaffected by these rulings.
