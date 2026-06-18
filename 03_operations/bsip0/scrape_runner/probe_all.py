#!/usr/bin/env python3
"""
probe_all.py — Multi-retailer access probe from an Israeli DC IP.

Self-contained. Dependencies: requests, beautifulsoup4.
Usage: python3 probe_all.py

For each Israeli online grocer: fetch 2 listing + 3 product pages via HTTP.
Detect anti-bot blocks, JS-rendered shells, and barcode extractability.
Outputs a rollout table at the end.

Retailers tested (9):
  Shufersal, Yohananof, Victory, Carrefour, Rami Levy,
  Tiv Taam, Machsaney Hashuk, Hazi Hinam, Osher Ad
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

# ---------------------------------------------------------------------------
# Retailer definitions
# ---------------------------------------------------------------------------

RETAILERS = [
    {
        "id": "shufersal",
        "name": "Shufersal",
        "domain": "shufersal.co.il",
        "base": "https://www.shufersal.co.il",
        "search_url": "/online/he/search?q={q}",
        "product_url": "/online/he/A{barcode}",
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["7290008316037", "7290014972572", "7290008316051"],
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "TLS fingerprint gated; clearest via static HTTP+BS4 /online/he/p/{code} or /A{barcode}",
    },
    {
        "id": "yohananof",
        "name": "Yohananof",
        "domain": "yochananof.co.il",
        "base": "https://www.yochananof.co.il",
        "search_url": "/?s={q}",
        "product_url": None,  # products found via search, no direct URL
        "listing_queries": ["יוגורט", "גבינה לבנה"],
        "product_ids": ["7290008316037", "יוגורט טבעי", "7290014972572"],
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים", "רכיבים"],
        "notes": "MUI React SPA — needs Playwright for product detail modals",
    },
    {
        "id": "victory",
        "name": "Victory",
        "domain": "victoryonline.co.il",
        "base": "https://www.victoryonline.co.il",
        "search_url": "/category?search={q}",
        "product_url": "/?catalogProduct={id}",
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["1470"],  # internal catalog product ID
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "Same SaaS as Yohananof — Playwright needed for product modal tabs",
    },
    {
        "id": "carrefour",
        "name": "Carrefour IL",
        "domain": "carrefour.co.il",
        "base": "https://www.carrefour.co.il",
        "search_url": "/search?q={q}",
        "product_url": "/product/{barcode}",
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["7290008316037", "7290014972572", "7290008316051"],
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "F5 BIG-IP WAF — HTTP 403 pre-render",
    },
    {
        "id": "rami_levy",
        "name": "Rami Levy",
        "domain": "rami-levy.co.il",
        "base": "https://www.rami-levy.co.il",
        "search_url": "/he/online/market/search?q={q}",
        "product_url": "/he/online/market/product/{barcode}",
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["7290008316037", "7290014972572", "7290008316051"],
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "Cloudflare Bot Management — HTTP 403 hard block",
    },
    {
        "id": "tiv_taam",
        "name": "Tiv Taam",
        "domain": "tivtaam.co.il",
        "base": "https://www.tivtaam.co.il",
        "search_url": "/search?q={q}",
        "product_url": None,
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["יוגורט", "קוטג'", "גבינה"],
        "dom_markers": [],
        "notes": "F5 BIG-IP Advanced WAF — HTTP 403",
    },
    {
        "id": "machsaney_hashuk",
        "name": "Machsaney Hashuk",
        "domain": "mck.co.il",
        "base": "https://www.mck.co.il",
        "search_url": "/search?q={q}",
        "product_url": None,
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["יוגורט", "קוטג'", "גבינה"],
        "dom_markers": [],
        "notes": "F5 BIG-IP Advanced WAF — HTTP 403",
    },
    {
        "id": "hazi_hinam",
        "name": "Hazi Hinam",
        "domain": "shop.hazi-hinam.co.il",
        "base": "https://shop.hazi-hinam.co.il",
        "search_url": "/search?q={q}",
        "product_url": "/catalog/{id}",
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["10", "15", "20"],  # category IDs; products load client-side
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "Angular SPA — catalog + search render client-side; Playwright needed",
    },
    {
        "id": "osher_ad",
        "name": "Osher Ad",
        "domain": "osherad.co.il",
        "base": "https://www.osherad.co.il",
        "search_url": "/search?q={q}",
        "product_url": None,
        "listing_queries": ["יוגורט", "קוטג'"],
        "product_ids": ["יוגורט", "קוטג'", "גבינה"],
        "dom_markers": ["הוסף לסל", "ערכים תזונתיים"],
        "notes": "Status UNKNOWN — not previously probed",
    },
]

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

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

DELAY = 1.5
TIMEOUT = 30

session = requests.Session()
session.headers.update(HEADERS)

ANTI_BOT_PATTERNS = [
    ("cf_challenge", r"(Just a moment|Checking your browser|Cloudflare|attention required)"),
    ("maintenance_img", r"Maintenance1\.jpg"),
    ("maintenance_page", r"(מתחזק|under maintenance|coming soon)"),
    ("tls_fingerprint_block", r"error\\?.*img.*[Mm]aintenance"),
    ("f5_block", r"(The requested URL was rejected|F5 site:|Your support ID)"),
    ("access_denied", r"(Access Denied|access denied|blocked)"),
    ("captcha", r"(captcha|recaptcha|g-recaptcha)"),
    ("empty_body", r"^.{0,100}$"),
    ("js_shell", r"^.{0,2000}$"),  # matched after length check
]

JS_RENDERING_PATTERNS = [
    r"<script[^>]*src=[\"'](?:.*?chunk|.*?bundle|.*?main\.)",
    r"root[^>]*>(\s|\n)*</",
    r"<app-root|<app-shell|<router-outlet",
    r"ng-version|ng-app",
    r"react-root|__NEXT_DATA__",
    r"wp-includes/js",
]

# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------


def detect_anti_bot(text):
    """Return list of anti-bot signal names detected."""
    signals = set()
    if not text:
        return ["empty_body"]
    lower = text.lower()
    for name, pattern in ANTI_BOT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, lower, re.IGNORECASE):
            signals.add(name)
    # TLS fingerprint: 200 OK, tiny body with maintenance image
    if "maintenance_img" in signals and len(text) < 5000:
        signals.add("tls_fingerprint_block")
    # JS shell: short body with no meaningful content
    if len(text) < 2000 and "maintenance_img" not in signals:
        signals.add("js_shell")
    return sorted(signals)


def detect_rendering_type(text):
    """Classify as 'static', 'js_spa', or 'unknown'."""
    if not text:
        return "unknown"
    score = 0
    for pat in JS_RENDERING_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            score += 1
    if score >= 2:
        return "js_spa"
    if score == 1 and len(text) > 5000:
        return "js_spa"
    if len(text) < 3000 and "<html" not in text[:500].lower():
        return "unknown"
    return "static"


def extract_barcodes(soup, text, retailer_id):
    """Extract barcodes from page using retailer-specific patterns."""
    barcodes = set()
    # Universal: JSON-LD
    for script in soup.select("script[type='application/ld+json']"):
        try:
            data = json.loads(script.string)
            items = data if isinstance(data, list) else [data]
            for item in items:
                for key in ("gtin13", "gtin12", "gtin", "sku", "mpn"):
                    val = item.get(key)
                    if val:
                        barcodes.add(str(val).strip())
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
    # Universal: data attributes with product code / ean
    for attr in ("data-product-code", "data-code", "data-ean", "data-barcode", "data-sku"):
        for el in soup.select(f"[{attr}]"):
            val = el.get(attr, "")
            if re.match(r'\d{8,14}', val):
                barcodes.add(val)
    # Shufersal: /A{barcode} URLs
    for a in soup.select("a[href*='/A']"):
        m = re.search(r'/A(\d{13})', a.get("href", ""))
        if m:
            barcodes.add(m.group(1))
    # CDN patterns (Yohananof/Victory)
    for m in re.finditer(r'gs1-products[^"\'\\]*?(\d{13})', text):
        barcodes.add(m.group(1))
    # Shufersal JSON-LD in script tags we may miss
    for m in re.finditer(r'"gtin13"\s*:\s*"(\d{13})"', text):
        barcodes.add(m.group(1))
    # General: 13-digit number that looks like EAN-13
    for m in re.finditer(r'\b(\d{13})\b', text):
        barcodes.add(m.group(1))
    return sorted(barcodes)


# ---------------------------------------------------------------------------
# Per-retailer probe
# ---------------------------------------------------------------------------


def probe_retailer(ret):
    print(f"\n{'=' * 60}")
    print(f"  {ret['name']} ({ret['domain']})")
    print(f"{'=' * 60}")
    print(f"  {ret['notes']}")

    results = []
    base = ret["base"]

    # --- Listing pages ---
    for i, q in enumerate(ret["listing_queries"]):
        path = ret["search_url"].replace("{q}", requests.utils.quote(q))
        url = f"{base}{path}"
        label = f"listing_{i + 1}"
        print(f"\n  [{label}] GET {url}")
        try:
            resp = session.get(url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as e:
            print(f"  → ERROR: {e}")
            results.append({"label": label, "type": "listing", "status": f"ERROR: {e}",
                            "bytes": 0, "anti_bot": [], "rendering": "unknown",
                            "barcodes": []})
            continue

        text = resp.text
        soup = BeautifulSoup(text, "html.parser")
        signals = detect_anti_bot(text)
        rendering = detect_rendering_type(text)
        barcodes = extract_barcodes(soup, text, ret["id"])
        body_len = len(text)

        print(f"  → HTTP {resp.status_code} | {body_len:,} bytes | {resp.elapsed.total_seconds():.1f}s")
        if signals:
            print(f"  ⚠ Anti-bot: {', '.join(signals)}")
        print(f"  → Rendering: {rendering}")
        if barcodes:
            print(f"  ✓ {len(barcodes)} barcodes found (sample: {', '.join(barcodes[:3])})")

        results.append({"label": label, "type": "listing", "status": resp.status_code,
                        "bytes": body_len, "anti_bot": signals, "rendering": rendering,
                        "barcodes": barcodes})
        time.sleep(DELAY)

    # --- Product pages ---
    for i, pid in enumerate(ret["product_ids"]):
        if ret["product_url"]:
            path = ret["product_url"].replace("{barcode}", pid).replace("{id}", pid).replace("{q}", requests.utils.quote(pid))
            url = f"{base}{path}"
        else:
            # No direct product URL pattern — search by term
            path = ret["search_url"].replace("{q}", requests.utils.quote(pid))
            url = f"{base}{path}"

        label = f"product_{i + 1}"
        print(f"\n  [{label}] GET {url}")
        try:
            resp = session.get(url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as e:
            print(f"  → ERROR: {e}")
            results.append({"label": label, "type": "product", "status": f"ERROR: {e}",
                            "bytes": 0, "anti_bot": [], "rendering": "unknown",
                            "barcodes": []})
            continue

        text = resp.text
        soup = BeautifulSoup(text, "html.parser")
        signals = detect_anti_bot(text)
        rendering = detect_rendering_type(text)
        barcodes = extract_barcodes(soup, text, ret["id"])
        body_len = len(text)

        print(f"  → HTTP {resp.status_code} | {body_len:,} bytes | {resp.elapsed.total_seconds():.1f}s")
        if signals:
            print(f"  ⚠ Anti-bot: {', '.join(signals)}")
        # Check for dom_markers
        found_markers = [m for m in ret["dom_markers"] if m in text]
        if found_markers:
            print(f"  ✓ DOM markers: {', '.join(found_markers[:3])}")
        print(f"  → Rendering: {rendering}")
        if barcodes:
            print(f"  ✓ {len(barcodes)} barcodes found (sample: {', '.join(barcodes[:3])})")

        results.append({"label": label, "type": "product", "status": resp.status_code,
                        "bytes": body_len, "anti_bot": signals, "rendering": rendering,
                        "barcodes": barcodes})
        if i < len(ret["product_ids"]) - 1:
            time.sleep(DELAY)

    # --- Per-retailer verdict ---
    verdict = compute_verdict(ret, results)
    return {**ret, "results": results, "verdict": verdict}


def compute_verdict(ret, results):
    """Classify retailer as CLEAN / JS_ONLY / BLOCKED."""
    if not results:
        return "BLOCKED"

    # Count categories
    blocked_signal = any(r.get("anti_bot") for r in results)
    any_200 = any(isinstance(r.get("status"), int) and r["status"] == 200 for r in results)
    any_js = any(r.get("rendering") == "js_spa" for r in results)
    any_static = any(r.get("rendering") == "static" for r in results)
    any_barcode = any(r.get("barcodes") for r in results)
    all_403 = all(isinstance(r.get("status"), int) and r["status"] == 403 for r in results)
    all_blocked = all(r.get("anti_bot") for r in results) or all_403
    any_error = any(isinstance(r.get("status"), str) and "ERROR" in r["status"] for r in results)

    if all_blocked:
        return "BLOCKED"
    if any_error and not any_200:
        return "BLOCKED"
    if not any_200:
        return "BLOCKED"
    if any_js and not any_static:
        return "JS_ONLY"
    if any_static and any_barcode:
        return "CLEAN"
    if any_static:
        return "DEGRADED"
    return "DEGRADED"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 72)
    print("  Bari Probe v1 — Multi-Retailer Access Probe")
    print("  Israeli DC IP required for accurate results")
    print("  Usage: python3 probe_all.py")
    print("=" * 72)
    print(f"\nRetailers: {len(RETAILERS)}")
    print(f"Delay: {DELAY}s | Timeout: {TIMEOUT}s | Max ~5 pages/retailer\n")

    all_verdicts = []
    for ret in RETAILERS:
        result = probe_retailer(ret)
        all_verdicts.append(result)

    # --- Output table ---
    print("\n\n")
    print("=" * 105)
    print("  ROLLOUT MAP — Retailer | Reachable | Anti-bot signals | Rendering | Barcode-extractable | Verdict")
    print("=" * 105)

    for r in all_verdicts:
        reachable = "YES" if any(
            isinstance(p.get("status"), int) and p["status"] == 200
            for p in r["results"]
        ) else "NO"

        all_signals = set()
        for p in r["results"]:
            for s in p.get("anti_bot", []):
                all_signals.add(s)

        renderings = set(p.get("rendering", "") for p in r["results"])
        barcode_any = any(p.get("barcodes") for p in r["results"] if isinstance(p.get("status"), int) and p["status"] == 200)
        barcode_str = "YES" if barcode_any else ("N/A (blocked)" if r["verdict"] == "BLOCKED" else "NO")

        print(f"  {r['name']:20s} {reachable:10s} {str(', '.join(sorted(all_signals))[:30]):32s} "
              f"{str(', '.join(renderings)):20s} {barcode_str:22s} {r['verdict']}")

    print("=" * 105)
    print("\nKEY:")
    print("  CLEAN    — reachable via static HTTP, barcodes extractable → Phase 1 ready")
    print("  JS_ONLY  — page renders require Playwright → needs browser automation")
    print("  DEGRADED — partial access (some blocked or no barcodes) → investigate")
    print("  BLOCKED  — WAF/anti-bot blocks all requests → needs proxy/stealth")

    # --- Summary counts ---
    counts = {"CLEAN": 0, "JS_ONLY": 0, "DEGRADED": 0, "BLOCKED": 0}
    for r in all_verdicts:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    print(f"\nSUMMARY: {counts['CLEAN']} CLEAN, {counts['JS_ONLY']} JS_ONLY, "
          f"{counts['DEGRADED']} DEGRADED, {counts['BLOCKED']} BLOCKED")


if __name__ == "__main__":
    main()
