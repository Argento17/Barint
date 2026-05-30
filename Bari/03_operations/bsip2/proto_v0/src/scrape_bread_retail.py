"""
Real Retailer Bread/Cracker Corpus — Scraper & BSIP1 Converter
run_id: real_bread_retail_001

Source: Open Food Facts public API (openfoodfacts.org)
  - Real barcodes, real Hebrew ingredient lists, real nutrition tables
  - Products sold in Israel (Israeli barcodes 729xxxxxxx + imports)
  - Provenance: source_url = OFF product page for each item

Fetch strategy:
  - Category queries: breads, crackers, crispbreads, rye-breads,
    wholemeal-breads, flatbreads, rice-cakes, seed-crackers
  - Keyword queries in Hebrew: לחם, קרקר, מחמצת, כוסמין, שיפון, לחמי קריספ
  - Deduplication by barcode
  - Relevance filter: exclude meat, dairy-primary, dessert, snack-bar

Output:
  raw/           — one JSON per product (OFF raw response preserved)
  bsip1/         — BSIP1-format product files for pipeline ingestion
  scrape_log.json — per-product provenance + quality flags
"""

from __future__ import annotations
import json
import time
import re
import pathlib
import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = pathlib.Path(r"C:\Bari\02_products\bread_retail")
RAW_DIR   = BASE_DIR / "raw"
BSIP1_DIR = BASE_DIR / "bsip1"
for d in (RAW_DIR, BSIP1_DIR, BASE_DIR / "bsip2", BASE_DIR / "reports"):
    d.mkdir(parents=True, exist_ok=True)

RUN_ID    = "real_bread_retail_001"
SCRAPE_TS = datetime.datetime.utcnow().isoformat() + "Z"
OFF_BASE  = "https://world.openfoodfacts.org/cgi/search.pl"

# ---------------------------------------------------------------------------
# Search plan
# ---------------------------------------------------------------------------
CATEGORY_QUERIES = [
    "breads",
    "crackers",
    "crispbreads",
    "rye-breads",
    "wholemeal-breads",
    "flatbreads",
    "rice-cakes",
    "seed-crackers",
    "sourdough-breads",
    "whole-grain-breads",
    "gluten-free-breads",
    "pitas",
    "rye-crispbreads",
    "whole-wheat-breads",
    "multigrain-breads",
    "protein-breads",
    "low-carb-breads",
]

KEYWORD_QUERIES = [
    # Hebrew
    "לחם",              # bread
    "קרקר",             # cracker
    "מחמצת",            # sourdough
    "כוסמין",           # spelt
    "שיפון",            # rye
    "לחמי קריספ",       # crispbread
    "אורז מלא",         # brown rice
    "לחם חיטה מלאה",    # whole wheat
    "לחם כוסמין",       # spelt bread
    "לחם שיפון",        # rye bread
    "לחם לבן",          # white bread
    "לחמניה",           # roll
    "פיתה",             # pita
    "חלה",              # challah
    "מצה",              # matza
    "לחם קל",           # light bread
    "לחם סיבים",        # fiber bread
    "לחם חלבון",        # protein bread
    "לחם ללא גלוטן",    # gluten-free
    "קרקר שיפון",       # rye cracker
    "קרקר דיאטה",       # diet cracker
    # English (for import brands sold in Israel)
    "bread",
    "cracker",
    "crispbread",
    "rye bread",
    "sourdough",
    "rice cake",
    "matzo",
    "wasa",
    "whole wheat bread",
    "pita",
]

BRAND_QUERIES = [
    # Major Israeli bread brands
    "אנג'ל",            # Angel — largest Israeli bread company
    "ברמן",             # Berman bakeries
    "לחמנו",            # Lechem Lanu artisan
    "יחיאל",            # Yechiel
    "אחים חסין",        # Hassin brothers
    "חסין",             # Hassin
    "הלחם",             # HaLechem
    "גיא",              # Gai (bakery)
    "בית הלחם",         # Beit HaLechem
    "אינבר",            # Einbar
    "אנג׳ל",            # Angel (alternate spelling)
    # Cracker / crispbread brands sold in Israel
    "וואסה",            # Wasa (Swedish crispbread)
    "ריוויטה",          # Ryvita
    "ויקינג",           # Viking
    "דיאטן",            # Dietan crackers
    "ויטה מין",         # Vitamins crackers
    "פיני",             # Pini crackers
    "אוסם",             # Osem (makes crackers)
    "שטראוס",           # Strauss
    "יופלה",            # Yotvata
]

# ---------------------------------------------------------------------------
# Relevance: EXCLUDE anything primarily from these categories
# ---------------------------------------------------------------------------
_EXCLUDE_CATS = {
    "meat", "beef", "chicken", "fish", "seafood", "dairy",
    "yogurts", "cheeses", "milk", "butter", "cream",
    "cakes", "cookies", "pastries", "desserts", "chocolates",
    "snack-bars", "granola-bars", "energy-bars", "beverages",
    "juices", "soft-drinks", "water", "soups",
    "pasta", "rice", "cereals", "muesli",
    "fruits", "vegetables", "nuts", "oils",
    "condiments", "sauces", "spreads", "jams",
    "protein-powders", "dietary-supplements",
}

_INCLUDE_CATS = {
    "breads", "bread", "crackers", "cracker", "crispbreads", "crispbread",
    "rye-breads", "wholemeal-breads", "flatbreads", "rice-cakes",
    "seed-crackers", "sourdough-breads", "whole-grain-breads",
    "gluten-free-breads", "pitas", "pitot", "lavash",
    "toasts", "rusk",
}

_EXCLUDE_NAME_KW = [
    "שניצל", "קציצ", "בשר", "דג", "עוף", "עגל", "כבש",
    "גלידה", "עוגה", "עוגיה", "פחזנית", "בורקס",
    "חלב", "גבינה", "יוגורט", "שמנת",
    "קפה", "תה", "מיץ", "שתייה", "קולה",
    "פסטה", "אורז", "קינואה",
]

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------
_SESSION = requests.Session()
_SESSION.headers.update({
    "User-Agent": "BariProject/1.0 (bari-nutrition-research; tbarhaim@gmail.com)"
})

def _get_json(params: dict, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            r = _SESSION.get(OFF_BASE, params=params, timeout=25)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            wait = 3 * (2 ** attempt)
            log.warning("Request failed (attempt %d/%d): %s — retry in %ds", attempt + 1, retries, e, wait)
            time.sleep(wait)
    return {}


def fetch_by_category(category: str, page: int = 1, page_size: int = 100) -> dict:
    return _get_json({
        "tagtype_0":     "categories",
        "tag_contains_0": "contains",
        "tag_0":         category,
        "tagtype_1":     "countries",
        "tag_contains_1": "contains",
        "tag_1":         "Israel",
        "action":        "process",
        "json":          1,
        "page_size":     page_size,
        "page":          page,
    })


def fetch_by_keyword(term: str, page: int = 1, page_size: int = 100) -> dict:
    return _get_json({
        "search_terms": term,
        "action":       "process",
        "json":         1,
        "countries":    "Israel",
        "page_size":    page_size,
        "page":         page,
    })


def fetch_by_brand(brand: str, page: int = 1, page_size: int = 100) -> dict:
    return _get_json({
        "tagtype_0":      "brands",
        "tag_contains_0": "contains",
        "tag_0":          brand,
        "tagtype_1":      "countries",
        "tag_contains_1": "contains",
        "tag_1":          "Israel",
        "action":         "process",
        "json":           1,
        "page_size":      page_size,
        "page":           page,
    })


# ---------------------------------------------------------------------------
# Relevance filter
# ---------------------------------------------------------------------------
def _is_relevant(raw: dict) -> bool:
    name = (raw.get("product_name_he") or raw.get("product_name") or "").lower()
    cats_str = (raw.get("categories") or raw.get("categories_tags") or "").lower()
    if isinstance(raw.get("categories_tags"), list):
        cats_str = " ".join(raw["categories_tags"]).lower()

    for kw in _EXCLUDE_NAME_KW:
        if kw in name:
            return False

    has_include = any(c in cats_str for c in _INCLUDE_CATS)
    has_exclude = any(c in cats_str for c in _EXCLUDE_CATS)

    if has_exclude and not has_include:
        return False

    # If no category signal at all, accept if name contains bread/cracker keyword
    if not has_include and not has_exclude:
        bread_kw = ["לחם", "קרקר", "קריספ", "פיתה", "לביבה", "מצה", "לחמניה", "חלה"]
        return any(kw in name for kw in bread_kw)

    return True


# ---------------------------------------------------------------------------
# Nutrition conversion: OFF → BSIP1
# ---------------------------------------------------------------------------
def _nn(raw: dict) -> dict:
    nm = raw.get("nutriments") or {}

    def g(key: str):
        for k in (key, key.replace("-", "_")):
            v = nm.get(f"{k}_100g") or nm.get(k)
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return None
        return None

    kcal = g("energy-kcal") or g("energy_kcal")
    if kcal is None:
        kj = g("energy-kj") or g("energy_kj") or g("energy")
        if kj is not None:
            kcal = round(float(kj) / 4.184, 1)

    sodium_g  = g("sodium")
    sodium_mg = round(sodium_g * 1000, 1) if sodium_g is not None else None

    fat_trans = g("trans-fat") or g("trans_fat")

    return {
        "energy_kcal":      round(kcal, 1) if kcal is not None else None,
        "fat_g":            g("fat"),
        "fat_saturated_g":  g("saturated-fat") or g("saturated_fat"),
        "fat_trans_g":      fat_trans,
        "sodium_mg":        sodium_mg,
        "carbohydrates_g":  g("carbohydrates"),
        "sugars_g":         g("sugars"),
        "dietary_fiber_g":  g("fiber"),
        "protein_g":        g("proteins"),
        "cholesterol_mg":   g("cholesterol"),
    }


# ---------------------------------------------------------------------------
# Ingredient parsing
# ---------------------------------------------------------------------------
_ING_SPLIT = re.compile(r"[,;،]|\band\b")

def _parse_ingredients(text: str) -> list[str]:
    if not text:
        return []
    parts = _ING_SPLIT.split(text)
    result = []
    for p in parts:
        p = p.strip().strip("()[].")
        if len(p) > 1:
            result.append(p)
    return result


def _parse_ingredient_order(ing_text: str) -> list[dict]:
    parts = [p.strip() for p in _ING_SPLIT.split(ing_text) if p.strip()]
    order = []
    for i, part in enumerate(parts, 1):
        pct = None
        m = re.search(r"\((\d+(?:\.\d+)?)\s*%\)", part)
        if m:
            pct = float(m.group(1))
        order.append({
            "position":            i,
            "text":                part,
            "percentage_declared": pct,
            "has_subgroup":        "(" in part and ")" in part and pct is None,
        })
    return order


# ---------------------------------------------------------------------------
# Quality scoring
# ---------------------------------------------------------------------------
def _quality_flags(raw: dict, nn: dict) -> tuple[float, list[str]]:
    flags: list[str] = []
    score = 1.0

    name = raw.get("product_name_he") or raw.get("product_name") or ""
    if not name:
        flags.append("missing_product_name_he")
        score -= 0.2
    elif len(name.split()) <= 1:
        flags.append("product_name_very_short")
        score -= 0.05

    ing_he = raw.get("ingredients_text_he") or ""
    ing_en = raw.get("ingredients_text") or ""
    if not ing_he and not ing_en:
        flags.append("ingredients_text_missing")
        score -= 0.25
    elif not ing_he:
        flags.append("ingredients_text_he_missing_has_other")
        score -= 0.10

    nn_present = sum(1 for v in nn.values() if v is not None)
    if nn_present == 0:
        flags.append("nutrition_entirely_missing")
        score -= 0.40
    elif nn.get("energy_kcal") is None:
        flags.append("kcal_missing")
        score -= 0.10
    if nn.get("dietary_fiber_g") is None:
        flags.append("fiber_missing")
        score -= 0.05
    if nn.get("carbohydrates_g") is None:
        flags.append("carbohydrates_missing")
        score -= 0.10

    stores = raw.get("stores") or ""
    if not stores:
        flags.append("retailer_unknown")

    if not raw.get("image_url") and not raw.get("image_front_url"):
        flags.append("image_missing")

    return max(0.0, round(score, 2)), flags


# ---------------------------------------------------------------------------
# BSIP1 converter
# ---------------------------------------------------------------------------
def _missing_fields(nn: dict, has_ing: bool) -> list[str]:
    missing = []
    for k, v in nn.items():
        if v is None:
            missing.append(k)
    if not has_ing:
        missing.append("ingredients_text_he")
    return missing


def to_bsip1(raw: dict, scrape_quality_score: float, quality_flags: list[str]) -> dict:
    barcode   = str(raw.get("code") or raw.get("id") or "")
    name_he   = (raw.get("product_name_he") or raw.get("product_name") or "").strip()
    name_en   = (raw.get("product_name_en") or raw.get("generic_name") or "").strip() or None
    brand     = (raw.get("brands") or "").split(",")[0].strip()
    quantity  = raw.get("quantity") or raw.get("serving_size") or None
    stores    = [s.strip() for s in (raw.get("stores") or "").split(",") if s.strip()]
    image_url = raw.get("image_url") or raw.get("image_front_url") or None
    allergens = [a.replace("en:", "").replace("he:", "") for a in
                 (raw.get("allergens_tags") or [])]
    labels    = raw.get("labels") or ""
    claims: list[str] = [l.strip() for l in labels.split(",") if l.strip()]
    off_url   = f"https://world.openfoodfacts.org/product/{barcode}/"

    ing_he   = (raw.get("ingredients_text_he") or "").strip()
    ing_text = ing_he or (raw.get("ingredients_text") or "").strip()
    ing_list = _parse_ingredients(ing_text)
    ing_order = _parse_ingredient_order(ing_text)

    nn = _nn(raw)
    missing = _missing_fields(nn, bool(ing_text))

    trust_score = round(scrape_quality_score * 0.8 + 0.1, 2)
    trust_level = "high" if trust_score >= 0.75 else ("medium" if trust_score >= 0.50 else "low")

    pid = f"bsip1_bread_retail_{barcode}"

    cats_raw = raw.get("categories") or ""
    if isinstance(raw.get("categories_tags"), list):
        cats_raw = ", ".join(raw["categories_tags"])

    return {
        "schema_version":          "bsip1_v0_1",
        "file_type":               "product",
        "canonical_product_id":    pid,
        "barcode":                 barcode,
        "canonical_name_he":       name_he,
        "canonical_name_en":       name_en,
        "brand":                   brand,
        "package_size_g":          None,
        "quantity_raw":            quantity,
        "unit_count":              None,
        "unit_size_g":             None,
        "serving_size_g":          None,
        "country_of_origin":       None,
        "kosher_certification":    None,
        "image_url":               image_url,
        "source_retailers":        stores if stores else ["open_food_facts_israel"],
        "source_url":              off_url,
        "off_categories":          cats_raw,
        "normalized_nutrition_per_100g": {
            **{k: None for k in ["energy_kcal","fat_g","fat_saturated_g","fat_trans_g",
                                  "sodium_mg","carbohydrates_g","sugars_g",
                                  "dietary_fiber_g","protein_g","cholesterol_mg"]},
            **nn,
        },
        "energy_source_unit":          "kcal",
        "ingredients_text_he":         ing_he,
        "ingredients_list":            ing_list,
        "ingredients_raw":             ing_text,
        "ingredients_raw_provenance": {
            "source":        "open_food_facts",
            "bsip0_status":  "real_scraped",
            "populated_at":  SCRAPE_TS,
            "missing":       not bool(ing_text),
            "note":          "Real product data from Open Food Facts Israeli product database",
        },
        "ingredient_order":       ing_order,
        "allergens_contains":     allergens,
        "allergens_may_contain":  [],
        "claims":                 claims,
        "front_of_pack_claims":   claims,
        "confidence": {
            "identity_confidence":   "real_barcode",
            "barcode_confidence":    "real_barcode",
            "nutrition_confidence":  "real_label_per_100g",
            "matched_by":            "open_food_facts",
            "observation_count":     1,
            "scrape_quality_score":  scrape_quality_score,
        },
        "barcode_validation_status":    "real_product",
        "barcode_confidence_reason":    "Real barcode from Open Food Facts Israeli product database",
        "nutrition_basis_claimed":      "ל100 גרם",
        "nutrition_basis_detected":     "per_100g",
        "nutrition_consistency_status": "real_label",
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality":      "real" if ing_he else ("transliterated" if ing_text else "missing"),
        "ingredient_warnings":          quality_flags,
        "canonical_trust_score":        trust_score,
        "canonical_trust_level":        trust_level,
        "canonical_risk_flags":         quality_flags,
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields":     missing,
        "inferred_fields":    [],
        "audit_ref":          f"off_{barcode}_audit.json",
        "run_id":             RUN_ID,
        "scrape_timestamp":   SCRAPE_TS,
        "scrape_source":      "open_food_facts",
        "nutriscore_grade":   raw.get("nutriscore_grade") or None,
    }


# ---------------------------------------------------------------------------
# Main collector
# ---------------------------------------------------------------------------
def collect_all() -> list[dict]:
    seen_barcodes: set[str] = set()
    raw_products: list[dict] = []

    def _ingest(resp: dict, source_tag: str):
        products = resp.get("products") or []
        for p in products:
            bc = str(p.get("code") or p.get("id") or "")
            if not bc or bc in seen_barcodes:
                continue
            if not _is_relevant(p):
                log.debug("SKIP (irrelevant) %s — %s", bc, p.get("product_name_he") or p.get("product_name"))
                continue
            seen_barcodes.add(bc)
            p["_source_tag"] = source_tag
            raw_products.append(p)
            log.info("  + %s  %s  [%s]", bc, (p.get("product_name_he") or p.get("product_name") or "")[:40], source_tag)

    # --- Category queries ---
    for cat in CATEGORY_QUERIES:
        log.info("Querying category: %s", cat)
        for page in range(1, 5):
            resp = fetch_by_category(cat, page=page, page_size=100)
            count = resp.get("count", 0)
            prods = resp.get("products") or []
            if not prods:
                break
            _ingest(resp, f"category:{cat}")
            log.info("  Page %d/%d — %d total, %d this page", page, (count//100)+1, count, len(prods))
            if len(prods) < 100 or page * 100 >= count:
                break
            time.sleep(2.0)
        time.sleep(2.0)

    # --- Keyword queries ---
    for term in KEYWORD_QUERIES:
        log.info("Querying keyword: %s", term)
        for page in range(1, 4):
            resp = fetch_by_keyword(term, page=page, page_size=100)
            count = resp.get("count", 0)
            prods = resp.get("products") or []
            if not prods:
                break
            _ingest(resp, f"keyword:{term}")
            log.info("  Page %d — %d total, %d this page", page, count, len(prods))
            if len(prods) < 100 or page * 100 >= count:
                break
            time.sleep(2.0)
        time.sleep(2.0)

    # --- Brand queries ---
    for brand in BRAND_QUERIES:
        log.info("Querying brand: %s", brand)
        resp = fetch_by_brand(brand, page_size=100)
        prods = resp.get("products") or []
        if prods:
            _ingest(resp, f"brand:{brand}")
            log.info("  %d products from brand:%s", len(prods), brand)
        time.sleep(2.0)

    return raw_products


# ---------------------------------------------------------------------------
# Save and convert
# ---------------------------------------------------------------------------
def run():
    log.info("=== BSIP2 Real Retailer Bread/Cracker Corpus Scraper ===")
    log.info("Run ID: %s | Source: Open Food Facts | Country: Israel", RUN_ID)

    raw_products = collect_all()
    log.info("Total unique relevant products fetched: %d", len(raw_products))

    scrape_log: list[dict] = []
    bsip1_products: list[dict] = []

    for raw in raw_products:
        bc = str(raw.get("code") or raw.get("id") or "unknown")
        nn = _nn(raw)
        score, flags = _quality_flags(raw, nn)

        # Save raw
        raw_path = RAW_DIR / f"off_{bc}.json"
        raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

        # Convert to BSIP1
        product = to_bsip1(raw, score, flags)
        pid = product["canonical_product_id"]
        bsip1_path = BSIP1_DIR / f"bsip1_{bc}.json"
        bsip1_path.write_text(json.dumps(product, ensure_ascii=False, indent=2), encoding="utf-8")
        bsip1_products.append(product)

        scrape_log.append({
            "barcode":         bc,
            "product_id":      pid,
            "name_he":         product["canonical_name_he"],
            "brand":           product["brand"],
            "source_tag":      raw.get("_source_tag", ""),
            "source_url":      product["source_url"],
            "retailers":       product["source_retailers"],
            "scrape_quality":  score,
            "quality_flags":   flags,
            "has_ingredients": bool(product["ingredients_text_he"] or product["ingredients_raw"]),
            "has_kcal":        product["normalized_nutrition_per_100g"].get("energy_kcal") is not None,
            "has_fiber":       product["normalized_nutrition_per_100g"].get("dietary_fiber_g") is not None,
            "raw_file":        str(raw_path),
            "bsip1_file":      str(bsip1_path),
            "scrape_ts":       SCRAPE_TS,
        })

    log.path = BASE_DIR / "scrape_log.json"
    (BASE_DIR / "scrape_log.json").write_text(
        json.dumps(scrape_log, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log.info("Done. %d products → raw/ and bsip1/", len(bsip1_products))
    log.info("Scrape log: %s", BASE_DIR / "scrape_log.json")
    return scrape_log, bsip1_products


if __name__ == "__main__":
    run()
