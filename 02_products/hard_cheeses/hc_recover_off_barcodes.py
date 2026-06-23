"""
HC OFF-Barcode Recovery — TASK-380 BSIP0→BSIP1
===============================================

Goal: find 7290102302864 (Gouda Pesto) and 7290014455252 (Grana Padano) at a
DIRECT Israeli retailer (Shufersal first, then Victory, then skip others if
unreachable from sandbox) and produce clean BSIP1 records without any
Open Food Facts data.

Rules:
- OFF BANNED — no import of any OFF client, no OFF field, no fallback.
- Missing-data discard: if no nutrition found one-shot, mark DISCARD.
- Plausibility gate mandatory on every panel (DAIRY_SOLID floor=20g).
- Provenance stamped on every field sourced from a retailer.

Run:
    python C:\\Bari\\02_products\\hard_cheeses\\hc_recover_off_barcodes.py

Outputs:
    02_products/hard_cheeses/bsip1_outputs/bsip1_hardcheese_7290102302864.json
    02_products/hard_cheeses/bsip1_outputs/bsip1_hardcheese_7290014455252.json
    (or DISCARD record if not found / fails plausibility)
    02_products/hard_cheeses/HC_REWORK_RUN_LOG.json  (reachability + per-barcode result)
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
BSIP1_DIR = BASE_DIR / "bsip1_outputs"
BSIP1_DIR.mkdir(parents=True, exist_ok=True)

SHARED = Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")
sys.path.insert(0, str(SHARED))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402
from plausibility_gate import check_panel, FoodClass  # noqa: E402

RUN_TS = datetime.now(timezone.utc).isoformat()
RUN_ID = f"hc_recover_off_barcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# ---------------------------------------------------------------------------
# Target barcodes
# ---------------------------------------------------------------------------
TARGETS = [
    {
        "barcode": "7290102302864",
        "name_hint": "Gouda Pesto",
        "name_he_hint": "גאודה פסטו ירוק",
        "reason": "open_food_facts_fallback — nutrition tab missing at yohananof",
        "yohananof_ingredients_captured": True,   # ingredients.html exists
        "yohananof_nutrition_captured": False,     # tab_missing
    },
    {
        "barcode": "7290014455252",
        "name_hint": "Grana Padano",
        "name_he_hint": "גבינה איטלקית גרנה פדנו",
        "reason": "open_food_facts_fallback — dialog_missing at yohananof",
        "yohananof_ingredients_captured": False,
        "yohananof_nutrition_captured": False,
    },
]

# ---------------------------------------------------------------------------
# Retailers to probe (in priority order per SOURCE_SELECTION_POLICY.md)
# ---------------------------------------------------------------------------
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}

RETAILERS = [
    {
        "id": "shufersal",
        "name": "Shufersal",
        "probe_url": "https://www.shufersal.co.il",
        "product_url_template": "https://www.shufersal.co.il/online/he/p/P_{barcode}/json",
        "product_page_template": "https://www.shufersal.co.il/online/he/p/P_{barcode}",
        "search_url_template": (
            "https://www.shufersal.co.il/online/he/search/results"
            "?q={barcode}%3Arelevance&pageSize=12"
        ),
    },
    {
        "id": "victory",
        "name": "Victory",
        "probe_url": "https://www.victoryonline.co.il",
        "search_url_template": "https://www.victoryonline.co.il/category?search={barcode}",
    },
    {
        "id": "yochananof",
        "name": "Yochananof",
        "probe_url": "https://www.yochananof.co.il",
        "search_url_template": "https://www.yochananof.co.il/?s={barcode}",
    },
    {
        "id": "rami_levy",
        "name": "Rami Levy",
        "probe_url": "https://www.ramilevi.co.il",
        "search_url_template": "https://www.ramilevi.co.il/Web/Catalog/Subcategory?subCatId=-1&q={barcode}",
    },
]

# ---------------------------------------------------------------------------
# Reachability probe
# ---------------------------------------------------------------------------

def probe_retailer(retailer: dict, timeout: int = 15) -> dict:
    url = retailer["probe_url"]
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return {
            "retailer": retailer["id"],
            "reachable": r.status_code < 400,
            "status_code": r.status_code,
            "body_bytes": len(r.content),
            "note": "OK" if r.status_code < 400 else f"HTTP {r.status_code}",
        }
    except requests.exceptions.SSLError as e:
        return {"retailer": retailer["id"], "reachable": False, "status_code": None,
                "body_bytes": 0, "note": f"SSL error: {str(e)[:80]}"}
    except requests.exceptions.ConnectionError as e:
        return {"retailer": retailer["id"], "reachable": False, "status_code": None,
                "body_bytes": 0, "note": f"Connection error: {str(e)[:80]}"}
    except Exception as e:
        return {"retailer": retailer["id"], "reachable": False, "status_code": None,
                "body_bytes": 0, "note": f"Error: {str(e)[:80]}"}


# ---------------------------------------------------------------------------
# Shufersal — barcode lookup via product page P_{barcode}
# ---------------------------------------------------------------------------

def _parse_shufersal_product_page(html: str, barcode: str) -> dict | None:
    """Parse a Shufersal product page for nutrition, ingredients, name."""
    soup = BeautifulSoup(html, "html.parser")

    # LD+JSON structured data
    ld_name, ld_gtin, ld_brand, ld_images = "", "", "", []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                brand = ld.get("brand", "")
                ld_brand = brand.get("name", "") if isinstance(brand, dict) else (brand or "")
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # If no LD+JSON product and name is empty → likely 404/redirect
    if not ld_name and not ld_gtin:
        # Check for product name in page
        h1 = soup.find("h1")
        if not h1 or len(h1.get_text(strip=True)) < 3:
            return None  # No product found

    # Nutrition — shared parser
    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    # Ingredients
    ingredients_raw = ""
    for label_text in ["רכיבים", "רכיב"]:
        ingr_label = soup.find(string=re.compile(label_text))
        if ingr_label:
            parent = ingr_label.find_parent()
            container = parent.find_parent() if parent else None
            if container:
                full_text = container.get_text(separator=" ", strip=True)
                m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
                if m:
                    ingredients_raw = m.group(1).strip()[:1500]
                    break
    if not ingredients_raw:
        for li in soup.find_all("li"):
            text = li.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{20,})", text)
            if m:
                ingredients_raw = m.group(1)[:1500]
                break

    name_he = ld_name or ""
    found_barcode = ld_gtin or ld_gtin or barcode

    return {
        "source": "shufersal",
        "name_he": name_he,
        "barcode_found": found_barcode,
        "brand": ld_brand,
        "image_url": ld_images[0] if ld_images else None,
        "nutrition_raw": nutr_raw,
        "nutrition_html_src": nutr_src,
        "ingredients_raw": ingredients_raw,
    }


def scrape_shufersal_barcode(barcode: str) -> dict | None:
    """Try to fetch a product from Shufersal by barcode. Returns parsed data or None."""
    # Shufersal barcode search via search results
    search_url = (
        f"https://www.shufersal.co.il/online/he/search/results"
        f"?q={barcode}%3Arelevance&pageSize=12"
    )
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=25, allow_redirects=True)
    except Exception as e:
        print(f"  [Shufersal search error] {e}", flush=True)
        return None

    if r.status_code != 200:
        print(f"  [Shufersal search] HTTP {r.status_code}", flush=True)
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Find product code matching our barcode from the search results
    product_code = None
    for li in soup.find_all("li", attrs={"data-product-code": True}):
        code = li.attrs.get("data-product-code", "")
        # Product code at Shufersal can be P_<barcode> or just the barcode
        if barcode in code or barcode == code.replace("P_", ""):
            product_code = code
            break

    # Also check ld+json for gtin
    if not product_code:
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                ld = json.loads(script.string)
                # ItemList with products
                if ld.get("@type") == "ItemList":
                    for item in ld.get("itemListElement", []):
                        prod = item.get("item", {})
                        if prod.get("gtin13") == barcode or prod.get("gtin") == barcode:
                            url_part = prod.get("url", "")
                            m = re.search(r"/p/([A-Za-z0-9_]+)", url_part)
                            if m:
                                product_code = m.group(1)
                            break
            except Exception:
                pass

    # Try direct product URL even without finding it in search
    # Shufersal product URL pattern: /online/he/p/P_<barcode>
    product_url = f"https://www.shufersal.co.il/online/he/p/P_{barcode}"
    print(f"  [Shufersal] Trying product URL: {product_url}", flush=True)
    try:
        r2 = requests.get(product_url, headers=HEADERS, timeout=25, allow_redirects=True)
    except Exception as e:
        print(f"  [Shufersal product page error] {e}", flush=True)
        return None

    if r2.status_code != 200:
        print(f"  [Shufersal product page] HTTP {r2.status_code} for {product_url}", flush=True)
        return None

    # Check we didn't get redirected to a generic page (maintenance / 404 page)
    page_text = r2.text
    if len(page_text) < 3000:
        print(f"  [Shufersal product page] Response too short ({len(page_text)} chars), likely empty", flush=True)
        return None

    result = _parse_shufersal_product_page(page_text, barcode)
    if result:
        result["source_url"] = r2.url
        result["fetched_at"] = RUN_TS
        print(f"  [Shufersal] Found: name_he={result['name_he']!r}, "
              f"nutr_keys={list(k for k, v in result['nutrition_raw'].items() if v)}", flush=True)
    return result


# ---------------------------------------------------------------------------
# Victory — barcode search
# ---------------------------------------------------------------------------

def scrape_victory_barcode(barcode: str) -> dict | None:
    """Try to fetch a product from Victory by barcode search."""
    search_url = f"https://www.victoryonline.co.il/category?search={barcode}"
    print(f"  [Victory] Searching: {search_url}", flush=True)
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=25, allow_redirects=True)
    except Exception as e:
        print(f"  [Victory search error] {e}", flush=True)
        return None

    if r.status_code != 200:
        print(f"  [Victory search] HTTP {r.status_code}", flush=True)
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Victory uses same SaaS as Yohananof — look for product cards
    name_he = None
    image_url = None

    # Try to find a product card that contains the barcode
    page_text = r.text
    if barcode not in page_text:
        print(f"  [Victory] Barcode {barcode} not found in search results", flush=True)
        return None

    # Product found — try to get more data
    print(f"  [Victory] Barcode found in page, attempting nutrition parse", flush=True)

    # Victory nutrition is in a modal — can't get it without Playwright
    # Mark as found (identity) but nutrition unavailable without JS rendering
    return {
        "source": "victory",
        "found_in_search": True,
        "nutrition_raw": {},
        "ingredients_raw": "",
        "note": "Victory barcode found in search but nutrition requires Playwright modal — not reachable from sandbox",
        "fetched_at": RUN_TS,
    }


# ---------------------------------------------------------------------------
# Nutrition normalization
# ---------------------------------------------------------------------------

def normalize_nutrition(nutr_raw: dict) -> dict:
    """Convert shared parse_nutrition_list output to canonical per-100g dict."""
    def to_float(v) -> float | None:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        # Try to parse string like "34.0 g", "≤ 0.5", "<1"
        m = re.search(r"[\d.]+", str(v).replace(",", "."))
        return float(m.group(0)) if m else None

    return {
        "energy_kcal": to_float(nutr_raw.get("energy") or nutr_raw.get("energy_kcal")),
        "fat_g": to_float(nutr_raw.get("fat")),
        "fat_saturated_g": to_float(nutr_raw.get("saturated") or nutr_raw.get("saturated_fat")),
        "fat_trans_g": to_float(nutr_raw.get("trans") or nutr_raw.get("trans_fat")),
        "carbohydrates_g": to_float(nutr_raw.get("carbs") or nutr_raw.get("carbohydrates")),
        "sugars_g": to_float(nutr_raw.get("sugars") or nutr_raw.get("sugar")),
        "dietary_fiber_g": to_float(nutr_raw.get("fiber") or nutr_raw.get("dietary_fiber")),
        "protein_g": to_float(nutr_raw.get("protein")),
        "sodium_mg": to_float(nutr_raw.get("sodium")),
        "calcium_mg": to_float(nutr_raw.get("calcium")),
    }


# ---------------------------------------------------------------------------
# Plausibility check (dairy_solid)
# ---------------------------------------------------------------------------

def run_plausibility_gate(nutr: dict, ingredients_text: str | None) -> dict:
    """Run the mandatory plausibility gate for dairy_solid."""
    verdict = check_panel(
        {
            "energyKcal": nutr.get("energy_kcal"),
            "carbs": nutr.get("carbohydrates_g"),
            "fat": nutr.get("fat_g"),
            "protein": nutr.get("protein_g"),
            "sugar": nutr.get("sugars_g"),
        },
        food_class=FoodClass.DAIRY_SOLID,
        ingredients_text=ingredients_text,
    )
    return {
        "ok": verdict.ok,
        "food_class": verdict.food_class,
        "accounted_mass": verdict.accounted_mass,
        "reasons": verdict.reasons,
    }


# ---------------------------------------------------------------------------
# BSIP1 record builder
# ---------------------------------------------------------------------------

def build_bsip1(barcode: str, target: dict, scrape_result: dict,
                nutr: dict, gate: dict, source_retailer: str) -> dict:
    """Build a BSIP1 record from a successful direct scrape."""
    ingredients_list = []
    ing_text = scrape_result.get("ingredients_raw", "") or ""
    if ing_text:
        # Split on commas, periods at end, semicolons — clean up
        raw_parts = re.split(r"[,;]", ing_text)
        ingredients_list = [p.strip().rstrip(".") for p in raw_parts if len(p.strip()) > 1]

    # Nova proxy (simple rule for hard cheese)
    nova = 1
    nova_notes = ["simple hard cheese ingredient profile → NOVA 1 candidate"]
    additive_count = 0
    detected_additives = []
    if ing_text:
        # Check for additives (E-numbers, preservatives)
        e_matches = re.findall(r"E[-\s]?\d{3,4}[a-zA-Z]?", ing_text, re.I)
        detected_additives = list(set(e_matches))
        additive_count = len(detected_additives)
        if additive_count > 0:
            nova = 2
            nova_notes = [f"additive detected ({', '.join(detected_additives)}) → NOVA 2"]
        # Check for flavor/color additives
        if re.search(r"צבע מאכל|מייצב|חומר משמר|חומצה", ing_text):
            nova = max(nova, 2)
            nova_notes.append("stabilizer/preservative/color found")

    missing = [k for k, v in nutr.items() if v is None and k in (
        "energy_kcal", "fat_g", "fat_saturated_g", "carbohydrates_g",
        "sugars_g", "protein_g", "sodium_mg")]

    confidence = 0.85
    trust_level = "high"
    if len(missing) > 2:
        confidence = 0.70
        trust_level = "medium"
    elif len(missing) > 0:
        confidence = 0.75

    risk_flags = []
    if source_retailer == "shufersal" and len(missing) == 0:
        risk_flags = []
    elif len(missing) > 0:
        risk_flags = [f"missing_fields: {missing}"]

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": f"bsip1_hardcheese_{barcode}",
        "barcode": barcode,
        "canonical_name_he": scrape_result.get("name_he") or target.get("name_he_hint", ""),
        "brand": scrape_result.get("brand") or None,
        "weight_g": None,
        "category": "hard_cheeses",
        "bsip_cheese_subpool": "hard" if "גרנה" in (scrape_result.get("name_he") or "") or "פרמזן" in (scrape_result.get("name_he") or "") else "yellow",
        "source_retailers": [source_retailer],
        "retailer_prices": {source_retailer: None},
        "image_url": scrape_result.get("image_url") or None,
        "fat_per_100g_scored": nutr.get("fat_g"),
        "fat_in_dry_matter_pct": None,
        "both_fat_values_on_label": False,
        "fat_label_documentation": None,
        "normalized_nutrition_per_100g": nutr,
        "energy_kcal": nutr.get("energy_kcal"),
        "fat_g": nutr.get("fat_g"),
        "fat_saturated_g": nutr.get("fat_saturated_g"),
        "fat_trans_g": nutr.get("fat_trans_g"),
        "protein_g": nutr.get("protein_g"),
        "carbohydrates_g": nutr.get("carbohydrates_g"),
        "sugars_g": nutr.get("sugars_g"),
        "sodium_mg": nutr.get("sodium_mg"),
        "dietary_fiber_g": nutr.get("dietary_fiber_g"),
        "calcium_mg": nutr.get("calcium_mg"),
        "ingredients_text_he": ing_text or None,
        "ingredients_list": ingredients_list,
        "ingredient_count": len(ingredients_list),
        "ingredient_text_quality": "good" if ingredients_list else "absent",
        "allergens_contains": ["milk"],
        "allergens_may_contain": [],
        "confidence": confidence,
        "canonical_trust_level": trust_level,
        "canonical_trust_score": confidence,
        "conflicts_summary": [],
        "missing_fields": missing,
        "inferred_fields": [],
        "audit_ref": None,
        "nova_proxy": nova,
        "nova_confidence": 0.7,
        "nova_confidence_band": "medium",
        "nova_notes": nova_notes,
        "detected_additives": detected_additives,
        "additive_count": additive_count,
        "data_sufficiency": "sufficient" if nutr.get("fat_g") and nutr.get("protein_g") else "insufficient",
        "bsip1_trust_level": trust_level,
        "bsip1_trust_score": confidence,
        "bsip1_risk_flags": risk_flags,
        "nutrition_consistency_status": "consistent" if gate["ok"] else "suspect",
        "consistency_checks": {
            "sugar_le_carbs": (
                (nutr.get("sugars_g") or 0) <= (nutr.get("carbohydrates_g") or float("inf"))
                if nutr.get("sugars_g") is not None else None
            ),
            "satfat_le_fat": (
                (nutr.get("fat_saturated_g") or 0) <= (nutr.get("fat_g") or float("inf"))
                if nutr.get("fat_saturated_g") is not None else None
            ),
            "kcal_plausible": gate["ok"],
            "macros_plausible": gate["ok"],
        },
        "plausibility_gate": gate,
        "provenance": {
            "source": f"{source_retailer}_storefront",
            "source_url": scrape_result.get("source_url") or None,
            "fetched_at": scrape_result.get("fetched_at") or RUN_TS,
            "panel_source": f"{source_retailer}_storefront",
            "verification_status": "candidate",
            "client_version": f"{source_retailer}_direct_scrape/1.0",
            "off_used": False,
        },
        "enrichment_timestamp": RUN_TS,
        "run_id": RUN_ID,
    }


def build_discard_record(barcode: str, target: dict, reason: str,
                         scrape_attempts: list[dict]) -> dict:
    """Build a DISCARD BSIP1 record (product cannot be recovered)."""
    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": f"bsip1_hardcheese_{barcode}",
        "barcode": barcode,
        "canonical_name_he": target.get("name_he_hint", ""),
        "category": "hard_cheeses",
        "data_sufficiency": "discard",
        "discard_reason": reason,
        "discard_per_rule": "missing_data_discard_rule (owner-2026-06-13)",
        "off_used": False,
        "scrape_attempts": scrape_attempts,
        "provenance": {
            "source": "none",
            "fetched_at": RUN_TS,
            "off_used": False,
            "verification_status": "discarded",
        },
        "enrichment_timestamp": RUN_TS,
        "run_id": RUN_ID,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70, flush=True)
    print(f"HC OFF-Barcode Recovery  run_id={RUN_ID}", flush=True)
    print(f"Targets: {[t['barcode'] for t in TARGETS]}", flush=True)
    print("=" * 70, flush=True)

    # 1) Reachability probe
    print("\n--- Reachability probe ---", flush=True)
    reachability = []
    for retailer in RETAILERS:
        print(f"  Probing {retailer['name']} ({retailer['probe_url']})...", flush=True)
        result = probe_retailer(retailer, timeout=15)
        reachability.append(result)
        status = "REACHABLE" if result["reachable"] else "BLOCKED"
        print(f"  {retailer['name']}: {status} — {result['note']}", flush=True)
        time.sleep(0.5)

    reachable_ids = {r["retailer"] for r in reachability if r["reachable"]}
    print(f"\n  Reachable retailers: {sorted(reachable_ids)}", flush=True)

    # 2) Per-barcode recovery
    results = []

    for target in TARGETS:
        barcode = target["barcode"]
        print(f"\n--- Recovering {barcode} ({target['name_hint']}) ---", flush=True)

        scrape_attempts = []
        recovered = False
        scrape_result = None
        source_retailer = None

        # --- Shufersal (priority 1) ---
        if "shufersal" in reachable_ids:
            print("  Attempting Shufersal...", flush=True)
            time.sleep(1.0)
            sr = scrape_shufersal_barcode(barcode)
            attempt = {
                "retailer": "shufersal",
                "attempted": True,
                "found": bool(sr and sr.get("name_he")),
                "nutrition_fields": list(k for k, v in (sr.get("nutrition_raw") or {}).items() if v) if sr else [],
                "ingredients_found": bool(sr and sr.get("ingredients_raw")),
            }
            scrape_attempts.append(attempt)
            if sr and sr.get("name_he") and sr.get("nutrition_raw"):
                nutr_normalized = normalize_nutrition(sr.get("nutrition_raw", {}))
                has_core_nutrition = (
                    nutr_normalized.get("fat_g") is not None and
                    nutr_normalized.get("protein_g") is not None and
                    nutr_normalized.get("energy_kcal") is not None
                )
                if has_core_nutrition:
                    scrape_result = sr
                    source_retailer = "shufersal"
                    print(f"  Shufersal FOUND with nutrition: fat={nutr_normalized['fat_g']}, "
                          f"protein={nutr_normalized['protein_g']}, kcal={nutr_normalized['energy_kcal']}", flush=True)
                    recovered = True
                else:
                    print(f"  Shufersal: found product but missing core nutrition fields", flush=True)
            else:
                print(f"  Shufersal: not found or no name returned", flush=True)

        # --- Victory (priority 2) ---
        if not recovered and "victory" in reachable_ids:
            print("  Attempting Victory...", flush=True)
            time.sleep(1.0)
            vr = scrape_victory_barcode(barcode)
            attempt = {
                "retailer": "victory",
                "attempted": True,
                "found": bool(vr and vr.get("found_in_search")),
                "nutrition_fields": [],
                "note": vr.get("note") if vr else "not found",
            }
            scrape_attempts.append(attempt)
            if vr and vr.get("found_in_search"):
                print(f"  Victory: product found in search but nutrition requires Playwright (blocked). "
                      f"Cannot recover nutrition from Victory in sandbox.", flush=True)
            else:
                print(f"  Victory: product not found", flush=True)

        # --- Yochananof (already attempted in original run; check what was captured) ---
        # The yohananof_scrape folder has what was captured
        yoh_dir = BASE_DIR / "yohananof_scrape" / barcode
        yoh_has_nutrition = (yoh_dir / "nutrition.html").exists() and (yoh_dir / "nutrition.html").stat().st_size > 100
        yoh_has_ingredients = (yoh_dir / "ingredients.html").exists() and (yoh_dir / "ingredients.html").stat().st_size > 100
        scrape_attempts.append({
            "retailer": "yochananof",
            "attempted": True,
            "method": "prior_playwright_scrape",
            "nutrition_captured": yoh_has_nutrition,
            "ingredients_captured": yoh_has_ingredients,
            "status": "tab_missing" if not yoh_has_nutrition else "success",
        })
        print(f"  Yochananof (prior scrape): nutrition_html={yoh_has_nutrition}, ingredients_html={yoh_has_ingredients}", flush=True)

        # --- Rami Levy (known blocked) ---
        scrape_attempts.append({
            "retailer": "rami_levy",
            "attempted": False,
            "reason": "known blocked from sandbox (rami_levy.yaml DEFERRED)",
        })

        # 3) Build BSIP1 or DISCARD
        if recovered and scrape_result:
            nutr = normalize_nutrition(scrape_result.get("nutrition_raw", {}))
            gate = run_plausibility_gate(nutr, scrape_result.get("ingredients_raw"))
            print(f"  Plausibility gate: ok={gate['ok']}, reasons={gate['reasons']}", flush=True)

            if gate["ok"]:
                bsip1 = build_bsip1(barcode, target, scrape_result, nutr, gate, source_retailer)
                out_path = BSIP1_DIR / f"bsip1_hardcheese_{barcode}.json"
                out_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  RECOVERED → {out_path}", flush=True)
                results.append({
                    "barcode": barcode,
                    "status": "RECOVERED",
                    "source_retailer": source_retailer,
                    "output_path": str(out_path),
                    "name_he": bsip1.get("canonical_name_he"),
                    "nutrition_summary": {
                        "energy_kcal": nutr.get("energy_kcal"),
                        "fat_g": nutr.get("fat_g"),
                        "fat_saturated_g": nutr.get("fat_saturated_g"),
                        "protein_g": nutr.get("protein_g"),
                        "carbohydrates_g": nutr.get("carbohydrates_g"),
                        "sodium_mg": nutr.get("sodium_mg"),
                    },
                    "ingredients_captured": bool(scrape_result.get("ingredients_raw")),
                    "plausibility": gate,
                    "scrape_attempts": scrape_attempts,
                })
            else:
                # Nutrition found but fails plausibility gate → DISCARD
                reason = f"plausibility_gate_fail: {'; '.join(gate['reasons'])}"
                bsip1 = build_discard_record(barcode, target, reason, scrape_attempts)
                bsip1["plausibility_gate"] = gate
                bsip1["nutrition_captured"] = nutr
                out_path = BSIP1_DIR / f"bsip1_hardcheese_{barcode}.json"
                out_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  DISCARD (plausibility fail) → {out_path}", flush=True)
                results.append({
                    "barcode": barcode,
                    "status": "DISCARD",
                    "reason": reason,
                    "output_path": str(out_path),
                    "scrape_attempts": scrape_attempts,
                })
        else:
            reason = "not_found_at_any_reachable_retailer_one_shot"
            bsip1 = build_discard_record(barcode, target, reason, scrape_attempts)
            out_path = BSIP1_DIR / f"bsip1_hardcheese_{barcode}.json"
            out_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  DISCARD (not found) → {out_path}", flush=True)
            results.append({
                "barcode": barcode,
                "status": "DISCARD",
                "reason": reason,
                "output_path": str(out_path),
                "scrape_attempts": scrape_attempts,
            })

    # 4) OFF contamination check on BSIP1 dir
    print("\n--- OFF contamination check on bsip1_outputs ---", flush=True)
    bsip1_files = list(BSIP1_DIR.glob("*.json"))
    off_files = []
    for f in bsip1_files:
        content = f.read_text(encoding="utf-8")
        if "open_food_facts" in content.lower():
            off_files.append(str(f.name))

    print(f"  Total BSIP1 files: {len(bsip1_files)}", flush=True)
    print(f"  Files with 'open_food_facts': {len(off_files)}", flush=True)
    if off_files:
        print(f"  OFF-contaminated files: {off_files}", flush=True)

    # 5) Write run log
    run_log = {
        "run_id": RUN_ID,
        "run_timestamp": RUN_TS,
        "targets": [t["barcode"] for t in TARGETS],
        "reachability": reachability,
        "results": results,
        "bsip1_dir_total_files": len(bsip1_files),
        "off_contaminated_files_in_bsip1_dir": off_files,
        "off_count": len(off_files),
    }
    log_path = BASE_DIR / "HC_REWORK_RUN_LOG.json"
    log_path.write_text(json.dumps(run_log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRun log → {log_path}", flush=True)

    # 6) Summary
    print("\n" + "=" * 70, flush=True)
    print("SUMMARY", flush=True)
    for r in results:
        print(f"  {r['barcode']}: {r['status']} — {r.get('source_retailer', r.get('reason', ''))}", flush=True)
    print(f"  OFF files in bsip1_outputs: {len(off_files)}", flush=True)
    print("=" * 70, flush=True)

    return run_log


if __name__ == "__main__":
    main()
