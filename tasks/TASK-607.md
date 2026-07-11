---
id: TASK-607
title: Served corpus barcode integrity: 146/710 products have a barcode too short to be a valid GTIN
owner: data-agent
status: BLOCKED
blocker: owner decision - backfill served barcode fields with recovered GTINs? (touches published JSON identity); + root-cause truncation source. Re-scrape recovers GTINs regardless.
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Found by TASK-602 fan-out (2026-07-11): the served bari-web/src/data/comparisons/*_frontend_v*.json 'barcode' field is too short to be a valid GTIN on 146/710 products (21%) - lengths 5-7 (also some 11 = UPC-A missing leading 0). Verified truncation on 3 yogurt-drink cases (58030->7290000058030 etc., resolved by name on the retailer). Spans nearly every shelf (cakes 24, bread 37, cheese 27, cookies 14, hummus 11, hard-cheese 11...). Consequence: (a) the barcode field is unreliable as a scrape/dedup key for ~1 in 5 products - blind re-scrapes false-negative; (b) product IDs derived from truncated barcodes (bsip1_*_72968) inherit it. The TASK-602 re-scrape RECOVERS true GTINs via name-resolution as it goes. OPEN DECISION (owner): also BACKFILL the served barcode fields with recovered true GTINs? That touches published JSON (identity only, not score/display) - owner-gated, movement note first. Root-cause the truncation source (scrape-time vs build-time) before backfill.
---

# TASK-607 — Served corpus barcode integrity: 146/710 products have a barcode too short to be a valid GTIN

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
