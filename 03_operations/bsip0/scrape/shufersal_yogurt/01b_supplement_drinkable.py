"""
TASK-515 supplement pass — extra drinkable-yogurt brand queries for Shufersal.

Mid-run scope change (coordinator, 2026-07-05): drinkable yogurt is now a
FIRST-CLASS subpool (own comparison page), so it needs the SAME query rigor as
spoonable, not just incidental boundary capture. This appends new codes (not
already in the base TASK-515 raw file) found under additional drinkable brand
anchors, using the exact same product-page parser as 01_scrape_yogurt_task515.py.
"""
from __future__ import annotations
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from time import sleep

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("shufersal_yogurt_core", HERE / "01_scrape_yogurt_task515.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

EXTRA_DRINKABLE_QUERIES = [
    ("אקטימל", "drinkable"),
    ("תנובה לשתיה", "drinkable"),
    ("יוגורט לשתייה תנובה", "drinkable"),
    ("שתית", "drinkable"),
    ("דנונה שתייה", "drinkable"),
    ("יוגורט שייק", "drinkable"),
    ("קוקטייל יוגורט", "drinkable"),
]


def main(base_raw_path: str):
    base = json.loads(Path(base_raw_path).read_text(encoding="utf-8"))
    seen_codes = {p.get("acquisition_query", "") for p in base}  # not codes; recompute below
    seen_barcodes = {p.get("barcode") for p in base}
    print(f"Base file: {len(base)} products, {len(seen_barcodes)} unique barcodes")

    new_products = []
    seen_new_codes: set[str] = set()
    for query, kind in EXTRA_DRINKABLE_QUERIES:
        for page in range(2):
            items = core._search_query(query, page, mode="boundary", boundary_kind=kind)
            if not items:
                print(f"  '{query}' page {page}: no results")
                break
            new_page = 0
            for item in items:
                code = item["code"]
                if code in seen_new_codes:
                    continue
                seen_new_codes.add(code)
                p = core._parse_product_page(code, {**item, "query": query, "tier": f"boundary:{kind}"})
                if p and p.get("barcode") not in seen_barcodes:
                    new_products.append(p)
                    seen_barcodes.add(p.get("barcode"))
                    new_page += 1
                sleep(0.5)
            print(f"  '{query}' page {page}: {len(items)} items, {new_page} genuinely new")

    print(f"\nNew products found: {len(new_products)}")
    merged = base + new_products
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_path = HERE.parent.parent.parent.parent / "02_products" / "yogurt_system" / "bsip0_task515" / f"shufersal_yogurt_bsip0_raw_MERGED_{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote merged: {out_path}  (total {len(merged)})")
    return out_path


if __name__ == "__main__":
    import glob
    files = sorted(glob.glob(r"C:\Bari\02_products\yogurt_system\bsip0_task515\shufersal_yogurt_bsip0_raw_2*.json"))
    main(files[-1])
