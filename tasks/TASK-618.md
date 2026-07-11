---
id: TASK-618
title: registry recovered_gtins() key-name mismatch: 3 true truncations get no recovered_gtin
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-613
lesson_trigger: none
summary: >
  TASK-613 flagged: registry_ops.py recovered_gtins() reads served_barcode/old_barcode/truncated_barcode + recovered_gtin/resolved_gtin/true_gtin/resolved_barcode, but the committed batch2 yogurt-drinkable field is 'true_gtin_discovered'. So the 3 true truncations (bsip1_yogurt_55336/4068035/58030) keep recovered_gtin=null and barcode_status=malformed instead of found_but_conflicting. Small key-alias fix; changes barcode_status transitions so verify deterministically (--check/--selftest) after. Left untouched by 613 per its stability guard.
---

# TASK-618 — registry recovered_gtins() key-name mismatch: 3 true truncations get no recovered_gtin

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
