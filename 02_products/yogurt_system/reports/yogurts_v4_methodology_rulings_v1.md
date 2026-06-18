---
id: yogurts_v4_methodology_rulings_v1
title: Yogurts v4 — Methodology Rulings for run_yogurt_006
source_task: TASK-250
challenger_report: red_team_yogurts_v4.md
authored: 2026-06-11
owner: nutrition-agent
status: RULING_ISSUED
---

# Yogurts v4 — Methodology Rulings (TASK-250)

Scope: five methodology questions raised by red-team findings RT-4, RT-6, RT-9, RT-10,
RT-11, RT-13 from `red_team_yogurts_v4.md`. These rulings are the required input for
TASK-249 (run_yogurt_006 regen). Every ruling below is in force only for the yogurt
corpus unless an activation scope note says otherwise.

Frozen invariants are untouched: milk run_005_headpin, bread provenance, snack ceiling.

---

## Ruling 1 — Null Sugar and A-Grade Eligibility (RT-6)

### Decision

A product may hold A when sugar_g is null, PROVIDED the engine records a missing-data
confidence reduction that is visible in the confidence_band. The current engine already
applies two missing-field reductions (fiber: −5, nova_confidence=low: −10) but those do
not reduce confidence_band below "high" for the three null-sugar 90/A products. The fix is
additive: add a missing sugar reduction that moves confidence_band to "partial" when
sugar_g is null. This surfaces the unknown without capping the grade.

Specifically: null sugar_g must add a confidence reduction of −10 in the BSIP2 trace,
consistent in magnitude with the nova_confidence=low reduction. With the two existing
reductions already at −15 (fiber + nova), adding −10 for null sugar brings total reductions
to −25, which is enough to cross from "high" (≥80) to "partial" (<80 but ≥60) territory in
the confidence scoring model. The consumer-facing display then shows partial/A instead of
high/A, honestly reflecting that sugar is unknown.

The grade itself is NOT capped. A-grade eligibility with null sugar is preserved. The
argument for capping at B when sugar is unknown is rejected: it conflates unknown with
known-high, which is the wrong epistemic direction. The better product (clean ingredients,
high protein, NOVA 2, no additives) should not be penalized for a data gap that the
confidence state already discloses. Capping at B would silently apply a sugar penalty for
sugar that was never observed.

### What TASK-249 Must Implement

Add a confidence reduction entry in the BSIP2 trace for `missing: sugar_g` with
reduction = −10. This applies to all products with `sugar_g is null`. No change to
scoring dimension weights, caps, or grade thresholds. Confidence_band recalculation flows
from the updated confidence_score. Verify the three null-sugar 90/A products now show
`confidence_band = partial` in their run_006 traces.

### Tripwire Assessment

This is a transparency fix, not a scoring rule change. It does not change any published
score, dimension weight, cap value, or grade. It touches confidence state only.
**No owner tripwire.** D7 co-sign (Nutrition + Product) is required because this modifies
engine behavior, but it is a methodology disclosure fix, not a score philosophy change.

### Rollback

Revert: remove the `missing: sugar_g` entry from the confidence reduction table in
score_engine.py. Confidence_score returns to pre-ruling values. Zero scoring impact.

---

## Ruling 2 — Null Saturated Fat and Penalty Silence (RT-9)

### Decision

Null satFat must NOT apply a conservative imputation penalty as a hard scoring rule for
run_yogurt_006. The same epistemic principle as Ruling 1 applies: unknown is not
known-high. However, satFat null must generate a confidence reduction just as null sugar
does (Ruling 1), for the same reason — it is a missing field that prevents a penalty
from firing.

The relevant missing-data reduction for `fat_saturated_g is null` is −5 (lighter than
sugar because saturated fat has a defined MoH red-label threshold at 5g/100g that does
not apply to most plain yogurts anyway; the practical consequence is that it primarily
affects full-fat Greek, not low-fat products). This is not symmetric to sugar because
saturated fat is more predictable from total fat than sugar is from total carbs.

Note: EV-REDLABEL-012 in constants.py already defines a null satFat imputation mechanism
(`REDLABEL_NULL_SATFAT_FAT_FLOOR = 15.0g`, `REDLABEL_DAIRY_SATFAT_FRACTION = 0.63`,
`REDLABEL_NULL_SATFAT_CONFIDENCE_HAIRCUT = 0.50`) gated behind `BARI_REDLABEL_V1`. That
flag is not active for the yogurt run. The BARI_REDLABEL_V1 imputation path, if activated
in a future run, would apply the sat-fat consequence at 50% weight with explicit
annotation — this is the architecturally correct long-term resolution. The run_006 ruling
keeps that gate OFF and relies on the confidence reduction disclosure instead.

For full-fat Greek yogurt products (RT-9 specifically names barcodes 7290017065588 at
10% fat and 7290014890589 at 8% fat): their null satFat is a parsing gap, not structural
data absence. TASK-249 should flag these two products for targeted BSIP0 re-scrape to
recover the satFat value before run_006 is frozen. If re-scrape recovers the value, the
penalty fires normally. If re-scrape does not recover it, the −5 confidence reduction
applies.

### What TASK-249 Must Implement

1. Add a confidence reduction entry for `missing: fat_saturated_g` with reduction = −5
   for all products with `fat_saturated_g is null`.
2. Flag barcodes 7290017065588 and 7290014890589 for targeted re-scrape before run_006
   scoring. If satFat is recovered, no confidence reduction needed; the penalty fires
   from the real value.

### Tripwire Assessment

Same as Ruling 1: transparency fix, not a scoring rule change. No grade or score changes.
**No owner tripwire.** D7 co-sign required (engine behavior change).

### Rollback

Revert: remove `missing: fat_saturated_g` confidence reduction from score_engine.py.
Zero scoring impact.

---

## Ruling 3 — Rounding at Grade Boundaries (RT-4 and RT-13)

### Decision

Standard rounding (round-to-nearest) at grade boundaries is NOT acceptable policy when
the rounding crosses a grade boundary. The correct rule is:

**Grade is derived from the engine's raw final_score_estimate BEFORE rounding, then
the score is rounded for display. The grade must agree with the grade the raw value
would have received.**

The current builder applies round(raw) then grade_from_score(rounded). This creates
grade promotion artifacts:
- RT-4: raw=34.8 → rounds to 35 → grade D. Engine: grade E. Consumer sees D.
- RT-13: raw=49.6 → rounds to 50 → grade C. Engine: grade D. Consumer sees C.

Both are grade promotions that override the engine's own judgment. The fix is:

```
display_score = round(raw_score)  # unchanged — for display only
grade = grade_from_score(raw_score)  # raw, pre-rounding — authoritative
```

This does not add a "floor rule" — it corrects an architectural error in the builder.
The score integer shown to the consumer may still be 35 or 50 (display rounding is
fine), but the grade letter must reflect the raw score, not the rounded score. A
product at 34.8 shows "35 / E". A product at 49.6 shows "50 / D".

This is the only defensible policy: the grade is the primary consumer signal. A product
the engine evaluated as E must not be displayed as D by a builder arithmetic artifact.

### What TASK-249 Must Implement

In `build_yogurts_frontend_v4.py` (or its v6 successor), change the grade assignment
logic to call `grade_from_score(raw_final_score_estimate)` before applying the display
rounding. The display `score` integer is still `round(raw)`. The `grade` field uses
raw. Verify in run_006:
- barcode 7290114313070 should publish as 35/E (not 35/D)
- barcode 7290102399819 should publish as 50/D (not 50/C)

This change affects the frontend builder only, not the scoring engine.

### Tripwire Assessment

This corrects a builder error that caused grade promotion. It does not change any score
value, does not modify scoring logic, and the two affected products score lower (E not D;
D not C) — there are no A-grade products affected. However, changing a published grade
(even a D to E or C to D) on a live product is a consumer-facing change on a product that
went live in run_005. This touches the "irreversible AND consumer-facing" wire (tripwire 2).

**This ruling requires owner sign-off before the run_006 frontend is published live.**
The fix should be implemented in run_006 and verified in the QA gate, but the go-live
decision requires owner confirmation of the grade correction policy. Document as a
pre-launch gate item for TASK-249.

### Rollback

Revert: restore grade assignment to `grade_from_score(round(raw))` in the builder.
The two products return to their run_005 published grades (35/D and 50/C).

---

## Ruling 4 — Sweetener Signal Absence for A-Grade Products (RT-10)

### Decision

The sweetener penalty/cap architecture already exists in the engine (SWEETENER_CAP_A/B/C
in constants.py, wired in score_engine.py lines 2079–2081). The problem identified in
RT-10 is NOT a missing scoring rule — it is a detection gap: the three A-grade products
show `sweetener_count=1` in BSIP1 enrichment_summary but `sweetener_tier=None` in the
BSIP2 trace. The engine cannot fire the cap because the signal is not reaching it.

Confirmed from trace inspection: all three RT-10 products have `sweetener_matches=[]`
and `sweetener_tier=None` in the BSIP2 trace, meaning signal_extractor.py found no
matching sweetener vocabulary in the ingredient text despite BSIP1 detecting a sweetener.

The ruling is: the sweetener detection gap in signal_extractor.py must be diagnosed and
fixed before run_006. This is a data quality / enrichment bug, not a methodology question.
Once fixed, if sweetener_tier becomes non-null (likely Tier A for stevia/acesulfame,
Tier C for aspartame/sucralose), the existing cap fires automatically at SWEETENER_CAP_A
= 75, SWEETENER_CAP_B = 73, or SWEETENER_CAP_C = 70.

A new sweetener scoring rule is NOT needed and NOT being added. The existing architecture
is correct. The fix target is the BSIP1-to-BSIP2 signal handoff (either the BSIP1
sweetener vocabulary is using different terms than signal_extractor.py expects, or the
enrichment_summary.sweetener_count is computed from a wider vocabulary than the BSIP2
sweetener_tier vocabulary).

Score impact if sweetener_tier becomes Tier A (most likely for these NOVA2/NOVA3 yogurts
which typically use stevia): SWEETENER_CAP_A = 75 would cap two of the three products
(81/A Bio Natural and 83/A Muller Active). The 90/A Danone Pro21 already caps at 94.8
via NOVA3 which is more restrictive than 75 — it would then also hit 75. All three
products would move from A to B.

This is an enrichment bug fix with scoring consequences, not a new methodology change.
Routes to TASK-249 for implementation, but the detection fix itself is Data Agent scope.

**A new yogurt-specific sweetener rule is deferred to post-launch.** The RT-10 concern
about a plain yogurt with a sweetener being graded the same as one without is valid for
the long term, but the immediate resolution is fixing detection so the existing cap fires.

### What TASK-249 Must Implement

1. Diagnose why sweetener_tier=None for barcodes 7290102395231, 7290114311069, and
   7290112336712 despite sweetener_count=1 in BSIP1. Check whether the BSIP1 sweetener
   vocabulary overlaps with the SWEETENER_TIER_*_HE lists in signal_extractor.py.
2. Fix the detection gap in signal_extractor.py (expand vocabulary) or in the BSIP1
   enrichment configuration (confirm which Hebrew sweetener terms are being detected
   and map them to the Tier A/B/C classification).
3. Re-run signal extraction for the three affected products and verify sweetener_tier
   is non-null in run_006 traces.
4. If sweetener_tier becomes non-null, verify the cap fires correctly and that the
   grade reflects the cap (predicted: Bio Natural 81→75/B, Muller Active 83→75/B,
   Danone Pro21 90→75/B).

### Tripwire Assessment

Fixing a detection bug so an existing cap fires is not a new scoring rule. The rule
already exists and is already approved. This is implementation correction.
**No owner tripwire.** D7 co-sign required (scoring behavior changes for three live
products).

### Rollback

Revert: restore the pre-fix sweetener vocabulary in signal_extractor.py or enrichment
configuration. The three products return to sweetener_tier=None and their run_005 scores.

---

## Ruling 5 — Ceiling Compression and Identical Scores at 90/A (RT-11)

### Decision

The score compression at the top of the range (three products scoring 90/A with different
protein levels) is intentional and acceptable. It is a direct consequence of the
BARI_RECAL_P0_YOGURT_TRIM post-cap (89.9 ceiling, documented in TASK-246) combined with
the NOVA2 base score. The ceiling compression is not an error — it is policy that
acknowledges the score scale cannot fully differentiate products at the top of a clean,
high-protein, minimally-processed band. This is honest: the differences between 10g,
12.5g, and 25g protein yogurts are real but all three are genuinely excellent products
from a structural food-quality standpoint.

No disclosure at the score level is needed. However, the category caveat copy (the
standard "הערת קטגוריה" yellow box on the comparison page) must explicitly note the
ceiling compression for high-protein products. The content should convey that the top-band
products are nutritionally differentiated beyond what the score communicates, and that
consumers comparing them should consider actual protein per serving.

Note on the corrupted product (barcode 7290116932620, protein=190g): this product is
excluded from the ceiling compression analysis. Its score is derived from a corrupted
protein value (RT-1, CRITICAL) and must be removed from the corpus or corrected before
run_006. If removed or corrected, the remaining two genuine 90/A products (barcodes
7290110321031 and 7290116935614) still compress at the ceiling — the ruling holds.

Additionally: per Ruling 4, if the sweetener detection fix is applied, Danone Pro21
(7290112336712) moves off 90/A to 75/B. The number of products at 90/A in run_006 may
be 2 or fewer, reducing the practical visibility of the compression issue.

### What TASK-249 Must Implement

1. No scoring change. No disclosure in the product-level score presentation.
2. Update the category caveat copy for the yogurts comparison page (routes to
   Content Agent) to include: a note that the top-scoring high-protein yogurts are
   differentiated primarily by actual protein grams per serving, and that the 90/A
   grade captures structural food quality but does not rank between products at the
   same level.
3. Exclude barcode 7290116932620 from the category until the protein=190 corruption
   is resolved (RT-1 resolution, Data Agent scope, TASK-249 pre-condition).

### Tripwire Assessment

Ceiling compression is not a scoring error. The caveat copy update is consumer-facing but
it is explanatory, not a score change. It clarifies rather than modifies the published
grade. **No owner tripwire** for the copy update. The product exclusion (barcode
7290116932620) involves removing a live product from the published corpus — this is a
data integrity action (corrupted data must not publish) and does not require owner
sign-off beyond Data Agent + Product Agent confirmation.

### Rollback

Caveat copy: revert the added protein-differentiation sentence. No scoring impact.
Product exclusion: restore the product to the corpus only after protein_g is corrected
to a plausible value (verified against the Shufersal product page).

---

## Pre-Launch Gate Summary for TASK-249

| Ruling | Action Required | Owner Tripwire | D7 Co-sign |
|--------|----------------|----------------|------------|
| 1 (null sugar → confidence partial) | Add confidence reduction −10 for null sugar_g | No | Yes |
| 2 (null satFat → confidence partial) | Add confidence reduction −5 for null satFat; flag 2 products for re-scrape | No | Yes |
| 3 (grade-before-round) | Fix builder grade assignment; owner sign-off before go-live | Yes — owner sign-off required before live publish | Yes |
| 4 (sweetener detection fix) | Diagnose + fix sweetener_tier null gap; verify cap fires | No | Yes |
| 5 (ceiling compression) | Update category caveat copy; exclude corrupted product | No | No (content update) |

D7 co-sign status: Nutrition Agent ruling issued. Product Agent co-sign required before
implementation begins for Rulings 1, 2, 3, 4.

---

## Evidence Citations

| Finding | Trace Source | Key Observation |
|---------|-------------|-----------------|
| RT-6 null sugar / confidence | run_yogurt_005 traces for 7290110321031, 7290116935614, 7290116932620 | confidence_band=high despite sugar_g=null; confidence_reductions=[fiber −5, nova −10] |
| RT-9 null satFat | run_yogurt_005 traces for 7290017065588, 7290014890589 | fat_saturated_g=null; ISRAELI_RED_LABEL_1_SAT_FAT cap not evaluated |
| RT-4 grade boundary | run_yogurt_005 trace for 7290114313070 | final_score=34.8, grade_estimate=E; builder publishes 35/D |
| RT-13 grade boundary | run_yogurt_005 trace for 7290102399819 | final_score=49.6, grade_estimate=D; builder publishes 50/C |
| RT-10 sweetener detection | run_yogurt_005 traces for 7290102395231, 7290114311069, 7290112336712 | sweetener_matches=[], sweetener_tier=None in BSIP2 signals despite sweetener_count=1 in BSIP1 enrichment |
| RT-11 ceiling compression | run_yogurt_005 traces, 3 x 90/A NOVA2 products | scores cap at 89.9 via BARI_RECAL_P0_YOGURT_TRIM; different protein levels produce identical published score |

---

## Governing Constraints (unchanged)

- Frozen invariants (milk run_005_headpin, bread provenance, snack ceiling) are
  untouched by all five rulings.
- BARI_RECAL_P0_YOGURT_TRIM (89.9 post-cap) remains as documented in TASK-246.
- OFF banned project-wide: no field in run_006 may use Open Food Facts as a source.
- Any implementation that changes a published score requires D7 co-sign before the
  run_006 corpus is frozen.
