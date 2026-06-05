---
name: bsip2-bread-retail-002-frontend
description: "Frontend dataset sprint — canonical JSON for bread_retail_002_v2; 108 products, 32 verified, 4 comparisons, 3 output files"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Frontend dataset built 2026-05-25 for bread_retail_002_v2 (Shufersal).

**Why:** Pre-Cursor handoff. One canonical JSON replaces direct report parsing. Cursor builds homepage, product cards, comparison pages, and blog visuals from this single file.

**How to apply:** All bread project UI work starts from `real_bread_retail_002_v2_frontend_dataset.json`. Do not read raw BSIP2 reports for UI data. Schema and examples docs explain every field.

## Files

| File | Location |
|:-----|:---------|
| Frontend dataset (JSON) | `C:\Bari\02_products\bread_retail_002\real_bread_retail_002_v2_frontend_dataset.json` |
| Schema doc | `C:\Bari\02_products\bread_retail_002\frontend_dataset_schema.md` |
| Examples doc | `C:\Bari\02_products\bread_retail_002\frontend_dataset_examples.md` |
| Builder script | `C:\Bari\03_operations\bsip2\proto_v0\src\build_frontend_dataset.py` |

## Dataset Numbers

- Total products: 108 (in-scope)
- Displayable: 32 (CAUTIOUS + ingredient text)
- Featured: 15 (top-scored displayable)
- Comparisons: 4 pre-built pairs
- Fermentation genuine: 7 (among displayable)
- Fermentation mismatch: 13 (name claims מחמצת, yeast is primary leavener)
- Fiber laundering: 4 products
- Seed halo: 14 products
- Avg fiber (verified): 6.2g/100g

## Key Design Decisions

1. **score=null for non-displayable products** — INSUFFICIENT products have `score: null` and `grade: null` so Cursor cannot accidentally display them.
2. **Fermentation signal logic** (nuanced) — ALL real Israeli sourdough breads also contain "שמרים" (yeast). Signal_fermentation_real = TRUE when מחמצת/שאור is in ingredients AND name doesn't claim "מחמצת" with שמרים as primary leavener. Mismatch = name claims מחמצת AND שמרים is in ingredient text.
3. **Ingredients merged from raw BSIP0 JSON** — BSIP2 per-product JSONs don't store ingredient text. Builder loads `real_bread_retail_002_v2_20260525T165557_bsip0_raw.json` and matches by barcode.
4. **confidence_level** three values: `verified` (CAUTIOUS/FULL + ingredients), `partial`, `insufficient`.

## 4 Comparison Pairs

- `comp_fermentation_rye` — genuine fermentation rye vs industrial yeast rye
- `comp_fermentation_claim` — product with genuine מחמצת (no name claim) vs product with name "מחמצת" + industrial yeast
- `comp_fiber_extremes` — highest vs lowest fiber (verified only)
- `comp_spelt_crackers` — top two spelt crackers by score

## Top 3 Verified Products

1. קרקר כוסמין מלא ושומשום — score=82, grade=A, fiber=10.0g
2. קרקר כוסמין אורגני — score=78, grade=B, fiber=9.3g
3. לחם שיפון קל — score=75, grade=B, fiber=12.4g (genuine fermentation)

[[bsip0-retailer-access-001]]
