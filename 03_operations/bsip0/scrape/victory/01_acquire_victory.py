"""
BSIP0 Victory (ויקטורי) — Product acquisition via local Playwright.

Victory runs the same SaaS as Yohananof (same CDN: d226b0iufwcjmj.cloudfront.net,
retailer ID 1470). This adapter is a direct port of the Yohananof scraper with
Victory-specific URL and popup handling.

Architecture:
  Identity:  il_prices via laibcatalog (chain 7290696200003) — barcodes + Hebrew names
  Panel:     Direct Playwright — open product modal, click "ערכים תזונתיים" / "רכיבים" tabs
  Fallback:  OFF per-barcode API if modal tabs return empty (common for imported products)
  Firecrawl: NOT used. Playwright-only.

Run order:
  1. python 01_acquire_victory.py          — discover + scrape (writes outputs/)
  2. python 02_build_bsip1_victory.py      — parse + build BSIP1 records

Output:
  C:\\Bari\\03_operations\\bsip0\\scrape\\victory\\outputs\\victory_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip
from integrations.clients import open_food_facts as off
from integrations.source_validator import require_il_prices_accessible

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

RETAILER_ID = "victory"
RETAILER_NAME = "ויקטורי"
CHAIN_ID = "7290696200003"  # confirmed via laibcatalog

BASE_URL = "https://www.victoryonline.co.il"
SEARCH_URL = BASE_URL + "/category?search={query}"  # same SaaS as Yohananof

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Name filter — caller sets INCLUDE_SIGNALS and HARD_DROP per category
# ---------------------------------------------------------------------------

def name_matches(name: str, include: list[str], drop: list[str]) -> bool:
    nl = (name or "").lower()
    if any(h.lower() in nl for h in drop):
        return False
    return any(s.lower() in nl for s in include)


def extract_weight_g(name: str) -> float | None:
    for pat in (
        re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.I),
        re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.I),
        re.compile(r"(\d[\d,.]*)\s*g\b", re.I),
    ):
        m = pat.search(name)
        if m:
            try:
                v = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    v *= 1000
                if 50 < v < 5000:
                    return v
            except ValueError:
                pass
    return None


# ---------------------------------------------------------------------------
# Image URL helpers (same CDN pattern as Yohananof)
# ---------------------------------------------------------------------------

def normalize_image_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None
    first = raw_url.split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        parsed = urlparse(first)
        qs = parse_qs(parsed.query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


def barcode_from_cdn_url(img_url: str) -> str | None:
    """
    Victory CDN embeds barcode in image path:
    d226b0iufwcjmj.cloudfront.net/gs1-products/1470/medium/<EAN>-<ID>/<EAN>/...
    """
    if not img_url:
        return None
    m = re.search(r"/gs1-products/\d+/\w+/(\d{8,13})-", img_url)
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Playwright helpers — ported from Yohananof scraper
# ---------------------------------------------------------------------------

def dismiss_all_popups(page) -> None:
    """Dismiss Victory's two known popups in order:
    1. MaxCard/loyalty marketing modal (DOM dialog with 'אישור' button)
    2. General cookie/consent dialogs

    The browser-level geolocation popup is suppressed at context creation
    via permissions=[] — it never reaches the DOM, so no action needed here.
    Call this after every page.goto() + wait, and again after any heavy interaction.
    """
    # Pass 1: named 'אישור' button inside a dialog or modal
    for selector in [
        'button:has-text("אישור")',
        'button:has-text("מסכים")',
        'button:has-text("הבנתי")',
        '[data-aria-desc="dialog_cookies_accept"]',
        '[role="dialog"] button',       # generic modal close — last resort
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=600):
                btn.click(force=True)
                page.wait_for_timeout(700)
        except Exception:
            pass

    # Pass 2: text-match sweep for any remaining overlay
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            btn = page.get_by_text(text, exact=True).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass


# Keep old name as alias so callers outside this file don't break
close_cookie_popup = dismiss_all_popups


def find_product_on_page(page, barcode: str, name: str) -> bool:
    """
    Scroll through a search results page to find the product card.
    Tries barcode-in-image-src first (CDN pattern), falls back to name text.
    Returns True if found and clicked to open modal.

    Victory uses AngularJS ng-src — check both src and ng-src attributes.
    """
    barcode_locator = page.locator(
        f'img[src*="{barcode}"], img[srcset*="{barcode}"], img[ng-src*="{barcode}"]'
    ).first
    name_locator = page.get_by_text(name, exact=False).first

    for i in range(1, 121):
        if i % 10 == 0:
            print(f"  Searching... attempt {i}/120 | {barcode} | {name[:40]}")

        try:
            if barcode_locator.count() > 0:
                barcode_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                barcode_locator.click(force=True)
                page.wait_for_timeout(4500)
                return True
        except Exception:
            pass

        try:
            if name_locator.count() > 0:
                name_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4500)
                return True
        except Exception:
            pass

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    return False


def capture_current_dialog(page, output_path: Path) -> str:
    try:
        dialog = page.locator('[role="dialog"]').first
        if dialog.count() == 0:
            output_path.write_text("", encoding="utf-8")
            return "dialog_missing"
        html = dialog.inner_html(timeout=5000)
        output_path.write_text(html, encoding="utf-8")
        return "success" if len(html.strip()) >= 50 else "captured_but_nearly_empty"
    except Exception as e:
        output_path.write_text("", encoding="utf-8")
        return f"dialog_capture_failed:{str(e)[:120]}"


def capture_tab(page, tab_name: str, output_path: Path, retries: int = 2) -> str:
    for attempt in range(1, retries + 1):
        try:
            if page.locator('[role="tab"]').count() == 0:
                return capture_current_dialog(page, output_path)
            tab = page.get_by_role("tab", name=tab_name).first
            if tab.count() == 0:
                output_path.write_text("", encoding="utf-8")
                return "tab_missing"
            tab.click(force=True)
            page.wait_for_timeout(2200)
            return capture_current_dialog(page, output_path)
        except PlaywrightTimeoutError:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return "timeout"
            page.wait_for_timeout(1200)
        except Exception as e:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return f"failed:{str(e)[:120]}"
            page.wait_for_timeout(1200)
    output_path.write_text("", encoding="utf-8")
    return "unknown_failure"


def close_dialog(page) -> None:
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Per-product scrape
# ---------------------------------------------------------------------------

def scrape_one(page, barcode: str, name: str, query: str) -> dict:
    product_dir = OUT_DIR / barcode
    product_dir.mkdir(parents=True, exist_ok=True)

    url = SEARCH_URL.format(query=quote(query))
    print(f"  → {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)  # AngularJS digest needs extra time after networkidle
    dismiss_all_popups(page)      # pass 1: geolocation already blocked; clears MaxCard modal
    page.wait_for_timeout(1000)
    dismiss_all_popups(page)      # pass 2: second modal sometimes fires after first is closed

    found = find_product_on_page(page, barcode, name)
    if not found:
        close_dialog(page)
        return {
            "barcode": barcode, "name": name, "status": "not_found",
            "ingredients": "not_found", "nutrition": "not_found",
            "provenance": {
                "identity_source": "victory/laibcatalog",
                "nutrition_source": None,
                "ingredients_source": None,
                "price_source": "victory/laibcatalog",
            },
        }

    tab_results = {
        "ingredients": capture_tab(page, "רכיבים", product_dir / "ingredients.html"),
        "nutrition":   capture_tab(page, "ערכים תזונתיים", product_dir / "nutrition.html"),
        "allergens":   capture_tab(page, "מידע אלרגני", product_dir / "allergens.html"),
    }
    close_dialog(page)
    return {
        "barcode": barcode, "name": name, "status": "scraped",
        **tab_results,
        "provenance": {
            "identity_source": "victory/laibcatalog",
            "nutrition_source": "victory_storefront",
            "ingredients_source": "victory_storefront",
            "price_source": "victory/laibcatalog",
        },
    }


# ---------------------------------------------------------------------------
# Storefront-first identity (fallback when il_prices feed unavailable)
# ---------------------------------------------------------------------------

def browse_category_for_candidates(
    page,
    category_query: str,
    include_signals: list[str],
    hard_drop: list[str],
    max_products: int,
) -> list[dict]:
    """
    Browse Victory category search results and collect product stubs (barcode + name)
    by extracting barcodes from CDN image URLs.

    Used when il_prices feed is unavailable for Victory.
    Returns list of dicts with keys: barcode, name, identity_source.
    """
    from urllib.parse import quote as _q
    url = SEARCH_URL.format(query=_q(category_query))
    print(f"  Category browse: {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)  # AngularJS digest needs extra time after networkidle
    close_cookie_popup(page)

    candidates = []
    seen_barcodes: set[str] = set()

    for scroll_i in range(1, 80):
        # ng-src is AngularJS binding; also check src for resolved images
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
                bc = barcode_from_cdn_url(normalize_image_url(src))
                if not bc or bc in seen_barcodes:
                    continue
                # Try to extract product name from surrounding card element
                name = ""
                try:
                    card = img.locator("xpath=ancestor::*[@class][3]").first
                    raw_text = (card.inner_text(timeout=500) or "").strip()
                    name = raw_text.split("\n")[0].strip()[:80]
                except Exception:
                    pass
                # Search page is already filtered by query — only hard-drop on explicit blockers.
                # Don't require include_signals match here (name extraction is unreliable).
                if name and any(h.lower() in name.lower() for h in hard_drop):
                    continue
                seen_barcodes.add(bc)
                candidates.append({"barcode": bc, "name": name or bc, "identity_source": "victory_storefront_browse"})
                if len(candidates) >= max_products:
                    return candidates
            except Exception:
                pass

        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(900)
        if scroll_i % 10 == 0:
            print(f"  Browsing... scroll {scroll_i}/80, found {len(candidates)} candidates so far")

    return candidates


# ---------------------------------------------------------------------------
# Main acquisition flow (il_prices identity → Playwright panel → OFF fallback)
# ---------------------------------------------------------------------------

def acquire(
    include_signals: list[str],
    hard_drop: list[str],
    category: str,
    max_products: int = 150,
    headless: bool = False,
) -> list[dict]:
    """
    Acquire up to `max_products` Victory products for `category`.

    Identity priority:
      1. il_prices laibcatalog feed (barcodes + Hebrew names, preferred)
      2. Victory storefront category browse (fallback when feed unavailable)

    Panel priority:
      1. Playwright (direct from product modal)
      2. OFF fallback (for products where modal is empty — often imported goods)
    """
    identity_source = "victory/laibcatalog"
    candidates_raw: list  # either PriceItem objects (il_prices) or dicts (browse)

    # --- Identity: il_prices (preferred) ---
    il_prices_ok = False
    try:
        require_il_prices_accessible(RETAILER_ID)
        files = ip.list_laibcatalog_files(CHAIN_ID)
        pf = [f for f in files if f.type == "PriceFull"]
        if pf:
            items = ip.fetch_items(pf[0])
            print(f"  Victory catalog via il_prices: {len(items)} items total")
            candidates_raw = []
            seen: set[str] = set()
            for it in items:
                bc = str(it.barcode)
                if not bc or bc in seen:
                    continue
                if name_matches(it.name or "", include_signals, hard_drop):
                    seen.add(bc)
                    candidates_raw.append({"barcode": bc, "name": (it.name or "").strip()})
            candidates_raw = candidates_raw[:max_products]
            il_prices_ok = True
            print(f"  Name-gate candidates (il_prices): {len(candidates_raw)}")
        else:
            print(f"  WARNING: No PriceFull files on laibcatalog for Victory (chain {CHAIN_ID}) — using storefront browse")
    except Exception as e:
        print(f"  WARNING: il_prices unavailable ({e}) — using storefront browse")

    if not il_prices_ok:
        identity_source = "victory_storefront_browse"

    # candidates_raw will be populated via Playwright below if il_prices failed
    if not il_prices_ok:
        candidates_raw = []  # will be filled inside Playwright context

    # --- Panel: Playwright ---
    run_report = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

    # Pick a representative search query for the storefront-browse fallback
    browse_query = include_signals[0] if include_signals else category

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        # permissions=[] auto-denies geolocation and other browser permission requests
        # silently — the "wants to know your location" native dialog never appears.
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()

        # Storefront browse identity (when il_prices unavailable)
        if not il_prices_ok:
            candidates_raw = browse_category_for_candidates(
                page, browse_query, include_signals, hard_drop, max_products
            )
            print(f"  Storefront browse candidates: {len(candidates_raw)}")

        for item in candidates_raw:
            bc = item["barcode"] if isinstance(item, dict) else str(item.barcode)
            name = item["name"] if isinstance(item, dict) else (item.name or "").strip()
            query = name[:40]

            print(f"\nScraping: {bc} | {name[:50]}")
            try:
                result = scrape_one(page, bc, name, query)
                # Record actual identity source
                if "provenance" in result:
                    result["provenance"]["identity_source"] = identity_source
                    result["provenance"]["price_source"] = (
                        "victory/laibcatalog" if il_prices_ok else None
                    )
                run_report.append(result)
            except Exception as e:
                close_dialog(page)
                run_report.append({
                    "barcode": bc, "name": name, "status": "failed",
                    "error": str(e)[:300],
                    "provenance": {
                        "identity_source": identity_source,
                        "nutrition_source": None,
                        "ingredients_source": None,
                        "price_source": "victory/laibcatalog" if il_prices_ok else None,
                    },
                })
                print(f"  FAILED: {e}")

        context.close()
        browser.close()

    # --- Fallback: OFF for empty-panel products ---
    scraped_ok = [r for r in run_report if r.get("status") == "scraped"]
    nutrition_empty = [r for r in scraped_ok if r.get("nutrition") in ("tab_missing", "dialog_missing", "not_found")]
    print(f"\nOFF fallback needed for {len(nutrition_empty)} products")

    for r in nutrition_empty:
        try:
            p = off.get_product(r["barcode"])
            r["off_panel"] = {
                "found": p.found,
                "has_panel": p.has_panel,
                "name": p.name,
                "nutriments": p.nutriments if p.found else {},
                "ingredients_text": p.ingredients_text if p.found else "",
            }
            if p.found and p.has_panel:
                r.setdefault("provenance", {})
                r["provenance"]["nutrition_source"] = "off_api"
                r["provenance"]["ingredients_source"] = "off_api"
        except Exception as e:
            r["off_panel"] = {"found": False, "error": str(e)[:100]}
        time.sleep(0.2)

    # --- Write output ---
    out_path = OUT_DIR / f"victory_bsip0_raw_{ts}.json"
    out_data = {
        "schema_version": "bsip0_v1",
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "category": category,
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "identity_mode": "il_prices" if il_prices_ok else "storefront_browse",
        "candidates_total": len(candidates_raw),
        "scraped_ok": len(scraped_ok),
        "failed": sum(1 for r in run_report if r.get("status") == "failed"),
        "not_found": sum(1 for r in run_report if r.get("status") == "not_found"),
        "off_fallback_attempted": len(nutrition_empty),
        "products": run_report,
    }
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote: {out_path}")
    return run_report


# ---------------------------------------------------------------------------
# Entry point — example: hard cheese category
# ---------------------------------------------------------------------------

HARD_CHEESE_INCLUDE = [
    "גבינה צהובה", "גבינה קשה", "עמק", "טל העמק", "גאודה", "אמנטל", "פרמזן",
    "צ'דר", "קשקבל", "מנצ'גו", "גרויר", "צהובה", "cheese",
]
HARD_CHEESE_DROP = [
    "גלידה", "שוקולד", "חטיף", "ביסלי", "חיתול", "שמפו", "ניקוי",
    "ממרח", "קוטג", "לבנה", "בולגרית",
]

JUICE_INCLUDE = [
    "מיץ", "נקטר", "juice", "עסיס", "פריגת", "טרופיקנה",
]
JUICE_DROP = [
    "סוכריות", "גלידה", "שוקולד", "שמפו", "ניקוי", "חיתול",
]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=["hard_cheese", "juice"], default="hard_cheese")
    parser.add_argument("--max", type=int, default=50)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if args.category == "hard_cheese":
        acquire(HARD_CHEESE_INCLUDE, HARD_CHEESE_DROP, "hard_cheese", args.max, args.headless)
    elif args.category == "juice":
        acquire(JUICE_INCLUDE, JUICE_DROP, "juice", args.max, args.headless)
