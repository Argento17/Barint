"""
BSIP0 Shufersal — Cookies / sweet biscuits scraper (TASK-275 / P64).

Purpose: acquire a BROAD Israeli cookie/biscuit corpus from Shufersal product pages:
  Hebrew names + ingredient panels + nutrition + gtin13 barcodes.
  Factory run #7 — broad radius at BSIP0; narrowing to "coffee cookie" shelf
  happens downstream at corpus-filter.

Category scope (broad sweet biscuits/cookies):
  - עוגיות / ביסקוויט / פתי בר / מארי / לוטוס / שורטברד / דייג'סטיב / ביסקוטי
  - Specialty: speculoos, tea biscuits, whole-grain, almond, vegan, organic

Excluded at scrape time (name-based; corpus-filter re-checks):
  - Crackers/savory, cakes/pastry, confection bars, wafers, cereals, infant/pet

OFF BAN (absolute, project-wide, TASK-238):
  The ONLY source for ingredients, nutrition, names, images, and barcodes is the
  DIRECT Shufersal scrape. If a field is not in the scrape, it is NULL — not filled
  from Open Food Facts or any other external source.

Architecture: mirrors shufersal_brined_cheeses/01_scrape_brined_cheeses.py (proven path).
  Integrates with raw_store (store.py) so raw HTML is banked alongside the
  parsed BSIP0 JSON for offline replay of any future parser fix.

Outputs:
  - Raw HTML: 03_operations/bsip0/raw_store/shufersal/cookies_coffee/<code>/<ts>.html
  - Manifest: 03_operations/bsip0/raw_store/shufersal/cookies_coffee/manifest.jsonl
  - BSIP0 JSON: 02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_<ts>.json
  - Log: 02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_log_<ts>.txt
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

# ── Path setup ────────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPT_DIR.parent / "_shared"
_STORE_DIR = _SCRIPT_DIR.parent.parent / "raw_store"

sys.path.insert(0, str(_SHARED_DIR))
sys.path.insert(0, str(_STORE_DIR))

from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list,
    extract_nutrition_raw,
    nutrition_implausible,
    composition_nutrition_report,
)
from store import store_page  # noqa: E402

# ── Constants ─────────────────────────────────────────────────────────────────
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
MAX_PRODUCTS = 300       # broad; no pre-trimming
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 3
PRODUCT_PAGE_DELAY = 0.7  # polite crawl

RETAILER = "shufersal"
CATEGORY = "cookies_coffee"

# ── Query plan — broad cookie/biscuit radius, mainstream-first ───────────────
QUERY_PLAN: list[tuple[str, str]] = [
    ("עוגיות",                  "mainstream"),
    ("ביסקוויט",                "mainstream"),
    ("ביסקוויטים",              "mainstream"),
    ("פתי בר",                  "mainstream"),
    ("פטיבר",                   "mainstream"),
    ("מארי",                    "mainstream"),
    ("לוטוס",                   "mainstream"),
    ("עוגיות חמאה",             "mainstream"),
    ("עוגיות שוקולד צ'יפס",     "mainstream"),
    ("שורטברד",                 "mainstream"),
    ("דייג'סטיב",               "mainstream"),
    ("ביסקוטי",                 "mainstream"),
    ("lotus",                   "specialty"),
    ("biscoff",                 "specialty"),
    ("speculoos",               "specialty"),
    ("עוגיות קפה",              "specialty"),
    ("עוגיות תה",               "specialty"),
    ("עוגיות מקמח מלא",         "specialty"),
    ("קנטוצ'יני",               "specialty"),
    ("עוגיות שקדים",            "specialty"),
    ("מקרון",                   "specialty"),
    ("עוגיות טבעוניות",         "specialty"),
    ("עוגיות אורגניות",         "specialty"),
    ("שופרסל עוגיות",           "specialty"),
]

# Shufersal sweet-biscuit aisle codes (best-effort; graceful on 404)
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A2508?pageSize={PAGE_SIZE}", "A2508_sweet_snacks"),
    (f"{BASE}/online/he/c/A250804?pageSize={PAGE_SIZE}", "A250804_packaged_cookies"),
    (f"{BASE}/online/he/c/A250801?pageSize={PAGE_SIZE}", "A250801_biscuits"),
]

# ── EXCLUDE signals — clearly NOT a cookie/biscuit candidate ─────────────────
# NOTE: שוקולד/chocolate handled conditionally in _is_excluded.
EXCLUDE_SIGNALS = [
    "קרקר", "cracker", "מצות", "מצה", "פריכיות", "אורז", "מלוח", "קרוטון",
    "בייגלה", "במבה", "ביסלי", "צ'יפס", "chips", "מקלות",
    "עוגה", "עוגת", "cake", "מאפה", "מאפים", "רוגלך", "קרואסון", "croissant",
    "בורקס", "שטרודל", "טארט", "פאי", "מאפין", "muffin", "דונאט", "donut",
    "חטיף", "חטיפים", "bar", "ופל", "wafer", "מרשמלו", "סוכריות", "גלידה",
    "ice cream",
    "דגני בוקר", "cereal", "גרנולה", "granola", "תינוק", "baby", "כלב", "חתול",
]

# ── INCLUDE signals — must match at least one to be a cookie candidate ───────
INCLUDE_SIGNALS = [
    "עוגי", "עוגיות", "ביסקוויט", "biscuit", "פתי בר", "פטיבר", "petit",
    "מארי", "marie", "לוטוס", "lotus", "biscoff", "speculoos", "שורטברד",
    "shortbread", "דייג'סטיב", "digestive", "ביסקוטי", "biscotti",
    "קנטוצ'יני", "cookie", "cookies",
]

_CHOCOLATE_EXCLUDE_TERMS = ("שוקולד", "chocolate")

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
                if 50 < val < 3000:
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


def _has_include_cookie_term(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


def _is_excluded(name: str) -> bool:
    nl = " " + name.lower() + " "
    if any(term in nl for term in _CHOCOLATE_EXCLUDE_TERMS):
        if not _has_include_cookie_term(name):
            return True
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_cookie(name: str) -> bool:
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
        if not _looks_like_cookie(name):
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


# ── Product page fetch + parse + raw-store bank ────────────────────────────────

def _parse_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None

    # Bank raw HTML into the raw_store for offline replay
    try:
        store_page(
            content=r.content,
            retailer=RETAILER,
            category=CATEGORY,
            page_id=code,
            url=r.url,
            barcode_hint="",  # will be set after ld+json parse; we bank first
            http_status=r.status_code,
            fetch_engine="requests",
        )
    except Exception as exc:
        print(f"  [raw_store WARN] could not bank {code}: {exc}", flush=True)

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

    # Nutrition — shared parser (TASK-142A / EV-026 + EV-046 fixes)
    # Reads TOTAL fat, captures saturated separately, never lets an "of which"
    # sub-row overwrite a total macro.
    nutr_raw = parse_nutrition_list(soup)
    # Persist the raw nutrition source (rows + outer HTML) so any FUTURE parser fix
    # replays offline — an EV-029-class bug never again forces a network re-scrape.
    nutr_src = extract_nutrition_raw(soup)

    # Serving size hint — best-effort from page text
    serving_g = None
    page_text = soup.get_text(separator=" ", strip=True)
    sm = re.search(r"מנה(?:\s*מומלצת)?\s*[:\-]?\s*(\d{1,3})\s*(?:גרם|גר|g)", page_text)
    if sm:
        try:
            serving_g = float(sm.group(1))
        except ValueError:
            pass

    # Ingredients — primary path: רכיב section; fallback: li scan
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1500]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{20,})", text)
            if m:
                ingredients_raw = m.group(1)[:1500]
                break

    claims_raw = ""
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in [
            "דל סוכר", "ללא סוכר", "מופחת סוכר", "light", "דל שומן",
            "ללא גלוטן", "gluten free", "טבעי", "אורגני", "organic",
            "טבעוני", "vegan", "מקמח מלא", "whole grain", "חלבון",
            "ללא חומרים", "ללא תוספת", "speculoos", "biscoff",
        ]):
            claims_raw += " " + text[:200]

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id": RETAILER,
        "retailer_name": "שופרסל",
        "source_url": product_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": ld_brand,
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "cookies_coffee",
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
        "ingredients_language": (
            "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw)
            else ""
        ),
        "claims_raw": claims_raw.strip()[:600],
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": (
            "high" if (nutr_raw and ingredients_raw)
            else ("medium" if nutr_raw else "low")
        ),
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "price_per_100g": _price_per_100g(meta.get("price", ""), weight_g),
        "acquisition_query": meta.get("query", ""),
        "acquisition_tier": meta.get("tier", ""),
        "off_source_used": False,   # OFF ban sentinel — always False
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
            sleep(0.4)
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
            sleep(0.4)
        log(f"  {cat_id} total new: {cat_new}")

    log(f"\nTotal unique product codes discovered: {len(seen_codes)}")

    log("\n=== Phase 3: Product page fetching + raw-store banking ===")
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
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, "
        f"{n_ingr}/{len(products)} ingredients, "
        f"{n_img}/{len(products)} images, "
        f"{n_high}/{len(products)} high-confidence")

    # OFF ban audit — should always be 0
    off_count = sum(1 for p in products if p.get("off_source_used"))
    log(f"OFF ban check: {off_count} products with off_source_used=True (MUST be 0)")
    if off_count > 0:
        raise RuntimeError(f"OFF ban violation: {off_count} products have off_source_used=True")

    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\cookies_coffee\bsip0_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"cookies_coffee_bsip0_raw_{ts}.json"
    log_path = out_dir / f"cookies_coffee_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_img = sum(1 for p in products if p["image_urls"])
    n_high = sum(1 for p in products if p["extraction_confidence"] == "high")
    n_low = sum(1 for p in products if p["extraction_confidence"] == "low")

    print("\n--- BSIP0 Composition Gate ---")
    print(f"Products:      {len(products)} [need >=25]")
    print(f"Nutrition:     {n_nutr}/{len(products)} ({100*n_nutr//max(len(products),1)}%) [target >=85%]")
    print(f"Ingredients:   {n_ingr}/{len(products)} ({100*n_ingr//max(len(products),1)}%) [target >=80%]")
    print(f"Images:        {n_img}/{len(products)}")
    print(f"High-conf:     {n_high}/{len(products)}   Low-conf: {n_low}/{len(products)}")

    # Plausibility guard (TASK-142A / EV-026 + EV-046)
    rep = composition_nutrition_report(products)
    status = "PASS" if rep["passed"] else "FAIL"
    print(f"Plausibility:  {rep['total']-rep['implausible']}/{rep['total']} plausible "
          f"({rep['implausible_pct']}% implausible) [{status}; fail >=5%]")
    for nm, why in rep["examples"]:
        print(f"   ! {nm}: {why}")

    # OFF ban audit
    off_count = sum(1 for p in products if p.get("off_source_used"))
    print(f"OFF ban check: {off_count}/0 violations (MUST be 0)")

    # Print summary of raw_store banked
    from store import page_count
    banked = page_count(RETAILER, CATEGORY)
    print(f"Raw-store banked: {banked} pages at 03_operations/bsip0/raw_store/{RETAILER}/{CATEGORY}/")

    gate_pass = (
        len(products) >= 25
        and n_nutr / max(len(products), 1) >= 0.85
        and n_ingr / max(len(products), 1) >= 0.80
        and off_count == 0
    )
    print(f"Gate:          {'PASS' if gate_pass else 'FAIL (check coverage above)'}")
    return products, gate_pass


if __name__ == "__main__":
    main()
