# First-Live-E Derivation — Provenance Record (RT-C1)

**Program:** TASK-515A drinkable-yogurt terminal red-team, Data Agent fix cycle
**Date:** 2026-07-08
**Category:** yogurt-drinkable (20-product corpus, `yogurt_drinkable_FINAL_v3.json`)
**Purpose:** Durable, re-verifiable provenance for the four products whose grade rests on
the ECS-v1 emulsifier-complexity penalty, and confirmation that the resulting E-grade
(55329) is an honestly earned score, not a missing-data or engine artifact.

All numbers below were re-derived in this session by (a) reading each product's committed
`bsip2_trace.json` directly and (b) executing the live `_emulsifier_complexity()` and
`_compute_polyol_penalty()` functions from `03_operations/bsip2/proto_v0/src/score_engine.py`
against each product's own `L3_inferred_classifications` block — not copied from a prior
claim. `score_engine.py` is byte-identical to the committed baseline `2474b04a` at the time
of this write (see FIX-1/FIX-2 return block in the same task cycle for the diff proof).

## Correction to the originating claim (spec-conflict duty)

The dispatch spec framed the −4.0 as uniformly "earned by carrageenan (concern-tier) +
modified-starch stabilizer (medium), both on-label" across all four products. Verified
composition is **not** uniform — only 55329 actually contains carrageenan. Documenting the
real per-product composition below because the arithmetic path differs even though the
final penalty value converges on the same −4.0 for all four (see table).

## Per-product derivation

All four share the same engine stage sequence (`score_engine.py` Stage 5–7, ~line 3907–3927):
`score_after_penalty = score_after_cap − scaled_penalty(guardrail) − polyol_penalty − emul_comp_penalty`.
For all four products, `total_penalty_before_scaling = total_penalty_after_scaling = 0.0`
(confirmed from trace) and `sprint1_penalty_polyol_count = 0` → `polyol_penalty = 0.0`
(confirmed by direct function call). So the entire cap→final delta is the emulsifier
penalty alone, with **zero contribution from any other guardrail or the polyol penalty.**

### 55329 — "יוגורט לשתייה תות מלון" (strawberry-melon drink)
- Emulsifier-family agents on label: **carrageenan** (`tax_emulsifier_concern`, recategorized
  to medium-weight for complexity purposes per the function's carrageenan special-case) +
  **modified-starch stabilizer** (`tax_emulsifier_medium`, gated — this is the same E1442
  agent corrected in FIX-1 of this cycle).
- `_emulsifier_complexity()` detail: `high_agents=[]`, `medium_agents=['modified_starch_stabilizer','carrageenan']`,
  `low_agents=[]`, `distinct_agent_count=2` → complexity_tier=**moderate** (adj=+1),
  `highest_individual_penalty=3` (medium_weight) → `total_penalty=4`, `total_capped=4`
  (family budget = 8, not reached).
- `score_after_cap = 38.28` → `− 0 (scaled guardrail) − 0.0 (polyol) − 4.0 (emul_comp) = 34.28`
  → `score_after_penalty = 34.28` → `score_after_floors = 34.28` → **`final_score_estimate = 34.3` → `grade_estimate = E`**.
- Both agents are declared on the product's own scraped label text (`ingredients_raw` /
  BSIP1 `bsip1_yogurt_55329.json`); this is not an inferred or defaulted classification.

### 55336 — modified starch (medium) + **guar_gum** (low), NOT carrageenan
- `_emulsifier_complexity()` detail: `medium_agents=['modified_starch_stabilizer']`,
  `low_agents=['guar_gum']`, `distinct_agent_count=2` → moderate tier (adj=+1),
  `highest_individual_penalty=3` → `total_penalty=4`, `total_capped=4`.
- `score_after_cap = 40.61` → `− 4.0 = 36.61` → **`final_score_estimate = 36.6` → `grade_estimate = D`**.

### 55343 — modified starch (medium) + **pectin** (low), NOT carrageenan
- `_emulsifier_complexity()` detail: `medium_agents=['modified_starch_stabilizer']`,
  `low_agents=['pectin']`, `distinct_agent_count=2` → moderate tier (adj=+1),
  `highest_individual_penalty=3` → `total_penalty=4`, `total_capped=4`.
- `score_after_cap = 40.46` → `− 4.0 = 36.46` → **`final_score_estimate = 36.5` → `grade_estimate = D`**.

### 58030 — modified starch (medium) + **guar_gum** (low), NOT carrageenan
- `_emulsifier_complexity()` detail: `medium_agents=['modified_starch_stabilizer']`,
  `low_agents=['guar_gum']`, `distinct_agent_count=2` → moderate tier (adj=+1),
  `highest_individual_penalty=3` → `total_penalty=4`, `total_capped=4`.
- `score_after_cap = 39.18` → `− 4.0 = 35.18` → **`final_score_estimate = 35.2` → `grade_estimate = D`**.

## Summary table

| barcode | agents (medium/low) | distinct | tier | emul_comp_penalty | score_after_cap | score_after_penalty | final_score | grade |
|---|---|---|---|---|---|---|---|---|
| 55329 | modified_starch(med) + carrageenan(med, recategorized) | 2 | moderate | 4.0 | 38.28 | 34.28 | 34.3 | **E** |
| 55336 | modified_starch(med) + guar_gum(low) | 2 | moderate | 4.0 | 40.61 | 36.61 | 36.6 | D |
| 55343 | modified_starch(med) + pectin(low) | 2 | moderate | 4.0 | 40.46 | 36.46 | 36.5 | D |
| 58030 | modified_starch(med) + guar_gum(low) | 2 | moderate | 4.0 | 39.18 | 35.18 | 35.2 | D |

Only **55329** is actually graded E among the four; 55336/55343/58030 are D. The −4.0
penalty mechanism is identical across all four (same `_emulsifier_complexity()` code path,
same moderate-tier arithmetic), but 55329's lower pre-penalty `score_after_cap` (38.28 vs
39–41 for the other three, driven by its own `dimension_scores`, not by this penalty) is
what pushes it specifically below the E/D boundary.

## Not a polyol penalty

`sprint1_penalty_polyol_count = 0` for all four (confirmed in `L3_inferred_classifications`
and by direct `_compute_polyol_penalty()` call, which returns `(0.0, ...)` for each). The
−4.0 is exclusively the ECS-v1 emulsifier-complexity mechanism (EV-045), not a sweetener/
polyol mechanism.

## Null-handling is neutral, not worst-case

All four products carry `fat_saturated_g = None` and `dietary_fiber_g = None` in
`L1_observed_signals` (unrecoverable from the scraped label — no fabrication per the OFF-ban
/ missing-data rules). Verified from each trace's `dimension_notes`:
- `nutrient_density`: *"fiber not-applicable for category 'dairy_protein' (EV-027:
  protein-only, 65/35→100/0)"* — the dimension re-weights to protein-only rather than
  scoring the missing fiber as zero-with-penalty.
- `fat_quality`: *"SRC-04: fat < 0.5g or structurally empty → neutral 50"* (this rule fires
  on low/near-zero total fat generally, not specifically on the null saturated-fat subfield
  — saturated fat has no separate scored dimension in this engine version).
- `satiety_support`: formula `(protein×3 + fiber×5) / max(50,kcal) × 400` computes the
  missing-fiber term as `0×5 = 0` (a neutral zero contribution to a sum, not a punitive cap),
  and still receives an unrelated `EV-006 viscous-fiber bonus(+2)`.

None of the four dimensions that touch these two null fields degrade the score below what a
present-but-average value would produce; the engine's documented null-handling rule (EV-027 /
SRC-04) is neutral-substitution, not worst-case substitution. **The E grade on 55329 is a
real, on-label-earned emulsifier-complexity outcome — not a missing-data artifact.**

## Known follow-up (NOT fixed in this record — separate task)

`03_operations/bsip2/proto_v0/src/trace_writer.py::assemble_trace()` omits
`emulsifier_complexity_penalty` from the serialized `penalties_applied` ledger — confirmed
empirically: `penalties_applied: []` in all four traces even though the engine's internal
output dict carries `"emulsifier_complexity_penalty": emul_comp_penalty` at
`score_engine.py:4640`. The arithmetic is unaffected (the engine computes and applies the
penalty correctly at Stage 7, `score_engine.py` ~line 3926–3927, before the trace is even
assembled) — this is a **disclosure gap, not a scoring bug**. It is benign for the numbers
but load-bearing for a public E-grade: a reader auditing the trace today cannot see why
55329 dropped 4.0 points after the cap. **Recommend a separate score-neutral
trace-serialization task** (add `emulsifier_complexity_penalty` +
`emulsifier_complexity_penalty_note` + the `_emulsifier_complexity()` detail dict to
`penalties_applied` in `trace_writer.py`) followed by a trace regen for the drinkable-yogurt
run (and an audit of whether other live categories have the same gap, since
`_emulsifier_complexity()` is shared engine code, not drinkable-yogurt-specific). This
record does not implement that fix — flagging only, per Data Agent scope (score-neutral
documentation task, RT-C1).

## Sign-off

- **Engine integrity:** `score_engine.py` byte-identical to baseline `2474b04a` (verified
  this session, empty `git diff`).
- **Score==trace:** confirmed via `validate_comparison_page.py` — 0/20 mismatches on the
  live drinkable-yogurt page including all four products in this record.
- **Data Agent** documents this record per RT-C1; does not self-approve scoring — this is a
  provenance record of an already-computed, already-shipped score, not a new rule proposal.
