# P129 Return — TASK-278 Phase-10: Maadanim × Sugar Wire + Pilot

**Return date:** 2026-06-14
**Agent:** data-agent
**Status:** RETURNED (gate failures C2b/C3/C6 — requires D7 clarification before activation)

---

## Summary

EV-092 (maadanim × sugar shelf-relative) is wired into the engine and the pilot ran cleanly. Engine invariants pass 342/342. The CRITICAL invariant C10 (milk delta=0) is 20/20 PASS. Three gate criteria fail: C2b (marginal: E-grade absorbs 40.8% of movers, 0.8% over limit), C3 (INV-B gap widens instead of narrows — directional reversal DOES occur but test fails on gap direction), and C6 (dead zone 47.9% > 40% cap).

The failures are structurally rooted in the maadanim corpus distribution: most products score in the E/D range (median 37/D-E at flag-off), which means penalty absorption is high and dead-zone count is above the 40% threshold written for categories with more mid-range scores. Flag is off by default — no published scores move. Full analysis and escalation items are in Section 6.

---

## Engine Edits

| Edit | File | Line reference | Description |
|---|---|---|---|
| Step 1 | `03_operations/bsip2/proto_v0/src/constants.py` | After L633 (after `SUGAR_SHELF_SCALE_GUARD_JUICES`) | Added 7 EV-092 constants block |
| Step 2a | `03_operations/bsip2/proto_v0/src/score_engine.py` | L1907 (evaluate_guardrails signature) | Added `maadanim_subtype: str | None = None` parameter |
| Step 2b | score_engine.py | L3220 (score_product body) | Added `bsip_maadanim_subtype = product.get("bsip_maadanim_subtype")` |
| Step 2c | score_engine.py | L3350-3354 (evaluate_guardrails call) | Added `maadanim_subtype=bsip_maadanim_subtype` to call |
| Step 2d | score_engine.py | After L2193 (EV-091 juice block end) | Inserted EV-092 SR call site in sugar family using `maadanim_subtype` |
| Step 2e | score_engine.py | After L3564 (Stage 7g juice floor end) | Inserted Stage 7h maadanim floor block |
| Step 2f | score_engine.py | After L3665-3666 (ev091 result fields) | Added `ev092_maadanim_floor_applied` + `ev092_maadanim_floor_note` to result dict |
| Import fix | score_engine.py | L61-65 (constants import block) | Added 7 EV-092 constants to import (missed in initial spec) |

---

## Pilot Corpora

| Corpus | Source | N loaded | N scored | Purpose |
|---|---|---|---|---|
| maadanim (all) | `03_operations/bsip1/run_maadanim_001/output/` | 200 | 200 | Primary scope |
| maadanim (EV-092 sugar scope) | same | — | 146 | bsip_maadanim_subtype not None AND sugars_g not None |
| milk | `run_005_headpin/products/` | 20 | 20 | C10 frozen invariant |
| yogurt | `03_operations/bsip1/run_yogurt_006/output/` | 88 | 88 | C10b isolation |
| cheese_spread | `03_operations/bsip1/run_cheese_003/output/` | 59 | 59 | C10c isolation |
| hard_cheese | `03_operations/bsip1/run_hard_cheeses_001/output/` | 37 | 37 | C10d isolation |
| juice | `03_operations/bsip1/run_juices_001/output/` | 65 | 65 | C10e isolation |

Errors: 0

---

## Shelf Stats (engine-computed vs proposal)

| Stat | Proposal (D7) | Engine computed |
|---|---|---|
| median | 9.70g | 9.70g |
| scale | 8.75g | 8.82g |
| n | 146 | 146 |

Scale difference: +0.07g (engine IQR/1.349 slightly higher than D7 rounded value). Engine values used for scoring.

---

## Score Distribution (maadanim sugar scope, n=146)

| Grade | Flag-off | Flag-on |
|---|---|---|
| S | 0 | 0 |
| A | 0 | 0 |
| B | 5 | 5 |
| C | 22 | 23 |
| D | 65 | 60 |
| E | 52 | 56 |
| insufficient_data | 2 | 2 |

Min/max: off=10/70.8, on=10/71.8. Median: off=38.5, on=37.0. StDev: off=13.23, on=13.89.

---

## Per-Product Summary (146 EV-092 scope products)

Full per-product table at: `C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001_sugar_pilot\maadanim_pilot_table.csv` (200 rows + header, sorted by sugars_g desc, includes all 200 maadanim products with null-sugar rows clearly identifiable).

Key figures derived from run_record.json:
- Movers (|delta|>0): 76/146 (52.1%)
- Big movers (|delta|>=1): 62/146 (42.5%)
- Dead zone (delta=0): 70/146 (47.9%)
- Grade changes: 7
- Mean |delta| among movers: 1.832
- Floor applied (ev092_maadanim_floor_applied=True): 0 products
  - Explanation: 37 products have sugars_g >= 16.08g, but all score <= 62 at flag-on by penalty alone before the floor fires. The floor is a safety clamp — it did not need to activate.
- Biscuit/cereal-routed products: 7 (EV-085 interaction potential; all delta recorded in run_record)

---

## INV-B Analysis

| | bc 2385455 (3.5g sugar) | bc 5014271300429 (52.0g sugar) | gap |
|---|---|---|---|
| Flag-off | 55.0/C | 42.4/D | +12.6 |
| Flag-on | 56.0/C | 36.4/D | +19.6 |
| Delta | +1.0 | -6.0 | gap widens |

Directional reversal: 2385455 > 5014271300429 both flag-off AND flag-on — reversal pre-existed and is maintained/deepened.

The C3 gate for INV-B requires `|gap|_on < |gap|_off AND directional reversal`. The reversal component PASSES. The gap-narrows component FAILS because both products move in the correct direction by different magnitudes (52g product penalized 6pts, 3.5g product relieved 1pt), widening the already-correct gap.

**Escalation note for Product/Nutrition Agent:** The INV-B gap criterion may need revision for cases where the directional reversal pre-exists at flag-off. The SR scoring is behaving correctly (penalizing high-sugar, relieving low-sugar) — the test criterion `|gap|_on < |gap|_off` is an incorrect proxy for inversions that are already directionally correct at baseline. Recommend accepting INV-B as PASS on directional reversal alone, or revising the C3 INV-B sub-criterion to `reversal_maintained AND high_sugar_penalized`.

---

## Gate Criteria Table

| # | Name | Result | Evidence |
|---|---|---|---|
| C1 | directional_distribution | PASS | above-median mean_delta=-1.434 (<=0); below-median mean_delta=+0.554 (>=0) |
| C2a | grade_dist | PASS | A+B+C: off=27 on=28 (not degraded) |
| C2b | grade_absorption | FAIL | E=31/76=40.8% > 40% cap (margin: 0.8%) |
| C2c | magnitude | PASS | mean|delta|=1.832, movers=76 (in [0.5, 6]) |
| C3 | gap_narrows_inversion | FAIL | INV-A PASS; INV-B: gap widens (12.6→19.6) though directional reversal maintained |
| C4 | min_movers | PASS | 62 products with |delta|>=1pt (need>=5) |
| C5 | min_grade_changes | PASS | 7 grade changes (need>=1) |
| C6 | max_absorption | FAIL | 70/146=47.9% in dead zone (need<=40%) |
| C7 | anti_immunity | PASS | 0 products with sugars_g>=16.08g at grade B |
| C8 | floor_compliance | PASS | 37 above-threshold, 0 floor violations |
| C9 | no_scope_bleed | PASS | 0 non-maadanim products with EV-092 fired |
| **C10** | **frozen_byte_id_milk** | **PASS** | **20/20 milk delta=0.0** |
| C10b | yogurt_isolation | PASS | 0 yogurt products with EV-092 fired |
| C10c | cheese_spread_isolation | PASS | 0 cheese_spread products with EV-092 fired |
| C10d | hard_cheese_isolation | PASS | 0 hard_cheese products with EV-092 fired |
| C10e | juice_isolation | PASS | 0 juice products with EV-092 fired |
| C11 | flag_off_drift | PASS | non-blocking informational only |

**Overall: FAIL (C2b, C3, C6)**
**CRITICAL invariant C10: PASS — 20/20 milk delta=0.0**

---

## Failure Analysis

**C6 (dead zone 47.9% > 40%):**

Root cause: maadanim category scores cluster very low (median 37, 52+56=108/146 in D+E). Products already heavily penalized for fat, calories, and NOVA have their sugar penalty absorbed into existing deficits rather than moving the score. The `z_dead=±0.30 × scale` dead zone was calibrated for a mid-range distribution; in maadanim's bottom-heavy distribution, the dead zone count is structurally higher. This is a distribution artifact, not an engine error. The 40% threshold was borrowed from the yogurt/juice criteria; it may need to be relaxed for maadanim's lower-scoring distribution (e.g., 55% or removed).

**C2b (E absorption 40.8%, marginal):**

E grade receives exactly 31 of 76 movers. Directly related to C6 — products near the bottom benefit from SR relief but often remain in E grade because starting score is already very low. Margin is 0.8% — a borderline result that may resolve if C6 threshold is adjusted (fewer movers from the dead-zone cohort exit dead zone in future iterations).

**C3 INV-B:**

Covered above in INV-B Analysis section. Criterion needs revision for pre-existing directional inversions.

---

## Not Done

- EV-092 flag-on activation: flag default=off, not activated
- Frontend JSON generation: not applicable (pilot only)
- C2b/C3/C6 criterion revisions: requires Product Agent + Nutrition Agent ruling
- biscuit/cereal EV-085 interaction review: 7 products routed there; all recorded in run_record; no anomalies observed but full audit not performed

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-10 maadanim×sugar wire+pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "engine_modified": true,
  "engine_changes": [
    "constants.py:after-L633: added EV-092 constants block (7 constants)",
    "score_engine.py:L1907: added maadanim_subtype param to evaluate_guardrails signature",
    "score_engine.py:L3220: added bsip_maadanim_subtype extraction in score_product",
    "score_engine.py:L3350-3354: added maadanim_subtype=bsip_maadanim_subtype to evaluate_guardrails call",
    "score_engine.py:after-L2193: inserted EV-092 SR call site in sugar family",
    "score_engine.py:after-L3564: inserted Stage 7h maadanim floor block",
    "score_engine.py:after-L3665: added ev092_maadanim_floor_applied + ev092_maadanim_floor_note to result dict",
    "score_engine.py:L61-65: added 7 EV-092 constants to import block"
  ],
  "engine_invariants": "342/342 PASS",
  "pilot_output": "02_products/maadanim/bsip2_outputs/run_maadanim_001_sugar_pilot/run_record.json",
  "pilot_corpora_n": {
    "maadanim_all": 200,
    "maadanim_sugar_scope": 146,
    "milk": 20,
    "yogurt": 88,
    "cheese_spread": 59,
    "hard_cheese_yellow": 37,
    "juices": 65
  },
  "gate_criteria_pass": ["C1","C2a","C2c","C4","C5","C7","C8","C9","C10","C10b","C10c","C10d","C10e","C11"],
  "gate_criteria_fail": ["C2b","C3","C6"],
  "gate_result": "FAIL — C2b (E absorption 40.8%/margin 0.8%), C3 (INV-B gap widens, reversal maintained), C6 (dead zone 47.9%)",
  "c10_milk_delta_zero_count": 20,
  "c10_milk_total": 20,
  "movers": 76,
  "big_movers": 62,
  "grade_changes": 7,
  "mean_abs_delta_movers": 1.832,
  "dead_zone_pct": 47.9,
  "floor_applied_count": 0,
  "above_floor_threshold_n": 37,
  "off_used": false,
  "tripwire_assessment": "No tripwire fires — flag default=off, zero published-score movement, internal pilot only. C2b/C3/C6 failures are gate failures requiring criterion revision, not a scoring philosophy change.",
  "escalation": "C3 INV-B criterion needs revision (gap-narrows is wrong proxy for pre-existing inversions; directional reversal maintained = sufficient). C6 40% dead-zone threshold needs relaxation for bottom-heavy maadanim distribution. C2b is a downstream effect of C6. Recommend Product Agent + Nutrition Agent rule on criterion adjustments.",
  "artifacts": [
    {
      "path": "02_products/maadanim/bsip2_outputs/run_maadanim_001_sugar_pilot/run_record.json",
      "sha256": "874198ddfb3bdbc15652118e0bf5df4eee5c402c5a6ea33244873272b28f0d2e"
    },
    {
      "path": "02_products/maadanim/bsip2_outputs/run_maadanim_001_sugar_pilot/maadanim_pilot_table.csv",
      "sha256": "2efde438d6bb90a72b18502dd0a73c44e5f23d9e8bbad6215cdb92629e90c047"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/score_engine.py",
      "sha256": "4d18feb1699905a7e7e33c61ecdafd5c6844a11c26886ea52a7d889f7858b43c"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/constants.py",
      "sha256": "8a84e294fca63abe3d24d73e83ae299fac1b184cf44a22fa626b91f80f5309f8"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/batch_run_maadanim_001_sugar_pilot.py",
      "sha256": "pilot_script"
    }
  ],
  "counts": {
    "maadanim_total_N": "200/200 files loaded",
    "maadanim_sugar_scope_N": "146/200 have bsip_maadanim_subtype not None AND sugars_g not None",
    "milk_N": "20/20 loaded and scored",
    "yogurt_N": "88/88 loaded and scored",
    "cheese_spread_N": "59/59 loaded and scored",
    "hard_cheese_N": "37/37 loaded and scored",
    "juice_N": "65/65 loaded and scored",
    "movers_N": "76/146",
    "big_movers_N": "62/146",
    "grade_changes_N": "7/146",
    "floor_applied_N": "0/37 (above-threshold products all clamped by penalty before floor fires)",
    "milk_delta_zero_N": "20/20",
    "errors_N": "0/469 total scored products"
  },
  "commands_run": [
    {"cmd": "python 03_operations/shadow/engine_invariants.py", "exit_code": 0, "result": "342/342 PASS"},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/batch_run_maadanim_001_sugar_pilot.py", "exit_code": 0, "result": "Pilot complete, run_record.json written"}
  ],
  "not_done": [
    "EV-092 flag activation (blocked by gate failures C2b/C3/C6)",
    "Criterion revision for C2b/C3/C6 (requires Product + Nutrition Agent ruling)",
    "Frontend JSON generation (not applicable until gate passes)"
  ],
  "acceptance_test": "PARTIAL — engine wired correctly, invariants pass 342/342, C10 20/20, scoping correct, floor correct. Gate fails on C2b/C3/C6 distribution criteria that need revision for maadanim's bottom-heavy score distribution.",
  "propose": "RETURNED"
}
```
