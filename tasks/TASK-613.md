---
id: TASK-613
title: PD-1 refinement: barcode_status must distinguish benign retailer-SKU from true truncation
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-609
lesson_trigger: correction
summary: >
  PD-1 registry flags all non-GTIN barcodes as 'malformed' (129/687). But batch-3 proved many 'short' barcodes are GENUINE Shufersal fresh-item SKUs that name-resolve directly (ld+json gtin == served value) — NOT truncation. Add a reason_code splitting malformed into non_gtin_retailer_sku (resolves on retailer URL) vs truncated/invalid, wired to the TASK-602 reconciliation tables' benign_sku-vs-true_truncation column. Honesty fix: a working retailer SKU shouldn't carry the same alarm as a broken barcode. Registry stays deterministic; recompile.
---

# TASK-613 — PD-1 refinement: barcode_status must distinguish benign retailer-SKU from true truncation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
