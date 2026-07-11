---
id: TASK-607
title: Served corpus barcode integrity: 146/710 products have a barcode too short to be a valid GTIN
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
lesson_trigger: correction
lesson_outcome: implementation_task
lesson_generated_task_id: TASK-613
lesson_evidence: "TASK-602 batch-3/4/5 barcode reconciliation: 0 true_truncation across ~120 short codes (all benign Shufersal SKUs/PLUs); census + registry confirm"
lesson_signature: barcode_short_misread_as_truncation
lesson_related: [TASK-613]
close_reason: >
  ALARM RESOLVED as largely FALSE. The 146/710 truncated-barcode scare was a misread: three
  re-scrape batches + the census confirm 0 true truncations corpus-wide (short codes are genuine
  Shufersal SKUs/PLUs that resolve directly; only ~3 yogurt-drinks were true truncations). The PD-1
  identity registry is now the identity source of truth (bari_pid = join key, barcode = attribute)
  and holds recovered_gtin. No mass served-barcode backfill needed. Reason-code split -> TASK-613.
  LESSON (correction): verify the MECHANISM (short != truncated) by resolving a sample against the
  retailer before quantifying a corpus-wide integrity crisis.
depends_on: []
blocks: []
category_id: null
summary: >
  Found by TASK-602 fan-out (2026-07-11): the served bari-web/src/data/comparisons/*_frontend_v*.json 'barcode' field is too short to be a valid GTIN on 146/710 products (21%) - lengths 5-7 (also some 11 = UPC-A missing leading 0). Verified truncation on 3 yogurt-drink cases (58030->7290000058030 etc., resolved by name on the retailer). Spans nearly every shelf (cakes 24, bread 37, cheese 27, cookies 14, hummus 11, hard-cheese 11...). Consequence: (a) the barcode field is unreliable as a scrape/dedup key for ~1 in 5 products - blind re-scrapes false-negative; (b) product IDs derived from truncated barcodes (bsip1_*_72968) inherit it. The TASK-602 re-scrape RECOVERS true GTINs via name-resolution as it goes. OPEN DECISION (owner): also BACKFILL the served barcode fields with recovered true GTINs? That touches published JSON (identity only, not score/display) - owner-gated, movement note first. Root-cause the truncation source (scrape-time vs build-time) before backfill.
---

# TASK-607 — Served corpus barcode integrity: 146/710 products have a barcode too short to be a valid GTIN

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
