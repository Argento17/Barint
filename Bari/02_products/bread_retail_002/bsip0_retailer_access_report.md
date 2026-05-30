# BSIP0 Retailer Access Audit

**Run:** `real_bread_retail_002` | **Date:** 2026-05-25 | **Timestamp:** 2026-05-25T15:56:01

This audit documents all retailer access attempts, HTTP probes, and the acceptance gate result.
It is produced before any BSIP1/BSIP2 pipeline execution.
No products are added to the corpus until the gate passes.

---

## 1. Gate Result

**Status: FAILED ✗**

Reason: zero_products — no real retailer bread/cracker products could be extracted

**Do NOT proceed to BSIP1/BSIP2 pipeline.**

The corpus does not meet minimum acceptance criteria.
Products collected: 0 (need 20)

---

## 2. Retailer Access Summary

| Retailer | HTTP Status | Blocker | Can Extract? |
|:---------|:-----------|:--------|:-------------|
| Shufersal | see probes | IN MAINTENANCE — HTTP 200 with maintenance placeholder | No |
| Rami Levy | see probes | BLOCKED — HTTP 403 Forbidden | No |
| Victory | see probes | BLOCKED (JS) — AngularJS SPA, headless browser required | No |
| Carrefour Israel | see probes | BLOCKED — HTTP 403 Forbidden | No |
| Tiv Taam | see probes | BLOCKED — HTTP 403 Forbidden | No |
| Wolt Market | see probes | PARTIAL — SSR accessible, product catalog requires auth/dynamic API | No |

---

## 3. Retailer-by-Retailer Findings

### Shufersal (שופרסל)

**Verdict:** IN MAINTENANCE — HTTP 200 with maintenance placeholder

**Technical detail:** All URLs return HTTP 200 with a 444-byte maintenance page (maintenance image from S3). Content is not accessible.

**Scrape method:** `impossible`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| home page | **200** (444B) | maintenance page |
| bread category | **200** (444B) | maintenance page |
| search: לחם | **200** (444B) | maintenance page |
| API v2 search | **200** (444B) | maintenance page |
| OCC API search | **200** (444B) | maintenance page |

### Rami Levy (רמי לוי)

**Verdict:** BLOCKED — HTTP 403 Forbidden

**Technical detail:** HTTP 403 on all endpoints including home page and API endpoints.

**Scrape method:** `impossible`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| home page | **403** (0B) | — |
| search: לחם | **403** (0B) | — |
| API catalog search | **403** (0B) | — |
| API category 10 | **403** (0B) | — |

### Victory (ויקטורי)

**Verdict:** BLOCKED (JS) — AngularJS SPA, headless browser required

**Technical detail:** HTTP 200 on all URLs, but all return identical 6716-byte AngularJS app shell (ng-version attribute visible in source). Content is not server-rendered. Requires headless browser.

**Scrape method:** `requires_headless_browser`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| home page | **200** (2044B) | usable content |
| search: לחם | **200** (2044B) | usable content |
| API products | **200** (2044B) | usable content |
| WP REST API | **200** (2044B) | usable content |

### Carrefour Israel (קרפור ישראל)

**Verdict:** BLOCKED — HTTP 403 Forbidden

**Technical detail:** HTTP 403 on all endpoints.

**Scrape method:** `impossible`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| home page | **403** (0B) | — |
| search: לחם | **403** (0B) | — |

### Tiv Taam (טיב טעם)

**Verdict:** BLOCKED — HTTP 403 Forbidden

**Technical detail:** HTTP 403 on all endpoints.

**Scrape method:** `impossible`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| home page | **403** (0B) | — |
| search: לחם | **403** (0B) | — |

### Wolt Market (וולט מרקט)

**Verdict:** PARTIAL — SSR accessible, product catalog requires auth/dynamic API

**Technical detail:** Consumer API front page accessible (698KB JSON, 20 sections, 307+ venue listings). Venue SSR page accessible (1.6MB HTML). React Query dehydrated state in page contains category structure (44 categories: מאפייה with subcategories לחם פרוס ושלם, קרקרים, etc.) but product items in SSR are only 24 promoted non-bread items. Category-specific product listings require dynamic API calls with authentication. restaurant-api.wolt.com menu endpoint returns 410 (deprecated). consumer-api.wolt.com venue endpoints return 404. No bread/cracker products extractable without auth token or headless browser.

**Scrape method:** `partial_ssr_only_non_bread`
**Products extracted:** 0

**HTTP Probes:**

| Probe | Status | Notes |
|:------|:-------|:------|
| Israel front (TLV) | **200** (82698B) | usable content |
| venue SSR page | **200** (273950B) | usable content |
| restaurant API v3 | **410** (0B) | — |
| consumer API v2 | **404** (0B) | — |

**Wolt-specific findings:**

- Front API accessible: True
- Venue SSR page accessible: True
- Products visible in SSR: 24 (promoted homepage items)
- Bread products in SSR: 0
- Bread category structure found: True
- Bread categories: מאפייה (menucategory-26), לחמים מהדליקטסן (menucategory-31), לחם פרוס ושלם (menucategory-32), פיתות, לחמניות וטורטיות (menucategory-33), חטיפים וקרקרים (menucategory-212), קרקרים (menucategory-218), פריכיות (menucategory-217)
- Grocery venues on Wolt: wolt-market-ben-yehuda, tiv-taam-ibn-gabirol, shufersal-drouyanov, carrefour-migdaley-david, victory-weizmann, spar-tel-aviv
- Dynamic API status: requires_auth

**Wolt conclusion:** Category structure is accessible via SSR embedded JSON.
Product listings for specific categories (bread, crackers) require dynamic API calls
that return 404/410 without authentication. The Wolt product catalog is not
extractable via HTTP scraping without a Wolt user auth token or headless browser.

---

## 4. Products Extracted

Total: 0

**No products extracted.** All retailers blocked or unable to provide product data.

---

## 5. Technical Blockers and Recommended Next Steps

### Blockers confirmed

| Retailer | Blocker | Evidence |
|:---------|:--------|:---------|
| Shufersal | Maintenance mode | All URLs → HTTP 200, 444-byte placeholder with S3 maintenance image |
| Rami Levy | HTTP 403 | Blocked on homepage, search, and API endpoints |
| Victory | AngularJS SPA | HTTP 200 but all URLs return identical 6716-byte JS shell |
| Carrefour Israel | HTTP 403 | Blocked on all endpoints |
| Tiv Taam | HTTP 403 | Blocked on all endpoints |
| Wolt Market | Dynamic API auth required | SSR accessible, but category product listings require auth |

### What would unlock scraping

1. **Shufersal**: Wait for maintenance to end, then retry. Their OCC API endpoint may work when online.
2. **Rami Levy**: Direct partnership/API credentials, or rate-limited retry with rotating proxies.
3. **Victory**: Headless browser (Playwright) — site uses AngularJS, server-renders nothing.
4. **Carrefour**: Direct API credentials or Wolt delivery integration (Carrefour is on Wolt with slug `carrefour-migdaley-david`).
5. **Tiv Taam**: Same as above — blocked; on Wolt as `tiv-taam-ibn-gabirol`.
6. **Wolt Market**: Auth token from Wolt account, or headless browser to navigate categories.

### OFF as enrichment (not primary corpus)

Open Food Facts may only be used as a nutritional enrichment layer once real retailer
products have been acquired. OFF MUST NOT serve as the primary product corpus.
The ~42 Israeli OFF products do not satisfy the 'real retailer provenance' requirement.

---

## 6. Honest Assessment

**This scrape failed the acceptance gate.**

The real Israeli retailer landscape as of 2026-05-25:
- All major supermarket chains actively block unauthenticated HTTP scraping
- JavaScript-rendered sites require headless browser infrastructure
- Wolt Market is the only semi-accessible source but requires auth for product menus
- Open Food Facts has ~42 Israeli bread products — insufficient for real retailer corpus

**Recommendation:** Build a headless-browser scraper (Playwright) targeting Wolt Market
and Victory. Alternatively, contact retailers directly for product data export.

*Generated by bsip0_scrape_audit.py — 2026-05-25T15:56:01*