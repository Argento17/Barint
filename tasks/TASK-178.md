---
id: TASK-178
title: Legacy-page score freshness audit — HEAD vs published run_004 engine drift + re-baseline plan
owner: qa-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-03
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced by TASK-169C: current BSIP2 HEAD reproduces only 13/20 of the published milk run_004 traces (2026-05-18) — pre-existing engine drift unrelated to the TASK-169 recal. Legacy pages (milk, and likely bread/snack) render May-18 published scores HEAD no longer reproduces, so any full rebuild would silently move scores. Deliverable: quantify HEAD-vs-published drift per legacy category, classify each delta (grade-affecting vs <2pt cosmetic), identify the engine changes since each freeze, and propose a clean re-baseline plan (rescore + per-invariant owner sign-off) so pages can be safely regenerated. No score ships from the audit.
---

# TASK-178 — Legacy-page score freshness audit — HEAD vs published run_004 engine drift + re-baseline plan

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
