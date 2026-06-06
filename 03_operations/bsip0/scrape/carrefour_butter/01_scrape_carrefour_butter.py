"""
BSIP0 Carrefour Israel — Butter (חמאה) scraper (TASK-191).

Carrefour uses AngularJS (ng-app=ZuZ) with lazy-loaded product pages. Full Playwright
scraping requires a two-pass workflow. This scraper uses a hybrid approach:

1. Tries the Carrefour search API endpoint (JSON) discovered from network inspection.
2. Falls back to Open Food Facts for nutrition panels per barcode found.
3. Uses a curated seed list for high-priority brands not discoverable via search.

Carrefour HTML structure (from retailer_capabilities/carrefour.yaml):
  - ingredients_anchor: 'רשימת רכיבים' ... until 'אלרגנים כלולים'
  - nutrition_anchor: 'סימון תזונתי' ... until 'אין להסתמך'
  - title_pattern: '<PRODUCT NAME> | קרפור Online'

EDPG: all records stamped with provenance; OFF panels are candidates.

Output: C:\\Bari\\02_products\\butter\\bsip0_outputs\\butter_carrefour_raw_{ts}.json
"""
from __future__ import annotations

import json
import sys
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
from time import sleep
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(r"C:\Bari")))

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

OUT_DIR = Path(r"C:\Bari\02_products\butter\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RETAILER = "carrefour"
RETAILER_NAME = "קרפור"
BASE_URL = "https://www.carrefour.co.il"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "application/json, text/html, */*",
    "Referer": BASE_URL,
}

# Same QUERY_PLAN as Shufersal butter
QUERY_PLAN: list[tuple[str, str]] = [
    ("חמאה",          "mainstream"),
    ("חמאת שמנת",     "mainstream"),
    ("butter",        "specialty"),
    ("kerrygold",     "specialty"),
    ("lurpak",        "specialty"),
    ("anchor butter", "specialty"),
    ("גהי",           "specialty"),
    ("חמאה מזוקקת",   "specialty"),
]

EXCLUDE_SIGNALS = [
    "ממרח", "מרגרינה", "שמן לפתית", "שמן צמחי", "שמנים צמחיים",
    "נטורינה", "בטעם חמאה", "butter flavor", "butter flavour",
    "חמאת בוטנים", "חמאת שקדים", "חמאת קשיו", "חמאת פיסטוקים",
    "שמן קוקוס", "קרם צמחי", "פלמנטין", "שומן אפייה",
]

# Curated seed list of priority barcodes to fetch from Carrefour via OFF.
# Carrefour Israel often carries different premium imports than Shufersal.
SEED_BARCODES: list[dict] = [
    # Kerrygold
    {"barcode": "5099460004149", "name_he": "חמאה קרי גולד ללא מלח", "brand": "Kerrygold", "query": "kerrygold"},
    {"barcode": "5099460004132", "name_he": "חמאה קרי גולד מלוחה", "brand": "Kerrygold", "query": "kerrygold"},
    {"barcode": "5099460010935", "name_he": "חמאה קרי גולד ללא מלח 250 גרם", "brand": "Kerrygold", "query": "kerrygold"},
    # Anchor
    {"barcode": "9414544900015", "name_he": "חמאה אנקור ללא מלח", "brand": "Anchor", "query": "anchor butter"},
    # Lurpak pure butter
    {"barcode": "5740900400221", "name_he": "חמאה לורפק ללא מלח", "brand": "לורפק", "query": "lurpak"},
    {"barcode": "5740900400238", "name_he": "חמאה לורפק מלוחה", "brand": "לורפק", "query": "lurpak"},
    # Le Gall variants (premium French)
    {"barcode": "3274932103802", "name_he": "חמאה לה גל זהב", "brand": "LE GALL", "query": "חמאה"},
    {"barcode": "3274932103857", "name_he": "חמאה לה גל זהב עם מלח", "brand": "LE GALL", "query": "חמאה"},
    # Echire — premium French AOP butter
    {"barcode": "3760088100025", "name_he": "חמאה אשירה AOP", "brand": "Echire", "query": "חמאה"},
    # Paysan Breton
    {"barcode": "3412130012558", "name_he": "חמאה פיזן ברטון ללא מלח", "brand": "Paysan Breton", "query": "חמאה"},
    {"barcode": "3412130012534", "name_he": "חמאה פיזן ברטון מלוחה", "brand": "Paysan Breton", "query": "חמאה"},
    # President
    {"barcode": "3228021530005", "name_he": "חמאה פרזידן ללא מלח", "brand": "President", "query": "president"},
    {"barcode": "3228021530012", "name_he": "חמאה פרזידן מלוחה", "brand": "President", "query": "president"},
    # Israeli brands at Carrefour
    {"barcode": "7290116932033", "name_he": "חמאה מהדרין", "brand": "תנובה", "query": "חמאה"},
    {"barcode": "7290019635147", "name_he": "חמאה איטלקית", "brand": "מחלבות גד", "query": "חמאה"},
    {"barcode": "7290019635130", "name_he": "חמאה איטלקית מלוחה", "brand": "מחלבות גד", "query": "חמאה"},
    # Valio Finnish butter
    {"barcode": "8175173",       "name_he": "חמאה ואליו ללא מלח", "brand": "VALIO", "query": "חמאה"},
    # Ghee
    {"barcode": "4260268321030", "name_he": "שמן גהי", "brand": "Ghee", "query": "גהי"},
    # Roshen (Ukrainian brand popular in Israel)
    {"barcode": "4823077630057", "name_he": "חמאה 82.5% רושן", "brand": "ROSHEN", "query": "חמאה"},
]

_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _parse_num(raw):
    if raw is None:
        return None
    m = _NUM_RE.search(str(raw).replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def _should_exclude(name: str) -> bool:
    name_lower = name.lower()
    for sig in EXCLUDE_SIGNALS:
        if sig.lower() in name_lower:
            return True
    return False


def _try_carrefour_search(query: str, session: requests.Session) -> list[dict]:
    """Attempt to query Carrefour's search endpoint. Returns partial product list."""
    results = []
    try:
        # Carrefour Israel search endpoint (AngularJS app / REST-style)
        search_url = f"{BASE_URL}/api/products/search"
        params = {"q": query, "pageSize": 20, "currentPage": 0}
        r = session.get(search_url, params=params, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            data = r.json()
            products = data.get("products") or data.get("results") or []
            for p in products:
                name = p.get("name") or p.get("summary") or ""
                barcode = p.get("gtin13") or p.get("ean") or p.get("code") or ""
                brand = p.get("brand") or p.get("manufacturer") or ""
                price = None
                try:
                    price = float(p.get("price", {}).get("value") or p.get("priceFormatted") or 0) or None
                except Exception:
                    pass
                if name and barcode and not _should_exclude(name):
                    results.append({"name_he": name, "brand": brand,
                                    "barcode": str(barcode), "price": price})
    except Exception as e:
        log.debug("Carrefour search API not available for '%s': %s", query, e)
    return results


def _build_record_from_off(seed: dict, off_product, session_price: float | None = None) -> dict:
    barcode = seed["barcode"]
    name_he = off_product.name or seed.get("name_he", "")
    brand = off_product.brand or seed.get("brand", "")

    n = off_product.nutriments or {}

    def _nv(key):
        v = n.get(key)
        if v is None:
            v = n.get(key.replace("_100g", "") if "_100g" in key else key + "_100g")
        return v

    energy_kcal = _nv("energy-kcal_100g") or _nv("energy_100g")
    protein = _nv("proteins_100g")
    carbs = _nv("carbohydrates_100g")
    fat = _nv("fat_100g")
    fiber = _nv("fiber_100g")
    sodium_g = _nv("sodium_100g")
    sugar = _nv("sugars_100g")
    sat_fat = _nv("saturated-fat_100g")

    sodium_mg = (sodium_g * 1000) if sodium_g is not None else None

    nutrition = {
        "energy_kcal_raw": str(energy_kcal) if energy_kcal is not None else "",
        "protein_raw":     str(protein) if protein is not None else "",
        "carbs_raw":       str(carbs) if carbs is not None else "",
        "fat_raw":         str(fat) if fat is not None else "",
        "fiber_raw":       str(fiber) if fiber is not None else "",
        "sodium_raw":      str(sodium_mg) if sodium_mg is not None else "",
        "sugar_raw":       str(sugar) if sugar is not None else "",
        "saturated_fat_raw": str(sat_fat) if sat_fat is not None else "",
    }

    has_panel = off_product.has_panel
    conf = "high" if has_panel and (protein is not None and fat is not None) else ("medium" if has_panel else "low")

    prov = off_product.provenance
    prov_dict = {
        "source": prov.source if prov else "open_food_facts",
        "source_id": barcode,
        "source_url": f"https://world.openfoodfacts.org/product/{barcode}",
        "fetched_at": prov.fetched_at if prov else datetime.now(timezone.utc).isoformat(),
        "client_version": prov.client_version if prov else "1.0",
        "verification_status": "candidate",
    }

    return {
        "retailer_id": RETAILER,
        "retailer_name": RETAILER_NAME,
        "source_url": f"{BASE_URL}/search?text={quote(seed.get('query', ''))}",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "name_he": name_he,
        "name_en": "",
        "brand": brand,
        "barcode": barcode,
        "category_raw": "חמאה",
        "subcategory_raw": "butter",
        "nutrition": nutrition,
        "nutrition_raw_source": {"rows": [], "html": ""},
        "ingredients_raw": off_product.ingredients_text or "",
        "ingredients_language": "he",
        "claims_raw": "",
        "image_urls": [off_product.image_url] if off_product.image_url else [],
        "extraction_method": "off_api",
        "extraction_confidence": conf,
        "price": session_price,
        "weight_g": None,
        "price_per_100g": None,
        "acquisition_query": seed.get("query", "חמאה"),
        "acquisition_tier": seed.get("tier", "specialty"),
        "off_found": True,
        "off_completeness": off_product.completeness,
        "provenance": prov_dict,
    }


def _build_stub_record(seed: dict, reason: str) -> dict:
    barcode = seed["barcode"]
    return {
        "retailer_id": RETAILER,
        "retailer_name": RETAILER_NAME,
        "source_url": f"{BASE_URL}/search?text={quote(seed.get('query', ''))}",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "name_he": seed.get("name_he", ""),
        "name_en": "",
        "brand": seed.get("brand", ""),
        "barcode": barcode,
        "category_raw": "חמאה",
        "subcategory_raw": "butter",
        "nutrition": {k: "" for k in [
            "energy_kcal_raw", "protein_raw", "carbs_raw", "fat_raw",
            "fiber_raw", "sodium_raw", "sugar_raw", "saturated_fat_raw"
        ]},
        "nutrition_raw_source": {"rows": [], "html": ""},
        "ingredients_raw": "",
        "ingredients_language": "he",
        "claims_raw": "",
        "image_urls": [],
        "extraction_method": "off_api",
        "extraction_confidence": "off_miss",
        "price": None,
        "weight_g": None,
        "price_per_100g": None,
        "acquisition_query": seed.get("query", "חמאה"),
        "acquisition_tier": seed.get("tier", "specialty"),
        "off_found": False,
        "off_miss_reason": reason,
        "provenance": {
            "source": "open_food_facts",
            "source_id": barcode,
            "source_url": f"https://world.openfoodfacts.org/product/{barcode}",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "client_version": "1.0",
            "verification_status": "candidate",
        },
    }


def main():
    try:
        from integrations.clients.open_food_facts import get_product as off_get
    except ImportError:
        log.error("Cannot import open_food_facts client.")
        sys.exit(1)

    session = requests.Session()
    results = []
    seen_barcodes: set[str] = set()
    found_count = 0
    miss_count = 0
    excluded_count = 0

    log.info("=== Carrefour Israel Butter Scraper (TASK-191) — %d seed barcodes ===",
             len(SEED_BARCODES))

    # Try to discover additional barcodes via Carrefour search API
    discovered: list[dict] = []
    for query, tier in QUERY_PLAN:
        log.info("  Search query: %s", query)
        found_via_api = _try_carrefour_search(query, session)
        for p in found_via_api:
            p["tier"] = tier
            if p["barcode"] not in {s["barcode"] for s in SEED_BARCODES}:
                if not _should_exclude(p.get("name_he", "")):
                    discovered.append(p)
                    log.info("    Discovered via API: %s | %s", p["barcode"], p["name_he"])
        sleep(0.5)

    # Merge discovered with seed list (seeds take priority for known brands)
    all_seeds = list(SEED_BARCODES)
    for d in discovered:
        if d["barcode"] not in {s["barcode"] for s in all_seeds}:
            all_seeds.append({"barcode": d["barcode"], "name_he": d.get("name_he", ""),
                               "brand": d.get("brand", ""), "query": d.get("query", "חמאה"),
                               "tier": d.get("tier", "mainstream")})

    # Fetch OFF panels for all barcodes
    for seed in all_seeds:
        barcode = seed["barcode"]
        name_he = seed.get("name_he", "")

        if barcode in seen_barcodes:
            continue
        seen_barcodes.add(barcode)

        if _should_exclude(name_he):
            log.info("  EXCLUDED: %s %s", barcode, name_he)
            excluded_count += 1
            continue

        log.info("  Fetching OFF: %s | %s", barcode, name_he)
        try:
            off = off_get(barcode)
            sleep(0.3)

            if not off.found:
                log.info("    OFF miss: %s", barcode)
                stub = _build_stub_record(seed, "off_not_found")
                results.append(stub)
                miss_count += 1
                continue

            off_name = off.name or name_he
            if _should_exclude(off_name):
                log.info("    EXCLUDED (OFF name): %s %s", barcode, off_name)
                excluded_count += 1
                continue

            record = _build_record_from_off(seed, off)
            results.append(record)
            found_count += 1
            log.info("    OK: %s | %s | panel=%s", barcode, off_name, off.has_panel)

        except Exception as e:
            log.warning("    Error: %s: %s", barcode, e)
            stub = _build_stub_record(seed, f"error:{str(e)[:100]}")
            results.append(stub)
            miss_count += 1

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = OUT_DIR / f"butter_carrefour_raw_{ts}.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("=== Done ===")
    log.info("  Found + enriched: %d", found_count)
    log.info("  OFF miss: %d", miss_count)
    log.info("  Excluded: %d", excluded_count)
    log.info("  Output: %s", out_path)
    return out_path


if __name__ == "__main__":
    main()
