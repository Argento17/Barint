# BSIP0 Carrefour Israel — v0.2

> Frozen: 2026-05-16T13:57:56+00:00

## Overview

BSIP0 is the raw retailer-specific capture stage of the BSIP pipeline.
This document describes the Carrefour Israel retailer module.
No normalization, cross-retailer logic, or scoring is performed here.
BSIP0 captures retailer reality as-is and preserves provenance.

## Pipeline scripts

| Script | Purpose |
|--------|---------|
| `01_discover_carrefour.py` | Playwright shelf scrape → `candidate_review.csv` / `.xlsx` |
| `02_approve_carrefour_candidates.py` | Human-approved CSV → `approved_candidates.json` |
| `03_scrape_carrefour.py` | PDP scrape + shelf-card capture → per-product folders |
| `04_parse_audit_carrefour.py` | Raw data richness check (no normalization) |
| `04_parse_carrefour.py` | Regex parser → per-product `product.json` + `parse_summary` |
| `05_final_audit_carrefour.py` | This script — freeze artifacts |

## Discovery stats

- Total shelf rows discovered: **95**
- Decision YES: 23 | REVIEW: 60 | REJECT: 12
- Rows with barcode: 60/95
- Rows with product_url: 16/95

## Scrape stats

- `scraped_product_page`: **13**
- `captured_shelf_card_only`: **5**
- `failed`: 0

## Parse completeness

### product_page

| Field | Coverage |
|-------|----------|
| ingredients | 13/13 |
| allergens | 13/13 |
| nutrition table | 13/13 |
| package_size | 13/13 |
| country_of_origin | 13/13 |
| avg nutrition rows | 10.0 |

### shelf_card_only

| Field | Coverage |
|-------|----------|
| ingredients | 0/5 |
| allergens | 0/5 |
| nutrition table | 0/5 |
| package_size | 5/5 |

> Shelf-card-only rows have no product page HTML.
> Nutrition, ingredients, and allergens are empty by design — not errors.

## Per-product folder structure

```
outputs/carrefour/<barcode_or_slug>/
  discovery.json        # raw discovery record
  discovery.txt         # human-readable discovery summary
  capture_status.json   # scrape outcome flags
  raw_page.html         # full PDP HTML (product_page only)
  product_image.jpg     # downloaded product image
  product.json          # parsed BSIP0 output
```

## product.json schema

```json
{
  "schema_version": "bsip0_v0_2",
  "retailer_parser_version": "carrefour_v0_2",
  "parsed_at": "ISO-8601",
  "scrape_mode": "product_page | shelf_card_only",
  "product_identity": {
    "barcode": "string",
    "name": "string",
    "brand": "string",
    "product_name_raw": "string",
    "package_size": "string",
    "serving_size_raw": "string",
    "country_of_origin": "string",
    "product_url": "string"
  },
  "raw_observations": {
    "ingredients_raw_he": "string",
    "allergens_raw_he": "string",
    "may_contain_raw_he": "string",
    "price_raw": "string",
    "image_local": "string",
    "card_text": "string"
  },
  "nutrition_rows_raw": [{"nutrient_he": "...", "per_100g_raw": "...", "per_serving_raw": "..."}],
  "nutrition_per_100g": {"energy": "...", "fat_total": "...", ...},
  "parser_warnings": []
}
```

## HTML parsing anchors

| Section | Start anchor | End anchor |
|---------|-------------|------------|
| Ingredients | `רשימת רכיבים` | `אלרגנים כלולים` |
| Allergens | `אלרגנים כלולים` | `אלרגנים שעשויים להיות כלולים` |
| May-contain | `אלרגנים שעשויים להיות כלולים` | `מידע נוסף` |
| Nutrition | `סימון תזונתי` | `אין להסתמך` |
| Country | `ארץ ייצור <value>` | — |
| Product name | `<title>NAME \| קרפור Online</title>` | — |

## Known limitations

- Shelf-card-only rows: no nutrition or ingredient data.
  These products were found on the shelf but had no resolvable product URL.
- `serving_size_raw` is often empty (Carrefour PDP rarely shows per-serving info).
- Package size is extracted from product name / card text; occasionally imprecise.
- Discovery covers 3 shelf categories (95814, 96922, 95815).
  Other bar-product categories may exist and are not yet included.

## BSIP pipeline

| Stage | Purpose |
|-------|---------|
| BSIP0 | Raw retailer-specific capture. Preserves retailer reality and provenance. No normalization. |
| BSIP1 | Cross-retailer product consolidation and normalization. Creates canonical deployable food records by resolving product identity across retailers, normalizing nutrition into comparable units, detecting conflicts, and preserving traceability back to BSIP0 observations. Does NOT score, rank, or interpret. |
| BSIP2 | Scoring, intelligence, interpretation. Health scores, UPF/NOVA classification, recommendations. |

BSIP1 reads these `product.json` files as input observations.
Every BSIP1 normalized field must remain traceable to its BSIP0 source.
