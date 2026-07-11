"""
BSIP0 Yohananof (יוחננוף) — generic, reusable acquisition engine. TASK-518.

Fixes the two real bugs diagnosed under TASK-518 that made every prior Yohananof
category scrape under-capture (e.g. 8 of ~22 discoverable yogurt SKUs):

  BUG #1 (the actual root cause of the under-capture, diagnosed via
  _smoke_probes/diag_yohananof_scroll3.py + scroll4.py): the candidate-discovery
  regex `_(\\d{13})_` required the barcode to be delimited by an UNDERSCORE on
  BOTH sides of the digit run inside the decoded `_next/image` proxy URL. Real
  Yohananof product filenames use at least 4 different patterns:
      <sku>_<EAN>_<n>.jpg   (underscore both sides -- the only one the old regex matched)
      <sku>_<EAN>.jpg       (underscore before, dot after)
      <EAN>_s1_<date>.jpg   (barcode at the START of the basename, "/" before it)
      <EAN>.jpg             (barcode is the whole basename)
  Of ~230 distinct product image URLs collected scrolling a real "יוגורט" shelf,
  702 individual DOM occurrences failed the old regex and only 8 distinct barcodes
  were ever extracted -- almost the entire shelf was silently invisible to the
  scraper. Fix: `(?<!\\d)(\\d{13})(?!\\d)` -- any run of exactly 13 digits not
  touching another digit on either side, regardless of what non-digit character
  (or start/end of string) surrounds it. Verified against all 4 real filename
  patterns (see _smoke_probes/outputs/diag_yohananof_scroll4.json).

  BUG #2 (tried and REJECTED, documented so it isn't retried): Yohananof's product
  modal CAN be opened directly via URL (`?search=<q>&openPopups=product-<barcode>;;r0:`)
  and this DOES work for whichever product(s) happen to be in the page's initial
  (unscrolled) result batch (confirmed in diag_yohananof_direct_nav.py) -- but it
  FAILS SILENTLY (dialog never appears, even in a brand-new page/tab) for any
  barcode that only exists further down the virtualized list, because the
  client-side product store that resolves `openPopups=product-<id>` is only
  populated with whatever page of results has actually been fetched/scrolled-to;
  confirmed with diag_yohananof_fresh_page.py (2 of 3 test barcodes never got a
  dialog even with a fresh Playwright page). So direct-nav is NOT a general
  per-product shortcut -- reverted to scroll-to-find-then-click (same family as
  Victory's approach), confirmed reliable in diag_yohananof_scroll_find_click.py:
  `img[src*="<barcode>"]` matches literally (EAN digits need no URL-encoding) even
  against the RAW (non-decoded) `src` attribute, so no decode step is needed for
  the click-target locator.

Architecture:
  Discovery: browse category search page, scroll (page.mouse.wheel -- confirmed in
    diag_yohananof_scroll.py/scroll2.py this DOES move the inner MUI virtualized
    <main> container's scrollTop even though document.scrollingElement never
    changes; pointer position at default (0,0) was NOT actually a blocker),
    extract candidates via the fixed regex, name from img[alt], stability-based
    stop (N consecutive scrolls with zero NEW barcodes, not a fixed iteration
    count).
  Panel: scroll-to-find the product's image by barcode substring
    (`img[src*="<barcode>"]`), click it to open the modal, click each of the 3
    tabs (רכיבים / ערכים תזונתיים / מידע אלרגני), capture the dialog's innerHTML
    per tab (nutrition rows are LAZY-MOUNTED -- capturing before the tab click
    gets an empty tabpanel; confirmed via diag_yohananof_modal_tabs.py vs
    modal_tabs2.py). Parsed via the shared
    `_shared/bsip0_nutrition.py::extract_nutrition_raw_auto` (auto-detects the
    `#simple-tabpanel-1` Yohananof format) -- same parser Yohananof panels already
    route through elsewhere, never a bespoke regex.

Fallback: NONE. Empty panels stay NULL -- OFF is banned project-wide
  (TASK-238/247/CLAUDE.md). "Unknown is acceptable; OFF is not."

Output: <caller-set OUT_DIR>/yohananof_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs, quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import extract_nutrition_raw_auto, parse_nutrition_rows  # noqa: E402

# ---------------------------------------------------------------------------
RETAILER_ID = "yohananof"
RETAILER_NAME = "יוחננוף"
BASE_URL = "https://yochananof.co.il"
SEARCH_URL = BASE_URL + "/category?search={query}"

# THE FIX (bug #1): 13 digits not touching another digit on either side, no
# underscore requirement. See module docstring.
_BARCODE_RE = re.compile(r"(?<!\d)(\d{13})(?!\d)")

_COOKIE_TEXTS = ["אישור", "מסכים", "קבל", "הבנתי", "Accept", "OK"]
_LOAD_MORE_TEXTS = ["טען עוד", "הצג עוד", "עוד תוצאות", "טעינת עוד", "load more"]
_TAB_LABELS = ["רכיבים", "ערכים תזונתיים", "מידע אלרגני"]  # ingredients, nutrition, allergens


def close_cookie_popup(page) -> None:
    for text in _COOKIE_TEXTS:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass


def _decode_next_image_url(raw_src: str) -> str:
    first = (raw_src or "").split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        qs = parse_qs(urlparse(first).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


def _try_click_load_more(page) -> bool:
    for text in _LOAD_MORE_TEXTS:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=300):
                btn.click(force=True)
                page.wait_for_timeout(1500)
                return True
        except Exception:
            pass
    return False


def name_matches(name: str, include: list[str], drop: list[str]) -> bool:
    nl = (name or "").lower()
    if any(h.lower() in nl for h in drop):
        return False
    return not include or any(s.lower() in nl for s in include)


def discover_candidates(
    page,
    category_query: str,
    include_signals: list[str],
    hard_drop: list[str],
    max_products: int,
    max_scrolls: int = 120,
    stale_limit: int = 15,
) -> list[dict]:
    """Browse a Yohananof category-search page and collect {barcode, name} stubs.

    Scrolls the true scrollable container (page.mouse.wheel scrolls whatever is
    under the pointer at its LAST position -- confirmed harmless to leave at
    default (0,0) in diag #2, real blocker was the regex, not pointer position).
    Stops on a stability signal (N consecutive scrolls with zero NEW barcodes),
    not a fixed iteration count -- naturally extends if the page is slow.
    """
    url = SEARCH_URL.format(query=_q(category_query))
    print(f"  [yohananof] discover: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    close_cookie_popup(page)

    candidates: list[dict] = []
    seen_barcodes: set[str] = set()
    stale_scrolls = 0

    for scroll_i in range(1, max_scrolls + 1):
        before = len(candidates)
        imgs = page.locator('img[src*="_next/image"]').all()
        for img in imgs:
            try:
                src = img.get_attribute("src") or ""
                decoded = _decode_next_image_url(src)
                m = _BARCODE_RE.search(decoded)
                if not m:
                    continue
                bc = m.group(1)
                if bc in seen_barcodes:
                    continue
                name = (img.get_attribute("alt") or "").strip()
                if not name:
                    continue
                if not name_matches(name, include_signals, hard_drop):
                    continue
                seen_barcodes.add(bc)
                candidates.append({"barcode": bc, "name": name, "identity_source": "yohananof_storefront_browse"})
                if len(candidates) >= max_products:
                    return candidates
            except Exception:
                pass

        if len(candidates) == before:
            stale_scrolls += 1
        else:
            stale_scrolls = 0
        if stale_scrolls >= stale_limit:
            print(f"  [yohananof] stopping: {stale_limit} consecutive scrolls with no new "
                  f"candidates (found {len(candidates)}, scroll {scroll_i}/{max_scrolls})")
            break

        clicked = _try_click_load_more(page)
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1400 if not clicked else 2000)
        if scroll_i % 10 == 0:
            print(f"  [yohananof] scroll {scroll_i}/{max_scrolls}, {len(candidates)} candidates so far")

    return candidates


def find_and_open_product(page, barcode: str, max_scrolls: int = 60) -> bool:
    """Scroll the category-search page until the product's image (matched by
    literal barcode substring in its src -- no decoding needed, EAN digits are
    never URL-escaped) appears, then click it to open the modal. Returns True if
    the modal opened."""
    locator = page.locator(f'img[src*="{barcode}"]').first
    for scroll_i in range(1, max_scrolls + 1):
        try:
            if locator.count() > 0:
                locator.scroll_into_view_if_needed(timeout=4000)
                page.wait_for_timeout(400)
                locator.click(force=True, timeout=4000)
                page.wait_for_timeout(2000)
                return page.locator('[role="dialog"]').count() > 0
        except Exception:
            pass
        _try_click_load_more(page)
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(900)
    return False


def scrape_product_panel(page, category_query: str, barcode: str, name: str) -> dict:
    """Navigate to the category search page, scroll-to-find the product image by
    barcode, click to open the modal, click each tab, capture per-tab dialog HTML,
    parse via the shared parser. (See module docstring -- direct openPopups= URL
    nav was tried and rejected; it only works for the initial unscrolled batch.)
    """
    url = SEARCH_URL.format(query=_q(category_query))
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        close_cookie_popup(page)
    except PlaywrightTimeoutError:
        return {"barcode": barcode, "name": name, "status": "nav_timeout"}

    opened = find_and_open_product(page, barcode)
    if not opened:
        return {"barcode": barcode, "name": name, "status": "not_found"}

    tab_html: dict[str, str] = {}
    for label in _TAB_LABELS:
        try:
            tab = page.get_by_role("tab", name=label).first
            if tab.count() == 0:
                tab_html[label] = ""
                continue
            tab.click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            dialog = page.locator('[role="dialog"]').first
            tab_html[label] = dialog.inner_html(timeout=4000)
        except Exception as e:
            tab_html[label] = ""
            print(f"    tab capture failed ({label}): {str(e)[:100]}")

    # Ingredients: read straight out of #simple-tabpanel-0 in the captured HTML.
    ingredients_raw = ""
    ingr_html = tab_html.get("רכיבים", "")
    if ingr_html:
        soup_i = BeautifulSoup(ingr_html, "html.parser")
        tab0 = soup_i.select_one("#simple-tabpanel-0")
        if tab0:
            ingredients_raw = tab0.get_text(" ", strip=True)

    # Nutrition: parse the nutrition-tab HTML via the shared auto-detect parser.
    nutrition_raw_source = {"rows": [], "selection": {"insufficient": True}}
    nutr_bare: dict[str, str] = {}
    nutr_html = tab_html.get("ערכים תזונתיים", "")
    if nutr_html:
        soup_n = BeautifulSoup(nutr_html, "html.parser")
        nutrition_raw_source = extract_nutrition_raw_auto(soup_n)
        nutr_bare = parse_nutrition_rows(nutrition_raw_source.get("rows", []))

    nutrition = {
        "energy_kcal_raw": nutr_bare.get("energy", ""),
        "protein_raw": nutr_bare.get("protein", ""),
        "carbs_raw": nutr_bare.get("carbs", ""),
        "fat_raw": nutr_bare.get("fat", ""),
        "fiber_raw": nutr_bare.get("fiber", ""),
        "sodium_raw": nutr_bare.get("sodium", ""),
        "sugar_raw": nutr_bare.get("sugar", ""),
        "saturated_fat_raw": nutr_bare.get("saturated_fat", ""),
    }

    status = "scraped" if (ingredients_raw or any(nutrition.values())) else "empty_panel"
    return {
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "barcode": barcode,
        "name_he": name,
        "status": status,
        "nutrition": nutrition,
        "nutrition_raw_source": nutrition_raw_source,
        "ingredients_raw": ingredients_raw,
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "provenance": {
            "identity_source": "yohananof_storefront_browse",
            "nutrition_source": "yohananof_storefront" if nutr_html else None,
            "ingredients_source": "yohananof_storefront" if ingr_html else None,
        },
    }


def acquire(
    include_signals: list[str],
    hard_drop: list[str],
    category: str,
    out_dir: Path,
    max_products: int = 30,
    headless: bool = True,
) -> tuple[list[dict], Path]:
    """Full discover -> scrape run for one Yohananof category query set."""
    out_dir.mkdir(parents=True, exist_ok=True)
    browse_query = include_signals[0] if include_signals else category
    run_report: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()

        candidates = discover_candidates(page, browse_query, include_signals, hard_drop, max_products)
        print(f"  [yohananof] discovered {len(candidates)} candidates")

        for i, cand in enumerate(candidates, 1):
            bc, name = cand["barcode"], cand["name"]
            print(f"  [{i}/{len(candidates)}] scraping {bc} | {name[:50]}")
            try:
                rec = scrape_product_panel(page, browse_query, bc, name)
            except Exception as e:
                rec = {"barcode": bc, "name": name, "status": "failed", "error": str(e)[:300]}
            run_report.append(rec)

        context.close()
        browser.close()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = out_dir / f"yohananof_bsip0_raw_{ts}.json"
    scraped_ok = [r for r in run_report if r.get("status") == "scraped"]
    out_data = {
        "schema_version": "bsip0_v1",
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "category": category,
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "candidates_total": len(candidates),
        "scraped_ok": len(scraped_ok),
        "empty_panel": sum(1 for r in run_report if r.get("status") == "empty_panel"),
        "not_found": sum(1 for r in run_report if r.get("status") == "not_found"),
        "failed": sum(1 for r in run_report if r.get("status") == "failed"),
        "products": run_report,
    }
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Wrote: {out_path}")
    return run_report, out_path
