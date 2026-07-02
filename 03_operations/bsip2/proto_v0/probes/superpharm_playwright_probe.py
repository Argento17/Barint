"""
Super-Pharm Playwright Layer 2 Probe
=====================================
Task: TASK-395 (de-chain program — Super-Pharm supplement facts verification)
Date: 2026-06-25
Purpose: Determine whether supplement facts + ingredient text appear in the
         fully rendered DOM of Super-Pharm product pages. The static-HTML
         probe (new_sources_probe_v1.md §A.2) confirmed identity/barcode but
         NOT supplement facts. This probe closes that open question.

Products probed:
  p/332649  — multivitamin prenatal (barcode 7290011899479)
  p/704023  — magnesium bisglycinate  (barcode 7290122852608)
  + 2 additional from magnesium category page /c/30301113

Strategy:
  1. Full render via Playwright headless Chromium (networkidle wait)
  2. Dismiss popups / cookie banners
  3. Try clicking supplement-facts / ingredients / extra-details tabs/accordions
  4. Capture full rendered HTML and query candidate selectors
  5. Intercept XHR/fetch calls for any product JSON API
  6. Report verified text verbatim — never infer

Run: python superpharm_playwright_probe.py
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Page, Response

# Output dir for captured HTML (for post-hoc manual inspection)
OUT_DIR = Path(__file__).parent / "superpharm_playwright_captures"
OUT_DIR.mkdir(exist_ok=True)

BASE = "https://shop.super-pharm.co.il"

TARGET_PRODUCTS = [
    {
        "label": "multivitamin-prenatal",
        "product_code": "332649",
        "barcode_expected": "7290011899479",
        "url": f"{BASE}/health/supplements/vitamins/c/30301000/p/332649",
        "url_alt": f"{BASE}/p/332649",
    },
    {
        "label": "magnesium-bisglycinate",
        "product_code": "704023",
        "barcode_expected": "7290122852608",
        "url": f"{BASE}/health/supplements/minerals/magnesium/מגנזיום-ביסגליצינאט/p/704023",
        "url_alt": f"{BASE}/p/704023",
    },
]

MAGNESIUM_CATEGORY_URL = f"{BASE}/health/supplements/minerals/magnesium/c/30301113"

# Tab/accordion selectors to try clicking — in priority order
# SAP Hybris typically renders a tab strip; labels vary by locale and product config
CLICK_TARGETS = [
    # Text-based — most reliable for Hebrew pages
    "text=מידע נוסף",
    "text=רכיבים",
    "text=מרכיבים",
    "text=תכולה",
    "text=עובדות תזונה",
    "text=נתוני תוסף",
    "text=ערכים תזונתיים",
    "text=הרכב",
    "text=פרטים נוספים",
    "text=More Info",
    "text=Supplement Facts",
    "text=Ingredients",
    # Attribute / class based
    "a[href*='supplement']",
    "a[href*='nutrition']",
    "a[href*='ingredients']",
    "a[href*='מרכיב']",
    "button[data-tab*='supplement']",
    "button[data-tab*='nutrition']",
    ".product-tabs li:not(.active)",
    ".tab-nav a:not(.active)",
    "li.tab:not(.selected)",
    "[role='tab']",
    # SAP Hybris accordion pattern
    "a.accordion-heading",
    ".product-details-tab a",
    ".product-info-tabs a",
    ".extra-details a",
    ".extra-details button",
    "a[data-toggle='tab']",
    # Generic expand
    ".collapse-toggle:not(.active)",
    ".expandable-content button",
]

# Content selectors to check AFTER clicking (for supplement facts text)
FACT_SELECTORS = [
    # Tables
    "table",
    ".nutrition-table",
    ".supplement-facts",
    ".nutritional-info",
    ".nutrition-info",
    ".nutr-table",
    ".product-nutritional-values",
    "[class*='supplement']",
    "[class*='nutrition']",
    "[id*='supplement']",
    "[id*='nutrition']",
    # Ingredient paragraph / div
    ".ingredients",
    ".ingredients-text",
    "[class*='ingredient']",
    "[id*='ingredient']",
    # Generic product detail containers
    ".product-description",
    ".product-details",
    ".product-info",
    ".extra-details",
    ".product-properties",
    ".product-attributes",
    # SAP Hybris patterns
    ".product-info-tab-panel",
    ".tab-content",
    ".tab-pane.active",
]

# XHR patterns to intercept — looking for a product JSON API
XHR_PATTERNS = [
    "/api/",
    "product",
    "p2/?",
    "hybris",
    ".json",
    "supplement",
    "nutrition",
    "/rest/",
    "ProductData",
]

# Hebrew characters — used to detect real Hebrew product content
HE_LETTERS = set("אבגדהוזחטיכלמנסעפצקרשת")


def contains_hebrew(text: str) -> bool:
    return any(c in HE_LETTERS for c in text)


def extract_text_summary(html: str, max_chars: int = 300) -> str:
    """Strip tags and return first max_chars of text content."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def check_supplement_facts_in_dom(page: Page, label: str) -> dict:
    """
    After page render + tab clicks, check for supplement facts content.
    Returns a structured finding dict.
    """
    result = {
        "label": label,
        "supplement_facts_found": False,
        "ingredient_list_found": False,
        "serving_size_found": False,
        "raw_text_found": [],
        "selectors_with_content": [],
        "tables_found": 0,
        "table_content_preview": [],
        "verified_by": "playwright-render",
    }

    # Check for tables first — supplement facts are almost always in a table
    try:
        tables = page.locator("table").all()
        result["tables_found"] = len(tables)
        for i, tbl in enumerate(tables[:5]):
            try:
                text = tbl.text_content(timeout=2000)
                if text and len(text.strip()) > 10:
                    result["table_content_preview"].append({
                        "table_index": i,
                        "text_preview": text.strip()[:400],
                        "contains_hebrew": contains_hebrew(text),
                    })
                    # Look for supplement-facts markers
                    if any(kw in text for kw in ["מג", "mg", "מיקרוגרם", "mcg", "IU", "מגנזיום", "ויטמין"]):
                        result["supplement_facts_found"] = True
                        result["raw_text_found"].append(f"TABLE[{i}]: {text.strip()[:300]}")
            except Exception:
                pass

    except Exception as e:
        result["selectors_with_content"].append(f"table-query-error: {e}")

    # Check candidate selectors
    for sel in FACT_SELECTORS:
        try:
            els = page.locator(sel).all()
            for el in els[:3]:
                try:
                    text = el.text_content(timeout=1500)
                    if not text or len(text.strip()) < 15:
                        continue
                    text = text.strip()
                    # Ingredient detection
                    ingredient_markers = [
                        "רכיבים", "מרכיבים", "תכולה", "הרכב",
                        "Ingredients", "ingredients",
                    ]
                    fact_markers = [
                        "מגנזיום", "ויטמין", "אבץ", "ברזל", "סידן",
                        "mg", "mcg", "IU", "מג", "Magnesium", "Vitamin",
                        "supplement facts", "Supplement Facts",
                        "עובדות", "מינון", "מנה", "serving",
                    ]
                    serving_markers = [
                        "מנה", "serving size", "גודל מנה", "נטו",
                        "per serving", "ל-מנה",
                    ]

                    found_marker = None
                    for m in ingredient_markers:
                        if m in text:
                            result["ingredient_list_found"] = True
                            found_marker = f"ingredient:{m}"
                            break
                    for m in fact_markers:
                        if m in text:
                            result["supplement_facts_found"] = True
                            found_marker = found_marker or f"fact:{m}"
                            break
                    for m in serving_markers:
                        if m in text:
                            result["serving_size_found"] = True
                            found_marker = found_marker or f"serving:{m}"
                            break

                    if found_marker or contains_hebrew(text[:50]):
                        result["selectors_with_content"].append(sel)
                        result["raw_text_found"].append(
                            f"{sel}: [{found_marker}] {text[:300]}"
                        )
                except Exception:
                    pass
        except Exception:
            pass

    # Deduplicate raw_text_found entries
    seen = set()
    deduped = []
    for item in result["raw_text_found"]:
        key = item[:80]
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    result["raw_text_found"] = deduped[:20]

    return result


def probe_product_page(page: Page, product: dict, captured_xhr: list) -> dict:
    """
    Navigate to a product page, wait for full render, try tab clicks,
    then check for supplement facts.
    """
    report = {
        "product_code": product["product_code"],
        "barcode_expected": product["barcode_expected"],
        "label": product["label"],
        "url_loaded": None,
        "page_title": None,
        "load_status": "not_attempted",
        "barcode_in_dom": None,
        "popup_dismissed": [],
        "tabs_clicked": [],
        "tab_click_notes": [],
        "dom_check_before_tabs": None,
        "dom_check_after_tabs": None,
        "xhr_calls_captured": [],
        "final_verdict": None,
    }

    # Navigate to product URL
    url = product["url"]
    print(f"\n[PROBE] Loading: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=40_000)
        # Wait for network to settle (supplement content may load via XHR)
        try:
            page.wait_for_load_state("networkidle", timeout=20_000)
        except Exception:
            print("  [warn] networkidle timeout — proceeding with current state")

        report["url_loaded"] = page.url
        report["page_title"] = page.title()
        report["load_status"] = "loaded"
        print(f"  Title: {report['page_title']}")
        print(f"  URL: {report['url_loaded']}")
    except Exception as e:
        report["load_status"] = f"failed: {e}"
        print(f"  [ERROR] Navigation failed: {e}")
        return report

    # Dismiss popups
    time.sleep(1.5)
    dismissed = []
    popup_sels = [
        "button[data-testid*='accept']",
        "button[id*='accept']",
        ".cookie-accept",
        "[aria-label*='סגור']",
        "button:has-text('אישור')",
        "button:has-text('קבל')",
        "button:has-text('המשך')",
        ".modal-close",
        "button.close",
    ]
    for sel in popup_sels:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=600):
                el.click(timeout=800)
                dismissed.append(sel)
                page.wait_for_timeout(500)
        except Exception:
            pass
    report["popup_dismissed"] = dismissed
    if dismissed:
        print(f"  Dismissed popups: {dismissed}")

    # Verify barcode in DOM
    try:
        bc = product["barcode_expected"]
        bc_found = page.locator(f"text={bc}").count() > 0
        report["barcode_in_dom"] = bc_found
        print(f"  Barcode {bc} in DOM: {bc_found}")
    except Exception:
        report["barcode_in_dom"] = None

    # --- BEFORE tab clicks: baseline check ---
    report["dom_check_before_tabs"] = check_supplement_facts_in_dom(
        page, f"{product['label']}_before_tabs"
    )
    print(f"  Before tabs — supplement_facts: {report['dom_check_before_tabs']['supplement_facts_found']}, "
          f"ingredients: {report['dom_check_before_tabs']['ingredient_list_found']}, "
          f"tables: {report['dom_check_before_tabs']['tables_found']}")

    # --- Tab click attempts ---
    for sel in CLICK_TARGETS:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=500):
                old_html_len = len(page.content())
                el.click(timeout=1000)
                page.wait_for_timeout(1500)  # allow content to load
                new_html_len = len(page.content())
                note = f"clicked: {sel} (html delta={new_html_len - old_html_len:+d})"
                report["tabs_clicked"].append(sel)
                report["tab_click_notes"].append(note)
                print(f"  Tab click: {note}")
        except Exception:
            pass

    # Allow any lazy-load content to settle after tab interactions
    if report["tabs_clicked"]:
        try:
            page.wait_for_load_state("networkidle", timeout=8_000)
        except Exception:
            pass
        time.sleep(1.0)

    # --- AFTER tab clicks: full check ---
    report["dom_check_after_tabs"] = check_supplement_facts_in_dom(
        page, f"{product['label']}_after_tabs"
    )
    print(f"  After tabs  — supplement_facts: {report['dom_check_after_tabs']['supplement_facts_found']}, "
          f"ingredients: {report['dom_check_after_tabs']['ingredient_list_found']}, "
          f"tables: {report['dom_check_after_tabs']['tables_found']}")

    # Capture XHR calls seen during this product page load
    report["xhr_calls_captured"] = [c["url"] for c in captured_xhr
                                     if product["product_code"] in c.get("url", "")
                                     or product["barcode_expected"] in c.get("url", "")]

    # Save full rendered HTML for manual inspection
    html_path = OUT_DIR / f"{product['label']}_rendered.html"
    html_path.write_text(page.content(), encoding="utf-8")
    print(f"  Saved rendered HTML: {html_path}")

    # Verdict
    after = report["dom_check_after_tabs"]
    facts_present = after["supplement_facts_found"] or after["ingredient_list_found"]
    report["final_verdict"] = "FACTS_FOUND" if facts_present else "NOT_FOUND"
    print(f"  VERDICT: {report['final_verdict']}")

    return report


def discover_extra_magnesium_products(page: Page) -> list[dict]:
    """
    Load the magnesium category page and pick 2 additional products
    beyond the two already known, to expand the probe sample.
    """
    print(f"\n[CATEGORY] Loading magnesium category: {MAGNESIUM_CATEGORY_URL}")
    try:
        page.goto(MAGNESIUM_CATEGORY_URL, wait_until="domcontentloaded", timeout=30_000)
        try:
            page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
    except Exception as e:
        print(f"  [ERROR] Category page failed: {e}")
        return []

    # Extract product codes and barcodes from the DOM
    products = []
    try:
        # SAP Hybris category pages render product cards with data attributes
        els = page.locator("[data-product-code]").all()
        print(f"  Found {len(els)} [data-product-code] elements")
        for el in els[:30]:
            try:
                code = el.get_attribute("data-product-code")
                ean = el.get_attribute("data-ean")
                name_attr = el.get_attribute("data-name")
                if code and ean:
                    products.append({
                        "product_code": code,
                        "barcode": ean,
                        "name": name_attr or "",
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"  [warn] data-product-code query failed: {e}")

    # Filter out the two already targeted
    known_codes = {"332649", "704023"}
    extra = [p for p in products if p["product_code"] not in known_codes]
    print(f"  Extra products found: {len(extra)}")
    for p in extra[:4]:
        print(f"    code={p['product_code']} ean={p['barcode']} name={p['name'][:40]}")

    return extra[:2]  # probe 2 additional


def run_probe() -> dict:
    """Main probe entry point."""
    all_xhr: list[dict] = []

    def on_response(response: Response):
        url = response.url
        if any(pat in url for pat in XHR_PATTERNS):
            try:
                body = response.body()
                all_xhr.append({
                    "url": url,
                    "status": response.status,
                    "body_len": len(body),
                    "body_preview": body[:500].decode("utf-8", errors="replace"),
                })
            except Exception:
                all_xhr.append({"url": url, "status": response.status, "body_len": 0})

    results = {
        "probe_date": "2026-06-25",
        "task": "TASK-395",
        "products": [],
        "xhr_api_candidates": [],
        "summary": {},
    }

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            viewport={"width": 1280, "height": 900},
            extra_http_headers={
                "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8",
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            },
        )
        page = context.new_page()
        page.on("response", on_response)

        # Probe 1: discover 2 extra magnesium products from category page
        extra_products = discover_extra_magnesium_products(page)

        # Build full product list: 2 known + 2 extra from category
        all_products = list(TARGET_PRODUCTS)
        for ep in extra_products[:2]:
            all_products.append({
                "label": f"mag-extra-{ep['product_code']}",
                "product_code": ep["product_code"],
                "barcode_expected": ep["barcode"],
                "url": f"{BASE}/health/supplements/minerals/magnesium/p/{ep['product_code']}",
                "url_alt": f"{BASE}/p/{ep['product_code']}",
            })

        # Probe each product page
        for product in all_products:
            report = probe_product_page(page, product, all_xhr)
            results["products"].append(report)

        # Collect interesting XHR calls
        interesting_xhr = [
            x for x in all_xhr
            if x.get("body_len", 0) > 100
            and any(kw in x.get("body_preview", "")
                    for kw in ["supplement", "nutrition", "ingredient", "מגנזיום",
                               "Magnesium", "mg", "serving", "productData",
                               "nutritionFacts", "ויטמין"])
        ]
        results["xhr_api_candidates"] = interesting_xhr[:10]

        context.close()
        browser.close()

    # Compute summary
    facts_found_count = sum(
        1 for p in results["products"]
        if p.get("final_verdict") == "FACTS_FOUND"
    )
    ingredient_found_count = sum(
        1 for p in results["products"]
        if p.get("dom_check_after_tabs", {}).get("ingredient_list_found", False)
    )
    results["summary"] = {
        "products_probed": len(results["products"]),
        "supplement_facts_found": facts_found_count,
        "ingredient_list_found": ingredient_found_count,
        "xhr_api_candidates_with_nutrition": len(results["xhr_api_candidates"]),
        "overall_verdict": (
            "SUPPLEMENT_FACTS_AVAILABLE"
            if facts_found_count > 0
            else "NOT_FOUND_AFTER_FULL_RENDER"
        ),
    }

    # Save full JSON results
    results_path = OUT_DIR / "probe_results.json"
    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[DONE] Results saved: {results_path}")
    print(f"Summary: {json.dumps(results['summary'], ensure_ascii=False, indent=2)}")

    return results


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    run_probe()
