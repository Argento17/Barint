#!/usr/bin/env python3
"""
probe_yohananof.py — GO/NO-GO test for Yohananof access via Playwright.

Self-contained. Dependencies: playwright (installs chromium).
Usage: python3 probe_yohananof.py

Opens 2 search/listing pages + 3 product pages via headless Chromium.
Reports per-URL: HTTP status (via CDP), page bytes, anti-bot markers,
                  whether product data tabs (ingredients/nutrition) are clickable.
Verdict: CLEAN / DEGRADED / BLOCKED
"""

import sys
import re
import time

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    print("ERROR: 'playwright' not installed.")
    print("  pip3 install playwright && playwright install chromium")
    sys.exit(1)

# --- Configuration ---
BASE = "https://www.yochananof.co.il"

SEARCH_QUERIES = [
    "יוגורט",
    "יוגורט יווני",
]

PRODUCT_SEARCH_TERMS = [
    "7290008316037",   # Tnuva yogurt — search by barcode
    "7290014972572",   # Strauss Danone — search by barcode
    "יוגורט טבעי",     # generic search term
]

HEADLESS = True
VIEWPORT = {"width": 1280, "height": 900}
TIMEOUT = 20000  # ms
DELAY = 2.0  # seconds between pages

LOCALE = "he-IL"
TIMEZONE = "Asia/Jerusalem"

EXTRA_HEADERS = {
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
}

results = []


def close_cookie_popup(page):
    """Dismiss Yohananof cookie consent popup if present."""
    try:
        # Try common cookie button selectors
        for sel in [
            "button:has-text('אשר')",
            "button:has-text('אישור')",
            "button:has-text('המשך')",
            "button:has-text('Accept')",
            "#cookies_accept",
            "[data-testid='cookie-accept']",
            ".cookie-accept",
        ]:
            btn = page.query_selector(sel)
            if btn:
                btn.click(timeout=3000)
                time.sleep(0.3)
                return True
    except Exception:
        pass
    return False


def get_page_text(page):
    """Get page text content, handling possible detached elements."""
    try:
        return page.inner_text("body")
    except Exception:
        try:
            return page.content()
        except Exception:
            return ""


def check_anti_bot(page, text):
    signals = []
    if not text:
        signals.append("empty_body")
        return signals
    lower = text.lower()
    if "just a moment" in lower or "enable javascript" in lower:
        signals.append("cf_challenge")
    if "access denied" in lower or "blocked" in lower:
        signals.append("access_denied")
    if "verify you are human" in lower or "captcha" in lower:
        signals.append("captcha")
    if "404" in text and "not found" in lower:
        signals.append("not_found")
    if len(text) < 300 and not ("html" in text.lower() or "<" in text):
        signals.append("empty_or_js_shell")
    # Check for blocked-by-IP markers
    if "your ip" in lower and ("block" in lower or "denied" in lower or "suspicious" in lower):
        signals.append("ip_block")
    return signals


def extract_barcodes_from_page(page, text):
    """Extract barcodes from Yohananof page using CDN URL patterns."""
    barcodes = set()
    # CDN image URL pattern: gs1-products/1470/medium/<EAN>-<ID>/
    # Also direct: gs1-products/<EAN>/
    html = page.content()
    for m in re.finditer(r'gs1-products[^"\']*?(\d{13})', html):
        barcodes.add(m.group(1))
    # data attributes
    for m in re.finditer(r'data-ean[=}]["\']?(\d{13})', html):
        barcodes.add(m.group(1))
    for m in re.finditer(r'data-barcode[=}]["\']?(\d{13})', html):
        barcodes.add(m.group(1))
    return sorted(barcodes)


def probe_listing(page, label, url):
    print(f"\n  [{label}] {url}")
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
        page.wait_for_timeout(2000)  # extra wait for dynamic content
    except PwTimeout:
        results.append({"label": label, "url": url, "status": "TIMEOUT"})
        print("  → TIMEOUT")
        return
    except Exception as e:
        results.append({"label": label, "url": url, "status": "ERROR", "error": str(e)})
        print(f"  → ERROR: {e}")
        return

    close_cookie_popup(page)
    page.wait_for_timeout(500)

    text = get_page_text(page)
    status = resp.status if resp else 0
    signals = check_anti_bot(page, text)
    barcodes = extract_barcodes_from_page(page, text)
    body_len = len(text)

    result = {
        "label": label,
        "url": url,
        "status": status,
        "bytes": body_len,
        "anti_bot_signals": signals,
        "barcodes_found": barcodes,
    }
    results.append(result)

    print(f"  → HTTP {status} | {body_len:,} chars | page title: {page.title()[:60]}")
    if signals:
        print(f"  ⚠ Anti-bot: {', '.join(signals)}")
    # Check for product card grid on listing pages
    cards = page.query_selector_all("[class*='product'], [class*='card'], [class*='item']")
    product_cards = [c for c in cards if c.inner_text().strip()]
    if product_cards:
        print(f"  ✓ ~{len(product_cards)} product cards visible")
    if barcodes:
        print(f"  ✓ Barcodes: {', '.join(barcodes[:5])}" +
              (f" ... (+{len(barcodes)-5} more)" if len(barcodes) > 5 else ""))


def probe_product(page, label, search_term):
    """Search for a product and check if detail tabs are accessible."""
    search_url = f"{BASE}/?s={search_term}"
    print(f"\n  [{label}] search: {search_term}")
    try:
        resp = page.goto(search_url, wait_until="domcontentloaded", timeout=TIMEOUT)
        page.wait_for_timeout(2000)
    except PwTimeout:
        results.append({"label": label, "url": search_url, "status": "TIMEOUT"})
        print("  → TIMEOUT on search")
        return

    close_cookie_popup(page)
    page.wait_for_timeout(500)

    text = get_page_text(page)
    status = resp.status if resp else 0
    signals = check_anti_bot(page, text)
    barcodes = extract_barcodes_from_page(page, text)
    body_len = len(text)

    # Check if we can see ingredient/nutrition tabs or a "detail" button
    tab_found = False
    tab_selectors = [
        "button:has-text('רכיבים')",
        "button:has-text('ערכים')",
        "button:has-text('תזונתיים')",
        "button:has-text('אלרגנים')",
        "button:has-text('מידע')",
        "[class*='tab']:has-text('רכיבים')",
        "[class*='tab']:has-text('ערכים')",
        "[class*='nutrition']",
        "[class*='ingredients']",
    ]
    for sel in tab_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                tab_found = True
                break
        except Exception:
            pass

    result = {
        "label": label,
        "url": search_url,
        "status": status,
        "bytes": body_len,
        "anti_bot_signals": signals,
        "barcodes_found": barcodes,
        "tabs_accessible": tab_found,
    }
    results.append(result)

    print(f"  → HTTP {status} | {body_len:,} chars | tabs: {'✓' if tab_found else '–'}")
    if signals:
        print(f"  ⚠ Anti-bot: {', '.join(signals)}")
    if barcodes:
        print(f"  ✓ Barcodes: {', '.join(barcodes[:5])}" +
              (f" ... (+{len(barcodes)-5} more)" if len(barcodes) > 5 else ""))
    if tab_found:
        print(f"  ✓ Product detail tabs visible (ingredients/nutrition)")


def verdict(results):
    if not results:
        return "BLOCKED — no results (browser launch failure?)"
    errors = [r for r in results if r.get("status") in ("TIMEOUT", "ERROR")]
    non_200 = [r for r in results if isinstance(r.get("status"), int) and r["status"] != 200]
    blocked_signals = [r for r in results if r.get("anti_bot_signals")]
    tab_found = [r for r in results if r.get("tabs_accessible")]

    evidence = []
    if errors:
        evidence.append(f"{len(errors)} timeouts/errors")
    if non_200:
        evidence.append(f"{len(non_200)} non-200: " +
                        ", ".join(str(r["status"]) for r in non_200))
    if blocked_signals:
        evidence.append(f"{len(blocked_signals)} pages with anti-bot signals")

    ok_count = len(results) - len(errors)
    ok_200 = len(results) - len(errors) - len(non_200)

    if ok_count == 0:
        v = "BLOCKED"
    elif ok_200 < len(results) * 0.6:
        v = "BLOCKED"
    elif blocked_signals:
        v = "DEGRADED"
    elif len(tab_found) == 0 and len(PRODUCT_SEARCH_TERMS) > 0:
        v = "DEGRADED"
    else:
        v = "CLEAN"

    evidence.append(
        f"{ok_count}/{len(results)} pages loaded, "
        f"{len(tab_found)}/{len(PRODUCT_SEARCH_TERMS)} with tabs"
    )
    return f"{v} — {'; '.join(evidence)}"


def main():
    print("=" * 60)
    print("Yohananof Connectivity Probe (Playwright)")
    print("=" * 60)
    print(f"Target: {BASE}")
    print(f"Headless: {HEADLESS}")
    print(f"Delay: {DELAY}s between pages\n")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            viewport=VIEWPORT,
            locale=LOCALE,
            timezone_id=TIMEZONE,
            extra_http_headers=EXTRA_HEADERS,
        )
        page = context.new_page()

        # --- Listing pages ---
        print("--- Listing pages ---")
        for i, q in enumerate(SEARCH_QUERIES):
            url = f"{BASE}/?s={q}"
            probe_listing(page, f"listing_{i+1}", url)
            time.sleep(DELAY)

        # --- Product pages (search then tab check) ---
        print("\n--- Product page access ---")
        for i, term in enumerate(PRODUCT_SEARCH_TERMS):
            probe_product(page, f"product_{i+1}", term)
            if i < len(PRODUCT_SEARCH_TERMS) - 1:
                time.sleep(DELAY)

        browser.close()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("RESULTS PER URL")
    print("=" * 60)
    for r in results:
        status_display = r.get("status", r.get("error", "?"))
        signals = r.get("anti_bot_signals", [])
        sig_str = f" ⚠{','.join(signals)}" if signals else ""
        barcode_str = f" [{len(r.get('barcodes_found', []))} barcodes]" if r.get("barcodes_found") else ""
        tab_str = " [tabs:✓]" if r.get("tabs_accessible") else ""
        print(f"  {r['label']:20s} HTTP {str(status_display):8s} {r.get('bytes', 0):>8,} chars{barcode_str}{tab_str}{sig_str}")

    v = verdict(results)
    print("\n" + "=" * 60)
    print(f"VERDICT: {v}")
    print("=" * 60)


if __name__ == "__main__":
    main()
