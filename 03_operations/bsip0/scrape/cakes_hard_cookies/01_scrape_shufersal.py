"""
BSIP0 Shufersal — Cakes + Hard Cookies (run_cakes_001 / TASK-283, factory run #8).

Owner directive (offline, full autonomy 2026-06-14): a NEW category = cakes (incl.
supermarket own-brand bakery cakes) + hard cookies (chocolate-chip type). TWO retail
sources — this is Retailer #1 (Shufersal); 01_scrape_yohananof.py is Retailer #2.

OFF BAN: absolute. Identity (barcode/name/brand/price) + nutrition + ingredients come
ONLY from the direct Shufersal product page. If a panel is absent (loose/in-store bakery
items often have none), the field stays empty/NULL — never an OFF or invented panel.

Architecture mirrors the proven shufersal_cheese/01_scrape_cheese.py path (search +
category browse -> product page -> ld+json + parse_nutrition_list + ingredients).
Output: 02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_{ts}.json
Broad scrape -> narrowed later at corpus-filter (the cookies-run playbook).
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
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

PAGE_SIZE = 48
MAX_PRODUCTS = 220
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 2
PRODUCT_PAGE_DELAY = 0.6

OUT_DIR = Path(r"C:\Bari\02_products\cakes_hard_cookies\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list, extract_nutrition_raw,
)

# ── Query plan — cakes + hard cookies, mainstream-first ─────────────────────────
QUERY_PLAN: list[tuple[str, str]] = [
    ("עוגה",               "mainstream"),
    ("עוגת שוקולד",        "mainstream"),
    ("עוגת שמרים",         "mainstream"),
    ("עוגת מאפין",         "mainstream"),
    ("עוגת גבינה",         "mainstream"),
    ("קוקיס",              "mainstream"),
    ("עוגיות שוקולד צ'יפס", "mainstream"),
    ("עוגיות",             "mainstream"),
    # specialty / brand & format anchors
    ("עוגת סבתא",          "specialty"),
    ("עוגת דבש",           "specialty"),
    ("עוגת פס",            "specialty"),
    ("עוגת היער השחור",    "specialty"),
    ("קראנץ",              "specialty"),
    ("שטרודל",             "specialty"),
    ("לה פוזואלוס",        "specialty"),
    ("שלונסקי עוגה",       "specialty"),
    ("עוגיות שבבי שוקולד", "specialty"),
    ("ביסקוויט",           "specialty"),
]

CATEGORY_URLS: list[tuple[str, str]] = []  # search-driven; category codes optional

# Hard cookie + cake INCLUDE gate (broad — corpus-filter narrows later)
INCLUDE_SIGNALS = [
    "עוגה", "עוגת", "עוגות", "cake",
    "קוקיס", "cookie", "עוגיות", "עוגיה", "ביסקוויט", "biscuit",
    "שבבי", "שוקולד צ'יפס", "chip", "קראנץ", "שטרודל", "מאפין", "muffin",
    "סבתא", "דבש", "מרציפן", "פס שוקולד",
]
# EXCLUDE — not a cake/hard-cookie (bread, savory, wafers, rice cakes, soft-biscuit run#7 overlap kept loose)
EXCLUDE_SIGNALS = [
    "לחם", "פיתה", "חלה", "באגט", "לחמני", "טוסט", "מצה", "קרקר", "cracker",
    "פריכיות אורז", "פריכית", "rice cake", "גלידה", "ice cream", "וופל", "wafle", "ופל",
    "בורקס", "מלוח", "צ'יפס תפו", "במבה", "ביסלי", "חטיף", "תינוק", "מטרנה",
    "סוכריות", "מסטיק", "שוקולד למריחה", "ממרח", "קפה ", "תה ", "קמח", "אבקת",
    "תערובת לאפיה", "תבנית", "נרות", "קישוט עוגה", "ציפוי",
]
MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]


def _is_maintenance(content) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 25):
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _extract_weight_g(name: str):
    for pat in (re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.I),
                re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.I),
                re.compile(r"(\d[\d,.]*)\s*g\b", re.I)):
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 40 < val < 3000:
                    return val
            except ValueError:
                pass
    return None


def _price_per_100g(price_str, weight_g):
    if not price_str or not weight_g:
        return None
    try:
        return round(float(price_str.replace(",", ".")) * 100 / weight_g, 2)
    except (ValueError, ZeroDivisionError):
        return None


def _is_excluded(name: str) -> bool:
    nl = " " + name.lower() + " "
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_target(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


def _parse_product_list_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for li in soup.find_all("li", attrs={"data-product-name": True}):
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        if d.get("data-food", "false").lower() != "true":
            continue
        if _is_excluded(name) or not _looks_like_target(name):
            continue
        price = d.get("data-product-price", "")
        weight_g = _extract_weight_g(name)
        results.append({"name": name, "code": code,
                        "categories": d.get("data-all-categories", ""),
                        "price": price, "weight_g": weight_g,
                        "price_per_100g": _price_per_100g(price, weight_g)})
    return results


def _search_query(query: str, page: int = 0) -> list[dict]:
    url = (f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
           f"&pageSize={PAGE_SIZE}&currentPage={page}")
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def _parse_product_page(code: str, meta: dict):
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    ld_name = ld_sku = ld_gtin = ld_brand = ""
    ld_images = []
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

    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    serving_g = None
    sm = re.search(r"מנה(?:\s*מומלצת)?\s*[:\-]?\s*(\d{1,3})\s*(?:גרם|גר|g)",
                   soup.get_text(separator=" ", strip=True))
    if sm:
        try:
            serving_g = float(sm.group(1))
        except ValueError:
            pass

    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            m = re.search(r"רכיב[ים:]*\s*(.*)", container.get_text(separator=" ", strip=True), re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1200]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            m = re.search(r"רכיב[ים:]*\s+(.{20,})", section.get_text(separator=" ", strip=True))
            if m:
                ingredients_raw = m.group(1)[:1200]
                break

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id": "shufersal", "retailer_name": "שופרסל",
        "source_url": product_url, "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name, "name_en": "", "brand": ld_brand, "barcode": barcode,
        "category_raw": meta.get("categories", ""), "subcategory_raw": "cakes_hard_cookies",
        "serving_size_g_hint": serving_g,
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""), "protein_raw": nutr_raw.get("protein", ""),
            "carbs_raw": nutr_raw.get("carbs", ""), "fat_raw": nutr_raw.get("fat", ""),
            "fiber_raw": nutr_raw.get("fiber", ""), "sodium_raw": nutr_raw.get("sodium", ""),
            "sugar_raw": nutr_raw.get("sugar", ""), "saturated_fat_raw": nutr_raw.get("saturated_fat", ""),
        },
        "nutrition_raw_source": nutr_src,
        "ingredients_raw": ingredients_raw,
        "ingredients_language": "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else "",
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": "high" if (nutr_raw and ingredients_raw) else ("medium" if nutr_raw else "low"),
        "price": meta.get("price", ""), "weight_g": weight_g,
        "price_per_100g": _price_per_100g(meta.get("price", ""), weight_g),
        "acquisition_query": meta.get("query", ""), "acquisition_tier": meta.get("tier", ""),
    }


def run_acquisition(verbose: bool = True):
    notes, seen_codes, code_meta = [], set(), {}

    def log(msg):
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    log("=== Phase 1: Search queries (cakes + hard cookies) ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        max_pages = MAX_PAGES_MAINSTREAM if tier == "mainstream" else MAX_PAGES_SPECIALTY
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results — stop")
                break
            new_page = 0
            for item in items:
                c = item["code"]
                if c and c not in seen_codes:
                    seen_codes.add(c)
                    code_meta[c] = {**item, "query": query, "tier": tier}
                    new_page += 1
            log(f"  '{query}' p{page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)

    log(f"\nUnique codes: {len(seen_codes)}\n=== Phase 3: Product pages ===")
    products, failed = [], 0
    for i, code in enumerate(list(seen_codes)[:MAX_PRODUCTS]):
        p = _parse_product_page(code, code_meta.get(code, {}))
        if p:
            products.append(p)
            if i % 25 == 0 and i > 0:
                print(f"  [{i}] {len(products)} OK", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_img = sum(1 for p in products if p["image_urls"])
    log(f"\nProduct pages: {len(products)} OK, {failed} failed")
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, {n_img}/{len(products)} images")
    return products, notes


if __name__ == "__main__":
    products, notes = run_acquisition()
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out = OUT_DIR / f"cakes_shufersal_bsip0_raw_{ts}.json"
    out.write_text(json.dumps({
        "meta": {"retailer_id": "shufersal", "category": "cakes_hard_cookies",
                 "scraped_at": ts, "count": len(products), "off_used": False,
                 "source": "direct shufersal product pages (OFF banned)"},
        "products": products,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / f"cakes_shufersal_log_{ts}.txt").write_text("\n".join(notes), encoding="utf-8")
    print(f"\nWROTE {out}  ({len(products)} products)")
