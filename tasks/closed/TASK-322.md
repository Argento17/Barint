---
id: TASK-322
title: HP carb+sodium cluster — detection METHOD + calibration DATASET (third Fazzino cluster), NO scoring activation
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  P173/C1-GROK delivered + ORCHESTRATOR-VERIFIED. method_hp_carb_sodium.py (standalone) computes the
  Fazzino carb+sodium cluster (>40% kcal carb via carbs*4/kcal, Atwater fallback when energy missing;
  Na>=200mg/100g); thresholds inert HP_CARB_SODIUM_* (NOT in score_engine/constants). Calibration over
  979 BSIP1 products / 12 shelves: independently reconciled 283 fired + 89 insufficient_data + 607
  not_fired = 979; calibration.json + calibration.md (321 lines, FP review table present, cites 283/979)
  both exist. OFF-ban honored (missing field -> insufficient_data, no fill). SCOPE GUARD VERIFIED: git diff
  --stat on score_engine.py / constants.py / configs/ / bari-web comparisons = EMPTY (exit 0) — zero
  scoring activation, zero published-score movement, as owner required. FP signal surfaced for the later
  D6/D7 step: endemic-food false positives (brined cheese 1/48 @45.55% carb, some cakes/cheese) need a
  context guard like the EV-054 brined-suppression precedent before any activation. Activation/governance
  remains OUT of scope (separate program). Not committed, not pushed.
depends_on: []
blocks: []
category_id: null
summary: >
  Build a standalone detection method for the Fazzino carbs+sodium hyper-palatability cluster (>40% kcal carbs + >=200mg/100g sodium) and run it across live BSIP1 corpora to produce a calibration/false-positive dataset. Method+data ONLY: no penalty wired, no published-score movement, behind no live scoring path. Governance/activation (D6/D7) is explicitly OUT of scope for now.
---

# TASK-322 — HP carb+sodium cluster — detection METHOD + calibration DATASET (third Fazzino cluster), NO scoring activation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
