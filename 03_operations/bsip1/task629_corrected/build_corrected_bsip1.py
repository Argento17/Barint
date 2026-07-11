"""
TASK-629 — Build corrected BSIP1 output for bread / crackers / cheese.

Scope: NUTRITION FIELDS ONLY. The TASK-602 re-scrape (batch-3/4/5) proved the
original BSIP0 capture for these three shelves mis-extracted total fat (grabbed
the saturated-fat row instead of the total-fat row -> EV-026 placeholder
0.25/0.5g) and separately had comma-thousands corruption on some sodium values
(fixed at the shared parser level by TASK-621, but these three shelves used
BESPOKE per-shelf BSIP1 builders that never called the shared parser -- so the
fix does not reach them by itself; it has to be re-applied by re-deriving
their BSIP1 nutrition from the corrected re-scrape capture).

This script does NOT touch ingredients_raw / ingredients_text_he / any derived
enrichment field (additives, NOVA proxy, matrix markers, etc). Those source
files also carry cleaner ingredient text, but changing ingredients is a
different, unrelated correction and out of this task's scope -- mixing it in
would make it impossible to attribute a score delta to "corrected nutrition"
alone. Flagged in the return for a possible follow-up task.

For every barcode in the current BSIP1 corpus:
  - If a corrected capture record exists for that barcode: copy the existing
    BSIP1 record, then overwrite normalized_nutrition_per_100g[k] with the
    corrected value for every key the corrected capture has a non-null value
    for. Keys absent/None in the corrected capture are left untouched (never
    null out a previously-populated field).
  - If no corrected capture record exists: copy the existing BSIP1 record
    unchanged (no basis to correct -> no correction applied).

Never fabricates: only overwrites with a value that was actually scraped in
the corrected capture.
"""
from __future__ import annotations
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")

NUTR_KEYS = [
    "energy_kcal", "fat_g", "fat_saturated_g", "fat_trans_g",
    "cholesterol_mg", "sodium_mg", "carbohydrates_g", "sugars_g",
    "dietary_fiber_g", "protein_g",
]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(obj, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def patch_one(existing: dict, corrected_numeric: dict) -> tuple[dict, list[str]]:
    out = json.loads(json.dumps(existing))  # deep copy
    nn = dict(out.get("normalized_nutrition_per_100g") or {})
    changed = []
    for k in NUTR_KEYS:
        new_v = corrected_numeric.get(k)
        if new_v is None:
            continue
        old_v = nn.get(k)
        if old_v != new_v:
            changed.append(f"{k}: {old_v} -> {new_v}")
        nn[k] = new_v
    out["normalized_nutrition_per_100g"] = nn
    out.setdefault("_task629_correction", {})
    out["_task629_correction"] = {
        "corrected": bool(changed),
        "changed_fields": changed,
        "source": "TASK-602 corrected re-scrape (EV-026 fat placeholder + comma-parser fix)",
    }
    return out, changed


def run_bread():
    existing_dir = ROOT / "03_operations/bsip1/run_bread_conform_001/output"
    out_dir = ROOT / "03_operations/bsip1/task629_corrected/bread/output"
    capture_path = ROOT / "02_products/bread/bsip0_outputs/task602_bread_rescrape_20260711/bread_rescrape_final.json"
    capture = load(capture_path)
    corrected_by_bc = {r["barcode"]: r["nutrition_numeric"] for r in capture["records"] if r.get("status") == "scraped"}

    report = {"shelf": "bread", "corrected_capture_count": len(corrected_by_bc), "existing_count": 0,
              "matched": [], "unmatched_existing": [], "unmatched_capture": set(corrected_by_bc.keys())}
    for fpath in sorted(existing_dir.glob("bsip1_*.json")):
        rec = load(fpath)
        bc = str(rec.get("barcode", "")).strip()
        report["existing_count"] += 1
        if bc in corrected_by_bc:
            new_rec, changed = patch_one(rec, corrected_by_bc[bc])
            report["matched"].append({"barcode": bc, "changed_fields": changed})
            report["unmatched_capture"].discard(bc)
            dump(new_rec, out_dir / fpath.name)
        else:
            report["unmatched_existing"].append(bc)
            dump(rec, out_dir / fpath.name)
    report["unmatched_capture"] = sorted(report["unmatched_capture"])
    return report


def run_crackers():
    existing_dir = ROOT / "03_operations/bsip1/run_crackers_conform_001/output"
    out_dir = ROOT / "03_operations/bsip1/task629_corrected/crackers/output"
    capture_path = ROOT / "02_products/crackers/bsip0_outputs/task602_crackers_rescrape_20260711/crackers_frontend_v1_rescrape_results_canonical.json"
    capture = load(capture_path)
    corrected_by_bc = {r["barcode"]: r["nutrition_numeric"] for r in capture if r.get("status") == "scraped"}

    report = {"shelf": "crackers", "corrected_capture_count": len(corrected_by_bc), "existing_count": 0,
              "matched": [], "unmatched_existing": [], "unmatched_capture": set(corrected_by_bc.keys())}
    for fpath in sorted(existing_dir.glob("bsip1_*.json")):
        rec = load(fpath)
        bc = str(rec.get("barcode", "")).strip()
        report["existing_count"] += 1
        if bc in corrected_by_bc:
            new_rec, changed = patch_one(rec, corrected_by_bc[bc])
            report["matched"].append({"barcode": bc, "changed_fields": changed})
            report["unmatched_capture"].discard(bc)
            dump(new_rec, out_dir / fpath.name)
        else:
            report["unmatched_existing"].append(bc)
            dump(rec, out_dir / fpath.name)
    report["unmatched_capture"] = sorted(report["unmatched_capture"])
    return report


def run_cheese():
    existing_dir = ROOT / "03_operations/bsip1/run_cheese_003/output"
    out_dir = ROOT / "03_operations/bsip1/task629_corrected/cheese/output"
    capture_path = ROOT / "02_products/cheese_spreads/bsip0_outputs/task602_cheese_frontend_v4_rescrape_20260711/cheese_frontend_v4_raw_capture_canonical.json"
    capture = load(capture_path)
    corrected_by_bc = {r["barcode"]: r["nutrition_numeric"] for r in capture if r.get("status") in (None, "scraped") and r.get("nutrition_numeric")}

    report = {"shelf": "cheese", "corrected_capture_count": len(corrected_by_bc), "existing_count": 0,
              "matched": [], "unmatched_existing": [], "unmatched_capture": set(corrected_by_bc.keys())}
    for fpath in sorted(existing_dir.glob("bsip1_*.json")):
        rec = load(fpath)
        bc = str(rec.get("barcode", "")).strip()
        report["existing_count"] += 1
        if bc in corrected_by_bc:
            new_rec, changed = patch_one(rec, corrected_by_bc[bc])
            report["matched"].append({"barcode": bc, "changed_fields": changed})
            report["unmatched_capture"].discard(bc)
            dump(new_rec, out_dir / fpath.name)
        else:
            report["unmatched_existing"].append(bc)
            dump(rec, out_dir / fpath.name)
    report["unmatched_capture"] = sorted(report["unmatched_capture"])
    return report


def main():
    reports = {"bread": run_bread(), "crackers": run_crackers(), "cheese": run_cheese()}
    for shelf, r in reports.items():
        matched_with_changes = [m for m in r["matched"] if m["changed_fields"]]
        print(f"=== {shelf} ===")
        print(f"  existing corpus: {r['existing_count']}")
        print(f"  corrected capture records: {r['corrected_capture_count']}")
        print(f"  matched (any field diff): {len(matched_with_changes)}/{len(r['matched'])}")
        print(f"  existing barcodes with NO correction available: {len(r['unmatched_existing'])}")
        print(f"  corrected-capture barcodes NOT in current corpus: {r['unmatched_capture']}")
    out_report_path = ROOT / "03_operations/bsip1/task629_corrected/build_report.json"
    dump(reports, out_report_path)
    print(f"\nReport written: {out_report_path}")


if __name__ == "__main__":
    main()
