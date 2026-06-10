"""
Shufersal BSIP0 storefront scraper — crawlee + DefaultFingerprintGenerator.

Architecture:
  1. il_prices feed (prices.shufersal.co.il) → barcodes + names + prices [identity]
  2. crawlee PlaywrightCrawler + DefaultFingerprintGenerator → product pages [nutrition]
  3. OFF → fallback for international barcodes only

The TLS fingerprint block (BLOCKED_TLS_FINGERPRINT_FAKE_200) is bypassed by
crawlee's browser fingerprint injection. Raw Playwright / Firecrawl still blocked.

Run from C:\Bari:
    python 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py --category juices --limit 40
    python 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py --category hard_cheeses --limit 40
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.fingerprint_suite import (
    DefaultFingerprintGenerator,
    HeaderGeneratorOptions,
    ScreenOptions,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SHUFERSAL_PRODUCT_URL = "https://www.shufersal.co.il/online/he/A{barcode}"

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


def extract_nutrition_from_html(html: str) -> dict:
    """Best-effort extraction of nutrition values from Shufersal product page HTML."""
    nutrition: dict = {}
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)

    # Patterns: "שומן 5.5 גרם", "אנרגיה 152 קק\"ל"
    patterns = {
        "energy_kcal": [r"אנרגיה[^\d]{0,10}([\d.]+)\s*(?:קק|kcal|kJ)", r"([\d.]+)\s*קק\"?ל"],
        "fat_g": [r"שומן[^\d]{0,10}([\d.]+)\s*ג"],
        "saturated_fat_g": [r"(?:שומן\s+)?רווי[^\d]{0,10}([\d.]+)\s*ג"],
        "carbs_g": [r"פחמימות[^\d]{0,10}([\d.]+)\s*ג"],
        "sugars_g": [r"(?:מתוכם\s+)?סוכרים[^\d]{0,10}([\d.]+)\s*ג"],
        "protein_g": [r"חלבון[^\d]{0,15}([\d.]+)\s*ג"],
        "sodium_mg": [r"נתרן[^\d]{0,10}([\d.]+)\s*מ"],
        "fiber_g": [r"(?:סיבים|סיבות)[^\d]{0,15}([\d.]+)\s*ג"],
        "calcium_mg": [r"סידן[^\d]{0,10}([\d.]+)\s*מ"],
    }
    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                try:
                    nutrition[field] = float(m.group(1))
                    break
                except ValueError:
                    pass
    return nutrition


# ---------------------------------------------------------------------------
# Crawler
# ---------------------------------------------------------------------------

class ShufersalScraper:
    def __init__(self, barcodes: list[str], category: str):
        self.barcodes = barcodes
        self.category = category
        self.results: dict[str, dict] = {}

    async def run(self) -> list[dict]:
        fp_gen = DefaultFingerprintGenerator(
            header_options=HeaderGeneratorOptions(browsers=["chrome"]),
            screen_options=ScreenOptions(min_width=1280, min_height=720),
        )
        crawler = PlaywrightCrawler(
            fingerprint_generator=fp_gen,
            headless=True,
            browser_type="chromium",
            browser_new_context_options={
                "locale": "he-IL",
                "timezone_id": "Asia/Jerusalem",
                "extra_http_headers": {"Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7"},
                "permissions": [],
            },
            navigation_timeout=timedelta(seconds=30),
            max_requests_per_crawl=len(self.barcodes),
            max_session_rotations=5,
        )

        @crawler.router.default_handler
        async def handler(context: PlaywrightCrawlingContext) -> None:
            page = context.page
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(3000)

            content = await page.content()
            url = page.url
            barcode = url.split("/A")[-1].split("?")[0] if "/A" in url else "unknown"

            # Check for block
            if any(sig in content for sig in BLOCK_SIGNALS):
                print(f"  [{barcode}] BLOCKED — fingerprint injection failed on this request")
                return

            # Extract page title / product name
            title = await page.title()
            product_name = title.split("|")[0].strip() if "|" in title else title

            # Try nutrition selectors
            nutrition_html = ""
            for sel in NUTRITION_SELECTORS:
                el = page.locator(sel).first
                try:
                    if await el.count() > 0 and await el.is_visible(timeout=500):
                        nutrition_html = await el.inner_html()
                        break
                except Exception:
                    pass

            # Try ingredient selectors
            ingredient_html = ""
            for sel in INGREDIENT_SELECTORS:
                el = page.locator(sel).first
                try:
                    if await el.count() > 0:
                        ingredient_html = await el.inner_html()
                        break
                except Exception:
                    pass

            # If no structured selectors, fall back to full page content parsing
            if not nutrition_html:
                nutrition_html = content

            nutrition = extract_nutrition_from_html(nutrition_html)
            ingredients_text = re.sub(r"<[^>]+>", " ", ingredient_html).strip() if ingredient_html else ""

            sufficient = bool(nutrition.get("energy_kcal") or nutrition.get("fat_g") or nutrition.get("protein_g"))

            record = {
                "barcode": barcode,
                "name": product_name,
                "category": self.category,
                "retailer": "shufersal",
                "source_url": url,
                "nutrition": nutrition,
                "ingredients_raw_he": ingredients_text,
                "sufficient": sufficient,
                "provenance": {
                    "panel_source": "shufersal_storefront",
                    "verification_status": "candidate",
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                },
            }
            self.results[barcode] = record
            status = "OK" if sufficient else "no_panel"
            print(f"  [{barcode}] {status} — {product_name[:50]}")

        urls = [SHUFERSAL_PRODUCT_URL.format(barcode=b) for b in self.barcodes]
        await crawler.run(urls)
        return list(self.results.values())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main(category: str, limit: int) -> None:
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
    results = await scraper.run()

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
            "unlock_method": "crawlee_1.7_DefaultFingerprintGenerator",
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
    asyncio.run(main(args.category, args.limit))
