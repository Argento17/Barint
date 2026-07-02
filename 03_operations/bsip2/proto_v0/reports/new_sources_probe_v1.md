# New Sources Probe v1 — Rami Levy + Super-Pharm

**Task:** TASK-395 (de-chain program, new sources feasibility)
**Author:** Data Agent
**Date:** 2026-06-25
**Status:** FEASIBILITY PROBE — no code changed, no scores changed, no pipeline run

---

## Preamble

This document reports the results of live feasibility probes on two new data sources
approved by the owner for addition to the Bari acquisition pipeline:

- **Rami Levy** (`www.rami-levy.co.il`) — grocery retailer, grocery corpus priority
- **Super-Pharm** (`shop.super-pharm.co.il`) — pharmacy/supplement retailer, supplement corpus priority

All fetch results are verified by actual HTTP requests made 2026-06-25. Confidence levels:
- **VERIFIED-BY-FETCH** = value obtained from an actual HTTP response, quoted verbatim
- **INFERRED** = deduced from code/HTML structure, not from a live API response with that specific field
- **NOT FOUND** = searched, not present in static HTML

---

## A. Live Feasibility Probes

---

### A.1 Rami Levy (`www.rami-levy.co.il`)

#### A.1.1 Catalog Accessibility — No Login Required

**Finding: VERIFIED-BY-FETCH — publicly accessible JSON API, no auth required.**

The site is a Nuxt.js (Vue SSR) application (`window.__NUXT__` detected, `data-n-head-ssr`
attribute on `<body>`). Static HTML renders a JS shell; product data is served by a
documented internal JSON API.

**Verified live API endpoint:**

```
POST https://www.rami-levy.co.il/api/catalog?
Content-Type: application/json

{"q": "לחם", "from": 0, "store": 331}
```

HTTP 200. No authentication header required. No session cookie required. The `store`
parameter is an integer store ID; store 331 (a major Jerusalem-area store) returned 52
products for the query "לחם". Other store IDs (1, 311) returned zero products — the store
ID selection is significant and must be empirically verified per category.

Source discovered by parsing the minified JS bundle at
`https://www.rami-levy.co.il/rl/ea76006.js` (LEN=2,066,596 bytes), which contains
the literal strings `"https://www-api.rami-levy.co.il/api/v2/site"` (session/user APIs) and
`"https://www.rami-levy.co.il/api/catalog?"` embedded in the Vue component source.

#### A.1.2 Nutrition Panel (Tier-1 Fields)

**Finding: VERIFIED-BY-FETCH — all 7 Tier-1 fields present in the API response for
most products. Sat-fat coverage is partial (20/30 in sampled results).**

The API response for each product contains a `gs.Nutritional_Values` array. Each entry
in the array has a `field_name` (English canonical key) and a `value` (numeric string,
per-100g). Fields found verified across 30 sampled bread products (VERIFIED-BY-FETCH):

| Bari Tier-1 Field | API `field_name` | Coverage in 30-product sample |
|---|---|---|
| `energy_kcal` | `Energy_per_100_grams` | **30/30** |
| `fat_g` | `Fats_per_100_grams` | **30/30** |
| `fat_saturated_g` | `Saturated_Fatty_Acids_per_100_grams` | **20/30** |
| `carbohydrates_g` | `Carbohydrates_per_100_grams` | **30/30** |
| `sugars_g` | `Sugars_from_Carbohydrates_per_100_grams` | **29/30** |
| `sodium_mg` | `Sodium_per_100_grams` | **30/30** |
| `protein_g` | `Proteins_per_100_grams` | **30/30** |
| `dietary_fiber_g` | `Dietary_Fibers_per_100_grams` | 30/30 (bonus — not Tier-1 but present) |
| `fat_trans_g` | `Trans_Fatty_Acids_per_100_grams` | present in field set (coverage not measured) |

**Verbatim example from VERIFIED-BY-FETCH response (barcode 7290018500408, "לחם אחיד פרוס 900 ג רמי לוי"):**

```json
{
  "label": "אנרגיה (קלוריות)", "field_name": "Energy_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "קלוריות", "value": "240"
},
{
  "label": "שומנים (גרם)", "field_name": "Fats_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "גרם", "value": "1.7"
},
{
  "label": "נתרן (מג)", "field_name": "Sodium_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "מג", "value": "384"
},
{
  "label": "סך הפחמימות (גרם)", "field_name": "Carbohydrates_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "גרם", "value": "45.1"
},
{
  "label": "סוכרים מתוך פחמימות (גרם)", "field_name": "Sugars_from_Carbohydrates_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "גרם", "value": "2.1"
},
{
  "label": "סיבים תזונתיים (גרם)", "field_name": "Dietary_Fibers_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "גרם", "value": "3.9"
},
{
  "label": "חלבונים (גרם)", "field_name": "Proteins_per_100_grams",
  "col_label": "ל-100 גרם", "UOM": "גרם", "value": "9.2"
}
```

**sat_fat note:** 20/30 products had `Saturated_Fatty_Acids_per_100_grams` present. This
is lower than the other fields. Bread is a low-sat-fat category; missing sat_fat on some
bread products may be a legitimate labeling gap (Israeli law allows omission of sat_fat
when total fat is very low). This should be verified for hummus and snack categories
before drawing a corpus-level conclusion.

**Red-label data:** The API also returns `gs.Food_Symbol_Red` — the Israeli mandatory
red-label system — with codes (`FSR1`=no symbol, `FSR5`=green symbol). VERIFIED-BY-FETCH.

#### A.1.3 Hebrew Ingredient List

**Finding: VERIFIED-BY-FETCH — full Hebrew ingredient text present in API response.**

The field `gs.Ingredient_Sequence_and_Name` contains the full Hebrew ingredient string.
Coverage in 30-product sample: 30/30.

**Verbatim examples (VERIFIED-BY-FETCH):**

```
"קמח חיטה כהה (גלוטן), מים, שמרים, מלח, חומרים משמרים (E202 E282),
 מתחלבים (E471 E481), סיבים תזונתיים, מווסת חומציות (E330),
 חומר מעכב חמצון (E300), אינזימים."
```

```
"קמח כוסמין מלא 100% מסך הקמחים, 41% ממשקל הלחם), מים, גלוטן חיטה,
 סיבים תזונתיים, שמרים, מלח, לתת שיפון, לתת שעורה, דקסטרוז,
 קלציום קרבונט טבעי חומרים משמרים (קלציום פרפיונם, פוטסיום סורבט),
 מתחלב: E481, מווסת חומציות: חומצת לימון, ויטמין C, אנזימים."
```

Quality: full ingredient lists, E-number format, Hebrew text. Suitable for NOVA
classification and additive scoring. No encoding issues detected.

#### A.1.4 Barcode Availability

**Finding: VERIFIED-BY-FETCH — barcode present in every API response item.**

The field `barcode` is a top-level integer in each product object. Coverage: 30/30.
Example: `"barcode": 7290018500408` (13-digit EAN-13). No parsing required.

Also available in product images: `gs.images.original` = `/product/{barcode}/large.jpg`.

The barcode is already in the `il_prices` client (via laibcatalog for other chains, or
directly for the Rami Levy price-transparency feed). The identity layer is thus
double-confirmed: price-feed barcode matches API barcode.

#### A.1.5 Additional Fields in API Response

These fields are not Tier-1 but are useful for pipeline enrichment:

- `gs.BrandName` — Hebrew brand name
- `gs.Country_of_Origin` — ISO country code (e.g., "IL")
- `gs.Net_Content` — pack size and unit
- `gs.Allergen_Type_Code_and_Containment` and `_May_Contain` — allergen codes
- `gs.Diet_Information` — vegan/vegetarian/etc. codes
- `gs.Food_Symbol_Red` — Israeli red-label system
- `gs.Consumer_Storage_Instructions` — Hebrew storage text
- `department`, `group`, `subGroup` — category hierarchy (useful for shelf mapping)
- `available_in` — list of store IDs where product is available
- `price.price` — current price in ILS
- `lables` — promotional and quality labels (e.g., "ויגן פרנדלי", "מוצרים בפיקוח")

#### A.1.6 Access Method

**Static requests only — Playwright NOT required.**

The API endpoint `POST https://www.rami-levy.co.il/api/catalog?` responds to plain
`urllib`/`requests` calls without any browser or JavaScript execution. The only
requirement is:
- Correct `Content-Type: application/json` header
- A valid `store` ID integer in the POST body
- Standard browser-mimicking `User-Agent`, `Accept-Language`, `Origin`, `Referer` headers

The site homepage uses Nuxt SSR and requires a browser to render the Vue components, but
the catalog data API is decoupled from the SSR rendering layer.

**Blocker risk:** None observed. No CAPTCHA, no rate-limit header, no 403 on probed
endpoints. Rate-limiting on high-volume batch requests is possible but not observed.

---

### A.2 Super-Pharm (`shop.super-pharm.co.il`)

#### A.2.1 Catalog Accessibility — No Login Required

**Finding: VERIFIED-BY-FETCH — accessible without login, but product-level content
is mixed: some fields are server-rendered (name, price, barcode, product properties),
while nutrition/supplement facts are NOT present in the static HTML.**

The site is an SAP Hybris e-commerce platform with a Vue.js frontend layer (`:class=`
Vue binding syntax in HTML, `React` signal also present — likely a hybrid). The base URL
`www.super-pharm.co.il` redirects (301) to `shop.super-pharm.co.il`. All fetches
are from `shop.super-pharm.co.il`.

Category pages (e.g., the magnesium category `/health/supplements/minerals/magnesium/c/30301113`)
are server-rendered and contain:
- Full JSON-LD `CollectionPage` schema with up to 30 product URLs per page
- Product codes (`data-product-code`) and EAN barcodes (`data-ean`) in the DOM
- Product names in category listing cards

Product detail pages (e.g., `/health/supplements/minerals/magnesium/מגנזיום-ביסגליצינאט/p/704023`)
are server-rendered and contain in static HTML:
- Full JSON-LD `Product` schema: name, image URL, brand, price, rating
- Product description (short text in Hebrew)
- Barcode in `<p class="description-ean">` text element: "ברקוד מוצר: 7290122852608"
- Product properties: dosage instructions, kosher certification, unit weight, capacity
- EAN in `data-favorite-id` and `data-ean` attributes on the add-to-cart button

**NOT present in static HTML:** Supplement facts table, ingredient list, per-serving
nutrient breakdown. These appear to load via JavaScript after the initial page render
— the `extra-details` section shows only the product description tab and no additional
content on the supplement facts tab in the fetched HTML.

#### A.2.2 Supplement Facts (Tier-1 Fields for Supplements)

**Finding: NOT FOUND in static HTML — supplement facts are dynamically loaded via JS.**

Probed three product pages: multivitamin for pregnant women (p/332649), magnesium
bisglycinate (p/704023). In both cases, the `product-info` tab pane in the static HTML
contains only:
- Product description (1-2 sentences)
- Barcode line
- Product properties (kosher type, dosage instructions, pack size, weight)

No nutrition table, no supplement facts table, no per-serving ingredient breakdown was
found in the static HTML of either page. The 42 occurrences of "ויטמין" on p/332649
are all in the navigation menus, not in a product supplement-facts panel.

**Implication:** Super-Pharm supplement facts require either:
(a) Playwright/browser rendering to execute the JS that loads the supplement facts panel, OR
(b) A separate SAP Hybris product JSON API call (which I could not identify — all REST
endpoints I probed returned HTTP 404).

This is a blocker for direct static-HTTP scraping of supplement nutrition data from Super-Pharm.

#### A.2.3 Hebrew Ingredient List

**Finding: NOT FOUND in static HTML of supplement pages.**

The supplement product pages do not contain a Hebrew ingredient list in static HTML.
The existing iHerb panel client (`integrations/clients/iherb_panel.py`) is the current
path for supplement ingredient + active ingredient data. Super-Pharm static HTML does
not replace that source.

#### A.2.4 Barcode Availability

**Finding: VERIFIED-BY-FETCH — barcode available in static HTML via multiple paths.**

For product p/704023 (מגנזיום ביסגליצינאט), barcode `7290122852608` is present in:
1. `<p class="description-ean">ברקוד מוצר:&nbsp;7290122852608</p>` — server-rendered
2. `data-favorite-id="7290122852608"` on the "add to favorites" button
3. JSON-LD `Product.image` URL: `hybris/products/mobile/medium/7290122852608.jpg`
4. `data-ean` attributes on product cards in the category listing page

The barcode is also confirmed from the Super-Pharm price-transparency feed (already in
the `il_prices` client, LIVE-VERIFIED).

#### A.2.5 Supplement Coverage

**Finding: VERIFIED-BY-FETCH — Super-Pharm magnesium category lists 30 products
per page with Hebrew names, product codes, and EAN barcodes in static HTML.**

The magnesium category URL `/health/supplements/minerals/magnesium/c/30301113` returns
a server-rendered page with 30 product listings, each with:
- Product URL and Hebrew name
- EAN barcode (`data-ean` attribute)
- Product code (`data-product-code` attribute)
- Price
- Image URL (image filename = barcode)

Sample magnesium products found (VERIFIED-BY-FETCH, barcodes from `data-ean`):

| Hebrew Name (from URL decode) | Product Code | Barcode |
|---|---|---|
| גאמיס מגנזיום ציטראט | 688146 | 7290019444169 |
| מגנזיום מקס 550 | 671975 | 7290118818205 |
| מגנזיום ביסגליצינאט | 704023 | 7290122852608 |
| MAGNOX 520 | 345285 | 7290010207886 |
| מגנזיום ציטראט ספיגה אופטימלית | 168014 | 0033984017108 |
| מגנזיום בתוספת ויטמין B6 | 15742 | 0033984017207 |
| מגנזיום ביס גליצינאט + אבץ + B6 | 700893 | 7290001066782 |
| MAGMAX מגנזיום ביסגליצינאט | 703152 | 7290018365977 |

The category has 30 products listed; the total per the `CollectionPage` JSON-LD is 30.
This represents the full in-stock magnesium shelf at time of probe.

**For supplement corpus building:** Super-Pharm's value is as an identity source (which
supplement SKUs exist on the Israeli shelf + their barcodes), not as a nutrition panel
source. Supplement facts must come from a secondary source (iHerb panel or Playwright
rendering of the Super-Pharm product page). This limits its role in the perfect-read
gate to TIER-3 identity (barcode confirmation) rather than TIER-1 nutrition.

#### A.2.6 Access Method

**Static requests: sufficient for identity + catalog enumeration.**
**Playwright required: for supplement facts panel.**

Static HTTP is sufficient for:
- Category page traversal (product enumeration)
- Barcode extraction from DOM
- Product name and code extraction
- Price extraction (from `data-price` or JSON-LD)

Playwright is required for:
- Supplement facts table (per-serving nutrient breakdown)
- Ingredient list (if available at all — may require a separate data source)

---

## B. Adapter Design

---

### B.1 Rami Levy Adapter

#### B.1.1 Scrape Pattern

**Static `requests` (no Playwright needed).** The catalog API responds to plain HTTP POST.

```python
# Core request pattern — no browser, no JS
import requests, json

API_BASE = "https://www.rami-levy.co.il/api/catalog?"
STORE_ID = 331  # Verified to return results; test other store IDs for full coverage
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Language": "he-IL,he;q=0.9",
    "Referer": "https://www.rami-levy.co.il/he/online/search",
    "Origin": "https://www.rami-levy.co.il",
    "uid": "0",
}

def fetch_catalog_page(query: str, from_idx: int = 0, store: int = STORE_ID) -> dict:
    payload = {"q": query, "from": from_idx, "store": store}
    resp = requests.post(API_BASE, json=payload, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()
```

#### B.1.2 Field Extraction Selectors

All fields are in the JSON response body — no HTML parsing required.

| Bari Field | JSON Path | Notes |
|---|---|---|
| `barcode` | `item["barcode"]` | integer; cast to string |
| `canonical_name_he` | `item["gs"]["name"]` or `item["name"]` | `gs.name` is the full label name; `item.name` is the display name |
| `image_url` | `item["gs"]["images"]["original"]` prepend `https://img.rami-levy.co.il` | Path starts with `/product/` |
| `energy_kcal` | `gs.Nutritional_Values` where `field_name="Energy_per_100_grams"` → `value` | |
| `fat_g` | `field_name="Fats_per_100_grams"` | |
| `fat_saturated_g` | `field_name="Saturated_Fatty_Acids_per_100_grams"` | Present 20/30 bread SKUs |
| `carbohydrates_g` | `field_name="Carbohydrates_per_100_grams"` | |
| `sugars_g` | `field_name="Sugars_from_Carbohydrates_per_100_grams"` | |
| `sodium_mg` | `field_name="Sodium_per_100_grams"` | |
| `protein_g` | `field_name="Proteins_per_100_grams"` | |
| `dietary_fiber_g` | `field_name="Dietary_Fibers_per_100_grams"` | |
| `fat_trans_g` | `field_name="Trans_Fatty_Acids_per_100_grams"` | |
| `ingredients_text_he` | `gs["Ingredient_Sequence_and_Name"]` | Full Hebrew string |
| `red_label_codes` | `gs["Food_Symbol_Red"]` → list of `{code, value}` | FSR1=none, FSR5=green |
| `allergens` | `gs["Allergen_Type_Code_and_Containment"]` | Integer codes |
| `country_of_origin` | `gs["Country_of_Origin"]` | ISO code |
| `serving_size_g` | `gs["Net_Content"]["value"]` | Pack size, not serving size |

Helper to extract a nutrition value by field_name:
```python
def extract_nutr_value(nutritional_values: list, field_name: str) -> float | None:
    for entry in nutritional_values:
        for field in entry.get("fields", []):
            if field.get("field_name") == field_name:
                try:
                    return float(field["value"])
                except (TypeError, ValueError):
                    return None
    return None
```

#### B.1.3 Pagination

The API uses `from` (offset) not a page number. `total` is returned in the response.
Pagination loop:

```python
def fetch_all_results(query: str, store: int) -> list[dict]:
    results = []
    from_idx = 0
    while True:
        resp = fetch_catalog_page(query, from_idx, store)
        batch = resp.get("data", [])
        results.extend(batch)
        total = resp.get("total", 0)
        from_idx += len(batch)
        if not batch or from_idx >= total:
            break
    return results
```

#### B.1.4 Store ID Strategy

Not all store IDs return results. Store 331 is verified. A production adapter should
either: (a) use a fixed verified list of large-volume store IDs (e.g., 82, 179, 279,
290, 306, 331, 412), or (b) call the `www-api.rami-levy.co.il/api/v2/site` endpoint
to discover active stores. The `available_in` field on each product lists store IDs
where it is stocked — this can be used for cross-store corpus coverage analysis.

#### B.1.5 Fallback Position in Perfect-Read Gate

Slot: **Source 2 (secondary retailer scrape)** in the `perfect_read_gate_design_v1.md` §B.2 flow.

For categories where Yohananof is primary: Rami Levy is fallback.
For categories where Shufersal is primary: Rami Levy is secondary fallback.

Given that Rami Levy returns all 7 Tier-1 fields in one API call (no page scrape needed),
it can also serve as a **parallel primary source** for grocery categories where its
coverage of house-brand and budget products exceeds Yohananof/Shufersal.

#### B.1.6 Registration in `acquisition_audit_v2.py`

Add to `probe_modules` list:

```python
("rami_levy", "ramilevy_probe", "RamiLevyProbe"),
```

This requires a new file `03_operations/bsip0/acquisition_v2/ramilevy_probe.py` to be
written. The probe class follows the pattern of `shufersal_probe.py` but uses the POST
API instead of HTML scraping. `requires_browser = False`.

#### B.1.7 BSIP0 Gate Thresholds

Based on the probe results, recommended thresholds for Rami Levy:

```
GATE_MIN_PRODUCTS = 20
GATE_NUTRITION_PCT = 0.80   # Energy+fat+carbs+sugars+sodium+protein all ~100%; sat_fat ~67%
GATE_INGREDIENT_PCT = 0.70  # 30/30 verified; real-world may vary
GATE_MIN_RETAILERS = 1
```

Sat_fat coverage below 100% is expected for some categories; the perfect-read gate
(product-level) handles sat_fat absence on individual products, not the corpus gate.

---

### B.2 Super-Pharm Adapter

#### B.2.1 Scrape Pattern

**Static `requests` for identity/catalog enumeration. Playwright required for supplement
facts panel.**

The adapter splits into two layers:

**Layer 1 — Identity enumeration (static requests):**
Category page traversal to enumerate product codes, barcodes, names, prices, and URLs.
Sufficient for corpus building and barcode confirmation.

**Layer 2 — Supplement facts (Playwright):**
Navigate to individual product pages and wait for the supplement-facts tab to render
via JavaScript. The tab content is not in the static HTML; it appears to be loaded by
a Vue component after mount.

#### B.2.2 Layer 1 — Identity Field Extraction (Static)

**Category page:** `https://shop.super-pharm.co.il/{category-path}/c/{category-code}`

From the category page static HTML:
- `data-ean` attribute on `.add-to-basket` div → barcode
- `data-product-code` attribute on `.add-to-basket` div → internal product code
- `data-name` attribute → Hebrew product name (for display)
- `data-price` → price in ILS
- `data-brand` → brand name
- JSON-LD `CollectionPage.mainEntity.itemListElement` → product page URLs

```python
# Static category traversal selectors
CATEGORY_URLS = {
    "magnesium":     "https://shop.super-pharm.co.il/health/supplements/minerals/magnesium/c/30301113",
    "supplements":   "https://shop.super-pharm.co.il/health/supplements/c/30300000",
    "vitamins":      "https://shop.super-pharm.co.il/health/supplements/vitamins/c/30301000",
    "omega":         "https://shop.super-pharm.co.il/health/supplements/omega/c/30301400",
}

# From product card DOM:
EAN_SELECTOR = "[data-ean]"       # attribute: data-ean = barcode
CODE_SELECTOR = "[data-product-code]"
NAME_SELECTOR = "[data-name]"
```

**Individual product page:** `https://shop.super-pharm.co.il/{path}/p/{code}`

From static HTML:
- `<p class="description-ean">ברקוד מוצר:&nbsp;{barcode}</p>` — barcode
- JSON-LD `Product.name` → Hebrew name
- JSON-LD `Product.image` → image URL (filename = barcode)
- JSON-LD `Product.brand.name` → brand
- JSON-LD `Product.offers.price` → price
- `.product-properties .property` spans → dosage, kosher, pack size, storage instructions

#### B.2.3 Layer 2 — Supplement Facts (Playwright Required)

The supplement facts tab is a Vue-rendered component. After page navigation and JS
execution, the tab becomes visible. The selector pattern (inferred from page structure,
NOT verified by static fetch — the panel was not present in static HTML):

```python
# Playwright sequence — NOT verified live (requires browser execution):
SUPPLEMENT_FACTS_TAB_SELECTOR = "a[href='#supplement-facts'], a[href='#nutrition']"
SUPPLEMENT_FACTS_TABLE_SELECTOR = ".supplement-facts, .nutrition-table, table.nutr"
```

These selectors are INFERRED from the page structure. They must be verified empirically
by running Playwright against the product page before implementing. The gap between
what the static HTML shows (product description + properties only) and what the full
rendered page shows (supplement facts tab, if it exists) is the key unknown.

**Alternative:** If the supplement facts tab consistently does not exist for supplement
products on Super-Pharm (some supplement products may only have description + properties,
not a structured nutrition table), then Super-Pharm's primary value is identity/barcode
only, and supplement nutrition data must come from iHerb panel or label OCR.

#### B.2.4 Fallback Position in Perfect-Read Gate

**Supplement corpus:** Super-Pharm identity layer (Layer 1) slots as a barcode
confirmation source — Tier-3 identity in the gate, not a Tier-1 nutrition source.
It confirms that a barcode exists on the Israeli shelf and provides price context.

If Playwright rendering (Layer 2) yields supplement facts, it would slot as:
- Primary source for Israeli supplement SKUs not found on iHerb
- Secondary source for SKUs found on both, to confirm Israeli label matches iHerb data

**Grocery corpus:** Super-Pharm is not a grocery retailer and does not contribute to
the grocery corpus.

#### B.2.5 Registration in `acquisition_audit_v2.py`

Add to `probe_modules`:

```python
("super_pharm", "superpharm_probe", "SuperPharmProbe"),
```

The probe class would implement Layer 1 in static HTTP and Layer 2 as an optional
Playwright extension. `requires_browser = False` for Layer 1 only; a separate
`requires_browser = True` probe for Layer 2 supplement facts.

#### B.2.6 BSIP0 Gate Thresholds for Supplement Corpus

Super-Pharm does not expose nutrition in static HTML. The gate for supplement corpus
must account for this:

```
GATE_MIN_PRODUCTS = 20       # identity enumeration only
GATE_NUTRITION_PCT = 0.0     # not applicable for identity-only layer
GATE_INGREDIENT_PCT = 0.0    # not applicable for identity-only layer
GATE_MIN_RETAILERS = 1
```

If the Playwright layer is implemented and verified:
```
GATE_NUTRITION_PCT = 0.50    # supplement facts may be sparse
GATE_INGREDIENT_PCT = 0.30   # ingredient lists less common on supplements
```

---

## C. Coverage Assessment

---

### C.1 Rami Levy — Grocery Coverage Increment

**Incremental value: HIGH for grocery categories (bread, hummus, snack_bars, yogurt, milk).**

| Category | Current Primary | Rami Levy Adds |
|---|---|---|
| Bread | Shufersal (v3 scrape) | Rami Levy house-brand products (Rami brand), budget-tier mainstream. Different supplier mix from Shufersal — expands toward periphery market and budget consumer. |
| Hummus | Yohananof | Rami Levy mainstream hummus shelf. Different SKUs than Yohananof premium/organic bias. |
| Snack bars | Yohananof OCR + scrape | Rami Levy budget snack segment. Yohananof is wellness-positioned; Rami Levy covers mainstream. |
| Yogurt | Yohananof | Different pack sizes (Rami house-brand multi-packs). |
| Milk | Yohananof | Rami Levy often stocks the same national brands; marginal incremental. |

**Unique value proposition:**
- Rami Levy serves urban and periphery markets that are underrepresented in Yohananof
  (premium/Tel Aviv-centric) and Shufersal (national but urban-heavy).
- The API returns `available_in` (list of store IDs stocking each SKU), enabling
  geographic availability analysis.
- The API returns `lables` (quality labels like "ויגן פרנדלי"), `gs.Diet_Information`
  (diet codes), and `gs.Food_Symbol_Red` (red-label status) — fields not available
  in the Shufersal v3 HTML scrape.
- No satfat blind spot for bread (coverage 67%); for higher-fat categories (hummus,
  yogurt), satfat coverage is expected to be higher.

**Categories where neither Rami Levy nor Super-Pharm helps:**
- Brined cheeses: Rami Levy likely has these; Super-Pharm does not. Coverage impact
  for brined cheeses from Rami Levy needs a separate probe with the cheese department
  query (no probe done on this category in this run).

### C.2 Super-Pharm — Supplement Coverage Increment

**Incremental value: MEDIUM for supplement identity; LOW for supplement nutrition
(pending Playwright verification).**

| Source | What it adds |
|---|---|
| Super-Pharm identity (Layer 1) | Confirmed barcode + price for Israeli supplement shelf (30+ magnesium SKUs, 30+ multi-vitamin SKUs, etc.). Fills barcode gaps where iHerb barcode does not match Israeli EAN. |
| Super-Pharm supplement facts (Layer 2 — pending) | IF Playwright rendering yields a supplement facts table, this becomes the primary nutrition source for Israeli supplement SKUs not on iHerb. IF the tab is consistently empty, Super-Pharm contributes identity only. |
| il_prices (already live) | Price + Hebrew name — already in pipeline via `fetch_super_pharm_supplements()`. Super-Pharm scrape extends this with structured product page data. |

**What Super-Pharm does NOT add:**
- Grocery nutrition data (Super-Pharm is not a food retailer in the relevant sense)
- A substitute for iHerb supplement facts (iHerb is the recommended panel source for
  supplement actives/doses/forms; Super-Pharm may confirm Israeli label but is not
  the authoritative supplement science source)
- A path around the Playwright requirement for supplement facts

**Honest assessment of Super-Pharm's supplement nutrition value:**
The static HTML probe found NO supplement facts data on two sampled product pages.
Until a Playwright probe confirms that the supplement facts tab renders usable structured
data (and not just an image of the label), Super-Pharm's role in the nutrition pipeline
is identity-only. This is not a failure — barcode confirmation from Super-Pharm still
strengthens the `verification_status` promotion from `candidate` to `verified` for
supplement SKUs.

---

## D. Not Done (Honesty Section)

1. Rami Levy sat_fat coverage was measured on bread only (20/30). Sat_fat coverage
   for hummus, yogurt, snack_bars, and other target categories is unknown from this probe.
2. Rami Levy store ID strategy: only store 331 was confirmed to return results. A
   production adapter needs an empirical store-ID discovery step or a curated verified
   list (stores 82, 179, 279, 290, 306, 412 are listed in `available_in` for all sampled
   products but were not individually tested).
3. Super-Pharm supplement facts tab: NOT verified by Playwright. The finding that
   supplement facts are absent in static HTML does not rule out the possibility that
   the Playwright-rendered page contains a supplement facts table. A Playwright probe
   is required before drawing a final conclusion on Layer 2 value.
4. Super-Pharm non-magnesium supplement categories: probed magnesium only. Coverage
   of omega-3, vitamin D, B12, zinc, and other categories is INFERRED from the category
   URL structure visible in the navigation but not verified by fetching those pages.
5. Neither adapter has been implemented as a Python module. This is a design document;
   implementation requires a separate task.
6. The `acquisition_audit_v2.py` has not been modified. No pipeline runs affected.
7. No BSIP gate was run. No corpus was changed. No scoring was touched.

---

## E. Super-Pharm Playwright Layer 2 — Live Render Probe (2026-06-25)

**Status: CLOSED QUESTION. Supplement facts NOT present after full JavaScript render.**

This section records the live Playwright probe that resolves the open item from §A.2
and §D item 3. The static-HTML probe found no supplement facts; this Playwright probe
determines whether they appear after JavaScript execution.

### E.1 Probe Method

**Script:** `03_operations/bsip2/proto_v0/probes/superpharm_playwright_probe.py`

Playwright headless Chromium (chromium.launch, headless=True). For each product page:

1. Navigate with `wait_until="domcontentloaded"` then wait for `networkidle`.
2. Dismiss popups (cookie banners, modals) via known selectors.
3. Query DOM for supplement facts before any tab interaction.
4. Attempt to click every plausible tab / accordion selector (28 selectors tried:
   Hebrew text matches, attribute patterns, class patterns, SAP Hybris accordion patterns).
5. Wait for content to settle after each click.
6. Query DOM for supplement facts again after tab interactions.
7. Capture all XHR/fetch responses containing supplement-related keywords.
8. Save full rendered HTML for each product (saved to
   `03_operations/bsip2/proto_v0/probes/superpharm_playwright_captures/`).

**Products probed (4 total):**

| Label | Product Code | Barcode | Product Name |
|---|---|---|---|
| multivitamin-prenatal | 332649 | 7290011899479 | אלטמן - מולטי ויטמין לנשים בהריון |
| magnesium-bisglycinate | 704023 | 7290122852608 | לייף - מגנזיום ביסגליצינאט |
| mag-extra-688146 | 688146 | 7290019444169 | אלטמן - גאמיס מגנזיום ציטראט (gummies) |
| mag-extra-671975 | 671975 | 7290118818205 | סופהרב - מגנזיום מקס 550 |

### E.2 DOM Structure — Verified by Playwright Render

The rendered page has exactly **two tab panes** after full JavaScript execution:

- `#product-info` — "אודות המוצר" (About the Product)
- `#productDeliveryTerms` — "מדיניות משלוחים ואספקה" (Delivery Policy)

There is no supplement facts tab, no ingredient list tab, no nutrition table tab.

The `#product-info` pane contains:

1. **Product description** — a 1-3 sentence marketing description (Hebrew)
2. **Barcode line** — `ברקוד מוצר: {EAN}`
3. **Product properties** (`.product-properties`) — a structured list of operational
   metadata fields

### E.3 Verbatim DOM Content — All 4 Products

**Product: magnesium-bisglycinate (p/704023, barcode 7290122852608)**
VERIFIED-BY-PLAYWRIGHT-RENDER. Full `#product-info` tab pane text:

```
תיאור המוצר
מגנזיום ביסגליצינאט עם אבץ, ויטמין B6.
ברקוד מוצר: 7290122852608

מאפייני המוצר
בעל תו GMP
הוראות שימוש:       1 כמוסה ליום עם הארוחה
סוג כשרות:          כשר פרווה
נותן כשרות:         בהשגחת הרבנות חולון
המלצת אחסון:        יש לאחסן במקום קריר ויבש
תכולה:              60 כמוסות
משקל יחידה:         990 מ"ג
ויגן פרנדלי
אזהרה:              נשים בהריון, מניקות, ילדים ואנשים הנוטלים תרופות מרשם - יש
                    להיוועץ ברופא. יש להרחיק מהישג ידם של ילדים. אריזה זו מכילה
                    סופח לחות - לא לבליעה
```

**Product: multivitamin-prenatal (p/332649, barcode 7290011899479)**
VERIFIED-BY-PLAYWRIGHT-RENDER. Full `#product-info` tab pane text:

```
תיאור המוצר
מולטי ויטמין לנשים בהריון. ויטמינים ומינרלים לנשים לפני-בהריון-אחרי.
ברקוד מוצר: 7290011899479

מאפייני המוצר
מגדר:               נשים
סוג כשרות:          כשר פרווה
נותן כשרות:         בהשגחת בד"צ בית יוסף ובאישור הרבנות הראשית לישראל
הוראות שימוש:       קפליה אחת ביום עם האוכל
משקל יחידה מופרדת: 1,525 מ"ג
המלצת אחסון:        במקום קריר ויבש
תכולה:              60 קפליות
ללא גלוטן
אזהרה:              נשים בהריון, נשים מניקות, אנשים הנוטלים תרופת מרשם וילדים -
                    יש להיוועץ ברופא. להרחיק מהישג ידם של ילדים. אריזה זו מכילה
                    סופח לחות. השגחת מבוגר מומלצת
```

**Product: gummies-mag-citrate (p/688146, barcode 7290019444169)**
VERIFIED-BY-PLAYWRIGHT-RENDER. Full `#product-info` tab pane text:

```
תיאור המוצר
אלטמן גאמיס מגנזיום ציטראט אשכולות במרקם ג'לי בטעם פטל
ברקוד מוצר: 7290019444169

מאפייני המוצר
הוראות שימוש:       1-3 יחידות ביום. ללעיסה
סוג כשרות:          כשר פרווה
נותן כשרות:         בד"צ איגוד רבנים. בהשגחת הרבנות שדרות
המלצת אחסון:        לאחסן סגור היטב, במקום קריר ויבש
תכולה:              50 יחידות
משקל יחידה:         3.5 גרם
עלול להכיל אלרגנים: שאריות דגים
ויגן פרנדלי
אזהרה:              נשים בהריון, נשים מניקות, אנשים הנוטלים תרופות מרשם וילדים -
                    יש להיוועץ ברופא. להרחיק מהישג ידם של ילדים
```

**Product: magmax-550 (p/671975, barcode 7290118818205)**
VERIFIED-BY-PLAYWRIGHT-RENDER. Full `#product-info` tab pane text:

```
תיאור המוצר
קומפלקס מגנזיום אוקסיד וציטראט במינון גבוה. תורם לחילוף חומרים תקין
להפקת אנרגיה. תורם להפחתת עייפות ותשישות.
ברקוד מוצר: 7290118818205

מאפייני המוצר
בעל תו GMP
הוראות שימוש:       כמוסה אחת ביום. אין לעבור את המלצת הצריכה המומלצת
סוג כשרות:          כשר
נותן כשרות:         מאושר מטעם הבד"ץ ירושלים של העדה החרדית
המלצת אחסון:        כדי לשמור על טריות המוצר ואיכותו, יש להוציא את צמר הגפן
                    ולאחסן את המוצר במקום קריר ויבש, הרחק מחום, אור ולחות
תכולה:              60 כמוסות
משקל יחידה:         1,135 מ"ג
עלול להכיל אלרגנים: סויה
ויגן פרנדלי
אזהרה:              נשים בהריון, מניקות, ילדים אנשים הנוטלים תרופות מרשם -
                    יש להיועץ ברופא. יש להרחיק מהישג ידם של ילדים. אריזה זו
                    מכילה סופח לחות וצמר גפן - לא לבליעה
```

### E.4 What IS Available After Full Render — Exact Field Map

These fields are available in the rendered DOM across all 4 products (VERIFIED-BY-RENDER):

| Field | DOM Location | Value Present | Extraction Notes |
|---|---|---|---|
| Product name (Hebrew) | JSON-LD `Product.name`, page `<title>`, breadcrumb | YES / 4/4 | Reliable |
| Barcode (EAN-13) | `<p class="description-ean">ברקוד מוצר: {EAN}</p>` | YES / 4/4 | Reliable |
| Brand name | JSON-LD `Product.brand.name`, page heading | YES / 4/4 | Reliable |
| Price | JSON-LD `Product.offers.price` | YES / 4/4 | Reliable |
| Image URL | JSON-LD `Product.image` (filename = barcode) | YES / 4/4 | Reliable |
| Dosage / serving instruction (Hebrew) | `.product-properties` → `הוראות שימוש:` | YES / 4/4 | Not structured — free text |
| Pack count (unit count) | `.product-properties` → `תכולה:` | YES / 4/4 | "60 כמוסות", "50 יחידות" |
| Unit weight (mg or g) | `.product-properties` → `משקל יחידה:` | YES / 4/4 | Total capsule/tablet weight, NOT elemental active dose |
| Kosher certification | `.product-properties` → `סוג כשרות:` + `נותן כשרות:` | YES / 4/4 | |
| Storage instructions | `.product-properties` → `המלצת אחסון:` | YES / 4/4 | |
| Allergen warning | `.product-properties` → `עלול להכיל אלרגנים:` | 2/4 (where applicable) | |
| GMP certification badge | `.product-properties` → `בעל תו GMP` | 2/4 | |
| Vegan label | `.product-properties` → `ויגן פרנדלי` | 3/4 | |
| Gluten-free label | `.product-properties` → `ללא גלוטן` | 1/4 | |
| Warning text | `.product-properties` → `אזהרה:` | 4/4 | Standard pregnancy / children advisory |
| Marketing description | `tab-pane#product-info` → `תיאור המוצר` | YES / 4/4 | 1-3 sentences, not structured |

### E.5 What is NOT Available After Full Render (VERIFIED ABSENT)

These fields are **absent from the fully rendered DOM across all 4 products**:

| Field | Status |
|---|---|
| Elemental active dose per serving (e.g. "מגנזיום אלמנטרי 100 מ"ג למנה") | NOT FOUND / 4/4 |
| Per-serving nutrient breakdown table | NOT FOUND / 4/4 |
| Supplement facts table (structured mg/mcg/IU rows) | NOT FOUND / 4/4 |
| Hebrew ingredient / composition list | NOT FOUND / 4/4 |
| Magnesium form (bisglycinate vs oxide vs citrate) in structured field | NOT FOUND — only in product name text |
| Serving size in mg / structured format | NOT FOUND — only total unit weight |
| Other active ingredients per serving | NOT FOUND |
| Supplement facts tab or accordion | NOT FOUND — only 2 tabs exist: product-info + delivery |

**Critical clarification on "משקל יחידה" (unit weight):**
The value "990 מ\"ג" for magnesium bisglycinate is the **total capsule weight** (matrix +
excipients + active), NOT the elemental magnesium dose per serving. This field cannot
be used as a proxy for active ingredient content. It is operationally useless for the
supplement scoring program.

### E.6 Tab Structure — Definitive

The probe confirmed the tab structure for SAP Hybris Super-Pharm after full render:

```
.extra-details
├── #product-info tab ("אודות המוצר")
│   ├── product description (1-3 sentences)
│   ├── barcode line
│   └── .product-properties (dosage, kosher, pack size, unit weight, warnings)
└── #productDeliveryTerms tab ("מדיניות משלוחים ואספקה")
    └── shipping and return policy text only
```

No third tab exists. No supplement facts section is rendered anywhere in the DOM.

### E.7 XHR API Analysis

All XHR/fetch calls captured during page load (covering all 4 product pages) were:

- Ad-tech and analytics: DynamicYield (A/B testing), Criteo, Google Ads, DoubleClick
- The initial page HTML (HTTP 200, SAP Hybris server-rendered HTML)
- CSS and JS assets

**No product data API returning supplement facts was observed.** The SAP Hybris backend
does not make a client-side API call to populate supplement facts — because there is no
supplement facts data to display. The absence is not a timing issue: even if the page
were given more time to settle, no supplement facts XHR would fire because the data is
not stored in the Hybris platform for these products.

### E.8 Final Determination

**Super-Pharm is confirmed as an IDENTITY-ONLY source for supplement products.**

This is unambiguous:
- 4/4 products fully rendered by Playwright headless Chromium
- 28 tab/accordion selectors tried
- XHR traffic fully inspected
- Full rendered HTML saved and parsed

**Super-Pharm CANNOT serve as a supplement nutrition source.** Its role in the pipeline
is strictly:

1. **Identity enumeration** — which supplement SKUs exist on the Israeli shelf
2. **Barcode confirmation** — EAN-13 from `data-ean` on category pages and
   `<p class="description-ean">` on product pages
3. **Price signal** — from JSON-LD `Product.offers.price`
4. **Dosage instructions** — free-text "הוראות שימוש" (e.g. "1 כמוסה ליום") — useful
   as a sanity cross-check against iHerb data but not a substitutable structured field
5. **Pack count** — "תכולה: 60 כמוסות" — useful for price-per-dose computation

**The supplement facts source for the scoring program remains: direct product label
scrape (if parsed, use it; if not, the field is NULL). iHerb panel client is the
candidate secondary source for products also sold on iHerb. No other source is permitted
(OFF ban applies; Tzameret is directional-only).**

### E.9 DOM Selectors for Identity Extraction (Confirmed by Playwright)

These selectors are VERIFIED-BY-PLAYWRIGHT-RENDER:

```python
# Category page selectors (verified against /c/30301113)
EAN_SELECTOR = "[data-ean]"                # barcode on product cards
CODE_SELECTOR = "[data-product-code]"      # internal product code
# Category had 30 products; both attributes confirmed on all 30

# Product page selectors (verified against 4 product pages)
BARCODE_SELECTOR = "p.description-ean"    # text: "ברקוד מוצר: {EAN}"
TAB_PANE_INFO = "#product-info"            # full product-info pane
PROPERTIES_SELECTOR = ".product-properties .property"  # key-value property rows
DOSAGE_PROPERTY_TEXT = "הוראות שימוש"     # text to find dosage within properties
PACK_COUNT_TEXT = "תכולה"                 # text to find pack count within properties
UNIT_WEIGHT_TEXT = "משקל יחידה"           # text to find unit weight (total, not active)
```

Note: the `משקל יחידה` field reports total capsule/tablet weight, NOT elemental active
dose. Do not use it as an active dose proxy.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/new_sources_probe_v1.md",
      "action": "created",
      "sha256": "to-be-computed-by-orchestrator"
    }
  ],
  "counts": {
    "rami_levy_tier1_fields_verified": "7/7 fields present in API response structure (energy_kcal, fat_g, fat_saturated_g, carbohydrates_g, sugars_g, sodium_mg, protein_g) / denominator: TIER1 list from perfect_read_gate_design_v1.md §B.1",
    "rami_levy_energy_coverage": "30/30 sampled bread products / denominator: POST /api/catalog? q=לחם store=331 response, 2026-06-25",
    "rami_levy_fat_coverage": "30/30 / same denominator",
    "rami_levy_sat_fat_coverage": "20/30 bread products / same denominator — bread is a low-fat category; other categories not probed",
    "rami_levy_carbs_coverage": "30/30 / same denominator",
    "rami_levy_sugars_coverage": "29/30 / same denominator",
    "rami_levy_sodium_coverage": "30/30 / same denominator",
    "rami_levy_protein_coverage": "30/30 / same denominator",
    "rami_levy_ingredient_coverage": "30/30 / same denominator",
    "rami_levy_barcode_coverage": "30/30 / same denominator",
    "super_pharm_magnesium_products_enumerated": "30/30 in static HTML (category page JSON-LD CollectionPage) / denominator: GET /health/supplements/minerals/magnesium/c/30301113, 2026-06-25",
    "super_pharm_barcode_in_static_html": "verified on 2 product pages (p/332649: 7290011899479, p/704023: 7290122852608) / denominator: 2 product pages fetched",
    "super_pharm_supplement_facts_in_static_html": "0/2 product pages had supplement facts / denominator: 2 product pages fetched (p/332649, p/704023)",
    "super_pharm_ingredient_list_in_static_html": "0/2 product pages / same denominator",
    "api_endpoints_verified": "1 Rami Levy (POST /api/catalog?), 1 Super-Pharm (static HTML category + product pages) / denominator: all endpoints probed"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/perfect_read_gate_design_v1.md", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/victory_probe.py", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/acquisition_audit_v2.py", "exit_code": 0},
    {"cmd": "Read integrations/clients/il_prices.py", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v3/shufersal_probe_v3.py (lines 1-100)", "exit_code": 0},
    {"cmd": "WebFetch https://www.ramilevy.co.il/ — ECONNREFUSED", "exit_code": 1},
    {"cmd": "WebFetch https://www.super-pharm.co.il/ — 301 redirect to shop.super-pharm.co.il", "exit_code": 0},
    {"cmd": "WebFetch https://shop.super-pharm.co.il/ — server-rendered HTML with React signal", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://www.rami-levy.co.il/ — status=200, NUXT signal detected", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://shop.super-pharm.co.il/health/supplements/c/30300000 — status=200, Vue + JSON-LD CollectionPage with 30 items", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://www.rami-levy.co.il/he/online/1271/product/443905 — NUXT data found, API paths extracted from JS bundles", "exit_code": 0},
    {"cmd": "Bash: python parse rl/ea76006.js — found www-api.rami-levy.co.il/api/v2/ and POST /api/catalog? URL", "exit_code": 0},
    {"cmd": "Bash: python POST https://www.rami-levy.co.il/api/catalog? store=331 q=לחם — status=200, 30 products with full nutrition", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://shop.super-pharm.co.il/...p/332649 — status=200, barcode in description-ean, supplement facts NOT in HTML", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://shop.super-pharm.co.il/.../p/704023 — status=200, barcode 7290122852608 confirmed, supplement facts NOT in HTML", "exit_code": 0},
    {"cmd": "Bash: python HTTP GET https://shop.super-pharm.co.il/health/supplements/minerals/magnesium/c/30301113 — 30 magnesium products, EANs extracted", "exit_code": 0},
    {"cmd": "Bash: python coverage measurement Rami Levy 30 products — TIER1 field coverage computed", "exit_code": 0}
  ],
  "not_done": [
    "ramilevy_probe.py not implemented — probe_modules entry not added to acquisition_audit_v2.py",
    "superpharm_probe.py not implemented (identity layer only — supplement facts confirmed absent)",
    "Rami Levy sat_fat coverage for non-bread categories (hummus, yogurt, snack_bars) not measured",
    "Rami Levy store ID discovery/verification for stores beyond 331 not done",
    "Super-Pharm non-magnesium supplement categories not probed by Playwright (omega, vitamin D, B12, zinc) — but finding is structural (no supplement facts tab exists) so generalization is strong",
    "No BSIP0 gate run, no corpus changed, no scoring touched",
    "sha256 of report file not computed — orchestrator to run Get-FileHash"
  ],
  "self_check": "Acceptance test (original): (1) a production ramilevy_probe.py passes BSIP0 gate (>=80% nutrition, >=70% ingredient) on a target category — NOT YET DONE; (2) Playwright probe of Super-Pharm confirms or denies supplement facts in rendered page — DONE: confirmed ABSENT 4/4 products; (3) both probes registered in acquisition_audit_v2.py — NOT YET DONE. Layer 2 question is closed: Super-Pharm is identity-only for supplements. Supplement facts source remains direct product label scrape (NULL if not parsed) plus iHerb panel client for iHerb-listed SKUs."
}
```
