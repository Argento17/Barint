"""
fetch_yohananof.py — Yohananof Playwright storefront scraper, BSIP0.5-conformant.

Fetch-only: no nutrition/ingredient parsing. Uses store.store_page() for persistence.
Two phases:
  (a) Playwright navigation + aggressive scrolling to enumerate product cards,
  (b) click each card → capture modal dialog HTML + screenshot → persist.

Usage:
    python fetch_yohananof.py              # defaults: category=yogurts
    python fetch_yohananof.py <category>   # uses built-in listing for category
    python fetch_yohananof.py <category> <url1> [url2...]  # custom listing URLs

Config: LISTING_CONFIGS maps category names to listing URLs.
Override category via first CLI arg; override all URLs via subsequent args.

VM:
    PLAYWRIGHT_BROWSERS_PATH=/opt/bari/playwright-browsers
    python = /opt/bari/venv/bin/python3
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RETAILER = "yohananof"
BASE_HOST = "https://yochananof.co.il"

STORE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STORE_DIR))
from store import store_page

# ---------------------------------------------------------------------------
# Listing configs — categories are config entries
# ---------------------------------------------------------------------------

LISTING_CONFIGS: dict[str, dict] = {
    "yogurts": {
        "category": "yogurts",
        "retailer": RETAILER,
        "listing_urls": [
            f"{BASE_HOST}/category?search={quote(q)}"
            for q in [
                "יוגורט", "יוגורט יווני", "יוגורט 3%",
                "יוגורט 1.5%", "יוגורט 0%", "יוגורט טבעי",
                "יוגורט פירות", "יוגורט פרוביוטי",
                "לבן", "סקי", "אשל", "גביע", "יופלה",
                "מעדן חלב", "פודינג",
            ]
        ],
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")

def sha256_of(content):
    return hashlib.sha256(content).hexdigest()

def extract_barcode(text):
    match = re.search(r"(729\d{10}|\d{13})", str(text) or "")
    return match.group(1) if match else ""

def close_cookie_popup(page):
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            button = page.get_by_text(text, exact=False).first
            if button.is_visible(timeout=800):
                button.click(force=True)
                page.wait_for_timeout(800)
                return
        except Exception:
            pass

def close_dialog(page):
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass

def mark_product_cards(page):
    """JS evaluation: walk DOM from img elements, score by price/weight/keywords."""
    return page.evaluate("""
    () => {
      const out = [];
      const seen = new Set();

      function visible(el) {
        const r = el.getBoundingClientRect();
        return r.width > 80 && r.height > 80 && r.bottom >= 0 && r.top <= window.innerHeight + 600;
      }

      function score(el) {
        const txt = (el.innerText || '').trim();
        if (!txt) return 0;
        let s = 0;
        if (txt.includes('\u20AA')) s += 3;
        if (txt.includes('\u05D2\u05E8') || txt.includes("\u05D2\u05E8'")) s += 2;
        if (txt.includes('\u05D9\u05D5\u05D2\u05D5\u05E8\u05D8') || txt.includes('\u05DC\u05D1\u05DF') || txt.includes('\u05D2\u05D1\u05D9\u05E2')) s += 3;
        if (el.querySelector('img')) s += 3;
        if (txt.length > 15 && txt.length < 1200) s += 1;
        return s;
      }

      for (const img of Array.from(document.querySelectorAll('img'))) {
        let el = img;
        let best = null;
        let bestScore = 0;

        for (let depth = 0; depth < 12 && el; depth++) {
          const s = score(el);
          if (s > bestScore) {
            best = el;
            bestScore = s;
          }
          el = el.parentElement;
        }

        if (!best || bestScore < 5 || !visible(best) || seen.has(best)) continue;
        seen.add(best);

        const imgEl = best.querySelector('img');
        const src = imgEl ? (imgEl.currentSrc || imgEl.src || '') : '';
        const srcset = imgEl ? (imgEl.getAttribute('srcset') || '') : '';
        const alt = imgEl ? (imgEl.getAttribute('alt') || '') : '';
        const text = (best.innerText || '').trim();

        out.push({
          card_text: text,
          image_alt: alt,
          image_url_raw: (src + ' ' + srcset).trim()
        });
      }

      return out;
    }
    """)

def choose_best_name(card_text, image_alt):
    lines = [clean(x) for x in clean(card_text).split("\n") if clean(x)]
    bad = ["\u20AA", "\u05D4\u05D5\u05E1\u05E3", "\u05E9\u05DE\u05D9\u05E8\u05D4",
           "\u05DE\u05D1\u05E6\u05E2", "\u05DC\u05E8\u05E9\u05D9\u05DE\u05D4",
           "\u05DE\u05D7\u05D9\u05E8", "\u05D9\u05D7' \u05D1"]
    candidates = [line for line in lines if len(line) >= 4 and not any(b in line for b in bad)]
    for line in candidates:
        if any(kw in line for kw in ["יוגורט", "לבן", "גביע", "סקי", "אשל"]):
            return line
    if candidates:
        return candidates[0]
    return clean(image_alt)

def is_modal_open(page):
    try:
        dialog = page.locator('[role="dialog"]').first
        return dialog.count() > 0
    except Exception:
        return False

def modal_html(page):
    try:
        dialog = page.locator('[role="dialog"]').first
        if dialog.count() > 0:
            return dialog.inner_html(timeout=5000)
    except Exception:
        pass
    return ""

# ---------------------------------------------------------------------------
# Phase A: Discover products from listing URLs
# ---------------------------------------------------------------------------

def discover_listing(page, url):
    """Navigate to listing, scroll aggressively, return unique product candidates."""
    print(f"\n  Listing: {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    products = {}
    stable_rounds = 0
    last_count = 0

    for round_no in range(1, 141):
        raw_cards = mark_product_cards(page)

        for c in raw_cards:
            combined = clean(f"{c.get('card_text','')} {c.get('image_alt','')} {c.get('image_url_raw','')}")
            barcode = extract_barcode(combined)
            name = choose_best_name(c.get("card_text", ""), c.get("image_alt", ""))
            if not name:
                continue

            key = barcode or name
            if key and key not in products:
                products[key] = {
                    "key": key,
                    "barcode": barcode,
                    "name": name,
                    "query": url,
                    "card_text": c.get("card_text", ""),
                    "image_alt": c.get("image_alt", ""),
                    "image_url_raw": c.get("image_url_raw", ""),
                }

        current_count = len(products)
        if current_count == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_count = current_count

        if stable_rounds >= 20:
            break

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(900)

        if round_no % 20 == 0:
            print(f"    Scroll round {round_no}: {current_count} products")

    return list(products.values())

# ---------------------------------------------------------------------------
# Phase B: Fetch product modal for each discovered product
# ---------------------------------------------------------------------------

def fetch_product_modal(page, product, category):
    """
    Open product card → capture modal dialog HTML + screenshot → persist.
    Returns store entry or None.
    """
    barcode = product.get("barcode", "")
    name = product.get("name", "")
    page_id = barcode or f"no_bc_{uuid.uuid4().hex[:12]}"

    # Navigate to search for this product
    url = f"{BASE_HOST}/category?search={quote(name[:25])}"
    print(f"\n    Fetching: {page_id} | {name}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    # Strategies to find and click the card
    barcode_locator = page.locator(f'img[src*="{barcode}"], img[srcset*="{barcode}"]').first if barcode else None
    name_locator = page.get_by_text(name, exact=False).first

    found = False
    for i in range(1, 61):
        if barcode_locator:
            try:
                if barcode_locator.count() > 0:
                    barcode_locator.scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(700)
                    barcode_locator.click(force=True)
                    page.wait_for_timeout(4500)
                    if is_modal_open(page):
                        found = True
                        break
            except Exception:
                pass

        try:
            if name_locator.count() > 0:
                name_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4500)
                if is_modal_open(page):
                    found = True
                    break
        except Exception:
            pass

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

        if not found and barcode_locator:
            try:
                if barcode_locator.count() > 0:
                    barcode_locator.scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(700)
                    barcode_locator.click(force=True)
                    page.wait_for_timeout(4500)
                    if is_modal_open(page):
                        found = True
                        break
            except Exception:
                pass

    if not found:
        print(f"    WARN: could not open modal for {page_id}")
        close_dialog(page)
        return None

    # Capture modal HTML
    html_content = modal_html(page)
    html_bytes = html_content.encode("utf-8") if html_content else b""

    # Persist HTML via store_page
    entry = store_page(
        content=html_bytes,
        retailer=RETAILER,
        category=category,
        page_id=page_id,
        url=url,
        barcode_hint=barcode,
        http_status=200 if html_bytes else 0,
        fetch_engine="playwright",
    )

    # Persist screenshot alongside the HTML
    if html_bytes:
        pdir = STORE_DIR / RETAILER / category / page_id
        pdir.mkdir(parents=True, exist_ok=True)
        try:
            sname = f"{entry['fetch_ts']}.png"
            page.screenshot(path=str(pdir / sname), full_page=False)
        except Exception:
            pass

    print(f"    OK: stored page_id={page_id} barcode_hint={barcode or 'N/A'} bytes={len(html_bytes)}")
    close_dialog(page)
    return entry

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry-run"]

    if args:
        cat_name = args[0]
        if len(args) > 1:
            custom_urls = args[1:]
        else:
            custom_urls = None
    else:
        cat_name = "yogurts"
        custom_urls = None

    if cat_name not in LISTING_CONFIGS and custom_urls is None:
        print(f"Unknown category '{cat_name}'. Available: {', '.join(LISTING_CONFIGS.keys())}")
        print("Or pass listing URLs directly.")
        sys.exit(1)

    if custom_urls:
        config = {
            "category": cat_name,
            "retailer": RETAILER,
            "listing_urls": custom_urls,
        }
    else:
        config = LISTING_CONFIGS[cat_name]

    category = config["category"]
    listing_urls = config["listing_urls"]

    print(f"\n{'='*60}")
    print(f"  Yohananof Storefront Scraper (fetch-only)")
    print(f"  Retailer: {RETAILER}")
    print(f"  Category: {category}")
    print(f"  Listing URLs: {len(listing_urls)}")
    print(f"  Store root: {STORE_DIR}")
    print(f"{'='*60}")

    all_products = []
    seen_keys = set()
    total_listings = len(listing_urls)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        )
        page = ctx.new_page()

        # Phase A: Discover from all listing URLs
        print(f"\n{'='*60}")
        print(f"  Phase A: Product Discovery ({total_listings} listings)")
        print(f"{'='*60}")
        for idx, url in enumerate(listing_urls, 1):
            print(f"\n  [{idx}/{total_listings}]")
            try:
                products = discover_listing(page, url)
                for p in products:
                    key = p["key"]
                    if key and key not in seen_keys:
                        seen_keys.add(key)
                        all_products.append(p)
                print(f"  -> {len(products)} discovered ({len(all_products)} unique so far)")
            except Exception as e:
                print(f"  ERROR on listing: {e}")

            time.sleep(2.0)

        print(f"\n  Total unique products: {len(all_products)}")

        if not all_products:
            print("  No products discovered. Aborting.")
            browser.close()
            return

        if dry_run:
            print(f"\n  DRY RUN — skipping Phase B. {len(all_products)} candidates available.")
            browser.close()
            return

        # Phase B: Fetch each product modal
        print(f"\n{'='*60}")
        print(f"  Phase B: Product Modal Fetch ({len(all_products)} products)")
        print(f"{'='*60}")

        persisted = 0
        failed = 0
        for idx, product in enumerate(all_products, 1):
            barcode = product.get("barcode", "")
            name = product.get("name", "")
            print(f"\n  [{idx}/{len(all_products)}] bc={barcode or 'N/A'} name={name[:40]}")
            try:
                result = fetch_product_modal(page, product, category)
                if result:
                    persisted += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print(f"    FAILED: {e}")
                close_dialog(page)

            time.sleep(2.5)

        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}")
    print(f"  Retailer:   {RETAILER}")
    print(f"  Category:   {category}")
    print(f"  Listings:   {total_listings}")
    print(f"  Discovered: {len(all_products)} unique products")
    print(f"  Dry run:    {dry_run}")
    print(f"  Persisted:  {persisted}")
    print(f"  Failed:     {failed}")

    from store import page_count
    total = page_count(RETAILER, category)
    print(f"  Pages in store: {total}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
