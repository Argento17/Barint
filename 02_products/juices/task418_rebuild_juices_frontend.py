# -*- coding: utf-8 -*-
"""
TASK-418 — Rebuild juices_frontend_v3.json from run_juices_task418_clean scores.

Updates per product:
  - score, grade, rank (re-rank by score descending)

Updates _meta:
  - generated (now)
  - run_id = "run_juices_task418_clean"

3 excluded barcodes (7290013153395, 7290110114886, 7290003009640) verified still A/85.
"""

import sys, json, pathlib, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_JSON = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json")
RUN_RECORD    = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_juices_task418_clean\run_record.json")

EXCLUDED_FROM_CLEANING = {"7290013153395", "7290110114886", "7290003009640"}


def main():
    print("=== TASK-418 Juices Frontend Rebuild ===")

    # Load run record
    rr = json.loads(RUN_RECORD.read_text(encoding="utf-8"))
    results = rr["results"]

    # Build score/grade lookup
    score_map = {}
    for row in results:
        bc = str(row["barcode"])
        score_map[bc] = {"score": row["fresh_score"], "grade": row["fresh_grade"]}

    print(f"Loaded run_record with {len(results)} product results")

    # Load frontend JSON
    frontend = json.loads(FRONTEND_JSON.read_text(encoding="utf-8"))
    products = frontend["products"]
    print(f"Frontend has {len(products)} products")

    # Verify excluded barcodes are A/85 in run record
    print("\nVerifying 3 excluded barcodes (should still be A/85):")
    for bc in EXCLUDED_FROM_CLEANING:
        if bc in score_map:
            s = score_map[bc]
            status = "PASS" if s["score"] == 85 and s["grade"] == "A" else "FAIL"
            print(f"  {status}  {bc}: {s['score']}/{s['grade']}")
        else:
            print(f"  MISSING  {bc}: not found in run record")

    # Update products
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
                excl = " [excluded-from-cleaning]" if bc in EXCLUDED_FROM_CLEANING else ""
                print(f"  UPDATE  {bc}: {old_score}/{old_grade} -> {new_score}/{new_grade}{excl}")
                p["score"] = new_score
                p["grade"] = new_grade
                updated_count += 1
            else:
                unchanged_count += 1
        else:
            not_in_run.append(bc)
            print(f"  WARN: barcode {bc} not in run record (not scored)")

    # Re-rank by score descending
    products.sort(key=lambda x: (-(x.get("score") or 0), x.get("rank", 999)))
    for i, p in enumerate(products, 1):
        p["rank"] = i
        p["categoryTotal"] = 17

    print(f"\nProducts updated: {updated_count}")
    print(f"Products unchanged: {unchanged_count}")
    print(f"Products not in run: {len(not_in_run)} -> {not_in_run}")

    # Update _meta
    meta = frontend.get("_meta", {})
    meta["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    meta["run_id"]    = "run_juices_task418_clean"
    from collections import Counter
    computed_dist = dict(sorted(Counter(p["grade"] for p in products).items()))
    meta["grade_distribution"] = computed_dist
    frontend["_meta"] = meta
    frontend["products"] = products

    print(f"New grade distribution: {computed_dist}")

    # Write back
    FRONTEND_JSON.write_text(json.dumps(frontend, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWritten: {FRONTEND_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
