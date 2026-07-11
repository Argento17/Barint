---
id: TASK-624
title: Barcode adjudication: resolve the 152 barcode issues (126 malformed / 23 pending / 3 conflicting)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
close_reason: "VERIFIED + committed 6a5fccf8. 152 barcode issues classified (6 recovered / 121 benign-SKU verified 76/76 vs retailer image slugs / 25 true-review); registry_ops --check+--selftest PASS; additive task624 marker; malformed 126->123, conflicting 3->6, unclassified-malformed 81->2. Manual-review spawns: 6 shelf-mapping PID_SPLIT->Product Agent, 14 NOT_FOUND->re-scrape lane, 1 manifest anomaly, 2 checksum candidates. PD index refreshes on next PD-2 run."
summary: >
  Classify the 152 barcode-issue products: recoverable (recover GTIN via registry_ops like TASK-618) vs benign-malformed (real retailer SKU, downgrade not break) vs true-manual-review. Apply the recoverable/benign classifications to the registry; queue true manual-review. Reduce the barcode defect class.
---

# TASK-624 — Barcode adjudication: resolve the 152 barcode issues (126 malformed / 23 pending / 3 conflicting)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
