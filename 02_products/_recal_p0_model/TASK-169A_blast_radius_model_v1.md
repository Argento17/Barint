# TASK-169A — P0 Recalibration Blast-Radius MODEL (v1)

**Status:** MODEL ONLY. No score shipped, no frontend JSON, no published run dir touched.
**Engine:** BSIP2 proto_v0 (HEAD), all P0 changes gated behind `BARI_RECAL_P0` (default OFF).
**Author:** Data Agent (implements the Nutrition Agent design `recalibration_p0_design_v1.md`).
**Date:** 2026-06-02.

---

## 0. Safety contract — flag-OFF byte-identical (VERIFIED)

`verify_recal_off_identical.py` + a stash-based HEAD baseline confirm: with
`BARI_RECAL_P0=off`, re-scoring `run_cheese_003` (n=59) reproduces the pristine HEAD engine
**byte-for-byte** — final score, grade, and **every dimension** match on all 59 products
(0 mismatches). The flag is the rollback and the regression guard. Every R1–R7 code path is
inert when the flag is unset.

> Note: 1 product (`...217492`, kcal 297) differs between the *published* run_cheese_003
> trace and current HEAD on `calorie_density` (40→65) — this is **pre-existing HEAD drift in
> the calorie-density / confidence path, NOT a P0 effect** (P0 touches no calorie-density code;
> score+grade are unchanged at 60/C). Flagged for QA but out of P0 scope.

## Regression (deliverable 3)
| Suite | Flag OFF | Flag ON |
|---|---|---|
| Golden corpus (`run_regression_check.py`) | 0 FAIL / 1 WARN | 0 FAIL / 1 WARN (identical) |
| Router (`run_router_regression.py`) | all PASS | all PASS |

The single golden WARN (`structural_class=B expected C, acceptable as secondary`) is
pre-existing and flag-insensitive (the golden runner reads static traces). Router is
unaffected because R6 reuses existing router subtypes — no routing logic changed.
**Authoritative OFF-clean proof = the 59/59 byte-identical re-score, not the static-trace
golden runner.**

---

## 1. What each change does (as implemented, per spec)

| ID | Change | Where |
|---|---|---|
| R1 | `PROTEIN_SCALE_TABLES` + `lookup_protein_scale()` — per-category protein curve feeding both `nutrient_density` and `protein_quality`. `default`/`snack_bar_granola` reproduce the legacy supplement curve exactly. | constants.py, score_engine.py |
| R2 | EV-027 fiber-not-applicable path OR-bound to `BARI_RECAL_P0` (cheese inherits via existing `dairy_protein` allowlist; no new category). | score_engine.py |
| R3 | `_leanness_score()` replaces the two neutral-50 short-circuits; lean band (`fat<=3g`) takes `max(penalty_curve, leanness)`. | score_engine.py |
| R4 | Plain-dairy NOVA-3→2 demotion guard (dairy base + plain + no thickener/gum/emulsifier/humectant/flavor/color). | nova_proxy.py |
| R5 | `ISRAELI_RED_LABEL_1_SAT_FAT` composite cap suppressed; `_red_satfat_penalty()` graded fat-dimension penalty instead. `regulatory_quality` still counts the label. | score_engine.py |
| R6 | `VEG_SPREAD_WEIGHTS` re-weight for sauce_spread veg subtypes (matbucha/pepper/eggplant) with protein<3g; anti-immunity clamp at 80 unless clean additives + sub-red-label sodium. | constants.py, score_engine.py |
| R7 | Plain-dairy live-culture fermentation credit: grants the existing +8 `FERMENTATION_DIRECT_BONUS` to plain cultured dairy even when the panel omits the culture word. | score_engine.py |

---

## 2. Headline cases — cheese (run_cheese_003, n=59)

| product | OFF | ON | Δ | moved by |
|---|---|---|---|---|
| **cottage 1%** | 74.9/B | **97.8/S** | +22.9 | R1+R2 (nutrient 36→88, protein 56→88), R4 (proc 65→85, WFI 60→85), **R7 +8** |
| **cottage 9%** | 52.0/C | **89.1/A** | +37.1 | R1+R2, R4, R5 (cap→penalty, fat 45→41), R7 +8 |
| cottage 12% | 52.0/C | 84.4/A | +32.4 | same as 9% |
| **white+garlic** (R7 inversion) | 76.9/B | **88.3/A** | +11.4 | R1+R2, R4; already had +8 ferm |
| **napoleon 16%** | 68.3/B | **81.5/A** | +13.2 | R1+R2, R4, **R7 +8** |
| white 9% | 55.0/C | 83.3/A | +28.3 | R1+R2, R4, R7 |

- **R7 inversion RESOLVED:** cottage 1% (97.8) now ranks **above** white+garlic (88.3). ✔
- **cottage 9% R5 collapse RESOLVED:** 52/C→89/A, now far above napoleon 16% (81.5). ✔
- Direction of every headline is correct. **Magnitude overshoots** (see §4).

## Hummus (run_hummus_002 lineage = canonical_bsip1, n=69)
- Chickpea/tahini hummus: OFF cluster compressed (many pinned at 85/A floor / 60s); ON
  spreads 80–94 with better differentiation, **median 69.2** (addresses "compressed in the
  60s"). One product overshoots to 94.2/S (`חומוס מוקפא`).
- **R6 veg-spreads (15 detected): the cleanest result.** matbucha 48.7/D-class → 62–70/B,
  eggplant spreads → 59–69, exactly the spec's "mid-B for clean matbucha" target. None
  cross the 80 anti-immunity ceiling; guard intact. No router changes.

---

## 3. FROZEN-CEILING collision report (deliverable 2 — owner signs each in P2)

All frozen corpora re-scored OFF vs ON. **Every frozen move is a P2 owner decision.**

| corpus | n | score moves | grade moves | crosses A (≥80) | reaches S (≥90) |
|---|---|---|---|---|---|
| **snack_bars** | 53 | 14 | **0** | 0 | 0 |
| **milk** (frozen top = 85/A) | 20 | 9 | 4 | **1** | 0 |
| **yogurt** (run_yogurt_003) | 86 | 82 | 38 | **15** | **3** |
| bread retail_003 | — | not modelled here (bespoke BSIP0→BSIP1 loader; see §6) | | | |

### snack_bars — CEILING HELD ✔
0 grade changes; max new score 60.1. R1 deliberately kept the supplement curve for
`snack_bar_granola`, so **snk-001 = 70/B is untouched**. The only moves are tiny R5 sat-fat
penalty nudges (+0.2 to +3.4), no grade flips. **This frozen invariant is safe.**

### milk — ONE A-CROSSING (frozen ceiling breach) ⚠
| product | OFF | ON | issue |
|---|---|---|---|
| חלב נטול לקטוז מועשר בחלבון 2% | 74.1/B | **87.3/A** | **crosses milk 85/A ceiling**; R1 milk_dairy curve + **erroneous R7 +8** |
| חלב בבקבוק 1% מועשר מהדרין | 56.6/C | 69.8/B | **erroneous R7 +8** (fluid milk is not cultured) |
| משקה אורז אורגני | 49.4/D | 52.3/C | R3 leanness on a low-fat plant drink |
| אלפרו שוקו משקה סויה | 34.5/E | 37.0/D | R3 leanness |

**Root cause of the milk breach: R7 is granting the fermentation +8 to plain *fluid* milk.**
Fluid milk is not a cultured product — this is an R7 over-reach (see §4).

### yogurt — 15 A-crossings, 3 S ⚠
High-protein GO yogurts → 93–98.8/S; plain/goat yogurts → 80–85/A. Yogurt *is* cultured (R7
+8 is legitimate here), but R1+R4+R7 **stack** to S. This is the same overshoot as cheese.

---

## 4. CRITICAL FINDING — escalation to Nutrition Agent (Hard Rule 7)

The model produces **score distributions well above the spec's stated targets** — a classic
rule-stacking overshoot. Halting per Hard Rule 7 ("if a scoring rule implementation produces
unexpected score distributions, halt and escalate to Nutrition before continuing"). The
directions are all correct; the **combined magnitude is too hot.** Three precise levers:

1. **R7 fermentation +8 is the dominant overshoot driver, and it leaks to fluid milk.**
   - Cottage 1% reaches **89.76 from R1+R2+R4 alone — i.e. ≈90/A, the owner's exact target.**
     The R7 +8 is what pushes it to 97.8/S. **If R7's +8 were reduced/removed for cottage,
     the owner's 90/A target lands almost perfectly without further tuning.**
   - R7 as written ("plain dairy ⇒ cultured") fires on **fluid milk** (`product_type_dairy`
     true, plain) → milk gets +8 and breaches the 85/A ceiling. Fluid milk is not cultured.
     **Recommend:** restrict R7 to non-fluid dairy (cheese/cottage/yogurt) OR down-weight the
     fermentation bonus within dairy (spec's R7 option-2), OR drop R7 entirely now that
     R1+R2+R4 already hit the cottage target. **Nutrition's call.**

2. **R4 NOVA 3→2 lifts TWO dimensions by ~20–25 each** (processing 65→85, WFI 60→85 =
   +3.0 + +1.0 weighted) and is too permissive on flavored cheese: **napoleon "שום שמיר"
   (garlic+dill, 16% fat) gets demoted to NOVA 2** because garlic/dill are ingredients, not
   `flavor_enhancer` additive markers, so the "plain" test passes. A 16%-sat flavored cheese
   reaching A is the same false-plain detection gap. **Recommend tightening the R4/R7 "plain"
   test** to exclude flavored/seasoned variants (name- or ingredient-based), not just
   additive-marker-based.

3. **The compound effect** (R1 protein lift + R2 fiber renorm + R4 two-dim lift + R7 +8) is
   additive and uncapped below S. Even with correct directions, dairy now mass-produces S
   grades (cheese: 4 S; yogurt: 3 S). **Recommend** Nutrition decide a dairy A/S discipline:
   either trim the apex anchors in `PROTEIN_SCALE_TABLES["dairy_protein"]` (13g→95 is hot), or
   reduce the R4 WFI/processing lift, or gate the fermentation bonus — pick the lever, re-model.

**R6 (veg-spread) and R3 (leanness) and R5 (sat-fat cliff→graded) are well-behaved** and need
no change — R6 in particular nails its target and respects the anti-immunity guard.

---

## 5. Evidence-registry note (governance)
P0 design names EV-029 (R1), EV-030 (R3), EV-031 (R5), EV-032 (R6) as NEW and EV-027 (R2),
EV-024/026 (R4/R7) as extensions. These registry entries must be written **before P1 merges**
(per `bari-bsip2-scoring-governance`). R7-as-implemented is a *signal/credit* change, not a
new rule — if Nutrition chooses option-2 (down-weight fermentation in dairy) that becomes a
new EV entry. Not my call to author — flagged for the governance owner.

## 6. Coverage gaps / what was NOT modelled
- **bread retail_003** uses a bespoke inline BSIP0→BSIP1 normalizer (not a `load_batch` dir),
  so it isn't in the OFF/ON harness. Bread protein curve is conservative (R1 `bread` table)
  and bread is not dairy (no R4/R7), so the expected bread blast radius is small (R3 leanness
  + R5 sat-fat only). **Recommend** a dedicated bread re-model in P1 once Nutrition re-tunes,
  before any bread frozen sign-off.
- Headline product nutrition values are inferred from dimension scores in the published
  traces (the trace export nulls `normalized_nutrition_per_100g`); the live BSIP1 inputs drive
  the model, so the numbers above are from a real re-score, not from the stripped traces.

## 7. Artifacts
- Engine (flag-gated): `03_operations/bsip2/proto_v0/src/constants.py`,
  `score_engine.py`, `nova_proxy.py`
- Harness: `…/src/run_recal_p0_blast_radius.py`, `…/src/verify_recal_off_identical.py`
- Model data: `02_products/_recal_p0_model/{cheese,hummus,milk,yogurt,snack_bars}_{off,on}.json`,
  `blast_radius_summary.json`, `cheese_HEAD_baseline.json`
- This report: `02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.md`
