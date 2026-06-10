"""
BSIP0 Scraper — Shufersal Frozen Vegetables

Tests Shufersal access, attempts static HTTP scraping.
Produces:
  - Raw HTML artifacts in bsip0_scrape/shufersal_frozen_vegetables/
  - True BSIP0 output in 02_products/frozen_vegetables/bsip0_outputs/
"""
import sys, os, json, re, time, pathlib, urllib.parse, gzip, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

# TASK-239: use the shared multi-table-aware parser (per-100g selection) — no inline
# nutrition extraction. The same parser runs live and on any offline re-extraction.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "_shared"))
import bsip0_nutrition as bn  # noqa: E402

# ── Configuration ───────────────────────────────────────────────────────
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()  # → C:\Bari
SCRAPE_DIR = BASE_DIR / "03_operations" / "bsip0" / "scrape" / "shufersal_frozen_vegetables"
RAW_HTML_DIR = SCRAPE_DIR / "raw_html"
PRODUCT_DIR = SCRAPE_DIR / "product_pages"
SEARCH_DIR = SCRAPE_DIR / "search_pages"
OUTPUT_DIR = BASE_DIR / "02_products" / "frozen_vegetables" / "bsip0_outputs"
REPORT_DIR = BASE_DIR / "02_products" / "frozen_vegetables" / "reports"

for d in [RAW_HTML_DIR, PRODUCT_DIR, SEARCH_DIR, OUTPUT_DIR, REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.shufersal.co.il/online/he/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

SHUFERSAL_SEARCH = "https://www.shufersal.co.il/online/he/search"
SHUFERSAL_HOME   = "https://www.shufersal.co.il/online/he/"
SHUFERSAL_PRODUCT = "https://www.shufersal.co.il/online/he/A{}"

# ── Session ─────────────────────────────────────────────────────────────
session = requests.Session()
session.headers.update(HEADERS)

def log(msg: str):
    try:
        print(f"[{datetime.now().isoformat()}] {msg}", flush=True)
    except UnicodeEncodeError:
        safe = msg.encode('ascii', 'replace').decode('ascii')
        print(f"[{datetime.now().isoformat()}] {safe}", flush=True)

# ── Step 1: Test access ─────────────────────────────────────────────────
log("Testing Shufersal access...")
try:
    r = session.get(SHUFERSAL_HOME, timeout=15)
    r.raise_for_status()
    blocked = "Maintenance1.jpg" in r.text or (
        "s3-eu-west-1" in r.text and "maintenance" in r.text.lower()
    )
    if blocked:
        log("BLOCKED: TLS fingerprint block detected. Attempting Playwright fallback.")
        USE_PLAYWRIGHT = True
    else:
        log(f"UNBLOCKED: {len(r.text)} bytes received")
        USE_PLAYWRIGHT = False
except Exception as e:
    log(f"ACCESS ERROR: {e}")
    sys.exit(1)

# ── Step 2: Search frozen vegetables ────────────────────────────────────
log("Searching for frozen vegetables...")
frozen_keywords = [
    "ירקות קפואים",
    "ירקות מוקפאים",
    "קטניות קפואות",
    "תירס קפוא",
    "ברוקולי קפוא",
    "אפונה קפואה",
    "שעועית קפואה",
    "פולי סויה קפואים",
    "ארטישוק קפוא",
    "כרובית קפואה",
    "גזר קפוא",
    "לקט ירקות קפוא",
    "פול קפוא",
    "חומוס קפוא",
    "במיה קפואה",
    "שום קפוא",
    "תבלינים קפואים",
]

all_products = {}
seen_codes = set()

for kw in frozen_keywords:
    log(f"  Searching: {kw}")
    params = {"q": kw, "pageSize": 48, "currentPage": 0}
    try:
        r = session.get(SHUFERSAL_SEARCH, params=params, timeout=15)
        r.raise_for_status()
    except Exception as e:
        log(f"    ERROR: {e}")
        continue

    soup = BeautifulSoup(r.text, "lxml")
    items = soup.find_all("li", attrs={"data-product-name": True})
    log(f"    Found {len(items)} items")

    for li in items:
        d = li.attrs
        code = d.get("data-product-code")
        if not code or code in seen_codes:
            continue
        seen_codes.add(code)
        product = {
            "product_code": code,
            "name_he": d.get("data-product-name"),
            "brand": d.get("data-product-manufacturer") or "",
            "price": d.get("data-product-price") or "",
            "package_size": d.get("data-product-dimension") or "",
            "barcode": d.get("data-product-ean") or "",
            "category_raw": d.get("data-all-categories") or "",
            "is_food": d.get("data-food") == "true",
            "image_url": d.get("data-product-image-url") or "",
            "scrape_source": "search_html",
            "search_keyword": kw,
        }
        all_products[code] = product

log(f"Total unique products found: {len(all_products)}")

# ── Step 3: Filter to scope-IN products ─────────────────────────────────
SCOPE_OUT_KEYWORDS = [
    "צ'יפס", "ציפס", "fries", "fry",
    "מוקפץ", "מוקפצים",
    "שניצל", "קציצה", "קציצות",
    "רוטב", "מרק",
    "פיצה", "ניוקי", "פסטה",
    "לביבות", "לביבה",
    "כופתאות",
    "מאפה", "מאפים",
    "פרי קפוא", "פרות קפואים",
    "תות", "מנגו", "פטל", "אוכמנית",
    "דג", "סלמון", "בשר", "עוף",
    "פשטידה",
    "בצק",
]

scope_in = {}
scope_out = {}

for code, p in all_products.items():
    name = (p.get("name_he") or "").lower()
    # Check scope-out keywords
    excluded = False
    for kw in SCOPE_OUT_KEYWORDS:
        if kw in name:
            excluded = True
            reason = f"scope_out: contains '{kw}'"
            break
    if excluded:
        p["exclusion_reason"] = reason
        scope_out[code] = p
    else:
        scope_in[code] = p

log(f"Scope-IN: {len(scope_in)}, Scope-OUT: {len(scope_out)}")

# ── Step 4: Scrape product pages for nutrition + ingredients ───────────
log("Scraping product pages for nutrition/ingredients...")

scrape_stats = {"success": 0, "failed": 0, "blocked": 0, "skipped": 0}

# TASK-239: the old `[:50]  # limit to 50 for now` dev cap silently truncated the
# corpus on every run. Now an explicit env cap defaulting to UNLIMITED (0 = no limit).
_SCRAPE_LIMIT = int(os.environ.get("BSIP0_SCRAPE_LIMIT", "0") or "0")
_scope_items = list(scope_in.items())
if _SCRAPE_LIMIT > 0:
    log(f"BSIP0_SCRAPE_LIMIT={_SCRAPE_LIMIT} — scraping first {_SCRAPE_LIMIT} of {len(_scope_items)} products")
    _scope_items = _scope_items[:_SCRAPE_LIMIT]

for code, p in _scope_items:
    url = SHUFERSAL_PRODUCT.format(code)
    log(f"  Fetching: {code} ({p.get('name_he', '?')[:30]})")

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            scrape_stats["failed"] += 1
            p["product_page_status"] = r.status_code
            continue

        # Check for block
        if "Maintenance1.jpg" in r.text:
            scrape_stats["blocked"] += 1
            p["product_page_status"] = "blocked"
            continue

        # Save raw HTML
        safe_name = re.sub(r'[^\w\-_\. ]', '_', code)
        html_path = PRODUCT_DIR / f"{safe_name}.html"
        html_path.write_text(r.text, encoding="utf-8")
        p["raw_html_path"] = str(html_path.relative_to(SCRAPE_DIR))

        # Parse product page
        soup = BeautifulSoup(r.text, "lxml")

        # Nutrition — shared parser: selects the per-100g table (never per-cube),
        # records the basis decision, and persists the replay-ready raw source.
        nutr_raw_source = bn.extract_nutrition_raw(soup)
        sel = nutr_raw_source["selection"]
        p["nutrition_basis"] = sel
        p["nutrition_raw_source"] = {"rows": nutr_raw_source["rows"], "tables": nutr_raw_source["tables"]}
        nutrition_raw = {}
        if not sel.get("insufficient"):
            for row in nutr_raw_source["rows"]:
                label = row.get("label", "")
                value = row.get("value", "")
                unit = (row.get("unit") or "").strip()
                if value and label:
                    nutrition_raw[label] = f"{value} {unit}".strip() if unit else value
        if nutrition_raw:
            p["nutrition_raw"] = nutrition_raw

        # Ingredients - look for "רכיבים" section
        ingredients = ""
        for tag in soup.find_all(["div", "span", "p"]):
            text = tag.get_text(strip=True)
            if "רכיב" in text and len(text) < 20:
                # Found ingredients header, get the content sibling
                next_el = tag.find_next(["div", "span", "p"])
                if next_el:
                    ingredients = next_el.get_text(strip=True)
                break
        if not ingredients:
            # Try regex on full text
            m = re.search(r'רכיבים?\s*:?\s*(.+?)(?:\n\n|\Z)', r.text, re.DOTALL)
            if m:
                ingredients = m.group(1).strip()[:500]
        p["ingredients_raw"] = ingredients

        # Image from JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if "image" in data:
                        p["image_url_ld"] = data["image"] if isinstance(data["image"], str) else (data["image"][0] if isinstance(data["image"], list) else "")
                    if data.get("gtin13"):
                        p["barcode_ld"] = data["gtin13"]
            except: pass

        p["product_page_status"] = r.status_code
        p["product_url"] = r.url
        scrape_stats["success"] += 1

    except Exception as e:
        log(f"    ERROR: {e}")
        scrape_stats["failed"] += 1
        p["product_page_status"] = f"error: {e}"

    time.sleep(0.5)  # polite delay

log(f"Scrape stats: {scrape_stats}")

# ── Step 5: Save artifacts ─────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Build the BSIP0 output
run_ts = datetime.now(timezone.utc).isoformat()
bsip0 = {
    "schema_version": "bsip0_v1",
    "run_id": "shufersal_frozen_vegetables_scrape_001",
    "run_ts": run_ts,
    "category": "frozen_vegetables",
    "retailer": "shufersal",
    "identity_source": "shufersal_search_page_http_scrape",
    "panel_source": "shufersal_product_page_http_scrape",
    "scrape_method": "static_http_requests_beautifulsoup",
    "search_keywords_used": frozen_keywords,
    "product_count_total": len(scope_in),
    "product_count_with_nutrition": sum(1 for p in scope_in.values() if p.get("nutrition_raw")),
    "product_count_with_ingredients": sum(1 for p in scope_in.values() if p.get("ingredients_raw")),
    "product_count_with_barcode_ld": sum(1 for p in scope_in.values() if p.get("barcode_ld")),
    "product_count_with_barcode_data_attr": sum(1 for p in scope_in.values() if p.get("barcode")),
    "scope_excluded_count": len(scope_out),
    "scope_excluded_detail": {
        k: {"name": v.get("name_he"), "reason": v.get("exclusion_reason")}
        for k, v in scope_out.items()
    },
    "scrape_stats": scrape_stats,
    "provenance": {
        "source": "shufersal_storefront",
        "method": "static_http_requests",
        "base_url": SHUFERSAL_HOME,
        "fetched_at": run_ts,
        "verification_status": "candidate",
        "tools": ["requests", "beautifulsoup4"],
        "block_status": "unblocked" if not USE_PLAYWRIGHT else "blocked_playwright_fallback",
    },
    "products": sorted(scope_in.values(), key=lambda x: x.get("name_he", "")),
}

# Save main JSON
output_path = OUTPUT_DIR / "bsip0_shufersal_frozen_vegetables_raw.json"
output_path.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")
log(f"BSIP0 output saved: {output_path}")

# Save search raw HTML
for kw in frozen_keywords:
    try:
        params = {"q": kw, "pageSize": 48, "currentPage": 0}
        r = session.get(SHUFERSAL_SEARCH, params=params, timeout=15)
        safe_kw = re.sub(r'[^\w\-_\. ]', '_', kw)[:40]
        (SEARCH_DIR / f"search_{safe_kw}.html").write_text(r.text, encoding="utf-8")
    except: pass

# ── Summary ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SCRAPE COMPLETE")
print("=" * 60)
print(f"Raw artifacts: {OUTPUT_DIR}")
print(f"Products found: {len(scope_in)}")
print(f"  With nutrition panel: {bsip0['product_count_with_nutrition']}")
print(f"  With ingredients:     {bsip0['product_count_with_ingredients']}")
print(f"  With barcode (LD):    {bsip0['product_count_with_barcode_ld']}")
print(f"  With barcode (attr):  {bsip0['product_count_with_barcode_data_attr']}")
print(f"Scope excluded: {len(scope_out)}")
