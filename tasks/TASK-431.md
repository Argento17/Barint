---
id: TASK-431
title: Brand backfill for bread + hummus (display-only, no re-score)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Capture the manufacturer/brand field for bread (26/29 missing) and hummus (57/57 missing) from the real scrape — existing BSIP0 artifacts first, targeted re-scrape only if needed. Display-only: scores/grades/nutrition byte-identical. Never OFF, never fabricate. Updates bread/hummus frontend JSON; brand then shows on catalog + comparison pages.
close_reason: >
  Verified (orchestrator, independent diff): hummus 0/57 -> 29/57 brands added (Strauss x14, Tzabar x13,
  Alllechem, Biton Yohai) from Rami Levy first-party API (direct retailer, NOT OFF), barcode-matched +
  name-plausibility checked; 3 ambiguous candidates correctly rejected (no fabrication). git diff = 29
  brand lines added, 0 score/grade/name lines changed (byte-clean, display-only). Bread stayed 3/29 —
  honestly blocked: 20/29 barcodes are internal Shufersal SKUs (non-GS1, uncross-matchable), 6 EAN13s
  absent from Rami Levy; reported not forced. Data agent also fixed a PRE-EXISTING schema-lag defect
  (page_output_schema_v1.json now whitelists the already-shipping `brand` field; additive, zero score
  impact, unblocks G1 across categories). Build green; brand now renders on catalog + hummus comparison page.
# TASK-431 — Brand backfill for bread + hummus (display-only, no re-score)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
