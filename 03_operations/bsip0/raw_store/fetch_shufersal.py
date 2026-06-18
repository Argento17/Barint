"""
fetch_shufersal.py — Shufersal listing+PDP fetcher for BSIP0.5.

Reuses the existing shufersal scraper's request/session logic. Given a listing
config {category, listing_urls[]}, it:
  (a) enumerates listing pages -> product URLs + barcodes,
  (b) fetches each product page,
  (c) persists to the raw store.

NO parsing beyond what enumeration needs. Categories are config entries, not code.

Usage:
  python fetch_shufersal.py <category_name>
  python fetch_shufersal.py yogurt

Config is defined in LISTING_CONFIGS below. Pass '--dry-run' to only enumerate
without fetching PDPs.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}
PAGE_SIZE = 48
FETCH_DELAY = 1.5
MAX_PAGES_PER_QUERY = 3

STORE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STORE_DIR))
from store import store_page  # noqa: E402

# ── Listing configs (categories are config entries, not code) ────────────
LISTING_CONFIGS: dict[str, dict] = {
    "yogurt": {
        "category": "yogurt",
        "retailer": "shufersal",
        "search_queries": [
            "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8",
            "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05d9\u05d5\u05d5\u05e0\u05d9",
            "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05d1\u05d9\u05d5",
            "\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d4",
            "\u05d9\u05d5\u05e4\u05dc\u05d4",
            "\u05d3\u05e0\u05d5\u05e0\u05d4",
            "\u05de\u05d5\u05dc\u05e8",
            "\u05e1\u05e7\u05d9\u05e8",
            "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05e4\u05e8\u05d5",
        ],
        "category_urls": [
            f"{BASE}/online/he/c/A4001?pageSize={PAGE_SIZE}",
            f"{BASE}/online/he/c/A4003?pageSize={PAGE_SIZE}",
        ],
    },
    "brined_cheeses": {
        "category": "brined_cheeses",
        "retailer": "shufersal",
        "search_queries": [
            # Primary shelf types (Hebrew)
            "\u05d2\u05d1\u05d9\u05e0\u05d4 \u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea",  # \u05d2\u05d1\u05d9\u05e0\u05d4 \u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea
            "\u05d2\u05d1\u05d9\u05e0\u05ea \u05e4\u05d8\u05d4",                           # \u05d2\u05d1\u05d9\u05e0\u05ea \u05e4\u05d8\u05d4
            "\u05d2\u05d1\u05d9\u05e0\u05d4 \u05e6\u05e4\u05ea\u05d9\u05ea",               # \u05d2\u05d1\u05d9\u05e0\u05d4 \u05e6\u05e4\u05ea\u05d9\u05ea
            "\u05d2\u05d1\u05d9\u05e0\u05d4 \u05de\u05dc\u05d5\u05d7\u05d4",              # \u05d2\u05d1\u05d9\u05e0\u05d4 \u05de\u05dc\u05d5\u05d7\u05d4
            "\u05d7\u05dc\u05d5\u05de\u05d9",                                               # \u05d7\u05dc\u05d5\u05de\u05d9
            "\u05e8\u05d9\u05e7\u05d5\u05d8\u05d4",                                        # \u05e8\u05d9\u05e7\u05d5\u05d8\u05d4
            # Fat-tier variants
            "\u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 5%",                               # \u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 5%
            "\u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 16%",                              # \u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 16%
            "\u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 24%",                              # \u05d1\u05d5\u05dc\u05d2\u05e8\u05d9\u05ea 24%
            "\u05e4\u05d8\u05d4 5%",                                                        # \u05e4\u05d8\u05d4 5%
            "\u05e4\u05d8\u05d4 16%",                                                       # \u05e4\u05d8\u05d4 16%
        ],
        "category_urls": [
            f"{BASE}/online/he/c/A06?pageSize={PAGE_SIZE}",
            f"{BASE}/online/he/c/A0601?pageSize={PAGE_SIZE}",
        ],
    },
}


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    signals = ["maintenance", "\u05d0\u05ea\u05e8 \u05d1\u05ea\u05d7\u05d6\u05d5\u05e7\u05d4", "\u05d1\u05ea\u05d7\u05d6\u05d5\u05e7\u05d4"]
    return len(text) < 5000 and any(s in text.lower() for s in signals)


def _extract_listing_items(html: str) -> list[dict]:
    """Extract product code + name from a listing page. Minimal parse — just enough for enumeration."""
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    results = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        results.append({
            "name": name,
            "code": code,
        })
    return results


def _search_page(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _extract_listing_items(r.text)


def _category_page(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _extract_listing_items(r.text)


def _fetch_pdp_persist(code: str, name: str, category: str, retailer: str, config: dict) -> dict | None:
    """Fetch a single PDP and persist to raw store. Returns store entry or None."""
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        print(f"  PDP FAIL {code}: HTTP {r.status_code if r else 'error'}", flush=True)
        return None

    # Extract barcode from JSON-LD for the barcode_hint
    barcode_hint = code
    try:
        soup = BeautifulSoup(r.text, "html.parser")
        for script in soup.find_all("script", type="application/ld+json"):
            if script.string:
                ld = json.loads(script.string)
                if ld.get("@type") == "Product":
                    barcode_hint = ld.get("gtin13", ld.get("sku", code))
                    break
    except Exception:
        pass

    entry = store_page(
        content=r.content,
        retailer=retailer,
        category=category,
        page_id=code,
        url=r.url,
        barcode_hint=barcode_hint or code,
        http_status=r.status_code,
        fetch_engine="requests",
    )
    print(f"  STORED {code} ({barcode_hint})", flush=True)
    return entry


def run_listing_enumeration(config: dict) -> tuple[list[dict], list[str]]:
    """Phase A: enumerate listing pages -> list of {code, name} dicts. Returns (products, notes)."""
    retailer = config["retailer"]
    category = config["category"]
    seen_codes: dict[str, dict] = {}
    notes: list[str] = []

    def log(msg: str):
        print(msg, flush=True)
        notes.append(msg)

    log(f"=== Phase A: Search queries ({category}/{retailer}) ===")
    for query in config.get("search_queries", []):
        for page in range(MAX_PAGES_PER_QUERY):
            items = _search_page(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code not in seen_codes:
                    seen_codes[code] = item
                    new_page += 1
            log(f"  '{query}' page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            time.sleep(FETCH_DELAY)

    log(f"\n=== Phase A: Category browsing ({len(seen_codes)} so far) ===")
    for cat_url in config.get("category_urls", []):
        for page in range(MAX_PAGES_PER_QUERY):
            items = _category_page(cat_url, page)
            if not items:
                log(f"  cat page {page}: no results")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code not in seen_codes:
                    seen_codes[code] = item
                    new_page += 1
            log(f"  cat page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            time.sleep(FETCH_DELAY)

    log(f"\nTotal unique product codes: {len(seen_codes)}")
    return list(seen_codes.values()), notes


def run_pdp_fetch(products: list[dict], config: dict, dry_run: bool = False) -> list[str]:
    """Phase B: fetch each PDP and persist to raw store. Returns notes."""
    retailer = config["retailer"]
    category = config["category"]
    notes: list[str] = []

    def log(msg: str):
        print(msg, flush=True)
        notes.append(msg)

    log(f"\n=== Phase B: PDP fetch ({len(products)} products) ===")
    if dry_run:
        log("  DRY RUN — not fetching PDPs")
        return notes

    stored = 0
    failed = 0
    for i, prod in enumerate(products):
        code = prod["code"]
        entry = _fetch_pdp_persist(code, prod.get("name", ""), category, retailer, config)
        if entry:
            stored += 1
        else:
            failed += 1
        if i % 10 == 9 and i > 0:
            log(f"  [{i+1}/{len(products)}] {stored} stored, {failed} failed")
        time.sleep(FETCH_DELAY)

    log(f"Phase B done: {stored} stored, {failed} failed")
    return notes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_shufersal.py <category> [--dry-run]")
        print(f"Available categories: {', '.join(LISTING_CONFIGS.keys())}")
        sys.exit(1)

    cat_name = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    if cat_name not in LISTING_CONFIGS:
        print(f"Unknown category '{cat_name}'. Available: {', '.join(LISTING_CONFIGS.keys())}")
        sys.exit(1)

    config = LISTING_CONFIGS[cat_name]

    # Phase A: enumerate
    products, notes_a = run_listing_enumeration(config)

    # Phase B: fetch PDPs
    notes_b = run_pdp_fetch(products, config, dry_run=dry_run)

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Category: {cat_name}")
    print(f"Products enumerated: {len(products)}")
    print(f"Dry run: {dry_run}")
    print(f"Notes: {len(notes_a) + len(notes_b)} lines")

    from store import page_count
    total = page_count(config["retailer"], config["category"])
    print(f"Pages in store: {total}")


if __name__ == "__main__":
    main()
