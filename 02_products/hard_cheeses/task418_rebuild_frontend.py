# -*- coding: utf-8 -*-
"""
TASK-418 — Rebuild hard_cheeses_frontend_v4.json from run_hc_task418_clean scores.

Updates per product (curated 31):
  - score, grade, rank (re-rank by score descending)
  - categoryTotal stays 31

Updates _meta:
  - generated (now)
  - source_run = "run_hc_task418_clean"
  - adds BARI_HC_DAIRY_SATFAT_V1 and BARI_DAIRY_SAT_FAT_INFER to flag_vector
  - grade_distribution

All other fields (copy, expansion, image URLs, etc.) are preserved exactly.
"""

import sys, json, pathlib, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_JSON = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v4.json")
RUN_SUMMARY   = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hc_task418_clean\run_summary.json")


def main():
    print("=== TASK-418 HC Frontend Rebuild ===")

    # Load run summary
    summary = json.loads(RUN_SUMMARY.read_text(encoding="utf-8"))
    stable_table = summary["curated_31"]["stable_table"]
    grade_dist_new = summary["curated_31"]["grade_distribution"]

    # Build score/grade lookup from run summary
    score_map = {}
    for row in stable_table:
        bc = str(row["barcode"])
        score_map[bc] = {"score": row["score"], "grade": row["grade"]}

    print(f"Loaded run_summary with {len(stable_table)} curated rows")
    print(f"New grade distribution: {grade_dist_new}")

    # Load frontend JSON
    frontend = json.loads(FRONTEND_JSON.read_text(encoding="utf-8"))
    products = frontend["products"]
    print(f"Frontend has {len(products)} products")

    # Track what changed
    updated_count   = 0
    unchanged_count = 0
    not_in_run      = []

    for p in products:
        bc = str(p["barcode"])
        if bc in score_map:
            old_score = p.get("score")
            old_grade = p.get("grade")
            new_score = score_map[bc]["score"]
            new_grade = score_map[bc]["grade"]

            if old_score != new_score or old_grade != new_grade:
                print(f"  UPDATE  {bc}: {old_score}/{old_grade} -> {new_score}/{new_grade}")
                p["score"] = new_score
                p["grade"] = new_grade
                updated_count += 1
            else:
                unchanged_count += 1
        else:
            not_in_run.append(bc)
            print(f"  WARN: barcode {bc} not found in run_summary (not in curated 31 or was discarded)")

    # Re-rank by score descending (ties: stable sort by existing rank)
    products.sort(key=lambda x: (-(x.get("score") or 0), x.get("rank", 999)))
    for i, p in enumerate(products, 1):
        p["rank"] = i
        p["categoryTotal"] = 31

    print(f"\nProducts updated: {updated_count}")
    print(f"Products unchanged: {unchanged_count}")
    print(f"Products not in curated run: {len(not_in_run)} -> {not_in_run}")

    # Update _meta
    meta = frontend.get("_meta", {})
    meta["generated"]    = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta["source_run"]   = "run_hc_task418_clean"
    meta["task"]         = "TASK-418"
    meta["grade_distribution"] = grade_dist_new

    # Add new flags to flag_vector
    fv = meta.get("flag_vector", {})
    fv["BARI_HC_DAIRY_SATFAT_V1"]  = "on"
    fv["BARI_DAIRY_SAT_FAT_INFER"] = "on"
    meta["flag_vector"] = fv

    frontend["_meta"] = meta
    frontend["products"] = products

    # Verify grade distribution matches re-computed
    from collections import Counter
    computed_dist = dict(sorted(Counter(p["grade"] for p in products).items()))
    print(f"\nComputed grade dist from products: {computed_dist}")
    print(f"Run summary grade dist:            {grade_dist_new}")
    if computed_dist != grade_dist_new:
        print("WARNING: grade distributions differ — using computed from products")
        meta["grade_distribution"] = computed_dist

    # Write back
    FRONTEND_JSON.write_text(json.dumps(frontend, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWritten: {FRONTEND_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
