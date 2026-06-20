"""
TASK-360 — Snacks Fresh Re-Scrape: Shufersal (primary) + Victory (cross-check)
=============================================================================
Pipeline: discover → scrape → plausibility gate → BSIP1 → BSIP2 → frontend JSON

Sources:
  PRIMARY   = Shufersal (requests, confirmed reachable 200)
  SECONDARY = Victory (Playwright cross-check for barcodes found on both)

HARD RULES enforced:
  - OFF BAN: no Open Food Facts, ever
  - TRIPWIRE-1: no scoring engine changes (03_operations/bsip2/**, page_generator configs)
  - No fabrication: if primary unreachable, script stops and reports
  - Copy fields = PENDING_COPY throughout (voice pass is a separate phase)

Output dirs:
  BSIP0  : 02_products/snack_bars/observations_bsip0/shufersal/<RUN_ID>/<barcode>/
  BSIP1  : 03_operations/bsip1/run_snacks_task360_shuf_<TS>/output/
  BSIP2  : 02_products/snack_bars/bsip2_outputs/<RUN_ID>/
  Frontend: bari-web/src/data/comparisons/snacks_frontend_v4.json
  Validator: 02_products/snack_bars/plausibility_gate.py  (standalone reusable module)
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import json
import logging
import math
import os
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

# ── Shared BSIP0 nutrition parser ─────────────────────────────────────────────
_SHARED = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")
sys.path.insert(0, str(_SHARED))
from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list,
    extract_nutrition_raw,
    parse_nutrition_numeric,
    nutrition_implausible,
)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
RUN_TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
RUN_ID = f"run_snacks_task360_shuf_{RUN_TS}"

BSIP0_DIR = SNACKS_DIR / "observations_bsip0" / "shufersal" / RUN_ID
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = SNACKS_DIR / "bsip2_outputs" / RUN_ID
BSIP2_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v4.json"
CONFIG_PATH = ROOT / "03_operations" / "page_generator" / "configs" / "snacks.json"

for _d in (BSIP0_DIR, BSIP1_DIR, BSIP2_DIR / "products"):
    _d.mkdir(parents=True, exist_ok=True)

# ── Shufersal HTTP config ─────────────────────────────────────────────────────
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
MAX_PAGES = 6
PRODUCT_DELAY = 0.8

# ── Shufersal snack-bar search queries ───────────────────────────────────────
SEARCH_QUERIES: list[tuple[str, str]] = [
    # (query_term, tier)
    ("חטיף דגנים",       "mainstream"),
    ("חטיף גרנולה",      "mainstream"),
    ("חטיף בריאות",      "mainstream"),
    ("חטיף שיבולת שועל", "mainstream"),
    ("חטיף תמרים",       "mainstream"),
    ("חטיף חלבון",       "specialty"),
    ("גרנולה בר",        "specialty"),
    ("מארז חטיפים",      "specialty"),
    ("nature valley",    "specialty"),
    ("slim delice",      "specialty"),
    ("פיטנס בר",         "specialty"),
    ("quaker בר",        "specialty"),
    ("חטיף אנרגיה",      "specialty"),
]

# Shufersal category codes for snack-bars shelf (best-effort)
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A13413?pageSize={PAGE_SIZE}", "A13413_snack_bars"),
    (f"{BASE}/online/he/c/A13414?pageSize={PAGE_SIZE}", "A13414_granola_bars"),
    (f"{BASE}/online/he/c/A07?pageSize={PAGE_SIZE}",    "A07_breakfast"),   # supplemental
]

# Hard-exclude signals: these names clearly are NOT snack bars
HARD_EXCLUDE = [
    # Clearly non-snack categories
    "ביסקוויט", "עוגיה", "עוגיות", "וופל",
    "קרקר", "פריכית", "פריכיות",
    "שוקולד טבלה", "שוקולד מריר", "שוקולד חלב",
    "גלידה", "ארטיק",
    "משקה", "מיץ", "חלב", "יוגורט",
    "לחם", "לחמנייה", "פיתה",
    "גבינה", "קוטג",
    "ממרח", "ריבה", "נוטלה",
    "קפסול", "כמוסה", "תרופה",
    # Cereal box (not a bar)
    "דגני בוקר קופסה", "קורנפלקס", "מוזלי",
    # Ptitim/pasta
    "פתיתים", "פסטה", "אטריות",
    # Salty/savory snacks (chips/puffs) not bars
    "ביסלי", "אסנס", "פרינגלס", "צ'יפס",
    "בייגלה", "קרוטונים",
]

# Positive signals: these names are clearly snack/cereal bars
INCLUDE_SIGNALS = [
    "חטיף", "חטיפי", "גרנולה", "granola", "בר ", "bar",
    "nature valley", "slim delice", "פיטנס", "fitness",
    "quaker", "שיבולת שועל", "תמרים", "חלבון", "protein",
    "אנרגיה", "snack", "crunch", "קראנצ'י",
]

# ── Plausibility gate thresholds (TASK-360 spec) ─────────────────────────────
GATE_MIN_ACCOUNTED_G = 70.0   # carbs+fat+protein+fiber per 100g
GATE_MIN_KCAL_DRY = 150.0     # dry snack minimum kcal/100g

SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק", "גלוקוז-פרוקטוז",
]

# ── Victory cross-check config ────────────────────────────────────────────────
VICTORY_BASE = "https://www.victoryonline.co.il"
# Victory uses the same CDN as Yohananof; we probe only barcodes we found on Shufersal.
# The cross-check is requests-first (no Playwright dependency for the cross-check itself).
# We use their product API endpoint if available, else skip gracefully.

# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def save_json(path: pathlib.Path | str, data) -> None:
    pathlib.Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _get(url: str, timeout: int = 30) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        log.warning("GET error %s: %s", url, exc)
        return None


_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
]

def _extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 5 < val < 2000:
                    return val
            except ValueError:
                pass
    return None


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and ("maintenance" in text.lower() or "בתחזוקה" in text)


def _should_exclude(name: str) -> tuple[bool, str]:
    nl = name.lower()
    for term in HARD_EXCLUDE:
        if term.lower() in nl:
            return True, f"hard_exclude:{term}"
    return False, ""


def _is_snack_bar(name: str) -> bool:
    nl = name.lower()
    excl, _ = _should_exclude(name)
    if excl:
        return False
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1: Shufersal discovery
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
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": d.get("data-product-price", ""),
            "weight_g": _extract_weight_g(name),
            "brand": d.get("data-product-brand", ""),
        })
    return results


def _search_shufersal(query: str, page: int = 0) -> list[dict]:
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


def _category_shufersal(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def discover_shufersal() -> dict[str, dict]:
    """Run category + search discovery. Returns {code: product_meta} deduped."""
    seen: dict[str, dict] = {}

    log.info("=== Phase 1: Shufersal category traversal ===")
    for base_url, cat_id in CATEGORY_URLS:
        for page in range(MAX_PAGES):
            items = _category_shufersal(base_url, page)
            if not items:
                break
            new_this_page = 0
            for item in items:
                code = item["code"]
                if not code or code in seen:
                    continue
                excl, reason = _should_exclude(item["name"])
                if excl:
                    continue
                if not _is_snack_bar(item["name"]):
                    continue
                seen[code] = {**item, "source": cat_id, "source_type": "category"}
                new_this_page += 1
            log.info("  [%s] page %d: %d new items (total %d)", cat_id, page, new_this_page, len(seen))
            if new_this_page == 0:
                break
            time.sleep(0.3)

    log.info("=== Phase 2: Shufersal search queries ===")
    for query, tier in SEARCH_QUERIES:
        max_pages = MAX_PAGES if tier == "mainstream" else 3
        for page in range(max_pages):
            items = _search_shufersal(query, page)
            if not items:
                break
            new_this_page = 0
            for item in items:
                code = item["code"]
                if not code or code in seen:
                    continue
                excl, _ = _should_exclude(item["name"])
                if excl:
                    continue
                if not _is_snack_bar(item["name"]):
                    continue
                seen[code] = {**item, "source": f"search:{query}", "source_type": "search", "tier": tier}
                new_this_page += 1
            log.info("  [%s] p%d: %d new (total %d)", query[:25], page, new_this_page, len(seen))
            if new_this_page == 0:
                break
            time.sleep(0.3)

    log.info("Discovery complete: %d unique snack candidates", len(seen))
    return seen


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2: Scrape Shufersal product pages
# ──────────────────────────────────────────────────────────────────────────────

_INGR_PATTERNS = [
    re.compile(r"רכיב[ים:]*\s*(.*)", re.DOTALL),
    re.compile(r"מרכיב[ים:]*\s*(.*)", re.DOTALL),
]


def _extract_ingredients(soup: BeautifulSoup) -> str:
    # Primary: look for label containing "רכיב"
    for label_text in ("רכיבים", "מרכיבים", "רכיב"):
        node = soup.find(string=re.compile(label_text))
        if node:
            parent = node.find_parent()
            container = parent.find_parent() if parent else None
            if container:
                full = container.get_text(separator=" ", strip=True)
                for pat in _INGR_PATTERNS:
                    m = pat.search(full)
                    if m:
                        return m.group(1).strip()[:1000]

    # Fallback: scan all <li> elements
    for li in soup.find_all("li"):
        text = li.get_text(separator=" ", strip=True)
        for pat in _INGR_PATTERNS:
            m = pat.search(text)
            if m and len(m.group(1).strip()) > 20:
                return m.group(1).strip()[:1000]
    return ""


def _extract_allergens(soup: BeautifulSoup) -> str:
    for node in soup.find_all(string=re.compile(r"אלרג")):
        parent = node.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            text = container.get_text(separator=" ", strip=True)
            if len(text) > 5:
                return text[:500]
    return ""


def _parse_serving_size_g(name: str, weight_g: float | None) -> dict:
    """
    Parse serving size from product name / weight.
    For snack bars: weight_g is often the package; a single bar = unit_size_g.
    """
    result: dict = {
        "package_size_g": weight_g,
        "unit_size_g": None,
        "unit_count": None,
        "serving_size_g": None,
        "parse_source": None,
    }
    if not weight_g:
        return result

    # Detect "N*Mg" or "N x Mg" (pack of N bars each M grams): e.g. "6*30g", "5x35g"
    m = re.search(r"(\d+)\s*[x\*×]\s*(\d+(?:\.\d+)?)\s*(?:g|גר)", name or "", re.IGNORECASE)
    if m:
        unit_count = int(m.group(1))
        unit_g = float(m.group(2))
        result["unit_count"] = unit_count
        result["unit_size_g"] = unit_g
        result["serving_size_g"] = unit_g
        result["parse_source"] = "name_multipack_pattern"
        return result

    # Try "N יח'" + weight e.g. "120 גרם 4 יח'"
    m2 = re.search(r"(\d+)\s*יח", name or "")
    if m2:
        unit_count = int(m2.group(1))
        result["unit_count"] = unit_count
        result["unit_size_g"] = round(weight_g / unit_count, 1)
        result["serving_size_g"] = round(weight_g / unit_count, 1)
        result["parse_source"] = "name_unit_count"
        return result

    # Single pack / not parseable: keep package_size_g, serving unknown
    result["parse_source"] = "package_only"
    return result


def scrape_shufersal_product(code: str, meta: dict) -> dict | None:
    """Scrape a single Shufersal product page. Returns BSIP0 record or None on failure."""
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=30)
    if not r or r.status_code != 200:
        log.warning("  HTTP %s for %s", r.status_code if r else "ERR", code)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    source_url = r.url

    # LD+JSON for identity
    ld_name = ld_sku = ld_gtin = ""
    ld_images: list[str] = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string or "{}")
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                imgs = ld.get("image", [])
                ld_images = [imgs] if isinstance(imgs, str) else imgs[:3]
                break
        except Exception:
            pass

    # Brand from breadcrumb or LD
    brand = ""
    brand_span = soup.find("span", itemprop="brand")
    if brand_span:
        brand = brand_span.get_text(strip=True)

    # Nutrition via shared parser (TASK-142A / EV-026 fix)
    nutr_parsed = parse_nutrition_list(soup)
    nutr_raw_src = extract_nutrition_raw(soup)

    # Convert to numeric using shared canonical path
    nutr_numeric_dict = {
        "energy_kcal_raw":       nutr_parsed.get("energy", ""),
        "fat_raw":               nutr_parsed.get("fat", ""),
        "saturated_fat_raw":     nutr_parsed.get("saturated_fat", ""),
        "carbs_raw":             nutr_parsed.get("carbs", ""),
        "sugar_raw":             nutr_parsed.get("sugar", ""),
        "fiber_raw":             nutr_parsed.get("fiber", ""),
        "protein_raw":           nutr_parsed.get("protein", ""),
        "sodium_raw":            nutr_parsed.get("sodium", ""),
    }
    nutr_numeric = parse_nutrition_numeric(nutr_numeric_dict)

    # Ingredients
    ingredients_raw = _extract_ingredients(soup)

    # Allergens
    allergens_raw = _extract_allergens(soup)

    # Identity
    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "").replace("p_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    serving_info = _parse_serving_size_g(name, weight_g)

    record = {
        "schema_version": "bsip0_task360_shuf_v1",
        "source": {
            "retailer": "Shufersal",
            "retailer_id": "shufersal",
            "source_url": source_url,
            "source_type": "product_page_html",
            "scrape_run": RUN_ID,
            "scraped_at": now_iso(),
        },
        "product_identity": {
            "name": name,
            "brand": brand or meta.get("brand", ""),
            "barcode": barcode,
            "shufersal_code": code,
            "image_urls": [u for u in ld_images if u],
            "category_raw": meta.get("categories", ""),
            "source_category": meta.get("source", ""),
        },
        "serving_info": serving_info,
        "nutrition_raw": {
            "parsed_strings": nutr_parsed,
            "raw_source": nutr_raw_src,
            "basis": nutr_raw_src.get("selection", {}).get("selected_basis", "unknown"),
            "basis_header": nutr_raw_src.get("selection", {}).get("selected_table_header", ""),
        },
        "nutrition_numeric_per_100g": nutr_numeric,
        "ingredients_raw": ingredients_raw,
        "allergens_raw": allergens_raw,
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "provenance": {
            "source": "shufersal_direct_scrape",
            "source_url": source_url,
            "fetched_at": now_iso(),
            "client_version": "task360_v1",
            "verification_status": "candidate",
            "off_check": "PASS - no Open Food Facts",
        },
    }
    return record


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4: Per-100g plausibility gate
# ──────────────────────────────────────────────────────────────────────────────

def plausibility_gate(nutr_numeric: dict, serving_info: dict, ingredients: str, barcode: str) -> dict:
    """
    Apply the TASK-360 per-100g plausibility gate.

    Returns dict with:
      verdict: "pass" | "converted_pass" | "quarantine"
      final_nutrition: the per-100g numeric dict to use (or None if quarantine)
      nutrition_basis: "per_100g" | "converted_from_serving" | None
      conversion_factor: float (1.0 for direct pass)
      fail_reasons: list[str]
      accounted_mass: float (carbs+fat+protein+fiber per 100g)
      kcal: float
    """
    kcal = nutr_numeric.get("energy_kcal") or 0.0
    carbs = nutr_numeric.get("carbohydrates_g") or 0.0
    fat = nutr_numeric.get("fat_g") or 0.0
    protein = nutr_numeric.get("protein_g") or 0.0
    fiber = nutr_numeric.get("dietary_fiber_g") or 0.0
    sugars = nutr_numeric.get("sugars_g")

    accounted = carbs + fat + protein + fiber

    def _check(n100_kcal, n100_acc, n100_sugars) -> list[str]:
        fails = []
        if n100_acc < GATE_MIN_ACCOUNTED_G:
            fails.append(f"accounted_mass={n100_acc:.1f}g < {GATE_MIN_ACCOUNTED_G}g per 100g")
        if n100_sugars is not None and n100_sugars == 0:
            if any(tok in (ingredients or "") for tok in SUGAR_BEARING_TOKENS):
                fails.append("sugars=0 but ingredients contain sugar-bearing tokens")
        if n100_kcal is not None and n100_kcal < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={n100_kcal:.0f} < {GATE_MIN_KCAL_DRY} for dry snack")
        return fails

    fails = _check(kcal, accounted, sugars)

    if not fails:
        return {
            "verdict": "pass",
            "final_nutrition": {k: v for k, v in nutr_numeric.items() if not k.startswith("_")},
            "nutrition_basis": "per_100g",
            "conversion_factor": 1.0,
            "fail_reasons": [],
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
        }

    # Try per-serving conversion
    serving_g = (
        serving_info.get("unit_size_g")
        or serving_info.get("serving_size_g")
        or serving_info.get("package_size_g")
    )

    if serving_g and 5.0 < serving_g < 90.0:
        factor = 100.0 / serving_g

        def _conv(v):
            return round(v * factor, 1) if v is not None else None

        converted = {
            "energy_kcal":        _conv(kcal),
            "fat_g":              _conv(fat),
            "fat_saturated_g":    _conv(nutr_numeric.get("fat_saturated_g")),
            "fat_trans_g":        _conv(nutr_numeric.get("fat_trans_g")),
            "cholesterol_mg":     _conv(nutr_numeric.get("cholesterol_mg")),
            "sodium_mg":          _conv(nutr_numeric.get("sodium_mg")),
            "carbohydrates_g":    _conv(carbs),
            "sugars_g":           _conv(sugars),
            "dietary_fiber_g":    _conv(fiber),
            "protein_g":          _conv(protein),
        }

        conv_carbs = converted.get("carbohydrates_g") or 0.0
        conv_fat = converted.get("fat_g") or 0.0
        conv_prot = converted.get("protein_g") or 0.0
        conv_fiber = converted.get("dietary_fiber_g") or 0.0
        conv_kcal = converted.get("energy_kcal") or 0.0
        conv_sugars = converted.get("sugars_g")
        conv_acc = conv_carbs + conv_fat + conv_prot + conv_fiber

        conv_fails = _check(conv_kcal, conv_acc, conv_sugars)

        if not conv_fails:
            return {
                "verdict": "converted_pass",
                "final_nutrition": converted,
                "nutrition_basis": "converted_from_serving",
                "conversion_factor": round(factor, 3),
                "serving_g_used": serving_g,
                "fail_reasons": fails,
                "original_fail_reasons": fails,
                "accounted_mass": round(conv_acc, 1),
                "kcal": conv_kcal,
            }

        return {
            "verdict": "quarantine",
            "final_nutrition": None,
            "nutrition_basis": None,
            "conversion_factor": factor,
            "serving_g_used": serving_g,
            "fail_reasons": fails,
            "post_conversion_fails": conv_fails,
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
        }

    return {
        "verdict": "quarantine",
        "final_nutrition": None,
        "nutrition_basis": None,
        "conversion_factor": 1.0,
        "fail_reasons": fails,
        "no_serving_size_available": True,
        "accounted_mass": round(accounted, 1),
        "kcal": kcal,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Victory cross-check (requests-only; no Playwright)
# ──────────────────────────────────────────────────────────────────────────────

VICTORY_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}


def _victory_reachable() -> bool:
    try:
        r = requests.get(VICTORY_BASE, headers=VICTORY_HEADERS, timeout=12, allow_redirects=True)
        return r.status_code < 400
    except Exception:
        return False


def _try_victory_product(barcode: str) -> dict | None:
    """
    Try to reach a Victory product by barcode search.
    Victory search: GET https://www.victoryonline.co.il/category?search=<barcode>
    Returns minimal cross-check dict if nutrition found, else None.
    """
    url = f"{VICTORY_BASE}/category?search={barcode}"
    try:
        r = requests.get(url, headers=VICTORY_HEADERS, timeout=20, allow_redirects=True)
        if r.status_code != 200:
            return None
    except Exception:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Use shared auto-detect parser
    from bsip0_nutrition import extract_nutrition_raw_auto, parse_nutrition_rows, parse_nutrition_numeric as _pnn
    nutr_raw = extract_nutrition_raw_auto(soup)
    rows = nutr_raw.get("rows", [])
    if not rows:
        return None

    parsed_strings = parse_nutrition_rows(rows)
    nutr_dict = {
        "energy_kcal_raw": parsed_strings.get("energy", ""),
        "fat_raw":         parsed_strings.get("fat", ""),
        "saturated_fat_raw": parsed_strings.get("saturated_fat", ""),
        "carbs_raw":       parsed_strings.get("carbs", ""),
        "sugar_raw":       parsed_strings.get("sugar", ""),
        "fiber_raw":       parsed_strings.get("fiber", ""),
        "protein_raw":     parsed_strings.get("protein", ""),
        "sodium_raw":      parsed_strings.get("sodium", ""),
    }
    numeric = _pnn(nutr_dict)

    return {
        "source": "victory_search_page",
        "basis": nutr_raw.get("selection", {}).get("selected_basis", "unknown"),
        "nutrition_numeric": {k: v for k, v in numeric.items() if not k.startswith("_")},
    }


def _compare_nutrition(shuf: dict, victory: dict) -> dict:
    """
    Compare two per-100g numeric dicts. Flags fields where values differ by > 15%.
    Returns {"agree": bool, "discrepancies": list}
    """
    discrepancies = []
    keys_to_compare = ["energy_kcal", "carbohydrates_g", "fat_g", "protein_g"]
    for k in keys_to_compare:
        sv = shuf.get(k)
        vv = victory.get(k)
        if sv is None or vv is None:
            continue
        if sv == 0 and vv == 0:
            continue
        denom = max(abs(sv), abs(vv), 1.0)
        diff_pct = abs(sv - vv) / denom * 100
        if diff_pct > 15:
            discrepancies.append({
                "field": k,
                "shufersal": sv,
                "victory": vv,
                "diff_pct": round(diff_pct, 1),
            })
    return {"agree": len(discrepancies) == 0, "discrepancies": discrepancies}


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5: Build BSIP1
# ──────────────────────────────────────────────────────────────────────────────

_E_PATTERN = re.compile(r"E(\d{3,4}[a-z]?)", re.IGNORECASE)

_ADDITIVE_TERMS = [
    ("לציטין סויה", "emulsifier"),
    ("לציטין", "emulsifier"),
    ("מתחלב", "emulsifier"),
    ("חומרי טעם", "flavor_generic"),
    ("חומר תפיחה", "raising_agent"),
    ("מגביר חמיצות", "acidity_regulator"),
    ("חומצה", "acid"),
    ("צבע", "color"),
    ("חומר ייצוב", "stabilizer"),
    ("עמילן מתוקן", "modified_starch"),
    ("מולטודקסטרין", "maltodextrin"),
    ("מלטודקסטרין", "maltodextrin"),
    ("פולידקסטרוז", "polydextrose"),
    ("גליצרול", "humectant"),
]

_SWEETENER_TERMS = [
    ("סוכר", "added_sugar"),
    ("דבש", "honey"),
    ("סירופ גלוקוזה", "glucose_syrup"),
    ("מולסה", "molasses"),
    ("פרוקטוז", "fructose"),
    ("גלוקוז", "glucose"),
    ("מחית תמרים", "date_paste"),
    ("תמרים", "date"),
]


def _infer_nova(ing: str, e_nums: list) -> tuple[int, float, list[str]]:
    has_ultra = bool(re.search(
        r"(E\d{3}|מלטודקסטרין|פולידקסטרוז|גליצרול|עמילן מתוקן|חומצה לקטית|אינולין"
        r"|גלוקוז-פרוקטוז|סירופ גלוקוזה-פרוקטוז)", ing
    ))
    has_e_nums = len(e_nums) >= 2
    has_flavor = "חומרי טעם" in ing
    has_protein_isolate = bool(re.search(r"(חלבון סויה|חלבון חלב|חלבון אפונה|פרוטאין)", ing))

    if has_ultra or has_protein_isolate:
        return 4, 0.85, ["ultra_processing_markers_detected"]
    if has_e_nums or has_flavor:
        return 3, 0.75, ["additives_or_flavors_detected"]
    if len(ing) > 20:
        return 2, 0.65, ["minimal_processing_inferred"]
    return 3, 0.5, ["insufficient_ingredient_data"]


def build_bsip1(bsip0: dict, gate_result: dict) -> dict:
    barcode = bsip0["product_identity"]["barcode"]
    pid = f"bsip1_{barcode}"
    ing = bsip0.get("ingredients_raw", "")
    nutrition = gate_result.get("final_nutrition") or {}

    e_nums = list(set(_E_PATTERN.findall(ing)))
    extracted_additives = [{"term": f"E{e}", "category": "e_number", "position": 1} for e in e_nums]
    for term, cat in _ADDITIVE_TERMS:
        if term in ing:
            extracted_additives.append({"term": term, "category": cat, "position": 1})

    extracted_sweeteners = []
    for term, cat in _SWEETENER_TERMS:
        if term in ing:
            extracted_sweeteners.append({"term": term, "category": cat, "position": 1})

    nova_proxy, nova_conf, nova_notes = _infer_nova(ing, e_nums)

    if not ing:
        ing_quality, ing_warnings = "missing", ["ingredients_missing"]
    elif len(ing) < 10:
        ing_quality, ing_warnings = "minimal", ["ingredient_text_very_short"]
    else:
        ing_quality, ing_warnings = "clean", []

    has_full_nutrition = (
        all(nutrition.get(k) is not None for k in ["energy_kcal", "fat_g", "carbohydrates_g", "protein_g"])
        and gate_result.get("verdict") in ("pass", "converted_pass")
    )

    missing_fields = []
    if not nutrition.get("energy_kcal"):
        missing_fields.append("energy_kcal")
    if not bsip0["serving_info"].get("serving_size_g"):
        missing_fields.append("serving_size_g")

    serving = bsip0.get("serving_info", {})

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": bsip0["product_identity"].get("name"),
        "canonical_name_en": None,
        "brand": bsip0["product_identity"].get("brand"),
        "package_size_g": serving.get("package_size_g"),
        "unit_count": serving.get("unit_count"),
        "unit_size_g": serving.get("unit_size_g"),
        "serving_size_g": serving.get("serving_size_g"),
        "country_of_origin": None,
        "kosher_certification": None,
        "image_url": (bsip0["product_identity"].get("image_urls") or [None])[0],
        "source_retailers": ["shufersal"],
        "normalized_nutrition_per_100g": {
            "energy_kcal":        nutrition.get("energy_kcal"),
            "fat_g":              nutrition.get("fat_g"),
            "fat_saturated_g":    nutrition.get("fat_saturated_g"),
            "fat_trans_g":        nutrition.get("fat_trans_g"),
            "cholesterol_mg":     nutrition.get("cholesterol_mg"),
            "sodium_mg":          nutrition.get("sodium_mg"),
            "carbohydrates_g":    nutrition.get("carbohydrates_g"),
            "sugars_g":           nutrition.get("sugars_g"),
            "dietary_fiber_g":    nutrition.get("dietary_fiber_g"),
            "protein_g":          nutrition.get("protein_g"),
        },
        "energy_source_unit": "kcal",
        "ingredients_text_he": ing or None,
        "ingredients_list": [
            s.strip() for s in re.split(r"[,،]", ing) if s.strip()
        ][:20] if ing else [],
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims": [],
        "confidence": {
            "identity_confidence": "medium",
            "barcode_confidence": "high" if len(barcode) >= 12 else "medium",
            "nutrition_confidence": "confirmed_per_100g" if has_full_nutrition else "unconfirmed",
            "matched_by": "shufersal_product_page",
            "observation_count": 1,
        },
        "barcode_validation_status": "from_ld_json" if len(barcode) >= 12 else "inferred",
        "barcode_confidence_reason": "Extracted from Shufersal product page LD+JSON gtin13.",
        "nutrition_basis_claimed": bsip0["nutrition_raw"].get("basis_header"),
        "nutrition_basis_detected": gate_result.get("nutrition_basis"),
        "nutrition_basis_gate": gate_result.get("verdict"),
        "nutrition_basis_conversion_factor": gate_result.get("conversion_factor", 1.0),
        "nutrition_serving_g_used": gate_result.get("serving_g_used"),
        "nutrition_consistency_status": "consistent" if has_full_nutrition else "insufficient",
        "nutrition_consistency_warnings": gate_result.get("fail_reasons", []),
        "ingredient_text_quality": ing_quality,
        "ingredient_warnings": ing_warnings,
        "canonical_trust_score": 0.85 if has_full_nutrition else 0.45,
        "canonical_trust_level": "medium" if has_full_nutrition else "low",
        "canonical_risk_flags": (
            ["per_serving_converted"] if gate_result.get("verdict") == "converted_pass" else []
        ) + ["shufersal_single_source"],
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields": missing_fields,
        "inferred_fields": [],
        "audit_ref": f"bsip1_audit_{barcode}.json",
        "ingredients_raw": ing,
        "ingredients_raw_provenance": {
            "source": "shufersal_product_page",
            "bsip0_status": "bsip0_scrape",
            "populated_at": "bsip1_task360_shuf",
            "missing": not bool(ing),
            "note": "Direct scrape from Shufersal product page HTML. TASK-360 Shufersal re-scrape.",
        },
        "ingredient_order": [
            {"position": i + 1, "text": s.strip(), "percentage_declared": None, "has_subgroup": "(" in s}
            for i, s in enumerate(re.split(r"[,،]", ing)[:20])
            if s.strip()
        ] if ing else [],
        "extracted_additives": extracted_additives,
        "extracted_flavors": [{"term": "חומרי טעם", "category": "flavor_generic", "position": 1}]
                              if "חומרי טעם" in ing else [],
        "extracted_sweeteners": extracted_sweeteners,
        "extracted_protein_markers": [],
        "extracted_matrix_markers": [],
        "extracted_fermentation_markers": [],
        "extracted_roasting_markers": [],
        "enrichment_summary": {
            "ingredient_count_parsed": len(re.split(r"[,،]", ing)) if ing else 0,
            "additive_count": len(extracted_additives),
            "flavor_marker_count": 1 if "חומרי טעם" in ing else 0,
            "sweetener_count": len(extracted_sweeteners),
            "protein_marker_count": 0,
            "matrix_marker_count": 0,
            "fermentation_marker_count": 0,
            "roasting_marker_count": 0,
            "has_flavor_descriptor": False,
            "has_prebiotic_fiber": "אינולין" in ing or "FOS" in ing,
            "has_live_cultures": False,
            "has_protein_isolate_or_concentrate": bool(
                re.search(r"(חלבון סויה|חלבון חלב|חלבון אפונה|פרוטאין)", ing)
            ),
        },
        "enrichment_version": "bsip1_task360_shuf",
        "enrichment_warnings": ing_warnings,
        "nova_proxy": nova_proxy,
        "nova_confidence": nova_conf,
        "nova_confidence_band": "high" if nova_conf >= 0.8 else "medium",
        "nova_notes": nova_notes,
    }


# ──────────────────────────────────────────────────────────────────────────────
# STEP 6: BSIP2 scoring (unchanged engine)
# ──────────────────────────────────────────────────────────────────────────────

def run_bsip2(bsip1_dir: pathlib.Path, output_dir: pathlib.Path) -> tuple[list, list]:
    sys.path.insert(0, str(BSIP2_SRC))

    # Scoring flags from snacks.json config — UNCHANGED (TRIPWIRE-1)
    os.environ["BARI_SHELF_RELATIVE_V1"]         = "off"
    os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"]  = "off"
    os.environ["BARI_RECAL_P0"]                  = "off"
    os.environ["BARI_GRAD_SODIUM_V1"]            = "off"
    os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
    os.environ["BARI_REDLABEL_V1"]               = "off"
    os.environ["BARI_SODIUM_CEREAL"]             = "off"
    os.environ["BARI_FAT_TECH_V1"]              = "on"
    os.environ["BARI_GLASSBOX_W4"]              = "on"
    os.environ["BARI_TASK144_FIXES"]            = "off"

    try:
        from input_loader import load_batch
        from signal_extractor import extract_signals
        from router_v2 import classify_category
        from nova_proxy import infer_nova
        from evaluation_scope import assign_evaluation_scope
        from score_engine import score_product
        from trace_writer import assemble_trace, write_trace
        from structural_classifier import classify_structural_class
    except ImportError as e:
        log.error("BSIP2 engine import failed: %s", e)
        return [], [{"error": str(e), "phase": "import"}]

    products = load_batch(bsip1_dir)
    log.info("BSIP2: loaded %d products", len(products))

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            signals     = extract_signals(product)
            cat_result  = classify_category(product)
            l3          = signals["L3_inferred_classifications"]
            nova_result = infer_nova(product, l3)
            eval_result = assign_evaluation_scope(product, cat_result["category"])
            score_result = score_product(product, signals, cat_result, nova_result, eval_result)
            trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
            trace["structural_class"] = classify_structural_class(trace)
            write_trace(trace, output_dir)
            traces.append(trace)
            log.info("  %s  score=%s  grade=%s",
                     pid, trace.get("final_score_estimate"), trace.get("grade_estimate"))
        except Exception as e:
            log.error("  BSIP2 ERROR %s: %s", pid, e)
            errors.append({"product_id": pid, "error": str(e)})

    log.info("BSIP2: scored=%d errors=%d", len(traces), len(errors))
    return traces, errors


# ──────────────────────────────────────────────────────────────────────────────
# STEP 7: Frontend JSON
# ──────────────────────────────────────────────────────────────────────────────

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def _score_to_grade(score) -> str | None:
    if score is None:
        return None
    for g, t in GRADE_SCALE:
        if score >= t:
            return g
    return "E"


DIMENSION_LABEL_MAP = {
    "processing_quality": "רמת עיבוד",
    "nutrient_density": "ערך תזונתי",
    "calorie_density": "צפיפות קלורית",
    "glycemic_quality": "איכות גליקמית",
    "protein_quality": "חלבון",
    "additive_quality": "תוספים",
    "satiety_support": "תחושת שובע",
    "fat_quality": "איכות שומן",
    "regulatory_quality": "איכות רגולטורית",
    "whole_food_integrity": "שלמות מזון",
}
DIMENSION_ORDER = [
    "processing_quality", "additive_quality", "nutrient_density", "protein_quality",
    "calorie_density", "glycemic_quality", "fat_quality", "satiety_support",
    "regulatory_quality", "whole_food_integrity",
]


def _build_bari_interpretation(trace: dict) -> list:
    dim_scores = trace.get("dimension_scores") or {}
    result = []
    for key in DIMENSION_ORDER:
        label = DIMENSION_LABEL_MAP.get(key, key)
        raw = dim_scores.get(key)
        sf = None
        if raw is not None:
            try:
                sf = float(raw)
                sf = round(sf, 1) if 0 <= sf <= 100 else None
            except (TypeError, ValueError):
                sf = None
        strength = (
            "data not available" if sf is None
            else ("חזק" if sf >= 80 else ("בינוני" if sf >= 50 else "נמוך"))
        )
        result.append({
            "interpretation": "PENDING_COPY",
            "key": key,
            "label": label,
            "score": sf,
            "strength": strength,
        })
    return result


def build_frontend_json(
    traces: list,
    bsip1_dir: pathlib.Path,
    gate_results: dict,
    quarantined: list,
    victory_crosschecks: dict,
) -> dict:
    """Build snacks_frontend_v4.json. All copy fields = PENDING_COPY."""
    config_sha = (
        hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest()
        if CONFIG_PATH.exists() else "N/A"
    )

    # Load BSIP1 corpus
    corpus: dict[str, dict] = {}
    for f in bsip1_dir.glob("bsip1_*.json"):
        if "audit" in f.name:
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            bc = str(rec.get("barcode", ""))
            if bc:
                corpus[bc] = rec
        except Exception:
            pass

    # Index traces by barcode
    trace_by_bc: dict[str, dict] = {}
    for trace in traces:
        ref = trace.get("input_reference") or {}
        bc = str(ref.get("barcode") or "")
        if bc:
            trace_by_bc[bc] = trace
        # Also try canonical_product_id → strip "bsip1_" prefix
        pid = ref.get("canonical_product_id") or ""
        if pid.startswith("bsip1_"):
            bc2 = pid[len("bsip1_"):]
            if bc2 and bc2 not in trace_by_bc:
                trace_by_bc[bc2] = trace

    products_out = []
    for bc, trace in sorted(
        trace_by_bc.items(),
        key=lambda x: -(x[1].get("final_score_estimate") or 0)
    ):
        crec = corpus.get(bc, {})
        score = trace.get("final_score_estimate")
        grade = _score_to_grade(score)
        name = crec.get("canonical_name_he") or ""
        image_url = crec.get("image_url")
        nn = crec.get("normalized_nutrition_per_100g") or {}

        gate = gate_results.get(bc, {})
        basis = gate.get("nutrition_basis", "per_100g")
        verdict = gate.get("verdict", "pass")
        conv_factor = gate.get("conversion_factor", 1.0)

        has_full = all(
            nn.get(k) is not None
            for k in ["energy_kcal", "fat_g", "carbohydrates_g", "protein_g"]
        )
        confidence = "full" if has_full else "partial"
        confidence_label_he = "נתונים מאומתים" if has_full else "נתונים בבדיקה"
        confidence_tooltip_he = (
            "הנתונים מאומתים ממקור ישיר (שופרסל). הציון מבוסס על נתוני תזונה ורכיבים מלאים."
            if has_full else
            "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן."
        )

        nutrition_display = {
            "energyKcal": nn.get("energy_kcal"),
            "protein":    nn.get("protein_g"),
            "sugar":      nn.get("sugars_g"),
            "fat":        nn.get("fat_g"),
            "fiber":      nn.get("dietary_fiber_g"),
            "sodium":     nn.get("sodium_mg"),
        }

        note_parts = ["ל-100 גרם"]
        if verdict == "converted_pass":
            note_parts.append(
                f"(המרה מ-{gate.get('serving_g_used', '?')}ג׳ מנה, ×{conv_factor:.3g})"
            )
        serving_note = " ".join(note_parts)

        # Victory cross-check note
        cc = victory_crosschecks.get(bc)
        victory_note = None
        if cc:
            if cc.get("agree"):
                victory_note = "victory_crosscheck:agree"
            elif cc.get("discrepancies"):
                discreps = cc["discrepancies"]
                victory_note = f"victory_crosscheck:disagree:{len(discreps)}_fields"
                log.warning("  Victory cross-check disagrees on %s: %s", bc, discreps)

        bari_interp = _build_bari_interpretation(trace)

        expansion = {
            "bottomLine": "PENDING_COPY",
            "comparisonContext": "PENDING_COPY",
            "confidenceLabel": confidence_label_he,
            "consumerExplanation": {
                "context": "PENDING_COPY",
                "good": ["PENDING_COPY"],
                "takeaway": "PENDING_COPY",
                "watchOut": [],
                "whyRated": "PENDING_COPY",
            },
            "ingredients": crec.get("ingredients_text_he"),
            "limitingFactors": ["PENDING_COPY"],
            "nutrition": nutrition_display,
            "positiveSignals": ["PENDING_COPY"],
            "servingNote": serving_note,
            "unknowns": [],
            "_nutrition_basis": basis,
            "_gate_verdict": verdict,
            "_victory_crosscheck": victory_note,
        }

        products_out.append({
            "bariInterpretation": bari_interp,
            "barcode": bc,
            "bestUseCases": ["PENDING_COPY"],
            "confidence": confidence,
            "confidence_label_he": confidence_label_he,
            "confidence_sub_reason": None if has_full else "incomplete_nutrition",
            "confidence_tooltip_he": confidence_tooltip_he,
            "consumerTakeaway": "PENDING_COPY",
            "d4_additives": [],
            "expansion": expansion,
            "grade": grade,
            "imageUrl": image_url,
            "insightLine": "PENDING_COPY",
            "name": name,
            "retailer": "shufersal",
            "rowVerdict": "PENDING_COPY",
            "score": score,
            "source_traceability_status": "resolved",
        })

    from collections import Counter
    grade_dist = dict(Counter(p["grade"] for p in products_out if p.get("grade")))

    quarantine_entries = [
        {
            "barcode": q["barcode"],
            "name": q.get("name"),
            "reason": "plausibility_gate_fail",
            "gate_fails": q.get("fail_reasons", []),
            "accounted_mass_g": q.get("accounted_mass"),
            "kcal": q.get("kcal"),
        }
        for q in quarantined
    ]

    meta = {
        "category": "snacks",
        "config_sha256": config_sha,
        "display_count": len(products_out),
        "generated": now_iso(),
        "generator_version": "TASK-360-shufersal-rescrape-v1.0",
        "grade_distribution": grade_dist,
        "off_check": "PASS — 0 products use Open Food Facts. OFF banned project-wide. All nutrition from Shufersal direct product page scrape.",
        "pending_copy_fields": [
            "insightLine", "rowVerdict", "consumerTakeaway",
            "bariInterpretation.interpretation",
            "expansion.consumerExplanation", "expansion.comparisonContext",
            "expansion.bottomLine", "expansion.positiveSignals",
            "expansion.limitingFactors", "bestUseCases",
        ],
        "product_count": len(products_out),
        "schema": "BariProductVM[]",
        "schema_version": "v4",
        "scope_note": "ניתוח מדף שופרסל — לא סקר שוק ישראלי כולל. TASK-360 re-scrape מ-Shufersal.",
        "source_run": RUN_ID,
        "primary_source": "shufersal",
        "cross_check_source": "victory",
        "staging_note": (
            "TASK-360 Shufersal re-scrape + plausibility gate. "
            "Nutrition corrected from per-serving to per-100g where applicable. "
            "Consumer copy NOT done — separate voice pass required. "
            "Do NOT deploy without copy review + adversarial QA."
        ),
        "quarantined_products": quarantine_entries,
        "quarantine_count": len(quarantined),
        "scoring_engine_unchanged": "TRIPWIRE-1 compliant — no changes to 03_operations/bsip2/** or page_generator configs",
        "editorial_note": (
            "הערת קטגוריה: קטגוריית חטיפי הדגנים היא מדף פינוק — כל המוצרים הם חטיפים מעובדים. "
            "הציונים מדרגים חטיף מול חטיף בלבד. ציון גבוה אינו אישור לאכול יותר."
        ),
    }

    return {"_meta": meta, "products": products_out}


# ──────────────────────────────────────────────────────────────────────────────
# Main pipeline
# ──────────────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 70)
    log.info("TASK-360 Snacks Re-Scrape — Shufersal primary + Victory cross-check")
    log.info("Run ID: %s", RUN_ID)
    log.info("=" * 70)

    # ── Sanity-check: verify Shufersal is reachable ────────────────────────────
    log.info("\n--- REACHABILITY CHECK ---")
    probe = _get(f"{BASE}/online/he/", timeout=20)
    if not probe or probe.status_code >= 400:
        print(f"\nFATAL: Shufersal unreachable (status={getattr(probe, 'status_code', 'ERR')}). "
              f"Cannot proceed — TASK-360 hard rule: stop and report if primary blocked.",
              file=sys.stderr)
        sys.exit(2)
    log.info("Shufersal: reachable (HTTP %d, %.1f KB)", probe.status_code, len(probe.content)/1024)

    vic_reachable = _victory_reachable()
    log.info("Victory: %s", "reachable" if vic_reachable else "UNREACHABLE (cross-check will be skipped)")

    # ── STEP 1: Discover ───────────────────────────────────────────────────────
    log.info("\n--- STEP 1: Shufersal Discovery ---")
    candidates = discover_shufersal()
    save_json(BSIP0_DIR / "all_discovered.json", [
        {**v, "code": k} for k, v in candidates.items()
    ])
    log.info("Discovered: %d unique snack candidates", len(candidates))

    if not candidates:
        print("FATAL: 0 snack candidates discovered from Shufersal. Check search queries / category URLs.",
              file=sys.stderr)
        sys.exit(2)

    # ── STEP 2: Scrape product pages ───────────────────────────────────────────
    log.info("\n--- STEP 2: Scrape Shufersal product pages ---")
    scrape_results = []

    for code, meta in candidates.items():
        name = meta.get("name", "")[:60]
        log.info("  Scraping: %s | %s", code, name)
        product_dir = BSIP0_DIR / code
        product_dir.mkdir(parents=True, exist_ok=True)

        bsip0_record = scrape_shufersal_product(code, meta)
        if bsip0_record is None:
            log.warning("  FAILED: %s | %s", code, name)
            scrape_results.append({
                "code": code, "barcode": "", "name": name, "status": "scrape_failed",
            })
            save_json(BSIP0_DIR / "scrape_progress.json", scrape_results)
            time.sleep(PRODUCT_DELAY)
            continue

        # Save raw BSIP0
        save_json(product_dir / "product.json", bsip0_record)

        barcode = bsip0_record["product_identity"]["barcode"]
        nutr_numeric = bsip0_record["nutrition_numeric_per_100g"]
        ing = bsip0_record.get("ingredients_raw", "")
        serving_info = bsip0_record.get("serving_info", {})

        # ── STEP 3: Parse serving size already done in scrape_shufersal_product ──
        # serving_info is embedded in bsip0_record

        # ── STEP 4 (inline): Plausibility gate ────────────────────────────────
        gate_result = plausibility_gate(nutr_numeric, serving_info, ing, barcode)

        # Attach gate to BSIP0 record and re-save
        bsip0_record["plausibility_gate"] = gate_result
        save_json(product_dir / "product.json", bsip0_record)

        scrape_results.append({
            "code": code,
            "barcode": barcode,
            "name": bsip0_record["product_identity"].get("name", name),
            "status": "scraped_ok",
            "gate_verdict": gate_result["verdict"],
            "accounted_mass": gate_result.get("accounted_mass"),
            "kcal": gate_result.get("kcal"),
            "fail_reasons": gate_result.get("fail_reasons", []),
            "nutrition_basis": gate_result.get("nutrition_basis"),
            "conversion_factor": gate_result.get("conversion_factor", 1.0),
        })

        log.info("    barcode=%s gate=%s acc=%.1fg kcal=%s",
                 barcode, gate_result["verdict"],
                 gate_result.get("accounted_mass", 0),
                 gate_result.get("kcal"))

        save_json(BSIP0_DIR / "scrape_progress.json", scrape_results)
        time.sleep(PRODUCT_DELAY)

    save_json(BSIP0_DIR / "scrape_results.json", scrape_results)

    # ── Victory cross-check (STEP 4b) ──────────────────────────────────────────
    log.info("\n--- STEP 4b: Victory cross-check ---")
    victory_crosschecks: dict = {}
    crosscheck_count = 0

    if vic_reachable:
        # Only cross-check products that passed the gate (don't waste time on quarantined)
        passed_results = [r for r in scrape_results if r["status"] == "scraped_ok"
                          and r.get("gate_verdict") in ("pass", "converted_pass")]
        log.info("Cross-checking %d passed products with Victory", len(passed_results))

        for res in passed_results[:30]:  # cap at 30 to keep runtime manageable
            bc = res["barcode"]
            if not bc:
                continue
            try:
                cc = _try_victory_product(bc)
                if cc and cc.get("nutrition_numeric"):
                    crosscheck_count += 1
                    # Load the Shufersal per-100g nutrition for comparison
                    bsip0_path = BSIP0_DIR / res["code"] / "product.json"
                    shuf_nutr = {}
                    if bsip0_path.exists():
                        bsip0_data = json.loads(bsip0_path.read_text(encoding="utf-8"))
                        gate = bsip0_data.get("plausibility_gate", {})
                        shuf_nutr = gate.get("final_nutrition") or {}

                    comparison = _compare_nutrition(shuf_nutr, cc["nutrition_numeric"])
                    victory_crosschecks[bc] = {
                        **comparison,
                        "victory_basis": cc.get("basis"),
                        "victory_nutrition": cc["nutrition_numeric"],
                    }
                    if not comparison["agree"]:
                        log.warning("  Victory disagrees for %s: %s", bc, comparison["discrepancies"])
                    else:
                        log.info("  Victory agrees for %s", bc)
                time.sleep(0.5)
            except Exception as e:
                log.warning("  Victory cross-check error for %s: %s", bc, e)
    else:
        log.info("Victory unreachable — cross-check skipped")

    save_json(BSIP0_DIR / "victory_crosschecks.json", victory_crosschecks)
    log.info("Victory cross-checks completed: %d products found on Victory", crosscheck_count)

    # ── STEP 5: Build BSIP1 ────────────────────────────────────────────────────
    log.info("\n--- STEP 5: Build BSIP1 ---")
    quarantined = []
    gate_results_by_bc: dict = {}
    bsip1_built = 0

    for res in scrape_results:
        if res["status"] != "scraped_ok":
            continue

        bc = res["barcode"]
        gate_verdict = res.get("gate_verdict")
        code = res["code"]

        if gate_verdict == "quarantine":
            quarantined.append({
                "barcode": bc,
                "name": res.get("name"),
                "fail_reasons": res.get("fail_reasons", []),
                "accounted_mass": res.get("accounted_mass"),
                "kcal": res.get("kcal"),
            })
            log.warning("  QUARANTINE: %s | %s", bc, "; ".join(res.get("fail_reasons", [])))
            continue

        bsip0_path = BSIP0_DIR / code / "product.json"
        if not bsip0_path.exists():
            log.warning("  No BSIP0 record at %s — skip", bsip0_path)
            continue

        bsip0_data = json.loads(bsip0_path.read_text(encoding="utf-8"))
        gate_result = bsip0_data.get("plausibility_gate", {})
        gate_results_by_bc[bc] = gate_result

        bsip1_rec = build_bsip1(bsip0_data, gate_result)
        bsip1_path = BSIP1_DIR / f"bsip1_{bc}.json"
        save_json(bsip1_path, bsip1_rec)
        bsip1_built += 1
        log.info("  BSIP1: %s | %s", bc, (bsip1_rec.get("canonical_name_he") or "")[:50])

    log.info("BSIP1 built: %d | Quarantined: %d", bsip1_built, len(quarantined))

    # ── STEP 6: BSIP2 ─────────────────────────────────────────────────────────
    log.info("\n--- STEP 6: BSIP2 scoring (unchanged engine) ---")
    traces, bsip2_errors = run_bsip2(BSIP1_DIR, BSIP2_DIR)

    # ── STEP 7: Frontend JSON ──────────────────────────────────────────────────
    log.info("\n--- STEP 7: Build frontend JSON ---")
    frontend = build_frontend_json(
        traces, BSIP1_DIR, gate_results_by_bc, quarantined, victory_crosschecks
    )
    save_json(FRONTEND_PATH, frontend)
    log.info("Frontend JSON: %s (%d products)", FRONTEND_PATH, len(frontend["products"]))

    # ── Run record ────────────────────────────────────────────────────────────
    total_attempts  = len([r for r in scrape_results])
    total_scraped   = len([r for r in scrape_results if r["status"] == "scraped_ok"])
    total_failed    = len([r for r in scrape_results if r["status"] == "scrape_failed"])
    passed_direct   = len([r for r in scrape_results if r.get("gate_verdict") == "pass"])
    passed_conv     = len([r for r in scrape_results if r.get("gate_verdict") == "converted_pass"])
    total_quarant   = len(quarantined)
    scored          = len(traces)

    log.info("\n" + "=" * 70)
    log.info("PIPELINE SUMMARY — TASK-360 (Shufersal)")
    log.info("=" * 70)
    log.info("Candidates discovered:       %d", len(candidates))
    log.info("Scrape attempts:             %d", total_attempts)
    log.info("Scraped OK:                  %d", total_scraped)
    log.info("Scrape failed:               %d", total_failed)
    log.info("Passed gate (direct):        %d", passed_direct)
    log.info("Passed gate (converted):     %d", passed_conv)
    log.info("Quarantined:                 %d", total_quarant)
    log.info("BSIP1 built:                 %d", bsip1_built)
    log.info("BSIP2 scored:                %d", scored)
    log.info("BSIP2 errors:                %d", len(bsip2_errors))
    log.info("Victory cross-checks:        %d", crosscheck_count)
    log.info("Frontend products:           %d", len(frontend["products"]))

    if quarantined:
        log.info("\nQuarantined:")
        for q in quarantined:
            log.info("  %s | %s | %s",
                     q["barcode"], (q.get("name") or "")[:30],
                     "; ".join(q.get("fail_reasons", [])))

    if bsip2_errors:
        log.info("\nBSIP2 errors:")
        for e in bsip2_errors:
            log.info("  %s: %s", e.get("product_id"), e.get("error", "")[:80])

    run_record = {
        "run_id": RUN_ID,
        "run_timestamp": now_iso(),
        "task": "TASK-360",
        "pipeline": "snacks_rescrape_shufersal_plausibility_gate",
        "primary_source": "shufersal",
        "cross_check_source": "victory" if vic_reachable else "victory_unreachable",
        "shufersal_reachable": True,
        "victory_reachable": vic_reachable,
        "candidates_discovered": len(candidates),
        "scrape_attempts": total_attempts,
        "scraped_ok": total_scraped,
        "scrape_failed": total_failed,
        "passed_gate_direct": passed_direct,
        "passed_gate_converted": passed_conv,
        "quarantined": total_quarant,
        "bsip1_built": bsip1_built,
        "bsip2_scored": scored,
        "bsip2_errors": len(bsip2_errors),
        "victory_crosschecks": crosscheck_count,
        "frontend_products": len(frontend["products"]),
        "quarantined_detail": quarantined,
        "bsip2_error_detail": bsip2_errors,
        "output_paths": {
            "bsip0_dir":      str(BSIP0_DIR),
            "bsip1_dir":      str(BSIP1_DIR),
            "bsip2_dir":      str(BSIP2_DIR),
            "frontend_json":  str(FRONTEND_PATH),
        },
        "scoring_engine_tripwire_check": (
            "TRIPWIRE-1 COMPLIANT — no changes to 03_operations/bsip2/** or page_generator configs. "
            "Score changes result only from corrected per-100g nutrition flowing through unchanged engine."
        ),
        "off_check": "PASS — no Open Food Facts used in any field",
    }
    save_json(BSIP0_DIR / "run_record.json", run_record)
    save_json(BSIP2_DIR / "run_record.json", run_record)

    log.info("\nRun record: %s", BSIP0_DIR / "run_record.json")
    log.info("TASK-360 Shufersal pipeline complete.")

    return run_record


if __name__ == "__main__":
    main()
