---
id: TASK-625
title: Diagnose protein_bars 32/32 whole-shelf breakage (systemic-cause probe)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
close_reason: "DIAGNOSIS delivered + verified vs shelf configs. protein_bars 32/32 = quarantined one-off script (batch_run_protein_bars_task365.py), scored inline, emitted NO standard BSIP2 traces (bsip1_dir=null) -> scores correct+reproducible but not trace-derivable. Fix class = TRACE-BACKFILL (not re-score). cakes/crackers/cheese = same TASK-563 family, partial run-dir drift. Spawns the trace-backfill lane."
summary: >
  protein_bars is 32/32 (100%) with >=1 PD issue — anomalous. READ-ONLY diagnosis: which check(s) fail for the whole shelf (calc/barcode/traceability/publishability), the single systemic root cause, and the fix class. Report only, no writes.
---

# TASK-625 — Diagnose protein_bars 32/32 whole-shelf breakage (systemic-cause probe)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
