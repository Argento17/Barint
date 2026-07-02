"""drift_analysis_task393.py — detailed score-only drift breakdown for TASK-393 return."""
import csv, json
from collections import Counter

CSV = r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_task393_fresh\verification_table.csv"

with open(CSV, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

drifts = [r for r in rows if r["grade_changed"] == "False" and r.get("score_delta") not in ("0.0", "0", "None", "")]
zero   = [r for r in rows if r["grade_changed"] == "False" and r.get("score_delta") in ("0.0", "0")]

print(f"Score-only drifts (non-zero delta): {len(drifts)}")
print(f"Zero-delta products:                {len(zero)}")

up   = [r for r in drifts if float(r["score_delta"]) > 0]
down = [r for r in drifts if float(r["score_delta"]) < 0]

print(f"  Up  (+delta): {len(up)}")
print(f"  Down (-delta): {len(down)}")

print("\nAll upward drifts (sorted by magnitude):")
for r in sorted(up, key=lambda x: float(x["score_delta"]), reverse=True):
    print(f"  {r['barcode'][:22]:22s} {r['old_grade']} {r['old_score']:>6s}->{r['new_score']:<6s} delta={r['score_delta']}  cat={r['category']}")

print("\nAll downward drifts (sorted by magnitude):")
for r in sorted(down, key=lambda x: float(x["score_delta"])):
    print(f"  {r['barcode'][:22]:22s} {r['old_grade']} {r['old_score']:>6s}->{r['new_score']:<6s} delta={r['score_delta']}  cat={r['category']}")

# Histogram of delta magnitudes
mags = [abs(float(r["score_delta"])) for r in drifts]
mag_hist = Counter(round(m, 1) for m in mags)
print("\nDelta magnitude histogram:")
for v in sorted(mag_hist.keys()):
    print(f"  |delta|={v}: {mag_hist[v]}")
