"""
Shufersal BSIP0 discovery — Hummus and Savory Dips.

Discovers hummus and savory dip products from the confirmed Shufersal shelf
categories (A162406, A162403, A162408) plus targeted search queries.

Usage:
    cd C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal_hummus
    python 01_discover_hummus_shufersal.py

Output:
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\shufersal\\all_discovered_raw.json
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\shufersal\\candidate_review.csv

Next:
    Open candidate_review.csv.
    For each row, set approved_for_scrape to YES, NO, or REVIEW.
    Then run: python 02_scrape_hummus_shufersal.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
import datetime
import pathlib
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Shufersal HTTP config ──────────────────────────────────────────────────────
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
MAX_PRODUCTS = 200
MAX_PAGES = 5
PRODUCT_PAGE_DELAY = 0.8
MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]

# ── Confirmed category codes (TASK-025) ───────────────────────────────────────
# A162406 = סלטי חומוס וטחינה (Hummus & Tahini Salads) — 48 products
# A162403 = סלטי חצילים (Eggplant Salads) — 26 products
# A162408 = סחוג ואריסה + מטבוחה (Schug + Matbucha) — 17 products
# A162405 = ממרחים מצוננים (Chilled Spreads) — 34 products (optional)
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A162406?pageSize={PAGE_SIZE}", "A162406_hummus_tahini"),
    (f"{BASE}/online/he/c/A162403?pageSize={PAGE_SIZE}", "A162403_eggplant"),
    (f"{BASE}/online/he/c/A162408?pageSize={PAGE_SIZE}", "A162408_schug_matbucha"),
    # A162405 optional — uncomment if primary categories don't clear the BSIP0 gate:
    # (f"{BASE}/online/he/c/A162405?pageSize={PAGE_SIZE}", "A162405_chilled_spreads"),
]

# ── Search query plan ─────────────────────────────────────────────────────────
# (query, tier) — mainstream = full pagination; specialty = 2 pages; brand = full
QUERY_PLAN: list[tuple[str, str]] = [
    ("חומוס",                  "mainstream"),
    ("ממרח חומוס",             "mainstream"),
    ("חומוס שום",              "mainstream"),
    ("חומוס חריף",             "mainstream"),
    ("חומוס דל שומן",          "mainstream"),
    ("חומוס אורגני",           "specialty"),
    ("חומוס ביו",              "specialty"),
    ("חומוס קל",               "specialty"),
    ("חומוס עם צנוברים",       "specialty"),
    ("מטבוחה",                 "mainstream"),
    ("ממרח חצילים",            "mainstream"),
    ("חציליות",                "mainstream"),
    ("ממרח פלפל",              "specialty"),
    ("פלפל צ'ומה",             "specialty"),
    # Brand searches
    ("אחלה חומוס",             "brand"),
    ("צבר חומוס",              "brand"),
    ("ידין חומוס",             "brand"),
    ("יקין חומוס",             "brand"),
]

# ── Hard exclude — TASK-018 + TASK-025 + TASK-026 ─────────────────────────────
HARD_EXCLUDE: list[str] = [
    # Ready-to-eat tahini dip — TASK-026 decision: defer to Tahini category
    "סלט טחינה", "טחינה מוכנה", "ממרח טחינה", "טחינה ביתית",
    # Raw tahini
    "טחינה גולמית",
    # Schug and harissa (hot condiments)
    "סחוג", "זחוג", "אריסה", "ארוסה", "חריסה מרוקאית", "חריסה תוניסאית",
    # Sweet spreads
    "ממרח שוקולד", "נוטלה", "ריבה", "ממרח תמרים", "דבש", "ממרח קרמל",
    # Dairy spreads
    "גבינה לבנה", "לאבנה", "גבינת שמנת", "קוטג", "ממרח גבינה",
    # Fish and meat
    "ממרח דגים", "דג מעושן", "ממרח טונה", "פטה",
    # European-style condiments
    "פסטו", "טפנד", "ממרח זיתים", "ארטישוק", "חזרת", "לימון בלאדי",
    # Pasta sauces and condiments
    "רוטב פסטה", "קטשופ", "חרדל", "מיונז",
    # Pickles
    "חמוצים", "כבוש", "זיתים",
    # Vegetable salads
    "קולסלאו", "כרוב לבן", "כרוב סגול", "גזר מרוקאי", "גזר קוריאני",
    "סלק", "תפוח אדמה", "בולגרי", "אוקראינ",
    # Hummus format (snack, not spread)
    "צ'יפס חומוס", "חומוסיות",
]

# ── Positive signals (help candidate_decision) ────────────────────────────────
POSITIVE_TYPES: list[str] = [
    "חומוס", "ממרח חומוס", "ממרח חצילים", "חציליות",
    "מטבוחה", "ממרח פלפל", "פלפל צ'ומה", "ממרח ירקות",
    "תבסיל", "סלט טורקי",
]

# ── Nutrition label map — RETIRED (TASK-192 / EV-046) ───────────────────────────
# The legacy NUTR_LABEL_MAP that lived here mapped BOTH "שומנים" (total fat) and the
# bare substring "שומן" (present in every "of which" fat sub-row) to `fat`, which is the
# exact EV-029 overwrite defect. It was already DEAD CODE in this discovery script (no
# nutrition is parsed here — the actual hummus nutrition parse lives in
# 02_scrape_hummus_shufersal.py, which uses the shared parser). Removed so the broken
# pattern can never be copied out of this file. The single source of truth for every
# Shufersal nutrition parse is _shared/bsip0_nutrition.py.

# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*מ[\"']?ל", re.IGNORECASE),
]


def _extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 10 < val < 5000:
                    return val
            except ValueError:
                pass
    return None


def _price_per_100g(price_str: str, weight_g: float | None) -> float | None:
    if not price_str or not weight_g:
        return None
    try:
        return round(float(price_str.replace(",", ".")) * 100 / weight_g, 2)
    except (ValueError, ZeroDivisionError):
        return None

# ──────────────────────────────────────────────────────────────────────────────
# Filtering
# ──────────────────────────────────────────────────────────────────────────────

def _should_exclude(name: str) -> tuple[bool, str]:
    name_lower = name.lower()
    for term in HARD_EXCLUDE:
        if term in name_lower:
            return True, f"hard_exclude:{term}"
    return False, ""


def _candidate_decision(name: str) -> tuple[str, str]:
    exclude, reason = _should_exclude(name)
    if exclude:
        return "REJECT", reason
    for term in POSITIVE_TYPES:
        if term in name:
            return "YES", f"positive_type:{term}"
    if "חומוס" in name or "ממרח" in name or "מטבוחה" in name:
        return "REVIEW", "possible_target"
    return "REVIEW", "needs_manual_check"

# ──────────────────────────────────────────────────────────────────────────────
# Page parsers
# ──────────────────────────────────────────────────────────────────────────────

def _parse_product_list_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    results = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        is_food = d.get("data-food", "false").lower() == "true"
        if not is_food:
            continue
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": d.get("data-product-price", ""),
            "weight_g": _extract_weight_g(name),
        })
    return results


def _search_query(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search"
        f"?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}"
        f"&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def _category_page(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)

# ──────────────────────────────────────────────────────────────────────────────
# Main discovery
# ──────────────────────────────────────────────────────────────────────────────

def run_discovery() -> list[dict]:
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        print(msg, flush=True)

    # Phase 1: Category traversal (primary — confirmed categories from TASK-025)
    log("=== Phase 1: Category traversal ===")
    for base_url, cat_id in CATEGORY_URLS:
        cat_new = 0
        for page in range(MAX_PAGES):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _category_page(base_url, page)
            if not items:
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    # Apply hard exclude at discovery stage
                    excl, reason = _should_exclude(item["name"])
                    if not excl:
                        seen_codes.add(code)
                        code_meta[code] = {**item, "source_category": cat_id, "query": cat_id}
                        new_page += 1
            cat_new += new_page
            log(f"  [{cat_id}] page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            time.sleep(0.3)
        log(f"  [{cat_id}] total: {cat_new} new products")

    # Phase 2: Search queries (supplementary — organic/brand/variant coverage)
    log(f"\n=== Phase 2: Search queries ({len(seen_codes)} products so far) ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        max_pages = MAX_PAGES if tier in ("mainstream", "brand") else 2
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes:
                    excl, _ = _should_exclude(item["name"])
                    if not excl:
                        seen_codes.add(code)
                        code_meta[code] = {**item, "source_category": "search", "query": query, "tier": tier}
                        new_page += 1
            log(f"  '{query}' page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            time.sleep(0.3)

    products = list(code_meta.values())
    log(f"\nDiscovery complete: {len(products)} unique products (after hard-exclude filter)")
    return products


def write_outputs(products: list[dict]) -> None:
    # Add candidate decisions
    for p in products:
        decision, reason = _candidate_decision(p["name"])
        p["suggested_decision"] = decision
        p["decision_reason"] = reason
        p["approved_for_scrape"] = "NO"

    # Save raw JSON
    raw_path = OUT_DIR / f"all_discovered_raw_{datetime.date.today().isoformat()}.json"
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Raw JSON: {raw_path}")

    # Save CSV for manual review (sorted: YES first, REVIEW second, REJECT last)
    csv_path = OUT_DIR / "candidate_review.csv"
    fields = [
        "approved_for_scrape", "suggested_decision", "decision_reason",
        "name", "code", "categories", "price", "source_category", "query",
    ]
    rows_sorted = sorted(
        products,
        key=lambda x: {"YES": 0, "REVIEW": 1, "REJECT": 2}.get(x.get("suggested_decision", "REVIEW"), 9),
    )
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(row)

    yes = sum(1 for p in products if p["suggested_decision"] == "YES")
    review = sum(1 for p in products if p["suggested_decision"] == "REVIEW")
    reject = sum(1 for p in products if p["suggested_decision"] == "REJECT")
    print(f"\n==============================")
    print(f"Discovery complete")
    print(f"  YES    : {yes}")
    print(f"  REVIEW : {review}")
    print(f"  REJECT : {reject}")
    print(f"  Total  : {len(products)}")
    print(f"\nNext: open candidate_review.csv")
    print(f"  Set approved_for_scrape = YES for products you want to scrape")
    print(f"  Apply corpus_filter.md rules for REVIEW items")
    print(f"  Then run: python 02_scrape_hummus_shufersal.py")
    print(f"==============================")


def main() -> None:
    products = run_discovery()
    if not products:
        print("ERROR: No products discovered. Check network connection and category codes.")
        sys.exit(1)
    write_outputs(products)


if __name__ == "__main__":
    main()
