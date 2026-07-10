---
id: TASK-475
title: Diagnose BSIP1->BSIP2 ingredient handoff loss (bread-family): scope + measured score impact
owner: data-agent
status: RETURNED
priority: CRITICAL
created_at: 2026-07-03
verified_at: 2026-07-03
depends_on: []
blocks: []
category_id: null
summary: >
  From TASK-474 bread red-team (CONFIRMED): bread BSIP1 has populated ingredient_order (12 items) but empty ingredients_list; BSIP2 reads ingredients_list -> scored ingredient_count=0 (NOVA/structural/confidence degraded). Same root as crackers F3. Scope UNKNOWN across categories (ingredient_count=0 appears widely but some are legit-empty e.g. juices). DIAGNOSE: per-product BSIP1(ingredient_order/text) vs BSIP2(ingredient_count) to separate real-loss from legit-empty across ALL live categories; then MEASURE score/grade delta if the handoff is fixed (re-run engine on corrected input, compare — DO NOT promote/deploy). Output = scope table + impact table for owner rescore go/no-go. TRIPWIRE-1: changes no published score.
---

## RETURNED — orchestrator-verified. Root cause + scope + measured impact in hand.

**Root cause (code-level, confirmed):** `03_operations/bsip2/proto_v0/src/input_loader.py::get_ingredients()` reads ONLY `ingredients_list`; never falls back to the populated `ingredient_order` / `ingredients_text_he`. Bread-family BSIP1 builds leave `ingredients_list=[]` while `ingredient_order` is full → scorer runs on `ingredient_count=0`.

**Scope (16 live categories, 580 products) — orchestrator spot-verified (bread 23/23 & crackers 19/19 REAL_LOSS match my own check; LEGIT_EMPTY = hard-cheeses 6 + juices 2 correctly genuinely-empty):**
- **REAL_LOSS = 57**: bread 23/23, crackers 19/19, protein-bars 15/32. Every other category OK.
- OK = 515, LEGIT_EMPTY = 8, none unmeasurable.

**Measured impact (57 re-scored on real BSIP1 ingredients, engine + exact live flag vector; NOTHING promoted):**
- **8 of 57 grades move — ALL DOWNWARD** (A→B, B→C, C→D). 0 up.
- Score Δ: mean −1.39, median −0.30, range −6.70..+7.00. 34 lower, 18 flat, 5 higher (no upward grade cross).
- Direction sensible: missing ingredients = escaped additive/processing penalties = **live scores INFLATED**; fix lowers them. Flagship bread 7290016245325 94.8/S→90.8/S (stays S); top sourdoughs stay A. Movers are lower-tier products losing inflation.

**Verification notes:** published scores untouched (only scratch artifacts + a gates report/test file, reverted). C0 gate substance-clean (FAILs = contract artifact-shape/count-format drift only). ⚠️ concurrent-agent collision: this Data Agent reverted my uncommitted TASK-472 crackers edits in the MAIN tree — harmless, PR #56 branch intact (commit 0e9d8241 verified).

**DECISION OWED (owner, tripwire-1):** fix `input_loader.py` fallback + re-flow bread/crackers/protein-bars (needs Nutrition+Product co-sign per scoring-rule-implementation hard rule) vs hold vs disclose-defer. Surfaced to owner with go/no-go. **No pipeline code / rescore until owner GO + co-sign.**

# TASK-475 — Diagnose BSIP1->BSIP2 ingredient handoff loss (bread-family): scope + measured score impact

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
