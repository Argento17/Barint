import json, os, glob, statistics
from collections import Counter

trace_dir = r"C:\Bari\02_products\cakes_hard_cookies\bsip2_outputs\run_cakes_001\products"
traces = glob.glob(os.path.join(trace_dir, "*/bsip2_trace.json"))

with open(r"C:\Bari\02_products\cakes_hard_cookies\factory_run_001\corpus_filter.json", encoding="utf-8") as f:
    cf = json.load(f)

in_scored_barcodes = {p["barcode"] for p in cf["products"] if p["decision"] == "IN_SCORED"}
out_of_scope_barcodes = {p["barcode"] for p in cf["products"] if p["decision"] == "OUT_OF_SCOPE"}

total = 0
all_data = []

for path in traces:
    with open(path, encoding="utf-8") as f:
        t = json.load(f)
    barcode = t["input_reference"]["barcode"]
    total += 1
    score = t.get("final_score_estimate")
    grade = t.get("grade_estimate")
    sugar = t["L1_observed_signals"].get("sugars_g")
    category = t.get("category", "default")
    row = {
        "barcode": barcode,
        "name": t["input_reference"].get("product_name_he", "")[:50],
        "score": score, "grade": grade, "sugar": sugar, "category": category,
        "in_scored": barcode in in_scored_barcodes,
        "out_of_scope": barcode in out_of_scope_barcodes,
    }
    all_data.append(row)

print(f"Total traces: {total}")

in_scored_data = [r for r in all_data if r["in_scored"]]
in_scored_with_sugar = [r for r in in_scored_data if r["sugar"] is not None]
print(f"In-scored products (corpus_filter): {len(in_scored_data)}")
print(f"In-scored WITH sugars_g: {len(in_scored_with_sugar)}")
print(f"In-scored WITHOUT sugars_g: {len(in_scored_data) - len(in_scored_with_sugar)}")

vals = sorted([r["sugar"] for r in in_scored_with_sugar])
n = len(vals)
median_v = statistics.median(vals)
q1 = statistics.quantiles(vals, n=4)[0]
q3 = statistics.quantiles(vals, n=4)[2]
iqr = q3 - q1
mad = statistics.median([abs(v - median_v) for v in vals])
robust_scale = max(iqr / 1.349, 1.4826 * mad, 1.40)
p90 = statistics.quantiles(vals, n=10)[8]
p10 = statistics.quantiles(vals, n=10)[0]
mean_v = statistics.mean(vals)
stdev_v = statistics.stdev(vals)

print(f"\n--- SUGAR STATS (in_scored with sugars_g, n={n}) ---")
print(f"min={vals[0]}, max={vals[-1]}, mean={mean_v:.2f}, stdev={stdev_v:.2f}")
print(f"median={median_v:.1f}, Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.3f}")
print(f"MAD={mad:.1f}, 1.4826*MAD={1.4826*mad:.3f}")
print(f"IQR/1.349={iqr/1.349:.3f}")
print(f"robust_scale=max({iqr/1.349:.3f}, {1.4826*mad:.3f}, 1.40)={robust_scale:.3f}")
print(f"P10={p10:.1f}, P90={p90:.1f}")

print("\n--- SUGAR DISTRIBUTION (5g buckets) ---")
buckets = {}
for v in vals:
    b = int(v // 5) * 5
    buckets[b] = buckets.get(b, 0) + 1
for k in sorted(buckets):
    print(f"  {k:3d}-{k+5:3d}g: {buckets[k]:3d}  {'#' * buckets[k]}")

scores_list = [r["score"] for r in in_scored_data if r["score"] is not None]
grade_dist = {}
for r in in_scored_data:
    g = r.get("grade")
    grade_dist[g] = grade_dist.get(g, 0) + 1
print(f"\n--- SCORE DISTRIBUTION (in_scored, n={len(scores_list)}) ---")
print(f"Grade dist: {dict(sorted(grade_dist.items()))}")
print(f"Score mean={statistics.mean(scores_list):.2f} stdev={statistics.stdev(scores_list):.2f}")
print(f"Score min={min(scores_list)} max={max(scores_list)} median={statistics.median(scores_list)}")
score_counts = Counter(scores_list)
print(f"Most common scores: {score_counts.most_common(5)}")

cats = Counter(r["category"] for r in all_data)
print(f"\n--- ROUTER CATEGORIES (all {total} traces) ---")
for cat, cnt in cats.most_common():
    print(f"  {cat}: {cnt}")

oos_with_trace = [r for r in all_data if r["out_of_scope"]]
print(f"\n--- OOS products with traces: {len(oos_with_trace)} ---")
for r in oos_with_trace:
    print(f"  bc={r['barcode']} sugar={r['sugar']} score={r['score']} grade={r['grade']}")

print("\n--- LOW SUGAR (< 10g, in_scored, sorted by sugar) ---")
low_s = [r for r in in_scored_with_sugar if r["sugar"] < 10]
low_s.sort(key=lambda x: x["sugar"])
for r in low_s:
    print(f"  bc={r['barcode']} sugar={r['sugar']} score={r['score']} grade={r['grade']}  {r['name'][:40]}")

print("\n--- HIGH SUGAR (> 35g, in_scored, sorted by sugar desc) ---")
high_s = [r for r in in_scored_with_sugar if r["sugar"] > 35]
high_s.sort(key=lambda x: x["sugar"], reverse=True)
for r in high_s:
    print(f"  bc={r['barcode']} sugar={r['sugar']} score={r['score']} grade={r['grade']}  {r['name'][:40]}")

print("\n--- ALL IN_SCORED sorted by score desc (top 25, with sugar) ---")
scored_sorted = sorted(in_scored_with_sugar, key=lambda x: x["score"] or 0, reverse=True)
for r in scored_sorted[:25]:
    print(f"  bc={r['barcode']} sug={r['sugar']:5.1f} sc={r['score']:5.1f} gr={r['grade']}  {r['name'][:35]}")
print("  ...")
for r in scored_sorted[-10:]:
    print(f"  bc={r['barcode']} sug={r['sugar']:5.1f} sc={r['score']:5.1f} gr={r['grade']}  {r['name'][:35]}")

# Z-score computation for each product (sugar, relative to in_scored_with_sugar pool)
print("\n--- Z-SCORES for low-sugar products ---")
for r in low_s:
    z = (r["sugar"] - median_v) / robust_scale
    print(f"  bc={r['barcode']} sugar={r['sugar']} z={z:.3f} score={r['score']} grade={r['grade']}")

print("\n--- POTENTIAL INV PAIRS (lower-sugar scores <= higher-sugar score) ---")
# Compare within in_scored_with_sugar: find pairs where sugar_A < sugar_B but score_A <= score_B
# Focus on products where z_A < -0.30 (low-sugar outlier) vs any higher-sugar
inv_candidates = []
for r in in_scored_with_sugar:
    z = (r["sugar"] - median_v) / robust_scale
    r["z"] = z

for i, rA in enumerate(in_scored_with_sugar):
    if rA["z"] > -0.30:
        continue  # must be low-sugar
    for rB in in_scored_with_sugar:
        if rB["barcode"] == rA["barcode"]:
            continue
        if rB["sugar"] <= rA["sugar"]:
            continue  # B must be higher sugar
        zB = rB["z"]
        if abs(zB) <= 0.30:
            continue  # B must be outside dead zone too
        if rA["score"] is not None and rB["score"] is not None and rA["score"] <= rB["score"]:
            inv_candidates.append({
                "low": rA, "high": rB,
                "sugar_diff": rB["sugar"] - rA["sugar"],
                "score_diff": rB["score"] - rA["score"],
            })

# Sort by score_diff (how egregious the inversion is)
inv_candidates.sort(key=lambda x: -x["sugar_diff"])
print(f"Found {len(inv_candidates)} inversion pairs")
for ic in inv_candidates[:10]:
    lo = ic["low"]
    hi = ic["high"]
    print(f"  LOW:  bc={lo['barcode']} sug={lo['sugar']:5.1f} z={lo['z']:.2f} sc={lo['score']} gr={lo['grade']}  {lo['name'][:30]}")
    print(f"  HIGH: bc={hi['barcode']} sug={hi['sugar']:5.1f} z={hi['z']:.2f} sc={hi['score']} gr={hi['grade']}  {hi['name'][:30]}")
    print(f"  sugar_diff={ic['sugar_diff']:.1f}g  score_diff={ic['score_diff']:.1f} (positive=high scores MORE)")
    print()
