"""
TASK-582 canary — proves the fixed 01_acquire_shufersal.py fetch layer against LIVE
Shufersal with 3 known barcodes already present in the BSIP0 corpus (the same 3 the
Shelf Watch pilot uses as its own canary set, confirmed live 2026-07-10). Parses only —
writes ONLY to this scratch dir, never touches any corpus/served JSON.

Polite: 3 requests total, 1 retry max on failure, delay between requests.
"""
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACQUIRE_PATH = HERE.parent / "01_acquire_shufersal.py"

spec = importlib.util.spec_from_file_location("acquire_shufersal_582", ACQUIRE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Known-existing barcodes already in the BSIP0 corpus (same set Shelf Watch pilot uses
# as its own canary — confirmed scraped=healthy live 2026-07-10, see
# 03_operations/shelf_watch/runs/shelf_watch_20260710T153237Z.json). Not invented.
CANARY_BARCODES = [
    ("breakfast_cereals", "5010029000061"),
    ("breakfast_cereals", "7297488098688"),
    ("bread", "7290016245325"),
]

REQUIRED_FIELDS = ["name", "nutrition", "ingredients_raw_he"]


def run_one(category: str, barcode: str) -> dict:
    attempt = 0
    result = None
    while attempt < 2:  # 1 try + at most 1 retry
        attempt += 1
        result = mod.fetch_shufersal_product(barcode)
        if result["status"] == "scraped":
            break
        if attempt < 2:
            time.sleep(1.5)
    result["category"] = category
    result["attempts"] = attempt
    return result


def main():
    out = []
    for i, (category, barcode) in enumerate(CANARY_BARCODES):
        r = run_one(category, barcode)
        field_coverage = {}
        if r["status"] == "scraped":
            field_coverage["name"] = bool(r.get("name"))
            field_coverage["ingredients_raw_he"] = bool(r.get("ingredients_raw_he"))
            nutr = r.get("nutrition") or {}
            field_coverage["nutrition_any_field"] = bool(nutr)
            field_coverage["nutrition_fields_present"] = sorted(nutr.keys())
            field_coverage["nutrition_field_count"] = len(nutr)
        out.append({
            "barcode": barcode,
            "category": category,
            "http_status_class": r["status"],
            "reason": r.get("reason"),
            "final_url": r.get("final_url"),
            "attempts": r["attempts"],
            "field_coverage": field_coverage,
            "raw": r,
        })
        print(f"[{barcode}] status={r['status']} attempts={r['attempts']} "
              f"reason={r.get('reason')} url={r.get('final_url')}")
        if i < len(CANARY_BARCODES) - 1:
            time.sleep(1.5)

    report = {
        "task": "TASK-582",
        "purpose": "canary_only_no_corpus_write",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": out,
    }
    out_path = HERE / "canary_results.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    scraped_count = sum(1 for r in out if r["http_status_class"] == "scraped")
    print(f"\n{scraped_count}/{len(out)} fetched status=scraped (200 + parsed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
