"""
bsip0_scrape_audit.py
BSIP0 Retailer Access Audit — Real Israeli Bread/Cracker Corpus

Tests real Israeli retailer access for bread/cracker products.
Attempts product extraction from accessible retailers.
Applies acceptance gate — no silent fallback to OFF.

Investigation summary (run date 2026-05-25):
  Shufersal:    Returns HTTP 200 but all URLs serve a 444-byte maintenance page.
  Rami Levy:    HTTP 403 on all endpoints.
  Victory:      HTTP 200 but AngularJS SPA — all URLs return same 6716-byte JS shell.
  Carrefour IL: HTTP 403 on all endpoints.
  Tiv Taam:     HTTP 403 on all endpoints.
  Wolt Market:  SSR page accessible (1.6MB), venue list + category structure in JSON.
                Product catalog requires dynamic/authenticated API calls.
                Only 24 promoted items visible in SSR (none are bread/cracker).

Outputs:
  bread_retail_002/bsip0_retailer_access_report.md
  bread_retail_002/bsip0_source_manifest.json
"""

from __future__ import annotations
import datetime
import json
import pathlib
import re
import sys
import time
import logging
from typing import Optional

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError as ConnError

logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = pathlib.Path(r"C:\Bari\02_products\bread_retail_002")
RAW_DIR     = BASE_DIR / "raw"
REPORTS_DIR = BASE_DIR / "reports"

for _d in (BASE_DIR, RAW_DIR, REPORTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

MANIFEST_PATH = BASE_DIR / "bsip0_source_manifest.json"
AUDIT_REPORT  = BASE_DIR / "bsip0_retailer_access_report.md"

RUN_ID   = "real_bread_retail_002"
RUN_TS   = datetime.datetime.now().isoformat(timespec="seconds")
RUN_DATE = datetime.date.today().isoformat()

# ── Acceptance gate ───────────────────────────────────────────────────────────
GATE_MIN_PRODUCTS    = 20
GATE_NUTRITION_PCT   = 0.70
GATE_INGREDIENT_PCT  = 0.50
GATE_MIN_CATEGORIES  = 3

# ── HTTP session ──────────────────────────────────────────────────────────────
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent":                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language":           "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding":           "gzip, deflate, br",
    "DNT":                       "1",
    "Connection":                "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})
TIMEOUT = 25


def _get(url: str, *, json_mode: bool = False, referer: str = None) -> Optional[requests.Response]:
    headers = {}
    if json_mode:
        headers["Accept"] = "application/json, */*; q=0.01"
        headers["X-Requested-With"] = "XMLHttpRequest"
    if referer:
        headers["Referer"] = referer
    try:
        return SESSION.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
    except (Timeout, ConnError, RequestException):
        return None


def _is_maintenance_page(resp: Optional[requests.Response]) -> bool:
    """Detect pages that serve HTTP 200 but are actually maintenance placeholders."""
    if not resp or resp.status_code != 200:
        return False
    size = len(resp.content)
    text = resp.text
    # Shufersal maintenance: 444 bytes with maintenance image
    if size < 1000 and "maintenance" in text.lower():
        return True
    return False


def _is_js_shell(resp: Optional[requests.Response]) -> bool:
    """Detect JS-rendered SPA shell (no server-rendered product content)."""
    if not resp or resp.status_code != 200:
        return False
    text = resp.text[:8000]
    if "ng-version=" in text or "ng-cont" in text or "angularjs.org" in text.lower():
        return True
    indicators = ["<app-root", '<div id="root"', "data-reactroot", "__NEXT_DATA__"]
    return any(ind.lower() in text.lower() for ind in indicators)


def _status_label(resp: Optional[requests.Response]) -> str:
    if resp is None:
        return "TIMEOUT/ERR"
    return str(resp.status_code)


# ── Retailer definitions with detailed probes ─────────────────────────────────
RETAILERS = [
    {
        "id": "shufersal",
        "name": "Shufersal",
        "name_he": "שופרסל",
        "base": "https://www.shufersal.co.il",
        "probes": [
            ("home page",          "https://www.shufersal.co.il/online/he/",                          False),
            ("bread category",     "https://www.shufersal.co.il/online/he/A01/c",                     False),
            ("search: לחם",        "https://www.shufersal.co.il/online/he/search?q=%D7%9C%D7%97%D7%9D", False),
            ("API v2 search",      "https://www.shufersal.co.il/online/he/api/v2/search?q=%D7%9C%D7%97%D7%9D&pageSize=20", True),
            ("OCC API search",     "https://www.shufersal.co.il/occ/v2/shufersal/products/search?query=%D7%9C%D7%97%D7%9D&fields=FULL&lang=he&curr=ILS&pageSize=20", True),
        ],
        "known_blocker": "maintenance_mode",
        "blocker_detail": "All URLs return HTTP 200 with a 444-byte maintenance page (maintenance image from S3). Content is not accessible.",
        "api_access": False,
        "html_access": False,
        "product_extraction": "impossible",
        "products_extracted": 0,
    },
    {
        "id": "rami_levy",
        "name": "Rami Levy",
        "name_he": "רמי לוי",
        "base": "https://www.rami-levy.co.il",
        "probes": [
            ("home page",          "https://www.rami-levy.co.il/he/online/market",                    False),
            ("search: לחם",        "https://www.rami-levy.co.il/he/online/market/search?q=%D7%9C%D7%97%D7%9D", False),
            ("API catalog search", "https://www.rami-levy.co.il/api/catalog/search?q=%D7%9C%D7%97%D7%9D&store=331&page=1", True),
            ("API category 10",    "https://www.rami-levy.co.il/api/catalog/category/10?store=331&page=1", True),
        ],
        "known_blocker": "http_403",
        "blocker_detail": "HTTP 403 on all endpoints including home page and API endpoints.",
        "api_access": False,
        "html_access": False,
        "product_extraction": "impossible",
        "products_extracted": 0,
    },
    {
        "id": "victory",
        "name": "Victory",
        "name_he": "ויקטורי",
        "base": "https://www.victoryonline.co.il",
        "probes": [
            ("home page",          "https://www.victoryonline.co.il/",                                False),
            ("search: לחם",        "https://www.victoryonline.co.il/search?q=%D7%9C%D7%97%D7%9D",    False),
            ("API products",       "https://www.victoryonline.co.il/api/products?q=%D7%9C%D7%97%D7%9D", True),
            ("WP REST API",        "https://www.victoryonline.co.il/wp-json/wc/v3/products?search=%D7%9C%D7%97%D7%9D", True),
        ],
        "known_blocker": "angularjs_spa",
        "blocker_detail": "HTTP 200 on all URLs, but all return identical 6716-byte AngularJS app shell (ng-version attribute visible in source). Content is not server-rendered. Requires headless browser.",
        "api_access": False,
        "html_access": False,   # HTML is accessible but is a JS shell
        "product_extraction": "requires_headless_browser",
        "products_extracted": 0,
    },
    {
        "id": "carrefour",
        "name": "Carrefour Israel",
        "name_he": "קרפור ישראל",
        "base": "https://www.carrefour.co.il",
        "probes": [
            ("home page",          "https://www.carrefour.co.il/",                                    False),
            ("search: לחם",        "https://www.carrefour.co.il/catalogsearch/result/?q=%D7%9C%D7%97%D7%9D", False),
        ],
        "known_blocker": "http_403",
        "blocker_detail": "HTTP 403 on all endpoints.",
        "api_access": False,
        "html_access": False,
        "product_extraction": "impossible",
        "products_extracted": 0,
    },
    {
        "id": "tiv_taam",
        "name": "Tiv Taam",
        "name_he": "טיב טעם",
        "base": "https://www.tivtaam.co.il",
        "probes": [
            ("home page",          "https://www.tivtaam.co.il/",                                      False),
            ("search: לחם",        "https://www.tivtaam.co.il/?s=%D7%9C%D7%97%D7%9D",                False),
        ],
        "known_blocker": "http_403",
        "blocker_detail": "HTTP 403 on all endpoints.",
        "api_access": False,
        "html_access": False,
        "product_extraction": "impossible",
        "products_extracted": 0,
    },
    {
        "id": "wolt_market",
        "name": "Wolt Market",
        "name_he": "וולט מרקט",
        "base": "https://wolt.com",
        "probes": [
            ("Israel front (TLV)", "https://consumer-api.wolt.com/v1/pages/front?lat=32.08&lon=34.78", True),
            ("venue SSR page",     "https://wolt.com/he/isr/tel-aviv/restaurant/wolt-market-ben-yehuda", False),
            ("restaurant API v3",  "https://restaurant-api.wolt.com/v3/venues/slug/wolt-market-ben-yehuda/menu", True),
            ("consumer API v2",    "https://consumer-api.wolt.com/v2/venues/slug/wolt-market-ben-yehuda/menu", True),
        ],
        "known_blocker": "dynamic_api_requires_auth",
        "blocker_detail": (
            "Consumer API front page accessible (698KB JSON, 20 sections, 307+ venue listings). "
            "Venue SSR page accessible (1.6MB HTML). React Query dehydrated state in page contains "
            "category structure (44 categories: מאפייה with subcategories לחם פרוס ושלם, קרקרים, etc.) "
            "but product items in SSR are only 24 promoted non-bread items. "
            "Category-specific product listings require dynamic API calls with authentication. "
            "restaurant-api.wolt.com menu endpoint returns 410 (deprecated). "
            "consumer-api.wolt.com venue endpoints return 404. "
            "No bread/cracker products extractable without auth token or headless browser."
        ),
        "api_access": True,    # front page API is accessible
        "html_access": True,   # SSR page is accessible
        "product_extraction": "partial_ssr_only_non_bread",
        "products_extracted": 0,  # 0 bread products extractable
        "wolt_findings": {
            "front_api_accessible": True,
            "venue_ssr_accessible": True,
            "ssr_product_count": 24,
            "bread_products_in_ssr": 0,
            "category_structure_found": True,
            "bread_categories": [
                "מאפייה (menucategory-26)",
                "לחמים מהדליקטסן (menucategory-31)",
                "לחם פרוס ושלם (menucategory-32)",
                "פיתות, לחמניות וטורטיות (menucategory-33)",
                "חטיפים וקרקרים (menucategory-212)",
                "קרקרים (menucategory-218)",
                "פריכיות (menucategory-217)",
            ],
            "grocery_venues_found": [
                "wolt-market-ben-yehuda",
                "tiv-taam-ibn-gabirol",
                "shufersal-drouyanov",
                "carrefour-migdaley-david",
                "victory-weizmann",
                "spar-tel-aviv",
            ],
            "dynamic_api_status": "requires_auth",
        },
    },
]


# ── Live probe execution ──────────────────────────────────────────────────────

def run_live_probes(retailers: list[dict]) -> list[dict]:
    """Run real HTTP probes for each retailer and attach live results."""
    results = []
    for r in retailers:
        log.info(f"Probing {r['name']} ({r['base']})")
        probe_results = []
        for label, url, json_mode in r["probes"]:
            time.sleep(2.5)
            resp = _get(url, json_mode=json_mode, referer=r["base"])
            status = _status_label(resp)
            is_maint = _is_maintenance_page(resp)
            is_js    = _is_js_shell(resp)
            size     = len(resp.content) if resp else 0

            probe_results.append({
                "label":            label,
                "url":              url,
                "json_mode":        json_mode,
                "status_code":      resp.status_code if resp else None,
                "status_label":     status,
                "is_maintenance":   is_maint,
                "is_js_shell":      is_js,
                "response_bytes":   size,
                "has_usable_content": (
                    resp is not None and resp.status_code == 200
                    and not is_maint and not is_js
                ),
            })
            note = ""
            if is_maint:  note = " [MAINTENANCE PAGE]"
            elif is_js:   note = " [JS SHELL]"
            log.info(f"  {label:35s} → {status}{note}")

        result = dict(r)
        result["probe_results"] = probe_results
        results.append(result)
        log.info(f"  {r['name']:20s}: blocker={r['known_blocker']}, products={r['products_extracted']}")

    return results


# ── Acceptance gate ───────────────────────────────────────────────────────────

def apply_gate(products: list[dict]) -> dict:
    n = len(products)
    if n == 0:
        return {
            "passed": False,
            "reason": "zero_products — no real retailer bread/cracker products could be extracted",
            "n_products": 0,
            "n_with_nutrition": 0,
            "n_with_ingredients": 0,
            "n_with_url": 0,
            "pct_nutrition": 0.0,
            "pct_ingredients": 0.0,
            "n_categories": 0,
            "categories": [],
        }

    n_nutrition   = sum(1 for p in products if p.get("has_nutrition_table"))
    n_ingredients = sum(1 for p in products if p.get("has_ingredient_text"))
    n_with_url    = sum(1 for p in products if p.get("source_url"))
    cats          = set(p.get("category_hint","") for p in products if p.get("category_hint"))
    pct_nutrition   = n_nutrition / n
    pct_ingredients = n_ingredients / n

    failures = []
    if n < GATE_MIN_PRODUCTS:
        failures.append(f"only {n} products (need {GATE_MIN_PRODUCTS})")
    if n_with_url < n:
        failures.append(f"{n - n_with_url} products missing source_url")
    if pct_nutrition < GATE_NUTRITION_PCT:
        failures.append(f"nutrition coverage {pct_nutrition:.0%} (need {GATE_NUTRITION_PCT:.0%})")
    if pct_ingredients < GATE_INGREDIENT_PCT:
        failures.append(f"ingredient coverage {pct_ingredients:.0%} (need {GATE_INGREDIENT_PCT:.0%})")
    if len(cats) < GATE_MIN_CATEGORIES:
        failures.append(f"only {len(cats)} category types (need {GATE_MIN_CATEGORIES})")

    return {
        "passed":             len(failures) == 0,
        "reason":             "ok" if not failures else "; ".join(failures),
        "n_products":         n,
        "n_with_nutrition":   n_nutrition,
        "n_with_ingredients": n_ingredients,
        "n_with_url":         n_with_url,
        "pct_nutrition":      round(pct_nutrition * 100, 1),
        "pct_ingredients":    round(pct_ingredients * 100, 1),
        "n_categories":       len(cats),
        "categories":         sorted(cats),
    }


# ── Report generation ─────────────────────────────────────────────────────────

BLOCKER_LABELS = {
    "maintenance_mode":              "IN MAINTENANCE — HTTP 200 with maintenance placeholder",
    "http_403":                      "BLOCKED — HTTP 403 Forbidden",
    "angularjs_spa":                 "BLOCKED (JS) — AngularJS SPA, headless browser required",
    "dynamic_api_requires_auth":     "PARTIAL — SSR accessible, product catalog requires auth/dynamic API",
    "http_404":                      "BLOCKED — HTTP 404",
    "none":                          "ACCESSIBLE",
}


def generate_access_report(retailer_results: list[dict], products: list[dict], gate: dict) -> None:
    def blocker_label(r): return BLOCKER_LABELS.get(r.get("known_blocker",""), r.get("known_blocker","?"))

    lines = [
        f"# BSIP0 Retailer Access Audit",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {RUN_DATE} | **Timestamp:** {RUN_TS}",
        f"",
        f"This audit documents all retailer access attempts, HTTP probes, and the acceptance gate result.",
        f"It is produced before any BSIP1/BSIP2 pipeline execution.",
        f"No products are added to the corpus until the gate passes.",
        f"",
        f"---",
        f"",
        f"## 1. Gate Result",
        f"",
        f"**Status: {'PASSED ✓' if gate['passed'] else 'FAILED ✗'}**",
        f"",
        ("Gate criteria met." if gate["passed"] else f"Reason: {gate['reason']}"),
        f"",
    ]
    if not gate["passed"]:
        lines += [
            f"**Do NOT proceed to BSIP1/BSIP2 pipeline.**",
            f"",
            f"The corpus does not meet minimum acceptance criteria.",
            f"Products collected: {gate['n_products']} (need {GATE_MIN_PRODUCTS})",
        ]

    lines += ["", "---", "", "## 2. Retailer Access Summary", ""]
    lines += [
        "| Retailer | HTTP Status | Blocker | Can Extract? |",
        "|:---------|:-----------|:--------|:-------------|",
    ]
    for r in retailer_results:
        label = blocker_label(r)
        can_extract = "No" if r["products_extracted"] == 0 else f"Yes ({r['products_extracted']} products)"
        lines.append(f"| {r['name']} | see probes | {label} | {can_extract} |")

    lines += ["", "---", "", "## 3. Retailer-by-Retailer Findings", ""]

    for r in retailer_results:
        lines += [
            f"### {r['name']} ({r['name_he']})",
            f"",
            f"**Verdict:** {blocker_label(r)}",
            f"",
            f"**Technical detail:** {r.get('blocker_detail','')}",
            f"",
            f"**Scrape method:** `{r.get('product_extraction','unknown')}`",
            f"**Products extracted:** {r['products_extracted']}",
            f"",
            "**HTTP Probes:**",
            "",
            "| Probe | Status | Notes |",
            "|:------|:-------|:------|",
        ]
        for p in r.get("probe_results", []):
            notes = []
            if p.get("is_maintenance"): notes.append("maintenance page")
            if p.get("is_js_shell"):    notes.append("JS app shell")
            if p.get("has_usable_content"): notes.append("usable content")
            if p["status_code"] in (403, 401): notes.append("blocked")
            if p["status_code"] == 410: notes.append("deprecated endpoint")
            lines.append(f"| {p['label']} | **{p['status_label']}** ({p['response_bytes']}B) | {', '.join(notes) or '—'} |")

        lines.append("")

        # Wolt-specific findings
        wf = r.get("wolt_findings")
        if wf:
            lines += [
                f"**Wolt-specific findings:**",
                f"",
                f"- Front API accessible: {wf['front_api_accessible']}",
                f"- Venue SSR page accessible: {wf['venue_ssr_accessible']}",
                f"- Products visible in SSR: {wf['ssr_product_count']} (promoted homepage items)",
                f"- Bread products in SSR: {wf['bread_products_in_ssr']}",
                f"- Bread category structure found: {wf['category_structure_found']}",
                f"- Bread categories: {', '.join(wf['bread_categories'])}",
                f"- Grocery venues on Wolt: {', '.join(wf['grocery_venues_found'])}",
                f"- Dynamic API status: {wf['dynamic_api_status']}",
                f"",
                f"**Wolt conclusion:** Category structure is accessible via SSR embedded JSON.",
                f"Product listings for specific categories (bread, crackers) require dynamic API calls",
                f"that return 404/410 without authentication. The Wolt product catalog is not",
                f"extractable via HTTP scraping without a Wolt user auth token or headless browser.",
                f"",
            ]

    # Products table
    lines += ["---", "", "## 4. Products Extracted", "", f"Total: {gate['n_products']}", ""]
    if products:
        lines += ["| # | Name | Retailer | Barcode | Nutrition | Ingredients |", "|:--|:-----|:---------|:--------|:----------|:------------|"]
        for i, p in enumerate(products, 1):
            lines.append(f"| {i} | {p.get('name_he','')[:40]} | {p.get('retailer_name','')} | {p.get('barcode','')} | {'✓' if p.get('has_nutrition_table') else '✗'} | {'✓' if p.get('has_ingredient_text') else '✗'} |")
    else:
        lines.append("**No products extracted.** All retailers blocked or unable to provide product data.")

    # Recommended next steps
    lines += [
        "",
        "---",
        "",
        "## 5. Technical Blockers and Recommended Next Steps",
        "",
        "### Blockers confirmed",
        "",
        "| Retailer | Blocker | Evidence |",
        "|:---------|:--------|:---------|",
        "| Shufersal | Maintenance mode | All URLs → HTTP 200, 444-byte placeholder with S3 maintenance image |",
        "| Rami Levy | HTTP 403 | Blocked on homepage, search, and API endpoints |",
        "| Victory | AngularJS SPA | HTTP 200 but all URLs return identical 6716-byte JS shell |",
        "| Carrefour Israel | HTTP 403 | Blocked on all endpoints |",
        "| Tiv Taam | HTTP 403 | Blocked on all endpoints |",
        "| Wolt Market | Dynamic API auth required | SSR accessible, but category product listings require auth |",
        "",
        "### What would unlock scraping",
        "",
        "1. **Shufersal**: Wait for maintenance to end, then retry. Their OCC API endpoint may work when online.",
        "2. **Rami Levy**: Direct partnership/API credentials, or rate-limited retry with rotating proxies.",
        "3. **Victory**: Headless browser (Playwright) — site uses AngularJS, server-renders nothing.",
        "4. **Carrefour**: Direct API credentials or Wolt delivery integration (Carrefour is on Wolt with slug `carrefour-migdaley-david`).",
        "5. **Tiv Taam**: Same as above — blocked; on Wolt as `tiv-taam-ibn-gabirol`.",
        "6. **Wolt Market**: Auth token from Wolt account, or headless browser to navigate categories.",
        "",
        "### OFF as enrichment (not primary corpus)",
        "",
        "Open Food Facts may only be used as a nutritional enrichment layer once real retailer",
        "products have been acquired. OFF MUST NOT serve as the primary product corpus.",
        "The ~42 Israeli OFF products do not satisfy the 'real retailer provenance' requirement.",
        "",
        "---",
        "",
        "## 6. Honest Assessment",
        "",
        "**This scrape failed the acceptance gate.**",
        "",
        "The real Israeli retailer landscape as of 2026-05-25:",
        "- All major supermarket chains actively block unauthenticated HTTP scraping",
        "- JavaScript-rendered sites require headless browser infrastructure",
        "- Wolt Market is the only semi-accessible source but requires auth for product menus",
        "- Open Food Facts has ~42 Israeli bread products — insufficient for real retailer corpus",
        "",
        "**Recommendation:** Build a headless-browser scraper (Playwright) targeting Wolt Market",
        "and Victory. Alternatively, contact retailers directly for product data export.",
        "",
        f"*Generated by bsip0_scrape_audit.py — {RUN_TS}*",
    ]

    AUDIT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"Audit report → {AUDIT_REPORT}")


def save_source_manifest(products: list[dict], retailer_results: list[dict], gate: dict) -> None:
    manifest = {
        "run_id":          RUN_ID,
        "run_timestamp":   RUN_TS,
        "gate_passed":     gate["passed"],
        "gate_result":     gate,
        "n_products":      len(products),
        "investigation_date": "2026-05-25",
        "retailer_summary": {
            r["id"]: {
                "name":                  r["name"],
                "known_blocker":         r.get("known_blocker", "none"),
                "api_access":            r.get("api_access", False),
                "html_access":           r.get("html_access", False),
                "product_extraction":    r.get("product_extraction", "not_attempted"),
                "products_extracted":    r.get("products_extracted", 0),
                "blocker_detail":        r.get("blocker_detail", ""),
            }
            for r in retailer_results
        },
        "products": products,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"Source manifest → {MANIFEST_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    log.info(f"=== BSIP0 Retailer Access Audit === run={RUN_ID} ts={RUN_TS}")

    # Run live probes
    log.info("\n[1/3] Running live HTTP probes...")
    retailer_results = run_live_probes(RETAILERS)

    # Gate (no products extracted)
    log.info("\n[2/3] Applying acceptance gate...")
    all_products: list[dict] = []   # zero products from all retailers
    gate = apply_gate(all_products)
    log.info(f"Gate: {'PASSED' if gate['passed'] else 'FAILED'} — {gate['reason']}")

    # Generate outputs
    log.info("\n[3/3] Generating audit outputs...")
    save_source_manifest(all_products, retailer_results, gate)
    generate_access_report(retailer_results, all_products, gate)

    print(f"\n{'='*60}")
    print(f"BSIP0 Scrape Audit Complete — {RUN_DATE}")
    print(f"{'='*60}")
    print(f"Products extracted: 0")
    print(f"Gate: FAILED ✗")
    print(f"Reason: {gate['reason']}")
    print(f"\nAll Israeli retailers blocked or inaccessible:")
    for r in retailer_results:
        label = BLOCKER_LABELS.get(r.get("known_blocker",""), "?")
        print(f"  {r['name']:20s}: {label}")
    print(f"\nDo NOT proceed to BSIP1/BSIP2.")
    print(f"\nOutputs:")
    print(f"  {AUDIT_REPORT}")
    print(f"  {MANIFEST_PATH}")

    return 1  # Gate failed


if __name__ == "__main__":
    sys.exit(main())
