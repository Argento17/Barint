"""
BSIP0 Victory — Yogurt acquisition, TASK-515 (yogurt category relaunch, multi-retailer).

Reuses the proven generic `acquire()` engine in 01_acquire_victory.py (same file used
for hard_cheese/juice): il_prices/laibcatalog identity (chain 7290696200003,
LIVE-VERIFIED) -> Playwright storefront panel scrape (nutrition/ingredients tabs).
NO OFF fallback anywhere — empty panels stay NULL (project-wide OFF ban, TASK-238/247).

TASK-515 scope: broad yogurt shelf + boundary items (drinkable/kefir/labneh) captured
and TAGGED via post-hoc name matching (the shared acquire() engine doesn't carry a
per-item boundary tag natively, so we derive scope_tag from the product name after
acquisition — corpus filter still decides inclusion, this only labels).

Output: 03_operations/bsip0/scrape/victory/outputs/victory_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("acquire_victory_core", HERE / "01_acquire_victory.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)  # gives us core.acquire, core.OUT_DIR, etc.

# ── Reachability fix (diagnosed 2026-07-05, TASK-515) ───────────────────────────
# core.browse_category_for_candidates() opens the category-search page with
# wait_until="networkidle". Victory's storefront is an Angular SPA with a
# persistent background poller — it can go 60s+ without ever reaching true
# network-idle, so the goto times out before any image scan happens (confirmed:
# this run failed at the FIRST page.goto, before the img-scraping loop). Swap to
# "domcontentloaded" + a generous explicit wait; the image/barcode extraction
# logic itself (cloudfront.net CDN + /gs1-products/ path) is unchanged.
def _fixed_browse_category_for_candidates(page, category_query, include_signals, hard_drop, max_products):
    from urllib.parse import quote as _q
    url = core.SEARCH_URL.format(query=_q(category_query))
    print(f"  Category browse (domcontentloaded): {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(9000)
    core.close_cookie_popup(page)

    candidates = []
    seen_barcodes: set[str] = set()
    for scroll_i in range(1, 60):
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
                bc = core.barcode_from_cdn_url(core.normalize_image_url(src))
                if not bc or bc in seen_barcodes:
                    continue
                name = ""
                try:
                    card = img.locator("xpath=ancestor::*[@class][3]").first
                    raw_text = (card.inner_text(timeout=500) or "").strip()
                    name = raw_text.split("\n")[0].strip()[:80]
                except Exception:
                    pass
                if name and any(h.lower() in name.lower() for h in hard_drop):
                    continue
                seen_barcodes.add(bc)
                candidates.append({"barcode": bc, "name": name or bc, "identity_source": "victory_storefront_browse"})
                if len(candidates) >= max_products:
                    return candidates
            except Exception:
                pass
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(900)
        if scroll_i % 10 == 0:
            print(f"  Browsing... scroll {scroll_i}/60, found {len(candidates)} candidates so far")
    return candidates


core.browse_category_for_candidates = _fixed_browse_category_for_candidates

sys.path.insert(0, str(HERE.parent / "_shared"))
from yogurt_task515_tagging import retag_records  # noqa: E402

HARD_DROP = [
    "גלידה", "ice cream", "חמאה", "מרגרינה", "שמנת", "גבינה צהובה",
    "קוטג", "קצפת", "מעדן", "מילקי", "מוס", "פודינג",
    "תוסף", "קפסול", "טבליות", "כמוסות", "זית", "זיתים", "olive",
    "שמפו", "סבון", "ניקוי",
]

# TASK-515 mid-run scope change: drinkable is first-class — it gets its OWN
# acquisition pass with a drinkable-anchored query (not just incidental capture
# under a spoonable search). Two passes, each capped, merged + deduped by barcode.
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
    print(f"=== Victory yogurt acquisition (TASK-515), max_per_pass={max_per_pass} ===")
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
        rec["source"] = "victory"
        rec["retailer_id"] = "victory"
        rec["retailer_name"] = "ויקטורי"
        rec["scraped_at"] = datetime.now(timezone.utc).isoformat()

    kept, rejected = retag_records(run_report, name_field="name")
    n_spoon = sum(1 for r in kept if r.get("subpool") == "spoonable")
    n_drink = sum(1 for r in kept if r.get("subpool") == "drinkable")
    print(f"\nSubpool split: {n_spoon} spoonable, {n_drink} drinkable, {len(rejected)} out-of-scope rejected")
    if rejected:
        for r in rejected[:10]:
            print(f"  REJECTED [{r.get('out_of_scope_reason')}]: {r.get('name')}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = HERE / "outputs" / f"victory_yogurt_task515_raw_{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
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
