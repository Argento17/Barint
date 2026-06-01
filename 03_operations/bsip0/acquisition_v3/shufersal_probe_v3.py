"""
Shufersal probe v3 — BSIP0 acquisition for bread_retail_003.

Design goal: representative supermarket shelf, NOT a healthy bread universe.
- Mainstream-first query ordering
- Up to 5 pages per query (SAP Hybris 0-indexed pagination)
- Category traversal: A1005, A1015, A1008, A1014
- Explicit brand searches: ברמן, וונדר, אנג'ל, דגנית
- Price tracking: data-product-price + weight from name → price_per_100g
- Hard cap 300 unique products; specialty queries skipped when cap reached

Output: list of raw product dicts (same schema as v2 raw BSIP0 JSON)
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
MAX_PRODUCTS = 300
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 2
PRODUCT_PAGE_DELAY = 0.9

NUTR_LABEL_MAP = {
    "אנרגיה": "energy",
    "קל":     "energy",
    "kcal":   "energy",
    "חלבונים": "protein",
    "חלבון":   "protein",
    "פחמימות": "carbs",
    "שומנים":  "fat",
    "שומן":    "fat",
    "סיבים תזונתיים": "fiber",
    "סיבים":  "fiber",
    "נתרן":   "sodium",
    "סוכרים": "sugar",
}

# Query tiers — mainstream first, specialty limited to 2 pages
QUERY_PLAN: list[tuple[str, str]] = [
    # (query, tier)
    ("לחם",          "mainstream"),
    ("לחם לבן",      "mainstream"),
    ("לחם פרוס",     "mainstream"),
    ("לחם אחיד",     "mainstream"),
    ("טוסט",         "mainstream"),
    ("פיתה",         "mainstream"),
    ("לאפה",         "mainstream"),
    ("חלה",          "mainstream"),
    ("לחם קל",       "mainstream"),
    ("לחם מלא",      "mainstream"),
    ("בגט",          "mainstream"),
    ("לחם שחור",     "mainstream"),
    # brand searches
    ("ברמן",         "brand"),
    ("וונדר",        "brand"),
    ("אנג'ל",        "brand"),
    ("דגנית",        "brand"),
    # crackers — cap at mainstream pages
    ("קרקר",         "mainstream"),
    # specialty — 2 pages only
    ("שיפון",        "specialty"),
    ("כוסמין",       "specialty"),
]

# Shufersal category codes for bread/bakery
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A1015?pageSize={PAGE_SIZE}", "A1015_bread"),
    (f"{BASE}/online/he/c/A1005?pageSize={PAGE_SIZE}", "A1005_bread_biscuits"),
    (f"{BASE}/online/he/c/A1008?pageSize={PAGE_SIZE}", "A1008_rolls"),
    (f"{BASE}/online/he/c/A1014?pageSize={PAGE_SIZE}", "A1014_pita_flatbread"),
]

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]


# ──────────────────────────────────────────────────────────────────────────────
# Weight extraction — parses product name to get g/ml weight for price/100g
# ──────────────────────────────────────────────────────────────────────────────

_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),   # kg → multiply by 1000
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE), # g
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*מ[\"']?ל", re.IGNORECASE),   # ml (treat as g)
]


def _extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):  # kg
                    val *= 1000
                if 10 < val < 5000:  # sanity: 10g–5kg
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


# ──────────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────────────────────────────────────

def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Search / category page parsing
# ──────────────────────────────────────────────────────────────────────────────

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
        is_food = d.get("data-food", "false").lower() == "true"
        if not is_food:
            continue
        cats = d.get("data-all-categories", "")
        price = d.get("data-product-price", "")
        weight_g = _extract_weight_g(name)
        results.append({
            "name": name,
            "code": code,
            "categories": cats,
            "price": price,
            "weight_g": weight_g,
            "price_per_100g": _price_per_100g(price, weight_g),
        })
    return results


def _search_query(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search"
        f"?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}"
        f"&currentPage={page}"
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


# ──────────────────────────────────────────────────────────────────────────────
# Product page parsing
# ──────────────────────────────────────────────────────────────────────────────

def _parse_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    ld_name, ld_sku, ld_gtin, ld_images = "", "", "", []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    nutr_raw: dict[str, str] = {}
    nutr_div = soup.find("div", class_="nutritionList")
    if nutr_div:
        for item in nutr_div.find_all("div", class_="nutritionItem"):
            divs = item.find_all("div")
            parts = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
            if len(parts) >= 2:
                value = parts[0]
                label = parts[-1]
                for he_label, field in NUTR_LABEL_MAP.items():
                    if he_label in label:
                        nutr_raw[field] = value
                        break

    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:800]

    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:800]
                break

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
        "brand": "",
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "",
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw": nutr_raw.get("protein", ""),
            "carbs_raw": nutr_raw.get("carbs", ""),
            "fat_raw": nutr_raw.get("fat", ""),
            "fiber_raw": nutr_raw.get("fiber", ""),
            "sodium_raw": nutr_raw.get("sodium", ""),
            "sugar_raw": nutr_raw.get("sugar", ""),
        },
        "ingredients_raw": ingredients_raw,
        "ingredients_language": "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else "",
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": "high" if nutr_raw else "medium",
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "price_per_100g": _price_per_100g(meta.get("price", ""), weight_g),
        "acquisition_query": meta.get("query", ""),
        "acquisition_tier": meta.get("tier", ""),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main acquisition
# ──────────────────────────────────────────────────────────────────────────────

def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    """
    Returns (products, notes) where products is a list of raw product dicts
    ready for BSIP1 normalization.
    """
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    # ── Phase 1: search queries ────────────────────────────────────────────────
    log("=== Phase 1: Search queries ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            log(f"  Cap {MAX_PRODUCTS} reached — skipping remaining queries")
            break
        max_pages = MAX_PAGES_MAINSTREAM if tier in ("mainstream", "brand") else MAX_PAGES_SPECIALTY
        new_total = 0
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results — stopping pagination")
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
                break  # no new products on this page
            sleep(0.3)
        log(f"  '{query}' total new: {new_total}")

    # ── Phase 2: category browsing ─────────────────────────────────────────────
    log(f"\n=== Phase 2: Category browsing ({len(seen_codes)} products so far) ===")
    for base_url, cat_id in CATEGORY_URLS:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        cat_new = 0
        for page in range(MAX_PAGES_MAINSTREAM):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _category_page(base_url, page)
            if not items:
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

    # ── Phase 3: fetch product pages ───────────────────────────────────────────
    log(f"\n=== Phase 3: Product page fetching (up to {MAX_PRODUCTS}) ===")
    products: list[dict] = []
    failed = 0
    codes_to_fetch = list(seen_codes)[:MAX_PRODUCTS]

    for i, code in enumerate(codes_to_fetch):
        p = _parse_product_page(code, code_meta.get(code, {}))
        if p:
            products.append(p)
            if verbose and i % 20 == 0 and i > 0:
                print(f"  [{i}/{len(codes_to_fetch)}] fetched {len(products)} products", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    log(f"\nProduct pages: {len(products)} OK, {failed} failed")

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_price = sum(1 for p in products if p["price_per_100g"])
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, {n_price}/{len(products)} price/100g")

    return products, notes


if __name__ == "__main__":
    products, notes = run_acquisition(verbose=True)
    print(f"\nDone: {len(products)} products")
    for p in products[:5]:
        print(f"  {p['name_he']} | barcode={p['barcode']} | fiber={p['nutrition']['fiber_raw']} | price_per_100g={p['price_per_100g']}")
