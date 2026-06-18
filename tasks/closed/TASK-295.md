---
id: TASK-295
title: TASK-233F migration bucket C (cookies_coffee, salty_snacks) → generate_page configs + parity verify
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
depends_on: [TASK-292]
blocks: []
category_id: null
closed_at: 2026-06-16
close_reason: >
  C1-Sonnet (Agent), orchestrator-verified vs LIVE. COOKIES_COFFEE: clean migration — configs/cookies_coffee.json
  reproduces live v2 118/118 barcodes + 118/118 grade (0 flips), generated==trace exact; self-gate PASS.
  101/118 score within |Δ|<0.6 vs live; 17 drift |Δ|=0.6-1.3 = engine drift (live mildly stale, NO grade impact).
  ACCEPTED. SALTY_SNACKS: CARVED OUT — bespoke loader; live v4 built by TASK-237/241 hand-built path, 0/29 barcode
  overlap with any BSIP2 run (runs hold a different Carrefour corpus). Not forced; needs fresh BSIP run or custom
  loader. Live pages untouched.

summary: >
  Author configs/{cookies_coffee,salty_snacks}.json on generate_page.py (cereals pattern); parity vs live; NEW files, no overwrite; flag bespoke-loader.
---

# TASK-295 — TASK-233F migration bucket C (cookies_coffee, salty_snacks) → generate_page configs + parity verify

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
