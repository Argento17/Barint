---
id: TASK-323
title: Counterfactual explanation METHOD — minimal-change-to-next-grade computed from BSIP2 traces, NO scoring change
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  P177/C1-GROK (retry 1) fixed the P174 minimization defect + ORCHESTRATOR-VERIFIED. Continuous levers now
  threshold-solve (binary search) to the value closest to current that still crosses the next grade band;
  ingredient-count cliff confirmed at 12 (constants.py PROCESSING_PENALTIES LONG_INGREDIENT_LIST), binary
  has_seed_oil unchanged. INDEPENDENT VERIFICATION: 19/19 continuous levers across achievable records are
  PARTIAL (target >0 and <current); ZERO remain at the 0.0 extreme (the original defect is gone). Cited
  case 5900020015174: sugars_g 24.8 -> 6.5 with note "simulated score 35.0 (D), crosses E->D at 35" — real
  boundary solve; per-product variance (6.5/2.4/9.5/0.4) reflects genuine distance to band, not a default.
  Counts reconcile: 53 processed / 17 achievable (8 single + 9 double via lever_type) / 36 achievable:false
  / 19 partial continuous. SCOPE GUARD VERIFIED EMPTY on score_engine/constants/configs/bari-web/02_products.
  Levers label-observable only; read-only simulation, no scoring path write. Activation (a real consumer
  counterfactual UI + Hebrew authoring) is a later step, out of this wave. Not committed, not pushed.
changes_requested_at: 2026-06-18
changes_requested_reason: >
  P174/C1-GEMINI built method_counterfactual.py + sample.json/md (53 traces, 13 achievable / 40
  achievable:false). STRUCTURE SOUND + orchestrator-verified: scope guard EMPTY (no score_engine/
  constants/config/page edits), levers are label-observable only (sugars_g, ingredient_count,
  has_seed_oil — no fabricated non-label levers), achievable:false honest, counts reconcile via
  lever_type (single 3 + double 10 = 13). BUT FAILS THE CENTRAL DoD ("minimal label change to cross the
  next grade boundary", example sodium -X mg): CONTINUOUS levers are NOT minimized — the method sets
  sugars_g target to 0.0 (the extreme) instead of solving for the threshold value where the grade flips,
  and ingredient_count to a fixed 12. Binary/cliff levers (has_seed_oil, the ingredient-count penalty
  cliff) are acceptably minimal; continuous nutrients are not. "Reduce sugar to 0 to improve the grade"
  is not an accurate/actionable counterfactual and would mislead the end-of-program engine test.
  RE-DISPATCH: retry routed to C1-GROK (Gemini return was all 429 capacity-exhaustion this run) to solve
  continuous levers to the minimal boundary-crossing value (threshold solve / binary search), keep binary
  + cliff levers as-is, preserve all the sound properties. No scoring change.
depends_on: []
blocks: []
category_id: null
summary: >
  Build a standalone post-score method that, given a product's BSIP2 trace (fired signals + dimension scores + grade boundaries), computes the minimal label change that would move it to the next grade band (e.g. sodium -X mg -> C to B). Pure read-over-traces method: changes no score, no engine path, no Hebrew copy (authoring is a later Content step). Emits a structured counterfactual record per product.
---

# TASK-323 — Counterfactual explanation METHOD — minimal-change-to-next-grade computed from BSIP2 traces, NO scoring change

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
