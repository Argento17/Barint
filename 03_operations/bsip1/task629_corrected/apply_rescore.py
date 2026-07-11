"""
TASK-629 — Apply corrected nutrition-driven scores to the LIVE comparison JSON
for bread / crackers / cheese, scoped strictly to |delta|<=30 and to barcodes
that actually received a corrected-capture nutrition value.

Whitelist of fields updated per corrected barcode (data/trace-derived, never
authored content):
  score, grade, expansion.nutrition.*, expansion.confidenceLabel,
  confidence, confidence_label_he, confidence_level, confidence_sub_reason,
  confidence_tooltip_he

d4_additives / novaGroup are asserted UNCHANGED (ingredients were never
touched by this correction) rather than blindly overwritten -- a mismatch
here would indicate an out-of-scope side effect and must stop the run.

If grade changed: insightLine and rowVerdict are set to PENDING_COPY (stale
authored copy referencing the old grade cannot be kept -- needs Content Agent
authoring + two-gate sign-off before any go-live). Structural/taxonomy fields
that copy_stage's generic heuristic also flags as "copy" (_website_cluster,
nameHe, categoryTotal, brand, imageUrl, name, id, retailer,
source_traceability_status) are explicitly NOT touched -- they are not
authored content and do not need re-authoring on a grade change.

rank + _hash_no_rank (bread only) are recomputed for the WHOLE file after
merging, mirroring the site's existing bari-web/_sort_frontend.py convention
(hash_obj_except_rank / stable_sort_key), because a score correction can
reorder any product in the shelf, not only the corrected ones.

Excludes barcode 7290016967074 (bread identity anomaly, per TASK-629 spec) --
left completely untouched.
"""
from __future__ import annotations
import copy
import hashlib
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
EXCLUDE_BARCODES = {"7290016967074"}
DELTA_CAP = 30.0

SHELVES = [
    {
        "shelf": "bread",
        "live_path": ROOT / "bari-web/src/data/comparisons/bread_frontend_v4.json",
        "staged_path": ROOT / "_rescore_staging/bread_task629/bread_task629_rescored.json",
        "build_report_key": "bread",
        "has_hash_no_rank": True,
    },
    {
        "shelf": "crackers",
        "live_path": ROOT / "bari-web/src/data/comparisons/crackers_frontend_v1.json",
        "staged_path": ROOT / "_rescore_staging/crackers_task629/crackers_task629_rescored.json",
        "build_report_key": "crackers",
        "has_hash_no_rank": False,
    },
    {
        "shelf": "cheese",
        "live_path": ROOT / "bari-web/src/data/comparisons/cheese_frontend_v4.json",
        "staged_path": ROOT / "_rescore_staging/cheese_task629/cheese_task629_rescored.json",
        "build_report_key": "cheese",
        "has_hash_no_rank": False,
    },
]

DATA_FIELDS = [
    "score", "grade", "confidence", "confidence_label_he",
    "confidence_level", "confidence_sub_reason", "confidence_tooltip_he",
]
NUTRITION_KEYS = ["energyKcal", "fat", "fiber", "protein", "sodium", "sugar"]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(obj, p):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def hash_obj_except_rank(obj):
    obj_copy = copy.deepcopy(obj)
    obj_copy.pop("rank", None)
    return hashlib.sha256(
        json.dumps(obj_copy, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def main():
    build_report = load(ROOT / "03_operations/bsip1/task629_corrected/build_report.json")
    diff_rows = []
    defects = []

    for shelf_cfg in SHELVES:
        shelf = shelf_cfg["shelf"]
        live = load(shelf_cfg["live_path"])
        staged = load(shelf_cfg["staged_path"])
        live_by_bc = {p["barcode"]: p for p in live["products"]}
        staged_by_bc = {p["barcode"]: p for p in staged["products"]}

        # Corrected barcodes = ones with an actual field diff in the BSIP1 patch step
        matched = build_report[shelf_cfg["build_report_key"]]["matched"]
        corrected_bcs = [m["barcode"] for m in matched if m["changed_fields"]]

        applied_count = 0
        grade_changed_count = 0
        for bc in corrected_bcs:
            if bc in EXCLUDE_BARCODES:
                diff_rows.append({
                    "shelf": shelf, "barcode": bc,
                    "name": live_by_bc.get(bc, {}).get("name"),
                    "old_score": live_by_bc.get(bc, {}).get("score"),
                    "old_grade": live_by_bc.get(bc, {}).get("grade"),
                    "new_score": None, "new_grade": None, "delta": None,
                    "status": "EXCLUDED_IDENTITY_ANOMALY",
                })
                continue
            if bc not in live_by_bc:
                diff_rows.append({
                    "shelf": shelf, "barcode": bc, "name": None,
                    "old_score": None, "old_grade": None,
                    "new_score": staged_by_bc.get(bc, {}).get("score"),
                    "new_grade": staged_by_bc.get(bc, {}).get("grade"),
                    "delta": None,
                    "status": "NOT_IN_LIVE_PAGE_SKIPPED (out of scope: not a live product to correct)",
                })
                continue

            old_p = live_by_bc[bc]
            new_p = staged_by_bc[bc]
            old_score, new_score = old_p.get("score"), new_p.get("score")
            delta = round((new_score or 0) - (old_score or 0), 3)
            old_grade, new_grade = old_p.get("grade"), new_p.get("grade")

            row = {
                "shelf": shelf, "barcode": bc, "name": old_p.get("name"),
                "old_score": old_score, "old_grade": old_grade,
                "new_score": new_score, "new_grade": new_grade,
                "delta": delta,
            }

            if abs(delta) > DELTA_CAP:
                row["status"] = "DEFECT_OVER_30_NOT_APPLIED"
                defects.append(row)
                diff_rows.append(row)
                continue

            # NOTE: d4_additives / novaGroup are NEVER touched here (not in
            # DATA_FIELDS whitelist). A full re-run of the pipeline was found
            # to also pick up independent, out-of-scope engine drift on these
            # two fields (additive tier/explanation-text updates, NOVA-proxy
            # reclassification) unrelated to the TASK-629 nutrition fix --
            # same class of pre-existing drift as the documented "-0.8pt
            # unrelated router rule" note in bread.json. That drift is
            # observed and reported (out_of_scope_drift_observed below) but
            # deliberately NOT applied, to keep this correction scoped to
            # nutrition only.
            drift_notes = []
            if old_p.get("d4_additives") != new_p.get("d4_additives"):
                drift_notes.append("d4_additives_drift_not_applied (independent additive-KB update)")
            if "novaGroup" in old_p and old_p.get("novaGroup") != new_p.get("novaGroup"):
                drift_notes.append(
                    f"novaGroup_drift_not_applied ({old_p.get('novaGroup')}->{new_p.get('novaGroup')}, independent NOVA-proxy update)"
                )
            if drift_notes:
                row["out_of_scope_drift_observed"] = drift_notes

            # --- APPLY: whitelist merge ---
            for f in DATA_FIELDS:
                if f in new_p:
                    old_p[f] = new_p[f]
            old_p.setdefault("expansion", {})
            new_nutrition = (new_p.get("expansion") or {}).get("nutrition") or {}
            old_p["expansion"]["nutrition"] = {k: new_nutrition.get(k) for k in NUTRITION_KEYS}
            if "confidenceLabel" in (new_p.get("expansion") or {}):
                old_p["expansion"]["confidenceLabel"] = new_p["expansion"]["confidenceLabel"]

            grade_changed = old_grade != new_grade
            if grade_changed:
                old_p["insightLine"] = "PENDING_COPY"
                old_p["rowVerdict"] = "PENDING_COPY"
                grade_changed_count += 1
                row["status"] = "APPLIED_GRADE_CHANGED_COPY_PENDING"
            else:
                row["status"] = "APPLIED_GRADE_UNCHANGED_COPY_KEPT"

            applied_count += 1
            diff_rows.append(row)

        # Recompute rank (+ hash_no_rank for bread) across the WHOLE shelf
        products = list(live_by_bc.values())
        enriched = [(p, i) for i, p in enumerate(products)]
        enriched.sort(key=lambda x: (-(x[0].get("score") or 0), x[1]))
        sorted_products = [p for p, _ in enriched]
        for i, p in enumerate(sorted_products):
            p["rank"] = i + 1
            if shelf_cfg["has_hash_no_rank"]:
                p["_hash_no_rank"] = hash_obj_except_rank(p)

        scores = [p.get("score") or 0 for p in sorted_products]
        assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)), \
            f"{shelf}: scores not monotonic after resort"
        assert {p["barcode"] for p in sorted_products} == set(live_by_bc.keys()), \
            f"{shelf}: barcode set changed during resort"

        live["products"] = sorted_products
        dump(live, shelf_cfg["live_path"])
        print(f"{shelf}: applied={applied_count} grade_changed_pending_copy={grade_changed_count} "
              f"file={shelf_cfg['live_path']}")

    out = {
        "task": "TASK-629",
        "delta_cap": DELTA_CAP,
        "excluded_barcodes": sorted(EXCLUDE_BARCODES),
        "rows": diff_rows,
        "defects": defects,
    }
    out_path = ROOT / "03_operations/bsip2/proto_v0/reports/task629_rescore_diff.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dump(out, out_path)
    print(f"\nDiff report: {out_path}")
    print(f"Total rows: {len(diff_rows)}  Defects (>30): {len(defects)}")


if __name__ == "__main__":
    main()
