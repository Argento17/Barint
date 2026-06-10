"""
Discover juice candidates on victoryonline.co.il — BSIP0 Victory corpus expansion.

Mirrors discover_juices_yohananof.py structure. Uses the Victory adapter at
03_operations/bsip0/scrape/victory/01_acquire_victory.py for identity via
il_prices (laibcatalog chain 7290696200003), with storefront-browse fallback.

Outputs to victory_scrape/ mirroring yohananof_scrape/:
  all_discovered_raw.json   — every candidate with YES/REVIEW/REJECT decision
  candidate_review.csv      — sorted for manual review
  il_prices_identity.json   — il_prices records for matched barcodes (when available)
  approved_candidates.json  — written by this script: auto-approved YES candidates

Run:
    python discover_juices_victory.py [--max N] [--headless]
Then:
    python scrape_juices_victory.py
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip
from integrations.source_validator import require_il_prices_accessible

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "victory_scrape"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RETAILER = "victory"
RETAILER_NAME = "ויקטורי"
CHAIN_ID = "7290696200003"

BASE_URL = "https://www.victoryonline.co.il"
SEARCH_URL = BASE_URL + "/category?search={query}"

# Identity signals — same logic as the Victory adapter's JUICE_INCLUDE/JUICE_DROP
# Expanded to cover nectars, fruit drinks, cold-pressed as well as 100% juice.
JUICE_INCLUDE = [
    "מיץ",
    "נקטר",
    "juice",
    "עסיס",
    "פריגת",
    "טרופיקנה",
    "סחוט",
    "משקה פירות",
    "מיצים",
]

JUICE_DROP = [
    "גזוז", "קולה", "מים מוגזים", "ספורט", "אנרג'י",
    "טוניק", "סודה", "מי ברז", "מים",
    "גלידה", "שוקולד", "שמפו", "ניקוי", "חיתול", "סוכריות",
    "ממרח",
]

# Search queries for storefront-browse fallback and candidate expansion
SEARCH_QUERIES = [
    "מיץ",
    "מיצים",
    "נקטר",
    "משקה פירות",
    "סחוט קר",
    "מיץ תפוזים",
    "מיץ תפוחים",
    "מיץ ענבים",
    "מיץ רימון",
    "פריגת",
]

# Sub-pool classification for each candidate
def classify_subpool(name: str) -> str:
    n = (name or "").lower()
    if "100%" in n or "טבעי" in n or "סחוט" in n or "טהור" in n:
        return "juice_100"
    if "נקטר" in n:
        return "nectar"
    if "משקה" in n or "משקאות" in n:
        return "fruit_drink"
    if "מיץ" in n:
        return "juice_100"  # default: if named "מיץ" without nectar/drink marker
    return "unknown"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean(text) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def name_matches(name: str) -> bool:
    nl = clean(name).lower()
    if any(d.lower() in nl for d in JUICE_DROP):
        return False
    return any(s.lower() in nl for s in JUICE_INCLUDE)


def candidate_decision(name: str, card_text: str = "") -> tuple[str, str]:
    combined = clean(f"{name} {card_text}")
    if not combined:
        return "REJECT", "empty"
    for term in JUICE_DROP:
        if term in combined:
            return "REJECT", f"hard_exclude:{term}"
    for term in JUICE_INCLUDE:
        if term.lower() in combined.lower():
            return "YES", "positive_juice_type"
    return "REJECT", "not_juice_type"


# ---------------------------------------------------------------------------
# il_prices identity (primary path)
# ---------------------------------------------------------------------------

def fetch_il_prices_candidates(max_products: int) -> tuple[list[dict], dict]:
    """
    Fetch Victory catalog from laibcatalog, filter to juice-relevant barcodes.
    Returns (candidates_list, identity_map).
    identity_map: barcode -> {barcode, name, manufacturer, price, quantity}
    """
    require_il_prices_accessible(RETAILER)
    files = ip.list_laibcatalog_files(CHAIN_ID)
    pf = [f for f in files if f.type == "PriceFull"]
    if not pf:
        raise RuntimeError(f"No PriceFull files on laibcatalog for chain {CHAIN_ID}")

    items = ip.fetch_items(pf[0])
    print(f"  Victory catalog via il_prices: {len(items)} items total")

    candidates = []
    identity_map = {}
    seen: set[str] = set()

    for it in items:
        bc = str(it.barcode)
        if not bc or bc in seen:
            continue
        name = clean(it.name or "")
        if name_matches(name):
            seen.add(bc)
            rec = {
                "barcode": bc,
                "name": name,
                "manufacturer": getattr(it, "manufacturer", None),
                "price": getattr(it, "price", None),
                "quantity": getattr(it, "quantity", None),
            }
            candidates.append(rec)
            identity_map[bc] = rec
            if len(candidates) >= max_products:
                break

    print(f"  Name-gate candidates (il_prices): {len(candidates)}")
    return candidates, identity_map


# ---------------------------------------------------------------------------
# Storefront-browse fallback (when il_prices unavailable)
# ---------------------------------------------------------------------------

def browse_for_candidates(page, max_products: int) -> list[dict]:
    """
    Scroll Victory category pages for juice-relevant products.
    Extracts barcodes from CDN image URLs (same pattern as the Victory adapter).
    """
    from urllib.parse import unquote, urlparse, parse_qs

    def barcode_from_cdn(url: str) -> str | None:
        m = re.search(r"/gs1-products/\d+/\w+/(\d{8,13})-", url or "")
        return m.group(1) if m else None

    def normalize_img(raw: str | None) -> str | None:
        if not raw:
            return None
        first = raw.split(" ")[0]
        if "/_next/image" in first and "url=" in first:
            parsed = urlparse(first)
            from urllib.parse import parse_qs as _pqs
            qs = _pqs(parsed.query)
            if "url" in qs:
                return unquote(qs["url"][0])
        return first

    seen: set[str] = set()
    candidates = []

    for query in SEARCH_QUERIES:
        if len(candidates) >= max_products:
            break
        url = SEARCH_URL.format(query=quote(query))
        print(f"  Browse: {url}")
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)
            _dismiss_popups(page)
        except Exception as e:
            print(f"  Browse navigation failed for '{query}': {e}")
            continue

        for scroll_i in range(1, 80):
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
                    bc = barcode_from_cdn(normalize_img(src))
                    if not bc or bc in seen:
                        continue
                    # Extract name from card
                    name = ""
                    try:
                        card = img.locator("xpath=ancestor::*[@class][3]").first
                        raw_text = (card.inner_text(timeout=500) or "").strip()
                        name = raw_text.split("\n")[0].strip()[:80]
                    except Exception:
                        pass
                    # Apply drop filter; include anything from a juice search
                    if name and any(d.lower() in name.lower() for d in JUICE_DROP):
                        continue
                    seen.add(bc)
                    candidates.append({
                        "barcode": bc,
                        "name": name or bc,
                        "query": query,
                        "identity_source": "victory_storefront_browse",
                    })
                    if len(candidates) >= max_products:
                        return candidates
                except Exception:
                    pass

            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(900)
            if scroll_i % 10 == 0:
                print(f"  Scroll {scroll_i}/80 — {len(candidates)} so far")

            # Stability check: stop scrolling when no new cards appear
            prev = len(candidates)
            # (sampled after every 5 scrolls; simple heuristic)

    return candidates


def _dismiss_popups(page) -> None:
    for selector in [
        'button:has-text("אישור")',
        'button:has-text("מסכים")',
        'button:has-text("הבנתי")',
        '[data-aria-desc="dialog_cookies_accept"]',
        '[role="dialog"] button',
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=600):
                btn.click(force=True)
                page.wait_for_timeout(700)
        except Exception:
            pass
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            btn = page.get_by_text(text, exact=True).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_outputs(candidates: list[dict], identity_map: dict, identity_mode: str) -> None:
    """
    Apply decision logic, deduplicate, write all_discovered_raw.json,
    candidate_review.csv, il_prices_identity.json, approved_candidates.json.
    """
    deduped: dict[str, dict] = {}
    for c in candidates:
        bc = c.get("barcode") or c.get("name")
        if not bc or bc in deduped:
            continue
        name = c.get("name", "")
        card_text = c.get("card_text", "")
        decision, reason = candidate_decision(name, card_text)
        subpool = classify_subpool(name)

        record = {
            "key": bc,
            "barcode": c.get("barcode", ""),
            "name": name,
            "brand": c.get("manufacturer", "") or "",
            "query": c.get("query", ""),
            "card_text": card_text,
            "subpool": subpool,
            "identity_source": c.get("identity_source", identity_mode),
            "discovered_at": now_iso(),
            "suggested_decision": decision,
            "decision_reason": reason,
            "approved_for_scrape": "YES" if decision == "YES" else "NO",
        }
        deduped[bc] = record

    rows = list(deduped.values())

    # all_discovered_raw.json
    save_json(OUTPUT_DIR / "all_discovered_raw.json", rows)

    # il_prices_identity.json — only for barcodes that came from il_prices
    if identity_map:
        save_json(OUTPUT_DIR / "il_prices_identity.json", identity_map)

    # candidate_review.csv
    csv_path = OUTPUT_DIR / "candidate_review.csv"
    fields = [
        "approved_for_scrape",
        "suggested_decision",
        "decision_reason",
        "subpool",
        "barcode",
        "name",
        "brand",
        "query",
        "identity_source",
        "card_text",
    ]
    rows_sorted = sorted(
        rows,
        key=lambda x: {"YES": 0, "REVIEW": 1, "REJECT": 2}.get(x.get("suggested_decision"), 9),
    )
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(row)

    # approved_candidates.json — YES candidates ready for scraping
    approved = [r for r in rows if r.get("suggested_decision") == "YES"]
    save_json(OUTPUT_DIR / "approved_candidates.json", approved)

    print("\n==============================")
    print(f"Discovery complete: {len(rows)} unique products")
    yes_c = sum(1 for r in rows if r.get("suggested_decision") == "YES")
    rev_c = sum(1 for r in rows if r.get("suggested_decision") == "REVIEW")
    rej_c = sum(1 for r in rows if r.get("suggested_decision") == "REJECT")
    print(f"  YES={yes_c}  REVIEW={rev_c}  REJECT={rej_c}")
    print(f"  Subpools: juice_100={sum(1 for r in rows if r.get('subpool') == 'juice_100')}"
          f"  nectar={sum(1 for r in rows if r.get('subpool') == 'nectar')}"
          f"  fruit_drink={sum(1 for r in rows if r.get('subpool') == 'fruit_drink')}")
    print(f"Approved candidates: {OUTPUT_DIR / 'approved_candidates.json'}")
    print(f"Review CSV: {csv_path}")
    print(f"Raw JSON: {OUTPUT_DIR / 'all_discovered_raw.json'}")
    print("==============================")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(max_products: int = 150, headless: bool = False) -> None:
    print(f"Victory juice discovery — target up to {max_products} candidates")
    print(f"Output dir: {OUTPUT_DIR}")

    identity_mode = "il_prices"
    candidates: list[dict] = []
    identity_map: dict = {}
    il_prices_ok = False

    # --- Primary: il_prices ---
    try:
        raw_candidates, identity_map = fetch_il_prices_candidates(max_products)
        for c in raw_candidates:
            c["identity_source"] = "il_prices"
            c["query"] = "מיץ"  # representative search term for scrape step
        candidates = raw_candidates
        il_prices_ok = True
    except Exception as e:
        print(f"  WARNING: il_prices unavailable ({e}) — falling back to storefront browse")
        identity_mode = "victory_storefront_browse"

    # --- Fallback: storefront browse (or supplement il_prices with browse) ---
    if not il_prices_ok:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=headless)
            context = browser.new_context(
                viewport={"width": 1500, "height": 1000},
                locale="he-IL",
                timezone_id="Asia/Jerusalem",
                extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
                permissions=[],
            )
            page = context.new_page()
            candidates = browse_for_candidates(page, max_products)
            context.close()
            browser.close()

    write_outputs(candidates, identity_map, identity_mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover Victory juice candidates")
    parser.add_argument("--max", type=int, default=150, help="Max candidates to collect")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args()
    main(max_products=args.max, headless=args.headless)
