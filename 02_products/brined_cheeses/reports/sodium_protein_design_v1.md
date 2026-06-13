# Shelf-Relative Sodium + Protein Re-weighting — Design v1 (DESIGN ONLY, pre-implementation)

**Author:** Nutrition Agent (C1), 2026-06-13 · orchestrator-verified facts · TASK-266 follow-up.
**Status:** DESIGN — needs owner go-ahead + Product D7 co-sign + cross-corpus proof BEFORE any engine
change. Touches scoring philosophy + can move published scores (tripwire). Flag-gated, default-off.

## Glass Box finding
The owner-recalled "shelf-relative / distance-from-mean" sodium method **does NOT exist** in the engine
or any spec (confirmed by Nutrition's Glob/Grep + the orchestrator's independent grep). Glass Box has a
PROTEIN-quality (DIAAS) signal only. The shelf-relative method must be built from scratch.

## A. Shelf-relative sodium surcharge — `BARI_SODIUM_SHELF_RELATIVE_V1` (default OFF)
Two layers: existing graduated absolute bands (EV-055) + NEW surcharge by distance above the **shelf
MEDIAN** (median, not mean — outlier-stable). Surcharge bands: ≥600mg above median → −6; 400-599 → −4;
200-399 → −2; <200 → 0. Below-median → no surcharge (no reward layer here). Combined sodium penalty
capped by a raised `SODIUM_FAMILY_BUDGET_BRINED = 16`. **Low-variance guard:** if shelf sodium stdev
< 150mg, suppress surcharge (don't punish tight high-sodium shelves). Scope: dairy_protein +
whole_food_fat. Median computed at batch-run time, stored in run_record.
**Expected:** bulgarit-5% 1,550mg (today 88/A) → ~80-83 (borderline A / high-B); 300mg tzfatit → unchanged.

## B. Protein re-weight for dairy_protein — `BARI_DAIRY_PROTEIN_REWEIGHT_V1` (default OFF)
Raise `protein_quality` 10%→14%, lower `calorie_density` 15%→11% (sums to 1.00). PLUS suppress
HP_FAT_SODIUM_COMBO for CLEAN low-sodium dairy (sodium ≤400mg AND additive_count=0) — a plain hard
cheese at 24% fat / 300mg is not an engineered HP stack. Precedent: veg_spread archetype re-weight
(EV-032/R6), EV-054 HP suppression.
**Expected:** 4861070 (25g protein) — protein contribution +3.8, HP penalty removed (+6), but
**confidence ceiling 75 binds** (no ingredient list = −25 confidence). So ~75/B; would be ~82-85/A
if an ingredient list existed. Honest: a clean high-protein cheese with no verifiable ingredients
can't reach A.

## Safety (cross-corpus, return-contract rule 8)
Flag-gated default-off → zero impact until enabled per-run. Milk (FROZEN run_005_headpin): sodium
40-60mg, far below all bands + near its own median → **0 surcharge, 0 move — safe.** Yogurt minimal.
Implementation MUST re-score every live corpus + diff vs committed baseline; NO published move without
owner. Each change independently rollback-able (two separate flags).

## Side-finding to investigate
4861070 (צפתית קשה) has `context_flag=null` despite "צפתית" being a brined keyword — possible routing
miss; moot here because sodium 300<500 blocks brined_food anyway. Worth a separate check.

## Codify as STANDARD for next products
- Endemic-sodium categories (sodium structurally non-reformulable): graduated bands + shelf-relative
  surcharge. - Protein-primary archetypes: archetype-specific weights elevating protein over calories.
