---
id: TASK-618
title: registry recovered_gtins() key-name mismatch: 3 true truncations get no recovered_gtin
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
close_reason: >
  Key-alias fix DELIVERED (data-agent, commit fff30a15) + orchestrator-verified. recovered_gtins()
  now reads the real committed field names (`barcode` + `true_gtin_discovered`) — no invented keys.
  VERIFIED: commit=2 registry files, --check PASS, distribution malformed 129→126 / found_but_conflicting
  0→3 (sum 687), recovered_gtin populated on EXACTLY the 3 yogurt truncations (7290000055336 /
  7290000058030 / 7290004068035), 684 records byte-identical. --selftest extended + PASS. Deterministic.
  The 3 genuine truncations now correctly carry their recovered GTIN + found_but_conflicting status.
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
