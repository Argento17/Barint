#!/usr/bin/env python3
"""
probe_shufersal.py — GO/NO-GO test for Shufersal access from an Israeli IP.

Self-contained. Dependencies: requests, beautifulsoup4 (stdlib fallback on bs4).
Usage: python3 probe_shufersal.py

Fetches 3 listing pages (search results) + 5 product pages.
Reports per-URL status, size, anti-bot markers, and whether barcodes are extractable.
Verdict: CLEAN / DEGRADED / BLOCKED
"""

import re
import sys
import time
import json

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: 'beautifulsoup4' not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)

# --- Configuration ---
BASE = "https://www.shufersal.co.il"

SEARCH_QUERIES = [
    "יוגורט",
    "יוגורט יווני",
    "גבינה לבנה",
]

PRODUCT_BARCODES = [
    "7290008316037",   # Tnuva yogurt nature
    "7290014972572",   # Strauss Danone
    "7290014494043",   # Tnuva Eshel
    "7290008316051",   # Tnuva yogurt 3%
    "7290014972595",   # Strauss Danone strawberry
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

DELAY = 2.0  # seconds between requests

session = requests.Session()
session.headers.update(HEADERS)

results = []


def check_anti_bot(text, url):
    """Return list of anti-bot signals detected in response body."""
    signals = []
    if not text:
        return ["empty_body"]
    lower = text.lower()
    if "maintenance" in lower and len(text) < 5000:
        signals.append("maintenance_page")
    if "just a moment" in lower or "enable javascript" in lower:
        signals.append("cf_challenge")
    if "verify you are human" in lower or "captcha" in lower:
        signals.append("captcha")
    if "access denied" in lower or "blocked" in lower:
        signals.append("access_denied")
    if re.search(r'src=["\'].*maintenance.*\.jpg', text, re.IGNORECASE):
        signals.append("maintenance_image")
    if len(text) < 1000 and not ("html" in lower or "<!" in text):
        signals.append("empty_or_js_shell")
    # Check for Shufersal's fake TLS-fingerprint maintenance page
    if "error\\" in text and "img" in text and len(text) < 3000:
        signals.append("tls_fingerprint_block")
    return signals


def extract_barcodes_bs4(soup, url):
    """Try to extract barcodes from the page using known Shufersal patterns."""
    barcodes = set()
    # JSON-LD
    for script in soup.select("script[type='application/ld+json']"):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                gtin = data.get("gtin13") or data.get("gtin12") or data.get("gtin")
                if gtin:
                    barcodes.add(str(gtin))
            elif isinstance(data, list):
                for item in data:
                    gtin = item.get("gtin13") or item.get("gtin12") or item.get("gtin")
                    if gtin:
                        barcodes.add(str(gtin))
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
    # data-product-code (Shufersal internal codes often embed barcode info)
    for el in soup.select("[data-product-code]"):
        code = el.get("data-product-code", "")
        if code:
            barcodes.add(f"code:{code}")
    # URL pattern /A{barcode}
    for a in soup.select("a[href*='/A']"):
        m = re.search(r'/A(\d{13})', a.get("href", ""))
        if m:
            barcodes.add(m.group(1))
    return sorted(barcodes)


def fetch_and_report(label, url):
    """Fetch a single URL and return a result dict."""
    print(f"\n  [{label}] GET {url}")
    try:
        resp = session.get(url, timeout=30)
        duration = resp.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        result = {
            "label": label,
            "url": url,
            "status": "ERROR",
            "error": str(e),
        }
        results.append(result)
        print(f"  → ERROR: {e}")
        return result

    body = resp.text
    soup = BeautifulSoup(body, "html.parser")
    signals = check_anti_bot(body, url)
    barcodes = extract_barcodes_bs4(soup, url)

    result = {
        "label": label,
        "url": url,
        "status": resp.status_code,
        "bytes": len(body),
        "duration_s": round(duration, 2),
        "anti_bot_signals": signals,
        "barcodes_found": barcodes,
    }
    results.append(result)

    print(f"  → HTTP {resp.status_code} | {len(body):,} bytes | {duration:.1f}s")
    if signals:
        print(f"  ⚠ Anti-bot: {', '.join(signals)}")
    if barcodes:
        print(f"  ✓ Barcodes: {', '.join(barcodes[:6])}" +
              (f" ... (+{len(barcodes)-6} more)" if len(barcodes) > 6 else ""))
    else:
        print(f"  – No barcodes extracted")
    return result


def verdict(results):
    """Evaluate overall result."""
    if not results:
        return "BLOCKED — no results (network unreachable?)"

    errors = [r for r in results if r.get("status") == "ERROR"]
    non_200 = [r for r in results if isinstance(r.get("status"), int) and r["status"] != 200]
    blocked_signals = [r for r in results if r.get("anti_bot_signals")]

    listing_results = [r for r in results if r["label"].startswith("listing")]
    product_results = [r for r in results if r["label"].startswith("product")]

    listing_ok = sum(1 for r in listing_results if r.get("status") == 200)
    product_ok = sum(1 for r in product_results if r.get("status") == 200)
    product_w_barcode = sum(1 for r in product_results
                            if r.get("barcodes_found"))

    evidence = []
    if errors:
        evidence.append(f"{len(errors)} connection errors")
    if non_200:
        evidence.append(f"{len(non_200)} non-200 responses: " +
                        ", ".join(str(r["status"]) for r in non_200))
    if blocked_signals:
        evidence.append(f"{len(blocked_signals)} pages with anti-bot signals")

    if listing_ok == 0 and product_ok == 0:
        v = "BLOCKED"
    elif listing_ok < len(listing_results) or product_ok < len(product_results):
        v = "DEGRADED"
    elif product_w_barcode < len(product_results):
        v = "DEGRADED"
    else:
        v = "CLEAN"

    evidence.append(
        f"listing: {listing_ok}/{len(listing_results)} OK, "
        f"product: {product_ok}/{len(product_results)} OK, "
        f"barcode-extractable: {product_w_barcode}/{len(product_results)}"
    )

    return f"{v} — {'; '.join(evidence)}"


def main():
    print("=" * 60)
    print("Shufersal Connectivity Probe")
    print("=" * 60)
    print(f"Target: {BASE}")
    print(f"User-Agent: {HEADERS['User-Agent'][:50]}...")
    print(f"Delay: {DELAY}s between requests\n")

    # --- Listing pages ---
    print("--- Listing pages (search) ---")
    for i, query in enumerate(SEARCH_QUERIES):
        url = f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
        fetch_and_report(f"listing_{i+1}", url)
        time.sleep(DELAY)

    # --- Product pages ---
    print("\n--- Product pages ---")
    for i, barcode in enumerate(PRODUCT_BARCODES):
        url = f"{BASE}/online/he/A{barcode}"
        fetch_and_report(f"product_{i+1}", url)
        if i < len(PRODUCT_BARCODES) - 1:
            time.sleep(DELAY)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("RESULTS PER URL")
    print("=" * 60)
    for r in results:
        status_display = r.get("status", r.get("error", "?"))
        signals = r.get("anti_bot_signals", [])
        sig_str = f" ⚠{','.join(signals)}" if signals else ""
        barcode_str = f" [{len(r.get('barcodes_found', []))} barcodes]" if r.get("barcodes_found") else " [no barcodes]"
        print(f"  {r['label']:20s} HTTP {str(status_display):8s} {r.get('bytes', 0):>8,} bytes{barcode_str}{sig_str}")

    v = verdict(results)
    print("\n" + "=" * 60)
    print(f"VERDICT: {v}")
    print("=" * 60)


if __name__ == "__main__":
    main()
