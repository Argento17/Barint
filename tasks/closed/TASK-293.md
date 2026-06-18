---
id: TASK-293
title: TASK-233F migration bucket A (juices, cheese) → generate_page configs + parity verify
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
depends_on: [TASK-292]
blocks: []
category_id: null
closed_at: 2026-06-16
close_reason: >
  C1-GROK (P154), orchestrator-verified. JUICES: configs/juices.json valid — generated reproduces the
  CURRENT engine 20/20 barcodes + 20/20 vs trace (run_juices_yohananof_002); self-gate PASS. Independent
  diff vs LIVE juices_frontend_v3.json = 15/20 score / 19/20 grade — the 5 deltas (incl. 7290019056737
  E32.3->D36.0) are ENGINE DRIFT (live page stale vs current blessed engine), NOT a config bug; a juices
  re-publish would move 5 scores/1 grade = owner-gated (tripwire-1), logged not shipped. CHEESE: correctly
  STOPPED — bespoke multi-retailer loader (build_yogurt_cheese_multiretailer_frontend.py; 17/45 barcode:null)
  incompatible with generate_page barcode-walk; needs a custom loader (backlog). Live pages untouched.

summary: >
  Author configs/{juices,cheese}.json on generate_page.py (cereals pattern); reproduce each live page's scored data (parity: barcodes/scores/grades); output to NEW files, no overwrite; flag bespoke-loader incompatibility.
---

# TASK-293 — TASK-233F migration bucket A (juices, cheese) → generate_page configs + parity verify

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
