# TASK-255 Phase 0 — Scrape-Infrastructure Recon Report

> Written: 2026-06-12 | Scope: read-only repo evidence | Next: design continuous crawl + shelf expansion

---

## Per-Retailer Scraper Table

| Retailer | Dir (under `03_operations/bsip0/scrape/`) | Scrapes Listings? | Scrapes PDPs? | Product ID | Tech | VPN need | Login need | HTML persisted? |
|---|---|---|---|---|---|---|---|---|
| **Shufersal** | `shufersal/` | Yes (il_prices) | Yes | Barcode (URL `/A{barcode}`) | Playwright + crawlee | **Yes (IL IP)** | No | In-memory only (no disk) |
| **Shufersal** | `shufersal_yogurt/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD gtin13) | HTTP+BS4 | **Yes (IL IP)** | No | `nutrition_raw_source` in BSIP0 JSON |
| **Shufersal** | `shufersal_butter/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_cheese/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_cereals/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_maadanim/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_hummus/` | Yes (search) | Yes | Internal code → barcode | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_olive_oil/` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | Same |
| **Shufersal** | `shufersal_frozen_vegetables/` | Yes (search) | Yes | Barcode (URL pattern `/A{barcode}`) | HTTP+BS4 | **Yes (IL IP)** | No | **Full HTML**: `product_pages/`, `search_pages/`, `category_pages/` |
| **Victory** | `victory/` | Yes (search) | Yes (modal) | Barcode (CDN image URL) | Playwright | No | No | Per-product panel HTML (`outputs/`) |
| **Yohananof** | `yohananof/` | Yes (search) | Yes (modal) | Barcode (CDN image URL) | Playwright | No | No | Per-product panel HTML (`outputs/`) |
| **Yohananof** | `yohananof_milk/` | Yes (search) | Yes (modal) | Barcode (CDN image URL) | Playwright | No | No | Per-product panel HTML (`outputs/`) |
| **Yohananof** | `yohananof_hummus/` | Yes (search) | Yes (modal) | Barcode (CDN image URL) | Playwright | No | No | Per-product panel HTML |
| **Yohananof** | `yohananof_olive_oil/` | Yes (search) | No (discover only) | Barcode (CDN image URL) | Playwright | No | No | None |
| **Yohananof** | `yohananof_butter/` | No (il_prices) | Yes (OFF API) | Barcode | OFF API | No | No | None |
| **Yohananof** | `yohananof_cheese/` | No (il_prices) | Yes (OFF API) | Barcode | OFF API | No | No | None |
| **Yohananof** | `yohananof_yogurt/` | No (il_prices) | Yes (OFF API) | Barcode | OFF API | No | No | None |
| **Carrefour** | `carrefour_butter/` | Yes (search API) | Yes (OFF) | Barcode (search API / seed list) | HTTP API + OFF | No | **Yes (storefront)** | `nutrition_raw_source` placeholder only |
| **Carrefour+Yohananof** | `multiretailer_cereals/` | No (il_prices) | Yes (OFF API) | Barcode | OFF API | No | No | None |
| **Carrefour+Victory** | `multiretailer_olive_oil/` | Yes (API) | No (discovery) | Barcode (API response) | REST API | No | No | None |
| **Shufersal (v3 bread)** | `../acquisition_v3/shufersal_probe_v3.py` | Yes (search+cat) | Yes | Internal code → barcode (JSON-LD) | HTTP+BS4 | **Yes (IL IP)** | No | None |
| **Hazi Hinam** | `hazi_hinam/` | Exploratory only | — | — | Playwright | No | No | None |

---

## Q1 — Scrapers: What each does, product identity

**Shufersal** (the HTTP+BS4 family: yogurt, butter, cheese, cereals, maadanim, hummus, olive oil, frozen_veg):
- Entry: `01_scrape_*.py` / `01_discover_*.py`, all `main()` entry point.
- **Listing phase**: search queries + category browsing (HTTP GET to Shufersal search/category URLs). Extracts product code + barcode from data attributes and JSON-LD.
- **PDP phase**: individual product page via `/online/he/p/{code}` or `/online/he/A{barcode}`. Extracts nutrition (via shared `bsip0_nutrition` parser), ingredients, allergens.
- **Product ID**: **Internal Shufersal code** on listing pages (`data-product-code`), **barcode** (GTIN-13 from JSON-LD `gtin13`) on PDP. Both are available.

**Shufersal** (Playwright family: `01_acquire_shufersal.py`):
- Entry: `asyncio.run(main(category, limit))` with crawlee PlaywrightCrawler.
- Uses il_prices for identity (barcode + name), scrapes individual PDPs via browser.
- Product ID: **Barcode** from Shufersal URL pattern `/A{barcode}`.

**Victory** (Playwright):
- Entry: `acquire()` (sync Playwright).
- Searches by barcode or name, opens product modal, captures 3 tab panels.
- Product ID: **Barcode** from CDN image URL or fallback name-matching.

**Yohananof** (Playwright family: hummus, milk, olive_oil, generic):
- Two-phase: `01_discover_*` (search → extract barcode from CDN URLs → `candidates.csv`) → `02_scrape_*` or `03_scrape_*` (open each product → capture modal tabs).
- Product ID: **Barcode** from CDN image URL pattern `gs1-products/.../<EAN>-<ID>/`.

**Yohananof** (OFF+il_prices family: butter, cheese, yogurt):
- il_prices feed for barcode list → OFF API per barcode for nutrition/ingredients.
- Product ID: **Barcode** from il_prices.
- **Note**: These use OFF as data source, which violates the project-wide OFF ban. They are legacy/must-be-rewritten scrapers.

**Carrefour**:
- Uses Carrefour search API (JSON) for discovery + OFF per barcode for nutrition panels. Curated seed list fallback.
- Product ID: **Barcode** from search API or seed list.
- **Note**: Also uses OFF for nutrition; needs rework for the OFF ban.

**Key evidence files:**
- `03_operations/bsip0/scrape/shufersal_yogurt/01_scrape_yogurt.py` — Shufersal yogurt scraper, HTTP+BS4.
- `03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py` — Shufersal crawlee Playwright scraper.
- `03_operations/bsip0/scrape/yohananof_yogurt/01_acquire_yohananof_yogurt.py` — Yohananof yogurt via il_prices+OFF.
- `03_operations/bsip0/scrape/carrefour_butter/01_scrape_carrefour_butter.py` — Carrefour hybrid API+OFF.

---

## Q2 — Session/access requirements

### Shufersal
- **Israeli-IP VPN is mandatory**. Without it, Shufersal returns either HTTP 403 or a fake HTTP 200 with maintenance-placeholder image (TLS fingerprint blocking via JA3/JA4).
- Unlocked 2026-06-07 via crawlee's `DefaultFingerprintGenerator` (browserforge) which injects realistic Chrome TLS/navigator fingerprints. Raw Playwright without it is still blocked.
- Cookie popup is auto-dismissed via `close_cookie_popup()` in the Playwright scraper. The HTTP+BS4 scrapers don't face cookie walls because they use direct page URLs.
- **No login credentials needed**.
- Documented in: `integrations/source_registry.py:134-152`, `03_operations/bsip0/README.md:24`.

### Yohananof
- **No VPN needed**. Storefront is accessible from non-IL IPs.
- **No login needed** (Angular SPA is publicly accessible).
- Cookie popup must be dismissed. Every Yohananof Playwright scraper has `close_cookie_popup(page)` function.
- Some scrapers run `headless=False` (for debugging); can run `headless=True` for production.
- Documented in: `integrations/source_registry.py:169-175`.

### Victory
- **No VPN needed**. Same SaaS backend as Yohananof.
- **No login needed**. Cookie popup dismissed via `dismiss_all_popups()`.
- Playwright required (Angular SPA returns 6716B JS shell).
- Documented in: `integrations/source_registry.py:177-183`.

### Carrefour
- Storefront is **login-gated** (F5 BIG-IP WAF + auth wall). Requires manual session cookie import.
- `acquisition_v2/carrefour_probe.py` detects login walls and sets `requires_manual_action=True` with instructions to export cookies from a manual browser login.
- The `carrefour_butter/` scraper bypasses the storefront by using the Carrefour search API (JSON endpoint) + OFF for panels. The search API may still be accessible.
- Documented in: `integrations/source_registry.py:185-204`.

### Rami Levy, Tiv Taam, Machsaney Hashuk
- All HTTP 403 blocked (Cloudflare/F5 WAF). **Not available** for scraping without residential proxies + stealth browser.
- Documented in: `integrations/source_registry.py:206-268`.

### Manual steps documented in:
- `03_operations/bsip0/acquisition_v2/README.md:64-71` — cookie export/import procedure.
- `03_operations/bsip0/acquisition_v2/retailer_base.py:117-118` — `requires_manual_action` data model.
- `03_operations/bsip0/scrape/retailer_capabilities/carrefour.yaml` — capabilities YAML.
- `03_operations/bsip0/scrape/retailer_capabilities/rami_levy.yaml` — DEFERRED status.

### Env/secrets:
- Only scraper-adjacent env var: `AZURE_DI_KEY` (OCR pipeline, `C:\Bari\.env`).
- No retailer credentials stored anywhere.

---

## Q3 — Raw page persistence (what can be hashed today)

### What is persisted (usable for content hashing):

| Form | Where | Scrapers | Use for hashing? |
|---|---|---|---|
| **`nutrition_raw_source`** (JSON rows + outer HTML) | Inside every BSIP0 JSON record (`02_products/*/bsip0_outputs/*.json`) | All 9 Shufersal HTTP+BS4 scrapers | **Partial** — only nutrition table HTML, not full page |
| **Full product HTML** (222 files) | `scrape/shufersal_frozen_vegetables/product_pages/*.html` | Frozen vegetables only | **Yes** — full page for hash |
| **Search HTML** (53 files) | `scrape/shufersal_frozen_vegetables/search_pages/*.html` | Frozen vegetables only | **Yes** — listing pages for hash |
| **Category HTML** (9 files) | `scrape/shufersal_frozen_vegetables/category_pages/*.html` | Frozen vegetables only | **Yes** — listing pages for hash |
| **Per-product panel HTML** (ingredients/nutrition/allergens.html) | `scrape/{yohananof,victory}/outputs/*/` | Yohananof (3 scrapers), Victory | **Yes** — but panel fragment only, not full page |
| **Crawlee session caches** (`.baf`) | `acquisition_v2/sessions/*/Default/Cache/` | acquisition_v2 probes | **Fragile** — internal browser cache, not designed for hashing |

### Key gap:
The **yogurt scraper** (`shufersal_yogurt/01_scrape_yogurt.py`) does **not** persist any raw HTML to disk. It parses nutrition/ingredients in-memory and writes only the structured BSIP0 JSON (with embedded `nutrition_raw_source`). To hash, we would either:
- (a) Add `page_html_path` or `raw_response_path` to the scraper output — store full HTML to disk before parsing.
- (b) Hash the `nutrition_raw_source.html` substring — but this only covers the nutrition table, not ingredient list, product name, images, etc.

### EV-029 / TASK-151:
Added `nutrition_raw_source` persistence (`bsip0_nutrition.py:195-208`). This embeds `{"rows": [...], "html": "<div class='nutritionList'>..."}` into each BSIP0 record so parser fixes can be replayed offline. It is **not** full-page persistence.

**Evidence**: `tasks/closed/TASK-151.md`, `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`, `memory-archive/bsip0_fat_overwrite_ev029.md`.

---

## Q4 — Listing sweep feasibility for yogurts

### Can the existing yogurt scraper enumerate a category listing?

**Shufersal yogurt scraper** (`shufersal_yogurt/01_scrape_yogurt.py`):
- **Yes** — it searches for yogurt keywords (`יוגורט`, `יוגורט יווני`, `יוגורט ביו`, `אקטיביה`, etc.) and browses category URLs on Shufersal.
- On listing pages, it extracts `data-product-code` (internal code) and from PDP JSON-LD it gets `gtin13` (barcode).
- Currently, it does BOTH listing + PDP in one pass. A listing-only sweep could be extracted.

**Yohananof yogurt scraper** (`yohananof_yogurt/01_acquire_yohananof_yogurt.py`):
- **No** — this scraper uses il_prices + OFF. It does NOT scrape Yohananof storefront at all. Cannot enumerate a live shelf.
- For Yohananof yogurt, a new storefront scraper (Playwright, following the pattern of `yohananof_milk/` or `yohananof_hummus/`) would be needed.

### What corpus file would we diff against?

The authoritative corpus for known yogurt products:

| File | Products | Source |
|---|---|---|
| `bari-web/src/data/comparisons/yogurts_frontend_v4.json` | **88 products** (live, current) | Generated from `run_yogurt_006_recal_p0_trim` |
| `02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json` | Raw scrape output (most recent) | Shufersal scrape 2026-06-11 |
| `02_products/yogurt_system/bsip0_outputs/yohananof_yogurt_bsip0_raw_20260607T060832.json` | Raw Yohananof (OFF) output | Yohananof via OFF 2026-06-07 |
| `03_operations/bsip1/run_yogurt_006/output/*.json` | Per-product BSIP1 records | Latest BSIP1 run |

**Recommended diff target**: `yogurts_frontend_v4.json` — 88 products with barcodes. New products from a listing sweep would be compared against this set.

**No standalone `shelf_map.json` exists for yogurt** — shelf configuration is embedded in `bari-web/src/lib/comparisons/yogurts-shelf-filters.ts` (frontend lens definitions) and the `category_config.json` at `02_products/yogurt_system/category_config.json`.

### Other categories with shelf_map.json (for reference):
- `02_products/juices/shelf_map.json`
- `02_products/hard_cheeses/bsip0_outputs/shelf_map.json`
- `02_products/cheese_spreads/factory_run_001/shelf_map.json`
- `02_products/breakfast_cereals/factory_run_002/shelf_map.json`

---

## Q5 — Cadence constraints: rate limiting, anti-bot, incidents

### Rate limiting implementations (in scraper code)

| File | Mechanism |
|---|---|
| `integrations/clients/http.py:53-54` | Shared HTTP client: exponential backoff on 429/5xx (backoff=1.5) |
| `03_operations/bsip2/proto_v0/src/scrape_bread_retail.py:178-180` | Exponential backoff on Shufersal: wait = 3*(2^attempt), 4 retries |
| `03_operations/bsip2/proto_v0/src/scrape_bread_retail.py:529-556` | **2-second delay** between category pages, between categories, between keyword pages, between keywords |
| `03_operations/bsip2/proto_v0/src/bsip0_scrape_audit.py:270` | **2.5-second delay** between retailer probes |

**Assessment**: The Shufersal HTTP+BS4 scrapers (yogurt, butter, etc.) do **NOT** have explicit delay/rate-limiting. Only the bread scrapers in `bsip2/proto_v0/src/` have deliberate pacing. This is a risk for aggressive listing sweeps.

### Anti-bot blockers per retailer (from `integrations/source_registry.py`):

| Retailer | Block type | Status | Workaround |
|---|---|---|---|
| **Shufersal** | TLS fingerprint (JA3/JA4) → fake 200 | **UNLOCKED** (crawlee 1.7 + DefaultFingerprintGenerator) | → Needs crawlee; raw Playwright still blocked |
| **Carrefour** | F5 BIG-IP WAF → 403 | **BLOCKED** | → Residential proxy + stealth Playwright |
| **Rami Levy** | Cloudflare Bot Mgmt → 403 | **BLOCKED** | → Residential proxy + stealth Playwright |
| **Tiv Taam** | F5 BIG-IP WAF → 403 | **BLOCKED** | → Residential proxy + stealth Playwright |
| **Machsaney Hashuk** | F5 BIG-IP WAF → 403 | **BLOCKED** | → Residential proxy + stealth Playwright |

### Incident history

| Incident | Task | Date | Summary |
|---|---|---|---|
| Shufersal maintenance block | `source_registry.py:134-152` | 2026-06-07 | TLS fingerprinting (JA3/JA4) returned fake maintenance page; unlocked via crawlee |
| Data fabrication (hard cheese) | `TASK-215.md` | 2026-06-07 | Agent synthesized BSIP0 JSON claiming source; round-hour timestamps gave it away |
| OFF 503 overload | `reports/reconciliation_135a_findings.md:18` | 2026-06-01 | OFF faceted search endpoints overloaded during yogurt run |
| Recal-went-live | `TASK-173.md:14` | ~2026-06-04 | Blind re-run shipped recal without proper engine pinning |
| Fabricated source claim live | `TASK-254.md` | 2026-06-12 | Copy claiming "official food source" with no trace evidence → Leap 6 machine gates |

### Other rate-limit notes (non-scraper):
- Semantic Scholar: 429 on clean single request (free tier) — `integrations/README.md:81`
- Google Trends: 429-prone on related-queries — `integrations/README.md:69`
- PageSpeed: 429 without API key — `integrations/README.md:77`
- gov.il: SSL-blocked from build sandbox — `integrations/clients/tzameret.py:15`

---

## ⚠️ Single Biggest Blocker for Scheduled (Unattended) Runs

**Israeli-IP VPN dependency for Shufersal.**

Shufersal is the only retailer with a working, direct-storefront scraper for yogurt (`shufersal_yogurt/01_scrape_yogurt.py`). It requires an Israeli IP — without one, Shufersal returns HTTP 403 or a fake TLS-fingerprint maintenance page. There is no VPN automation, no VPN health-check, no retry-with-VPN logic in any script. Every Shufersal scrape today is an ad-hoc manual step: "VPN must be on, then run."

For a scheduled crawler to be unattended, either:
- **(a)** VPN connection/disconnection must be automated (scripted OpenVPN/WireGuard with health-check loop + retry), or
- **(b)** The scraper must work without VPN, which requires a residential proxy service or similar — currently not implemented or budgeted.

All other constraints (rate limiting, missing raw-HTML persistence, cookie handling) are solvable in code. The VPN dependency is an **operational/infrastructure** blocker that no code change can work around without either automation or proxy budget.

**Evidence chain**: `tasks/TASK-255.md:21,60-61` → `02_products/yogurt_system/reports/source_assessment_135_run_yogurt_003.md:6,86,97-99` → `01_framework/operations/comparison_chain_gap_analysis_v1.md:93-94` → `integrations/source_registry.py:134-152`.
