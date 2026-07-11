"""
BSIP0 Shufersal -- Functional/High-Protein Dairy Drinks scraper (TASK-492B).

Purpose: EVIDENCE-GATHERING ONLY for the functional-dose-ingredient blog table.
  Not a category corpus build. No BSIP1 enrichment, no BSIP2 scoring. Governed by
  01_framework/nutrition/functional_dose_ingredient_ruling_v1.md Section 3.1 (the
  required field list) and Section 3.2 (dose-honesty bands).

Named trigger product: Tnuva GO (creatine-added high-protein dairy drink).
Scope: Israeli high-protein / functional dairy DRINKS (milk-based protein drinks,
  not yogurt, not cottage, not plain milk) -- the shelf Tnuva GO actually competes on.

Source-selection policy (scrape_source_selection_policy): never default to one
  retailer. Shufersal primary (reachable via requests). Victory/Yochananof attempted
  for cross-check where reachable. OFF is NEVER used (project-wide ban).

Extra extraction beyond the standard macro parser (bsip0_nutrition.py handles
  energy/protein/carbs/fat/fiber/sodium/sugar): a CREATINE-SPECIFIC extractor that
  scans full page text (ingredients + any "functional info" / marketing panel) for
  the word "קריאטין" (creatine) and tries to capture an adjacent per-serving mg
  figure. Per the ruling's missing-data discard rule: if no mg figure is found next
  to the word, dose is left NULL/"undisclosed" -- never assumed.

Output: C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal_functional_dairy\\
  functional_dairy_bsip0_raw_<ts>.json + log
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
MAX_PRODUCTS = 80
MAX_PAGES = 3
PRODUCT_PAGE_DELAY = 0.6

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw  # noqa: E402

# Query plan -- named trigger first, then the functional/high-protein dairy-drink shelf.
QUERY_PLAN: list[tuple[str, str]] = [
    ("טנובה גו",              "trigger"),      # Tnuva GO -- named trigger product
    ("משקה חלבון",            "mainstream"),   # "protein drink"
    ("חלב עתיר חלבון",        "mainstream"),   # "high-protein milk"
    ("יוגורט לשתייה חלבון",   "mainstream"),   # drinkable high-protein yogurt-adjacent
    ("קריאטין משקה",          "mainstream"),   # "creatine drink" direct
    ("משקה חלבי חלבון",       "mainstream"),
    ("יוטבתה חלבון",          "specialty"),    # Yotvata protein line
    ("תרו חלבון",             "specialty"),    # Tara protein line
    ("שטראוס חלבון משקה",     "specialty"),    # Strauss protein drink
]

# Exclude signals -- keep this a DRINK shelf, not yogurt cups/cottage/plain milk/bars.
EXCLUDE_SIGNALS = [
    "חטיף", "בר חלבון", "protein bar", "גבינה", "קוטג", "יוגורט יווני בקערה",
    "גביע", "תוסף תזונה", "כמוסות", "אבקת חלבון",  # powder tubs are supplement-lane, not this shelf
]

INCLUDE_SIGNALS = [
    "משקה", "drink", "לשתייה", "גו ", " go", "חלבון", "protein", "קריאטין", "creatine",
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
        re.compile(r"(\d[\d,.]*)\s*מ\"?ל", re.IGNORECASE),   # ml (drinks are usually ml)
        re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*ml\b", re.IGNORECASE),
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


def _price_per_100(price_str: str, weight_g: float | None) -> float | None:
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


def _looks_relevant(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


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
        price = d.get("data-product-price", "")
        weight_g = _extract_weight_g(name)
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": price,
            "weight_g": weight_g,
            "price_per_100": _price_per_100(price, weight_g),
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


# ── Creatine-specific extraction (NOT a standard macro; ruling S3.1) ────────────

_CREATINE_TOKENS = ("קריאטין", "creatine")
_MG_NEAR_RE = re.compile(
    r"(\d[\d.,]*)\s*(?:מ\"?ג|mg)\b", re.IGNORECASE
)
_FORM_TOKENS = {
    "מונוהידרט": "monohydrate", "monohydrate": "monohydrate",
    "hcl": "hcl", "הידרוכלוריד": "hcl",
    "buffered": "buffered", "מאוגן": "buffered",
}


def _extract_creatine_evidence(page_text: str, ingredients_raw: str) -> dict:
    """Scan full page text + ingredients for a creatine mention and try to find an
    adjacent per-serving mg figure. Missing-data discard rule: no figure found near
    the word => dose stays NULL/'undisclosed', never assumed."""
    out = {
        "creatine_mentioned": False,
        "creatine_mg_per_serving": None,
        "creatine_form": None,
        "creatine_context_snippet": "",
        "named_or_blended": None,  # "named_quantified" | "blend_no_split" | None
    }
    combined = f"{page_text} {ingredients_raw}"
    if not any(tok in combined for tok in _CREATINE_TOKENS):
        return out
    out["creatine_mentioned"] = True

    # Find all occurrences, capture a window around each for mg search + snippet.
    best_snippet = ""
    mg_found = None
    for tok in _CREATINE_TOKENS:
        for m in re.finditer(re.escape(tok), combined, re.IGNORECASE):
            start = max(0, m.start() - 80)
            end = min(len(combined), m.end() + 80)
            window = combined[start:end]
            if not best_snippet:
                best_snippet = window.strip()
            mg_m = _MG_NEAR_RE.search(window)
            if mg_m and mg_found is None:
                try:
                    mg_found = float(mg_m.group(1).replace(",", "."))
                except ValueError:
                    pass
            for tok_form, form_name in _FORM_TOKENS.items():
                if tok_form in window.lower() or tok_form in window:
                    out["creatine_form"] = form_name

    out["creatine_context_snippet"] = best_snippet[:300]
    out["creatine_mg_per_serving"] = mg_found  # None if not found -- NEVER assumed

    # named/quantified vs blend: if an mg figure sits in the same window as the word,
    # treat as named+quantified; else if word appears inside a "בלנד"/"תערובת"/
    # "functional blend" context, flag as blend with no split.
    if mg_found is not None:
        out["named_or_blended"] = "named_quantified"
    elif any(b in best_snippet for b in ("בלנד", "תערובת", "blend", "מיוחדת")):
        out["named_or_blended"] = "blend_no_split"
    else:
        out["named_or_blended"] = "named_no_dose"  # named on label, no mg disclosed anywhere on page

    return out


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

    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    page_text = soup.get_text(separator=" ", strip=True)

    # Serving size (ruling S3.1: serving_size_g_or_ml)
    serving_g = None
    sm = re.search(r"מנה(?:\s*מומלצת)?\s*[:\-]?\s*(\d{1,4})\s*(?:מ\"?ל|גרם|גר|ml|g)\b", page_text)
    if sm:
        try:
            serving_g = float(sm.group(1))
        except ValueError:
            serving_g = None

    # Servings per container / per day (ruling S3.1)
    servings_per_container = None
    spc_m = re.search(r"(\d{1,3})\s*מנות\s*(?:במיכל|באריזה|בבקבוק)?", page_text)
    if spc_m:
        try:
            servings_per_container = float(spc_m.group(1))
        except ValueError:
            pass
    servings_per_day = None
    spd_m = re.search(r"(\d{1,2})\s*מנות?\s*(?:ליום|מומלצות ליום|בכל יום)", page_text)
    if spd_m:
        try:
            servings_per_day = float(spd_m.group(1))
        except ValueError:
            pass

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
                ingredients_raw = m.group(1).strip()[:1500]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:1500]
                break

    creatine_evidence = _extract_creatine_evidence(page_text, ingredients_raw)

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id": "shufersal",
        "retailer_name": "שופרסל",
        "source_url": product_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "brand": ld_brand,
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "functional_high_protein_dairy_drink",
        "serving_size_g_or_ml": serving_g,
        "servings_per_container": servings_per_container,
        "servings_per_day_stated": servings_per_day,
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
        "creatine_evidence": creatine_evidence,
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "price_per_100": _price_per_100(meta.get("price", ""), weight_g),
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

    log("=== Phase 1: Search queries (Shufersal) ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            log(f"  Cap {MAX_PRODUCTS} reached -- skipping remaining queries")
            break
        new_total = 0
        for page in range(MAX_PAGES):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results -- stopping")
                break
            new_page = 0
            for item in items:
                name = item["name"]
                if not _looks_relevant(name) and tier != "trigger":
                    continue
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

    log(f"\nTotal unique product codes: {len(seen_codes)}")

    log("\n=== Phase 2: Product page fetching ===")
    products: list[dict] = []
    failed = 0
    codes_to_fetch = list(seen_codes)[:MAX_PRODUCTS]
    for i, code in enumerate(codes_to_fetch):
        p = _parse_product_page(code, code_meta.get(code, {}))
        if p:
            products.append(p)
            if verbose:
                ce = p["creatine_evidence"]
                flag = "CREATINE" if ce["creatine_mentioned"] else "-"
                print(f"  [{i+1}/{len(codes_to_fetch)}] {p['name_he'][:50]!r} [{flag}]", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    log(f"\nProduct pages: {len(products)} OK, {failed} failed")
    n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["protein_raw"])
    n_ingr = sum(1 for p in products if p["ingredients_raw"])
    n_creatine = sum(1 for p in products if p["creatine_evidence"]["creatine_mentioned"])
    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, "
        f"{n_creatine}/{len(products)} mention creatine")
    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_functional_dairy")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"functional_dairy_bsip0_raw_{ts}.json"
    log_path = out_dir / f"functional_dairy_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products: {len(products)}")
    print(f"Raw JSON: {raw_path}")
    return products, raw_path


if __name__ == "__main__":
    main()
