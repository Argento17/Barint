---
id: TASK-324
title: Salvage TASK-239 BSIP0 parser hardening from salty-snacks-v4 into master (then retire the branch)
owner: data-agent
status: CLOSED
priority: HIGH
close_reason: >
  Orchestrator-verified 2026-06-18 on salvage/bsip0-parser-task239 (9adafb208, pushed). Data Agent reconciled
  salty-snacks-v4's TASK-239 parser into master's diverged parser (additive multi-table machinery, no conflicts;
  public signatures stable). Orchestrator ran the tests independently: 20/20 PASS (12 pre-existing + 8 new
  dual-table). Regression: 505 products across 5 files UNCHANGED; 33 products gain a corrected Hebrew-"מג" sodium
  reading (documented improvement, BSIP0 scrape-time → no live-score impact, scores baked in frontend JSONs).
  ZERO OFF-enabling code (gate references OFF tokens only as blocking-detection strings; the contradictory
  "retract OFF ban" commit was NOT brought). salty-snacks-v4 value salvaged → branch DELETED. PR salvage/bsip0-parser-task239
  → master is owner's merge gate (engine, score-neutral for live).
created_at: 2026-06-18
depends_on: [TASK-323]
blocks: []
category_id: null
summary: >
  salty-snacks-v4 (wiped category) carries real UNMERGED, category-agnostic engine value in _shared/:
  TASK-239 BSIP0 nutrition-parser hardening (dual-table parsing + BSIP0 exit gate + fixtures + unit tests).
  master's parser diverged independently (663 lines / 12 markers vs salty's 829 / 23). Salvage the TASK-239
  features into master's parser via careful reconciliation, tests passing, no nutrition-parse regression on
  live products, PR to master — THEN salty-snacks-v4 is safe to delete. Last loose end of the consolidation.
---

# TASK-324 — Salvage TASK-239 BSIP0 parser hardening

## Dispatch: Data Agent (2026-06-18), worktree C:\bari-parsersalvage → branch salvage/bsip0-parser-task239
Reconcile salty-snacks-v4's TASK-239 parser (`_shared/bsip0_nutrition.py` +dual-table, `05_bsip0_gate.py`,
fixtures, `test_bsip0_nutrition.py`) into master's diverged parser. Tests pass + no live nutrition regression →
PR to master. RETURNED-UNVERIFIED until orchestrator verifies. After merge, delete salty-snacks-v4.
