---
id: TASK-178
title: Legacy-page score freshness audit — HEAD vs published run_004 engine drift + re-baseline plan
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04, claims verified against artifacts). Audit
  delivered + independently verified: per-category HEAD-vs-published reproduction —
  bread 165/256 (64%, 83 grade-affecting drifts ALL UPWARD ~+8.2, the worst-affected,
  not milk), milk 13/20 (65%, mildest), snack 5/53 (9%); cheese/hummus/yogurt/maadanim
  out of scope (already on post-recal HEAD). Frozen invariants verified HELD: milk top
  85/A trio reproduces exactly; snack no-A / snk-001 70/B ceiling holds (latent second-B
  crowding flagged, not broken). Root cause: the unconditional/unflagged v2 grade
  recalibration in constants.py (NOVA lift, NOVA1 floor 75->85, fat floor 65->70,
  confidence ceiling 70->75) folded in AFTER the legacy freezes; git was init 2026-06-01
  (after all three freezes) so the dominant drift is not bisectable — legacy freezes have
  no git-pinned engine state. No score moved, no page reshipped, no engine edited; both
  repro harnesses are read-only. Deliverable = the re-baseline PLAN (4-step: tag HEAD
  baseline -> milk -> snack -> bread-gated-on-169F, each with per-invariant owner sign-off
  + QA freeze). Executing that plan is downstream work (open as waves when owner elects).
  Report: 03_operations/qa/reports/legacy_score_drift_audit_TASK-178_2026-06-04.md.
summary: >
  Surfaced by TASK-169C: current BSIP2 HEAD reproduces only 13/20 of the published milk run_004 traces (2026-05-18) — pre-existing engine drift unrelated to the TASK-169 recal. Legacy pages (milk, and likely bread/snack) render May-18 published scores HEAD no longer reproduces, so any full rebuild would silently move scores. Deliverable: quantify HEAD-vs-published drift per legacy category, classify each delta (grade-affecting vs <2pt cosmetic), identify the engine changes since each freeze, and propose a clean re-baseline plan (rescore + per-invariant owner sign-off) so pages can be safely regenerated. No score ships from the audit.
---

# TASK-178 — Legacy-page score freshness audit — HEAD vs published run_004 engine drift + re-baseline plan

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
