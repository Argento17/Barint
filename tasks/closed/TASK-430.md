---
id: TASK-430
title: Juices baseline non-reproducible: diagnose before any refresh (carved out of TASK-418 bundle)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
closed_at: 2026-07-01
close_reason: >
  Diagnosis complete + orchestrator-VERIFIED (P276). PREMISE CORRECTED: juices is NOT non-reproducible —
  published juices_frontend_v3 reproduces 17/17 EXACT against committed traces
  run_juices_yohananof_002/products (orchestrator independently confirmed 17/17, drift 0; e.g. 7290019056720
  committed trace = 41.8/D = published). The earlier "11/17" was a HEAD-rescore comparison artifact, not a
  baseline defect. All 6 P268 drifters = engine-drift (0 invocation-gap, 0 genuinely-defective): the published
  scores rest on run_juices_yohananof_002 (generated ~2026-06-07); the HEAD engine differs due to a
  functional-fiber classifier change (EV-006 extension, commit 75e4e73b 2026-06-14, i.e. AFTER publish).
  7290019056737 (36.0/D) = correct committed-trace value, restored by TASK-409 (e51db8d1), not an artifact.
  CAVEAT (orchestrator): the agent's stated "+2 fiber bonus at HEAD" cannot alone explain the DOWNWARD HEAD
  drift (committed trace shows satiety_support=0) — exact mechanism needs Nutrition confirmation. OUTCOME:
  juices correctly HELD from the TASK-418 refresh (it is engine-evolution, not a data-clean like HC/cheese).
  ROUTED: "should stabilizer-context pectin/gums (E412/E414) earn a functional-fiber bonus in zero-fiber
  juices?" is a Nutrition scoring-philosophy question — and adopting HEAD juice scores would MOVE published
  scores (tripwire #1, owner-gated). Flagged for Nutrition + owner; not implemented (lane law).
depends_on: []
blocks: []
category_id: null
summary: >
  Juices baseline non-reproducible: diagnose before any refresh (carved out of TASK-418 bundle)
---

# TASK-430 — Juices baseline non-reproducible: diagnose before any refresh (carved out of TASK-418 bundle)

## Context (orchestrator, 2026-07-01)
The owner approved a bundled TASK-418 refresh (HC + the TASK-405 cheese/cereals set). Verification (P268 +
orchestrator) shows **juices does NOT fit the clean-refresh story and must NOT ship in that deploy:**
- **Baseline non-reproducible:** `juices_frontend_v3.json` published scores don't reproduce under the config's
  invocation (P268: 11/17 reproduce; `7290019056737` pub=36.0 matches neither pre- nor post-D4 engine output).
- **Drift is DOWNWARD** (unlike cheese/cereals which drift up from TASK-405 de-pollution): 6 juices drifters
  all negative (−0.6 to −5.7), incl. a grade move DOWN `7290019056737` D→E.
- **NOT TASK-405-cleaned:** the juices drifters carry no `_task405_clean` stamp (verified) — so the downward
  drift has NO established mechanism. Refreshing blind would LOWER live scores for an unknown reason.
- Prior context: juices `v3` uses a different schema; validate_comparison_page + run_gates G1 FAILED on it
  before (TASK-418 abort note).

## Deliverable
Do a TASK-429-style diagnosis for juices: find/document the canonical invocation (flags + shelf-stats + corpus
source + schema) that byte-reproduces the published `juices_frontend_v3` scores, OR prove the published scores
rest on a since-changed engine/data state and classify each drifter {invocation-gap | data-refresh |
genuinely-defective}. Resolve `7290019056737` specifically. Score-neutral analysis; isolated worktree; no
deploy. Output the movement table + mechanism per drifter. Blocks any juices refresh.
