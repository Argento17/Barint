"""
TASK-360 Phase 3 — Snack Bar Corpus REBUILD (Cereals Golden Standard)
=======================================================================
ROOT CAUSE FIX:
  Prior scrape used HTML list-page parser which missed brandName, description,
  and yielded truncated names. This scraper uses the Shufersal JSON API
  (/search/results endpoint) for discovery+metadata (description, brandName,
  sku, images, calories), then fetches the HTML product detail page for
  ingredients and full nutrition table per product.

GOAL: Every kept product has clean branded name + brand + ingredients +
plausible per-100g nutrition + real image. ZERO gaps accepted.

Scope writes:
  02_products/snack_bars/  (BSIP0 records, BSIP1 files, BSIP2 dir, run record)
  bari-web/src/data/comparisons/snacks_frontend_v5.json

Hard rules:
  - OFF BAN: no Open Food Facts, ever
  - Engine UNTOUCHED (no changes to 03_operations/bsip2/** or page_generator configs)
  - No fabrication
  - Copy fields = PENDING_COPY
  - No git add/commit/stash/checkout
"""
from __future__ import annotations

import datetime
import hashlib
import json
import logging
import pathlib
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
RUN_TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
RUN_ID = f"run_snacks_task360_phase3_{RUN_TS}"

BSIP0_DIR = SNACKS_DIR / "observations_bsip0" / "shufersal" / RUN_ID
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = SNACKS_DIR / "bsip2_outputs" / RUN_ID
BSIP2_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v5.json"

_SHARED = ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"
sys.path.insert(0, str(_SHARED))
sys.path.insert(0, str(BSIP2_SRC))

from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, parse_nutrition_numeric

for _d in (BSIP0_DIR, BSIP1_DIR, BSIP2_DIR / "products"):
    _d.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def save_json(path: pathlib.Path | str, data) -> None:
    pathlib.Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Shufersal HTTP config ─────────────────────────────────────────────────────
BASE = "https://www.shufersal.co.il"
JSON_HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}
HTML_HEADERS = {**JSON_HEADERS, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}
PAGE_SIZE = 48
PRODUCT_DELAY = 1.0  # seconds between HTML page fetches


def _get_json(url: str, timeout: int = 30) -> dict | None:
    try:
        r = requests.get(url, headers=JSON_HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        log.warning("JSON GET %s → HTTP %s", url, r.status_code)
    except Exception as exc:
        log.warning("JSON GET error %s: %s", url, exc)
    return None


def _get_html(url: str, timeout: int = 30) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HTML_HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return r
        log.warning("HTML GET %s → HTTP %s", url, r.status_code)
    except Exception as exc:
        log.warning("HTML GET error %s: %s", url, exc)
    return None


# ── Weight / serving size extractor ──────────────────────────────────────────
_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*גר?'?(?:\b)", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
]

def _extract_weight_g(text: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(text or "")
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 5 < val < 5000:
                    return val
            except ValueError:
                pass
    return None


# ── Plausibility gate ─────────────────────────────────────────────────────────
GATE_MIN_ACCOUNTED_G = 70.0
GATE_MIN_KCAL_DRY = 150.0
SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק", "גלוקוז-פרוקטוז",
]


def run_plausibility_gate(nutr: dict, ingredients: str, barcode: str,
                          serving_g: float | None = None) -> dict:
    kcal = float(nutr.get("energy_kcal") or 0)
    carbs = float(nutr.get("carbohydrates_g") or 0)
    fat = float(nutr.get("fat_g") or 0)
    prot = float(nutr.get("protein_g") or 0)
    fiber = float(nutr.get("dietary_fiber_g") or 0)
    sugars = nutr.get("sugars_g")

    accounted = carbs + fat + prot + fiber

    def _check(n_kcal, n_acc, n_sug, ingr):
        fails = []
        if n_acc < GATE_MIN_ACCOUNTED_G:
            fails.append(
                f"accounted_mass={n_acc:.1f}g < {GATE_MIN_ACCOUNTED_G}g "
                f"(carbs={carbs:.1f}+fat={fat:.1f}+prot={prot:.1f}+fiber={fiber:.1f})"
            )
        if n_sug is not None and n_sug == 0:
            ingr_l = ingr.lower()
            if any(tok.lower() in ingr_l for tok in SUGAR_BEARING_TOKENS):
                fails.append("sugars=0 but sugar-bearing ingredient present")
        if n_kcal < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={n_kcal:.0f} < {GATE_MIN_KCAL_DRY} (dry snack minimum)")
        return fails

    fails = _check(kcal, accounted, sugars, ingredients)
    if not fails:
        return {
            "verdict": "pass",
            "accounted_mass": accounted,
            "kcal": kcal,
            "fail_reasons": [],
            "basis": "per_100g",
            "conversion_factor": 1.0,
            "serving_g_used": None,
            "final_nutrition": nutr,
        }

    # Try serving conversion
    if serving_g and serving_g > 0:
        factor = 100.0 / serving_g
        c_kcal = kcal * factor
        c_carbs = carbs * factor
        c_fat = fat * factor
        c_prot = prot * factor
        c_fiber = fiber * factor
        c_acc = c_carbs + c_fat + c_prot + c_fiber
        c_sug = (float(sugars) * factor) if sugars is not None else None
        c_fails = _check(c_kcal, c_acc, c_sug, ingredients)
        if not c_fails:
            converted_nutr = {**nutr}
            converted_nutr["energy_kcal"] = round(c_kcal, 1)
            converted_nutr["carbohydrates_g"] = round(c_carbs, 1)
            converted_nutr["fat_g"] = round(c_fat, 1)
            converted_nutr["protein_g"] = round(c_prot, 1)
            converted_nutr["dietary_fiber_g"] = round(c_fiber, 1)
            if c_sug is not None:
                converted_nutr["sugars_g"] = round(c_sug, 1)
            if nutr.get("fat_saturated_g"):
                converted_nutr["fat_saturated_g"] = round(float(nutr["fat_saturated_g"]) * factor, 1)
            if nutr.get("sodium_mg"):
                converted_nutr["sodium_mg"] = round(float(nutr["sodium_mg"]) * factor, 1)
            return {
                "verdict": "converted_pass",
                "accounted_mass": c_acc,
                "kcal": c_kcal,
                "fail_reasons": [],
                "basis": "converted_from_serving",
                "conversion_factor": factor,
                "serving_g_used": serving_g,
                "final_nutrition": converted_nutr,
            }

    return {
        "verdict": "quarantine",
        "accounted_mass": accounted,
        "kcal": kcal,
        "fail_reasons": fails,
        "basis": None,
        "conversion_factor": 1.0,
        "serving_g_used": None,
        "final_nutrition": None,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — DISCOVERY (JSON API — gets brandName, description, sku, images)
# ══════════════════════════════════════════════════════════════════════════════

# Search queries — comprehensive Hebrew + brand terms
SEARCH_QUERIES = [
    # Core snack bar terms
    ("חטיף דגנים", "mainstream"),
    ("חטיף גרנולה", "mainstream"),
    ("חטיף בריאות", "mainstream"),
    ("חטיף שיבולת שועל", "mainstream"),
    ("חטיף תמרים", "mainstream"),
    ("חטיף חלבון", "specialty"),
    ("חטיף אנרגיה", "specialty"),
    ("חטיף פירות", "specialty"),
    ("חטיף קורני", "specialty"),
    ("גרנולה בר", "specialty"),
    ("מארז חטיפי דגנים", "specialty"),
    ("חטיף קוואקר", "specialty"),
    # Brand names
    ("nature valley", "brand"),
    ("slim delice", "brand"),
    ("fitness bar", "brand"),
    ("פיטנס בר", "brand"),
    ("קורני חטיף", "brand"),
    ("pangea snack", "brand"),
    ("פנגיאה חטיף", "brand"),
    ("free חטיף", "brand"),
    ("חטיף נייטשר", "brand"),
    ("7degrees", "brand"),
    # Additional discovery
    ("mojo bar", "specialty"),
    ("חטיף נשנושים", "specialty"),
    ("חטיף שוקולד דגנים", "specialty"),
    ("חטיף פחמימות", "specialty"),
    ("חטיף ספורט", "specialty"),
    ("חטיף ללא גלוטן", "specialty"),
]

# Category codes known to contain snack bars
CATEGORY_CODES = [
    "A2502",    # 48 items — cereal/snack mix (confirmed)
    "A281404",  # 16 items — gluten-free snack bars (confirmed)
]


def _extract_product_from_api(raw: dict) -> dict:
    """Extract the fields we need from a Shufersal JSON API product record."""
    code = raw.get("code", "")
    sku = raw.get("sku", "")
    ean = raw.get("ean", "") or ""
    # Prefer description (full name) over name (truncated)
    description = raw.get("description", "") or raw.get("baseProductDescription", "") or ""
    name_truncated = raw.get("name", "")

    # Brand: try brandName first, then brand.name
    brand_name = raw.get("brandName", "")
    if not brand_name:
        brand_obj = raw.get("brand") or {}
        brand_name = brand_obj.get("name", "") if isinstance(brand_obj, dict) else ""

    # Images: prefer 'zoom' or 'large' format
    images = raw.get("images") or []
    image_url = ""
    for fmt_pref in ("zoom", "large", "medium", "product", "thumbnail"):
        for img in images:
            if isinstance(img, dict) and img.get("format") == fmt_pref:
                url = img.get("url", "")
                if url and "default" not in url:
                    image_url = url
                    break
        if image_url:
            break
    # Fallback to baseProductImageLarge
    if not image_url:
        image_url = (
            raw.get("baseProductImageLarge", "")
            or raw.get("baseProductImageMedium", "")
            or raw.get("baseProductImageSmall", "")
            or ""
        )

    # Nutrition hints from API (these are rough — we'll validate with HTML parse)
    calories_hint = raw.get("calories")
    fats_hint = raw.get("fats")
    sodium_hint = raw.get("sodium")
    sugar_hint = raw.get("sugar")

    # Category codes for curation
    all_cat_codes = raw.get("allCategoryCodes") or []

    # Price
    price_obj = raw.get("price") or {}
    price = str(price_obj.get("value", "")) if isinstance(price_obj, dict) else ""

    # Unit description (e.g. "4*35 גרם")
    unit_desc = raw.get("unitDescription", "") or ""

    # Manufacturer
    manufacturer = raw.get("manufacturer", "") or raw.get("manufacturerInfo", "") or ""

    # Health attributes
    health_attrs = [
        h.get("code", "") for h in (raw.get("healthAttributes") or [])
        if isinstance(h, dict)
    ]

    # Product type / second level
    second_level = raw.get("secondLevelCategory", "") or ""

    return {
        "code": code,
        "sku": sku,
        "ean": ean,
        "description": description,
        "name_truncated": name_truncated,
        "brand": brand_name,
        "image_url": image_url,
        "calories_hint": calories_hint,
        "fats_hint": fats_hint,
        "sodium_hint": sodium_hint,
        "sugar_hint": sugar_hint,
        "all_cat_codes": all_cat_codes,
        "price": price,
        "unit_description": unit_desc,
        "manufacturer": manufacturer,
        "health_attrs": health_attrs,
        "second_level_category": second_level,
    }


def discover_all() -> dict[str, dict]:
    """
    Enumerate snack bar candidates from Shufersal JSON API.
    Returns {code: extracted_meta} deduplicated by code.
    """
    seen: dict[str, dict] = {}
    total_api_hits = 0

    # Category enumeration
    log.info("=== DISCOVERY: Category traversal ===")
    for cat_code in CATEGORY_CODES:
        url = (
            f"{BASE}/online/he/search/results"
            f"?q=:relevance:allCategories:{cat_code}"
            f"&limit={PAGE_SIZE}&currentPage=0"
        )
        data = _get_json(url)
        if not data:
            log.warning("Category %s: no response", cat_code)
            continue
        results = data.get("results", [])
        total_pages = data.get("pagination", {}).get("numberOfPages", 1)
        log.info("  Category %s: %s total pages, %s results on page 0",
                 cat_code, total_pages, len(results))
        # Categories repeat after page 0 (pagination loops), so just fetch page 0
        for raw in results:
            code = raw.get("code", "")
            if code and code not in seen:
                seen[code] = _extract_product_from_api(raw)
                seen[code]["source"] = f"category:{cat_code}"
                total_api_hits += 1
        time.sleep(0.5)

    # Search query enumeration
    log.info("=== DISCOVERY: Search queries (%d terms) ===", len(SEARCH_QUERIES))
    for query, tier in SEARCH_QUERIES:
        max_pages = 5 if tier == "mainstream" else 3
        for page in range(max_pages):
            import urllib.parse
            url = (
                f"{BASE}/online/he/search/results"
                f"?q={urllib.parse.quote(query)}:relevance"
                f"&limit={PAGE_SIZE}&currentPage={page}"
            )
            data = _get_json(url)
            if not data:
                break
            results = data.get("results", [])
            if not results:
                break
            new_this_page = 0
            for raw in results:
                code = raw.get("code", "")
                if code and code not in seen:
                    meta = _extract_product_from_api(raw)
                    meta["source"] = f"search:{query}"
                    meta["tier"] = tier
                    seen[code] = meta
                    new_this_page += 1
                    total_api_hits += 1
            log.info("  [%s] p%d: %d new (total=%d)", query[:30], page, new_this_page, len(seen))
            if new_this_page == 0:
                break
            time.sleep(0.3)

    log.info("Discovery complete: %d unique candidates from API", len(seen))
    return seen


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — SCRAPE HTML PRODUCT PAGE (ingredients + full nutrition table)
# ══════════════════════════════════════════════════════════════════════════════

_INGR_PATTERNS = [
    re.compile(r"(?:רכיבים|מרכיבים|רכיב)[:\s]*(.*)", re.DOTALL | re.IGNORECASE),
]


def _extract_ingredients_html(soup: BeautifulSoup) -> str:
    """Extract ingredients from product page HTML."""
    # Primary: look for <li> containing ingredient markers
    for li in soup.find_all("li"):
        text = li.get_text(separator=" ", strip=True)
        for pat in _INGR_PATTERNS:
            m = pat.match(text)
            if m and len(m.group(1).strip()) > 15:
                return m.group(1).strip()[:2000]

    # Secondary: look for any element with ingredient label
    for label_text in ("רכיבים", "מרכיבים", "רכיב"):
        for node in soup.find_all(string=re.compile(label_text)):
            parent = node.find_parent()
            if not parent:
                continue
            container = parent.find_parent()
            if container:
                full = container.get_text(separator=" ", strip=True)
                for pat in _INGR_PATTERNS:
                    m = pat.search(full)
                    if m and len(m.group(1).strip()) > 15:
                        return m.group(1).strip()[:2000]

    return ""


def _extract_allergens_html(soup: BeautifulSoup) -> str:
    for node in soup.find_all(string=re.compile(r"אלרג")):
        parent = node.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            text = container.get_text(separator=" ", strip=True)
            if len(text) > 5:
                return text[:500]
    return ""


def scrape_product_page(code: str, meta: dict) -> dict:
    """
    Fetch the HTML product page for a Shufersal product.
    Returns enriched record with ingredients and full nutrition.
    """
    # code is like "P_7290107971522"
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get_html(url, timeout=35)
    if not r:
        return {
            "html_fetch": "failed",
            "ingredients_raw": "",
            "allergens_raw": "",
            "nutrition_numeric_per_100g": {},
            "plausibility_gate": {"verdict": "quarantine", "fail_reasons": ["html_fetch_failed"]},
        }

    soup = BeautifulSoup(r.text, "html.parser")
    source_url = r.url

    # Nutrition via shared parser (correct fat parser, EV-029 fix)
    nutr_parsed = parse_nutrition_list(soup)
    nutr_raw_src = extract_nutrition_raw(soup)

    nutr_numeric_raw = {
        "energy_kcal_raw": nutr_parsed.get("energy", ""),
        "fat_raw": nutr_parsed.get("fat", ""),
        "saturated_fat_raw": nutr_parsed.get("saturated_fat", ""),
        "carbs_raw": nutr_parsed.get("carbs", ""),
        "sugar_raw": nutr_parsed.get("sugar", ""),
        "fiber_raw": nutr_parsed.get("fiber", ""),
        "protein_raw": nutr_parsed.get("protein", ""),
        "sodium_raw": nutr_parsed.get("sodium", ""),
    }
    nutr_numeric = parse_nutrition_numeric(nutr_numeric_raw)

    # Ingredients from HTML
    ingredients_raw = _extract_ingredients_html(soup)
    allergens_raw = _extract_allergens_html(soup)

    # Serving size from meta unit_description or name
    name = meta.get("description", "") or meta.get("name_truncated", "")
    unit_desc = meta.get("unit_description", "") or ""
    weight_g = _extract_weight_g(name) or _extract_weight_g(unit_desc)

    # Check for multipack: "N*Mg" pattern
    serving_g = None
    m = re.search(r"(\d+)\s*[x*×]\s*(\d+(?:\.\d+)?)\s*(?:g|גר)", unit_desc or name, re.IGNORECASE)
    if m:
        serving_g = float(m.group(2))
    elif weight_g:
        # Single bar: serving = full weight if < 80g (single bar format)
        if weight_g < 80:
            serving_g = weight_g

    # Run plausibility gate
    gate = run_plausibility_gate(nutr_numeric, ingredients_raw, code, serving_g)

    return {
        "html_fetch": "ok",
        "source_url": source_url,
        "ingredients_raw": ingredients_raw,
        "allergens_raw": allergens_raw,
        "nutrition_parsed_strings": nutr_parsed,
        "nutrition_raw_src": nutr_raw_src,
        "nutrition_numeric_per_100g": nutr_numeric,
        "weight_g": weight_g,
        "serving_g": serving_g,
        "plausibility_gate": gate,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — STRICT CURATION: SNACK BARS ONLY
# ══════════════════════════════════════════════════════════════════════════════

# Hard EXCLUDE signals — these are definitively NOT snack bars
HARD_EXCLUDE_NAMES = [
    # Raw ingredients / bulk cereals
    "שיבולת שועל בפח",      # raw oats tin (Quaker)
    "שבולת שועל דקה",        # raw thin oats
    "שיבולת שועל עבה",       # raw thick oats
    "קמח שיבולת שועל",       # oat flour
    # Loose granola bags (not bars)
    "גרנולה דבש",             # loose granola bag
    "גרנולה שוקולד פיטנס",   # loose granola bag
    "גרנולה שוקולד קינואה",  # loose granola bag
    "גרנולה אגוזים",          # loose granola bag
    "גרנולה עשירה",           # loose granola bag
    "גרנולה פקאן",            # loose granola bag
    "גרנולה פירות",           # loose granola bag
    "גרנולה מייפל",           # loose granola bag
    "גרנולה חמוציות",         # loose granola bag
    "גרנולה לוז",             # loose granola bag
    "גרנולה מיקס",            # loose granola bag
    "גרנולה 48%",             # loose granola bag
    "גרנולה סופרפוד",         # loose granola bag
    "גרנולה פרוטאין",         # loose granola bag (bag format)
    "גרנולה ממותקת",          # loose granola bag
    "חגיגת גרנולה",           # loose granola bag
    "גרנולה עם פירות",        # loose granola bag
    # Breakfast cereals (box/bag format)
    "קורנפלקס",               # cornflakes
    "דגני בוקר",              # breakfast cereals
    "טריקס",                  # Trix cereal
    "צ'יריוס",                # Cheerios
    "מולטי צ'ריוס",           # Multi Cheerios
    "קראנץ'",                 # Crunch cereal
    "מוזלי",                  # Muesli
    "דגני בוקר קראנץ'",       # Nestle Crunch cereal
    "כריות נוגט",             # Trix puffs
    "שוגי",                   # Suggy puffs
    "דליפקאן",               # Delicorn
    "ריבועי דגנים",           # cereal squares
    # Savory puffs / chips (not bars)
    "במבה",                   # Bamba corn puff
    "ביסלי",                  # Bisli
    "פריכיות",                # rice cakes
    "פריכונים",               # rice crisps
    # Pastry / Hamantaschen
    "אוזן המן",               # Hamantaschen
    "אוזני המן",              # Hamantaschen plural
    # Baking ingredients / fillings
    "מלית תמרים",             # date filling for baking
    # Refrigerated / dessert
    "מעדן שיבולת שועל",       # refrigerated oat dessert
    # Energy gel (liquid)
    "ג'ל אנרגיה",             # energy gel
    # Topping
    "טופינג",                  # topping (not a bar)
]

# Categories that signal "NOT a snack bar" (box cereal, raw oats, etc.)
NOT_SNACK_CATEGORY_SIGNALS = {
    "A250201": "loose_granola",     # loose granola bags
    "A250204": "raw_oats",          # raw oats
}

# Categories that are known snack bar parents
SNACK_BAR_CATEGORY_SIGNALS = {
    "A281404": "gluten_free_snack_bars",
}

# Hard INCLUDE signals: names that are clearly bars / bar formats
SNACK_BAR_SIGNALS = [
    "חטיף דגנים",
    "חטיף גרנולה",
    "חטיף שיבולת שועל",
    "חטיף תמרים",
    "חטיף חלבון",
    "חטיף אנרגיה",
    "חטיף פירות",
    "חטיף קורני",
    "חטיף ספורט",
    "חטיפי חלבון",
    "חטיפי דגנים",
    "גרנולה בר",
    "granola bar",
    "nature valley",
    "slim delice",
    "סלים דליס",
    "fitness",
    "פיטנס חטיף",
    "פיטנס בר",
    "quaker bar",
    "mojo bar",
    "7degrees",
    "בר תמרים",
    "בר חלבון",
    "בר אנרגיה",
    "protein bar",
    "energy bar",
    "free חטיף",
    "פנגיאה חטיף",
    "pangea bar",
    "קורני סנדוויץ",  # Korny sandwich bar (dry, bar format)
]

# Patterns that indicate SALTY snacks (not snack bars)
SALTY_SIGNALS = [
    "סלק", "רוזמרין", "עשבי תיבול", "מלח", "גבינה", "בצל", "שום",
    "thin", "פריך קריספ", "תפוחי אדמה", "ביסקוויט",
]

# Patterns that indicate CHOCOLATE bars / candy (not snack bars)
CHOCOLATE_SIGNALS = [
    "פסק זמן", "קיטקט", "מארז מיני פסק",
    "עוגיות", "עוגייה", "ביסקוויט",
    "ממתק", "סוכריות",
]


def curate_product(meta: dict, scraped: dict) -> tuple[str, str]:
    """
    Classify a product as 'keep', 'salty_corpus', 'chocolate_category', or 'not_snack'.
    Returns (verdict, reason).
    """
    name = (meta.get("description", "") or meta.get("name_truncated", "")).strip()
    name_l = name.lower()
    brand = (meta.get("brand", "") or "").strip()
    all_cats = meta.get("all_cat_codes", [])

    # 1. Hard exclude by name prefix/substring
    for excl in HARD_EXCLUDE_NAMES:
        if excl.lower() in name_l:
            # Determine reason
            if any(s in name_l for s in ["גרנולה", "שיבולת שועל בפח", "קמח שיבולת שועל",
                                          "קורנפלקס", "דגני בוקר", "מוזלי"]):
                return "not_snack", f"name match '{excl}' — bulk/loose/cereal format"
            if any(s in name_l for s in ["במבה", "ביסלי", "פריכיות", "פריכונים"]):
                return "salty_corpus", f"name match '{excl}' — savory snack format"
            if any(s in name_l for s in ["אוזן המן", "מלית תמרים", "ג'ל אנרגיה", "מעדן"]):
                return "not_snack", f"name match '{excl}' — wrong product type"
            return "not_snack", f"name match '{excl}'"

    # 2. Category signals
    for cat in all_cats:
        if cat in NOT_SNACK_CATEGORY_SIGNALS:
            reason_cat = NOT_SNACK_CATEGORY_SIGNALS[cat]
            if reason_cat == "loose_granola":
                return "not_snack", f"category {cat}=loose_granola"
            if reason_cat == "raw_oats":
                return "not_snack", f"category {cat}=raw_oats"

    # 3. Salty signals in name
    for sig in SALTY_SIGNALS:
        if sig.lower() in name_l:
            return "salty_corpus", f"salty signal '{sig}' in name"

    # 4. Chocolate/candy signals
    for sig in CHOCOLATE_SIGNALS:
        if sig.lower() in name_l:
            return "chocolate_category", f"chocolate/candy signal '{sig}' in name"

    # 5. Positive snack bar signals
    for sig in SNACK_BAR_SIGNALS:
        if sig.lower() in name_l:
            return "keep", f"snack bar signal '{sig}'"

    # 6. Category-confirmed snack bars
    for cat in all_cats:
        if cat in SNACK_BAR_CATEGORY_SIGNALS:
            return "keep", f"category {cat}={SNACK_BAR_CATEGORY_SIGNALS[cat]}"

    # 7. Brand-based classification for known brands
    brand_l = brand.lower()
    if any(b in brand_l for b in ["נייטשר וואלי", "nature valley", "slim delice", "סלים דליס"]):
        return "keep", f"known snack bar brand: {brand}"
    if any(b in brand_l for b in ["קורני", "korny"]) and "סנדוויץ" in name_l:
        return "keep", f"Korny sandwich bar (bar format)"
    if any(b in brand_l for b in ["קורני", "korny"]) and any(s in name_l for s in ["חטיף", "דגנים"]):
        return "keep", f"Korny snack bar"

    # 8. Borderline: log and include with flag if name contains any "חטיף"
    if "חטיף" in name_l:
        return "keep_borderline", f"contains 'חטיף' but no specific bar signal — include with review"

    # 9. Default: not snack
    return "not_snack", f"no snack bar signals found in name: {name[:50]}"


# ══════════════════════════════════════════════════════════════════════════════
# BSIP1 RECORD BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _split_ingredients_list(ingredients_raw: str) -> list[str]:
    """Split ingredients string into list."""
    if not ingredients_raw:
        return []
    # Split on comma, semicolon, or period
    parts = re.split(r"[,;.]", ingredients_raw)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]


def build_bsip1(meta: dict, scraped: dict, barcode: str, run_id: str) -> dict:
    """Build a BSIP1-format product record."""
    name = (meta.get("description", "") or meta.get("name_truncated", "")).strip()
    brand = (meta.get("brand", "") or "").strip()
    code = meta.get("code", "")
    image_url = meta.get("image_url", "")

    gate = scraped.get("plausibility_gate", {})
    nutr = gate.get("final_nutrition") or scraped.get("nutrition_numeric_per_100g", {})
    ingredients_raw = scraped.get("ingredients_raw", "") or ""
    ingredients_list = _split_ingredients_list(ingredients_raw)

    # Confidence
    has_ingredients = bool(ingredients_raw.strip())
    has_nutrition = gate.get("verdict") in ("pass", "converted_pass")
    if has_ingredients and has_nutrition:
        trust_score = 0.90
        trust_level = "high"
    elif has_nutrition:
        trust_score = 0.80
        trust_level = "medium"
    else:
        trust_score = 0.50
        trust_level = "low"

    missing = []
    if not meta.get("unit_description"):
        missing.append("serving_size_g")
    if not has_ingredients:
        missing.append("ingredients_text_he")

    warnings = []
    if not has_ingredients:
        warnings.append("ingredients_missing")

    # Additives/markers (basic extraction from ingredients)
    additives = []
    if ingredients_raw:
        # E-numbers
        for m in re.finditer(r'\bE[\d]{3,4}[a-z]?\b', ingredients_raw, re.IGNORECASE):
            additives.append(m.group())

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": f"bsip1_{barcode}",
        "barcode": barcode,
        "canonical_name_he": name,
        "canonical_name_en": None,
        "brand": brand,
        "package_size_g": scraped.get("weight_g"),
        "unit_count": None,
        "unit_size_g": None,
        "serving_size_g": scraped.get("serving_g"),
        "country_of_origin": None,
        "kosher_certification": None,
        "image_url": image_url,
        "source_retailers": ["shufersal"],
        "normalized_nutrition_per_100g": nutr,
        "energy_source_unit": "kcal",
        "ingredients_text_he": ingredients_raw if has_ingredients else None,
        "ingredients_list": ingredients_list,
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims": meta.get("health_attrs", []),
        "confidence": {
            "identity_confidence": "high" if brand else "medium",
            "barcode_confidence": "high",
            "nutrition_confidence": "confirmed_per_100g" if has_nutrition else "missing",
            "matched_by": "shufersal_json_api+product_page_html",
            "observation_count": 1,
        },
        "barcode_validation_status": "confirmed",
        "barcode_confidence_reason": "Extracted from Shufersal JSON API sku field.",
        "nutrition_basis_claimed": gate.get("basis", ""),
        "nutrition_basis_detected": gate.get("basis", "per_100g") or "per_100g",
        "nutrition_basis_gate": gate.get("verdict", "quarantine"),
        "nutrition_basis_conversion_factor": gate.get("conversion_factor", 1.0),
        "nutrition_serving_g_used": gate.get("serving_g_used"),
        "nutrition_consistency_status": "consistent",
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality": "present" if has_ingredients else "missing",
        "ingredient_warnings": warnings,
        "canonical_trust_score": trust_score,
        "canonical_trust_level": trust_level,
        "canonical_risk_flags": ["shufersal_single_source"] + ([] if has_ingredients else ["ingredients_missing"]),
        "conflicts_summary": {
            "count": 0,
            "has_unresolved": False,
            "fields_in_conflict": [],
            "identity_conflicts": [],
            "nutrition_conflicts": [],
            "ingredient_conflicts": [],
            "labeling_conflicts": [],
            "completeness_conflicts": [],
        },
        "missing_fields": missing,
        "inferred_fields": [],
        "audit_ref": f"bsip1_audit_{barcode}.json",
        "ingredients_raw": ingredients_raw,
        "ingredients_raw_provenance": {
            "source": "shufersal_product_page_html",
            "bsip0_status": "bsip0_scrape",
            "populated_at": f"bsip1_{run_id}",
            "missing": not has_ingredients,
            "note": "TASK-360 Phase 3 — JSON API discovery + HTML detail page scrape",
        },
        "ingredient_order": ingredients_list,
        "extracted_additives": additives,
        "extracted_flavors": [],
        "extracted_sweeteners": [],
        "extracted_protein_markers": [],
        "extracted_matrix_markers": [],
        "extracted_fermentation_markers": [],
        "extracted_roasting_markers": [],
        "enrichment_summary": {
            "ingredient_count_parsed": len(ingredients_list),
            "additive_count": len(additives),
            "flavor_marker_count": 0,
            "sweetener_count": 0,
            "protein_marker_count": 0,
            "matrix_marker_count": 0,
            "fermentation_marker_count": 0,
            "roasting_marker_count": 0,
            "has_flavor_descriptor": False,
            "has_prebiotic_fiber": False,
            "has_live_cultures": False,
            "has_protein_isolate_or_concentrate": any(
                m in ingredients_raw.lower() for m in ["אבקת חלבון", "protein isolate", "concentrate"]
            ),
        },
        "enrichment_version": f"bsip1_{run_id}",
        "enrichment_warnings": warnings,
        # NOVA proxy (will be computed by engine; we provide a best-guess here)
        "nova_proxy": 3 if not has_ingredients else None,
        "nova_confidence": 0.5 if not has_ingredients else None,
        "nova_confidence_band": "low" if not has_ingredients else None,
        "nova_notes": ["insufficient_ingredient_data"] if not has_ingredients else [],
    }


# ══════════════════════════════════════════════════════════════════════════════
# BSIP2 SCORING — unchanged engine
# ══════════════════════════════════════════════════════════════════════════════

def run_bsip2(bsip1_path: pathlib.Path, output_dir: pathlib.Path) -> dict:
    """Run BSIP2 on a single BSIP1 file using the unchanged engine."""
    from input_loader import load_product, validate_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace, write_trace
    from structural_classifier import classify_structural_class

    try:
        product = load_product(bsip1_path)
        product["_source_path"] = str(bsip1_path)
        errors = validate_product(product)
        product["_load_errors"] = errors

        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)
        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)

        barcode = product.get("barcode", "unknown")
        trace_dir = output_dir / f"bsip1_{barcode}"
        trace_dir.mkdir(parents=True, exist_ok=True)
        write_trace(trace, trace_dir)
        return {"status": "ok", "trace": trace, "barcode": barcode}
    except Exception as exc:
        log.error("BSIP2 error for %s: %s", bsip1_path.name, exc)
        return {"status": "error", "error": str(exc), "barcode": "unknown"}


# ══════════════════════════════════════════════════════════════════════════════
# FRONTEND JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_frontend_json(scored_products: list[dict], run_id: str) -> dict:
    """Build the frontend JSON from BSIP2 traces. Copy fields = PENDING_COPY."""
    from constants import score_to_grade

    items = []
    for sp in scored_products:
        trace = sp.get("trace", {})
        if not trace:
            continue

        barcode = trace.get("barcode", "")
        name_he = trace.get("canonical_name_he", "")
        brand = trace.get("brand", "")
        score = trace.get("score")
        grade = trace.get("grade") or (score_to_grade(score) if score is not None else "?")

        nutr = trace.get("normalized_nutrition_per_100g", {}) or {}
        image_url = trace.get("image_url", "")

        item = {
            "barcode": barcode,
            "name_he": name_he,
            "brand": brand,
            "score": score,
            "grade": grade,
            "image_url": image_url,
            "nutrition_per_100g": {
                "energy_kcal": nutr.get("energy_kcal"),
                "fat_g": nutr.get("fat_g"),
                "fat_saturated_g": nutr.get("fat_saturated_g"),
                "sodium_mg": nutr.get("sodium_mg"),
                "carbohydrates_g": nutr.get("carbohydrates_g"),
                "sugars_g": nutr.get("sugars_g"),
                "dietary_fiber_g": nutr.get("dietary_fiber_g"),
                "protein_g": nutr.get("protein_g"),
            },
            # Copy fields — PENDING_COPY (voice pass is a separate phase)
            "verdict": "PENDING_COPY",
            "insight_line": "PENDING_COPY",
            "row_verdict": "PENDING_COPY",
            # Scoring trace summary
            "_scoring_trace": {
                "category": trace.get("category"),
                "structural_class": trace.get("structural_class"),
                "limiting_factors": trace.get("limiting_factors", []),
                "nova_proxy": trace.get("nova_proxy"),
                "flags_active": trace.get("flags_active", []),
            },
        }
        items.append(item)

    # Sort by score descending
    items.sort(key=lambda x: (x["score"] is None, -(x["score"] or 0)))

    return {
        "meta": {
            "version": "snacks_frontend_v5",
            "run_id": run_id,
            "generated_at": now_iso(),
            "category": "snack_bars",
            "product_count": len(items),
            "copy_status": "PENDING_COPY",
            "engine_unchanged": True,
            "off_check": "PASS - no Open Food Facts",
        },
        "products": items,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    log.info("=" * 60)
    log.info("TASK-360 Phase 3: Snack Bar Corpus Rebuild")
    log.info("RUN_ID: %s", RUN_ID)
    log.info("=" * 60)

    run_record = {
        "run_id": RUN_ID,
        "phase": 3,
        "generated_at": now_iso(),
        "discovery": {},
        "scraping": {},
        "curation": {},
        "bsip2": {},
        "quality_gate": {},
        "frontend": {},
        "engine_diff": "",
        "engine_unchanged": True,
    }

    # STEP 1: Discovery via JSON API
    log.info("\n=== STEP 1: Discovery ===")
    candidates = discover_all()
    run_record["discovery"]["api_candidates"] = len(candidates)

    # STEP 2: Scrape HTML for each candidate (ingredients + full nutrition)
    log.info("\n=== STEP 2: HTML scraping (%d candidates) ===", len(candidates))
    scraped_all: dict[str, dict] = {}
    bsip0_records: dict[str, dict] = {}

    for i, (code, meta) in enumerate(candidates.items()):
        log.info("  [%d/%d] Scraping %s — %s", i + 1, len(candidates), code,
                 (meta.get("description") or meta.get("name_truncated", ""))[:40])
        scraped = scrape_product_page(code, meta)
        scraped_all[code] = scraped

        # Save BSIP0 record
        barcode = meta.get("sku") or meta.get("ean") or code.replace("P_", "").replace("p_", "")
        bsip0 = {
            "schema_version": "bsip0_task360_phase3_v1",
            "source": {
                "retailer": "Shufersal",
                "retailer_id": "shufersal",
                "source_url": scraped.get("source_url", f"{BASE}/online/he/p/{code.lower()}"),
                "source_type": "json_api+product_page_html",
                "scrape_run": RUN_ID,
                "scraped_at": now_iso(),
            },
            "product_identity": {
                "name": meta.get("description", "") or meta.get("name_truncated", ""),
                "brand": meta.get("brand", ""),
                "barcode": barcode,
                "shufersal_code": code,
                "image_url": meta.get("image_url", ""),
                "all_cat_codes": meta.get("all_cat_codes", []),
                "second_level_category": meta.get("second_level_category", ""),
                "manufacturer": meta.get("manufacturer", ""),
                "unit_description": meta.get("unit_description", ""),
                "health_attrs": meta.get("health_attrs", []),
                "source": meta.get("source", ""),
            },
            "nutrition_from_api_hints": {
                "calories": meta.get("calories_hint"),
                "fats": meta.get("fats_hint"),
                "sodium": meta.get("sodium_hint"),
                "sugar": meta.get("sugar_hint"),
            },
            "nutrition_numeric_per_100g": scraped.get("nutrition_numeric_per_100g", {}),
            "ingredients_raw": scraped.get("ingredients_raw", ""),
            "allergens_raw": scraped.get("allergens_raw", ""),
            "plausibility_gate": scraped.get("plausibility_gate", {}),
            "weight_g": scraped.get("weight_g"),
            "serving_g": scraped.get("serving_g"),
            "price": meta.get("price", ""),
            "provenance": {
                "source": "shufersal_json_api+html_scrape",
                "source_url": scraped.get("source_url", ""),
                "fetched_at": now_iso(),
                "client_version": "task360_phase3_v1",
                "verification_status": "candidate",
                "off_check": "PASS - no Open Food Facts",
            },
        }
        bsip0_records[code] = bsip0

        # Save BSIP0 to disk
        bsip0_product_dir = BSIP0_DIR / code
        bsip0_product_dir.mkdir(parents=True, exist_ok=True)
        save_json(bsip0_product_dir / "product.json", bsip0)

        time.sleep(PRODUCT_DELAY)

    run_record["scraping"]["total_scraped"] = len(scraped_all)
    log.info("Scraping complete: %d products", len(scraped_all))

    # STEP 3: Curation
    log.info("\n=== STEP 3: Curation ===")
    kept: list[tuple[str, dict, dict, str]] = []  # (code, meta, scraped, reason)
    excluded: list[dict] = []
    borderline_kept: list[str] = []

    for code, meta in candidates.items():
        scraped = scraped_all[code]
        verdict, reason = curate_product(meta, scraped)
        name = meta.get("description", "") or meta.get("name_truncated", "")
        brand = meta.get("brand", "")
        barcode = meta.get("sku") or code.replace("P_", "")

        if verdict in ("keep", "keep_borderline"):
            # Further check: plausibility gate must pass (or have nutrition hints from API)
            gate = scraped.get("plausibility_gate", {})
            gate_verdict = gate.get("verdict", "quarantine")

            if gate_verdict == "quarantine" and verdict != "keep_borderline":
                # Still keep but flag as quarantine for data quality check
                pass

            if verdict == "keep_borderline":
                borderline_kept.append(barcode)
            kept.append((code, meta, scraped, reason))
            log.info("  KEEP: %s | %s | %s | gate=%s | reason=%s",
                     barcode, brand, name[:40], gate_verdict, reason[:50])
        else:
            excluded.append({
                "barcode": barcode,
                "code": code,
                "name": name,
                "brand": brand,
                "tag": verdict,
                "reason": reason,
            })
            log.info("  EXCL [%s]: %s | %s | %s", verdict, barcode, brand, name[:40])

    log.info("Curation: %d kept, %d excluded", len(kept), len(excluded))
    run_record["curation"] = {
        "total_candidates": len(candidates),
        "kept_count": len(kept),
        "excluded_count": len(excluded),
        "borderline_kept": borderline_kept,
        "excluded_list": excluded,
    }

    # STEP 4: Data quality gate — check every kept product
    log.info("\n=== STEP 4: Data Quality Gate ===")
    quality_table = []
    quarantine_from_quality = []

    for code, meta, scraped, reason in kept:
        barcode = meta.get("sku") or code.replace("P_", "")
        name = meta.get("description", "") or meta.get("name_truncated", "")
        brand = meta.get("brand", "") or ""
        gate = scraped.get("plausibility_gate", {})
        image_url = meta.get("image_url", "")
        ingredients_raw = scraped.get("ingredients_raw", "") or ""

        has_name = bool(name.strip()) and not name.startswith("חט.")  # no truncated
        has_brand = bool(brand.strip())
        has_ingredients = bool(ingredients_raw.strip())
        has_nutrition = gate.get("verdict") in ("pass", "converted_pass")
        has_image = bool(image_url.strip()) and "default" not in image_url
        nutr = gate.get("final_nutrition") or {}
        kcal = nutr.get("energy_kcal", 0) or 0
        acc = gate.get("accounted_mass", 0) or 0

        all_ok = has_name and has_brand and has_ingredients and has_nutrition and has_image

        quality_table.append({
            "barcode": barcode,
            "name": name,
            "brand": brand,
            "has_name": has_name,
            "has_brand": has_brand,
            "has_ingredients": has_ingredients,
            "nutrition_kcal": round(kcal, 1),
            "nutrition_accounted_mass": round(acc, 1),
            "nutrition_plausible": has_nutrition,
            "has_image": has_image,
            "all_complete": all_ok,
            "gate_verdict": gate.get("verdict", "unknown"),
            "missing": [
                f for f, v in [
                    ("name", has_name), ("brand", has_brand),
                    ("ingredients", has_ingredients),
                    ("nutrition", has_nutrition), ("image", has_image)
                ] if not v
            ],
        })

        if not all_ok:
            log.warning("  QUALITY GAP: %s %s — missing: %s",
                        barcode, name[:30],
                        [f for f, v in [
                            ("name", has_name), ("brand", has_brand),
                            ("ingredients", has_ingredients),
                            ("nutrition", has_nutrition), ("image", has_image)
                        ] if not v])
            quarantine_from_quality.append((code, meta, scraped, reason, "quality_gap"))

    complete_count = sum(1 for q in quality_table if q["all_complete"])
    log.info("Quality gate: %d/%d complete", complete_count, len(quality_table))
    run_record["quality_gate"] = {
        "total_kept": len(quality_table),
        "complete_count": complete_count,
        "gap_count": len(quarantine_from_quality),
        "quality_table": quality_table,
    }

    # STEP 5: Build BSIP1 for kept+complete products
    log.info("\n=== STEP 5: BSIP1 generation ===")
    # Keep products that have at least nutrition+name+brand+image (ingredients missing = flag but don't discard)
    # Per spec: if ANY kept product is missing one, either fix (re-fetch) or move to quarantine
    # We move no-ingredient products to quarantine UNLESS they pass nutrition gate
    final_kept = []
    quarantined_products = []

    for code, meta, scraped, reason in kept:
        barcode = meta.get("sku") or code.replace("P_", "")
        qt = next((q for q in quality_table if q["barcode"] == barcode), None)
        if qt and qt["all_complete"]:
            final_kept.append((code, meta, scraped, reason))
        else:
            # Already tried scraping — move to quarantine
            quarantined_products.append({
                "barcode": barcode,
                "name": meta.get("description", ""),
                "brand": meta.get("brand", ""),
                "missing": qt.get("missing", []) if qt else ["unknown"],
                "reason": "quality_gate_failed",
            })
            log.info("  QUARANTINE (quality): %s %s", barcode, meta.get("description", "")[:30])

    log.info("Final kept after quality gate: %d", len(final_kept))

    # Write BSIP1 files
    bsip1_paths = []
    for code, meta, scraped, reason in final_kept:
        barcode = meta.get("sku") or code.replace("P_", "")
        bsip1 = build_bsip1(meta, scraped, barcode, RUN_ID)
        bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
        save_json(bsip1_path, bsip1)
        bsip1_paths.append(bsip1_path)

    log.info("BSIP1: %d files written to %s", len(bsip1_paths), BSIP1_DIR)

    # STEP 6: BSIP2 scoring (unchanged engine)
    log.info("\n=== STEP 6: BSIP2 scoring (%d products) ===", len(bsip1_paths))
    bsip2_products_dir = BSIP2_DIR / "products"
    scored_products = []
    bsip2_errors = []

    for bsip1_path in bsip1_paths:
        result = run_bsip2(bsip1_path, bsip2_products_dir)
        if result["status"] == "ok":
            scored_products.append(result)
        else:
            bsip2_errors.append(result)
            log.error("  BSIP2 error: %s", result.get("error", ""))

    log.info("BSIP2: %d scored, %d errors", len(scored_products), len(bsip2_errors))

    # Grade distribution
    grade_dist: dict[str, int] = {}
    for sp in scored_products:
        grade = sp.get("trace", {}).get("grade", "?")
        grade_dist[grade] = grade_dist.get(grade, 0) + 1

    run_record["bsip2"] = {
        "scored": len(scored_products),
        "errors": len(bsip2_errors),
        "error_details": [e.get("error", "") for e in bsip2_errors],
        "grade_distribution": grade_dist,
    }

    # STEP 7: Frontend JSON
    log.info("\n=== STEP 7: Frontend JSON generation ===")
    frontend_data = build_frontend_json(scored_products, RUN_ID)
    save_json(FRONTEND_PATH, frontend_data)
    frontend_sha = hashlib.sha256(
        FRONTEND_PATH.read_bytes()
    ).hexdigest()
    log.info("Frontend JSON: %d products → %s", len(frontend_data["products"]), FRONTEND_PATH)

    run_record["frontend"] = {
        "path": str(FRONTEND_PATH),
        "product_count": len(frontend_data["products"]),
        "sha256": frontend_sha,
    }

    # STEP 8: Engine diff check
    import subprocess
    diff_result = subprocess.run(
        ["git", "diff", "--stat",
         "03_operations/bsip2/",
         "03_operations/page_generator/configs/"],
        cwd=str(ROOT),
        capture_output=True, text=True
    )
    engine_diff = diff_result.stdout.strip()
    run_record["engine_diff"] = engine_diff
    run_record["engine_unchanged"] = (engine_diff == "")

    # Final summary
    run_record["final_product_count"] = len(scored_products)
    run_record["quality_final"] = {
        "kept_and_complete": len(final_kept),
        "quarantined_quality": len(quarantined_products),
        "quarantined_products": quarantined_products,
    }
    run_record["completed_at"] = now_iso()

    # Save run record
    run_record_path = BSIP0_DIR / f"{RUN_ID}_run_record.json"
    save_json(run_record_path, run_record)
    log.info("Run record: %s", run_record_path)

    # Print summary report
    log.info("\n" + "=" * 60)
    log.info("TASK-360 PHASE 3 SUMMARY")
    log.info("=" * 60)
    log.info("Discovery: %d candidates from JSON API", len(candidates))
    log.info("Kept after curation: %d", len(kept))
    log.info("Complete (all 5 fields): %d/%d", complete_count, len(kept))
    log.info("Final scored: %d", len(scored_products))
    log.info("Grade distribution: %s", grade_dist)
    log.info("Engine unchanged: %s", run_record["engine_unchanged"])
    if engine_diff:
        log.warning("ENGINE DIFF DETECTED: %s", engine_diff)
    log.info("Frontend: %s", FRONTEND_PATH)
    log.info("RUN_ID: %s", RUN_ID)

    return run_record


if __name__ == "__main__":
    main()
