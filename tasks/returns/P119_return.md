# P119 Return — TASK-278 Phase-7: cheese_spreads × sat_fat wire + pilot

**Agent:** Data Agent
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-7 cheese_spreads×sat_fat wire + pilot

---

## Summary

Engine wired (constants.py + score_engine.py), engine_invariants 342 PASS, pilot
`run_cheese_005_satfat_pilot` executed (59 cheese + 20 milk + 89 yogurt = 168 products scored).

**Gate result: 9 PASS / 3 FAIL / 1 n/a-docs**

C10 milk CRITICAL: PASS (all 20 delta=0.0).

Three failures, all explainable and root-caused:
- **C3 Inv-2 FAIL** — genuine mechanism finding: both inv-2 products are below median, so both
  get relief (gap widens from 4.2→6.2). D6 predicted narrowing but both products are sub-median.
- **C9 FAIL** — harness artifact: the 1 "non-cream-cheese dairy" with nonzero delta is
  yogurt_mixin 7290102397600, delta=-0.4 from EV-088 YOGURT FLOOR (not EV-089). EV-089 scope
  guard is correct; this is EV-088 co-activation when BARI_SHELF_RELATIVE_V1=True.
- **C10b FAIL** — same root cause: 7290102397600 (yogurt_mixin, sugars_g=13.6g) gets
  clamped by EV-088 floor (Stage 7d, fires for CULTURED_YOGURT_SUBTYPES + sugars>=12g), not
  by EV-089. The cheese_spread sat_fat SR branch (EV-089) never fires for yogurt_mixin (correct:
  yogurt_mixin not in CREAM_CHEESE_SPREAD_SUBTYPES). Delta=-0.4 = EV-088 floor, not EV-089.

**EV-089 scope guard is CONFIRMED CORRECT.** The C9/C10b failures require either:
(a) Revising C10b criterion to exclude EV-088-induced deltas (the criterion as written tests
    "delta from cheese_spread SR" but the harness can't isolate which SR caused the delta), or
(b) Disabling EV-088 in the pilot harness for a clean isolation test of EV-089 alone.

**C3 Inv-2** requires D7 gate revision (Inv-2 pair must be revised to a genuinely
above/below-median pair, or the gap-widening corrected).

---

## Definition of Done

| Item | Status |
|---|---|
| constants.py: 8 constants added (7 FATSAT_SHELF_REL_CHEESESPREAD_* + CREAM_CHEESE_SPREAD_SUBTYPES) | DONE |
| score_engine.py: EV-089 SR call site in FAT_QUALITY family + EV-089 floor branch (Stage 7e) | DONE |
| score_engine.py: EV-089 trace fields in result dict | DONE (floor_applied, floor_note) |
| engine_invariants 342 PASS (post-wiring, before pilot) | DONE: 342 PASS |
| Pilot script created: batch_run_cheese_shelfrel_v1.py | DONE |
| Pilot run: run_cheese_005_satfat_pilot/ (168 traces + run_record.json) | DONE |
| C10 milk byte-id CRITICAL: all 20 delta=0.0 | PASS |
| C10b yogurt byte-id: 89 yogurt products, 1 nonzero (EV-088 floor, NOT EV-089) | FAIL (harness artifact) |
| Named pair scores reported | DONE |
| Off=0 | CONFIRMED |
| MEASURED NOT PUBLISHED | CONFIRMED |

---

## Engine Changes Made

### constants.py — 8 new constants added

After `SUGAR_SHELF_REL_YOGURT_B_MAX = 3`, added:

```python
# EV-089 cheese_spreads×sat_fat shelf-relative (P119, 2026-06-14; n=24 cream_cheese from run_cheese_003)
FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN = 16.05
FATSAT_SHELF_REL_CHEESESPREAD_IQR = 2.60
FATSAT_SHELF_REL_CHEESESPREAD_SCALE = 2.0756        # MAD-primary: 1.4826×1.40=2.0756
FATSAT_SHELF_REL_CHEESESPREAD_FLOOR = 62
FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G = 16.5
FATSAT_SHELF_REL_CHEESESPREAD_P_MAX = 6
FATSAT_SHELF_REL_CHEESESPREAD_B_MAX = 3

CREAM_CHEESE_SPREAD_SUBTYPES: frozenset = frozenset({"cream_cheese", "cheese_spread"})
```

`FATSAT_SHELF_REL_SCOPE` unchanged (remains `frozenset()`).
`CULTURED_YOGURT_SUBTYPES` unchanged.

### score_engine.py — 2 new blocks

**Block 1 (EV-089 SR call site):** In `evaluate_guardrails`, FAT_QUALITY family section, after the
existing `FATSAT_SHELF_REL_SCOPE` call site and before `fat_cap = _coordinate_family(...)`:
- Initialized `_cheese_satfat_g = nn.get("fat_saturated_g")` + `_sr_cheese_satfat = 0` unconditionally
- Guard: `BARI_SHELF_RELATIVE_V1 AND category=="dairy_protein" AND cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES AND fat_saturated_g is not None`
- Calls `shelf_relative_differentiator(nutrient="fat_saturated_g", direction="asymmetric", normalize_distance=True, bands=SUGAR_SHELF_SURCHARGE_BANDS/SUGAR_SHELF_RELIEF_BANDS)`
- Appends to `fat_pens_fired` via `check_penalty("FATSAT_CHEESE_SPREAD_SHELF_REL_V1", ...)`

**Block 2 (EV-089 floor):** In `score_product`, Stage 7e, after EV-088 yogurt floor:
- Guard: `BARI_SHELF_RELATIVE_V1 AND category=="dairy_protein" AND cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES AND sat_fat_g is not None AND sat_fat_g >= 16.5g`
- `score_after_penalty = min(score_after_penalty, 62)`
- Variables: `_cheese_spread_floor_applied`, `_cheese_spread_floor_note` in result dict

---

## Pilot Results

### Corpus
- Cheese (run_cheese_003): 59 products loaded
- Milk (run_milk_002): 20 products (C10)
- Yogurt (run_yogurt_005): 89 products (C10b)
- Total scored: 168 products (dual run)

### Shelf stats
- `fat_saturated_g`: median=16.05, scale=2.0756, n=24 (cream_cheese-only)
- All other stats cleared (sugars_g stats absent → EV-088 SR no longer fires, but EV-088 FLOOR still fires when flag=True)

### C10 Milk byte-id (CRITICAL) — PASS

All 20 milk products: delta=0.0. Frozen invariant safe.

### C10b Yogurt byte-id — FAIL (harness artifact)

89 yogurt products total. 1 nonzero delta:
- `7290102397600` (yogurt_mixin): delta=-0.4

**Root cause:** This delta is from **EV-088 YOGURT SUGAR FLOOR** (Stage 7d), NOT from EV-089.
When `BARI_SHELF_RELATIVE_V1=True`, EV-088 floor fires for any product with:
- `category=="dairy_protein" AND subtype in CULTURED_YOGURT_SUBTYPES AND sugars_g >= 12.0g`
7290102397600 has sugars_g=13.6g → gets clamped. Flag-off: no clamp. Delta=-0.4 is floor effect.

EV-089 scope guard (cream_cheese/cheese_spread) does NOT fire on yogurt_mixin — confirmed from trace.
This is not a scope guard failure for EV-089. It is EV-088 co-activation.

### Named Pairs

| Pair | Barcode | sat_fat_g | flag_off | flag_on | delta |
|---|---|---|---|---|---|
| Inv-1 A | 4129118 | 14.0 | 43.8 | 44.8 | +1.0 |
| Inv-1 B | 7290116935409 | 16.2 | 45.0 | 45.0 | 0.0 |
| Inv-2 A | 7622201521493 | 7.8 | 47.3 | 50.3 | +3.0 |
| Inv-2 B | 4129101 | 15.0 | 43.1 | 44.1 | +1.0 |

Inv-1: gap_off=1.2, gap_on=0.2 → NARROWS (PASS)
Inv-2: gap_off=4.2, gap_on=6.2 → WIDENS (FAIL)

Inv-2 root cause: both products (7.8g and 15.0g) are below median 16.05g → both get relief.
D6 predicted narrowing but both are in the relief zone → gap widens, not narrows.

### Gate Criteria

| # | Name | Result | Evidence |
|---|---|---|---|
| C1 | directional_distribution | **PASS** | above_median n=12 mean_delta=-1.5 (<=0 ✓); below_median n=12 mean_delta=+1.617 (>=0 ✓) |
| C2 | grade_dist_and_magnitude | **PASS** | (A) 0 high_sat@B ✓; (B) 3 low_sat<=10g @C+ ✓; (C) mean|d|=2.493>=0.5 ✓ |
| C3 | gap_narrows_inversion | **FAIL** | Inv-1 gap 1.2→0.2 NARROWS ✓; Inv-2 gap 4.2→6.2 WIDENS ✗ (both inv-2 products below median) |
| C4 | min_movers | **PASS** | 15 movers >= 5 ✓ |
| C5 | min_grade_changes | **PASS** | 2 grade changes >= 1 ✓ |
| C6 | max_absorption | **PASS** | 0/15=0.0% <= 40% ✓ |
| C7 | anti_immunity | **PASS** | 0 products sat_fat>=18g at grade B flag-on ✓ |
| C8 | floor_compliance | **PASS** | 7 products checked (sat_fat>=16.5g), 0 violations ✓ |
| C9 | no_scope_bleed | **FAIL** | 1 non-cream_cheese dairy with delta≠0 (7290102397600/yogurt_mixin, EV-088 floor artifact) |
| C10 | frozen_byte_id_milk | **PASS CRITICAL** | 20/20 milk delta=0.0 ✓ |
| C10b | yogurt_byte_id | **FAIL** | 1/89 yogurt with delta≠0 (EV-088 floor, not EV-089 scope) |
| C11 | flag_off_drift | n/a-docs | 26 mismatches vs run_cheese_004 (non-blocking) |

### Cream_cheese per-product table (sorted by sat_fat_g)

| barcode | sat_fat_g | flag_off | flag_on | delta | grade_off | grade_on |
|---|---|---|---|---|---|---|
| 7290019635116 | 3.0 | 44.3 | 47.3 | +3.0 | D | D |
| 7290116934365 | 3.8 | 62.0 | 65.0 | +3.0 | C | B |
| 7622201798154 | 7.1 | 60.6 | 63.6 | +3.0 | C | C |
| 7622201521493 | 7.8 | 47.3 | 50.3 | +3.0 | D | C |
| 7290014759084 | 9.6 | 53.9 | 56.9 | +3.0 | C | C |
| 4129118 | 14.0 | 43.8 | 44.8 | +1.0 | D | D |
| 7290108502541 | 14.3 | 47.6 | 48.6 | +1.0 | D | D |
| 4129101 | 15.0 | 43.1 | 44.1 | +1.0 | D | D |
| 7290019635383 | 15.0 | 23.2 | 24.2 | +1.0 | E | E |
| 7290019635581 | 15.0 | 32.4 | 32.8 | +0.4 | E | E |
| 7290014762831 | 15.8 | 44.8 | 44.8 | 0.0 | D | D |
| 7622201139278 | 16.0 | 45.5 | 45.5 | 0.0 | D | D |
| 7290116933078 | 16.1 | 42.7 | 42.7 | 0.0 | D | D |
| 7290116936604 | 16.1 | 44.5 | 44.5 | 0.0 | D | D |
| 7290116931982 | 16.2 | 42.8 | 42.8 | 0.0 | D | D |
| 7290116932644 | 16.2 | 41.7 | 41.7 | 0.0 | D | D |
| 7290116935409 | 16.2 | 45.0 | 45.0 | 0.0 | D | D |
| 4129156 | 16.5 | 42.9 | 42.9 | 0.0 | D | D |
| 7290019635376 | 17.0 | 51.2 | 51.2 | 0.0 | C | C |
| 554976 | 18.6 | 46.1 | 44.1 | -2.0 | insuff | insuff |
| 5992889 | 19.6 | 46.1 | 42.1 | -4.0 | insuff | insuff |
| 554969 | 20.0 | 46.1 | 42.1 | -4.0 | insuff | insuff |
| 7290011499624 | 20.0 | 33.6 | 29.6 | -4.0 | E | E |
| 7296073453123 | 20.0 | 46.1 | 42.1 | -4.0 | insuff | insuff |
| 7290019635369 | null | 54.7 | 54.7 | 0.0 | C | C |
| 7290108504378 | null | 55.4 | 55.4 | 0.0 | C | C |

Grade changes (C5): 7290116934365 C→B; 7622201521493 D→C (both low-sat-fat, relief path)

### Milk table (all must be delta=0.0)

All 20 milk products: delta=0.0. C10 PASS.

---

## Failure Root Causes and Recommended Path

### C3 Inv-2 FAIL

**Root cause:** D6 chose Inv-2 pair as 7622201521493 (7.8g) vs 4129101 (15.0g). Both are
below the median of 16.05g. Both receive SR relief. 7622201521493 gets +3 (z=-3.97), 4129101 gets +1 (z=-0.51). Gap widens: 4.2→6.2.

**Recommended resolution (D7 gate revision):** Replace Inv-2 with a genuinely above-median/below-median pair, or accept gap-widening as correct directional behavior (C1 already captures this: direction IS correct). Alternatively, reframe C3 to test "gap between the HIGHEST sat_fat and LOWEST sat_fat" rather than a specific named pair. Both inversions showing the mechanism are visible in the per-product table (e.g., 7290019635116 at 3.0g gains +3, while 554969 at 20.0g loses -4 — that's a genuine correction).

### C9/C10b FAIL (same product, EV-088 artifact)

**Root cause:** The pilot harness sets only `fat_saturated_g` shelf stats, but `BARI_SHELF_RELATIVE_V1=True` also activates the EV-088 yogurt sugar FLOOR (Stage 7d in score_product). This floor fires for any yogurt_mixin with sugars_g>=12g regardless of sat_fat stats.

**Recommended resolution (pilot harness fix, no gate revision needed):** In the cheese_spread SR pilot, disable the EV-088 floor by either:
- (a) Temporarily patching `SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G` to a very high value before the run, or
- (b) Adding a flag to disable EV-088 floor independently of BARI_SHELF_RELATIVE_V1.
OR: Revise C10b criterion to clarify that EV-088-induced deltas are excluded from the cheese_spread SR isolation test (the EV-089 scope guard itself is confirmed correct).

The EV-089 scope guard was confirmed to NOT fire on yogurt_mixin — the delta comes from the independently-wired EV-088 floor. This is a test-harness design issue, not an engine bug.

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-7 cheese_spreads×sat_fat wire + pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "pilot_run_dir": "run_cheese_005_satfat_pilot",
  "constants_added": [
    "FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN",
    "FATSAT_SHELF_REL_CHEESESPREAD_IQR",
    "FATSAT_SHELF_REL_CHEESESPREAD_SCALE",
    "FATSAT_SHELF_REL_CHEESESPREAD_FLOOR",
    "FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G",
    "FATSAT_SHELF_REL_CHEESESPREAD_P_MAX",
    "FATSAT_SHELF_REL_CHEESESPREAD_B_MAX",
    "CREAM_CHEESE_SPREAD_SUBTYPES"
  ],
  "milk_byte_id": {
    "pass": true,
    "milk_products_checked": 20,
    "any_nonzero_delta": false,
    "milk_deltas": "all 0.0"
  },
  "yogurt_byte_id": {
    "pass": false,
    "yogurt_products_checked": 89,
    "any_nonzero_delta": true,
    "yogurt_deltas_nonzero": [
      {"barcode": "7290102397600", "delta": -0.4, "subtype": "yogurt_mixin",
       "root_cause": "EV-088 yogurt sugar floor (Stage 7d) fires when BARI_SHELF_RELATIVE_V1=True AND sugars_g=13.6>=12.0g; NOT from EV-089 cheese_spread SR (scope guard confirmed correct)"}
    ]
  },
  "named_pairs": {
    "inv1_a": {"barcode": "4129118", "sat_fat_g": 14.0, "flag_off": 43.8, "flag_on": 44.8},
    "inv1_b": {"barcode": "7290116935409", "sat_fat_g": 16.2, "flag_off": 45.0, "flag_on": 45.0},
    "inv1_gap_off": 1.2, "inv1_gap_on": 0.2, "inv1_narrows": true,
    "inv2_a": {"barcode": "7622201521493", "sat_fat_g": 7.8, "flag_off": 47.3, "flag_on": 50.3},
    "inv2_b": {"barcode": "4129101", "sat_fat_g": 15.0, "flag_off": 43.1, "flag_on": 44.1},
    "inv2_gap_off": 4.2, "inv2_gap_on": 6.2, "inv2_narrows": false,
    "inv2_fail_root_cause": "Both products below median 16.05g; both receive relief; gap widens (correct mechanically but wrong pair for gap-narrows test)"
  },
  "gate_results": [
    {"criterion": "C1",  "name": "directional_distribution",    "pass": true,  "evidence": "above_median mean=-1.5<=0 PASS; below_median mean=+1.617>=0 PASS"},
    {"criterion": "C2",  "name": "grade_dist_and_magnitude",    "pass": true,  "evidence": "(A) 0@B PASS; (B) 3 low_sat@C+ PASS; (C) mean|d|=2.493>=0.5 PASS"},
    {"criterion": "C3",  "name": "gap_narrows_inversion",       "pass": false, "evidence": "Inv-1 NARROWS 1.2->0.2 PASS; Inv-2 WIDENS 4.2->6.2 FAIL (both sub-median, both get relief)"},
    {"criterion": "C4",  "name": "min_movers",                  "pass": true,  "evidence": "15 movers >= 5"},
    {"criterion": "C5",  "name": "min_grade_changes",           "pass": true,  "evidence": "2 grade changes >= 1"},
    {"criterion": "C6",  "name": "max_absorption",              "pass": true,  "evidence": "0/15=0.0% <= 40%"},
    {"criterion": "C7",  "name": "anti_immunity",               "pass": true,  "evidence": "0 sat_fat>=18g@B flag-on"},
    {"criterion": "C8",  "name": "floor_compliance",            "pass": true,  "evidence": "7 checked sat_fat>=16.5g, 0 >62"},
    {"criterion": "C9",  "name": "no_scope_bleed",              "pass": false, "evidence": "1 nonzero: 7290102397600/yogurt_mixin delta=-0.4 (EV-088 floor, NOT EV-089 scope failure)"},
    {"criterion": "C10", "name": "frozen_byte_id_milk",         "pass": true,  "evidence": "20/20 milk delta=0.0 CRITICAL PASS"},
    {"criterion": "C10b","name": "yogurt_byte_id",              "pass": false, "evidence": "1/89 yogurt nonzero: 7290102397600 delta=-0.4 (EV-088 floor, not EV-089)"},
    {"criterion": "C11", "name": "flag_off_drift",              "pass": "n/a-docs-only", "evidence": "26 mismatches vs run_cheese_004"}
  ],
  "cream_cheese_movers": 15,
  "grade_changes": 2,
  "absorption": 0.0,
  "engine_invariants": "342 PASS",
  "off_used": false,
  "not_done": [
    "Gate not passed: C3 Inv-2 FAIL (D7 gate revision or new inversion pair needed)",
    "Gate not passed: C9/C10b FAIL (EV-088 co-activation artifact; harness fix or criterion clarification needed)"
  ]
}
```

---

## Machine-Readable Return Contract

```json
{
  "artifacts_claimed": [
    {
      "path": "03_operations/bsip2/proto_v0/src/constants.py",
      "change": "8 FATSAT_SHELF_REL_CHEESESPREAD_* + CREAM_CHEESE_SPREAD_SUBTYPES constants added after SUGAR_SHELF_REL_YOGURT_B_MAX"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/score_engine.py",
      "change": "EV-089 SR call site in FAT_QUALITY family (evaluate_guardrails) + EV-089 floor branch Stage 7e (score_product) + imports updated + result dict fields added"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/batch_run_cheese_shelfrel_v1.py",
      "change": "new pilot script created"
    },
    {
      "path": "02_products/cheese_spreads/bsip2_outputs/run_cheese_005_satfat_pilot/run_record.json",
      "sha256": "f7134b0b6b0dbb1bab22db2697b3019d6ac1b5c5abb579605a69f030b65dccbc"
    }
  ],
  "counts": {
    "constants_added": {"numerator": 8, "denominator": "8 required", "value": "8/8"},
    "engine_invariants": {"numerator": 342, "denominator": "342", "value": "342/342 PASS"},
    "milk_products_checked": {"numerator": 20, "denominator": "20 in run_milk_002", "value": "20/20 delta=0.0"},
    "yogurt_products_checked": {"numerator": 89, "denominator": "89 in run_yogurt_005", "value": "1/89 nonzero (EV-088 floor artifact)"},
    "cream_cheese_movers": {"numerator": 15, "denominator": "26 cream_cheese", "value": "15/26"},
    "grade_changes": {"numerator": 2, "denominator": "26 cream_cheese", "value": "2/26"},
    "gate_criteria_pass": {"numerator": 9, "denominator": "11 active", "value": "9/11 + 1 n/a-docs"},
    "off_used": {"numerator": 0, "denominator": "0 permitted", "value": "0/0 CONFIRMED"}
  },
  "commands_run": [
    {"cmd": "python 03_operations/shadow/engine_invariants.py (pre-wire)", "exit": 0},
    {"cmd": "Edit constants.py — add EV-089 constants block", "exit": 0},
    {"cmd": "Edit score_engine.py — add imports", "exit": 0},
    {"cmd": "Edit score_engine.py — add EV-089 SR call site in FAT_QUALITY", "exit": 0},
    {"cmd": "Edit score_engine.py — add EV-089 floor branch Stage 7e", "exit": 0},
    {"cmd": "Edit score_engine.py — add EV-089 result dict fields", "exit": 0},
    {"cmd": "python 03_operations/shadow/engine_invariants.py (post-wire)", "exit": 0, "result": "342 PASS"},
    {"cmd": "Write batch_run_cheese_shelfrel_v1.py", "exit": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/batch_run_cheese_shelfrel_v1.py", "exit": 0}
  ],
  "not_done": [
    "Gate not passed: C3 Inv-2 (pair selection issue — D7 gate revision needed)",
    "Gate not passed: C9/C10b (EV-088 floor co-activation — harness fix or criterion clarification needed)"
  ],
  "acceptance_test": "engine_invariants 342/342 PASS. Milk byte-id: 20/20 delta=0.0 PASS. EV-089 scope guard confirmed correct (no yogurt_mixin received cheese_spread SR penalty). 3 gate failures root-caused: C3 both inv-2 products sub-median (need gate revision), C9/C10b EV-088 floor co-activation artifact (need harness fix or criterion clarification). OFF=0.",
  "propose": "RETURNED"
}
```
