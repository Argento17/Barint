---
id: TASK-591
title: Corpus audit: published fat values with EV-026 signature (fat=0.5 from trans-row overwrite)
owner: nutrition-agent
status: IN_PROGRESS
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
