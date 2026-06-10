"""
BSIP0 Scraper — Shufersal Frozen Vegetables (v2, production).

Discovers frozen vegetable products from Shufersal search/category pages,
scrapes product pages for nutrition panels + ingredient lists,
saves raw HTML artifacts, produces true BSIP0 output JSON.
"""
import sys, os, json, re, time, pathlib, io
from datetime import datetime, timezone
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup

# ── Paths ───────────────────────────────────────────────────────────────
BASE = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()  # → C:\Bari
SCRAPE_DIR = BASE / "03_operations" / "bsip0" / "scrape" / "shufersal_frozen_vegetables"
PRODUCT_DIR = SCRAPE_DIR / "product_pages"
SEARCH_DIR = SCRAPE_DIR / "search_pages"
CATEGORY_DIR = SCRAPE_DIR / "category_pages"
OUTPUT_DIR = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs"
for d in [SCRAPE_DIR, PRODUCT_DIR, SEARCH_DIR, CATEGORY_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── HTTP config ─────────────────────────────────────────────────────────
session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "keep-alive",
})

SHUFERSAL_SEARCH = "https://www.shufersal.co.il/online/he/search"
SHUFERSAL_CATEGORY = "https://www.shufersal.co.il/online/he/c/{}"
SHUFERSAL_PRODUCT = "https://www.shufersal.co.il/online/he/p/{}"

# ── Logging ─────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().isoformat()[:19]
    safe = msg.encode('ascii', 'replace').decode('ascii')
    print(f"[{ts}] {safe}", flush=True)

log("=" * 60)
log("BSIP0 Scrape — Shufersal Frozen Vegetables (v2)")
log("=" * 60)

# ── Step 1: Discover products ──────────────────────────────────────────
log("Searching frozen vegetable keywords on Shufersal...")

FROZEN_KEYWORDS = [
    "ירקות קפואים", "ירקות מוקפאים",
    "אפונה קפואה", "ברוקולי קפוא", "כרובית קפואה",
    "תירס קפוא", "גזר קפוא", "שעועית קפואה",
    "פולי סויה קפואים", "ארטישוק קפוא",
    "לקט ירקות קפוא", "פול קפוא", "חומוס קפוא",
    "במיה קפואה", "תרד קפוא",
    "שום קפוא", "תבלינים קפואים",
    "קטניות קפואות",
]

SCOPE_OUT = [
    "צ'יפס", "ציפס", "fry", "fries",
    "מוקפץ", "שניצל", "קציצה",
    "רוטב", "מרק", "פיצה",
    "ניוקי", "לביבה", "כופתאות",
    "מאפה", "מאפים",
    "פרי קפוא", "פרות קפואים",
    "תות", "מנגו", "פטל", "אוכמנית",
    "דג", "סלמון", "בשר", "עוף",
    "פשטידה", "בצק", "נודלס",
    "חזה", "פרגיות",
    "קלחוני", "קלח",  # corn on the cob → borderline, exclude
    "שמן",  # cooking oil
    "קפה",  # iced coffee
    "גמדי",  # baby corn / mini veg → exclude
]

seen_codes = set()
products = {}

# Search pages
for kw in FROZEN_KEYWORDS:
    for page in range(2):  # pages 0 and 1
        params = {"q": kw, "pageSize": 48, "currentPage": page}
        try:
            r = session.get(SHUFERSAL_SEARCH, params=params, timeout=15)
            r.raise_for_status()
        except Exception as e:
            log(f"  SEARCH ERROR: {kw} page {page}: {e}")
            continue

        # Save raw HTML
        safe_kw = re.sub(r'[^\w]', '_', kw)[:30]
        (SEARCH_DIR / f"search_{safe_kw}_p{page}.html").write_text(r.text, encoding="utf-8")

        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all("li", attrs={"data-product-name": True})
        for li in items:
            d = li.attrs
            code = d.get("data-product-code")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            products[code] = {
                "product_code": code,
                "name_he": d.get("data-product-name"),
                "brand": d.get("data-product-manufacturer") or "",
                "price": d.get("data-product-price") or "",
                "barcode_data_attr": d.get("data-product-ean") or "",
                "category_raw": d.get("data-all-categories") or "",
                "is_food": d.get("data-food") == "true",
                "image_url": d.get("data-product-image-url") or "",
                "scrape_source": "search",
            }

# Category pages (A160501 = frozen vegetables)
CATEGORY_CODES = ["A160501", "A1605", "A500901"]
for cat_code in CATEGORY_CODES:
    for page in range(3):  # pages 0, 1, 2
        url = SHUFERSAL_CATEGORY.format(cat_code) + f"?pageSize=48&currentPage={page}"
        try:
            r = session.get(url, timeout=15)
            r.raise_for_status()
        except Exception as e:
            log(f"  CAT ERROR: {cat_code} p{page}: {e}")
            continue

        (CATEGORY_DIR / f"cat_{cat_code}_p{page}.html").write_text(r.text, encoding="utf-8")

        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all("li", attrs={"data-product-name": True})
        for li in items:
            d = li.attrs
            code = d.get("data-product-code")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            products[code] = {
                "product_code": code,
                "name_he": d.get("data-product-name"),
                "brand": d.get("data-product-manufacturer") or "",
                "price": d.get("data-product-price") or "",
                "barcode_data_attr": d.get("data-product-ean") or "",
                "category_raw": d.get("data-all-categories") or "",
                "is_food": d.get("data-food") == "true",
                "image_url": d.get("data-product-image-url") or "",
                "scrape_source": "category",
            }

log(f"Total unique products discovered: {len(products)}")

# ── Step 2: Scope filter ───────────────────────────────────────────────
scope_in = {}
scope_out = {}
for code, p in products.items():
    name = (p.get("name_he") or "").lower()
    excluded = False
    for kw in SCOPE_OUT:
        if kw in name:
            scope_out[code] = {**p, "exclusion_reason": f"scope_out: '{kw}'"}
            excluded = True
            break
    if not excluded:
        scope_in[code] = p

log(f"Scope-IN: {len(scope_in)}, Scope-OUT: {len(scope_out)}")

# ── Step 3: Product page scraping ──────────────────────────────────────
log("Scraping product pages for nutrition/ingredients...")

stats = {"success": 0, "failed": 0, "missing_nutrition": 0, "missing_ingredients": 0}

for idx, (code, p) in enumerate(sorted(scope_in.items()), 1):
    log(f"  [{idx}/{len(scope_in)}] {code}")

    url = SHUFERSAL_PRODUCT.format(code)
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            stats["failed"] += 1
            p["product_page_status"] = r.status_code
            continue

        # Check for block
        if "Maintenance1.jpg" in r.text:
            stats["failed"] += 1
            p["product_page_status"] = "blocked"
            continue

        # Save raw HTML
        safe_name = re.sub(r'[^\w\-]', '_', code)
        html_path = PRODUCT_DIR / f"{safe_name}.html"
        html_path.write_text(r.text, encoding="utf-8")
        p["raw_html_path"] = str(html_path.relative_to(SCRAPE_DIR))
        p["product_page_status"] = r.status_code
        p["product_url"] = r.url

        soup = BeautifulSoup(r.text, "lxml")

        # ── JSON-LD ──
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    p["barcode_ld"] = data.get("gtin13") or ""
                    img = data.get("image")
                    if isinstance(img, list):
                        p["image_url_jsonld"] = img[0] if img else ""
                    elif isinstance(img, str):
                        p["image_url_jsonld"] = img
                    offers = data.get("offers")
                    if isinstance(offers, dict) and offers.get("price"):
                        p["price_jsonld"] = offers["price"]
                    if data.get("sku"):
                        p["sku"] = data["sku"]
            except json.JSONDecodeError:
                pass

        # ── Nutrition panel ──
        nutrition_raw = {}
        first_nutrition_list = soup.find("div", class_="nutritionList")
        nutr_items = first_nutrition_list.find_all("div", class_="nutritionItem") if first_nutrition_list else []
        for item in nutr_items:
            label_el = item.find(class_="name") or item.find(class_="text") or item.find("span", class_=lambda c: c and "name" in c if c else False)
            value_el = item.find(class_="number") or item.find(class_="value") or item.find("span", class_=lambda c: c and ("number" in c or "value" in c) if c else False)
            if label_el and value_el:
                label = label_el.get_text(strip=True)
                value = value_el.get_text(strip=True)
                if label and value:
                    nutrition_raw[label] = value

        # Fallback: try table-based nutrition
        if not nutrition_raw:
            for table in soup.find_all("table"):
                for row in table.find_all("tr"):
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True)
                        value = cells[-1].get_text(strip=True)
                        if label and value:
                            nutrition_raw[label] = value

        if nutrition_raw:
            p["nutrition_raw"] = nutrition_raw
        else:
            stats["missing_nutrition"] += 1

        # ── Ingredients ──
        ingredients_raw = ""
        for tag in soup.find_all(["div", "span", "p", "h3", "h4"]):
            text = tag.get_text(strip=True)
            if text.strip() in ("רכיבים", "מרכיבים", "רכיב", "מרכיב"):
                next_el = tag.find_next(["div", "span", "p"])
                if next_el:
                    candidate = next_el.get_text(strip=True)
                    if len(candidate) > 5 and len(candidate) < 2000:
                        ingredients_raw = candidate
                        break

        if not ingredients_raw:
            # Regex fallback: find "רכיבים:" or similar
            m = re.search(
                r'(?:רכיבים?|מרכיבים?)\s*:?\s*(.+?)(?:\.\s*(?:מכיל|עלול|ללא|\d|$)|$)',
                r.text, re.DOTALL
            )
            if m:
                ingredients_raw = m.group(1).strip()[:1500]

        if ingredients_raw:
            p["ingredients_raw"] = ingredients_raw
        else:
            stats["missing_ingredients"] += 1

        stats["success"] += 1

    except Exception as e:
        stats["failed"] += 1
        p["product_page_status"] = f"error: {e}"

    # Polite delay
    if idx % 5 == 0:
        time.sleep(1)
    else:
        time.sleep(0.3)

log(f"Scrape stats: success={stats['success']} failed={stats['failed']} "
    f"missing_nutrition={stats['missing_nutrition']} missing_ingredients={stats['missing_ingredients']}")

# ── Step 4: Build BSIP0 output ─────────────────────────────────────────
run_ts = datetime.now(timezone.utc).isoformat()
products_list = sorted(scope_in.values(), key=lambda x: (x.get("name_he") or ""))

bsip0 = {
    "schema_version": "bsip0_v1",
    "run_id": "shufersal_frozen_vegetables_scrape_001",
    "run_ts": run_ts,
    "category": "frozen_vegetables",
    "retailer": "shufersal",
    "acquisition_method": "static_http_requests",
    "scrape_date": datetime.now().strftime("%Y-%m-%d"),
    "identity_source": "shufersal_search_html + category_html",
    "panel_source": "shufersal_product_page_html",
    "scrape_artifacts": {
        "search_pages": len(list(SEARCH_DIR.glob("*.html"))),
        "category_pages": len(list(CATEGORY_DIR.glob("*.html"))),
        "product_pages": len(list(PRODUCT_DIR.glob("*.html"))),
        "artifact_root": str(SCRAPE_DIR),
    },
    "product_count": len(products_list),
    "scope_excluded_count": len(scope_out),
    "scope_excluded": {
        k: {"name": v.get("name_he"), "reason": v.get("exclusion_reason")}
        for k, v in scope_out.items()
    },
    "completeness": {
        "with_nutrition": sum(1 for p in products_list if p.get("nutrition_raw")),
        "with_ingredients": sum(1 for p in products_list if p.get("ingredients_raw")),
        "with_barcode_ld": sum(1 for p in products_list if p.get("barcode_ld")),
        "with_barcode_data_attr": sum(1 for p in products_list if p.get("barcode_data_attr")),
        "with_image_url": sum(1 for p in products_list if p.get("image_url") or p.get("image_url_jsonld")),
        "with_product_url": sum(1 for p in products_list if p.get("product_url")),
        "with_raw_html": sum(1 for p in products_list if p.get("raw_html_path")),
    },
    "provenance": {
        "source": "shufersal_storefront",
        "method": "static_http_requests_beautifulsoup",
        "base_url": "https://www.shufersal.co.il/online/he/",
        "fetched_at": run_ts,
        "tools": ["requests", "beautifulsoup4"],
        "block_status": "unblocked",
    },
    "products": products_list,
}

output_path = OUTPUT_DIR / "bsip0_shufersal_frozen_vegetables_raw.json"
output_path.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Scrape log ──────────────────────────────────────────────────────────
log_path = SCRAPE_DIR / "scrape_log.json"
log_data = {
    "run_id": "shufersal_frozen_vegetables_scrape_001",
    "run_ts": run_ts,
    "products_discovered": len(products),
    "scope_in": len(scope_in),
    "scope_out": len(scope_out),
    "product_pages_attempted": len(scope_in),
    "product_pages_success": stats["success"],
    "product_pages_failed": stats["failed"],
    "missing_nutrition": stats["missing_nutrition"],
    "missing_ingredients": stats["missing_ingredients"],
    "artifacts": {
        "search_html": len(list(SEARCH_DIR.glob("*.html"))),
        "category_html": len(list(CATEGORY_DIR.glob("*.html"))),
        "product_html": len(list(PRODUCT_DIR.glob("*.html"))),
    },
}
log_path.write_text(json.dumps(log_data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Summary ─────────────────────────────────────────────────────────────
log("=" * 60)
log("SCRAPE COMPLETE")
log("=" * 60)
log(f"Raw artifacts root: {SCRAPE_DIR}")
log(f"BSIP0 output: {output_path}")
log(f"Products in scope: {len(products_list)}")
for k, v in bsip0["completeness"].items():
    log(f"  {k}: {v}/{len(products_list)}")
log(f"Scope excluded: {len(scope_out)}")
log(f"Scrape log: {log_path}")
log("=" * 60)
