"""Compile the full 22-row sentinel grade table + 7 non-sentinel rows for TASK-397."""
from __future__ import annotations
import json, pathlib, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

staging_dir = pathlib.Path(__file__).parent / "products"
baseline_dir = pathlib.Path(r"C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_001\products")
bsip1_dir    = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output")

rows = []
for pid_dir in sorted(staging_dir.iterdir()):
    t_path = pid_dir / "bsip2_trace.json"
    if not t_path.exists():
        continue
    trace = json.loads(t_path.read_text(encoding="utf-8"))
    barcode = trace.get("input_reference", {}).get("barcode", "")

    # Load baseline
    base_path = baseline_dir / pid_dir.name / "bsip2_trace.json"
    if base_path.exists():
        base = json.loads(base_path.read_text(encoding="utf-8"))
        base_score = base.get("final_score_estimate")
        base_grade = base.get("grade_estimate")
        base_fq    = base.get("dimension_scores", {}).get("fat_quality")
    else:
        base_score = base_grade = base_fq = None

    # Load BSIP1 for fat_sentinel
    bsip1_path = bsip1_dir / f"bsip1_{barcode}.json"
    fat_sentinel = False
    if bsip1_path.exists():
        p1 = json.loads(bsip1_path.read_text(encoding="utf-8"))
        fat_sentinel = p1.get("normalized_nutrition_per_100g", {}).get("fat_sentinel", False)

    new_score = trace.get("final_score_estimate")
    new_grade = trace.get("grade_estimate")
    new_fq    = trace.get("dimension_scores", {}).get("fat_quality")

    rows.append({
        "barcode":      barcode,
        "pid":          pid_dir.name,
        "fat_sentinel": fat_sentinel,
        "base_score":   base_score,
        "base_grade":   base_grade,
        "base_fq":      base_fq,
        "new_score":    new_score,
        "new_grade":    new_grade,
        "new_fq":       new_fq,
        "grade_move":   base_grade != new_grade if base_grade else None,
    })

# Sort: sentinels first, then non-sentinels
rows.sort(key=lambda r: (not r["fat_sentinel"], r["barcode"]))

print("=" * 110)
print("TASK-397 Grade Table: Bread Sentinel Re-score")
print("Baseline: run_bread_conform_001 | Staging: task397_rescore (BARI_FAT_SENTINEL_V1=on)")
print("=" * 110)
print(f"{'barcode':<16} | {'sentinel':<8} | {'base_score':<10} | {'base_grade':<10} | {'new_score':<10} | {'new_grade':<10} | {'base_fq':<8} | {'new_fq':<8} | move?")
print("-" * 110)

sentinel_rows = [r for r in rows if r["fat_sentinel"]]
nonsentinel_rows = [r for r in rows if not r["fat_sentinel"]]

for r in sentinel_rows:
    move_marker = "MOVE" if r.get("grade_move") else "same"
    print(f"{r['barcode']:<16} | {'True':<8} | {str(r['base_score']):<10} | {str(r['base_grade']):<10} | {str(r['new_score']):<10} | {str(r['new_grade']):<10} | {str(r['base_fq']):<8} | {str(r['new_fq']):<8} | {move_marker}")

print(f"\n--- Non-sentinel (must be unchanged) ---")
for r in nonsentinel_rows:
    move_marker = "MOVE ***" if r.get("grade_move") else "same"
    print(f"{r['barcode']:<16} | {'False':<8} | {str(r['base_score']):<10} | {str(r['base_grade']):<10} | {str(r['new_score']):<10} | {str(r['new_grade']):<10} | {str(r['base_fq']):<8} | {str(r['new_fq']):<8} | {move_marker}")

print(f"\nSummary:")
print(f"  Sentinel rows: {len(sentinel_rows)}")
print(f"  Non-sentinel rows: {len(nonsentinel_rows)}")
grade_movers = [r for r in rows if r.get("grade_move")]
print(f"  Grade moves: {len(grade_movers)}")
for r in grade_movers:
    print(f"    {r['barcode']}: {r['base_grade']} -> {r['new_grade']}")
