"""
Shufersal BSIP0 storefront scraper — direct-by-barcode requests + BeautifulSoup.

Architecture:
  1. il_prices feed (prices.shufersal.co.il) → barcodes + names + prices [identity]
  2. requests + BeautifulSoup, direct product-by-barcode URL → product pages [nutrition]

FIX HISTORY (TASK-582, 2026-07-10): the previous URL template
(``https://www.shufersal.co.il/online/he/A{barcode}``) 404s on every request — stale.
The verified-live pattern is ``https://www.shufersal.co.il/online/he/p/p_{barcode}``,
confirmed working by 03_operations/shelf_watch/shelf_watch.py::fetch_shufersal_product
(live canary runs 2026-07-10). This script's request layer now mirrors that exact
fetch construction (URL template, headers, status/maintenance/ld+json-gtin checks) —
plain ``requests``, no browser/crawlee needed; the old crawlee+DefaultFingerprintGenerator
architecture (kept for a TLS-fingerprint block that a corrected direct URL does not hit)
is removed. Nutrition parsing now uses the shared canonical parser
(03_operations/bsip0/scrape/_shared/bsip0_nutrition.py) that every other Shufersal
BSIP0 scraper uses, instead of the previous ad-hoc whole-page regex scan — this avoids
resurrecting the EV-026/EV-029 fat-field-overwrite bug class the shared module exists
to prevent.

OFF is NOT a source anywhere in this script (project-wide ban, TASK-238) — the earlier
docstring's "OFF fallback" line described something never implemented in code and has
been removed as part of this fix.

Run from C:\Bari:
    python 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py --category juices --limit 40
    python 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py --category hard_cheeses --limit 40
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parents[1] / "_shared"))
import bsip0_nutrition as bn  # noqa: E402

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SHUFERSAL_BASE = "https://www.shufersal.co.il"
SHUFERSAL_PRODUCT_URL = SHUFERSAL_BASE + "/online/he/p/p_{barcode}"
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}
REQUEST_TIMEOUT = 25
REQUEST_DELAY_S = 0.6

CATEGORY_QUERIES: dict[str, list[str]] = {
    "juices": ["מיץ", "מיצים", "נקטר", "משקה פירות", "סחוט", "smoothie"],
    "hard_cheeses": ["גבינה צהובה", "גבינה קשה", "עמק", "גאודה", "אמנטל", "קשקבל", "גבינה בולגרית", "צפתית"],
    "breakfast_cereals": ["קורנפלקס", "גרנולה", "דגני בוקר", "שיבולת שועל", "מוזלי"],
    "yogurt": ["יוגורט", "לבן", "גביע"],
    "snack_bars": ["חטיף", "אנרגיה", "granola bar"],
}

# DOM selectors for Shufersal product pages (React SSR + hydration)
NUTRITION_SELECTORS = [
    "[class*='nutritionTable']",
    "[class*='nutrition-table']",
    "[class*='NutritionTable']",
    "[data-testid*='nutrition']",
    ".nutrition",
    "#nutrition",
    "[class*='productNutrition']",
    "[class*='product-nutrition']",
]

INGREDIENT_SELECTORS = [
    "[class*='ingredient']",
    "[class*='Ingredient']",
    "[data-testid*='ingredient']",
    "[class*='productIngredient']",
]

BLOCK_SIGNALS = ["Maintenance1.jpg", "s3-eu-west-1.amazonaws.com/www.shufersal.co.il"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_output_path(category: str, run_id: str) -> Path:
    out_dir = Path(f"02_products/{category}/bsip0_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"bsip0_shufersal_{category}_{run_id}.json"


def extract_ingredients(soup: BeautifulSoup) -> str:
    """Shufersal product-page ingredients. PRIMARY: div.componentsText (the precise
    container confirmed live — see shelf_watch.py::extract_ingredients for the same
    approach). FALLBACK: the class-substring selectors this script already carried
    (INGREDIENT_SELECTORS), then a broad 'רכיב' text search."""
    container = soup.select_one("div.componentsText")
    if container is not None:
        return container.get_text(" ", strip=True)

    for sel in INGREDIENT_SELECTORS:
        el = soup.select_one(sel)
        if el is not None:
            text = el.get_text(" ", strip=True)
            if text:
                return text

    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        broad = parent.find_parent() if parent else None
        if broad:
            full_text = broad.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                return m.group(1).strip()
    return ""


# ---------------------------------------------------------------------------
# Fetch (requests + BeautifulSoup, direct-by-barcode URL — TASK-582 fix).
# Mirrors 03_operations/shelf_watch/shelf_watch.py::fetch_shufersal_product, the
# verified-live fetch construction (URL template, headers, status/maintenance/
# ld+json-gtin checks). Returns a status envelope, never raises.
# ---------------------------------------------------------------------------

def fetch_shufersal_product(barcode: str) -> dict:
    url = SHUFERSAL_PRODUCT_URL.format(barcode=barcode)
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except Exception as e:
        return {"status": "scrape_failed", "reason": f"request_exception: {str(e)[:200]}", "barcode": barcode}

    if r.status_code == 404:
        return {"status": "page_gone", "reason": "http_404_on_direct_barcode_url", "barcode": barcode,
                "final_url": r.url}
    if r.status_code != 200:
        return {"status": "scrape_failed", "reason": f"http_{r.status_code}", "barcode": barcode}

    text = r.text
    if len(text) < 5000 and any(s in text.lower() for s in ("maintenance", "אתר בתחזוקה", "בתחזוקה")):
        return {"status": "scrape_failed", "reason": "maintenance_page", "barcode": barcode}
    if any(sig in text for sig in BLOCK_SIGNALS):
        return {"status": "scrape_failed", "reason": "block_signal_detected", "barcode": barcode}

    soup = BeautifulSoup(text, "html.parser")

    ld_gtin = ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
        except Exception:
            continue
        if ld.get("@type") == "Product":
            ld_gtin = ld.get("gtin13", ld.get("gtin", "")) or ""
            break

    if not ld_gtin:
        return {"status": "scrape_failed", "reason": "no_ld_json_product_block", "barcode": barcode,
                "final_url": r.url}
    if str(ld_gtin).strip() != barcode:
        return {"status": "page_gone", "reason": f"gtin_mismatch: resolved to {ld_gtin}", "barcode": barcode,
                "final_url": r.url}

    title = soup.title.get_text(strip=True) if soup.title else ""
    product_name = title.split("|")[0].strip() if "|" in title else title

    # Nutrition — the shared canonical parser (same module every other Shufersal BSIP0
    # scraper uses; see module docstring for why this replaces the old ad-hoc regex scan).
    # parse_nutrition_list() returns bare field names ("fat", "sodium", "energy", ...);
    # parse_nutrition_numeric() requires the "_raw"-suffixed key contract
    # shufersal_cereals/01_scrape_cereals.py uses (the live cereals corpus builder) —
    # note "energy" (bare) -> "energy_kcal_raw", NOT a generic f"{k}_raw" suffix.
    # Passing parse_nutrition_list()'s output straight into parse_nutrition_numeric()
    # without this exact rename silently returns None for every field (found live while
    # canary-testing this fix, TASK-582 — same latent gap present in shelf_watch.py's
    # identical direct-chain call; flagged separately, not fixed here as shelf_watch.py
    # is out of this task's scope).
    nutr_bare = bn.parse_nutrition_list(soup)
    nutr_for_numeric = {
        "energy_kcal_raw": nutr_bare.get("energy", ""),
        "protein_raw": nutr_bare.get("protein", ""),
        "carbs_raw": nutr_bare.get("carbs", ""),
        "fat_raw": nutr_bare.get("fat", ""),
        "fiber_raw": nutr_bare.get("fiber", ""),
        "sodium_raw": nutr_bare.get("sodium", ""),
        "sugar_raw": nutr_bare.get("sugar", ""),
        "saturated_fat_raw": nutr_bare.get("saturated_fat", ""),
    }
    nutrition = {k: v for k, v in bn.parse_nutrition_numeric(nutr_for_numeric).items()
                 if not k.startswith("_") and v is not None}

    ingredients_text = extract_ingredients(soup)

    sufficient = bool(nutrition.get("energy_kcal") or nutrition.get("fat_g") or nutrition.get("protein_g"))

    return {
        "status": "scraped",
        "barcode": barcode,
        "final_url": r.url,
        "name": product_name,
        "nutrition": nutrition,
        "ingredients_raw_he": ingredients_text,
        "sufficient": sufficient,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


class ShufersalScraper:
    def __init__(self, barcodes: list[str], category: str):
        self.barcodes = barcodes
        self.category = category
        self.results: dict[str, dict] = {}

    def run(self) -> list[dict]:
        for i, barcode in enumerate(self.barcodes, 1):
            r = fetch_shufersal_product(barcode)
            if r["status"] == "scraped":
                record = {
                    "barcode": barcode,
                    "name": r["name"],
                    "category": self.category,
                    "retailer": "shufersal",
                    "source_url": r["final_url"],
                    "nutrition": r["nutrition"],
                    "ingredients_raw_he": r["ingredients_raw_he"],
                    "sufficient": r["sufficient"],
                    "provenance": {
                        "panel_source": "shufersal_storefront",
                        "verification_status": "candidate",
                        "fetched_at": r["fetched_at"],
                    },
                }
                self.results[barcode] = record
                status = "OK" if r["sufficient"] else "no_panel"
                print(f"  [{barcode}] {status} — {r['name'][:50]}")
            else:
                print(f"  [{barcode}] {r['status']} — {r.get('reason')}")
            if i < len(self.barcodes):
                time.sleep(REQUEST_DELAY_S)
        return list(self.results.values())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(category: str, limit: int) -> None:
    sys.path.insert(0, str(Path(__file__).parents[4]))
    from integrations.clients.il_prices import fetch_items, CHAINS

    chain_cfg = CHAINS["shufersal"]
    print(f"Fetching il_prices identity for shufersal (chain {chain_cfg['chain_id']})...")
    try:
        items = fetch_items(chain_id=chain_cfg["chain_id"], kind=chain_cfg["kind"])
    except Exception as e:
        print(f"il_prices fetch failed: {e}")
        return

    # Filter to category-relevant products by name keywords
    queries = CATEGORY_QUERIES.get(category, [])
    relevant = []
    for item in items:
        name_lower = (item.name or "").lower()
        if any(q.lower() in name_lower for q in queries):
            relevant.append(item)

    if not relevant:
        print(f"No il_prices items matched category '{category}' queries: {queries}")
        return

    barcodes = list({item.barcode for item in relevant if item.barcode})[:limit]
    print(f"Found {len(relevant)} matching items, scraping {len(barcodes)} unique barcodes")

    scraper = ShufersalScraper(barcodes=barcodes, category=category)
    results = scraper.run()

    sufficient = [r for r in results if r["sufficient"]]
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = build_output_path(category, run_id)

    output = {
        "category": category,
        "retailer": "shufersal",
        "run_id": run_id,
        "total_scraped": len(results),
        "sufficient_count": len(sufficient),
        "products": results,
        "meta": {
            "scraper": "01_acquire_shufersal.py",
            "unlock_method": "requests_bs4_direct_barcode_url (TASK-582 fix)",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOutput: {out_path}")
    print(f"Results: {len(results)} scraped, {len(sufficient)} sufficient ({len(sufficient)/max(1,len(results))*100:.0f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="juices", choices=list(CATEGORY_QUERIES.keys()))
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    main(args.category, args.limit)
