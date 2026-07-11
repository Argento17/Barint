---
id: TASK-624
title: Barcode adjudication: resolve the 152 barcode issues (126 malformed / 23 pending / 3 conflicting)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
summary: >
  Classify the 152 barcode-issue products: recoverable (recover GTIN via registry_ops like TASK-618) vs benign-malformed (real retailer SKU, downgrade not break) vs true-manual-review. Apply the recoverable/benign classifications to the registry; queue true manual-review. Reduce the barcode defect class.
---

# TASK-624 — Barcode adjudication: resolve the 152 barcode issues (126 malformed / 23 pending / 3 conflicting)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
