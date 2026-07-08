"""
BSIP0 Shufersal — Yogurt scraper, TASK-515 (yogurt category relaunch, multi-retailer).

Supersedes the run_yogurt_003 script (01_scrape_yogurt.py) for THIS run only — that
script's output/scoring history stays frozen and untouched. This is a NEW acquisition
using the same proven 3-phase engine (search -> product page -> nutrition/ingredients
parse), broadened per TASK-515 scope:

  CORE scope (mainstream spoon yogurt, same as run_yogurt_003):
    plain / Greek / bio-probiotic / high-protein / flavored spoon yogurt, kids' yogurt.

  BOUNDARY scope (owner directive 2026-07-05 — SCRAPE, TAG, DO NOT SILENTLY DECIDE):
    drinkable yogurt (יוגורט לשתייה / משקה יוגורט), kefir (קפיר), labneh (לבנה).
    These are captured via a SEPARATE query phase with a permissive gate (only true
    junk is dropped) and tagged scope_tag="boundary:<kind>". The corpus filter
    (BSIP1) — not this scraper — decides inclusion.

  Cottage cheese (קוטג'): NOT scraped here. It already has a dedicated corpus/category
    elsewhere in the pipeline. Flagged in the run summary for a Product/Nutrition
    ruling on double-listing risk; not re-litigated by this scraper.

OFF is never used. Ingredients + nutrition are direct-scrape only; unparsed = NULL.
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
MAX_PRODUCTS = 180
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 2
MAX_PAGES_BOUNDARY = 3
PRODUCT_PAGE_DELAY = 0.6

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402

# ── CORE query plan (mainstream spoon yogurt) — same anchors as run_yogurt_003 ──
QUERY_PLAN: list[tuple[str, str]] = [
    ("יוגורט",            "mainstream"),
    ("יוגורט יווני",      "mainstream"),
    ("יוגורט ביו",        "mainstream"),
    ("יוגורט טבעי",       "mainstream"),
    ("אקטיביה",           "mainstream"),
    ("יופלה",             "mainstream"),
    ("דנונה",             "mainstream"),
    ("מולר",              "mainstream"),
    ("סקיר",              "mainstream"),
    ("skyr",              "mainstream"),
    ("יוגורט פרו",        "mainstream"),
    ("יוגורט חלבון",      "specialty"),
    ("go יופלה",          "specialty"),
    ("pro 20",            "specialty"),
    ("יוגורט פירות",      "specialty"),
    ("יוגורט וניל",       "specialty"),
    ("פרופ",              "specialty"),
    ("froop",             "specialty"),
    ("תנובה יוגורט",      "specialty"),
    ("שטראוס יוגורט",     "specialty"),
    ("יוגורט לילדים",     "specialty"),   # kids' yogurt — explicit TASK-515 scope
    ("דנונינו",            "specialty"),   # kids brand anchor
    ("פטיט",              "specialty"),   # kids brand anchor
]

CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A4001?pageSize={PAGE_SIZE}", "A4001_dairy"),
    (f"{BASE}/online/he/c/A4003?pageSize={PAGE_SIZE}", "A4003_dairy_alt"),
]

# ── BOUNDARY query plan — TASK-515: scrape + tag, never silently exclude ────────
BOUNDARY_QUERY_PLAN: list[tuple[str, str]] = [
    ("יוגורט לשתייה",  "drinkable"),
    ("משקה יוגורט",     "drinkable"),
    ("יוגורט שתיה",     "drinkable"),
    ("קפיר",            "kefir"),
    ("kefir",           "kefir"),
    ("לבנה",            "labneh"),
    ("labneh",          "labneh"),
    ("labne",           "labneh"),
]

# CORE gate: name-based EXCLUDE (keeps mainstream queries from picking up
# desserts/supplements/non-yogurt dairy/boundary items — boundary items are
# captured separately via BOUNDARY_QUERY_PLAN instead).
EXCLUDE_SIGNALS = [
    "משקה", "שתיה", "שתייה", "drink", "שייק", "smoothie", "כפיר", "kefir",
    "איראן", "ayran", "לאסי", "lassi", "אקטימל", "actimel", "יקולט", "yakult",
    "דנאקטיב", "danactive", "לשתיה",
    "מעדן", "מילקי", "מוס", "פודינג", "ברולה", "פנה קוטה", "פנהקוטה",
    "קינוח", "קרם ", "דניאלה",
    "תוסף", "קפסול", "טבליות", "כמוסות",
    "גלידה", "ice cream", "חמאה", "מרגרינה", "שמנת", "גבינה צהובה",
    "גבינה לבנה", "קוטג", "לבן ", "קצפת", "לבנה",
    "זית", "זיתים", "olive",
]

INCLUDE_SIGNALS = [
    "יוגורט", "yogurt", "yoghurt", "יווני", "greek", "סקיר", "skyr",
    "אקטיביה", "activia", "ביו", "bio", "פרו ", "pro ", "go ", "froop",
    "פרופ", "מולר", "muller", "müller", "דנונינו", "פטיט",
]

# BOUNDARY gate: only drop obvious non-food / unrelated junk. Do NOT apply the
# core INCLUDE/EXCLUDE gate here — that would defeat the point of a boundary scrape.
BOUNDARY_HARD_DROP = [
    "שמפו", "סבון", "ניקוי", "מרכך", "נייר טואלט", "חיתול",
    "שוקולד מוצק", "ממתק", "חטיף", "עוגיה", "עוגייה", "waffle",
]

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]


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
        re.compile(r"(\d[\d,.]*)\s*מ[\"']?ל", re.IGNORECASE),
    ]
    for pat in patterns:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 10 < val < 5000:
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
    nl = name.lower()
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_yogurt(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


def _is_boundary_hard_drop(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in BOUNDARY_HARD_DROP)


def _parse_product_list_page(html: str, mode: str, boundary_kind: str = "") -> list[dict]:
    """mode='core' applies the strict include/exclude gate; mode='boundary' applies
    only the permissive hard-drop and tags every surviving item with boundary_kind."""
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
        if mode == "core":
            if _is_excluded(name):
                continue
            if not _looks_like_yogurt(name):
                continue
        else:  # boundary
            if _is_boundary_hard_drop(name):
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
            "scope_tag": "core" if mode == "core" else f"boundary:{boundary_kind}",
        })
    return results


def _search_query(query: str, page: int = 0, mode: str = "core", boundary_kind: str = "") -> list[dict]:
    url = (
        f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text, mode, boundary_kind)


def _category_page(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text, mode="core")


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

    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1000]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:1000]
                break

    claims_raw = ""
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in ["ללא סוכר", "דל סוכר", "פרוביוטי", "חלבון", "עשיר ב", "ללא תוספת"]):
            claims_raw += " " + text[:200]

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id": "shufersal",
        "retailer_name": "שופרסל",
        "source": "shufersal",
        "source_url": product_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": "",
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "yogurt",
        "scope_tag": meta.get("scope_tag", "core"),
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
        "claims_raw": claims_raw.strip()[:400],
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": "high" if (nutr_raw and ingredients_raw) else ("medium" if nutr_raw else "low"),
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "price_per_100g": _price_per_100g(meta.get("price", ""), weight_g),
        "acquisition_query": meta.get("query", ""),
        "acquisition_tier": meta.get("tier", ""),
    }


def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    log("=== Phase 1: CORE search queries (mainstream spoon yogurt) ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            log(f"  Cap {MAX_PRODUCTS} reached — skipping remaining queries")
            break
        max_pages = MAX_PAGES_MAINSTREAM if tier == "mainstream" else MAX_PAGES_SPECIALTY
        new_total = 0
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page, mode="core")
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

    log(f"\n=== Phase 3: BOUNDARY search queries (drinkable / kefir / labneh — tagged, not decided) ===")
    boundary_new_total = 0
    for query, kind in BOUNDARY_QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        new_q = 0
        for page in range(MAX_PAGES_BOUNDARY):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page, mode="boundary", boundary_kind=kind)
            if not items:
                log(f"  [boundary:{kind}] '{query}' page {page}: no results — stopping")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    seen_codes.add(code)
                    code_meta[code] = {**item, "query": query, "tier": f"boundary:{kind}"}
                    new_page += 1
            new_q += new_page
            log(f"  [boundary:{kind}] '{query}' page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)
        boundary_new_total += new_q
    log(f"  Boundary total new: {boundary_new_total}")

    log(f"\nTotal unique product codes: {len(seen_codes)}")

    log("\n=== Phase 4: Product page fetching ===")
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
    n_core = sum(1 for p in products if p["scope_tag"] == "core")
    n_boundary = sum(1 for p in products if p["scope_tag"].startswith("boundary"))
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, "
        f"{n_img}/{len(products)} images, {n_high}/{len(products)} high-confidence")
    log(f"Scope split: {n_core} core, {n_boundary} boundary")
    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\yogurt_system\bsip0_task515")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"shufersal_yogurt_bsip0_raw_{ts}.json"
    log_path = out_dir / f"shufersal_yogurt_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")

    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    gate_pass = (len(products) >= 30
                 and n_nutr / max(len(products), 1) >= 0.60
                 and n_ingr / max(len(products), 1) >= 0.40)
    print("\n--- BSIP0 Composition Gate ---")
    print(f"Products:    {len(products)} [need >=30]")
    print(f"Nutrition:   {n_nutr}/{len(products)} ({100*n_nutr//max(len(products),1)}%) [need >=60%]")
    print(f"Ingredients: {n_ingr}/{len(products)} ({100*n_ingr//max(len(products),1)}%) [need >=40%]")
    print(f"Gate:        {'PASS' if gate_pass else 'FAIL'}")
    return products, gate_pass, raw_path


if __name__ == "__main__":
    main()
