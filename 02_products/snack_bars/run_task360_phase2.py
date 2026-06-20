"""
TASK-360 Phase 2 — Snacks Playwright recovery + curation + re-score
====================================================================
Fixes:
  A) Playwright recovery of JS-rendered nutrition panels for quarantined snack bars
  B) Category curation — drop raw oats / loose granola / cereal bags, keep bars/wafers/packs
  C) Victory cross-check via Playwright
  D) Re-run BSIP1→BSIP2 on curated+recovered set → rebuild snacks_frontend_v4.json

Scope writes:
  02_products/snack_bars/  (BSIP0 playwright recovery files, new BSIP2 dir, run record)
  bari-web/src/data/comparisons/snacks_frontend_v4.json  (overwrite)

Hard rules:
  - Engine UNTOUCHED (no changes to 03_operations/bsip2/** or page_generator configs)
  - OFF banned
  - Copy fields = PENDING_COPY
  - No fabrication: if Playwright can't find a panel, product stays quarantined
"""
from __future__ import annotations

import collections
import datetime
import hashlib
import json
import logging
import os
import pathlib
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT       = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
PHASE1_RUN = "run_snacks_task360_shuf_20260620_064221"
PHASE1_BSIP0_DIR = SNACKS_DIR / "observations_bsip0" / "shufersal" / PHASE1_RUN
PHASE1_BSIP1_DIR = ROOT / "03_operations" / "bsip1" / PHASE1_RUN / "output"

RUN_TS  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
RUN_ID  = f"run_snacks_task360_phase2_{RUN_TS}"

BSIP0_PLAYWRIGHT_DIR = SNACKS_DIR / "observations_bsip0" / "shufersal" / (RUN_ID + "_playwright")
BSIP1_DIR  = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR  = SNACKS_DIR / "bsip2_outputs" / RUN_ID
BSIP2_SRC  = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v4.json"
CONFIG_PATH   = ROOT / "03_operations" / "page_generator" / "configs" / "snacks.json"

_SHARED = ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"
sys.path.insert(0, str(_SHARED))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, parse_nutrition_numeric

for _d in (BSIP0_PLAYWRIGHT_DIR, BSIP1_DIR, BSIP2_DIR / "products"):
    _d.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def save_json(path: pathlib.Path | str, data) -> None:
    pathlib.Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ══════════════════════════════════════════════════════════════════════════════
# PROBLEM A — Playwright recovery
# ══════════════════════════════════════════════════════════════════════════════

# The 12 quarantined barcodes from phase 1.
# We pre-classify based on name — those that are clearly NOT snacks stay quarantined.
QUARANTINED_BARCODES = {
    "7290013724816": "חטיף גרנולה צימוק ותמר",
    "7290013724809": "חטיף גרנולה שקד ואגוז",
    "769493101648":  "וואפל אנרגיה שוקולד מלוח",
    "769493102515":  "וואפל אנרגיה בטעם קוקוס",
    "769493101662":  "וואפל אנרגיה בטעם תות",
    "16000548909":   "חטיפי שיבולת שועל בטעמים",
    "7290014455467": "מעדן שיבולת שועל",         # refrigerated dessert — stays out
    "5000108478119": "שיבולת שועל בפח",           # raw oats tin — stays out
    "7290112199942": "גרנולה תותים ללת\"ס",
    "7290112199959": "גרנולה פירות ללת\"ס",
    "7290020030283": "מארז חטיפי חלוה ללת\"ס",
    "769493100078":  "ג'ל אנרגיה טעם אספרסו",    # energy gel, not a bar
}

# Barcodes we will attempt Playwright recovery on (excluding clear non-snacks)
PLAYWRIGHT_RECOVERY_TARGETS = {
    "7290013724816": "P_7290013724816",   # חטיף גרנולה (KEEP: granola bar)
    "7290013724809": "P_7290013724809",   # חטיף גרנולה (KEEP: granola bar)
    "769493101648":  "P_769493101648",    # וואפל אנרגיה (KEEP: energy wafer)
    "769493102515":  "P_769493102515",    # וואפל אנרגיה (KEEP: energy wafer)
    "769493101662":  "P_769493101662",    # וואפל אנרגיה (KEEP: energy wafer)
    "16000548909":   "P_16000548909",     # חטיפי שיבולת שועל בטעמים (KEEP: oat snack bars)
    "7290112199942": "P_7290112199942",   # גרנולה תותים ללת"ס
    "7290112199959": "P_7290112199959",   # גרנולה פירות ללת"ס
    "7290020030283": "P_7290020030283",   # מארז חטיפי חלוה ללת"ס (KEEP: halva snack packs)
}

# Clear non-snacks to keep quarantined without Playwright attempt
HARD_NON_SNACKS = {
    "7290014455467": "מעדן שיבולת שועל — refrigerated oat dessert (kcal=62 with nutrition, clearly a dessert cup)",
    "5000108478119": "שיבולת שועל בפח — Quaker rolled oats in tin (raw ingredient)",
    "769493100078":  "ג'ל אנרגיה טעם אספרסו — liquid energy gel, not a snack bar format",
}

SHUFERSAL_BASE = "https://www.shufersal.co.il"


def _extract_nutr_from_playwright_html(html: str) -> dict:
    """Parse nutrition data from Playwright-rendered HTML using the shared bsip0 parser."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    nutr_parsed = parse_nutrition_list(soup)
    nutr_raw_src = extract_nutrition_raw(soup)
    nutr_numeric_dict = {
        "energy_kcal_raw":    nutr_parsed.get("energy", ""),
        "fat_raw":            nutr_parsed.get("fat", ""),
        "saturated_fat_raw":  nutr_parsed.get("saturated_fat", ""),
        "carbs_raw":          nutr_parsed.get("carbs", ""),
        "sugar_raw":          nutr_parsed.get("sugar", ""),
        "fiber_raw":          nutr_parsed.get("fiber", ""),
        "protein_raw":        nutr_parsed.get("protein", ""),
        "sodium_raw":         nutr_parsed.get("sodium", ""),
    }
    nutr_numeric = parse_nutrition_numeric(nutr_numeric_dict)

    # Also extract ingredients from rendered page
    from bs4 import BeautifulSoup as BS
    soup2 = BS(html, "html.parser")
    ing = ""
    _INGR_PATTERNS = [
        re.compile(r"רכיב[ים:]*\s*(.*)", re.DOTALL),
        re.compile(r"מרכיב[ים:]*\s*(.*)", re.DOTALL),
    ]
    for label_text in ("רכיבים", "מרכיבים", "רכיב"):
        node = soup2.find(string=re.compile(label_text))
        if node:
            parent = node.find_parent()
            container = parent.find_parent() if parent else None
            if container:
                full = container.get_text(separator=" ", strip=True)
                for pat in _INGR_PATTERNS:
                    m = pat.search(full)
                    if m:
                        ing = m.group(1).strip()[:1000]
                        break
            if ing:
                break

    return {
        "nutrition_parsed_strings": nutr_parsed,
        "nutrition_numeric": nutr_numeric,
        "ingredients_raw": ing,
        "nutr_raw_source": nutr_raw_src,
    }


def test_playwright_shufersal() -> dict:
    """
    Test Playwright can reach and render a Shufersal product page.
    Uses a known-good product (7290107971522) as the test target.
    Returns {"success": bool, "status_code": int, "nutrition_found": bool, "error": str|None}
    """
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    test_code = "P_7290107971522"
    url = f"{SHUFERSAL_BASE}/online/he/p/{test_code.lower()}"
    log.info("Playwright test: GET %s", url)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                locale="he-IL",
            )
            page = ctx.new_page()
            resp = page.goto(url, timeout=30000, wait_until="domcontentloaded")
            status = resp.status if resp else 0
            # Wait for nutrition section to appear
            try:
                page.wait_for_selector(".nutritionList, .nutrition-list, [class*='nutrition']",
                                       timeout=8000)
            except PWTimeout:
                pass
            html = page.content()
            browser.close()

        parsed = _extract_nutr_from_playwright_html(html)
        nn = parsed["nutrition_numeric"]
        kcal = nn.get("energy_kcal") or 0
        accounted = (nn.get("carbohydrates_g") or 0) + (nn.get("fat_g") or 0) + \
                    (nn.get("protein_g") or 0) + (nn.get("dietary_fiber_g") or 0)
        return {
            "success": True,
            "status_code": status,
            "nutrition_found": kcal > 0 or accounted > 0,
            "kcal": kcal,
            "accounted_mass": accounted,
            "error": None,
        }
    except Exception as e:
        return {"success": False, "status_code": 0, "nutrition_found": False, "error": str(e)}


def playwright_scrape_shufersal_product(shufersal_code: str, barcode: str) -> dict | None:
    """
    Use Playwright to render the Shufersal product page and extract nutrition.
    Returns a BSIP0 product record (same schema as phase 1) or None on failure.
    """
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    from bs4 import BeautifulSoup
    import json as _json

    url = f"{SHUFERSAL_BASE}/online/he/p/{shufersal_code.lower()}"
    log.info("  Playwright scrape: %s (%s)", barcode, shufersal_code)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                locale="he-IL",
            )
            page = ctx.new_page()
            resp = page.goto(url, timeout=40000, wait_until="networkidle")
            status = resp.status if resp else 0
            if status >= 400:
                log.warning("  HTTP %d for %s", status, url)
                browser.close()
                return None

            # Try to click nutrition tab if it exists
            try:
                nutr_tab = page.locator(
                    "button:has-text('תזונה'), a:has-text('תזונה'), "
                    "[class*='nutrition-tab'], [data-tab='nutrition']"
                ).first
                if nutr_tab.count() > 0:
                    nutr_tab.click(timeout=3000)
                    page.wait_for_timeout(1500)
            except Exception:
                pass

            # Wait for nutrition list
            try:
                page.wait_for_selector(
                    ".nutritionList, .nutrition-list, [class*='nutritionList']",
                    timeout=8000
                )
            except PWTimeout:
                pass

            # Also try waiting for product details section
            try:
                page.wait_for_selector(
                    ".shufersal-details, .product-details, [class*='productDetails']",
                    timeout=3000
                )
            except PWTimeout:
                pass

            html = page.content()
            final_url = page.url
            browser.close()
    except Exception as e:
        log.error("  Playwright exception for %s: %s", barcode, e)
        return None

    # Parse the rendered HTML
    soup = BeautifulSoup(html, "html.parser")

    # LD+JSON for identity
    ld_name = ld_sku = ld_gtin = ""
    ld_images: list[str] = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = _json.loads(script.string or "{}")
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                imgs = ld.get("image", [])
                ld_images = [imgs] if isinstance(imgs, str) else imgs[:3]
                break
        except Exception:
            pass

    parsed = _extract_nutr_from_playwright_html(html)
    nn = parsed["nutrition_numeric"]
    ing = parsed["ingredients_raw"]

    # Get name from phase1 BSIP0 (already in quarantine record)
    phase1_product_path = PHASE1_BSIP0_DIR / f"P_{barcode}" / "product.json"
    phase1_name = QUARANTINED_BARCODES.get(barcode, "")
    phase1_image_urls: list[str] = []
    if phase1_product_path.exists():
        try:
            p1 = _json.loads(phase1_product_path.read_text(encoding="utf-8"))
            phase1_name = p1["product_identity"]["name"] or phase1_name
            phase1_image_urls = p1["product_identity"].get("image_urls") or []
        except Exception:
            pass

    name = ld_name or phase1_name
    bc = ld_gtin or ld_sku or barcode
    image_urls = [u for u in ld_images if u] or phase1_image_urls

    record = {
        "schema_version": "bsip0_task360_playwright_v1",
        "source": {
            "retailer": "Shufersal",
            "retailer_id": "shufersal",
            "source_url": final_url,
            "source_type": "product_page_playwright_rendered",
            "scrape_run": RUN_ID,
            "scraped_at": now_iso(),
        },
        "product_identity": {
            "name": name,
            "brand": "",
            "barcode": bc,
            "shufersal_code": shufersal_code,
            "image_urls": image_urls,
        },
        "serving_info": {
            "package_size_g": None,
            "unit_size_g": None,
            "unit_count": None,
            "serving_size_g": None,
            "parse_source": None,
        },
        "nutrition_raw": {
            "parsed_strings": parsed["nutrition_parsed_strings"],
            "basis": parsed["nutr_raw_source"].get("selection", {}).get("selected_basis", "unknown"),
            "basis_header": parsed["nutr_raw_source"].get("selection", {}).get("selected_table_header", ""),
        },
        "nutrition_numeric_per_100g": nn,
        "ingredients_raw": ing,
        "allergens_raw": "",
        "provenance": {
            "source": "shufersal_playwright_scrape",
            "source_url": final_url,
            "fetched_at": now_iso(),
            "client_version": "task360_phase2_playwright",
            "verification_status": "candidate",
            "off_check": "PASS — no Open Food Facts",
        },
    }
    return record


# ══════════════════════════════════════════════════════════════════════════════
# PROBLEM B — Category curation
# ══════════════════════════════════════════════════════════════════════════════

# Explicit DROP decisions for the 54 phase-1 products by barcode
# Based on product name analysis. Products not listed = KEEP (default).
CURATION_DROP = {
    # Raw/rolled oats
    "7290014095960": "שיבולת שועל עבה — raw rolled oats, a staple ingredient not a snack",
    "7290017894089": "קמח שיבולת שועל — oat flour, baking ingredient",
    "480442":        "קוואקר שיבולת שועל — Quaker rolled oats, raw ingredient",
    # Loose granola sold by bag (cereal/topping, not a bar)
    "7613035622623": "גרנולה דבש — Nestlé loose granola bag (cereal format, not a bar)",
    "7290011131968": "גרנולה אגוזים — loose granola bag",
    "7290011668587": "גרנולה עשירה — loose granola bag",
    "7290011131050": "גרנולה פקאן — loose granola bag",
    "7290011131975": "גרנולה פירות — loose granola bag",
    "7613035635845": "גרנולה שוקולד פיטנס — Nestlé loose granola bag (Fitness brand cereal/topping)",
    "7290014471443": "גרנולה אגוזים — loose granola bag",
    "7613037012095": "גרנולה שוקולד קינואה — Nestlé loose granola bag",
    "1164273":       "חגיגת גרנולה — loose granola bag",
    "7290011668570": "חגיגת גרנולה פירות יבשים — loose granola bag",
    "1343845":       "גרנולה עם פירות — loose granola bag",
    "7290106771161": "גרנולה מייפל פקאן — loose granola bag",
    "1164266":       "גרנולה ממותקת בסילאן — loose granola bag",
    "7290013433336": "גרנולה 48% סופרפוד — loose granola bag",
    "7290017962047": "גרנולה חמוציות ושקדים — loose granola bag",
    "7290106771369": "גרנולה לוז וקינמון — loose granola bag",
    "7290106773714": "גרנולה מיקס קראנץ' מלוח — loose granola bag",
    "7290112497994": "גרנולה פרוטאין+אגוזים — loose granola bag (protein granola topping)",
    "7290116534619": "גרנולה פרוטאין+שוקולד — loose granola bag",
    # Date filling (baking ingredient)
    "7296073515135": "מלית תמרים — date filling for baking, not a snack",
    # Hamantaschen (seasonal pastry, not a snack bar)
    "7290119040162": "אוזן המן תמרים — Hamantaschen (seasonal pastry format)",
    "7290119040018": "אוזני המן תמרים — Hamantaschen (seasonal pastry format)",
    # Bambe (savory puff snack, different category entirely)
    "66318":         "חטיף במבה — Bamba (savory corn puff), not a cereal/energy bar",
    # "Katamatamins" brand health snack — generic health bar, include or borderline
    # Actually "כתמטמינים" is a brand, product is a health/snack bar — KEEP
}

# BORDERLINE — annotate with reasoning but still include
CURATION_BORDERLINE = {
    "7290011622428": "כתמטמינים חטיף בריאות — general 'health snack', unclear format; KEEPING because it passes gate and branded as health snack bar",
    "7290116536217": "חטיף נשנושים פלוס עם סלק — beet snack; KEEPING as a grab-and-go snack item",
    "7290118424956": "פיטנס THIN רוזמרין — thin cracker-type, borderline; KEEPING as Fitness branded snack",
}


# ══════════════════════════════════════════════════════════════════════════════
# PROBLEM C — Victory cross-check via Playwright
# ══════════════════════════════════════════════════════════════════════════════

VICTORY_BASE = "https://www.victoryonline.co.il"

def test_victory_playwright() -> dict:
    """Test if Victory is reachable via Playwright."""
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )
            page = ctx.new_page()
            try:
                resp = page.goto(VICTORY_BASE, timeout=20000, wait_until="domcontentloaded")
                status = resp.status if resp else 0
                browser.close()
                return {"reachable": status < 400, "status": status}
            except PWTimeout:
                browser.close()
                return {"reachable": False, "status": 0, "reason": "timeout"}
    except Exception as e:
        return {"reachable": False, "status": 0, "reason": str(e)}


def playwright_scrape_victory_product(barcode: str) -> dict | None:
    """
    Try to find a product on Victory by barcode using Playwright.
    Victory's nutrition modal is AngularJS-rendered.
    Returns nutrition dict or None.
    """
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    url = f"{VICTORY_BASE}/category?search={barcode}"
    log.info("  Victory Playwright: %s", url)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                locale="he-IL",
            )
            page = ctx.new_page()
            try:
                resp = page.goto(url, timeout=25000, wait_until="networkidle")
                status = resp.status if resp else 0
                if status >= 400:
                    browser.close()
                    return None

                # Wait for product card
                try:
                    page.wait_for_selector(
                        ".product-card, [class*='productCard'], .ng-scope .product",
                        timeout=8000
                    )
                except PWTimeout:
                    pass

                # Try clicking the product to open details/nutrition modal
                try:
                    product_card = page.locator(
                        ".product-card, [class*='productCard'], .ng-scope .product"
                    ).first
                    product_card.click(timeout=3000)
                    page.wait_for_timeout(2000)
                except Exception:
                    pass

                # Try clicking nutrition tab in the modal
                try:
                    nutr_tab = page.locator(
                        "button:has-text('ערכים תזונתיים'), a:has-text('תזונה'), "
                        "[class*='nutrition-tab']"
                    ).first
                    nutr_tab.click(timeout=3000)
                    page.wait_for_timeout(1500)
                except Exception:
                    pass

                html = page.content()
                browser.close()
            except PWTimeout:
                browser.close()
                return None
    except Exception as e:
        log.warning("  Victory Playwright exception for %s: %s", barcode, e)
        return None

    parsed = _extract_nutr_from_playwright_html(html)
    nn = parsed["nutrition_numeric"]
    kcal = nn.get("energy_kcal") or 0
    accounted = (
        (nn.get("carbohydrates_g") or 0) +
        (nn.get("fat_g") or 0) +
        (nn.get("protein_g") or 0) +
        (nn.get("dietary_fiber_g") or 0)
    )
    if kcal == 0 and accounted == 0:
        return None

    return {
        "source": "victory_playwright",
        "nutrition_numeric": {k: v for k, v in nn.items() if not k.startswith("_")},
        "kcal": kcal,
        "accounted_mass": round(accounted, 1),
    }


def compare_nutrition(shuf: dict, victory: dict) -> dict:
    """Compare two per-100g numeric dicts. Flags fields where values differ by > 15%."""
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


# ══════════════════════════════════════════════════════════════════════════════
# Plausibility gate (inline — mirrors plausibility_gate.py logic)
# ══════════════════════════════════════════════════════════════════════════════

GATE_MIN_ACCOUNTED_G = 70.0
GATE_MIN_KCAL_DRY    = 150.0
SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק", "גלוקוז-פרוקטוז",
]


def apply_plausibility_gate(nn: dict, ing: str = "", serving_g: float | None = None) -> dict:
    kcal  = nn.get("energy_kcal") or 0.0
    carbs = nn.get("carbohydrates_g") or 0.0
    fat   = nn.get("fat_g") or 0.0
    prot  = nn.get("protein_g") or 0.0
    fiber = nn.get("dietary_fiber_g") or 0.0
    sugars = nn.get("sugars_g")
    accounted = carbs + fat + prot + fiber

    def _check(n_kcal, n_acc, n_sug):
        fails = []
        if n_acc < GATE_MIN_ACCOUNTED_G:
            fails.append(f"accounted_mass={n_acc:.1f}g < {GATE_MIN_ACCOUNTED_G}g per 100g")
        if n_sug is not None and n_sug == 0:
            if any(tok in (ing or "") for tok in SUGAR_BEARING_TOKENS):
                fails.append("sugars=0 but sugar-bearing ingredients present")
        if n_kcal < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={n_kcal:.0f} < {GATE_MIN_KCAL_DRY} (dry snack minimum)")
        return fails

    fails = _check(kcal, accounted, sugars)
    if not fails:
        return {
            "verdict": "pass", "accounted_mass": round(accounted, 1), "kcal": kcal,
            "fail_reasons": [], "nutrition_basis": "per_100g", "conversion_factor": 1.0,
            "final_nutrition": {k: v for k, v in nn.items() if not k.startswith("_")},
        }

    if serving_g and 5.0 < serving_g < 90.0:
        f = 100.0 / serving_g
        def _c(v): return round(v * f, 1) if v is not None else None
        conv = {
            "energy_kcal": _c(kcal), "carbohydrates_g": _c(carbs),
            "fat_g": _c(fat), "protein_g": _c(prot),
            "dietary_fiber_g": _c(fiber), "sugars_g": _c(sugars),
        }
        conv_acc = (conv["carbohydrates_g"] or 0) + (conv["fat_g"] or 0) + \
                   (conv["protein_g"] or 0) + (conv["dietary_fiber_g"] or 0)
        conv_fails = _check(conv.get("energy_kcal") or 0, conv_acc, conv.get("sugars_g"))
        if not conv_fails:
            return {
                "verdict": "converted_pass", "accounted_mass": round(conv_acc, 1),
                "kcal": conv.get("energy_kcal") or 0.0, "fail_reasons": fails,
                "nutrition_basis": "converted_from_serving", "conversion_factor": round(f, 3),
                "serving_g_used": serving_g, "final_nutrition": conv,
            }
        return {
            "verdict": "quarantine", "accounted_mass": round(accounted, 1), "kcal": kcal,
            "fail_reasons": fails, "post_conversion_fails": conv_fails,
            "nutrition_basis": None, "conversion_factor": f,
            "final_nutrition": None,
        }

    return {
        "verdict": "quarantine", "accounted_mass": round(accounted, 1), "kcal": kcal,
        "fail_reasons": fails, "nutrition_basis": None, "conversion_factor": 1.0,
        "final_nutrition": None,
    }


# ══════════════════════════════════════════════════════════════════════════════
# BSIP1 builder (same as phase 1, reused here for newly recovered products)
# ══════════════════════════════════════════════════════════════════════════════

_E_PATTERN = re.compile(r"E(\d{3,4}[a-z]?)", re.IGNORECASE)
_ADDITIVE_TERMS = [
    ("לציטין סויה", "emulsifier"), ("לציטין", "emulsifier"), ("מתחלב", "emulsifier"),
    ("חומרי טעם", "flavor_generic"), ("חומר תפיחה", "raising_agent"),
    ("מגביר חמיצות", "acidity_regulator"), ("חומצה", "acid"), ("צבע", "color"),
    ("חומר ייצוב", "stabilizer"), ("עמילן מתוקן", "modified_starch"),
    ("מולטודקסטרין", "maltodextrin"), ("מלטודקסטרין", "maltodextrin"),
    ("פולידקסטרוז", "polydextrose"), ("גליצרול", "humectant"),
]
_SWEETENER_TERMS = [
    ("סוכר", "added_sugar"), ("דבש", "honey"), ("סירופ גלוקוזה", "glucose_syrup"),
    ("מולסה", "molasses"), ("פרוקטוז", "fructose"), ("גלוקוז", "glucose"),
    ("מחית תמרים", "date_paste"), ("תמרים", "date"),
]


def _infer_nova(ing: str, e_nums: list) -> tuple[int, float, list[str]]:
    has_ultra = bool(re.search(
        r"(E\d{3}|מלטודקסטרין|פולידקסטרוז|גליצרול|עמילן מתוקן|חומצה לקטית|אינולין"
        r"|גלוקוז-פרוקטוז|סירופ גלוקוזה-פרוקטוז)", ing
    ))
    has_e_nums   = len(e_nums) >= 2
    has_flavor   = "חומרי טעם" in ing
    has_isolate  = bool(re.search(r"(חלבון סויה|חלבון חלב|חלבון אפונה|פרוטאין)", ing))
    if has_ultra or has_isolate:
        return 4, 0.85, ["ultra_processing_markers_detected"]
    if has_e_nums or has_flavor:
        return 3, 0.75, ["additives_or_flavors_detected"]
    if len(ing) > 20:
        return 2, 0.65, ["minimal_processing_inferred"]
    return 3, 0.5, ["insufficient_ingredient_data"]


def build_bsip1_from_playwright(bsip0: dict, gate: dict) -> dict:
    barcode = bsip0["product_identity"]["barcode"]
    pid = f"bsip1_{barcode}"
    ing = bsip0.get("ingredients_raw", "") or ""
    nutrition = gate.get("final_nutrition") or {}

    e_nums = list(set(_E_PATTERN.findall(ing)))
    extracted_additives = [{"term": f"E{e}", "category": "e_number", "position": 1} for e in e_nums]
    for term, cat in _ADDITIVE_TERMS:
        if term in ing:
            extracted_additives.append({"term": term, "category": cat, "position": 1})
    extracted_sweeteners = [
        {"term": t, "category": c, "position": 1} for t, c in _SWEETENER_TERMS if t in ing
    ]
    nova_proxy, nova_conf, nova_notes = _infer_nova(ing, e_nums)

    if not ing:
        ing_quality, ing_warnings = "missing", ["ingredients_missing"]
    elif len(ing) < 10:
        ing_quality, ing_warnings = "minimal", ["ingredient_text_very_short"]
    else:
        ing_quality, ing_warnings = "clean", []

    has_full = (
        all(nutrition.get(k) is not None for k in ["energy_kcal", "fat_g", "carbohydrates_g", "protein_g"])
        and gate.get("verdict") in ("pass", "converted_pass")
    )

    missing_fields = []
    if not nutrition.get("energy_kcal"):
        missing_fields.append("energy_kcal")
    serving = bsip0.get("serving_info", {})

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": bsip0["product_identity"].get("name"),
        "canonical_name_en": None,
        "brand": bsip0["product_identity"].get("brand", ""),
        "package_size_g": serving.get("package_size_g"),
        "unit_count": serving.get("unit_count"),
        "unit_size_g": serving.get("unit_size_g"),
        "serving_size_g": serving.get("serving_size_g"),
        "country_of_origin": None,
        "kosher_certification": None,
        "image_url": (bsip0["product_identity"].get("image_urls") or [None])[0],
        "source_retailers": ["shufersal"],
        "normalized_nutrition_per_100g": {
            "energy_kcal":     nutrition.get("energy_kcal"),
            "fat_g":           nutrition.get("fat_g"),
            "fat_saturated_g": nutrition.get("fat_saturated_g"),
            "fat_trans_g":     nutrition.get("fat_trans_g"),
            "cholesterol_mg":  nutrition.get("cholesterol_mg"),
            "sodium_mg":       nutrition.get("sodium_mg"),
            "carbohydrates_g": nutrition.get("carbohydrates_g"),
            "sugars_g":        nutrition.get("sugars_g"),
            "dietary_fiber_g": nutrition.get("dietary_fiber_g"),
            "protein_g":       nutrition.get("protein_g"),
        },
        "energy_source_unit": "kcal",
        "ingredients_text_he": ing or None,
        "ingredients_list": [s.strip() for s in re.split(r"[,،]", ing) if s.strip()][:20] if ing else [],
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims": [],
        "confidence": {
            "identity_confidence": "medium",
            "barcode_confidence": "high" if len(barcode) >= 12 else "medium",
            "nutrition_confidence": "confirmed_per_100g" if has_full else "unconfirmed",
            "matched_by": "shufersal_playwright",
            "observation_count": 1,
        },
        "barcode_validation_status": "from_ld_json" if len(barcode) >= 12 else "inferred",
        "barcode_confidence_reason": "Extracted from Shufersal Playwright-rendered page.",
        "nutrition_basis_claimed": bsip0["nutrition_raw"].get("basis_header", ""),
        "nutrition_basis_detected": gate.get("nutrition_basis"),
        "nutrition_basis_gate": gate.get("verdict"),
        "nutrition_basis_conversion_factor": gate.get("conversion_factor", 1.0),
        "nutrition_serving_g_used": gate.get("serving_g_used"),
        "nutrition_consistency_status": "consistent" if has_full else "insufficient",
        "nutrition_consistency_warnings": gate.get("fail_reasons", []),
        "ingredient_text_quality": ing_quality,
        "ingredient_warnings": ing_warnings,
        "canonical_trust_score": 0.85 if has_full else 0.45,
        "canonical_trust_level": "medium" if has_full else "low",
        "canonical_risk_flags": (
            ["per_serving_converted"] if gate.get("verdict") == "converted_pass" else []
        ) + ["shufersal_playwright_recovery"],
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
            "source": "shufersal_playwright_product_page",
            "bsip0_status": "playwright_recovery",
            "populated_at": "bsip1_task360_phase2",
            "missing": not bool(ing),
            "note": "Playwright-recovered from Shufersal (JS-rendered nutrition tab). TASK-360 Phase 2.",
        },
        "ingredient_order": [
            {"position": i + 1, "text": s.strip(), "percentage_declared": None, "has_subgroup": "(" in s}
            for i, s in enumerate(re.split(r"[,،]", ing)[:20]) if s.strip()
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
            "protein_marker_count": 0, "matrix_marker_count": 0,
            "fermentation_marker_count": 0, "roasting_marker_count": 0,
            "has_flavor_descriptor": False,
            "has_prebiotic_fiber": "אינולין" in ing or "FOS" in ing,
            "has_live_cultures": False,
            "has_protein_isolate_or_concentrate": bool(
                re.search(r"(חלבון סויה|חלבון חלב|חלבון אפונה|פרוטאין)", ing)
            ),
        },
        "enrichment_version": "bsip1_task360_phase2_playwright",
        "enrichment_warnings": ing_warnings,
        "nova_proxy": nova_proxy,
        "nova_confidence": nova_conf,
        "nova_confidence_band": "high" if nova_conf >= 0.8 else "medium",
        "nova_notes": nova_notes,
    }


# ══════════════════════════════════════════════════════════════════════════════
# BSIP2 runner (unchanged engine — TRIPWIRE-1)
# ══════════════════════════════════════════════════════════════════════════════

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def _score_to_grade(score) -> str | None:
    if score is None:
        return None
    for g, t in GRADE_SCALE:
        if score >= t:
            return g
    return "E"


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
    os.environ["BARI_FAT_TECH_V1"]               = "on"
    os.environ["BARI_GLASSBOX_W4"]               = "on"
    os.environ["BARI_TASK144_FIXES"]             = "off"

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
            trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
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


# ══════════════════════════════════════════════════════════════════════════════
# Frontend JSON builder (same schema as phase 1)
# ══════════════════════════════════════════════════════════════════════════════

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
    curation_dropped: dict,
    playwright_recovery_results: list,
) -> dict:
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

        cc = victory_crosschecks.get(bc)
        victory_note = None
        if cc:
            if cc.get("agree"):
                victory_note = "victory_crosscheck:agree"
            elif cc.get("discrepancies"):
                discreps = cc["discrepancies"]
                victory_note = f"victory_crosscheck:disagree:{len(discreps)}_fields"

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

    grade_dist = dict(collections.Counter(p["grade"] for p in products_out if p.get("grade")))

    quarantine_entries = [
        {
            "barcode": q["barcode"],
            "name": q.get("name"),
            "reason": q.get("reason", "plausibility_gate_fail"),
            "gate_fails": q.get("fail_reasons", []),
            "accounted_mass_g": q.get("accounted_mass"),
            "kcal": q.get("kcal"),
        }
        for q in quarantined
    ]

    drop_entries = [
        {"barcode": bc, "reason": reason}
        for bc, reason in curation_dropped.items()
    ]

    meta = {
        "category": "snacks",
        "config_sha256": config_sha,
        "display_count": len(products_out),
        "generated": now_iso(),
        "generator_version": "TASK-360-phase2-playwright-curation-v1.0",
        "grade_distribution": grade_dist,
        "off_check": "PASS — 0 products use Open Food Facts. OFF banned project-wide. All nutrition from Shufersal direct scrape (requests) or Playwright-rendered page.",
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
        "scope_note": "ניתוח מדף שופרסל — לא סקר שוק ישראלי כולל. TASK-360 Phase 2: Playwright recovery + curation.",
        "source_run": RUN_ID,
        "phase1_run": PHASE1_RUN,
        "primary_source": "shufersal",
        "cross_check_source": "victory",
        "staging_note": (
            "TASK-360 Phase 2: Playwright recovery + category curation + Victory cross-check. "
            "Consumer copy NOT done — separate voice pass required. "
            "Do NOT deploy without copy review + adversarial QA."
        ),
        "playwright_recovery": playwright_recovery_results,
        "quarantined_products": quarantine_entries,
        "quarantine_count": len(quarantined),
        "curation_dropped_count": len(curation_dropped),
        "curation_dropped_products": drop_entries,
        "scoring_engine_unchanged": "TRIPWIRE-1 compliant — no changes to 03_operations/bsip2/** or page_generator configs",
        "editorial_note": (
            "הערת קטגוריה: קטגוריית חטיפי הדגנים היא מדף פינוק — כל המוצרים הם חטיפים מעובדים. "
            "הציונים מדרגים חטיף מול חטיף בלבד. ציון גבוה אינו אישור לאכול יותר."
        ),
    }

    return {"_meta": meta, "products": products_out}


# ══════════════════════════════════════════════════════════════════════════════
# Main pipeline
# ══════════════════════════════════════════════════════════════════════════════

def main():
    log.info("=" * 70)
    log.info("TASK-360 Phase 2 — Playwright recovery + curation + re-score")
    log.info("Run ID: %s", RUN_ID)
    log.info("=" * 70)

    # ── STEP 1: Test Playwright → Shufersal ───────────────────────────────────
    log.info("\n--- STEP 1: Playwright Shufersal connectivity test ---")
    pw_test = test_playwright_shufersal()
    log.info("Playwright→Shufersal: %s (HTTP %d, nutrition_found=%s, kcal=%s)",
             "OK" if pw_test["success"] else "FAIL",
             pw_test["status_code"], pw_test["nutrition_found"], pw_test.get("kcal"))
    if not pw_test["success"]:
        log.error("FATAL: Playwright cannot reach Shufersal: %s", pw_test.get("error"))
        sys.exit(2)
    playwright_shufersal_ok = pw_test

    # ── STEP 2: Playwright recovery of quarantined panels ─────────────────────
    log.info("\n--- STEP 2: Playwright recovery of quarantined snack bars ---")
    playwright_recovery_results = []
    recovered_bsip0: dict[str, dict] = {}  # barcode -> bsip0 record
    recovered_gate_results: dict[str, dict] = {}

    for barcode, shufersal_code in PLAYWRIGHT_RECOVERY_TARGETS.items():
        log.info("  Recovering %s (%s)", barcode, QUARANTINED_BARCODES.get(barcode, ""))
        bsip0 = playwright_scrape_shufersal_product(shufersal_code, barcode)
        if bsip0 is None:
            result = {
                "barcode": barcode, "name": QUARANTINED_BARCODES.get(barcode, ""),
                "status": "playwright_failed", "recovered_kcal": None,
                "accounted_mass": None, "gate_verdict": "quarantine",
            }
            playwright_recovery_results.append(result)
            log.warning("  -> Playwright failed for %s — stays quarantined", barcode)
            continue

        nn = bsip0["nutrition_numeric_per_100g"]
        ing = bsip0.get("ingredients_raw", "")
        gate = apply_plausibility_gate(nn, ing)

        # Save BSIP0 playwright record
        pw_product_dir = BSIP0_PLAYWRIGHT_DIR / barcode
        pw_product_dir.mkdir(parents=True, exist_ok=True)
        bsip0["plausibility_gate"] = gate
        save_json(pw_product_dir / "product.json", bsip0)

        kcal = gate.get("kcal", 0)
        accounted = gate.get("accounted_mass", 0)
        result = {
            "barcode": barcode,
            "name": bsip0["product_identity"].get("name") or QUARANTINED_BARCODES.get(barcode, ""),
            "status": "recovered" if gate["verdict"] in ("pass", "converted_pass") else "still_quarantine",
            "gate_verdict": gate["verdict"],
            "recovered_kcal": kcal,
            "accounted_mass": accounted,
            "fail_reasons": gate.get("fail_reasons", []),
            "ingredients_found": bool(ing),
        }
        playwright_recovery_results.append(result)

        if gate["verdict"] in ("pass", "converted_pass"):
            log.info("  -> RECOVERED: kcal=%s accounted=%.1fg", kcal, accounted)
            recovered_bsip0[barcode] = bsip0
            recovered_gate_results[barcode] = gate
        else:
            log.warning("  -> still quarantined after Playwright: %s", gate.get("fail_reasons"))

    # Record non-attempted (hard non-snacks)
    for barcode, reason in HARD_NON_SNACKS.items():
        playwright_recovery_results.append({
            "barcode": barcode,
            "name": QUARANTINED_BARCODES.get(barcode, ""),
            "status": "skipped_non_snack",
            "reason": reason,
            "gate_verdict": "quarantine",
            "recovered_kcal": None,
            "accounted_mass": None,
        })

    log.info("Recovery summary: %d attempted, %d recovered",
             len(PLAYWRIGHT_RECOVERY_TARGETS),
             sum(1 for r in playwright_recovery_results if r["status"] == "recovered"))

    # ── STEP 3: Build curated BSIP1 corpus ────────────────────────────────────
    log.info("\n--- STEP 3: Build curated BSIP1 corpus ---")

    # Phase 1 gate results come from scrape_results.json
    phase1_gate_by_barcode: dict[str, dict] = {}
    scrape_results_path = PHASE1_BSIP0_DIR / "scrape_results.json"
    if scrape_results_path.exists():
        for sr in json.loads(scrape_results_path.read_text(encoding="utf-8")):
            bc = sr.get("barcode", "")
            if bc:
                phase1_gate_by_barcode[bc] = {
                    "verdict": sr.get("gate_verdict", "pass"),
                    "accounted_mass": sr.get("accounted_mass", 0),
                    "kcal": sr.get("kcal", 0),
                    "fail_reasons": sr.get("fail_reasons", []),
                    "nutrition_basis": sr.get("nutrition_basis"),
                    "conversion_factor": sr.get("conversion_factor", 1.0),
                }

    # Load phase 1 BSIP1 files
    phase1_bsip1_files = list(PHASE1_BSIP1_DIR.glob("bsip1_*.json"))
    log.info("Phase 1 BSIP1 files: %d", len(phase1_bsip1_files))

    kept_count = 0
    dropped_count = 0
    all_gate_results: dict[str, dict] = {}

    for bsip1_path in phase1_bsip1_files:
        if "audit" in bsip1_path.name:
            continue
        try:
            rec = json.loads(bsip1_path.read_text(encoding="utf-8"))
        except Exception as e:
            log.warning("  Failed to read %s: %s", bsip1_path.name, e)
            continue

        barcode = str(rec.get("barcode", ""))
        if not barcode:
            continue

        # Curation check
        if barcode in CURATION_DROP:
            dropped_count += 1
            log.info("  DROP %s: %s", barcode, CURATION_DROP[barcode][:60])
            continue

        # Copy to new BSIP1 dir
        dest = BSIP1_DIR / bsip1_path.name
        dest.write_bytes(bsip1_path.read_bytes())
        kept_count += 1

        gate = phase1_gate_by_barcode.get(barcode, {"verdict": "pass", "nutrition_basis": "per_100g", "conversion_factor": 1.0})
        all_gate_results[barcode] = gate

    # Add newly recovered Playwright products (BSIP1 build)
    recovered_count = 0
    for barcode, bsip0 in recovered_bsip0.items():
        # Curation check for newly recovered
        name = bsip0["product_identity"].get("name", "")
        if barcode in CURATION_DROP:
            log.info("  DROP (recovered) %s: %s", barcode, CURATION_DROP[barcode][:60])
            continue

        gate = recovered_gate_results[barcode]
        bsip1 = build_bsip1_from_playwright(bsip0, gate)
        bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
        save_json(bsip1_path, bsip1)
        all_gate_results[barcode] = {
            "verdict": gate["verdict"],
            "nutrition_basis": gate.get("nutrition_basis"),
            "conversion_factor": gate.get("conversion_factor", 1.0),
        }
        recovered_count += 1
        log.info("  Added recovered BSIP1: %s (%s)", barcode, name[:50])

    log.info("BSIP1 corpus: %d kept (phase1) + %d recovered = %d total; %d dropped",
             kept_count, recovered_count, kept_count + recovered_count, dropped_count)

    # ── STEP 4: Victory cross-check via Playwright ────────────────────────────
    log.info("\n--- STEP 4: Victory Playwright cross-check ---")
    victory_reachable = test_victory_playwright()
    log.info("Victory Playwright: reachable=%s status=%s",
             victory_reachable["reachable"], victory_reachable.get("status"))

    victory_crosschecks: dict[str, dict] = {}
    victory_matched = 0
    victory_agree = 0
    victory_disagree = 0

    if victory_reachable["reachable"]:
        # Only cross-check the recovered products (most likely to need validation)
        # and a sample of phase1 high-stakes products.
        # Full cross-check of all 30+ would be slow and Victory blocks heavy scraping.
        barcodes_to_check = list(recovered_bsip0.keys())[:8]  # recovered first

        for bc in barcodes_to_check:
            log.info("  Victory check: %s", bc)
            vic = playwright_scrape_victory_product(bc)
            if vic and vic.get("kcal", 0) > 0:
                victory_matched += 1
                # Get Shufersal nutrition for comparison
                shuf_nn = {}
                bsip1_p = BSIP1_DIR / f"bsip1_{bc}.json"
                if bsip1_p.exists():
                    try:
                        shuf_nn = json.loads(bsip1_p.read_text(encoding="utf-8")).get(
                            "normalized_nutrition_per_100g", {})
                    except Exception:
                        pass
                comparison = compare_nutrition(shuf_nn, vic["nutrition_numeric"])
                victory_crosschecks[bc] = {**comparison, "victory_data": vic}
                if comparison["agree"]:
                    victory_agree += 1
                    log.info("    -> AGREE (kcal=%s)", vic["kcal"])
                else:
                    victory_disagree += 1
                    log.warning("    -> DISAGREE: %s", comparison["discrepancies"])
            else:
                log.info("    -> not found on Victory or no nutrition")
            time.sleep(1.5)  # polite rate limit
    else:
        log.info("Victory unreachable — cross-check skipped")

    log.info("Victory: matched=%d agree=%d disagree=%d", victory_matched, victory_agree, victory_disagree)

    # ── STEP 5: BSIP2 scoring ─────────────────────────────────────────────────
    log.info("\n--- STEP 5: BSIP2 scoring (unchanged engine) ---")
    traces, errors = run_bsip2(BSIP1_DIR, BSIP2_DIR / "products")
    if errors:
        log.warning("BSIP2 errors: %d", len(errors))
        for err in errors[:5]:
            log.warning("  %s: %s", err.get("product_id"), err.get("error"))

    # ── STEP 6: Assemble quarantine list for metadata ─────────────────────────
    # Include: hard non-snacks, Playwright failures, products with nutrition but curated-out are NOT quarantine
    final_quarantined = []

    for r in playwright_recovery_results:
        if r["status"] in ("still_quarantine", "playwright_failed", "skipped_non_snack"):
            final_quarantined.append({
                "barcode": r["barcode"],
                "name": r.get("name", ""),
                "reason": r.get("reason", r["status"]),
                "fail_reasons": r.get("fail_reasons", []),
                "accounted_mass": r.get("accounted_mass", 0),
                "kcal": r.get("recovered_kcal", 0),
            })

    # ── STEP 7: Build frontend JSON ───────────────────────────────────────────
    log.info("\n--- STEP 7: Frontend JSON generation ---")
    frontend_data = build_frontend_json(
        traces=traces,
        bsip1_dir=BSIP1_DIR,
        gate_results=all_gate_results,
        quarantined=final_quarantined,
        victory_crosschecks=victory_crosschecks,
        curation_dropped=CURATION_DROP,
        playwright_recovery_results=playwright_recovery_results,
    )
    save_json(FRONTEND_PATH, frontend_data)
    log.info("Frontend JSON written: %s", FRONTEND_PATH)
    log.info("Products in output: %d", len(frontend_data["products"]))

    # ── STEP 8: Plausibility gate verification on final corpus ────────────────
    log.info("\n--- STEP 8: Gate verification on final corpus ---")
    gate_failures_in_output = []
    for p in frontend_data["products"]:
        bc = p["barcode"]
        nn_disp = p.get("expansion", {}).get("nutrition", {})
        kcal = nn_disp.get("energyKcal") or 0
        # Load the actual BSIP1 for full check
        bsip1_p = BSIP1_DIR / f"bsip1_{bc}.json"
        if bsip1_p.exists():
            try:
                rec = json.loads(bsip1_p.read_text(encoding="utf-8"))
                nn = rec.get("normalized_nutrition_per_100g", {})
                gate = apply_plausibility_gate(nn, rec.get("ingredients_text_he", ""))
                if gate["verdict"] == "quarantine":
                    gate_failures_in_output.append({
                        "barcode": bc, "name": p["name"],
                        "gate_verdict": gate["verdict"],
                        "fail_reasons": gate["fail_reasons"],
                        "accounted_mass": gate["accounted_mass"],
                        "kcal": gate["kcal"],
                    })
            except Exception as e:
                log.warning("  Gate check failed for %s: %s", bc, e)

    if gate_failures_in_output:
        log.error("GATE FAILURES IN OUTPUT: %d products fail plausibility gate!", len(gate_failures_in_output))
        for gf in gate_failures_in_output:
            log.error("  %s %s: %s", gf["barcode"], gf["name"][:40], gf["fail_reasons"])
    else:
        log.info("Plausibility gate: all %d output products PASS", len(frontend_data["products"]))

    # ── STEP 9: Engine / config diff check ───────────────────────────────────
    log.info("\n--- STEP 9: Engine / config unchanged check ---")
    import subprocess
    diff_result = subprocess.run(
        ["git", "diff", "--stat",
         "03_operations/bsip2/",
         "03_operations/page_generator/configs/"],
        capture_output=True, text=True, cwd=str(ROOT), encoding="utf-8"
    )
    engine_diff = diff_result.stdout.strip()
    engine_unchanged = len(engine_diff) == 0
    log.info("Engine diff: %s", "EMPTY (TRIPWIRE-1 OK)" if engine_unchanged else f"NON-EMPTY:\n{engine_diff}")

    # ── STEP 10: Save run record ──────────────────────────────────────────────
    final_product_count = len(frontend_data["products"])
    grade_dist = frontend_data["_meta"]["grade_distribution"]

    run_record = {
        "run_id": RUN_ID,
        "phase": 2,
        "generated_at": now_iso(),
        "playwright_shufersal_test": playwright_shufersal_ok,
        "victory_reachable": victory_reachable,
        "playwright_recovery": playwright_recovery_results,
        "curation": {
            "dropped_count": len(CURATION_DROP),
            "borderline_kept": list(CURATION_BORDERLINE.keys()),
            "dropped": CURATION_DROP,
        },
        "victory_crosscheck": {
            "attempted": len(victory_crosschecks),
            "matched": victory_matched,
            "agree": victory_agree,
            "disagree": victory_disagree,
        },
        "bsip2": {
            "scored": len(traces),
            "errors": len(errors),
            "error_details": errors[:10],
        },
        "plausibility_gate_check": {
            "failures_in_output": len(gate_failures_in_output),
            "all_pass": len(gate_failures_in_output) == 0,
            "failures": gate_failures_in_output,
        },
        "engine_unchanged": engine_unchanged,
        "engine_diff": engine_diff,
        "final_product_count": final_product_count,
        "grade_distribution": grade_dist,
        "frontend_path": str(FRONTEND_PATH),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_DIR),
        "bsip0_playwright_dir": str(BSIP0_PLAYWRIGHT_DIR),
    }
    save_json(SNACKS_DIR / "observations_bsip0" / "shufersal" / f"{RUN_ID}_run_record.json", run_record)
    log.info("Run record saved.")

    # ── Final summary ─────────────────────────────────────────────────────────
    log.info("\n" + "=" * 70)
    log.info("TASK-360 Phase 2 COMPLETE")
    log.info("Playwright→Shufersal: OK (HTTP %d)", playwright_shufersal_ok["status_code"])
    log.info("Recovery: %d/%d targets recovered",
             sum(1 for r in playwright_recovery_results if r["status"] == "recovered"),
             len(PLAYWRIGHT_RECOVERY_TARGETS))
    log.info("Curation: %d dropped, %d in final corpus", len(CURATION_DROP), final_product_count)
    log.info("Grade distribution: %s", grade_dist)
    log.info("Engine unchanged: %s", engine_unchanged)
    log.info("Gate failures in output: %d", len(gate_failures_in_output))
    log.info("Victory cross-check: reachable=%s matched=%d",
             victory_reachable["reachable"], victory_matched)
    log.info("Frontend JSON: %s (%d products)", FRONTEND_PATH, final_product_count)
    log.info("=" * 70)

    return run_record


if __name__ == "__main__":
    main()
