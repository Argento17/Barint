---
id: TASK-627
title: Trace-backfill: emit standard BSIP2 traces for bespoke-scored shelves (protein_bars pilot) so scores become trace-derivable (scores UNCHANGED)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-625
summary: >
  protein_bars 32/32 scored by quarantine script, no standard traces -> not derivable. Emit standard per-barcode BSIP2 trace files from the existing rerank_table_rescore.json (scores UNCHANGED, verify byte-identical) so build_dossiers load_bsip2_traces finds them -> calculation check flips warn->pass. Pilot protein_bars; template for other bespoke shelves. Do NOT re-score.
---

# TASK-627 — Trace-backfill: emit standard BSIP2 traces for bespoke-scored shelves (protein_bars pilot) so scores become trace-derivable (scores UNCHANGED)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
