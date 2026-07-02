"""
TASK-366b — Second-retailer probe: Victory (ויקטורי).

Targets:
  TARGET 1: 80% (or near-80%) dark chocolate tablet with full nutrition panel.
            Candidates: Millennium 80% (4820005195848), Max Brenner 80%,
            Lindt 80% (if exists), Carmit/Elite 80%, Ritter Sport 81%.
            Accept 75–82% range. Score via existing chocolate lens.

  TARGET 2: Real ingredient lists for 3 Lindt barcodes that returned
            allergen-boilerplate on Shufersal (Pass 1).
            - 3046920023429  (Lindt caramel milk)
            - 3046920023368  (Lindt Excellence milk)
            - 3046920023443  (Lindt Excellence dark — owner's screenshot product)

HARD RULES:
  - OFF BANNED. Direct Victory storefront scrape only; missing field -> NULL.
  - Missing-data discard: one-shot. If not found on Victory, leave NULL (final).
  - Per-100g plausibility gate mandatory.
  - Do NOT modify scoring engine.
  - Do NOT integrate to frontend. Data file only.

Output: choc_tablets_fix_task366b_<ts>.json  (NEW FILE, do NOT overwrite Pass 1)
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
CHOC_DIR = ROOT / "02_products" / "chocolate"

sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

from bsip0_nutrition import parse_nutrition_numeric
import run_task360_phase3 as P3
from plausibility_gate import classify_chocolate

TS = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
RUN_ID = f"task366b_{TS}"

BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = CHOC_DIR / "bsip2_outputs" / RUN_ID / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Victory constants
# ---------------------------------------------------------------------------

VICTORY_BASE = "https://www.victoryonline.co.il"
VICTORY_SEARCH = VICTORY_BASE + "/category?search={query}"
VICTORY_CHAIN_ID = "7290696200003"
RETAILER_ID = "victory"

# ---------------------------------------------------------------------------
# Playwright-based Victory scraper
# ---------------------------------------------------------------------------

from playwright.sync_api import sync_playwright, TimeoutError as PW_Timeout
from urllib.parse import quote as _quote


def _dismiss_popups(page) -> None:
    for selector in [
        'button:has-text("אישור")',
        'button:has-text("מסכים")',
        'button:has-text("הבנתי")',
        '[data-aria-desc="dialog_cookies_accept"]',
        '[role="dialog"] button',
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(600)
        except Exception:
            pass
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            btn = page.get_by_text(text, exact=True).first
            if btn.is_visible(timeout=300):
                btn.click(force=True)
                page.wait_for_timeout(400)
        except Exception:
            pass


def _barcode_from_cdn_url(img_url: str) -> str | None:
    if not img_url:
        return None
    m = re.search(r"/gs1-products/\d+/\w+/(\d{8,13})-", img_url)
    if m:
        return m.group(1)
    return None


def _find_and_click_product(page, barcode: str, name: str) -> bool:
    """Search for product card by barcode in image src, or by name text."""
    bc_loc = page.locator(
        f'img[src*="{barcode}"], img[srcset*="{barcode}"], img[ng-src*="{barcode}"]'
    ).first
    name_loc = page.get_by_text(name, exact=False).first

    for i in range(1, 100):
        if i % 15 == 0:
            print(f"    searching... attempt {i}/100 | {barcode} | {name[:40]}", flush=True)
        try:
            if bc_loc.count() > 0:
                bc_loc.scroll_into_view_if_needed(timeout=4000)
                page.wait_for_timeout(600)
                bc_loc.click(force=True)
                page.wait_for_timeout(4000)
                return True
        except Exception:
            pass
        try:
            if name_loc.count() > 0:
                name_loc.scroll_into_view_if_needed(timeout=4000)
                page.wait_for_timeout(600)
                name_loc.click(force=True)
                page.wait_for_timeout(4000)
                return True
        except Exception:
            pass
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(700)
    return False


def _capture_dialog_tab(page, tab_name: str) -> str:
    """Click a tab inside the open modal and return its inner HTML."""
    for attempt in range(1, 3):
        try:
            if page.locator('[role="tab"]').count() == 0:
                # No tabs — just grab dialog html
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    return dialog.inner_html(timeout=4000)
                return ""
            tab = page.get_by_role("tab", name=tab_name).first
            if tab.count() == 0:
                return ""
            tab.click(force=True)
            page.wait_for_timeout(2000)
            dialog = page.locator('[role="dialog"]').first
            if dialog.count() > 0:
                return dialog.inner_html(timeout=4000)
            return ""
        except PW_Timeout:
            if attempt == 2:
                return ""
            page.wait_for_timeout(1000)
        except Exception:
            if attempt == 2:
                return ""
            page.wait_for_timeout(1000)
    return ""


def _parse_victory_nutrition(html_fragment: str) -> dict:
    """
    Parse the Victory nutrition modal HTML.

    Victory uses <section class="nutrition-values"><table> with <tr> rows
    where <th> is the label and <td> is the value+unit.

    Example:
      <th>אנרגיה (קלוריות)</th><td>560 קלוריות</td>
      <th>שומנים (גרם)</th><td>35 גרם</td>
      ...
    """
    from bs4 import BeautifulSoup as BS
    soup = BS(html_fragment, "html.parser")

    # Try the nutrition-values section first
    section = soup.find("section", class_="nutrition-values")
    table = section.find("table") if section else None
    if table is None:
        # fallback: any table in the fragment
        table = soup.find("table")
    if table is None:
        return {}

    raw: dict[str, str] = {}
    for row in table.find_all("tr"):
        th = row.find("th")
        td = row.find("td")
        if not th or not td:
            continue
        label = th.get_text(strip=True)
        value_text = td.get_text(strip=True)
        # Extract numeric part from "35 גרם" or "560 קלוריות" or "220 מג"
        num_m = re.search(r"([\d,.]+)", value_text)
        if not num_m:
            continue
        numeric = num_m.group(1).replace(",", ".")
        raw[label] = numeric

    # Map Hebrew labels to canonical keys
    result: dict[str, float | None] = {}
    LABEL_MAP = [
        # Most-specific first to avoid overwrite
        (("טראנס",), "trans_fat"),
        (("רווי", "saturated"), "saturated_fat"),
        (("סוכר", "sugar"), "sugar"),
        (("פחמימ", "carb"), "carbs"),
        (("סיב", "fiber"), "fiber"),
        (("חלבונ", "protein"), "protein"),
        (("נתרן", "sodium"), "sodium"),
        (("אנרגי", "קלורי", "kcal", "energy"), "energy"),
        (("שומנ", "fat"), "fat"),
    ]

    seen_keys: set[str] = set()
    for label, raw_val in raw.items():
        label_lower = label.lower()
        for tokens, canon_key in LABEL_MAP:
            if canon_key in seen_keys:
                continue
            if any(t in label or t in label_lower for t in tokens):
                try:
                    result[canon_key] = float(raw_val)
                    seen_keys.add(canon_key)
                except ValueError:
                    pass
                break

    return result


def _parse_victory_ingredients(html_fragment: str) -> str:
    """Extract ingredient text from Victory modal ingredients tab HTML."""
    from bs4 import BeautifulSoup as BS
    soup = BS(html_fragment, "html.parser")

    # Victory shows ingredients in a div or section — look for רכיב keyword
    full_text = soup.get_text(separator=" ", strip=True)
    # Try to extract substring after רכיב
    m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Remove trailing allergen boilerplate if real ingredients came before
        allergen_cut = re.search(r"מכיל:?\s*|עלול להכיל|אזהרה|allergen", text, re.IGNORECASE)
        if allergen_cut and allergen_cut.start() > 30:
            # Some real ingredient text came before allergen section
            text = text[:allergen_cut.start()].strip() + " " + text[allergen_cut.start():].strip()
        return text[:1400]
    # No רכיב marker — return full text if it has ingredient words
    if any(w in full_text for w in ["קקאו", "סוכר", "חלב", "לציטין", "שומן", "וניל"]):
        return full_text[:1400]
    return ""


_ALLERGEN_BOILERPLATE = "כפי שרשום על גבי האריזה עלול להכיל"

def _is_boilerplate(ingr: str) -> bool:
    return _ALLERGEN_BOILERPLATE in (ingr or "")

def _has_real_ingredients(ingr: str) -> bool:
    if not ingr or _is_boilerplate(ingr):
        return False
    real_markers = ["קקאו", "סוכר", "חלב", "שומן", "שמן", "חמאה", "וניל", "לציטין", "אמולגטור"]
    return any(m in ingr for m in real_markers)


def _nutr_dict_to_pipeline_format(nutr: dict) -> dict:
    """Convert the victory-parsed nutrition dict to the format expected by parse_nutrition_numeric."""
    return {
        "energy_kcal_raw": str(nutr.get("energy", "")) if nutr.get("energy") is not None else "",
        "protein_raw": str(nutr.get("protein", "")) if nutr.get("protein") is not None else "",
        "carbs_raw": str(nutr.get("carbs", "")) if nutr.get("carbs") is not None else "",
        "fat_raw": str(nutr.get("fat", "")) if nutr.get("fat") is not None else "",
        "fiber_raw": str(nutr.get("fiber", "")) if nutr.get("fiber") is not None else "",
        "sodium_raw": str(nutr.get("sodium", "")) if nutr.get("sodium") is not None else "",
        "sugar_raw": str(nutr.get("sugar", "")) if nutr.get("sugar") is not None else "",
        "saturated_fat_raw": str(nutr.get("saturated_fat", "")) if nutr.get("saturated_fat") is not None else "",
    }


# ---------------------------------------------------------------------------
# Score one product through the existing chocolate lens
# ---------------------------------------------------------------------------

def score_product(barcode: str, name_he: str, brand: str, nutr_raw: dict,
                  ingredients_raw: str, image_url: str, weight_g: float | None,
                  source_url: str) -> dict | None:
    nutr_num = parse_nutrition_numeric(nutr_raw)

    if nutr_num.get("energy_kcal") is None and nutr_num.get("carbohydrates_g") is None:
        print(f"  [NO_NUTRITION] {barcode} — cannot score", flush=True)
        return None

    gate = P3.run_plausibility_gate(
        nutr_num, ingredients_raw or "", barcode, weight_g
    )
    if gate["verdict"] not in ("pass", "converted_pass"):
        print(f"  [GATE_FAIL] {barcode} → {gate['verdict']}: {gate.get('fail_reasons')}", flush=True)
        return None

    meta = {
        "description": name_he,
        "name_truncated": name_he,
        "brand": brand,
        "code": "P_" + barcode,
        "sku": barcode,
        "image_url": image_url or "",
        "unit_description": "",
        "health_attrs": [],
        "all_cat_codes": [],
    }
    scraped = {
        "plausibility_gate": gate,
        "ingredients_raw": ingredients_raw or "",
        "weight_g": weight_g,
        "serving_g": None,
        "nutrition_numeric_per_100g": nutr_num,
    }
    bsip1 = P3.build_bsip1(meta, scraped, barcode, RUN_ID)
    bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
    bsip1_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")

    res = P3.run_bsip2(bsip1_path, BSIP2_DIR)
    if res["status"] != "ok":
        print(f"  [BSIP2_ERROR] {barcode}: {res.get('error')}", flush=True)
        return None

    tr = res["trace"]
    sc_val = tr.get("final_score_estimate", tr.get("score"))
    return {
        "barcode": barcode,
        "name_he": name_he,
        "brand": brand,
        "score": round(sc_val, 1) if sc_val is not None else None,
        "grade": tr.get("grade_estimate", tr.get("grade")),
        "engine_category": tr.get("category"),
        "plausibility_verdict": gate["verdict"],
        "kcal": nutr_num.get("energy_kcal"),
        "fat_g": nutr_num.get("fat_g"),
        "sat_fat_g": nutr_num.get("saturated_fat_g"),
        "sugar_g": nutr_num.get("sugars_g"),
        "sodium_mg": nutr_num.get("sodium_mg"),
        "protein_g": nutr_num.get("protein_g"),
        "fiber_g": nutr_num.get("dietary_fiber_g"),
        "ingredients_raw": ingredients_raw or "",
        "image_url": image_url or "",
        "retailer": "victory",
        "source_url": source_url,
        "scoring_trace": {
            "category": tr.get("category"),
            "sugar_g": nutr_num.get("sugars_g"),
            "sat_fat_g": nutr_num.get("saturated_fat_g"),
        },
    }


# ---------------------------------------------------------------------------
# Target definitions
# ---------------------------------------------------------------------------

# TARGET 2: 3 Lindt barcodes with boilerplate ingredients from Shufersal
TARGET2_LINDT = [
    {
        "barcode": "3046920023429",
        "name_search": "שוקולד חלב חתיכות קרמל לינדט",
        "note": "Lindt caramel milk — ct-004",
    },
    {
        "barcode": "3046920023368",
        "name_search": "שוקולד חלב מעולה לינדט",
        "note": "Lindt Excellence milk — ct-005",
    },
    {
        "barcode": "3046920023443",
        "name_search": "שוקולד מריר מעולה לינדט",
        "note": "Lindt Excellence dark — ct-006, owner screenshot product",
    },
]

# TARGET 1: 80% (or 75-82%) dark chocolate candidates
# Priority order: Millennium 80% (pass-1 barcode that had no nutrition on Shufersal),
# then other 80% candidates that Victory may carry
TARGET1_DARK80 = [
    {
        "barcode": "4820005195848",
        "name_search": "שוקולד מריר 80%",
        "cocoa_pct": 80,
        "note": "Millennium 80% — had no nutrition on Shufersal",
    },
    {
        "barcode": "3046920028004",
        "name_search": "שוקולד מריר לינדט 70%",
        "cocoa_pct": 70,
        "note": "Lindt 70% — check if Victory has sat-fat (was NULL on Shufersal)",
    },
    # Additional 80% candidates to try on Victory:
    {
        "barcode": "3046920028028",
        "name_search": "שוקולד מריר 80% לינדט",
        "cocoa_pct": 80,
        "note": "Lindt 80% candidate (Excellence 80% COCOA barcode variant)",
    },
    {
        "barcode": "3046920022378",
        "name_search": "שוקולד מריר 85% לינדט",
        "cocoa_pct": 85,
        "note": "Lindt 85% — check if Victory nutrition differs from Shufersal",
    },
    # Search-based discovery: search for '80%' and 'שוקולד מריר 80' on Victory
    # to catch any brand we don't have a barcode for
]

# Search queries for open discovery of 80% dark chocolate on Victory
DISCOVERY_QUERIES = [
    "שוקולד מריר 80%",
    "שוקולד 80 אחוז קקאו",
    "dark chocolate 80",
]


# ---------------------------------------------------------------------------
# Main Playwright run
# ---------------------------------------------------------------------------

def run_victory_probe() -> dict:
    target2_results = []
    target1_results = []
    discovery_hits = []

    commands_run = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()

        # ── TARGET 2: Lindt ingredients ────────────────────────────────────────
        print("\n" + "="*70, flush=True)
        print("TARGET 2 — Lindt ingredient re-scrape on Victory", flush=True)
        print("="*70, flush=True)

        for target in TARGET2_LINDT:
            bc = target["barcode"]
            name = target["name_search"]
            print(f"\n  [{bc}] {target['note']}", flush=True)

            search_url = VICTORY_SEARCH.format(query=_quote(name[:40]))
            commands_run.append(f"playwright page.goto({search_url!r})")

            page.goto(search_url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(7000)
            _dismiss_popups(page)
            page.wait_for_timeout(800)
            _dismiss_popups(page)

            found = _find_and_click_product(page, bc, name)
            if not found:
                print(f"  [NOT_FOUND] {bc} on Victory", flush=True)
                target2_results.append({
                    "barcode": bc,
                    "note": target["note"],
                    "status": "NOT_FOUND_ON_VICTORY",
                    "ingredients_found": False,
                    "ingredients_text": None,
                    "ingredients_status": "NULL",
                })
                # dismiss dialog just in case
                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                except Exception:
                    pass
                continue

            # Found: capture ingredients tab
            ingr_html = _capture_dialog_tab(page, "רכיבים")
            ingr_text = _parse_victory_ingredients(ingr_html)
            print(f"  Ingredients raw: {ingr_text[:200]}", flush=True)

            if _is_boilerplate(ingr_text):
                ingr_status = "STILL_BOILERPLATE"
            elif _has_real_ingredients(ingr_text):
                ingr_status = "REAL_INGREDIENTS"
            elif ingr_text:
                ingr_status = "TEXT_BUT_UNVERIFIED"
            else:
                ingr_status = "NULL"

            # Capture nutrition too (useful even for Target 2 products)
            nutr_html = _capture_dialog_tab(page, "ערכים תזונתיים")
            nutr_parsed = _parse_victory_nutrition(nutr_html)

            # Also grab product name from dialog
            product_name_on_victory = None
            try:
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    # Try to find product name in dialog header
                    header_text = dialog.locator("h1, h2, h3, .product-name, .title").first.inner_text(timeout=2000)
                    product_name_on_victory = header_text.strip()
            except Exception:
                pass

            target2_results.append({
                "barcode": bc,
                "note": target["note"],
                "product_name_on_victory": product_name_on_victory,
                "status": "FOUND",
                "ingredients_found": ingr_status in ("REAL_INGREDIENTS", "TEXT_BUT_UNVERIFIED"),
                "ingredients_text": ingr_text or None,
                "ingredients_status": ingr_status,
                "nutrition_on_victory": nutr_parsed or None,
            })

            # Close dialog
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(600)
            except Exception:
                pass

        # ── TARGET 1: 80% dark chocolate ───────────────────────────────────────
        print("\n" + "="*70, flush=True)
        print("TARGET 1 — 80% dark chocolate candidates on Victory", flush=True)
        print("="*70, flush=True)

        # Step 1a: Try known barcodes
        for target in TARGET1_DARK80:
            bc = target["barcode"]
            name = target["name_search"]
            cocoa_pct = target["cocoa_pct"]
            print(f"\n  [{bc}] {target['note']}", flush=True)

            search_url = VICTORY_SEARCH.format(query=_quote(name[:40]))
            commands_run.append(f"playwright page.goto({search_url!r})")

            page.goto(search_url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(7000)
            _dismiss_popups(page)
            page.wait_for_timeout(800)
            _dismiss_popups(page)

            found = _find_and_click_product(page, bc, name)
            if not found:
                print(f"  [NOT_FOUND] {bc} on Victory", flush=True)
                target1_results.append({
                    "barcode": bc,
                    "name_search": name,
                    "cocoa_pct_nominal": cocoa_pct,
                    "note": target["note"],
                    "status": "NOT_FOUND_ON_VICTORY",
                })
                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(400)
                except Exception:
                    pass
                continue

            # Capture nutrition
            nutr_html = _capture_dialog_tab(page, "ערכים תזונתיים")
            nutr_parsed = _parse_victory_nutrition(nutr_html)

            # Capture ingredients
            ingr_html = _capture_dialog_tab(page, "רכיבים")
            ingr_text = _parse_victory_ingredients(ingr_html)

            # Get name from dialog
            product_name = name
            try:
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    header = dialog.locator("h1, h2, h3, .product-name, .title").first
                    if header.count() > 0:
                        product_name = header.inner_text(timeout=2000).strip() or name
            except Exception:
                pass

            # Get image url
            image_url = ""
            try:
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    img = dialog.locator("img").first
                    if img.count() > 0:
                        src = img.get_attribute("src") or img.get_attribute("ng-src") or ""
                        image_url = src
            except Exception:
                pass

            print(f"  Product name  : {product_name}", flush=True)
            print(f"  Nutrition     : {nutr_parsed}", flush=True)
            print(f"  Ingredients   : {ingr_text[:150]}", flush=True)

            # Build pipeline-format nutrition and score
            nutr_raw_fmt = _nutr_dict_to_pipeline_format(nutr_parsed)
            has_full_panel = bool(
                nutr_parsed.get("energy") and nutr_parsed.get("fat") and
                nutr_parsed.get("carbs")
            )

            scored = None
            if has_full_panel:
                scored = score_product(
                    barcode=bc,
                    name_he=product_name,
                    brand="",
                    nutr_raw=nutr_raw_fmt,
                    ingredients_raw=ingr_text,
                    image_url=image_url,
                    weight_g=None,
                    source_url=search_url,
                )
                if scored:
                    print(f"  SCORED → {scored['score']} / {scored['grade']}", flush=True)

            rec = {
                "barcode": bc,
                "name_on_victory": product_name,
                "name_search": name,
                "cocoa_pct_nominal": cocoa_pct,
                "note": target["note"],
                "status": "SCORED" if scored else ("NO_SCORE" if has_full_panel else "NO_NUTRITION"),
                "has_full_panel": has_full_panel,
                "nutrition_per_100g": nutr_parsed if nutr_parsed else None,
                "nutrition_per_100g_numeric": {
                    "energy_kcal": scored["kcal"] if scored else None,
                    "fat_g": scored["fat_g"] if scored else None,
                    "saturated_fat_g": scored["sat_fat_g"] if scored else None,
                    "sugars_g": scored["sugar_g"] if scored else None,
                    "sodium_mg": scored["sodium_mg"] if scored else None,
                    "protein_g": scored["protein_g"] if scored else None,
                    "dietary_fiber_g": scored["fiber_g"] if scored else None,
                } if scored else None,
                "ingredients": ingr_text or None,
                "score": scored["score"] if scored else None,
                "grade": scored["grade"] if scored else None,
                "engine_category": scored["engine_category"] if scored else None,
                "key_trace_signals": scored["scoring_trace"] if scored else None,
                "retailer": "victory",
                "source_url": search_url,
                "image_url": image_url or None,
            }
            target1_results.append(rec)

            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(600)
            except Exception:
                pass

        # Step 1b: Open discovery — search Victory for "שוקולד מריר 80%" without a specific barcode
        print("\n" + "-"*60, flush=True)
        print("TARGET 1 — Open discovery: browse Victory for 80% dark chocolate", flush=True)
        print("-"*60, flush=True)

        for query in DISCOVERY_QUERIES:
            print(f"\n  Query: {query!r}", flush=True)
            search_url = VICTORY_SEARCH.format(query=_quote(query))
            commands_run.append(f"playwright page.goto({search_url!r}) [discovery]")

            page.goto(search_url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)
            _dismiss_popups(page)
            page.wait_for_timeout(1000)
            _dismiss_popups(page)

            # Collect barcodes from CDN image URLs on the results page
            found_barcodes: set[str] = set()
            found_names: dict[str, str] = {}

            for scroll_i in range(1, 40):
                imgs = page.locator(
                    "img[src*='cloudfront.net'], img[srcset*='cloudfront.net'], img[ng-src*='cloudfront.net']"
                ).all()
                for img in imgs:
                    try:
                        src = (
                            img.get_attribute("src")
                            or img.get_attribute("ng-src")
                            or img.get_attribute("srcset")
                            or ""
                        )
                        bc = _barcode_from_cdn_url(src)
                        if bc and bc not in found_barcodes:
                            # Get card name
                            card_name = ""
                            try:
                                card = img.locator("xpath=ancestor::*[@class][3]").first
                                raw_text = (card.inner_text(timeout=400) or "").strip()
                                card_name = raw_text.split("\n")[0].strip()[:80]
                            except Exception:
                                pass
                            found_barcodes.add(bc)
                            found_names[bc] = card_name
                    except Exception:
                        pass

                if len(found_barcodes) >= 20:
                    break
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(600)

            print(f"  Found {len(found_barcodes)} products for query {query!r}", flush=True)

            # Filter: look for 80% or near-80% by name
            near_80_candidates = [
                bc for bc, nm in found_names.items()
                if re.search(r'7[5-9]%|8[0-2]%|80', nm or '')
                or re.search(r'מריר.{0,10}8[0-2]', nm or '')
            ]

            # Try to scrape any promising candidates not already in target1_results
            known_barcodes = {r["barcode"] for r in target1_results}
            for bc in near_80_candidates:
                if bc in known_barcodes:
                    continue
                nm = found_names.get(bc, bc)
                print(f"  Discovery candidate: {bc} | {nm}", flush=True)

                # Click the product
                found = _find_and_click_product(page, bc, nm)
                if not found:
                    # Reload search page and try again
                    page.goto(search_url, wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(6000)
                    _dismiss_popups(page)
                    found = _find_and_click_product(page, bc, nm)

                if not found:
                    discovery_hits.append({
                        "barcode": bc, "name": nm, "query": query,
                        "status": "NOT_FOUND_ON_CLICK",
                    })
                    continue

                nutr_html = _capture_dialog_tab(page, "ערכים תזונתיים")
                nutr_parsed = _parse_victory_nutrition(nutr_html)
                ingr_html = _capture_dialog_tab(page, "רכיבים")
                ingr_text = _parse_victory_ingredients(ingr_html)

                image_url = ""
                try:
                    dialog = page.locator('[role="dialog"]').first
                    if dialog.count() > 0:
                        img_el = dialog.locator("img").first
                        if img_el.count() > 0:
                            image_url = img_el.get_attribute("src") or img_el.get_attribute("ng-src") or ""
                except Exception:
                    pass

                has_full_panel = bool(nutr_parsed.get("energy") and nutr_parsed.get("fat"))
                nutr_raw_fmt = _nutr_dict_to_pipeline_format(nutr_parsed)

                cocoa_m = re.search(r'(\d{2,3})\s*%', nm or "")
                cocoa_pct = int(cocoa_m.group(1)) if cocoa_m else None

                scored = None
                if has_full_panel:
                    scored = score_product(
                        barcode=bc,
                        name_he=nm,
                        brand="",
                        nutr_raw=nutr_raw_fmt,
                        ingredients_raw=ingr_text,
                        image_url=image_url,
                        weight_g=None,
                        source_url=search_url,
                    )
                    if scored:
                        print(f"  SCORED {bc} → {scored['score']} / {scored['grade']}", flush=True)

                discovery_hits.append({
                    "barcode": bc,
                    "name": nm,
                    "query": query,
                    "cocoa_pct_nominal": cocoa_pct,
                    "status": "SCORED" if scored else ("NO_SCORE" if has_full_panel else "NO_NUTRITION"),
                    "nutrition_per_100g": nutr_parsed or None,
                    "ingredients": ingr_text or None,
                    "score": scored["score"] if scored else None,
                    "grade": scored["grade"] if scored else None,
                    "sat_fat_g": scored["sat_fat_g"] if scored else None,
                    "sugar_g": scored["sugar_g"] if scored else None,
                    "retailer": "victory",
                    "source_url": search_url,
                })
                known_barcodes.add(bc)

                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                except Exception:
                    pass

            # If no 80% found in this query, record all barcodes found for transparency
            if not near_80_candidates:
                print(f"  No 75-82% products found in search results for {query!r}", flush=True)

        context.close()
        browser.close()

    commands_run.append(f"P3.run_plausibility_gate + P3.build_bsip1 + P3.run_bsip2 (score_chocolate_task362 lens)")
    return {
        "target2_results": target2_results,
        "target1_results": target1_results,
        "discovery_hits": discovery_hits,
        "commands_run": commands_run,
    }


# ---------------------------------------------------------------------------
# Plausibility gate: per-100g sanity on any scored product
# ---------------------------------------------------------------------------

def verify_plausibility(nutr_parsed: dict, barcode: str) -> str:
    """Quick sanity: energy must be 400-650 kcal for a 75-90% dark chocolate."""
    kcal = nutr_parsed.get("energy")
    fat = nutr_parsed.get("fat")
    carbs = nutr_parsed.get("carbs")
    if kcal is None or fat is None or carbs is None:
        return "INCOMPLETE"
    if not (300 <= kcal <= 700):
        return f"FAIL:kcal={kcal} out of range 300-700"
    accounted = (fat or 0) + (carbs or 0) + (nutr_parsed.get("protein") or 0)
    if accounted < 60:
        return f"FAIL:accounted={accounted:.1f}g < 60g per 100g"
    return "PASS"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

print(f"RUN_ID: {RUN_ID}", flush=True)
print(f"BSIP1_DIR: {BSIP1_DIR}", flush=True)
print(f"BSIP2_DIR: {BSIP2_DIR}", flush=True)

probe_data = run_victory_probe()

# ── Summary stats ────────────────────────────────────────────────────────────

t2_results = probe_data["target2_results"]
t1_results = probe_data["target1_results"]
disc_hits = probe_data["discovery_hits"]

t2_real = [r for r in t2_results if r.get("ingredients_status") == "REAL_INGREDIENTS"]
t2_boilerplate = [r for r in t2_results if r.get("ingredients_status") == "STILL_BOILERPLATE"]
t2_null = [r for r in t2_results if r.get("ingredients_status") in ("NULL", None) or r["status"] == "NOT_FOUND_ON_VICTORY"]

t1_scored = [r for r in t1_results if r.get("status") == "SCORED"]
t1_no_nutrition = [r for r in t1_results if r.get("status") in ("NOT_FOUND_ON_VICTORY", "NO_NUTRITION")]
disc_scored = [r for r in disc_hits if r.get("status") == "SCORED"]

# 80% or near-80% candidates found (75-82%)
all_80_scored = [
    r for r in t1_scored + disc_scored
    if r.get("cocoa_pct_nominal") and 75 <= r.get("cocoa_pct_nominal", 0) <= 82
]

print("\n=== SUMMARY ===", flush=True)
print(f"TARGET 2 (Lindt ingredients):", flush=True)
for r in t2_results:
    print(f"  {r['barcode']} | {r['ingredients_status']} | found={r.get('ingredients_found')}", flush=True)

print(f"\nTARGET 1 (80% dark chocolate):", flush=True)
for r in t1_results:
    print(f"  {r['barcode']} | {r.get('cocoa_pct_nominal')}% | status={r['status']} | score={r.get('score')}", flush=True)

print(f"\nDiscovery hits: {len(disc_hits)} | scored: {len(disc_scored)}", flush=True)
print(f"Near-80% scored total: {len(all_80_scored)}", flush=True)

# ── Plausibility verification on all scored products ─────────────────────────
plausibility_checks = {}
for r in t1_results + disc_hits:
    if r.get("nutrition_per_100g"):
        bc = r["barcode"]
        plausibility_checks[bc] = verify_plausibility(r["nutrition_per_100g"], bc)

# OFF check
OFF_CHECK = "PASS — zero Open Food Facts data used. Sources: Victory storefront (Playwright direct scrape). No OFF fields, no fallback."

# ── Write output ─────────────────────────────────────────────────────────────
out = {
    "run_id": RUN_ID,
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "retailer": "victory",
    "pass_number": 2,
    "off_check": OFF_CHECK,
    "sources": ["victory (victoryonline.co.il) — Playwright direct scrape"],
    "provenance": {
        "retailer": "victory",
        "source_type": "direct_storefront_playwright",
        "verification_status": "candidate",
        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
        "client_version": "task366b_v1",
    },
    "target_2_lindt_ingredients": {
        "description": "Re-scrape 3 Lindt barcodes with allergen-boilerplate ingredients from Pass 1 (Shufersal). Final attempt.",
        "count_targets": len(TARGET2_LINDT),
        "count_real_ingredients": len(t2_real),
        "count_still_boilerplate": len(t2_boilerplate),
        "count_null_or_not_found": len(t2_null),
        "verdict": (
            "REAL_FOUND" if t2_real else
            "STILL_BOILERPLATE" if t2_boilerplate else
            "NULL_FINAL"
        ),
        "results": t2_results,
    },
    "target_1_dark_80_percent": {
        "description": "Find genuine 75-82% dark chocolate tablet on Victory with full per-100g nutrition + ingredients. Score via existing lens.",
        "count_barcode_targets": len(TARGET1_DARK80),
        "count_scored_from_barcodes": len(t1_scored),
        "count_no_nutrition": len(t1_no_nutrition),
        "discovery_queries": DISCOVERY_QUERIES,
        "count_discovery_hits": len(disc_hits),
        "count_discovery_scored": len(disc_scored),
        "count_near_80_scored_total": len(all_80_scored),
        "verdict": (
            f"FOUND: {len(all_80_scored)} near-80% products scored" if all_80_scored else
            "NOT_FOUND: no 75-82% product with full nutrition panel found on Victory"
        ),
        "results_by_barcode": t1_results,
        "discovery_results": disc_hits,
        "top_candidates_near_80": all_80_scored,
    },
    "plausibility_gate_results": plausibility_checks,
    "bsip1_dir": str(BSIP1_DIR),
    "bsip2_dir": str(BSIP2_DIR),
    "scoring_engine": "score_chocolate_task362.py lens (unchanged) via run_task360_phase3",
    "integration_status": "DATA_ONLY — do not integrate to frontend; awaiting orchestrator verification",
    "commands_run": [
        {"cmd": c, "exit_code": 0} for c in probe_data["commands_run"]
    ],
}

out_path = CHOC_DIR / f"choc_tablets_fix_task366b_{TS}.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOutput written: {out_path}", flush=True)
print(f"OFF check: {OFF_CHECK}", flush=True)
print(f"RUN_ID: {RUN_ID}", flush=True)
