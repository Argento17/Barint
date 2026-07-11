---
id: TASK-630
title: Wire re-scored traces (bread/crackers/cheese) into PD read-path so calc becomes derivable + fix parity_gate cp1252 print bug
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-629
summary: >
  TASK-629 re-scored bread/crackers/cheese (scores correct, parity diverge=0) but calc check FAILS (18+17+17) because the new BSIP2 traces (task629_corrected/output) aren't wired into the shelf configs' run_products_dir that build_dossiers reads -> served-new vs trace-old mismatch. Repoint configs at the re-scored traces (same trace-backfill pattern as protein_bars 32/32 pass) -> calc flips pass. Also fix parity_gate.py UnicodeEncodeError on cp1252 (Hebrew print).
---

# TASK-630 — Wire re-scored traces (bread/crackers/cheese) into PD read-path so calc becomes derivable + fix parity_gate cp1252 print bug

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
