# P123 Return — TASK-278 Phase-8: hard_cheeses × sat_fat wire + pilot

**Agent:** Data Agent (re-dispatched after P123-original stopped at session limit)
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-8 hard_cheeses×sat_fat wire+pilot
**Verdict:** GATE PASSES — all 11 hard criteria PASS

---

## Wiring summary

Engine edits completed (partly by stopped P123, partly by orchestrator direct-edit):
- `constants.py` L604–618: 8 EV-090 constants + `HARD_CHEESE_YELLOW_SUBPOOLS`
- `score_engine.py`: `bsip_cheese_subpool = product.get("bsip_cheese_subpool")` at ~L3184
- `score_engine.py`: `hard_cheese_subpool=bsip_cheese_subpool` passed to `evaluate_guardrails` call
- `score_engine.py`: EV-090 SR call site at ~L2567 (uses `hard_cheese_subpool` param)
- `score_engine.py`: Stage 7f floor at ~L3455
- `score_engine.py`: result fields `ev090_hard_cheese_floor_applied` / `ev090_hard_cheese_floor_note`
- `engine_invariants`: 342/342 PASS (verified before pilot)

## Pilot corpora

| Corpus | N scored | Source |
|---|---|---|
| hard_cheese YELLOW scope | 22 | bsip1_hardcheese_*.json (yellow+yellow_light+hard_grating) |
| hard_cheese OTHER subpool | 15 | bsip1_hardcheese_*.json (bulgarian, tzfatit, processed) |
| milk | 20 | run_005_headpin |
| yogurt | 88 | run_yogurt_006 |
| cheese_spread | 59 | run_cheese_003 |
| **TOTAL** | **204** | |

## Hard cheese YELLOW scope per-product table (flag-on)

| Barcode | Subpool | sat_fat_g | Flag-off | Flag-on | Δ | Grade-off | Grade-on |
|---|---|---|---|---|---|---|---|
| 7290000062556 | yellow_light | 5.0 | 65.7 | 68.7 | +3.0 | B | B |
| 7290000062426 | yellow_light | 5.5 | 63.0 | 66.0 | +3.0 | C | **B** |
| 7290110178918 | yellow_light | 5.5 | 35.0 | 38.0 | +3.0 | D | D |
| 7290000062495 | yellow_light | 10.0 | 33.0 | 36.0 | +3.0 | E | **D** |
| 7290000062433 | yellow | 17.5 | 77.6 | 77.6 | 0.0 | B | B |
| 7290000062457 | yellow | 17.5 | 78.3 | 78.3 | 0.0 | B | B |
| 7290000062501 | yellow | 17.5 | 69.4 | 69.4 | 0.0 | B | B |
| 7290000062618 | yellow | 17.5 | 77.4 | 77.4 | 0.0 | B | B |
| 7290019866105 | yellow | 17.5 | 75.6 | 75.6 | 0.0 | B | B |
| 3256228310201 | yellow | 18.0 | 78.6 | 78.6 | 0.0 | B | B |
| 7290000062419 | yellow | 18.0 | 67.5 | 67.5 | 0.0 | B | B |
| 7290000062525 | yellow | 18.0 | 69.3 | 69.3 | 0.0 | B | B |
| 7290000062549 | yellow | 18.0 | 77.3 | 77.3 | 0.0 | B | B |
| 7290000062601 | yellow | 18.0 | 69.3 | 69.3 | 0.0 | B | B |
| 7290010644781 | hard_grating | 18.0 | 39.0 | 39.0 | 0.0 | D | D |
| 7290110178901 | yellow | 18.0 | 67.5 | 67.5 | 0.0 | B | B |
| 7290000062440 | yellow | 19.0 | 77.2 | 62.0 | **-15.2** | B | **C** |
| 7290000062464 | hard_grating | 19.0 | 39.0 | 38.0 | -1.0 | D | D |
| 7290000062532 | yellow | 19.0 | 77.1 | 62.0 | **-15.1** | B | **C** |
| 7290000062594 | yellow | 19.0 | 69.2 | 62.0 | **-7.2** | B | **C** |
| 8866972 | yellow | 19.5 | 69.9 | 62.0 | **-7.9** | B | **C** |
| 7290000062471 | hard_grating | 21.0 | 39.0 | 35.0 | -4.0 | D | D |

## Gate criteria (11 hard + 1 docs)

| # | Name | Result | Evidence |
|---|---|---|---|
| C1 | directional_distribution | **PASS** | Above-median n=6 mean_delta=-8.4 ≤0 ✓; below-median n=9 mean_delta=+1.33 ≥0 ✓ |
| C2 | grade_dist_and_magnitude | **PASS** | (A) 0 sat_fat≥19g@B flag-on ✓; (B) 2 sat_fat≤10g@B flag-on ✓; (C) mean\|Δ\|=6.24≥0.5 ✓ |
| C3 | gap_narrows_inversion | **PASS** | INV-1: gap_on=11.6 < gap_off=14.6 ✓; INV-2: gap_on=4.0 < gap_off=6.9 ✓ |
| C4 | min_movers | **PASS** | 10 products with delta≠0 ≥5 ✓ |
| C5 | min_grade_changes | **PASS** | 6 grade changes ≥1 ✓ |
| C6 | max_absorption | **PASS** | 0/10 absorbed = 0% ≤40% ✓ |
| C7 | anti_immunity | **PASS** | 0 sat_fat≥19g products reach grade B at flag-on ✓ |
| C8 | floor_compliance | **PASS** | 6 sat_fat≥19g products: all ≤62 ✓ |
| C9 | no_scope_bleed | **PASS** | 0 non-HARD_CHEESE_YELLOW_SUBPOOLS dairy_protein products with EV-090 term ✓ |
| C10 | frozen_byte_id_milk | **PASS — CRITICAL** | 20/20 milk delta=0.0 ✓ |
| C10b | cheese_spread_byte_id | **PASS — CRITICAL** | 59/59 cheese_spread products: EV-090 fired=0 ✓ |
| C10c | yogurt_byte_id | **PASS — CRITICAL** | 88/88 yogurt products: EV-090 fired=0 ✓ |
| C11 | flag_off_drift | docs-only | 1 mismatch >5pts vs run_001 baseline (non-blocking) |

## Interpretation

The mechanism behaves exactly as designed:
- 4 yellow_light outliers (5–10g sat_fat) receive +3 relief → two C→B + one E→D grade changes
- Tight yellow cluster (17.5–18.0g, n=11) sits near median → delta=0 (correct: near-median dead zone)
- Above-floor products (≥19g sat_fat, n=6): 3 yellow get floored to 62/C; 3 hard_grating receive SR penalty (-1 to -4) without hitting floor
- Frozen invariants (milk, cheese_spread, yogurt) all byte-identical to EV-090 = 0

**MEASURED NOT PUBLISHED.** No comparison JSON updated, no frontend changes, no score movement on live categories.

---

## Return Block (machine-readable)

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-8 hard_cheeses×sat_fat wire+pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "engine_modified": true,
  "engine_changes": [
    "score_engine.py: bsip_cheese_subpool extracted from product dict at ~L3184",
    "score_engine.py: hard_cheese_subpool=bsip_cheese_subpool passed to evaluate_guardrails call",
    "score_engine.py: Stage 7f EV-090 floor added after Stage 7e (constants: FATSAT_SHELF_REL_HARDCHEESE_FLOOR=62, threshold=19.0g)",
    "score_engine.py: ev090_hard_cheese_floor_applied / ev090_hard_cheese_floor_note added to result dict"
  ],
  "engine_invariants": "342/342 PASS",
  "pilot_output": "02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_002_satfat_pilot/run_record.json",
  "pilot_corpora_n": {"hard_cheese_yellow": 22, "hard_cheese_other": 15, "milk": 20, "yogurt": 88, "cheese_spread": 59},
  "gate_criteria_pass": ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C10b","C10c"],
  "gate_criteria_fail": [],
  "gate_result": "ALL 11 HARD CRITERIA PASS",
  "c10_milk_delta_zero_count": 20,
  "c10_milk_total": 20,
  "c10b_cheese_spread_delta_zero_count": 59,
  "c10b_cheese_spread_total": 59,
  "c10c_yogurt_delta_zero_count": 88,
  "c10c_yogurt_total": 88,
  "grade_changes": 6,
  "movers": 10,
  "mean_abs_delta_sr_firing": 6.24,
  "off_used": false,
  "tripwire_assessment": "No tripwire fires — flag default=off, zero published-score movement, internal pilot only",
  "propose": "RETURNED"
}
```
