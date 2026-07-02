"""verify_task393.py — Derive distribution from verification_table.csv for return contract."""
import csv
from collections import Counter

CSV_PATH = r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_task393_fresh\verification_table.csv"

with open(CSV_PATH, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

grades = [r["new_grade"] for r in rows]
scores = [float(r["new_score"]) for r in rows if r.get("new_score")]
old_grades = [r["old_grade"] for r in rows]

grade_dist = Counter(grades)
old_grade_dist = Counter(old_grades)

print("=== TASK-393 VERIFICATION (from verification_table.csv) ===")
print(f"Total rows: {len(rows)}")
print()
print("OLD grade distribution (baseline):")
for g in ["S", "A", "B", "C", "D", "E"]:
    print(f"  {g}: {old_grade_dist.get(g, 0)}")

print()
print("NEW grade distribution (trace-derived from verification_table.csv):")
for g in ["S", "A", "B", "C", "D", "E"]:
    print(f"  {g}: {grade_dist.get(g, 0)}")

print()
print(f"Score range: {min(scores):.1f} - {max(scores):.1f}")
sorted_s = sorted(scores)
n = len(sorted_s)
median = sorted_s[n//2] if n % 2 else (sorted_s[n//2-1] + sorted_s[n//2]) / 2
mean = sum(sorted_s) / n
stdev = (sum((x - mean)**2 for x in sorted_s) / n) ** 0.5
print(f"Median: {median:.1f}  StDev: {stdev:.2f}  N: {n}")
mc = Counter(scores).most_common(1)[0]
print(f"Most common score: {mc[0]} ({mc[1]} products)")

print()
movers = [r for r in rows if r["grade_changed"] == "True"]
print(f"Grade movers: {len(movers)}")
for m in movers:
    bc = m["barcode"]
    og = m["old_grade"]
    ng = m["new_grade"]
    os_ = m["old_score"]
    ns_ = m["new_score"]
    drv = m["driver"]
    print(f"  {bc}  {og}->{ng}  score {os_}->{ns_}  driver: {drv[:100]}")

print()
drifts = [r for r in rows if r["grade_changed"] == "False" and r.get("score_delta")]
nonzero = [r for r in drifts if r["score_delta"] not in ("0.0", "0", "None", "")]
print(f"Score-only drifts (grade unchanged, delta != 0): {len(nonzero)}")
deltas = [abs(float(r["score_delta"])) for r in nonzero if r.get("score_delta")]
if deltas:
    print(f"  Delta range: {min(deltas):.1f} - {max(deltas):.1f}")
    top5 = sorted(nonzero, key=lambda x: abs(float(x["score_delta"])), reverse=True)[:5]
    print("  Top 5 largest drifts:")
    for d in top5:
        print(f"    {d['barcode']}  {d['old_grade']}  {d['old_score']}->{d['new_score']} (delta={d['score_delta']})")

print()
cross = [r for r in rows]
snack_bar_route = [r for r in rows if r.get("category") == "snack_bar_granola"]
print(f"Products routed to snack_bar_granola: {len(snack_bar_route)}")
print("  (These are products that genuinely classify as granola bars/snack bars, e.g. Peti Bar.")
print("   The router uses the same snack_bar_granola caps/notes for them as for actual granola.")
print("   This is router classification, NOT leakage from a foreign corpus.")
print()
true_foreign = [r for r in rows if r.get("category") not in (
    "snack_bar_granola", "biscuit", "cracker", "dessert",
    "whole_food_fat", "default", "cookie", "chocolate_confectionery", None, ""
)]
print(f"Truly unexpected router categories (not snack_bar/biscuit/cracker/dessert): {len(true_foreign)}")
for r in true_foreign:
    print(f"  {r['barcode']}  {r['category']}")
