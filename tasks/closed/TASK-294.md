---
id: TASK-294
title: TASK-233F migration bucket B (hard_cheeses, cakes_hard_cookies) → generate_page configs + parity verify
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
depends_on: [TASK-292]
blocks: []
category_id: null
closed_at: 2026-06-16
close_reason: >
  C1-GEMINI (P155), orchestrator-verified vs LIVE pages. CAKES_HARD_COOKIES: clean single-run migration —
  configs/cakes.json reproduces live 65/65 barcodes + 65/65 score + 65/65 grade (run_cakes_shelfrel_001,
  84 exclusions for the Wave-1 cakes-only subset). ACCEPTED. HARD_CHEESES: CARVED OUT — agent pointed config
  at run_hardcheese_redlabel_v1_001 (UNSHIPPED experimental BARI_REDLABEL_V1 run) → 0/28 score match vs live;
  and the stated source run_hard_cheeses_yohananof_001 also fails (live 77.6 vs trace 73.6) → live page is a
  multiretailer MERGE (Shufersal baseline + Yohananof), same bespoke-loader class as cheese. Misleading config/
  output REMOVED. hard_cheeses + cheese → backlog: generate_page custom merge-loader. Live pages untouched.

summary: >
  Author configs/{hard_cheeses,cakes_hard_cookies}.json on generate_page.py (cereals pattern); parity vs live; NEW files, no overwrite; flag bespoke-loader.
---

# TASK-294 — TASK-233F migration bucket B (hard_cheeses, cakes_hard_cookies) → generate_page configs + parity verify

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
