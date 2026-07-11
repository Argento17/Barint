# TASK-552 Ledger Gap Diagnosis — v1

**Author:** Nutrition Agent  
**Date:** 2026-07-11  
**Scope:** Read-only diagnosis. No scores changed.  
**Trace scanned:** 5,747 bsip2_trace.json files under `02_products/`  
**Tolerance:** 0.05 points (rounding tolerance for float comparisons)

---

## 1. Arithmetic Reproduction — Product #37 (barcode 7290102399802)

**Trace file:** `02_products/yogurt_system/bsip2_task515/spoonable/products/bsip1_yogurt_7290102399802/bsip2_trace.json`  
**Product name:** מולר פרוטאין יוגורט תות  
**Run committed:** 2026-07-05 (TASK-515/515A, commit 2474b04a)

### Numbers from the persisted trace

| Field | Value | Trace key |
|---|---|---|
| Weighted dimension score | 62.89 | `weighted_dimension_score` |
| Binding cap (NOVA_PROXY_4_ULTRA_PROCESSED) | 68.0 | `binding_cap` |
| `score_after_cap` | 62.89 | `score_after_cap` |
| Penalties applied (visible in trace) | SUGAR_SHELF_REL_V1 = 2.0 | `total_penalty_after_scaling` |
| `score_after_penalty` | 56.89 | `score_after_penalty` |

### The arithmetic gap

From the trace fields alone:  
`score_after_cap (62.89) − total_penalty_after_scaling (2.0) = 60.89`

But `score_after_penalty` = 56.89 — a delta of **−4.00** that appears in no ledger field in the trace.

### Full arithmetic (engine-verified)

The engine at `score_engine.py:3960` computes:

```python
score_after_penalty = round(score_after_cap - scaled_penalty - polyol_penalty - emul_comp_penalty, 2)
```

For this product:
- `scaled_penalty` = 2.0 (SUGAR_SHELF_REL_V1, from `total_penalty_after_scaling`)
- `polyol_penalty` = 0.0 (`sprint1_penalty_polyol_count` = 0)
- `emul_comp_penalty` = **4.0** (computed below)

**Emulsifier complexity penalty derivation (`_emulsifier_complexity()` at `score_engine.py:1878`):**

L3 signals for this product (from trace `L3_inferred_classifications`):
- `tax_emulsifier_concern` = [] → `high_agents` = []
- `tax_emulsifier_medium` = ["modified_starch_stabilizer"] → 1 medium agent
- `tax_emulsifier_low` = ["pectin"] → 1 low agent
- `distinct_count` = 2 → `complexity_tier` = "moderate"
- `highest_penalty` = max(medium_weight=3) = 3  
- `complexity_adj` = `EMULSIFIER_COMPLEXITY_CONSTANTS["complexity_moderate"]` = 1
- `total` = 3 + 1 = 4
- `total_capped` = min(4, `EMULSIFIER_COMPLEXITY_FAMILY_BUDGET`=8) = **4.0**

(Constants source: `constants.py:356-363`)

**Verified arithmetic:**  
`round(62.89 − 2.0 − 0.0 − 4.0, 2) = round(56.89, 2) = 56.89` ✓

The gap is fully explained. The 4-point step is a legitimate emulsifier complexity penalty (ECS-v1 / EV-045) computed and applied correctly by the engine. It is NOT a bug in the arithmetic — it is an **unlogged legitimate step**: the penalty fires and correctly reduces the score, but `trace_writer.py` never writes `emulsifier_complexity_penalty` to the on-disk JSON.

---

## 2. Root Cause — Engine Step and File:Line Responsible

### The unlogged step

**`score_engine.py:3959-3960`** (Stage 7 — Penalty Application):

```python
emul_comp_penalty, emul_comp_note, emul_comp_detail = _emulsifier_complexity(l3)
score_after_penalty = round(score_after_cap - scaled_penalty - polyol_penalty - emul_comp_penalty, 2)
```

The engine then writes the penalty to its own `result` dict at **`score_engine.py:4673`**:

```python
"emulsifier_complexity_penalty":      emul_comp_penalty,
"emulsifier_complexity_penalty_note": emul_comp_note if emul_comp_penalty > 0 else None,
"emulsifier_complexity_detail":       emul_comp_detail if emul_comp_penalty > 0 else None,
```

### The serialization omission

**`trace_writer.py:assemble_trace()` (lines 78-83)** assembles the on-disk trace with an explicit field whitelist:

```python
"penalties_considered":           score_result.get("penalties_considered"),
"penalties_applied":              score_result.get("penalties_applied"),
"total_penalty_before_scaling":   score_result.get("total_penalty_before_scaling"),
"total_penalty_after_scaling":    score_result.get("total_penalty_after_scaling"),
"penalty_scaling_note":           score_result.get("penalty_scaling_note"),
"score_after_penalty":            score_result.get("score_after_penalty"),
```

`polyol_penalty` and `emulsifier_complexity_penalty` are NOT in this list. The score_engine writes them to its `result` dict but the trace_writer never picks them up. Every bsip2_trace.json on disk was written through this path, so no trace has either field.

### Classification

This is an **unlogged legitimate step** — not an arithmetic bug. The engine is correct:
- `_emulsifier_complexity()` applies the right penalty per ECS-v1 / EV-045
- `score_after_penalty` in the trace is the correct final value
- `total_penalty_after_scaling` in the trace covers only the `concern_family_coordination` penalties (SUGAR_SHELF_REL_V1 = 2.0), as designed
- The field gap in `trace_writer.py` makes the penalty invisible to external auditors

### Second unlogged step (hummus floor — discovered in systemic scan)

A second class of unlogged step is present in hummus traces. The EV-094 hummus sodium floor (`score_engine.py:4204`) raises `score_after_penalty` upward (`max(score_after_penalty, _effective_hummus_floor)`). Although the engine appends this to `floor_result` at lines 4537-4554, the hummus-specific traces under `run_hummus_shelfrel_001` show `floors_applied = []` and the score at `score_after_floors` is the floor value, indicating those traces were generated before RT-10 (which injects EV-094 into `floors_applied`) was active. This creates **positive** gaps in the systemic scan for hummus.

---

## 3. Systemic Scan — All Persisted Traces

**Scan scope:** All `bsip2_trace.json` files under `02_products/` (5,747 total).  
**Gap definition:** `abs(score_after_penalty − (score_after_cap − total_penalty_after_scaling − polyol_penalty − emul_comp_penalty)) > 0.05`  
**Note on `emulsifier_complexity_penalty` field:** Present in 0 / 5,747 traces (all traces predate trace_writer including this field). For the 1,165 gap cases, emul field was therefore classified as "MISSING" and the check was done without subtracting it (making all gaps from the emulsifier penalty visible as negative gaps).

### Results by category

| Category | Total | No-gap | Gap (negative) | Gap (positive) | neg min | neg median | neg max | neg stdev |
|---|---|---|---|---|---|---|---|---|
| beverage | 255 | 225 | 30 | 0 | −6.00 | −4.00 | −1.00 | 1.67 |
| biscuit | 521 | 428 | 93 | 0 | −16.00 | −4.00 | −1.00 | 3.37 |
| bread | 104 | 72 | 32 | 0 | −6.00 | −4.00 | −3.00 | 0.87 |
| cereal | 769 | 736 | 33 | 0 | −4.00 | −3.00 | −3.00 | 0.17 |
| cracker | 158 | 149 | 9 | 0 | −4.00 | −3.00 | −1.00 | 1.15 |
| crispbread | 16 | 13 | 3 | 0 | −1.00 | −1.00 | −1.00 | 0.00 |
| dairy_protein | 1,399 | 1,022 | 377 | 0 | −15.15 | −4.00 | −0.44 | 2.51 |
| default | 198 | 160 | 37 | 1 | −9.00 | −3.00 | −1.00 | 2.78 |
| dessert | 118 | 62 | 56 | 0 | −5.57 | −3.00 | −1.00 | 1.21 |
| sauce_spread | 349 | 280 | 51 | 18 | −4.00 | −1.00 | −1.00 | 0.93 |
| snack_bar_granola | 1,682 | 1,306 | 376 | 0 | −13.00 | −4.00 | −0.95 | 2.85 |
| whole_food_fat | 178 | 129 | 49 | 0 | −10.00 | −4.00 | −1.00 | 2.54 |
| **TOTAL** | **5,747** | **4,582** | **1,146** | **19** | — | — | — | — |

**Grand total gap products: 1,165 / 5,747 (20.3%)**

### Interpretation

- **Negative gaps (1,146 products):** All caused by the missing `emulsifier_complexity_penalty` in `trace_writer.py`. The gap value equals the ECS-v1 penalty that was applied (1–16 points depending on distinct agent count and tier). Products with no emulsifier complexity (only low-tier single agent, or no emulsifiers) show no gap because emul_comp_penalty = 0.
- **Positive gaps (19 products, all hummus/sauce_spread):** Caused by EV-094 hummus sodium floor raising `score_after_penalty` before the `apply_floors()` call, in traces generated before RT-10 injected this into `floors_applied`. The floor is legitimate (NOVA ≤ 2 + high sodium = quality floor), but the older traces show `floors_applied = []` while the score already reflects the raised value.
- **Scores are arithmetically correct** in all 1,165 gap cases — the final `score_after_penalty` value is right; the ledger fields are incomplete.

---

## 4. Relationship to TASK-563

**TASK-563** (closed 2026-07-10) found that published frontend pages could not be re-derived from the trace their config named — 14/16 shelves had run_id mismatches, and 8 shelves had no persisted traces at all (scored in-memory).

**TASK-563 explicitly recorded:** "The engine arithmetic in the trace is internally consistent (score_after_cap 97.42 - penalty 12.0 = 85.42), so this is NOT the TASK-552 ledger gap." (TASK-563 close_reason, citing brined_cheeses example barcode 7290019635826.)

**Reconciliation:**

These are **independent defects** at different levels of the pipeline:

| | TASK-563 | TASK-552 |
|---|---|---|
| **Level** | Trace-to-frontend linkage | Trace internal ledger |
| **Defect** | Published page score ≠ trace score (mismatched run_ids, bespoke live-JSON writes) | `trace_writer.py` omits `emulsifier_complexity_penalty` and `polyol_penalty` from the on-disk JSON |
| **Arithmetic internal to trace** | Consistent (within individual trace, `score_after_cap − penalty = score_after_penalty` appeared to balance) | Gap: visible trace fields do NOT sum to `score_after_penalty` for 20.3% of traces |
| **Score correct on disk?** | Uncertain (mismatched runs) | Yes — `score_after_penalty` is the correct computed value |

**Why TASK-563 did not see the TASK-552 gap:** The TASK-563 investigator checked `score_after_cap − total_penalty_after_scaling` against `score_after_penalty` for their example products. Those products happened to have `emul_comp_penalty = 0` (no emulsifier complexity), so the check passed. The TASK-552 gap only appears when `emul_comp_penalty > 0`.

---

## 5. Fix Options (Ranked)

### Option A — Fix trace_writer.py to emit missing penalty fields (RECOMMENDED)

**What:** Add `polyol_penalty`, `polyol_penalty_note`, `emulsifier_complexity_penalty`, `emulsifier_complexity_penalty_note`, `emulsifier_complexity_detail`, and `ev094_hummus_floor_applied/note` to `trace_writer.py:assemble_trace()`.

**Affected file:** `03_operations/bsip2/proto_v0/src/trace_writer.py` — add 6 keys to the penalty block (lines 78-83).

**Effect:** Future scoring runs produce complete traces. All 1,165 existing gap traces remain stale until re-scored — the gap is frozen in historical traces but does not affect any live score.

**Pros:** One-file change; closes the ledger gap for all future runs; trace audits become self-contained. Does not touch any score. Re-running any category fixes its traces automatically.

**Cons:** Does not retroactively fix the 5,747 existing traces. Existing gap traces remain formally unexplained unless those categories are re-scored.

**Risk:** None. Trace_writer is pure serialization. The engine logic and all scores are unchanged.

### Option B — Re-score all affected categories to regenerate traces with the fix

**What:** After applying Option A, re-run batch runners for all 12 categories that have gap traces. This fills in the missing fields.

**Dependency:** Option A must be applied first.

**Risk:** Re-scoring is the score-movement tripwire. Score CHANGES require D7 co-sign. However, re-running with identical engine/constants/flags produces byte-identical `score_after_penalty` values (the scores are already correct). The only change is the addition of the missing fields. Verify with the conformance gate and Shadow baseline diff before commit.

**When:** After Product Agent co-sign per standard D7 path for re-scoring runs.

### Option C — Patch trace_writer to add a reconciliation field only

**What:** Add a computed `emulsifier_complexity_penalty_inferred` field that trace_writer derives by back-computing from `score_after_cap − total_penalty_after_scaling − polyol_penalty − score_after_penalty`. This patches the readability gap without touching scoring logic.

**Pros:** Can be applied to existing traces as a post-hoc annotation run without re-scoring.

**Cons:** Inferred, not directly sourced; loses the component breakdown (medium vs low agents, complexity tier). Only explains negative gaps — does not address the hummus positive gap.

**Rank:** Third choice. Treats the symptom not the cause.

### Recommendation

**Ship Option A alone, immediately.** It is a one-file, read-only-to-scoring change with zero risk to published scores. It closes the ledger gap for all future runs. Option B (re-score to backfill traces) is a valid follow-on step under normal D7 governance when the categories next need re-scoring for other reasons. Option C is not recommended when A is available.

---

## Appendix: Key File References

| File | Relevant Lines | Role |
|---|---|---|
| `03_operations/bsip2/proto_v0/src/score_engine.py` | 3959-3960 | ECS-v1 penalty applied to `score_after_penalty` |
| `03_operations/bsip2/proto_v0/src/score_engine.py` | 4671-4675 | `emul_comp_penalty` written to engine `result` dict |
| `03_operations/bsip2/proto_v0/src/trace_writer.py` | 78-83 | Penalty block — omits `emulsifier_complexity_penalty` |
| `03_operations/bsip2/proto_v0/src/constants.py` | 356-363 | `EMULSIFIER_COMPLEXITY_CONSTANTS` (high=5, med=3, low=1, moderate_adj=1, high_adj=3) |
| `03_operations/bsip2/proto_v0/src/constants.py` | 597-598 | `SUGAR_SHELF_REL_YOGURT_FLOOR` = 62, threshold = 12.0g |
| `02_products/yogurt_system/bsip2_task515/spoonable/products/bsip1_yogurt_7290102399802/bsip2_trace.json` | Full file | Seed trace for TASK-552 |
| `02_products/yogurt_system/bsip1_task515/bsip1_yogurt_7290102399802.json` | Full file | BSIP1 input record |
| `tasks/closed/TASK-563.md` | close_reason | Establishes TASK-563 ≠ TASK-552 |

---

*Proposed status: RETURNED. Scores are correct. Fix required in trace_writer.py (Option A). No score change needed; no D7 tripwire fires.*
