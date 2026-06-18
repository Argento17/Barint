---
id: TASK-327
title: Spine first-run: palm-hydro alias flip (cakes) + spine validation
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-18
depends_on: []
blocks: []
category_id: cakes
close_reason: >
  Two-part deliverable both DONE + orchestrator-verified. (1) ENGINE: palm-hydro aliases (שמן דקל מוקשה /
  שמן דקלים מוקשה / שומן דקל מוקשה) added to the EXISTING EV-097 generic tier (ceiling 55, NOT partial 40)
  behind new flag BARI_PALM_HYDRO_V1 default-OFF (signal_extractor.py +22/-4). Functional test: OFF=all False
  (byte-identical); ON=target fires, plain שמן דקל + עמילן מוקשה stay False (C3 traps clear). C3 (P206)
  validated generic-tier placement (PMIDs 3362176/17224066). COMMITTED default-OFF per owner (2026-06-18) —
  dormant-but-proven, like EV-011 parked. (2) SPINE FIRST-RUN: spine_flip --set BARI_PALM_HYDRO_V1=on ran all
  stages in 6.1s, frozen breach NONE, gates REVIEW (guard working). Spine machinery VALIDATED. FINDING: flag is
  a NO-OP on live corpus (0 score_moves; 0 products carry שמן דקל מוקשה anywhere) → nothing to merge, no
  tripwire-1. First run also surfaced (a) affected_set over-inclusion and (b) the render-contract gap → TASK-330.
  Staging-only; NO deploy.
summary: >
  Add palm-hydrogenation aliases (שמן דקל מוקשה) to the EXISTING EV-097 generic PHVO tier (ceiling 55, NOT partial/trans tier 40) behind a new default-OFF flag; then exercise spine_flip.py end-to-end on cakes as the spine's first live validation. Staging-only; merge owner-gated (published-score move = tripwire 1).
---

# TASK-327 — Spine first-run: palm-hydro alias flip (cakes) + spine validation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
