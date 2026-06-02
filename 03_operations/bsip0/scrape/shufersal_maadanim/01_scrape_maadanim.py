"""
BSIP0 Shufersal — מעדנים (dairy desserts) scraper.

Category scope:
  - Flavored dairy desserts (מעדן חלב, מילקי-style)
  - Protein dairy desserts (מעדן חלבון)
  - Mousse / pudding dairy desserts
  - Flavored yogurt desserts (dessert-positioned, NOT plain yogurt)
  - Children's dairy desserts
  - Reduced-sugar dairy desserts
  - Cheese-based desserts (מוס גבינה, פנה קוטה)

Excluded:
  - Plain yogurt (without dessert positioning)
  - Ice cream (גלידה) — different cold-chain shelf
  - Milk (חלב) and plain dairy

Architecture: mirrors shufersal_probe_v3.py (bread_retail_003).
Output: maadanim_bsip0_raw_{timestamp}.json + audit log.
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
MAX_PRODUCTS = 200
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 2
PRODUCT_PAGE_DELAY = 0.9

# Shared BSIP0 nutrition parser (TASK-142A / EV-026 fix). Replaces the former
# NUTR_LABEL_MAP, whose substring map let trans/saturated "of which" sub-rows
# overwrite total fat (fat→0.5) and never captured saturated fat.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402

# ── Query plan ────────────────────────────────────────────────────────────────
# Tier "mainstream" = up to MAX_PAGES_MAINSTREAM pages
# Tier "specialty"  = up to MAX_PAGES_SPECIALTY pages
QUERY_PLAN: list[tuple[str, str]] = [
    # Core category terms
    ("מעדן",             "mainstream"),
    ("מעדנים",           "mainstream"),
    ("פודינג",           "mainstream"),
    ("מוס",              "mainstream"),
    ("קינוח",            "mainstream"),
    # Brand/product anchors — high recall
    ("מילקי",            "mainstream"),
    ("עדנה",             "mainstream"),
    ("יופלה",            "mainstream"),
    ("מילקי בר",         "mainstream"),
    # Protein/wellness positioning
    ("מעדן חלבון",       "mainstream"),
    ("פרוביו",           "mainstream"),
    ("High Protein",     "specialty"),
    ("מעדן פרוטאין",     "specialty"),
    # Children's
    ("מעדן ילדים",       "specialty"),
    ("קינוח ילדים",      "specialty"),
    # Reduced sugar / light
    ("מעדן ללא סוכר",    "specialty"),
    ("מעדן דיאט",        "specialty"),
    ("מעדן קל",          "specialty"),
    # Format terms
    ("קרם דסרט",         "specialty"),
    ("מוס גבינה",        "specialty"),
    ("פנה קוטה",         "specialty"),
    ("קרם ברולה",        "specialty"),
    ("פודינג חלב",       "specialty"),
    # Flavor-specific mainstream terms that surface dessert products
    ("שוקולד מעדן",      "specialty"),
    ("וניל מעדן",        "specialty"),
    ("תות מעדן",         "specialty"),
]

# Shufersal category codes for dairy desserts
# A4001 = dairy products (general), A4005 = desserts, A4006 = yogurt/cultured
# These are probed — add results from actual shufersal browsing
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A4001?pageSize={PAGE_SIZE}", "A4001_dairy"),
    (f"{BASE}/online/he/c/A4005?pageSize={PAGE_SIZE}", "A4005_dairy_desserts"),
    (f"{BASE}/online/he/c/A4003?pageSize={PAGE_SIZE}", "A4003_dairy_alt"),
    (f"{BASE}/online/he/c/A5010?pageSize={PAGE_SIZE}", "A5010_desserts"),
]

# Products to EXCLUDE (ice cream, plain dairy — collected but filtered post-scrape)
EXCLUDE_SIGNALS = [
    "גלידה", "ice cream", "שמנת מתוקה", "חמאה", "מרגרינה",
    "גבינה צהובה", "גבינה לבנה", "קוטג'", "חלב ",
    "שמנת חמוצה", "לבן", "קפיר",
]

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]

# ── Helpers ───────────────────────────────────────────────────────────────────

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
    """Return True if this product should be excluded from מעדנים corpus."""
    name_lower = name.lower()
    return any(sig.lower() in name_lower for sig in EXCLUDE_SIGNALS)


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
        is_food = d.get("data-food", "false").lower() == "true"
        if not is_food:
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


# ── Product page ──────────────────────────────────────────────────────────────

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

    # Nutrition — shared parser (TASK-142A / EV-026): reads TOTAL fat, captures
    # saturated separately, never lets an "of which" sub-row overwrite a total macro.
    nutr_raw = parse_nutrition_list(soup)
    # Persist raw nutrition source (rows + outer HTML) so any FUTURE parser fix
    # replays offline — an EV-029-class bug never again forces a network re-scrape.
    nutr_src = extract_nutrition_raw(soup)

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
                ingredients_raw = m.group(1).strip()[:1000]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:1000]
                break

    # Allergens / claims extraction
    claims_raw = ""
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in ["ללא סוכר", "דל סוכר", "פרוביוטי", "פרוביו", "חלבון", "עשיר ב"]):
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
        "brand": "",
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "maadanim",
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


# ── Main acquisition ──────────────────────────────────────────────────────────

def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    # Phase 1: Search queries
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

    # Phase 2: Category browsing
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

    # Phase 3: Fetch product pages
    log(f"\n=== Phase 3: Product page fetching ===")
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
    n_img  = sum(1 for p in products if p["image_urls"])
    n_high = sum(1 for p in products if p["extraction_confidence"] == "high")
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, {n_img}/{len(products)} images, {n_high}/{len(products)} high-confidence")

    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\maadanim")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_path = out_dir / f"maadanim_bsip0_raw_{ts}.json"
    log_path  = out_dir / f"maadanim_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)

    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print(f"\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")

    # Gate check
    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    gate_pass = len(products) >= 30 and n_nutr / max(len(products), 1) >= 0.60 and n_ingr / max(len(products), 1) >= 0.40
    print(f"\n--- Composition Gate ---")
    print(f"Products:    {len(products)} [need ≥30]")
    print(f"Nutrition:   {n_nutr}/{len(products)} ({100*n_nutr//max(len(products),1)}%) [need ≥60%]")
    print(f"Ingredients: {n_ingr}/{len(products)} ({100*n_ingr//max(len(products),1)}%) [need ≥40%]")
    print(f"Gate:        {'PASS' if gate_pass else 'FAIL — do NOT proceed to BSIP1'}")

    return products, gate_pass


if __name__ == "__main__":
    main()
