---
id: TASK-543
title: Reconcile yogurt frontend_out mirror files (d4 + copy drift across FINAL_v2/v3 vs frontend_v1 vs bari-web)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  During the yogurt copy/data fix cycle (2026-07-08), multiple mirror copies diverged: bari-web/src/data/comparisons/yogurt_*_frontend_v1.json (the RENDERED source-of-truth, now fully correct: fixed d4 + re-voiced+surgically-corrected copy) vs 02_products/.../frontend_out/{FINAL_v2,FINAL_v3,frontend_v1,COPY_DRAFT,D7_SUPPRESS}.json which carry stale d4 (E472e/DATEM, empty LBG) and/or stale copy. Data Agent flagged frontend_out was already out-of-sync before edits + different generator-run timestamps. ACTION: designate ONE canonical mirror, regenerate/resync it from the corrected bari-web file (or retire the stale snapshots), so provenance matches live. Not a render blocker (bari-web is authoritative) but must be clean before commit. Verify 0 score/grade drift after resync.
---

# TASK-543 — Reconcile yogurt frontend_out mirror files (d4 + copy drift across FINAL_v2/v3 vs frontend_v1 vs bari-web)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
