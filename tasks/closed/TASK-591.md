---
id: TASK-591
title: Corpus audit: published fat values with EV-026 signature (fat=0.5 from trans-row overwrite)
owner: nutrition-agent
status: CLOSED
close_reason: >
  BUILD-LIGHT (Codex gpt-5.6-terra) read-only audit delivered and orchestrator-verified: C0 PASS,
  sanity anchor reproduced (5010029000061 CONFIRMED 0.5 vs 2.0), one replay independently re-run by
  orchestrator (7296073705574: raw rows -> 13.6g vs published 0.5 - matches the table), denominators
  named (757 products / 20 files). RESULT: 22 fat==0.5 hit records (20 unique barcodes);
  15 CONFIRMED_DISCREPANCY - ALL in cereals_frontend_v2.json (15 of the shelf's 20 products; true
  fat 2.0-13.6g), 7 NO_EVIDENCE (2 bread x2 files, 3 yogurt), 0 CONSISTENT. Zero corpus writes
  (verified: only report + return created). Report: 03_operations/reports/task591_fat_ev026_audit.md.
  OWNER DIGEST: displayed nutrition on ~75% of the cereals shelf is wrong (EV-026-era values);
  score impact undetermined (cereals is one of the TASK-563 8 non-recoverable-trace shelves);
  any correction = tripwire-1, joins the standing 8-shelf paper-trail decision.
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Escalated from TASK-590 and orchestrator-verified in the raw JSON: cereals_frontend_v2.json publishes fat=0.5 for barcode 5010029000061 while the freshly parsed live label reads 2.0g - 0.5 is the exact pre-TASK-142A EV-026 signature (trans row 'pahot me-0.5' overwrote total fat). Audit the PATTERN corpus-wide, not the instance: every published fat value of exactly 0.5 across all served comparison JSONs, cross-checked against raw captured panels where they exist. READ-ONLY deliverable: a discrepancy table (product, published fat, evidence fat, source file). NO data or score changes - if any discrepancy implies score movement, that is a tripwire-1 owner decision; produce the movement table and stop. Note: once TASK-590's shelf_watch fix runs its first real weekly scan, affected products will surface as nutrition_drift on fat_g - those alerts corroborate, they do not authorize correction.
---

# TASK-591 — Corpus audit: published fat values with EV-026 signature (fat=0.5 from trans-row overwrite)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
