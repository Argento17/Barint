---
id: TASK-296
title: Single-path migration of remaining categories onto generate_page.py — brined/butter/bread/cheese-spreads/hard_cheeses (NO bespoke loaders, NO segments)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  Orchestrator-verified both lanes (P156/C1-GROK + Piece-B/C1-Sonnet) independently against artifacts.
  OUTCOME: the single generate_page path is universal — the blocker to a clean baseline is DATA/provenance,
  not architecture. (1) brined → configs/brined_cheeses.json reproduces the GOLDEN page exactly: barcode set
  36/36, rounded-score 0/36, grade 0/36 (verified; the 33/36 "strict" delta = float-vs-int display only).
  Bonus: live _meta.product_count=48 is stale, actual=36. (2) hard_cheeses → configs/hard_cheeses.json,
  score-provenance correctly resolved to run_hard_cheeses_003_shelfrel (30/30 live barcodes reproduced;
  stale _meta.run_id=yohananof_001 confirmed wrong), 0 score/0 grade mismatch on the 28 non-OFF products.
  Both configs ACCEPTED onto the baseline. BLOCKED-ON-DATA (cannot migrate without violating OFF/no-fabrication):
  butter (21/31 live products OFF-contaminated + no per-file corpus), cheese-spreads (no committed run reproduces
  live; built off uncommitted BARI_RECAL_P0 variant; 17/45 null barcodes), bread (no products/ trace tree;
  15/19 null barcodes), salty_snacks (no traces — TASK-228). SURFACED TO OWNER (tripwire-1 / OFF hard rule):
  3 live pages serve OFF-sourced ingredients NOW — butter (21/31), hard_cheeses (2/30) — launch blockers per
  TASK-238. Live pages untouched; no commit; no publish. Residual = upstream data work + owner OFF decisions.
summary: >
  Bring the remaining real-trace categories onto the SINGLE generate_page.py config path (no per-category Python loaders). One config per category pointing at the run that actually produced the live scores (matched by score-provenance, NOT stale _meta.run_id). cheese-spreads uses the generator's already-supported list-valued run_products_dir for its multi-source merge. salty_snacks EXCLUDED (no BSIP2 traces exist — blocked on TASK-228, not a loader problem). Output to NEW files; never overwrite live; prove barcode+score+grade parity vs live.
---

# TASK-296 — Single-path migration of remaining categories onto generate_page.py — brined/butter/bread/cheese-spreads/hard_cheeses (NO bespoke loaders, NO segments)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
