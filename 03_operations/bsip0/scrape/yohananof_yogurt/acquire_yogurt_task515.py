"""
BSIP0 Yohananof — Yogurt acquisition, TASK-515 (yogurt category relaunch, multi-retailer).

The prior 01_acquire_yohananof_yogurt.py in this directory is DISABLED (raises at
import) because it paired il_prices identity with Open Food Facts panels — banned
project-wide (TASK-238/247). This script is a clean replacement that follows the
BSIP0 playbook's Yochananof workaround exactly: Playwright + cookie-dismiss +
product-modal scrape, direct from yochananof.co.il — NEVER OFF, NEVER the
requests/JSON API (TLS/403 bot-wall on that path).

Architecture: Yohananof runs the same commerce SaaS as Victory (same CDN,
d226b0iufwcjmj.cloudfront.net) — this reuses Victory's generic acquire() engine
(03_operations/bsip0/scrape/victory/01_acquire_victory.py) by monkey-patching its
module-level BASE_URL/SEARCH_URL/CHAIN_ID/RETAILER_ID/RETAILER_NAME/OUT_DIR
constants before calling acquire(). Identity: il_prices/laibcatalog chain
7290455000004 (registered "yohananof", kind=laibcatalog). Panel: Playwright
storefront scrape only. No OFF fallback — empty panels stay NULL.

Output: 03_operations/bsip0/scrape/yohananof_yogurt/outputs/yohananof_yogurt_task515_raw_<ts>.json
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_DIR = Path(r"C:\Bari\03_operations\bsip0\scrape\victory")
HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("acquire_victory_core_for_yohananof", VICTORY_DIR / "01_acquire_victory.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

# ── Re-point the shared engine at Yohananof ─────────────────────────────────────
core.RETAILER_ID = "yohananof"
core.RETAILER_NAME = "יוחננוף"
core.CHAIN_ID = "7290455000004"
core.BASE_URL = "https://yochananof.co.il"
core.SEARCH_URL = core.BASE_URL + "/category?search={query}"
core.OUT_DIR = OUT_DIR

# ── Yohananof-specific candidate discovery ──────────────────────────────────────
# core.browse_category_for_candidates() (ported from Victory) filters images by
# 'cloudfront.net' substring and extracts the barcode from a Victory-CDN path
# (/gs1-products/<chain>/.../<EAN>-...). Diagnosed 2026-07-05 (TASK-515): Yohananof
# does NOT use that CDN at all — product thumbnails are served through Next.js'
# own image proxy pointed at api.yochananof.co.il, e.g.:
#   /_next/image?url=https%3A%2F%2Fapi.yochananof.co.il%2Fmedia%2Fcatalog%2Fproduct%2F
#     cache%2F.../3%2F7%2F370610_7290110578053_4.jpg&w=384&q=75
# The 13-digit EAN barcode is embedded literally in the (decoded) filename as
# <sku>_<EAN>_<n>.jpg. The product name is on img[alt] directly (MUI card),
# so no separate ancestor-text guess is needed. Replaces the cloudfront-only scan.
_BARCODE_IN_FILENAME = re.compile(r"_(\d{13})_")


def _decode_next_image_url(raw_src: str) -> str:
    first = (raw_src or "").split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        qs = parse_qs(urlparse(first).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


_LOAD_MORE_TEXTS = ["טען עוד", "הצג עוד", "עוד תוצאות", "טעינת עוד", "load more"]


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


def browse_yohananof_candidates(page, category_query, include_signals, hard_drop, max_products):
    """Fixed 2026-07-05 (TASK-515A): the original 60-iteration/900ms-wait loop
    plateaued at 8 candidates and never grew past scroll ~20, even though a
    diagnostic re-load of the SAME page with more patience (explicit load-more
    button clicks + longer per-scroll settle time) surfaced 22 distinct product
    images. Root cause: this is a MUI virtualized list — new items need more
    settle time per scroll AND some pagination is gated behind an explicit
    "load more"-style control, not pure infinite-scroll. Fix: longer per-scroll
    wait (1400ms), explicit load-more click attempts every iteration, and a
    STABILITY-based stop (N consecutive scrolls with zero new candidates) instead
    of a fixed iteration count — this naturally extends the search if the page is
    just slow, and stops promptly once genuinely exhausted.
    """
    from urllib.parse import quote as _q
    url = core.SEARCH_URL.format(query=_q(category_query))
    print(f"  [yohananof] Category browse: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    core.close_cookie_popup(page)

    candidates = []
    seen_barcodes: set[str] = set()
    stale_scrolls = 0
    STALE_LIMIT = 15  # consecutive no-growth scrolls before giving up
    MAX_SCROLLS = 120

    for scroll_i in range(1, MAX_SCROLLS + 1):
        before = len(candidates)
        imgs = page.locator('img[src*="_next/image"]').all()
        for img in imgs:
            try:
                src = img.get_attribute("src") or ""
                decoded = _decode_next_image_url(src)
                m = _BARCODE_IN_FILENAME.search(decoded)
                if not m:
                    continue
                bc = m.group(1)
                if bc in seen_barcodes:
                    continue
                name = (img.get_attribute("alt") or "").strip()
                if not name:
                    continue
                if any(h.lower() in name.lower() for h in hard_drop):
                    continue
                if include_signals and not any(s.lower() in name.lower() for s in include_signals):
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

        if stale_scrolls >= STALE_LIMIT:
            print(f"  [yohananof] Stopping: {STALE_LIMIT} consecutive scrolls with no new "
                  f"candidates (found {len(candidates)} total, scroll {scroll_i}/{MAX_SCROLLS})")
            break

        clicked = _try_click_load_more(page)
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1400 if not clicked else 2000)
        if scroll_i % 10 == 0:
            print(f"  [yohananof] Browsing... scroll {scroll_i}/{MAX_SCROLLS}, "
                  f"found {len(candidates)} candidates so far (stale={stale_scrolls})")

    return candidates


core.browse_category_for_candidates = browse_yohananof_candidates

sys.path.insert(0, str(HERE.parent / "_shared"))
from yogurt_task515_tagging import retag_records  # noqa: E402

HARD_DROP = [
    "גלידה", "ice cream", "חמאה", "מרגרינה", "שמנת", "גבינה צהובה",
    "קוטג", "קצפת", "מעדן", "מילקי", "מוס", "פודינג",
    "תוסף", "קפסול", "טבליות", "כמוסות", "זית", "זיתים", "olive",
    "שמפו", "סבון", "ניקוי",
]

# TASK-515 mid-run scope change: drinkable is first-class — own acquisition pass
# with a drinkable-anchored query, not just incidental capture under "יוגורט".
SPOONABLE_INCLUDE = [
    "יוגורט", "yogurt", "yoghurt", "יווני", "greek", "סקיר", "skyr",
    "אקטיביה", "activia", "ביו", "bio", "מולר", "muller", "müller",
    "יופלה", "yoplait", "דנונה", "danone", "פרופ", "froop",
    "קפיר", "kefir", "לאבנה", "labneh", "labne",
]
DRINKABLE_INCLUDE = [
    "משקה יוגורט", "אקטימל", "actimel", "לשתייה", "יוגורט לשתייה",
    "דנונה לשתיה", "לאסי", "אירן", "שייק יוגורט",
]


def main(max_per_pass: int = 25, headless: bool = False):
    print(f"=== Yohananof yogurt acquisition (TASK-515), max_per_pass={max_per_pass} ===")
    print(f"    BASE_URL={core.BASE_URL}  CHAIN_ID={core.CHAIN_ID}  RETAILER_ID={core.RETAILER_ID}")
    seen_barcodes: set[str] = set()
    run_report: list[dict] = []

    print("\n--- Pass 1: spoonable-anchored query ---")
    r1 = core.acquire(SPOONABLE_INCLUDE, HARD_DROP, "yogurt", max_products=max_per_pass, headless=headless)
    for rec in r1:
        bc = rec.get("barcode")
        if bc and bc not in seen_barcodes:
            seen_barcodes.add(bc)
            run_report.append(rec)

    print("\n--- Pass 2: drinkable-anchored query (first-class subpool, own pass) ---")
    r2 = core.acquire(DRINKABLE_INCLUDE, HARD_DROP, "yogurt", max_products=max_per_pass, headless=headless)
    for rec in r2:
        bc = rec.get("barcode")
        if bc and bc not in seen_barcodes:
            seen_barcodes.add(bc)
            run_report.append(rec)

    for rec in run_report:
        rec["source"] = "yohananof"
        rec["retailer_id"] = "yohananof"
        rec["retailer_name"] = "יוחננוף"
        rec["scraped_at"] = datetime.now(timezone.utc).isoformat()

    kept, rejected = retag_records(run_report, name_field="name")
    n_spoon = sum(1 for r in kept if r.get("subpool") == "spoonable")
    n_drink = sum(1 for r in kept if r.get("subpool") == "drinkable")
    print(f"\nSubpool split: {n_spoon} spoonable, {n_drink} drinkable, {len(rejected)} out-of-scope rejected")
    if rejected:
        for r in rejected[:10]:
            print(f"  REJECTED [{r.get('out_of_scope_reason')}]: {r.get('name')}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = OUT_DIR / f"yohananof_yogurt_task515_raw_{ts}.json"
    out_path.write_text(json.dumps({"kept": kept, "rejected": rejected}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote: {out_path}")
    return kept, rejected, out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=25)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    main(max_per_pass=args.max, headless=args.headless)
