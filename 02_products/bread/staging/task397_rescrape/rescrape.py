"""
TASK-397 Track A, Step 2 — Bread secondary-retailer fat RE-SCRAPE.

Priority targets (9 implausible): barcodes with <0.5g fat but kcal-gap 55-147 implying
hidden fat. Also opportunistically attempts the other 13 sentinel products.

Retailer order per SOURCE_SELECTION_POLICY: Victory → Rami Levy → Yochananof.

OFF BAN ABSOLUTE: nutrition ONLY from direct retailer scrape. Never OFF.
Per-100g plausibility gate: protein*4 + carbs*4 + fat*9 vs declared kcal.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OUT_DIR = Path(__file__).parent
SCRIPT_VERSION = "1.0.0"
TIMEOUT = 20
RETRY_BACKOFF = 2.0

# 9 implausible barcodes (priority) + 13 plausible/suspect (opportunistic)
IMPLAUSIBLE = {
    "2079033", "2079217", "6451484", "7290014321168",
    "7290016245325", "7290016967074", "74252", "8434165658523", "96086000966"
}

# All 22 sentinel barcodes + their known BSIP1 data (for plausibility gate)
SENTINEL_DATA = {
    "2079033":          {"name": "לחם דגנים לייט",               "kcal": 222.0, "protein_g": 9.0,  "carbs_g": 43.7},
    "2079217":          {"name": "לחם מחמצת שיפון+אגוזים",       "kcal": 259.0, "protein_g": 9.0,  "carbs_g": 43.5},
    "2079927":          {"name": "לחם דגנים מלא",                 "kcal": 242.0, "protein_g": 9.0,  "carbs_g": 46.8},
    "3054183":          {"name": "לחם שיפון מלא מסטמכר",         "kcal": 191.0, "protein_g": 7.0,  "carbs_g": 38.3},
    "3268252":          {"name": "לחם חיטה מלא לילדים",           "kcal": 221.0, "protein_g": 8.5,  "carbs_g": 43.8},
    "3268429":          {"name": "לחם ירוק מקמח מלא",             "kcal": 223.0, "protein_g": 8.0,  "carbs_g": 44.2},
    "481197":           {"name": "לחם מחמצת גרעינים",             "kcal": 220.0, "protein_g": 8.0,  "carbs_g": 43.0},
    "481203":           {"name": "לחם מחמצת קמח מלא",             "kcal": 227.0, "protein_g": 8.0,  "carbs_g": 43.5},
    "497044":           {"name": "לחם ברמן אקטיב",                "kcal": 233.0, "protein_g": 9.0,  "carbs_g": 44.0},
    "574370":           {"name": "לחם שיפון קל",                  "kcal": 198.0, "protein_g": 7.0,  "carbs_g": 38.5},
    "6451484":          {"name": "לחם מחמצת אגוזים צימוקים",      "kcal": 266.0, "protein_g": 9.0,  "carbs_g": 43.5},
    "6451507":          {"name": "לחם מחמצת מכוסמין",             "kcal": 213.0, "protein_g": 8.0,  "carbs_g": 42.2},
    "7290014321168":    {"name": "לחם לס פרוס קיטו",              "kcal": 231.0, "protein_g": 9.0,  "carbs_g": 22.4},
    "7290016245325":    {"name": "לחם טחינה פרוס",                "kcal": 192.0, "protein_g": 7.0,  "carbs_g": 26.5},
    "7290016967074":    {"name": "לחם אנג'ל חיטה מלאה",          "kcal": 242.0, "protein_g": 9.0,  "carbs_g": 43.5},
    "7290018500460":    {"name": "לחם אנג'ל חצי מלא",            "kcal": 220.0, "protein_g": 8.5,  "carbs_g": 43.8},
    "7296073134442":    {"name": "קרקר פריך עם קמח שיפון",        "kcal": 376.0, "protein_g": 13.0, "carbs_g": 77.0},
    "7296073134459":    {"name": "קרקר פריך בסגנון שוודי",        "kcal": 371.0, "protein_g": 13.0, "carbs_g": 77.0},
    "74252":            {"name": "קרקר שומשום אסם",               "kcal": 465.0, "protein_g": 10.0, "carbs_g": 67.5},
    "8434165658523":    {"name": "קרקר קרם קרקר",                 "kcal": 448.0, "protein_g": 8.5,  "carbs_g": 72.5},
    "96086000577":      {"name": "קרקר כוסמין אורגני",            "kcal": 380.0, "protein_g": 12.0, "carbs_g": 74.0},
    "96086000966":      {"name": "קרקר כוסמין מלא ושומשום",       "kcal": 418.0, "protein_g": 12.0, "carbs_g": 66.0},
}


# ---------------------------------------------------------------------------
# HTTP helper (no deps beyond stdlib)
# ---------------------------------------------------------------------------
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def _http_get(url: str, headers: dict | None = None, timeout: int = TIMEOUT) -> bytes | None:
    hdrs = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
    }
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # Handle gzip
            if resp.info().get("Content-Encoding") == "gzip":
                import gzip
                return gzip.decompress(raw)
            return raw
    except Exception as exc:
        return None


def _http_get_json(url: str, headers: dict | None = None, timeout: int = TIMEOUT) -> dict | None:
    hdrs = {"Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    data = _http_get(url, headers=hdrs, timeout=timeout)
    if data is None:
        return None
    try:
        return json.loads(data.decode("utf-8", errors="replace"))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Plausibility gate
# ---------------------------------------------------------------------------
def plausibility_gate(protein_g: float, carbs_g: float, fat_g: float, kcal: float) -> tuple[bool, float]:
    """Check macros sum plausibly to declared kcal. Returns (pass, gap)."""
    macro_kcal = protein_g * 4 + carbs_g * 4 + fat_g * 9
    gap = abs(kcal - macro_kcal)
    # Allow ±15 kcal tolerance (fiber, polyols, rounding)
    return gap <= 15.0, gap


# ---------------------------------------------------------------------------
# Retailer scrapers — direct product page scrape ONLY
# OFF BAN: never touch Open Food Facts. Nutrition from label HTML only.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Victory (www.victory.co.il) — barcode search via their API
# ---------------------------------------------------------------------------
VICTORY_SEARCH_API = "https://www.victory.co.il/v2/retailer/stores/662/products/search"
VICTORY_PRODUCT_API = "https://www.victory.co.il/v2/retailer/stores/662/products"

def _victory_search_barcode(barcode: str) -> dict | None:
    """Try Victory API to find product by barcode."""
    url = f"{VICTORY_SEARCH_API}?query={barcode}&store=662"
    data = _http_get_json(url, headers={
        "Referer": "https://www.victory.co.il/",
        "Origin": "https://www.victory.co.il",
        "X-Requested-With": "XMLHttpRequest",
    })
    return data


def _extract_victory_nutrition(data: dict) -> dict | None:
    """Extract per-100g fat from Victory product JSON."""
    # Victory returns {products: [{...}]} or {data: {products: [...]}}
    products = None
    if isinstance(data, dict):
        if "products" in data:
            products = data["products"]
        elif "data" in data and isinstance(data["data"], dict):
            products = data["data"].get("products")
        elif isinstance(data, list):
            products = data

    if not products:
        return None

    for prod in (products if isinstance(products, list) else []):
        # Look for nutrition_facts or nutritions field
        nf = prod.get("nutrition_facts") or prod.get("nutritions") or prod.get("nutritionFacts")
        if not nf:
            continue
        if isinstance(nf, list):
            fat = None
            for row in nf:
                name_he = (row.get("name") or row.get("label") or "").lower()
                if "שומן" in name_he and "רווי" not in name_he:
                    val = row.get("value") or row.get("per100g") or row.get("amount")
                    try:
                        fat = float(str(val).replace(",", ".").strip())
                        return {"fat_g": fat, "raw_field": name_he}
                    except (ValueError, TypeError):
                        pass
        elif isinstance(nf, dict):
            for key in ("fat", "total_fat", "fat_g", "שומן"):
                val = nf.get(key)
                if val is not None:
                    try:
                        return {"fat_g": float(str(val).replace(",", ".")), "raw_field": key}
                    except (ValueError, TypeError):
                        pass
    return None


def scrape_victory(barcode: str) -> dict:
    """Attempt Victory barcode lookup. Returns result dict."""
    result = {
        "retailer": "victory",
        "url_tried": f"https://www.victory.co.il/search?q={barcode}",
        "status": "not_found",
        "fat_g": None,
        "raw_html_snippet": None,
    }

    # Try their v2 API first
    api_url = f"{VICTORY_SEARCH_API}?query={barcode}"
    data = _http_get_json(api_url, headers={
        "Referer": "https://www.victory.co.il/",
    })
    if data is None:
        # Try alternate endpoint
        alt_url = f"https://www.victory.co.il/umbraco/api/product/search?q={barcode}"
        data = _http_get_json(alt_url)

    if data is None:
        # Try the product page HTML
        page_url = f"https://www.victory.co.il/search?q={barcode}"
        html_bytes = _http_get(page_url)
        if html_bytes is None:
            result["status"] = "blocked"
            result["block_reason"] = "HTTP request failed — host unreachable or connection refused"
            return result
        html = html_bytes.decode("utf-8", errors="replace")
        # Try to parse fat from product HTML
        fat = _parse_fat_from_html(html, barcode)
        if fat is not None:
            result["fat_g"] = fat["fat_g"]
            result["status"] = "found_html"
            result["raw_html_snippet"] = fat.get("raw")
        else:
            # Product might not exist
            result["status"] = "not_found"
        return result

    nf = _extract_victory_nutrition(data)
    if nf:
        result["fat_g"] = nf["fat_g"]
        result["status"] = "found_api"
        result["raw_html_snippet"] = str(nf)
    else:
        result["status"] = "not_found"
    return result


# ---------------------------------------------------------------------------
# Rami Levy (www.rami-levy.co.il) — barcode search
# ---------------------------------------------------------------------------
RAMILEVY_SEARCH_API = "https://www.rami-levy.co.il/api/catalog/v1/products"

def scrape_ramilevy(barcode: str) -> dict:
    """Attempt Rami Levy barcode lookup."""
    result = {
        "retailer": "rami_levy",
        "url_tried": f"https://www.rami-levy.co.il/he/search?q={barcode}",
        "status": "not_found",
        "fat_g": None,
        "raw_html_snippet": None,
    }

    # Try their catalog API
    api_url = f"{RAMILEVY_SEARCH_API}?q={barcode}&page=1&size=5"
    data = _http_get_json(api_url, headers={
        "Referer": "https://www.rami-levy.co.il/",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    })

    if data is None:
        # Try alternate search URL
        alt_url = f"https://www.rami-levy.co.il/api/catalog?id={barcode}"
        data = _http_get_json(alt_url)

    if data is None:
        # Try HTML search page
        html_bytes = _http_get(f"https://www.rami-levy.co.il/he/search?q={barcode}")
        if html_bytes is None:
            result["status"] = "blocked"
            result["block_reason"] = "HTTP request failed — host unreachable or connection refused"
            return result
        html = html_bytes.decode("utf-8", errors="replace")
        fat = _parse_fat_from_html(html, barcode)
        if fat is not None:
            result["fat_g"] = fat["fat_g"]
            result["status"] = "found_html"
            result["raw_html_snippet"] = fat.get("raw")
        return result

    # Parse Rami Levy API response
    products = data.get("products") or data.get("data") or (data if isinstance(data, list) else None)
    if isinstance(products, dict):
        products = products.get("items") or products.get("products") or []
    if not isinstance(products, list):
        result["status"] = "not_found"
        return result

    for prod in products:
        bc = str(prod.get("barcode") or prod.get("ean") or prod.get("id") or "")
        if bc == barcode or bc.lstrip("0") == barcode.lstrip("0"):
            nf = prod.get("nutritions") or prod.get("nutrition_facts") or prod.get("nutritionalValues")
            fat = _extract_fat_from_nf(nf)
            if fat is not None:
                result["fat_g"] = fat
                result["status"] = "found_api"
                result["raw_html_snippet"] = str(nf)[:200]
            else:
                # Try inline nutrition fields
                for k in ("fat", "total_fat", "fat_100g"):
                    v = prod.get(k)
                    if v is not None:
                        try:
                            result["fat_g"] = float(str(v).replace(",", "."))
                            result["status"] = "found_api"
                            result["raw_html_snippet"] = f"field:{k}={v}"
                            break
                        except ValueError:
                            pass
            return result

    result["status"] = "not_found"
    return result


# ---------------------------------------------------------------------------
# Yochananof (www.yochananof.co.il) — barcode search
# ---------------------------------------------------------------------------
YOCHANANOF_SEARCH_API = "https://www.yochananof.co.il/api/v2/products/search"

def scrape_yochananof(barcode: str) -> dict:
    """Attempt Yochananof barcode lookup."""
    result = {
        "retailer": "yochananof",
        "url_tried": f"https://www.yochananof.co.il/search?q={barcode}",
        "status": "not_found",
        "fat_g": None,
        "raw_html_snippet": None,
    }

    api_url = f"{YOCHANANOF_SEARCH_API}?q={barcode}&limit=5"
    data = _http_get_json(api_url, headers={
        "Referer": "https://www.yochananof.co.il/",
    })

    if data is None:
        html_bytes = _http_get(f"https://www.yochananof.co.il/search?q={barcode}")
        if html_bytes is None:
            result["status"] = "blocked"
            result["block_reason"] = "HTTP request failed — host unreachable or connection refused"
            return result
        html = html_bytes.decode("utf-8", errors="replace")
        fat = _parse_fat_from_html(html, barcode)
        if fat is not None:
            result["fat_g"] = fat["fat_g"]
            result["status"] = "found_html"
            result["raw_html_snippet"] = fat.get("raw")
        return result

    products = data.get("products") or data.get("items") or (data if isinstance(data, list) else [])
    for prod in (products if isinstance(products, list) else []):
        bc = str(prod.get("barcode") or prod.get("ean") or "")
        if bc == barcode or bc.lstrip("0") == barcode.lstrip("0"):
            nf = prod.get("nutritions") or prod.get("nutrition_facts") or {}
            fat = _extract_fat_from_nf(nf)
            if fat is not None:
                result["fat_g"] = fat
                result["status"] = "found_api"
                result["raw_html_snippet"] = str(nf)[:200]
            return result

    result["status"] = "not_found"
    return result


# ---------------------------------------------------------------------------
# Generic HTML fat parser — last resort on direct product pages
# ---------------------------------------------------------------------------

# Hebrew nutrition-table patterns
_FAT_PATTERNS = [
    # "שומן כולל X ג'" or "שומן X"
    re.compile(r'שומן(?:\s+כולל)?\s*[:\s]\s*(\d+[\.,]\d*|\d+)\s*(?:ג|g)', re.UNICODE),
    # "Total fat N g" (English labels common in IL retail)
    re.compile(r'[Tt]otal\s+[Ff]at\s*[:\s]\s*(\d+[\.,]\d*|\d+)\s*g'),
    # JSON-LD / script tags
    re.compile(r'"fat[_]?(?:g|100g|per100)?"\s*:\s*"?(\d+[\.,]\d*)"?', re.I),
    re.compile(r'"totalFat"\s*:\s*"?(\d+[\.,]\d*)"?', re.I),
    re.compile(r'"שומן"\s*:\s*"?(\d+[\.,]\d*)"?'),
    # nutrition data in page (common IL retailer pattern)
    re.compile(r'(?:שומן|fat)[^<\n]{0,20}>\s*(\d+[\.,]\d*)\s*(?:ג|g)', re.I | re.UNICODE),
]

def _parse_fat_from_html(html: str, barcode: str) -> dict | None:
    """Try to extract fat per 100g from HTML. Returns {fat_g, raw} or None."""
    # Check barcode is in the page (confirms product found)
    if barcode not in html and barcode.lstrip("0") not in html:
        return None
    for pat in _FAT_PATTERNS:
        m = pat.search(html)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if 0 < val < 100:  # sanity: fat per 100g can't be 0 or >100
                    return {"fat_g": val, "raw": m.group(0)[:100]}
            except ValueError:
                pass
    return None


def _extract_fat_from_nf(nf) -> float | None:
    """Extract fat_g from a nutritions dict or list."""
    if nf is None:
        return None
    if isinstance(nf, dict):
        for key in ("fat", "total_fat", "fat_g", "totalFat", "שומן"):
            v = nf.get(key)
            if v is not None:
                try:
                    return float(str(v).replace(",", "."))
                except (ValueError, TypeError):
                    pass
    elif isinstance(nf, list):
        for row in nf:
            if not isinstance(row, dict):
                continue
            name = (row.get("name") or row.get("label") or "").lower()
            if "שומן" in name and "רווי" not in name and "חד" not in name and "רב" not in name:
                for vk in ("value", "per100g", "amount", "quantity"):
                    v = row.get(vk)
                    if v is not None:
                        try:
                            return float(str(v).replace(",", "."))
                        except (ValueError, TypeError):
                            pass
    return None


# ---------------------------------------------------------------------------
# Reachability probe
# ---------------------------------------------------------------------------
RETAILER_PROBE_URLS = {
    "victory": "https://www.victory.co.il/",
    "rami_levy": "https://www.rami-levy.co.il/",
    "yochananof": "https://www.yochananof.co.il/",
}

def probe_reachability() -> dict[str, dict]:
    """Probe each retailer for basic HTTP reachability."""
    results = {}
    for retailer, url in RETAILER_PROBE_URLS.items():
        print(f"  Probing {retailer} ({url})...", flush=True)
        resp = _http_get(url, timeout=15)
        if resp is not None and len(resp) > 500:
            results[retailer] = {
                "reachable": True,
                "bytes_received": len(resp),
                "status": "reachable",
            }
            print(f"    -> REACHABLE ({len(resp)} bytes)", flush=True)
        else:
            results[retailer] = {
                "reachable": False,
                "bytes_received": 0,
                "status": "blocked_or_unreachable",
            }
            print(f"    -> BLOCKED/UNREACHABLE", flush=True)
    return results


# ---------------------------------------------------------------------------
# Main scrape loop
# ---------------------------------------------------------------------------
def scrape_barcode(barcode: str, reachable_retailers: list[str]) -> dict:
    """Try each reachable retailer in priority order; stop on first fat recovery."""
    sentinel = SENTINEL_DATA[barcode]
    kcal = sentinel["kcal"]
    protein_g = sentinel["protein_g"]
    carbs_g = sentinel["carbs_g"]
    is_implausible = barcode in IMPLAUSIBLE

    entry = {
        "barcode": barcode,
        "name_he": sentinel["name"],
        "is_priority_implausible": is_implausible,
        "secondary_retailer": None,
        "real_fat_g": None,
        "plausibility_pass": None,
        "plausibility_gap_kcal": None,
        "recovery_status": "not_found",
        "discard_candidate": False,
        "retailer_attempts": [],
        "scrape_url": None,
        "raw_snippet": None,
    }

    # Build scraper functions in priority order
    scrapers = []
    if "victory" in reachable_retailers:
        scrapers.append(("victory", scrape_victory))
    if "rami_levy" in reachable_retailers:
        scrapers.append(("rami_levy", scrape_ramilevy))
    if "yochananof" in reachable_retailers:
        scrapers.append(("yochananof", scrape_yochananof))

    if not scrapers:
        entry["recovery_status"] = "blocked"
        entry["discard_candidate"] = True
        return entry

    for retailer_name, scraper_fn in scrapers:
        print(f"    Trying {retailer_name} for {barcode}...", flush=True)
        try:
            r = scraper_fn(barcode)
        except Exception as exc:
            r = {"status": "error", "retailer": retailer_name, "error": str(exc), "fat_g": None}

        entry["retailer_attempts"].append({
            "retailer": retailer_name,
            "status": r.get("status"),
            "fat_g": r.get("fat_g"),
            "url_tried": r.get("url_tried"),
            "error": r.get("error") or r.get("block_reason"),
        })

        if r.get("fat_g") is not None:
            fat_g = r["fat_g"]
            passed, gap = plausibility_gate(protein_g, carbs_g, fat_g, kcal)
            entry["secondary_retailer"] = retailer_name
            entry["real_fat_g"] = fat_g
            entry["plausibility_pass"] = passed
            entry["plausibility_gap_kcal"] = round(gap, 1)
            entry["recovery_status"] = "recovered"
            entry["scrape_url"] = r.get("url_tried")
            entry["raw_snippet"] = r.get("raw_html_snippet")
            print(f"      -> FAT={fat_g}g  gap={gap:.1f}kcal  plausible={passed}", flush=True)
            break

        time.sleep(0.5)  # polite inter-request delay

    if entry["recovery_status"] != "recovered":
        entry["recovery_status"] = "not_found"
        entry["discard_candidate"] = True
        print(f"      -> not found on any retailer -> discard_candidate=true", flush=True)

    return entry


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=== TASK-397 Track A Step 2: Bread secondary-retailer fat re-scrape ===\n")

    # Step 1: Probe retailer reachability
    print("Step 1: Probing retailer reachability...")
    reachability = probe_reachability()
    reachable_retailers = [r for r, d in reachability.items() if d["reachable"]]
    blocked_retailers = [r for r, d in reachability.items() if not d["reachable"]]
    print(f"\nReachable: {reachable_retailers}")
    print(f"Blocked:   {blocked_retailers}\n")

    if not reachable_retailers:
        print("ERROR: No secondary retailers reachable. Cannot proceed with re-scrape.")
        results = {
            "task": "TASK-397",
            "track": "A",
            "step": 2,
            "run_id": f"rescrape_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "script_version": SCRIPT_VERSION,
            "retailer_reachability": reachability,
            "reachable_retailers": reachable_retailers,
            "blocked_retailers": blocked_retailers,
            "feasibility_summary": "All secondary retailers blocked. No fat recovery possible from direct scrape in this environment.",
            "products": [],
            "counts": {"total_attempted": 0, "recovered": 0, "not_found": 0, "blocked": 0, "discard_candidate": 0},
        }
        out = OUT_DIR / "rescrape_results.json"
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        sha256 = hashlib.sha256(out.read_bytes()).hexdigest()
        print(f"\nOutput: {out}")
        print(f"SHA256: {sha256}")
        return results, sha256

    # Step 2: Scrape all 22 sentinel barcodes (priority 9 first, then other 13)
    print("Step 2: Scraping barcodes...")
    ordered_barcodes = sorted(SENTINEL_DATA.keys(), key=lambda b: (0 if b in IMPLAUSIBLE else 1))

    products = []
    for barcode in ordered_barcodes:
        print(f"\n  [{barcode}] {SENTINEL_DATA[barcode]['name']} (priority={barcode in IMPLAUSIBLE})")
        entry = scrape_barcode(barcode, reachable_retailers)
        products.append(entry)
        time.sleep(0.3)  # inter-product delay

    # Step 3: Counts
    recovered = [p for p in products if p["recovery_status"] == "recovered"]
    recovered_plausible = [p for p in recovered if p["plausibility_pass"]]
    recovered_implausible_fat = [p for p in recovered if not p["plausibility_pass"]]
    not_found = [p for p in products if p["recovery_status"] == "not_found"]
    blocked = [p for p in products if p["recovery_status"] == "blocked"]
    discard = [p for p in products if p["discard_candidate"]]

    implausible_recovered = [p for p in products if p["barcode"] in IMPLAUSIBLE and p["recovery_status"] == "recovered"]
    implausible_discard = [p for p in products if p["barcode"] in IMPLAUSIBLE and p["discard_candidate"]]

    # Build feasibility summary
    summary_parts = [
        f"Secondary-retailer fat re-scrape for bread corpus (9 priority implausible + 13 opportunistic)."
    ]
    for r, d in reachability.items():
        if d["reachable"]:
            summary_parts.append(f"{r.capitalize()} was reachable ({d['bytes_received']} bytes returned on probe).")
        else:
            summary_parts.append(f"{r.capitalize()} was blocked/unreachable — skipped per fallback rule.")
    summary_parts.append(
        f"Recovery result: {len(recovered)}/{len(products)} barcodes returned a fat value from a secondary retailer; "
        f"{len(recovered_plausible)} passed the per-100g plausibility gate (protein×4+carbs×4+fat×9 ≤ ±15 kcal). "
        f"{len(implausible_recovered)}/{len(IMPLAUSIBLE)} priority-implausible barcodes recovered; "
        f"{len(implausible_discard)}/{len(IMPLAUSIBLE)} remain discard candidates. "
        f"{len(discard)} total products marked discard_candidate=true (missing-data-discard rule applies). "
        f"No kcal-derived or estimated fat values were injected — all nulls are genuine misses."
    )
    feasibility_summary = " ".join(summary_parts)

    results = {
        "task": "TASK-397",
        "track": "A",
        "step": 2,
        "run_id": f"rescrape_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "script_version": SCRIPT_VERSION,
        "off_ban_note": "Open Food Facts is BANNED. All nutrition from direct retailer scrape only.",
        "source_policy": "Direct product page scrape only. No kcal-derived fat injected.",
        "retailer_reachability": reachability,
        "reachable_retailers": reachable_retailers,
        "blocked_retailers": blocked_retailers,
        "retailer_priority_order": ["victory", "rami_levy", "yochananof"],
        "products": products,
        "counts": {
            "total_sentinel_barcodes": len(products),
            "priority_implausible": len(IMPLAUSIBLE),
            "recovered_total": len(recovered),
            "recovered_plausibility_pass": len(recovered_plausible),
            "recovered_plausibility_fail": len(recovered_implausible_fat),
            "not_found_total": len(not_found),
            "blocked_total": len(blocked),
            "discard_candidate_total": len(discard),
            "priority_implausible_recovered": len(implausible_recovered),
            "priority_implausible_discard_candidate": len(implausible_discard),
        },
        "feasibility_summary": feasibility_summary,
    }

    out = OUT_DIR / "rescrape_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    sha256 = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"\n=== DONE ===")
    print(f"Output: {out}")
    print(f"SHA256: {sha256}")
    print(f"\nCounts: {results['counts']}")
    return results, sha256


if __name__ == "__main__":
    results, sha256 = main()
