"""
TASK-629 integrity re-check — re-derive every corrected nutrition value
directly from the persisted raw rows (nutrition_raw_source.rows), through the
SHARED, TASK-621-hardened parser (parse_nutrition_rows -> bare_to_raw_keys ->
parse_nutrition_numeric), instead of trusting each capture file's own
precomputed "nutrition_numeric" field.

Triggered by a caught defect: crackers barcode 7290018790328 carries
sodium_raw="1,200 מג" (1200 mg) but its precomputed nutrition_numeric.sodium_mg
= 1.2 -- the comma-thousands bug TASK-621 was supposed to have closed
project-wide, still present in whatever produced this capture's
"nutrition_numeric" field (canonicalization_schema="task616_type_b_rows_
reconstructed_from_nutrition_raw"). Bypassing that field and re-deriving from
the raw rows through the shared parser is the only way to trust the numbers.
"""
from __future__ import annotations
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))
import bsip0_nutrition as shared  # noqa: E402

ROOT = pathlib.Path(r"C:\Bari")

SOURCES = [
    {
        "shelf": "bread",
        "path": ROOT / "02_products/bread/bsip0_outputs/task602_bread_rescrape_20260711/bread_rescrape_final.json",
        "records_key": "records",
    },
    {
        "shelf": "crackers",
        "path": ROOT / "02_products/crackers/bsip0_outputs/task602_crackers_rescrape_20260711/crackers_frontend_v1_rescrape_results_canonical.json",
        "records_key": None,
    },
    {
        "shelf": "cheese",
        "path": ROOT / "02_products/cheese_spreads/bsip0_outputs/task602_cheese_frontend_v4_rescrape_20260711/cheese_frontend_v4_raw_capture_canonical.json",
        "records_key": None,
    },
]

NUM_KEYS = ["energy_kcal", "fat_g", "fat_saturated_g", "sodium_mg",
            "carbohydrates_g", "sugars_g", "dietary_fiber_g", "protein_g"]


def get_records(src):
    data = json.loads(src["path"].read_text(encoding="utf-8"))
    if src["records_key"]:
        return data[src["records_key"]]
    return data


def main():
    mismatches = []
    total = 0
    for src in SOURCES:
        for rec in get_records(src):
            if rec.get("status") not in (None, "scraped"):
                continue
            rows = (rec.get("nutrition_raw_source") or {}).get("rows") or []
            if not rows:
                continue
            total += 1
            bare = shared.parse_nutrition_rows(rows)
            raw_keys = shared.bare_to_raw_keys(bare)
            recomputed = shared.parse_nutrition_numeric(raw_keys)
            trusted = rec.get("nutrition_numeric") or {}
            diffs = {}
            for k in NUM_KEYS:
                rv, tv = recomputed.get(k), trusted.get(k)
                if rv is None and tv is None:
                    continue
                if rv is None or tv is None or abs(rv - tv) > 0.05:
                    diffs[k] = {"trusted_in_capture": tv, "recomputed_via_shared_parser": rv}
            if diffs:
                mismatches.append({
                    "shelf": src["shelf"],
                    "barcode": rec.get("barcode"),
                    "name": rec.get("name") or rec.get("name_he"),
                    "diffs": diffs,
                    "integrity_flags": recomputed.get("_integrity"),
                })

    print(f"Re-verified {total} corrected-capture records via the shared parser.")
    print(f"Mismatches vs each capture's own precomputed nutrition_numeric: {len(mismatches)}")
    for m in mismatches:
        print(f"  {m['shelf']} {m['barcode']} ({m['name']}): {m['diffs']}  integrity={m['integrity_flags']}")

    out_path = ROOT / "03_operations/bsip1/task629_corrected/shared_parser_reverify_report.json"
    out_path.write_text(json.dumps({"total_checked": total, "mismatches": mismatches}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport: {out_path}")


if __name__ == "__main__":
    main()
