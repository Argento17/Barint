---
id: TASK-212
title: "Project Beaver — Playwright image re-scrape: Yohananof + Carrefour product pages for butter (21), granola/cereals (7)"
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-06-07
depends_on: [TASK-208]
blocks: []
roadmap_impact: false
cc_reviewed: 2026-06-09
close_reason: "Original scope (Playwright re-scrape) rendered moot — image coverage reached 100% via enrichment passes before execution. Assessment found 3 data-infra gaps (count mismatches, orphan hard_cheeses.json, missing barcodes) which were resolved by TASK-212B (now CLOSED). Both the original scope and the spawned normalization task are complete."
work_type: data-fix
project: beaver
---

# TASK-212 — Playwright Image Re-Scrape

## Context

TASK-208 exhausted all passive image recovery paths (BSIP0 raw outputs, OFF API) for the 28 products
with missing images across butter (21), granola (6), and cereals (1). Recovery failed because:

1. **Butter (21 products):** Yohananof + Carrefour scrapers used the price-transparency feed for
   identity + OFF for nutrition — they never visited product pages or captured storefront image URLs.
   The barcodes are Israeli retail-internal codes not registered in OFF.

2. **Granola + cereals (7 products):** Products exist in OFF but have no contributor-uploaded images.

The only remaining recovery path is an active Playwright scrape of the individual product pages on
Yohananof and Carrefour to extract their native storefront CDN image URLs.

## Scope

### Butter — 21 products

Extract the 21 product IDs and barcodes from `butter_frontend_v2.json`
where `imageUrl: null` AND `retailer != "shufersal"`. For each:

1. Identify the retailer (yohananof or carrefour)
2. Construct the product page URL from the barcode or name (need to find the URL pattern)
3. Launch Playwright → navigate to product page → extract image URL
4. Verify URL returns a real image (HEAD request, HTTP 200)
5. Update `imageUrl` in `butter_frontend_v2.json`

### Granola + cereals — 7 products

These came from the Shufersal cereals shelf but don't have images. For Shufersal products, the
CDN pattern is:
`https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/{STORE_CODE}_Z_P_{barcode}_1.png`

The `{STORE_CODE}` (e.g., `KAG24`, `UYK52`) varies by product and can't be inferred from the barcode.

## Acceptance criteria

- [ ] Product pages visited for all 21 butter products
- [ ] At least 10/21 butter images recovered (if product pages are accessible)
- [ ] Granola/cereals: attempt made via Shufersal CDN pattern or page visit
- [ ] All recovered URLs verified via HEAD request (HTTP 200)
- [ ] `butter_frontend_v2.json`, `granola_frontend_v1.json`, `cereals_frontend_v1.json` updated

## Return block (Data Agent + QA Agent, 2026-06-09)

**Proposed status:** RETURNED → CLOSED

### What was found

The original Playwright re-scrape scope (28 products: 21 butter + 7 granola/cereals) is **no longer needed**. Image coverage across all targeted categories is now **100%** — resolved between TASK-212 creation and present via image enrichment passes.

| Category | Products | Null Images (now) | Original Gap |
|----------|:--------:|:-----------------:|:------------:|
| Butter | 31 | **0** | 21 (was) |
| Granola | 42 | **0** | 6 (was) |
| Cereals | 34 | **0** | 1 (was) |
| Yogurts | 19 | **0** | 1 (was, out of scope) |

### Why this matters beyond images

Investigating TASK-212 revealed **3 launch-blocking data integrity gaps** that are more critical than the image re-scrape:

---

### Gap 1: 28 products silently missing from frontend arrays (HIGH severity)

**3 files have `_meta.product_count` mismatches with actual array length:**

| File | Meta Says | Array Has | Missing |
|------|:---------:|:---------:|:-------:|
| `bread_frontend_v2.json` | 24 | **19** | 5 |
| `cheese_frontend_v3.json` | 57 | **45** | 12 |
| `granola_frontend_v1.json` | 53 | **42** | 11 |

---

### Gap 2: Dangerous orphan duplicate `hard_cheeses.json` (HIGH severity)

Two files in the comparisons directory claim `v2` with identical product IDs but **completely different data**:

| Attribute | `hard_cheeses.json` (orphan) | `hard_cheeses_frontend_v2.json` (live) |
|-----------|:---------------------------:|:-------------------------------------:|
| Products | 30 (same IDs) | 30 (same IDs) |
| Images | **0/30 have images** | 30/30 have images |
| Grade dist. | 28× B, 1× C, 1× D | 9× B, 21× D |
| Page import | **Not imported** (page uses `_v2`) | Imported |

---

### Gap 3: 390/471 products (83%) lack barcode field (MEDIUM severity)

Only 3 of 14 live frontend files include a `barcode` field.

## Assessment

### TASK-212 (original scope): **ACCEPT as effectively complete**

The image gaps that prompted this task have been resolved. No Playwright re-scrape is needed.

### Broader data infrastructure: **RETURN — 3 gaps found requiring TASK-212B**

Resolved by TASK-212B (CLOSED 2026-06-09): count fixes, orphan archiving, barcode backfill, schema validator.
