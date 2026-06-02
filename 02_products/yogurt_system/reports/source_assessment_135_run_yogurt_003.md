# TASK-135 subtask — Yogurt BSIP0 source assessment for run_yogurt_003

**Owner:** data-agent · **Date:** 2026-06-01 · **Parent:** TASK-135 (DEC-005 retirement)
**Scope:** Source assessment only — **no scraping implemented.** Determines the single best
authoritative source to acquire a real, ingredient-bearing yogurt corpus for `run_yogurt_003`.
**Verdict:** 🟢 **GO — Shufersal** (static HTTP + HTML parse, VPN-gated). Conditional on Israeli-IP VPN.

---

## 1. The requirement run_yogurt_003 must satisfy

TASK-135A's NO-GO was caused by a single measured gap, not a pipeline fault: **OFF Israeli yogurt
ingredient coverage = 0/50.** Yogurt BSIP2 scoring is ingredient-structure-driven (router, NOVA
proxy, fermentation/culture markers, additive/sweetener/stabilizer penalties, `bsip_yogurt_subtype`).
So the source for run_yogurt_003 must supply, on real Israeli SKUs:

1. **Ingredient panels** (Hebrew `רכיבים`) — the binding constraint
2. **Nutrition per-100g** (energy/protein/carbs/fat/fiber/sodium/sugar)
3. **Real barcodes** (gtin13) for identity/dedup
4. **Clean Hebrew product names** (`product_name_he`) — OFF left these empty on all 50

OFF supplies (3) and partial (2) but **fails (1) and (4)** — the two that matter most for this category.

## 2. Source comparison

Evidence base = the bread program's BSIP0 access audit (memory `bsip0-retailer-access-001`,
2026-05-25, **with VPN**) and the working `shufersal_probe.py` proven on `real_bread_retail_002_v2`
(110 products) and `real_bread_retail_003_v1` (258 scraped). Yogurt is the same retailer surface
(packaged dairy on the same site/templates), so the bread-proven path transfers directly.

| Source | Access (w/ VPN) | Method | Ingredients | Nutrition | Barcode (gtin13) | Hebrew names | Scrape feasibility | Maint. burden |
|---|---|---|---|---|---|---|---|---|
| **Shufersal** | **ACCESSIBLE** | Static HTTP + HTML parse | ✅ `רכיבים` tab | ✅ `.nutritionList` | ✅ JSON-LD | ✅ native | **Proven** (probe exists, reusable) | **Low** — no browser, no auth |
| Yohananof | Auth-walled | — | unknown | unknown | — | Untested/blocked | High |
| Victory | Blocked | Browser (Playwright) | unknown | unknown | — | Angular SPA — no cards render | High |
| Rami Levy | Unknown | — | unknown | unknown | — | 403 in v1; untested w/ VPN | Medium–High |
| Carrefour IL | Partial | Browser | behind login | behind login | — | Login wall blocks catalog | High |
| Wolt Market | Partial | Browser | behind auth | behind auth | — | Auth token required | High |
| OFF (135A baseline) | Open (no VPN) | API | ❌ **0% measured** | Partial | ✅ | ❌ empty | Trivial — but **useless for yogurt** | Low |

**Only Shufersal supplies all four required fields by a proven, low-maintenance method.** Every
other Israeli retailer is auth/SPA-blocked (the same wall documented for bread), and OFF is the
already-rejected ingredient-blind path that produced the 135A NO-GO.

## 3. Why Shufersal, concretely

The existing `03_operations/bsip0/acquisition_v2/shufersal_probe.py` already extracts exactly the
four required fields, server-rendered, no JS/browser:

- **Search** `/online/he/search?q=<query>&pageSize=48` → `<li data-product-name data-product-code data-food>`
- **Ingredients** — text after `רכיבים` in the product tab (Hebrew, native)
- **Nutrition** — `div.nutritionList > div.nutritionItem` value/unit/label triplets (mapped to 7 fields)
- **Barcode + image** — JSON-LD `@type=Product` → `gtin13`, `sku`, `image[]`
- **Hebrew name** — `data-product-name` / JSON-LD `name` (clean, unlike OFF's "Yoghort/Yugort")

Reuse cost is near-zero: clone the bread `acquisition_v3` structure and swap `SEARCH_QUERIES` to
yogurt terms + brand searches:
`יוגורט`, `יוגורט יווני`, `יוגורט ביו`, `אקטיביה`, `סקיר`, `תנובה`, `שטראוס`, `יופלה`, `דנונה`, `מולר`, `גד`
plus category browse — mirroring the mainstream-first + brand-search method that gave bread its coverage.
(Keep the **yogurt / מעדנים boundary** explicit at curation — drinkable lassi and dessert מעדנים are
out of scope, as 135A already excluded.)

## 4. Expected coverage (extrapolated from bread, same retailer/method)

- **Nutrition:** ~75% of fetched product pages render the table (bread 002_v2 = 83/110). A curated
  shelf focused on **mainstream high-traffic SKUs** (תנובה/שטראוס/יופלה/מולר/דנונה) lands higher,
  because those pages are the most complete.
- **Ingredients:** ~75% on 002_v2's curated set; degrades on a wide net (003 hit 46% INSUFFICIENT
  when scraping 258 SKUs broadly). For yogurt, **curate to the mainstream shelf** rather than
  maximizing breadth — this keeps ingredient coverage high, which is the field that decides the run.
- **Barcode:** ~100% (JSON-LD present on product pages).
- **Hebrew names:** ~100% native.
- **Realistic target for a ~30–50 SKU curated yogurt shelf:** clears the bread gate thresholds
  (nutrition ≥70%, ingredient ≥40%) comfortably; non-INSUFFICIENT majority — enough for the engine
  to populate router/NOVA/fermentation/additive signals and produce consumer explanations, which
  035A's OFF run could not.

## 5. Expected effort

| Item | Effort |
|---|---|
| Reuse `shufersal_probe.py` extraction core | None — works as-is |
| Swap to yogurt queries + brand/category searches | Low (config-level, ~1 file) |
| Curation/boundary script (yogurt vs מעדנים, dedup) | Low — adapt `02_curate_and_bsip1.py` |
| BSIP1 map + BSIP2 run (unchanged, engine 0.4.0) | None new — pipeline already exists |
| **Hard dependency: Israeli-IP VPN** | **Operational, not code** — without it the site blocks (403 / maintenance placeholder) |

Net: **low-to-moderate**, dominated by the VPN/operational requirement, not engineering. No new
framework, no auth-token harvesting, no browser automation.

## 6. Recommendation & GO/NO-GO

- **Recommended source: 🟢 Shufersal** — the single source that meets all four field requirements
  via a proven, low-maintenance, browser-free path. It is already the canonical BSIP0 source for the
  bread program.
- **run_yogurt_003 acquisition: 🟢 GO**, conditional on the one hard dependency below.
- **Single blocking dependency:** **Israeli-IP VPN must be available at scrape time.** With VPN →
  GO. Without VPN → all Israeli retailers (Shufersal included) block, and the only open source is
  the already-rejected ingredient-blind OFF → **NO-GO** (would reproduce the 135A wall).
- **Sources NOT to use:** OFF (ingredient-blind — the 135A NO-GO cause); Victory/Yohananof/
  Carrefour/Wolt/Rami Levy (auth-walled or SPA-blocked, high maintenance, unproven for ingredients).

**This unblocks the exact condition TASK-135 requires to close:** a real-product run with ingredient
panels + Hebrew names. Shufersal supplies both. TASK-135 stays BLOCKED until run_yogurt_003 executes
and reconciles; this assessment clears the source question and defines the GO path.

*data-agent · TASK-135 source assessment · 2026-06-01 · assessment only, no scrape implemented · engine 0.4.0 untouched*
