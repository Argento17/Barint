#!/usr/bin/env python3
"""
probe_v2.py — Render-based retailer access probe from Israeli DC IP.

Uses repo-mined real endpoints + headless Playwright to determine honest
access verdicts for all 9 Israeli grocery retailers.

Usage (on VM): bari-python probe_v2.py [--quick] [--no-screenshots]

Output: /opt/bari/probe_v2_output/
"""

import sys
import os
import re
import json
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Runtime config
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(os.environ.get("PROBE_V2_OUTPUT", "/opt/bari/probe_v2_output"))
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
QUICK_MODE = "--quick" in sys.argv
NO_SCREENSHOTS = "--no-screenshots" in sys.argv

# ---------------------------------------------------------------------------
# Imports with user-friendly errors
# ---------------------------------------------------------------------------

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip3 install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip3 install playwright && playwright install chromium")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Shared session
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

JSON_HEADERS = {**HEADERS, "Accept": "application/json, text/plain, */*"}
API_HEADERS = {**HEADERS, "Accept": "application/json",
               "Referer": "https://www.shufersal.co.il/online/he/"}

DELAY = 1.5
TIMEOUT = 30

session = requests.Session()
session.headers.update(HEADERS)

all_results = []  # global accumulator

# ---------------------------------------------------------------------------
# Anti-bot detection
# ---------------------------------------------------------------------------

ANTI_BOT_PATTERNS = [
    ("cf_challenge", r"(Just a moment|Checking your browser|Cloudflare|attention required)"),
    ("maintenance_img", r"Maintenance1\.jpg"),
    ("maintenance_page", r"(מתחזק|under maintenance|coming soon)"),
    ("tls_fingerprint_block", r"error\\?.*img.*[Mm]aintenance"),
    ("f5_block", r"(The requested URL was rejected|F5 site:|Your support ID)"),
    ("access_denied", r"(Access Denied|access denied|blocked)"),
    ("captcha", r"(captcha|recaptcha|g-recaptcha)"),
    ("ip_block", r"(your ip.*block|suspicious.*ip)"),
]

JS_RENDERING_PATTERNS = [
    r"<script[^>]*src=[\"'](?:.*?chunk|.*?bundle|.*?main\.)",
    r"root[^>]*>(\s|\n)*</",
    r"<app-root|<app-shell|<router-outlet",
    r"ng-version|ng-app",
    r"react-root|__NEXT_DATA__",
]


def detect_anti_bot(text):
    signals = set()
    if not text:
        return ["empty_body"]
    for name, pattern in ANTI_BOT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.add(name)
    if "maintenance_img" in signals and len(text) < 5000:
        signals.add("tls_fingerprint_block")
    return sorted(signals)


def detect_rendering_type(text):
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


def extract_barcodes_from_text(text):
    barcodes = set()
    for m in re.finditer(r'/A(\d{13})', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'gs1-products[^"\'\\]*?(\d{13})', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'"gtin13"\s*:\s*"(\d{13})"', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'data-ean[=}]["\']?(\d{13})', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'data-barcode[=}]["\']?(\d{13})', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'\b(729\d{10})\b', text):
        barcodes.add(m.group(1))
    return sorted(barcodes)


def extract_barcodes_from_json(text):
    barcodes = set()
    for m in re.finditer(r'"(?:gtin13|ean|barcode|productCode)"\s*:\s*"(\d{13})"', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'"(?:gtin13|ean|barcode|productCode)"\s*:\s*(\d{13})', text):
        barcodes.add(m.group(1))
    for m in re.finditer(r'\b(729\d{10})\b', text):
        barcodes.add(m.group(1))
    return sorted(barcodes)


# ---------------------------------------------------------------------------
# Probe methods
# ---------------------------------------------------------------------------


def probe_static(label, url):
    print(f"  [{label}] GET {url}")
    try:
        resp = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        duration = resp.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(f"  \u2192 ERROR: {e}")
        return {"label": label, "method": "static", "url": url,
                "status": "ERROR", "error": str(e), "bytes": 0,
                "anti_bot": [], "rendering": "unknown", "barcodes": []}
    text = resp.text
    signals = detect_anti_bot(text)
    rendering = detect_rendering_type(text)
    barcodes = extract_barcodes_from_text(text)
    body_len = len(text)
    print(f"  \u2192 HTTP {resp.status_code} | {body_len:,} bytes | {duration:.1f}s | "
          f"{'ANTI-BOT: ' + ', '.join(signals) if signals else 'no signals'} | {rendering}")
    if barcodes:
        print(f"  \u2713 {len(barcodes)} barcodes: {', '.join(barcodes[:5])}")
    return {"label": label, "method": "static", "url": url,
            "status": resp.status_code, "bytes": body_len,
            "duration_s": round(duration, 2),
            "anti_bot": signals, "rendering": rendering, "barcodes": barcodes}


def probe_api(label, url, headers=None):
    print(f"  [{label}] API {url}")
    h = headers or JSON_HEADERS
    try:
        resp = session.get(url, timeout=TIMEOUT, headers=h, allow_redirects=True)
        duration = resp.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(f"  \u2192 ERROR: {e}")
        return {"label": label, "method": "api", "url": url,
                "status": "ERROR", "error": str(e), "bytes": 0,
                "anti_bot": [], "valid_json": False, "product_count": 0, "barcodes": []}
    body_len = len(resp.text)
    valid_json = False
    product_count = 0
    try:
        data = resp.json()
        valid_json = True
        if isinstance(data, dict):
            for key in ("products", "results", "data", "items", "hits"):
                if key in data and isinstance(data[key], list):
                    product_count = len(data[key])
                    break
        elif isinstance(data, list):
            product_count = len(data)
    except (json.JSONDecodeError, ValueError):
        pass
    barcodes = extract_barcodes_from_json(resp.text) if valid_json else []
    signals = detect_anti_bot(resp.text)
    print(f"  \u2192 HTTP {resp.status_code} | {body_len:,} bytes | {duration:.1f}s | "
          f"JSON: {'yes' if valid_json else 'no'} | ~{product_count} products"
          f"{' | ANTI-BOT: ' + ', '.join(signals) if signals else ''}")
    if barcodes:
        print(f"  \u2713 {len(barcodes)} barcodes: {', '.join(barcodes[:5])}")
    return {"label": label, "method": "api", "url": url,
            "status": resp.status_code, "bytes": body_len,
            "duration_s": round(duration, 2),
            "anti_bot": signals, "valid_json": valid_json,
            "product_count": product_count, "barcodes": barcodes}


def probe_playwright_page(page, label, url, config=None):
    """Run a single Playwright page load using an existing browser page."""
    cfg = config or {}
    print(f"  [{label}] PW {url}")
    result = {"label": label, "method": "playwright", "url": url,
              "status": None, "bytes": 0, "anti_bot": [], "barcodes": [],
              "page_title": "", "product_cards": 0, "modal_tabs": False}
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(cfg.get("wait_after_load", 3000))
    except PwTimeout:
        result["status"] = "TIMEOUT"
        print(f"  \u2192 TIMEOUT")
        return result
    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)
        print(f"  \u2192 ERROR: {e}")
        return result
    http_status = resp.status if resp else 0
    result["status"] = http_status
    try:
        html = page.content()
    except Exception:
        html = ""
    try:
        text = page.inner_text("body")
    except Exception:
        text = html
    result["page_title"] = page.title()
    result["bytes"] = len(text)
    signals = detect_anti_bot(html)
    result["anti_bot"] = signals
    barcodes = extract_barcodes_from_text(html)
    result["barcodes"] = barcodes
    cards = page.query_selector_all(
        "[class*='product'], [class*='card'], [class*='item'], [class*='tile']")
    visible_cards = []
    for c in cards:
        try:
            t = c.inner_text()
            if t.strip():
                visible_cards.append(c)
        except Exception:
            pass
    result["product_cards"] = len(visible_cards)
    for sel in [
        "button:has-text('\u05e8\u05db\u05d9\u05d1\u05d9\u05dd')",
        "button:has-text('\u05e2\u05e8\u05db\u05d9\u05dd \u05ea\u05d6\u05d5\u05e0\u05ea\u05d9\u05d9\u05dd')",
        "button:has-text('\u05de\u05d9\u05d3\u05e2 \u05d0\u05dc\u05e8\u05d2\u05e0\u05d9')",
        "[class*='nutrition']",
        "[class*='ingredients']",
    ]:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                result["modal_tabs"] = True
                break
        except Exception:
            pass
    print(f"  \u2192 HTTP {http_status} | {len(text):,} chars | "
          f"title: {page.title()[:50]} | cards: {len(visible_cards)}"
          f"{' | ANTI-BOT: ' + ', '.join(signals) if signals else ''}")
    if barcodes:
        print(f"  \u2713 {len(barcodes)} barcodes: {', '.join(barcodes[:5])}")
    if result["modal_tabs"]:
        print(f"  \u2713 Product detail tabs visible")
    if not NO_SCREENSHOTS:
        safe = re.sub(r'[^a-z0-9]+', '_', label.lower())[:50]
        sp = SCREENSHOT_DIR / f"{ret_id}_{safe}.png"
        try:
            page.screenshot(path=str(sp), full_page=False)
            result["screenshot"] = str(sp)
        except Exception:
            pass
    return result


# ---------------------------------------------------------------------------
# Retailer definitions with real endpoints (from repo scrapers)
# ---------------------------------------------------------------------------

RETAILERS = [
    {
        "id": "shufersal",
        "name": "Shufersal",
        "note": "TLS-fingerprint gated; crawlee DefaultFingerprintGenerator unlocks; API endpoints may work",
        "popup_selectors": [
            "button:has-text('\u05d0\u05e9\u05e8')",
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
            "#onetrust-accept-btn-handler",
        ],
        "static_tests": [
            ("search_yogurt", "https://www.shufersal.co.il/online/he/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [
            ("occ_search", "https://www.shufersal.co.il/occ/v2/shufersal/products/search?query=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&fields=FULL&lang=he&curr=ILS&pageSize=5"),
            ("v2_search", "https://www.shufersal.co.il/online/he/api/v2/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&pageSize=5"),
        ],
        "pw_tests": [
            ("listing_yogurt", "https://www.shufersal.co.il/online/he/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
            ("product_A_barcode", "https://www.shufersal.co.il/online/he/A7290008316037", {"wait_after_load": 5000}),
            ("product_p_code", "https://www.shufersal.co.il/online/he/p/1344167", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "yohananof",
        "name": "Yohananof",
        "note": "Two hostnames: yohananof.co.il (user-corrected) vs yochananof.co.il (legacy scraper). Search via /category?search=",
        "popup_selectors": [
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
            "button:has-text('\u05de\u05e1\u05db\u05d9\u05dd')",
            "button:has-text('\u05d0\u05e9\u05e8')",
        ],
        "static_tests": [
            ("search_yohananof", "https://www.yohananof.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
            ("search_yochananof", "https://yochananof.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [],
        "pw_tests": [
            ("pw_yohananof", "https://www.yohananof.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 4000}),
            ("pw_yochananof", "https://yochananof.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 4000}),
        ],
    },
    {
        "id": "victory",
        "name": "Victory",
        "note": "Same SaaS as Yohananof. REST API at /api/products and /v2/retailers/1470/...",
        "popup_selectors": [
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
            "button:has-text('\u05de\u05e1\u05db\u05d9\u05dd')",
        ],
        "static_tests": [
            ("category_search", "https://www.victoryonline.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
            ("plain_search", "https://www.victoryonline.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [
            ("api_products", "https://www.victoryonline.co.il/api/products?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", JSON_HEADERS),
            ("v2_retailer_api", "https://www.victoryonline.co.il/v2/retailers/1470/branches/2930/products?appId=4&isSearch=true&languageId=1&query=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&size=5&from=0&filters=%7B%22must%22%3A%7B%22exists%22%3A%5B%22family.id%22%2C%22family.categoriesPaths.id%22%2C%22branch.regularPrice%22%5D%2C%22term%22%3A%7B%22branch.isActive%22%3Atrue%2C%22branch.isVisible%22%3Atrue%7D%7D%2C%22mustNot%22%3A%7B%22term%22%3A%7B%22branch.regularPrice%22%3A0%7D%7D%7D", API_HEADERS),
        ],
        "pw_tests": [
            ("search_listing", "https://www.victoryonline.co.il/category?search=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "carrefour",
        "name": "Carrefour IL",
        "note": "F5 BIG-IP WAF blocks storefront; /v2/retailers/1540 and /api/products/search may bypass",
        "popup_selectors": [
            "#onetrust-accept-btn-handler",
            "button:has-text('\u05d0\u05e0\u05d9 \u05de\u05e1\u05db\u05d9\u05dd')",
            "button:has-text('\u05e7\u05d1\u05dc')",
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
        ],
        "static_tests": [
            ("plain_search", "https://www.carrefour.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
            ("catalog_search", "https://www.carrefour.co.il/catalogsearch/result/?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [
            ("api_search", "https://www.carrefour.co.il/api/products/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&pageSize=5", JSON_HEADERS),
            ("v2_retailer_api", "https://www.carrefour.co.il/v2/retailers/1540/branches/3003/products?appId=4&isSearch=true&languageId=1&query=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&size=5&from=0&filters=%7B%22must%22%3A%7B%22exists%22%3A%5B%22family.id%22%2C%22family.categoriesPaths.id%22%2C%22branch.regularPrice%22%5D%2C%22term%22%3A%7B%22branch.isActive%22%3Atrue%2C%22branch.isVisible%22%3Atrue%7D%7D%2C%22mustNot%22%3A%7B%22term%22%3A%7B%22branch.regularPrice%22%3A0%7D%7D%7D", API_HEADERS),
        ],
        "pw_tests": [
            ("storefront_product", "https://www.carrefour.co.il/product/7290008316037", {"wait_after_load": 5000}),
            ("storefront_search", "https://www.carrefour.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "rami_levy",
        "name": "Rami Levy",
        "note": "Cloudflare Bot Management paid tier; /api/catalog/search may have different WAF rules",
        "popup_selectors": [
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
            "button:has-text('\u05d4\u05d1\u05e0\u05ea\u05d9')",
        ],
        "static_tests": [
            ("market_search", "https://www.rami-levy.co.il/he/online/market/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [
            ("catalog_api", "https://www.rami-levy.co.il/api/catalog/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98&store=331&page=1", JSON_HEADERS),
        ],
        "pw_tests": [
            ("market_search_pw", "https://www.rami-levy.co.il/he/online/market/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "tiv_taam",
        "name": "Tiv Taam",
        "note": "F5 BIG-IP Advanced WAF; /?s= search pattern",
        "popup_selectors": [],
        "static_tests": [
            ("search", "https://www.tivtaam.co.il/?s=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [],
        "pw_tests": [
            ("search_pw", "https://www.tivtaam.co.il/?s=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "machsaney_hashuk",
        "name": "Machsaney Hashuk",
        "note": "F5 BIG-IP Advanced WAF; /search?q= pattern",
        "popup_selectors": [],
        "static_tests": [
            ("search", "https://www.mck.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
        ],
        "api_tests": [],
        "pw_tests": [
            ("search_pw", "https://www.mck.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
        ],
    },
    {
        "id": "hazi_hinam",
        "name": "Hazi Hinam",
        "note": "Angular SPA; no WAF; /catalog/{id}/{slug} loads client-side",
        "popup_selectors": [
            "button:has-text('\u05e1\u05d2\u05d5\u05e8')",
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
            "button:has-text('\u05d4\u05d1\u05e0\u05ea\u05d9')",
            "[class*='cookie'] button",
        ],
        "static_tests": [
            ("homepage", "https://shop.hazi-hinam.co.il/"),
            ("dairy_catalog", "https://shop.hazi-hinam.co.il/catalog/78/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D"),
        ],
        "api_tests": [],
        "pw_tests": [
            ("homepage_pw", "https://shop.hazi-hinam.co.il/", {"wait_after_load": 5000}),
            ("dairy_catalog_pw", "https://shop.hazi-hinam.co.il/catalog/78/מוצרי-חלב-וביצים", {"wait_after_load": 6000}),
        ],
    },
    {
        "id": "osher_ad",
        "name": "Osher Ad",
        "note": "Status unknown; /search?q= gave 404 in v1",
        "popup_selectors": [
            "button:has-text('\u05d0\u05d9\u05e9\u05d5\u05e8')",
        ],
        "static_tests": [
            ("search", "https://www.osherad.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
            ("homepage", "https://www.osherad.co.il/"),
        ],
        "api_tests": [],
        "pw_tests": [
            ("search_pw", "https://www.osherad.co.il/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98", {"wait_after_load": 5000}),
            ("homepage_pw", "https://www.osherad.co.il/", {"wait_after_load": 5000}),
        ],
    },
]

# ---------------------------------------------------------------------------
# Verdict computation
# ---------------------------------------------------------------------------


def compute_verdict(retailer_id, retailer_results):
    static_r = [r for r in retailer_results if r["method"] == "static"]
    api_r = [r for r in retailer_results if r["method"] == "api"]
    pw_r = [r for r in retailer_results if r["method"] == "playwright"]

    any_static_ok = any(
        isinstance(r.get("status"), int) and r["status"] == 200
        and not r.get("anti_bot") for r in static_r)
    any_static_barcodes = any(
        r.get("barcodes") for r in static_r
        if isinstance(r.get("status"), int) and r["status"] == 200)

    any_api_ok = any(
        isinstance(r.get("status"), int) and r["status"] == 200
        and r.get("valid_json") for r in api_r)
    any_api_barcodes = any(
        r.get("barcodes") for r in api_r
        if isinstance(r.get("status"), int) and r["status"] == 200)

    any_pw_ok = any(
        isinstance(r.get("status"), int) and r["status"] == 200
        and not r.get("anti_bot") for r in pw_r)
    any_pw_barcodes = any(
        r.get("barcodes") for r in pw_r
        if isinstance(r.get("status"), int) and r["status"] == 200)

    if any_static_ok and any_static_barcodes:
        return "CLEAN", "static HTTP works with barcodes"
    if any_api_ok and any_api_barcodes:
        return "API_OK", f"REST API provides products"
    if any_pw_ok and any_pw_barcodes:
        return "JS_OK", "Playwright renders products with barcodes"
    if any_pw_ok:
        return "DEGRADED", "Playwright loads pages, no barcodes"
    if any_static_ok:
        return "DEGRADED", "static HTTP loads, no barcodes (JS shell)"
    return "BLOCKED", "all methods blocked by WAF/anti-bot"


# ---------------------------------------------------------------------------
# Per-retailer probe
# ---------------------------------------------------------------------------


ret_id = ""


def probe_retailer(ret):
    global ret_id
    ret_id = ret["id"]
    print(f"\n{'=' * 60}")
    print(f"  {ret['name']}")
    print(f"  {ret['note']}")
    print(f"{'=' * 60}")

    retailer_results = []

    # Static HTTP
    if ret["static_tests"]:
        print(f"\n  --- Static HTTP ---")
        for label, url in ret["static_tests"]:
            r = probe_static(label, url)
            retailer_results.append({"retailer": ret["id"], **r})
            all_results.append({"retailer": ret["id"], **r})
            time.sleep(DELAY)

    # REST API
    if ret["api_tests"]:
        print(f"\n  --- REST API ---")
        for item in ret["api_tests"]:
            label, url = item[0], item[1]
            headers = item[2] if len(item) > 2 else None
            r = probe_api(label, url, headers=headers)
            retailer_results.append({"retailer": ret["id"], **r})
            all_results.append({"retailer": ret["id"], **r})
            time.sleep(DELAY)

    # Playwright
    if ret["pw_tests"] and not QUICK_MODE:
        print(f"\n  --- Playwright ---")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                ctx = browser.new_context(
                    viewport={"width": 1280, "height": 900},
                    locale="he-IL",
                    timezone_id="Asia/Jerusalem",
                    extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
                )
                page = ctx.new_page()
                for i, item in enumerate(ret["pw_tests"]):
                    label, url = item[0], item[1]
                    config = item[2] if len(item) > 2 else {}
                    r = probe_playwright_page(page, label, url, config=config)
                    retailer_results.append({"retailer": ret["id"], **r})
                    all_results.append({"retailer": ret["id"], **r})
                    if i < len(ret["pw_tests"]) - 1:
                        time.sleep(DELAY)
                browser.close()
        except Exception as e:
            print(f"  \u2192 BROWSER LAUNCH ERROR: {e}")

    verdict_label, evidence = compute_verdict(ret["id"], retailer_results)
    print(f"\n  >> VERDICT: {verdict_label} ({evidence})")
    return {"retailer": ret["id"], "name": ret["name"],
            "verdict": verdict_label, "evidence": evidence}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 72)
    print("  Bari Probe v2 — Render-Based Retailer Access Probe")
    print("  Israeli DC IP required (VM: 45.93.95.32)")
    print(f"  Mode: {'quick (no Playwright)' if QUICK_MODE else 'full'}"
          f" | Screenshots: {'no' if NO_SCREENSHOTS else 'yes'}")
    print(f"  Output: {OUTPUT_DIR}")
    print("=" * 72)
    print(f"\nRetailers: {len(RETAILERS)} | Delay: {DELAY}s | Timeout: {TIMEOUT}s\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    all_verdicts = [probe_retailer(ret) for ret in RETAILERS]

    # Rollout map
    print("\n\n")
    print("=" * 120)
    print("  ROLLOUT MAP — Retailer | Static | API | PW | Barcodes | Verdict")
    print("=" * 120)
    for v in all_verdicts:
        rr = [r for r in all_results if r["retailer"] == v["retailer"]]
        s_ok = any(
            isinstance(r.get("status"), int) and r["status"] == 200
            and not r.get("anti_bot") and r["method"] == "static" for r in rr)
        s_lbl = "OK" if s_ok else "BLOCKED"
        a_ok = any(
            isinstance(r.get("status"), int) and r["status"] == 200
            and r.get("valid_json") for r in rr)
        a_lbl = "OK" if a_ok else "N/A" if not any(r["method"] == "api" for r in rr) else "BLOCKED"
        p_ok = any(
            isinstance(r.get("status"), int) and r["status"] == 200
            and not r.get("anti_bot") and r["method"] == "playwright" for r in rr)
        p_lbl = "OK" if p_ok else "N/A" if not any(r["method"] == "playwright" for r in rr) else "BLOCKED"
        b_any = any(r.get("barcodes") for r in rr if isinstance(r.get("status"), int) and r["status"] == 200)
        b_lbl = "YES" if b_any else "NO"
        print(f"  {v['name']:20s} {s_lbl:9s} {a_lbl:10s} {p_lbl:10s} {b_lbl:8s} {v['verdict']}")
    print("=" * 120)
    print("\nKEY: CLEAN=static OK+barcodes | API_OK=REST API works | JS_OK=Playwright works | BLOCKED=all blocked")

    counts = {}
    for v in all_verdicts:
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    print(f"\nCounts: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}")

    # Save JSON
    out = {
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "quick" if QUICK_MODE else "full",
        "screenshots": not NO_SCREENSHOTS,
        "verdicts": all_verdicts,
        "details": all_results,
    }
    jp = OUTPUT_DIR / "probe_v2_results.json"
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nResults: {jp}")

    has_degraded = any(v["verdict"] in ("DEGRADED", "BLOCKED") for v in all_verdicts)
    sys.exit(1 if has_degraded else 0)


if __name__ == "__main__":
    main()
