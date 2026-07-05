"""
BSIP0 Shufersal — Rice/corn/buckwheat cake ("פריכיות") scraper (TASK-516).

Purpose: acquire the פריכיות (puffed rice/corn/buckwheat cake, "rice cake")
corpus the owner asked to fold into the EXISTING crackers shelf as a same-
page expansion (not a new category page). Modelled directly on the proven
shufersal_cookies_coffee/01_scrape_cookies_coffee.py pattern (ld+json brand
extraction, raw_store banking, shared nutrition parser) so this corpus does
NOT repeat the crackers corpus's brand-field gap (see brand_extractor.py /
fetch_brand_patch.py for that root cause).

Category scope (Crackers Category Constitution v1, Section 1.1):
  IN by name: פריכיות אורז / פריכיות תירס / פריכיות כוסמת (rice / corn /
  buckwheat puffed cakes) and their line extensions (mini, flavored,
  multigrain, +quinoa/teff, low-sodium, organic, chocolate-coated).
  Constitution flags a Rule-5 boundary test at BSIP1/corpus-filter time:
  fat <2g/100g AND ingredient_count <=2 -> route to a "borderline sub-pool"
  rather than silently merging into the main cracker cluster. This scraper
  does NOT make that admission call -- it acquires the raw candidate set;
  corpus-filter (a separate, Product/Nutrition-reviewed step) applies the
  boundary rule.

Excluded at scrape time (name-based; corpus-filter re-checks):
  - Plain rice/rice dishes (אורז בסמטי, אורז יסמין, אורז לבן, etc. -- a
    completely different product, matched by the same "אורז" substring)
  - Rice/corn snack bars or energy bars using "פריכיות" in a compound name
    but structurally a bar (פריכיות אנרגי, פריכיות תחתית שוקולד as a bar base)
  - Rice chips (צ'יפס אורז) -- different format (fried/extruded chip, not a
    flat cake)
  - Instant soup / noodle products that happen to contain "תירס" (corn)

OFF BAN (absolute, project-wide): the ONLY source for ingredients,
nutrition, names, images, brand, and barcodes is the DIRECT Shufersal
scrape. If a field is not in the scrape, it is NULL.

Outputs:
  - Raw HTML: 03_operations/bsip0/raw_store/shufersal/ricecakes/<code>/<ts>.html
  - Manifest: 03_operations/bsip0/raw_store/shufersal/ricecakes/manifest.jsonl
  - BSIP0 JSON: 02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_<ts>.json
  - Log: 02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_log_<ts>.txt
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

_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPT_DIR.parent / "_shared"
_STORE_DIR = _SCRIPT_DIR.parent.parent / "raw_store"

sys.path.insert(0, str(_SHARED_DIR))
sys.path.insert(0, str(_STORE_DIR))

from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list,
    extract_nutrition_raw,
    composition_nutrition_report,
)
from store import store_page  # noqa: E402

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
MAX_PRODUCTS = 150
MAX_PAGES = 4
PRODUCT_PAGE_DELAY = 0.7

RETAILER = "shufersal"
CATEGORY = "ricecakes"

QUERY_PLAN: list[str] = [
    "פריכיות",
    "פריכיות אורז",
    "פריכיות תירס",
    "פריכיות כוסמת",
    "פריכיות דקות",
    "פריכיות אורז מלא",
    "פריכיות אנרגי",
    "פריכיות טף",
    "פריכית אורז",
]

# Category browse fallback (Shufersal aisle codes; best-effort, graceful on 404)
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A2508?pageSize={PAGE_SIZE}", "A2508_sweet_snacks"),
]

# EXCLUDE — a candidate whose name matches one of these is NOT a rice cake
EXCLUDE_SIGNALS = [
    "בסמטי", "יסמין", "אדום", "לבן", "פרסי", "תאילנדי", "עגול", "סושי",
    "מיקס קלאסי", "הודי",  # plain rice varieties, not puffed cakes
    "צ'יפס", "chips",       # rice chips, different format
    "נודלס", "נמס", "מרק", "מבושל בואקום",  # noodle/soup/cooked-rice products
    "שמן",                  # corn oil etc.
    "אנרגי",                # energy-bar formats using "פריכיות" loosely
    "תחתית שוקולד",         # chocolate-bar-base products
    "בימבם",                # different snack (puffed corn snack, not a flat cake)
]

INCLUDE_SIGNALS = [
    "פריכי", "פרכי",  # covers פריכיות + the "פרכיות" typo variant seen live
]


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in ["maintenance", "אתר בתחזוקה", "בתחזוקה"])


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
                if 20 < val < 3000:
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
    return any(sig in name for sig in EXCLUDE_SIGNALS)


def _looks_like_ricecake(name: str) -> bool:
    return any(sig in name for sig in INCLUDE_SIGNALS)


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
        if not _looks_like_ricecake(name):
            continue
        if _is_excluded(name):
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


def _parse_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None

    try:
        store_page(
            content=r.content,
            retailer=RETAILER,
            category=CATEGORY,
            page_id=code,
            url=r.url,
            barcode_hint="",
            http_status=r.status_code,
            fetch_engine="requests",
        )
    except Exception as exc:
        print(f"  [raw_store WARN] could not bank {code}: {exc}", flush=True)

    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    ld_name, ld_gtin, ld_images, ld_brand = "", "", [], ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", "")) or ld.get("sku", "")
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
    page_text = soup.get_text(separator=" ", strip=True)
    sm = re.search(r"מנה(?:\s*מומלצת)?\s*[:\-]?\s*(\d{1,3})\s*(?:גרם|גר|g)", page_text)
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
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1500]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{10,})", text)
            if m:
                ingredients_raw = m.group(1)[:1500]
                break

    claims_raw = ""
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in [
            "דל סוכר", "ללא סוכר", "מופחת סוכר", "light", "דל שומן", "דל נתרן",
            "ללא גלוטן", "gluten free", "טבעי", "אורגני", "organic",
            "טבעוני", "vegan", "מקמח מלא", "whole grain", "חלבון",
            "ללא חומרים", "ללא תוספת", "ללא מלח", "כשל\"פ", "כשל\"מ",
        ]):
            claims_raw += " " + text[:200]

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or code.replace("P_", "")
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
        "subcategory_raw": "ricecakes",
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
        "off_source_used": False,
    }


def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    log("=== Phase 1: Search queries ===")
    for query in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        new_total = 0
        for page in range(MAX_PAGES):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    seen_codes.add(code)
                    code_meta[code] = {**item, "query": query, "tier": "search"}
                    new_page += 1
            new_total += new_page
            log(f"  '{query}' page {page}: {len(items)} candidate items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.4)
        log(f"  '{query}' total new: {new_total}")

    log(f"\n=== Phase 2: Category browsing ({len(seen_codes)} so far) ===")
    for base_url, cat_id in CATEGORY_URLS:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        cat_new = 0
        for page in range(MAX_PAGES):
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
            log(f"  {cat_id} page {page}: {len(items)} candidate items, {new_page} new (total {len(seen_codes)})")
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
            if verbose and i % 10 == 0 and i > 0:
                print(f"  [{i}/{len(codes_to_fetch)}] fetched {len(products)} OK", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    log(f"\nProduct pages: {len(products)} OK, {failed} failed")
    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_img = sum(1 for p in products if p["image_urls"])
    n_brand = sum(1 for p in products if p["brand"])
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, "
        f"{n_ingr}/{len(products)} ingredients, "
        f"{n_img}/{len(products)} images, "
        f"{n_brand}/{len(products)} brand")

    off_count = sum(1 for p in products if p.get("off_source_used"))
    log(f"OFF ban check: {off_count} products with off_source_used=True (MUST be 0)")
    if off_count > 0:
        raise RuntimeError(f"OFF ban violation: {off_count} products have off_source_used=True")

    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\crackers\bsip0_ricecakes")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"ricecakes_bsip0_raw_{ts}.json"
    log_path = out_dir / f"ricecakes_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_brand = sum(1 for p in products if p["brand"])

    print("\n--- BSIP0 Composition Gate ---")
    print(f"Products:      {len(products)}")
    print(f"Nutrition:     {n_nutr}/{len(products)}")
    print(f"Ingredients:   {n_ingr}/{len(products)}")
    print(f"Brand:         {n_brand}/{len(products)}")

    rep = composition_nutrition_report(products)
    status = "PASS" if rep["passed"] else "FAIL"
    print(f"Plausibility:  {rep['total']-rep['implausible']}/{rep['total']} plausible "
          f"({rep['implausible_pct']}% implausible) [{status}]")
    for nm, why in rep["examples"]:
        print(f"   ! {nm}: {why}")

    off_count = sum(1 for p in products if p.get("off_source_used"))
    print(f"OFF ban check: {off_count}/0 violations (MUST be 0)")

    from store import page_count
    banked = page_count(RETAILER, CATEGORY)
    print(f"Raw-store banked: {banked} pages at 03_operations/bsip0/raw_store/{RETAILER}/{CATEGORY}/")

    return products


if __name__ == "__main__":
    main()
