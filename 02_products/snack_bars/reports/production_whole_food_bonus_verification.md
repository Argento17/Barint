# Production Whole-Food Bonus Verification
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Priority 1 Verification  
**Question:** Does the whole_food_bonus issue exist in the active production scoring engine or only in the archived prototype?

---

## Verdict

**The bug exists only in the archived Python prototype. It has not affected any production scores. However, the intended whole-food bonus was also not applied in production scoring — by omission, not by bug. The net effect on production scores is identical: the whole-food positive reward mechanism has never been active.**

---

## 1. What the Production Engine Is

The production scoring engine is not the Python prototype at `C:\Bari\99_archive\bisp2_concept_prototype\`. All 53 snack bar products were scored using a manual CE trace system.

**Evidence:**

Every scored product has a `bsip2_trace.json` file at:
```
C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products\<product_id>\bsip2_trace.json
```

File header from `bsip1_16000423534\bsip2_trace.json` (Nature Valley oat bar):
```json
{
  "bsip2_version": "proto_v0",
  "trace_generated_at": "2026-05-19T18:06:24.686539Z",
  "specification_version": "bsip2_concept_v1 + score_resolution_contract_SRC-v1",
  ...
}
```

The trace structure uses an L1–L6 layered framework (`L1_observed_signals`, `L2_derived_signals`, `L3_inferred_classifications`, `L4_interpreted_concerns`, `L5_behavioral_hypotheses`, `L6_policy_decisions`). This is not the Python prototype's output format. The Python `score_product()` produces `FoodAssessment` objects with `dimensions`, `guardrails`, `trace`, and `reason_codes`. These are structurally different.

The Python prototype's `run_bsip2.py` entry point reads `.xlsx` or `.csv` input and writes `.xlsx` output. No such input/output files exist in the snack bars run directory. The batch summary (`run_snack_bars_001_batch_summary.md`) records 0 pipeline errors — if the Python engine had been used, products with oat or almond ingredients would have crashed with `KeyError` and appeared as pipeline errors.

**The archived Python prototype was not used to produce any production snack bar scores.**

---

## 2. Confirmation That the Bug Exists in the Prototype

**File:** `C:\Bari\99_archive\bisp2_concept_prototype\bsip2_dimensions.py`  
**Lines:** 59–60 (processing_quality section) and 120–121 (whole_food_integrity section)

```python
# Line 59–60
if f.get("has_whole_food_marker"):
    pq += p["whole_food_bonus"]       # p = P["processing_quality"]

# Line 120–121
if f.get("has_whole_food_marker"):
    wfi += p["whole_food_bonus"]      # p = P["whole_food_integrity"]
```

**`bsip2_config.py` — `processing_quality` params (complete):**
```python
"processing_quality": {
    "base": 100,
    "nova_4_penalty": 24,
    "nova_3_penalty": 12,
    "ingredient_count_threshold": 8,
    "ingredient_count_penalty_per_extra": 1.2,
    "engineered_marker_penalty": 6,
    "matrix_marker_bonus": 2.5,      ← actual key
    "matrix_relief_cap": 8,
}
```

The key `"whole_food_bonus"` does not exist in either `processing_quality` or `whole_food_integrity` parameter blocks. The correct key is `"matrix_marker_bonus"`.

**Empirical confirmation:**

```
$ python -c "from bsip2_score import score_product; from tests.fixtures import RAW_ALMONDS; r = score_product(RAW_ALMONDS)"

Traceback (most recent call last):
  File "bsip2_score.py", line 242, in score_product
    dims_obj = calculate_dimensions(features)
  File "bsip2_dimensions.py", line 60, in calculate_dimensions
    pq += p["whole_food_bonus"]
KeyError: 'whole_food_bonus'
```

`RAW_ALMONDS` (ingredients: `"שקדים"`) triggers the bug because `"שקדים"` matches `INGREDIENT_MARKERS["whole_food_positive"]`, setting `has_whole_food_marker=True`. The same crash occurs for any product with oats, almonds, nuts, peanuts, or seeds in its ingredients.

There is no `try/except` around `calculate_dimensions()` in `bsip2_score.py` (line 242). The exception propagates and the scoring call fails entirely.

---

## 3. Whole-Food Bonus Status in Production Scores

Production dimension scores for `bsip1_16000423534` (Nature Valley oat and dark chocolate bar — contains oats and whole grain):

```json
"dimension_scores": {
  "processing_quality": 65,
  "nutrient_density": 22.2,
  "calorie_density": 85.0,
  "glycemic_quality": 72.5,
  "protein_quality": 18.5,
  "additive_quality": 82,
  "satiety_support": 51.5,
  "fat_quality": 81.6,
  "regulatory_quality": 95.0,
  "whole_food_integrity": 52
}
```

`whole_food_integrity = 52` is exactly the base value from `bsip2_config.py` (`"base": 52`). No whole-food bonus was applied to a product that contains oats, which would qualify for the bonus under the intended design (`INGREDIENT_MARKERS["whole_food_positive"]` includes `"שיבולת שועל"`).

The processing_quality for this product is 65. Given NOVA3 penalty of -12, the base calculation starts at 88. The 23-point gap (88→65) reflects additional processing markers applied by the CE (glucose syrup, flavouring, etc.). No +2.5 whole_food_bonus was added.

This pattern is consistent across all production traces reviewed: `whole_food_integrity` equals 52 (base) plus NOVA penalties and ingredient complexity penalties only. The intended +7 for whole-food ingredients and +2.5 to processing_quality for whole-food presence have never been applied in production.

---

## 4. Production Scoring Differences from Prototype

The production scoring differs from the Python prototype in additional ways beyond the whole_food_bonus:

| Parameter | Python prototype | Production (manual CE) |
|---|---|---|
| NOVA3 cap | 75 | 82 |
| NOVA4 cap | 60 | 68 |
| Date bar HIGH_SUGAR cap | Applied at 60 (sugar ≥ 25g) | Not applied (natural sugar exempted manually) |
| whole_food_bonus | KeyError (never fires) | Not applied (by omission) |
| Dimension name | `calorie_density_quality` | `calorie_density` |

The production manual CE scoring is a parallel specification that was developed alongside but independently of the Python prototype. The Python prototype is a concept implementation, not the execution engine for production scoring.

---

## 5. Summary

| Question | Answer |
|---|---|
| Does the bug exist in the archived prototype? | **Yes** — confirmed by `KeyError: 'whole_food_bonus'` at `bsip2_dimensions.py:60` and `:121` |
| Was the prototype used to score production products? | **No** — production used manual CE traces (bsip2_version: proto_v0, L1–L6 framework) |
| Did the bug affect any production scores? | **No** — prototype was not the execution engine |
| Was the whole_food_bonus applied in production scoring? | **No** — `whole_food_integrity = 52` (base only) in all reviewed production traces |
| Net effect on current scores | The intended whole-food reward mechanism has never been active in any scored product |
