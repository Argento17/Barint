---
name: bsip2-bread-retail-003
description: "Bread retail 003 — representative shelf correction; 258 scraped, 256 in-scope, 81 coherent, 13 reports; acquisition v3 with mainstream-first queries and brand searches"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Acquisition + pipeline run 2026-05-26 for bread_retail_003_v1 (Shufersal representative shelf).

**Why:** 002_v2 was wellness-skewed (64% wellness keywords, 0% standard white bread). 003 corrects this with mainstream-first queries, explicit brand searches (ברמן, וונדר, אנג'ל, דגנית), category browsing, and composition gating.

**How to apply:** Use bread_retail_003 results when comparing commodity vs. wellness bread. 002_v2 is still the canonical basis for the website/frontend (32 verified products).

## Files

| File | Location |
|:-----|:---------|
| Raw BSIP0 JSON | `C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json` |
| BSIP2 per-product JSONs | `C:\Bari\02_products\bread_retail_003\bsip2\` |
| Reports (13 total) | `C:\Bari\02_products\bread_retail_003\reports\` |
| Acquisition scripts | `C:\Bari\03_operations\bsip0\acquisition_v3\` |
| Pipeline batch runner | `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_bread_retail_003.py` |

## Acquisition v3 Results

- Total scraped: 258 unique product codes
- Phase 1 (search queries): 236 — mainstream-first: לחם, לחם לבן, לחם פרוס, לחם אחיד, פיתה, חלה, לחם קל, לחם מלא, בגט, לחם שחור, ברמן, וונדר, אנג'ל, דגנית, קרקר, שיפון, כוסמין
- Phase 2 (category browsing): +22 new from A1015, A1005, A1008, A1014
- Queries returning 0 results: טוסט, לאפה (those terms don't surface in Shufersal search)
- 0 failed product page fetches

## Composition Gate (PASS after fix)

- Total: 258 | Mainstream: 36% | Spelt: 7% | Sourdough-label: 12.4%
- Commodity anchors: 20 | Simple white: 16 | Pita/toast: 28
- Classifier bug fixed: "פיתה" (singular) → also matches "פיתות" (plural)

## Pipeline Results

- In-scope: 256 (2 excluded: sweet pastries)
- Pipeline errors: 0
- Coherent (CAUTIOUS + ingredients): 81/256 (vs 32/108 in 002_v2)
- Degradation: CAUTIOUS 31%, UNCERTAIN 22%, INSUFFICIENT 46%
- Score avg 54.0, median 56.4, range 40–82
- Grade A: 2, Grade B: 98, Grade C: 35, Grade D: 121

## Top Products (coherent)

1. לחם טחינה פרוס — score=82 grade=A, fiber=18.5g, מחמצת ✓
2. קרקר כוסמין מלא ושומשום — score=82 grade=A, fiber=10.0g
3. לחם ירוק מקמח מלא — score=80 grade=B, fiber=6.4g
4. קרקר כוסמין אורגני — score=78 grade=B, fiber=9.3g
5. לחם מחמצת קמח מלא — score=77 grade=B, fiber=6.7g

## Structural Findings (mass_market_anchors report)

| Segment | Count | Avg Score | Avg Fiber |
|:--------|:------|:----------|:----------|
| Commodity | 42 | 50.7 | 5.5g |
| Wellness | 89 | 60.0 | 6.6g |

- Score gap: 9.3 points — wellness scores higher, but most of the gap comes from INSUFFICIENT commodity products dragging average down
- Fiber gap: 1.1g/100g (small)
- Fermentation: commodity 4/42 (10%), wellness 37/89 (42%) — fermentation is primarily a wellness-segment phenomenon
- Fiber laundering: wellness 3/89, commodity 1/42 — present in both, slightly more in wellness

## Known Limitations

- Price/100g data: 100% unknown — weight extraction from product page names failed (product page names differ from search result names in format)
- Price tier analysis blocked until price data is fixed
- 46% INSUFFICIENT (same structural constraint as 002_v2 — Shufersal doesn't always show nutrition/ingredients on product pages)

## Key Observation vs 002_v2

Brand coverage confirmed: ברמן (11 products), וונדר/וונדרס (15+), אנג'ל (11+), דגנית (7). These were 0 in 002_v2.
Challah products dominated commodity segment — ברמן and וונדר appear heavily as challah/sweet bread variants, not plain sliced white bread. The plain sliced white bread from these brands (לחם אחיד, לחם פרוס) also appears.

[[bsip2-bread-retail-002-frontend]]
[[bsip2_real_bread_retail_001]]
