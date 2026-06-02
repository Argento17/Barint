"""
BSIP0 Shufersal — Cottage / White Cheese (Cheese Spreads) scraper (run_cheese_001).

Purpose: acquire a REAL Israeli fresh-cheese corpus from Shufersal product pages with
  Hebrew names + ingredient panels + nutrition + gtin13 barcodes — the greenfield
  real-data cycle for TASK-142 (reuses the proven run_cereals_002 / run_yogurt_003 path).

Category scope (fresh, soft, refrigerated, spreadable or curd-format white cheese):
  - Cottage (גבינת קוטג', fat tiers 3/5/9% = variants)
  - White cheese / quark (גבינה לבנה / קוורק, 3/5/9%)
  - Labaneh (לבנה, incl. oil/za'atar toppings)
  - Cream cheese / spread (גבינת שמנת / ממרח גבינה, savory flavored stays in pool)

Excluded at scrape time (name-based; BSIP1 curation re-checks):
  - Yellow / hard / semi-hard / processed-slice cheese (צהובה / קשקבל / גאודה / משולשים / פרוסות)
  - Brined / salty cheese (בולגרית / פטה / צפתית)
  - Yogurt / kefir / drinkable dairy (יוגורט / קפיר / משקה) — yogurt_system scope
  - Sweetened dessert cheese / מעדנים (מילקי / פודינג / מוס) — maadanim scope
  - Infant / toddler cheese; supplements

Architecture mirrors shufersal_cereals/01_scrape_cereals.py (proven Shufersal path).
Output: C:\\Bari\\02_products\\cheese_spreads\\bsip0_outputs\\cheese_bsip0_raw_{ts}.json + log
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

PAGE_SIZE = 48
MAX_PRODUCTS = 160
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 2
PRODUCT_PAGE_DELAY = 0.6

# Shared BSIP0 nutrition parser (TASK-142A / EV-026 fix). Replaces the former
# NUTR_LABEL_MAP, whose substring map let trans/saturated "of which" sub-rows
# overwrite total fat (fat→0.5) and never captured saturated fat.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list,
    extract_nutrition_raw,
    nutrition_implausible,
    composition_nutrition_report,
)

# ── Query plan — cheese-targeted, mainstream-first ──────────────────────────────
QUERY_PLAN: list[tuple[str, str]] = [
    ("גבינת קוטג'",        "mainstream"),
    ("גבינה לבנה",         "mainstream"),
    ("לבנה",               "mainstream"),
    ("גבינת שמנת",         "mainstream"),
    ("ממרח גבינה",         "mainstream"),
    ("קוורק",              "mainstream"),
    ("גבינה 5%",           "mainstream"),
    ("גבינה 9%",           "mainstream"),
    # brand anchors / specialty
    ("פילדלפיה",           "specialty"),
    ("נפוליאון גבינה",     "specialty"),
    ("תנובה ממרח",         "specialty"),
    ("עמק לבנה",           "specialty"),
    ("פיראוס לבנה",        "specialty"),
    ("שמנת לבישול",        "specialty"),
    ("גבינת מטבח",         "specialty"),
    ("ריקוטה",             "specialty"),
    ("מסקרפונה",           "specialty"),
    ("גבינת עזים רכה",     "specialty"),
]

# Shufersal category codes probed for fresh cheese (best-effort; graceful 404)
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A06?pageSize={PAGE_SIZE}", "A06_dairy"),
]

# Name-based EXCLUDE signals (yellow/hard/processed/brined/yogurt/dessert/infant)
EXCLUDE_SIGNALS = [
    "צהובה", "קשקבל", "גאודה", "עמק פרוס", "מוצרלה", "mozzarella", "פרמזן", "parmesan",
    "cheddar", "צ'דר", "אמנטל", "גבינה צהובה",
    "משולש", "פרוסות", "פרוס ", "slice", "מותכת", "מעובדת", "processed",
    "בולגרית", "פטה", "feta", "צפתית", "מלוחה",
    "יוגורט", "yogurt", "yoghurt", "קפיר", "kefir", "משקה", "drink", "שתיה", "שתייה",
    "מילקי", "פודינג", "מוס ", "גלידה", "ice cream", "קרמברלה", "דניאלה", "מילקה",
    "תינוק", "מטרנה", "סימילק", "תוסף", "קפסול", "אבקת",
]

# Name-based INCLUDE gate (must look like a fresh white cheese / spread)
INCLUDE_SIGNALS = [
    "קוטג'", "קוטג", "cottage", "גבינה לבנה", "גבינת לבנה", "לבנה", "labaneh", "labneh",
    "קוורק", "quark", "גבינת שמנת", "שמנת לבישול", "ממרח גבינה", "ממרח", "גבינה רכה",
    "cream cheese", "פילדלפיה", "philadelphia", "נפוליאון", "napoleon",
    "גבינה 5%", "גבינה 9%", "גבינה 3%", "גבינת מטבח", "ריקוטה", "ricotta",
    "מסקרפונה", "mascarpone", "גבינת עזים", "גבינה",
]

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _extract_weight_g(name: str) -> float | None:
    patterns = [
        re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
    ]
    for pat in patterns:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 50 < val < 2000:
                    return val
            except ValueError:
                pass
    return None


def _price_per_100g(price_str: str, weight_g: float | None) -> float | None:
    if not price_str or not weight_g:
        return None
    try:
        price = float(price_str.replace(",", "."))
        return round(price * 100 / weight_g, 2)
    except (ValueError, ZeroDivisionError):
        return None


def _is_excluded(name: str) -> bool:
    nl = " " + name.lower() + " "
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_cheese(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


# ── Page parsing ──────────────────────────────────────────────────────────────

def _parse_product_list_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    results = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        if d.get("data-food", "false").lower() != "true":
            continue
        if _is_excluded(name):
            continue
        if not _looks_like_cheese(name):
            continue
        price = d.get("data-product-price", "")
        weight_g = _extract_weight_g(name)
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": price,
            "weight_g": weight_g,
            "price_per_100g": _price_per_100g(price, weight_g),
        })
    return results


def _search_query(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def _category_page(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


# ── Product page ──────────────────────────────────────────────────────────────

def _parse_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    ld_name, ld_sku, ld_gtin, ld_images, ld_brand = "", "", "", [], ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                brand = ld.get("brand", "")
                ld_brand = brand.get("name", "") if isinstance(brand, dict) else (brand or "")
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # Nutrition — shared parser (TASK-142A / EV-026): reads TOTAL fat, captures
    # saturated separately, never lets an "of which" sub-row overwrite a total macro.
    nutr_raw = parse_nutrition_list(soup)
    # Persist the raw nutrition source (rows + outer HTML) so any FUTURE parser fix
    # replays offline — an EV-029-class bug never again forces a network re-scrape.
    nutr_src = extract_nutrition_raw(soup)

    # Serving size hint (for developmental D3 indicator) — best-effort
    serving_g = None
    page_text = soup.get_text(separator=" ", strip=True)
    sm = re.search(r"מנה(?:\s*מומלצת)?\s*[:\-]?\s*(\d{1,3})\s*(?:גרם|גר|g)", page_text)
    if sm:
        try:
            serving_g = float(sm.group(1))
        except ValueError:
            serving_g = None

    # Ingredients
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1200]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{20,})", text)
            if m:
                ingredients_raw = m.group(1)[:1200]
                break

    # Claims (fat % / light / protein / culture / no-additives / kids)
    claims_raw = ""
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in [
            "דל שומן", "מופחת שומן", "light", "לайт", "חצי שומן", "%",
            "עשיר בחלבון", "חלבון", "תרבית", "פרוביוטי", "חיידק",
            "ללא חומרים", "ללא תוספת", "טבעי", "ילדים", "אורגני", "עזים", "כבשים"]):
            claims_raw += " " + text[:200]

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id": "shufersal",
        "retailer_name": "שופרסל",
        "source_url": product_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": ld_brand,
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "cheese_spread",
        "serving_size_g_hint": serving_g,
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw": nutr_raw.get("protein", ""),
            "carbs_raw": nutr_raw.get("carbs", ""),
            "fat_raw": nutr_raw.get("fat", ""),
            "fiber_raw": nutr_raw.get("fiber", ""),
            "sodium_raw": nutr_raw.get("sodium", ""),
            "sugar_raw": nutr_raw.get("sugar", ""),
            "saturated_fat_raw": nutr_raw.get("saturated_fat", ""),
        },
        "nutrition_raw_source": nutr_src,
        "ingredients_raw": ingredients_raw,
        "ingredients_language": "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else "",
        "claims_raw": claims_raw.strip()[:500],
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": "high" if (nutr_raw and ingredients_raw) else ("medium" if nutr_raw else "low"),
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "price_per_100g": _price_per_100g(meta.get("price", ""), weight_g),
        "acquisition_query": meta.get("query", ""),
        "acquisition_tier": meta.get("tier", ""),
    }


# ── Main acquisition ──────────────────────────────────────────────────────────

def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    log("=== Phase 1: Search queries ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            log(f"  Cap {MAX_PRODUCTS} reached — skipping remaining queries")
            break
        max_pages = MAX_PAGES_MAINSTREAM if tier == "mainstream" else MAX_PAGES_SPECIALTY
        new_total = 0
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results — stopping")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    seen_codes.add(code)
                    code_meta[code] = {**item, "query": query, "tier": tier}
                    new_page += 1
            new_total += new_page
            log(f"  '{query}' page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)
        log(f"  '{query}' total new: {new_total}")

    log(f"\n=== Phase 2: Category browsing ({len(seen_codes)} so far) ===")
    for base_url, cat_id in CATEGORY_URLS:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        cat_new = 0
        for page in range(MAX_PAGES_MAINSTREAM):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _category_page(base_url, page)
            if not items:
                log(f"  {cat_id} page {page}: no results — stopping")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    seen_codes.add(code)
                    code_meta[code] = {**item, "query": f"category:{cat_id}", "tier": "category"}
                    new_page += 1
            cat_new += new_page
            log(f"  {cat_id} page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)
        log(f"  {cat_id} total new: {cat_new}")

    log(f"\nTotal unique product codes: {len(seen_codes)}")

    log("\n=== Phase 3: Product page fetching ===")
    products: list[dict] = []
    failed = 0
    codes_to_fetch = list(seen_codes)[:MAX_PRODUCTS]
    for i, code in enumerate(codes_to_fetch):
        p = _parse_product_page(code, code_meta.get(code, {}))
        if p:
            products.append(p)
            if verbose and i % 20 == 0 and i > 0:
                print(f"  [{i}/{len(codes_to_fetch)}] fetched {len(products)} OK", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    log(f"\nProduct pages: {len(products)} OK, {failed} failed")
    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_img = sum(1 for p in products if p["image_urls"])
    n_high = sum(1 for p in products if p["extraction_confidence"] == "high")
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, "
        f"{n_img}/{len(products)} images, {n_high}/{len(products)} high-confidence")
    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\cheese_spreads\bsip0_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"cheese_bsip0_raw_{ts}.json"
    log_path = out_dir / f"cheese_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    print("\n--- BSIP0 Composition Gate ---")
    print(f"Products:    {len(products)} [need >=30]")
    print(f"Nutrition:   {n_nutr}/{len(products)} ({100*n_nutr//max(len(products),1)}%) [target >=90%]")
    print(f"Ingredients: {n_ingr}/{len(products)} ({100*n_ingr//max(len(products),1)}%) [target >=90%]")

    # Plausibility guard (TASK-142A / EV-026): coverage alone is not enough — a
    # fat-overwrite parse can pass at 90%+ coverage while fat is collapsed to 0.5g.
    rep = composition_nutrition_report(products)
    status = "PASS" if rep["passed"] else "FAIL"
    print(f"Plausibility:{rep['total']-rep['implausible']}/{rep['total']} plausible "
          f"({rep['implausible_pct']}% implausible) [{status}; fail >=5%]")
    for nm, why in rep["examples"]:
        print(f"   ! {nm}: {why}")
    return products


if __name__ == "__main__":
    main()
