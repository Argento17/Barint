# CHANGELOG — BSIP0 v0.2

> Frozen: 2026-05-16T13:57:56+00:00
> Retailer: Carrefour Israel
> Scope: bar-format snack products (cereal bars, energy bars, granola bars)

This is the first stable BSIP0 ingestion baseline.
It covers raw data capture only. No normalization, cross-retailer consolidation, or scoring.

---

## What is BSIP0

BSIP0 is the raw-capture stage of the BSIP food data pipeline.
Its contract: store raw retailer reality. Preserve provenance. Defer interpretation.

---

## Changes in v0.2 (Carrefour Israel)

### Discovery stabilization

- Scrapes 3 shelf category URLs: 95814 (חטיפי דגנים ואנרגיה), 96922 (חטיפי דגנים), 95815 (חטיפי אנרגיה)
- Produces 95 stable discovered rows across all runs
- Decision split: YES=23, REVIEW=60, REJECT=12
- Output: `candidate_review.csv` + `candidate_review.xlsx` (barcode as text)
- Barcode source tracked per row: `visible_text`, `gs1_image_url`, or `none`
- Promotional text stripped before deduplication (`_strip_promo`)
- Deduplication key: `name[:60]|price|pack_size` (not barcode — barcode is often absent at discovery time)

### click_resolve validation

- YES rows with no product_url receive a browser click to resolve the SPA overlay URL
- Pattern confirmed: all resolved URLs follow `?catalogProduct=XXXXXX` (AngularJS overlay, not a new page)
- Restricted to YES rows only — REVIEW rows are not resolved (prevents wasted runtime)
- 16/23 YES rows resolved to product URLs; 5 had no resolvable URL (shelf_card_only path)

### Dual scrape modes

- `03_scrape_carrefour.py` implements two explicit paths based on `product_url` presence:
  - `product_page`: navigate to PDP, scroll to bottom to trigger lazy-load, capture full HTML
  - `shelf_card_only`: download image from card, write discovery data, no browser navigation
- `scrape_mode` field written to `discovery.json` and `capture_status.json` on every product

### Shelf-card-only support

- 5 products had no resolvable product URL at scrape time
- These are captured with image + card text only
- Parser explicitly leaves nutrition, ingredients, allergens empty for these rows
- No data is invented; `parser_warnings` states the limitation clearly
- Folder naming: barcode if available, Hebrew name slug otherwise

### GS1 barcode protection

- `repair_barcode` in `02_approve_carrefour_candidates.py` applies a GS1-only guard when
  extracting barcodes from `image_url_raw`
- Guard: `/gs1-products/` must appear in the URL before the regex is applied
- Prevents 13-digit Unix timestamps in CDN resource URLs (`/retailers/.../resources/`) from
  being misidentified as barcodes
- Bug class: three Carrefour private-label products previously received the same fake barcode
  (`1710846947694`) and overwrote each other's folder on each scrape run

### XLSX barcode text safety

- All XLSX outputs (`candidate_review.xlsx`, `parse_summary.xlsx`, `final_audit_summary.xlsx`)
  write barcode column cells with:
  - `cell.value = str(barcode)` — never cast to int/float
  - `cell.number_format = "@"` — forces Excel to treat as text
- Prevents silent scientific notation rendering (e.g. `5.9E+12` instead of `5900020022325`)

### Structured nutrition parsing

- `04_parse_carrefour.py` extracts nutrition from a flat text block between two Hebrew anchors:
  `סימון תזונתי` → `אין להסתמך`
- 10 named nutrients extracted: energy, fat_total, fat_saturated, fat_trans, cholesterol,
  sodium, carbohydrates, sugars, dietary_fiber, protein
- Output: `nutrition_rows_raw` (list of {nutrient_he, per_100g_raw, per_serving_raw})
  and `nutrition_per_100g` (keyed dict of raw strings)
- Raw text preserved throughout — no numeric parsing in BSIP0
- 13/13 product_page products: full nutrition table parsed (avg 10.0 rows)

### Provenance preservation

- Every product folder contains:
  - `discovery.json`: full discovery record including card_text, image_alt, shelf_url,
    product_url, barcode_source, scrape_mode
  - `capture_status.json`: per-section capture outcome flags
  - `raw_page.html`: full PDP HTML at time of capture (product_page only)
  - `product_image.*`: downloaded product image
  - `product.json`: parsed BSIP0 output with parser_warnings

---

## Architecture review findings (documented, not yet acted on)

The following gaps were identified in the v0.2 architecture review and are
documented for BSIP0 v0.3 / bsip0_core work:

- `clean()`, `save_json()`, `now_iso()`, `normalize_image_url()`, `download_image()`
  are duplicated across all scripts in both retailers — should move to `bsip0_core/`
- Yohananof `repair_barcode` lacks the GS1 guard (same bug class as the Carrefour fix above)
- Yohananof `parser.py` normalizes nutrition to float immediately — violates BSIP0 raw-reality contract
- Yohananof `04_audit_bsip0.py` is empty — no audit tooling exists for Yohananof
- Schema version strings have drifted: `"bsip0.v1"` (Yohananof) vs `"bsip0_carrefour_v1"` (Carrefour)
- Yohananof discovery produces no XLSX; barcode scientific notation risk in CSV review

---

## Files in this freeze

| File | Description |
|------|-------------|
| `freeze_manifest.json` | Machine-readable freeze record with known_limitations |
| `final_audit_summary.json` | Pipeline counts and per-mode completeness |
| `final_audit_summary.xlsx` | Same, two-sheet XLSX |
| `parse_summary.json` | Per-product parse completeness (18 products) |
| `parse_summary.xlsx` | Same, XLSX with barcode as text |
| `parse_audit.json` | Raw data richness audit (no normalization) |
| `retailer_capabilities.yaml` | Machine-readable capability profile |
| `README_BSIP0_CARREFOUR.md` | Human-readable pipeline documentation |
| `CHANGELOG_BSIP0_v0_2.md` | This file |

---

## Pass conditions met at freeze

- `product_page` rows: nutrition 13/13, ingredients 13/13, allergens 13/13, package_size 13/13, country 13/13
- `shelf_card_only` rows: no false/invented data, explicit warnings in product.json
- 0 parser errors, 0 crashes
- No scientific notation barcodes in any XLSX output
- No fake barcodes from CDN resource URL timestamps
- All product.json files write `scrape_mode` field
- `run_report.json` failed=0

---

## Next milestone (v0.3 candidates)

- Extract `bsip0_core/` shared utilities
- Define canonical BSIP0 product.json schema contract
- Fix Yohananof `repair_barcode` GS1 guard
- Fix Yohananof parser: preserve `nutrition_rows_raw` (raw text)
- Implement Yohananof `05_audit` (parity with Carrefour)
- Unified `retailer_capabilities.yaml` for both retailers
