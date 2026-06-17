---
id: TASK-319
title: Spine step 4 — orchestration command (flip a flag → shadow gate → affected-set → trigger → copy → gates → deploy-ready bundle)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-316, TASK-317, TASK-318]
blocks: [TASK-320]
category_id: null
close_reason: >
  C1-GROK built spine_flip.py (commit abc275e00). Orchestrator-verified by independently RUNNING both paths: e2e
  BARI_GLASSBOX_W4=on → affected cereals+hummus, both re-scored+copy-staged+gated, bundle+report+consolidated_author_set written,
  "DEPLOY-READY: 2 shelves, 0 author, gates REVIEW, frozen breach none. No push performed.", exit 1 (movement), 6.1s. Frozen gate:
  BARI_RECAL_P0=on → frozen_breaches [milk,snack_bars], "FROZEN BREACH — HARD BLOCK", exit 2, 0 shelves processed, 2.8s. Exit codes
  confirmed cleanly (1 movement / 2 frozen). No push/PR/deploy occurred; orchestration only (subprocess to the existing CLIs);
  single new file. "gates REVIEW" = the known G1/G2/G6 v3-schema-vs-match-live artifact (integrity gates G4/G5/G7/G8 clean), recorded
  honestly. SPINE CORE COMPLETE — a scoring-flag change now becomes a gated, copy-applied, deploy-ready bundle via one command.
summary: >
  The crown: one command that chains the now-existing pieces into the owner's "flip a switch → everything re-flows" flow.
  `spine_flip.py --set BARI_X=on`: (1) affected_set.py (step 2) → affected shelves + FROZEN GATE (frozen_touched → STOP/BLOCK,
  exit 2); (2) for each affected shelf, rescore_all.py (trigger; step-1 render contract → drop-in staging); (3) copy_stage.py
  (step 3) → carry grade-unchanged copy + author_set; (4) run_gates.py per shelf (G1-G8 must pass); (5) aggregate a spine_run
  report (affected shelves, score/grade moves vs baseline, consolidated author_set = what copy needs authoring, gate results,
  frozen status, OFF=0); (6) emit a DEPLOY-READY BUNDLE (staged pages + report + author_set). Orchestration ONLY — chains existing
  CLIs; NO engine/scoring edits; staging-only; **NO push/PR/deploy** (the deploy-ready bundle is produced; owner does the merge).
  OFF-ban absolute. Verify end-to-end on a real flag what-if (e.g. BARI_GLASSBOX_W4=on → affects cereals+hummus). Route C1-GROK.
---

# TASK-319 — Spine step 4: orchestration command

See `tasks/prompts/P169_spine_orchestration.md`. This is the visible spine: one command turns a scoring-flag change into a
gated, copy-applied, deploy-ready bundle. Frozen invariants are a hard stop. Deploy/merge stays owner-gated.
