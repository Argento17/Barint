---
id: TASK-292
title: Cereals generate_page migration — pattern-setter for TASK-233F core consolidation onto generate_page.py
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  C1-GEMINI (P153), orchestrator-verified independently: generated cereals_generated_v1.json vs live
  cereals_frontend_v2.json = 20/20 barcodes identical, 0 score/grade mismatches, live page untouched,
  self-gate PASS. configs/cereals.json captures the curation (43 exclusions: 25 granola subpool + 6 OFF
  + 12 out-of-scope). PROVES generate_page.py as THE TASK-233F shared core (frontend_core.py = phantom,
  abandoned). Pattern set for the remaining category migrations.
depends_on: [TASK-233F]
blocks: []
category_id: null
summary: >
  Prove generate_page.py as THE shared core (frontend_core.py is a phantom). Author configs/cereals.json reproducing the live curated cereals page's scored data (parity: same products/scores/grades) from run_cereals_008. Output to a NEW file, do NOT overwrite live. Sets the pattern for the other ~9 category migrations.
---

# TASK-292 — Cereals generate_page migration — pattern-setter for TASK-233F core consolidation onto generate_page.py

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
