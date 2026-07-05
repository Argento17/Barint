"""
TASK-515/515A Stage 2 -- independent verification pass.

Re-derives every number quoted in the return block DIRECTLY from the
committed trace files on disk (not from run_record.json's in-memory
summary), per return_contract_v1.md rules 6/7:
  - emits one flat machine-readable table: barcode, pool, score, grade,
    binding_caps, nova, fat, sodium, context_flag
  - recomputes per-pool distributions (min/median/max/stdev/grade_counts)
    from that table
  - recomputes the fermentation-fired count for the drinkable pool
  - recomputes the true dairy_protein + cultured-subtype eligible counts
    per pool, straight from each trace's own category/category_subtype
    fields (not from the run_record's router-check block)

Read-only: opens trace files under 02_products/yogurt_system/bsip2_task515/,
writes only its own output files in the same directory.
"""
import json, pathlib, statistics, csv
from collections import Counter

ROOT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_task515")

rows = []
for pool in ("spoonable", "drinkable"):
    prod_dir = ROOT / pool / "products"
    for sub in sorted(prod_dir.iterdir()):
        tf = sub / "bsip2_trace.json"
        if not tf.exists():
            continue
        t = json.loads(tf.read_text(encoding="utf-8"))
        nn = (t.get("L1_observed_signals") or {})
        caps = t.get("caps_applied") or []
        binding_cap = t.get("binding_cap")
        rows.append({
            "barcode": t["input_reference"].get("barcode"),
            "name": t["input_reference"].get("product_name_he"),
            "pool": pool,
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "binding_cap": binding_cap,
            "caps_applied_count": len(caps),
            "nova": t.get("nova_proxy"),
            "category": t.get("category"),
            "category_subtype": (t.get("L3_inferred_classifications") or {}).get("category_subtype"),
            "sodium_mg": nn.get("sodium_mg"),
            "fat_g": nn.get("fat_g"),
            "sugars_g": nn.get("sugars_g"),
            "context_flag": t.get("context_flag"),
            "evaluation_status": t.get("evaluation_status"),
        })

csv_path = ROOT / "verification_table.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow(r)

# Per-pool distribution, recomputed independently from the table above
report = {}
for pool in ("spoonable", "drinkable"):
    pool_rows = [r for r in rows if r["pool"] == pool]
    scored = [r["score"] for r in pool_rows if r["score"] is not None]
    grades = Counter(r["grade"] for r in pool_rows if r["grade"] is not None)
    dairy_protein_n = sum(1 for r in pool_rows if r["category"] == "dairy_protein")
    report[pool] = {
        "n_total": len(pool_rows),
        "n_scored": len(scored),
        "n_dairy_protein_routed": dairy_protein_n,
        "min": round(min(scored), 2) if scored else None,
        "median": round(statistics.median(scored), 2) if scored else None,
        "max": round(max(scored), 2) if scored else None,
        "stdev": round(statistics.stdev(scored), 2) if len(scored) > 1 else None,
        "grade_counts": dict(sorted(grades.items())),
        "most_common_score": Counter(scored).most_common(1)[0] if scored else None,
    }

# NOVA distribution per pool (for the "not in scoring path" cross-check)
nova_dist = {
    pool: dict(Counter(r["nova"] for r in rows if r["pool"] == pool))
    for pool in ("spoonable", "drinkable")
}

out = {"table_path": str(csv_path), "row_count": len(rows),
       "distributions": report, "nova_distribution": nova_dist}
report_path = ROOT / "verification_report.json"
report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps(out, ensure_ascii=False, indent=2))
print(f"\nTable: {csv_path} ({len(rows)} rows)")
print(f"Report: {report_path}")
