import json, os, glob, math, statistics

BASE = r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_001\products"
subdirs = sorted(glob.glob(os.path.join(BASE, "*", "bsip2_trace.json")))

print(f"Found {len(subdirs)} trace files")
assert len(subdirs) == 61, f"Expected 61, got {len(subdirs)}"

grades = []
scores = []
categories = {}
context_flags = {}
off_used_count = 0
brined_food_count = 0
two_plus_red_labels_count = 0
binding_cap_hist = {}
all_fired_caps = {}
grade_by_cat = {}

for fp in subdirs:
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    
    # Grade
    grade = d.get("grade_estimate")
    grades.append(grade)
    
    # Score
    score = d.get("final_score_estimate")
    if score is not None:
        scores.append(score)
    
    # Category
    cat = d.get("category")
    categories[cat] = categories.get(cat, 0) + 1
    
    # Context flag
    cf = d.get("context_flag")
    context_flags[fp] = cf
    if cf == "brined_food":
        brined_food_count += 1
    
    # OFF
    off = d.get("off_used", False) or d.get("off_source_used", False)
    if off:
        off_used_count += 1
    
    # Red labels count - check for ISRAELI_RED_LABELS_2_PLUS in caps_considered
    has_2plus = False
    for cap in d.get("caps_considered", []):
        if cap.get("rule") == "ISRAELI_RED_LABELS_2_PLUS" and cap.get("fired") == True:
            has_2plus = True
    # Also check red_label_count if available
    rlc = d.get("L3_inferred_classifications", {}).get("red_label_count", 0)
    if rlc >= 2:
        if not has_2plus:
            pass  # conservative: use cap firing
    if has_2plus:
        two_plus_red_labels_count += 1
    
    # Binding cap
    bc = d.get("binding_cap")
    if bc is not None:
        bc_key = str(bc)
        binding_cap_hist[bc_key] = binding_cap_hist.get(bc_key, 0) + 1
    
    # Fired caps
    for cap in d.get("caps_considered", []):
        if cap.get("fired"):
            rn = cap.get("rule", "UNKNOWN")
            all_fired_caps[rn] = all_fired_caps.get(rn, 0) + 1
    
    # Grade by category
    if cat not in grade_by_cat:
        grade_by_cat[cat] = {}
    grade_by_cat[cat][grade] = grade_by_cat[cat].get(grade, 0) + 1

# --- TALLIES ---
print("\n=== 1. GRADE DISTRIBUTION ===")
for g in ["A","B","C","D","E"]:
    cnt = grades.count(g)
    print(f"{g}: {cnt}")

print("\n=== 2. SCORE STATS ===")
print(f"Count: {len(scores)}")
print(f"Min: {min(scores)}")
print(f"Max: {max(scores)}")
sorted_scores = sorted(scores)
median = statistics.median(sorted_scores)
mean = statistics.mean(sorted_scores)
stdev = statistics.stdev(sorted_scores)
print(f"Median: {median}")
print(f"Mean: {mean:.2f}")
print(f"Stdev: {stdev:.2f}")
# most common score
from collections import Counter
score_counter = Counter(scores)
most_common_score, most_common_count = score_counter.most_common(1)[0]
print(f"Most common score: {most_common_score} (x{most_common_count})")
print(f"Full score histogram:")
for val, cnt in sorted(score_counter.items()):
    print(f"  {val}: {cnt}")

print("\n=== 3. OFF USED ===")
print(f"off_used/off_source_used = true: {off_used_count}")

print("\n=== 4. BRINED FOOD ===")
print(f"context_flag == brined_food: {brined_food_count}")

print("\n=== 5. ROUTING TALLY ===")
for cat, cnt in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {cnt}")

print("\n=== 6. BINDING CAP HISTOGRAM ===")
for bc, cnt in sorted(binding_cap_hist.items(), key=lambda x: -x[1]):
    print(f"  {bc}: {cnt}")

print("\n=== FIRED CAP NAMES (all) ===")
for rn, cnt in sorted(all_fired_caps.items(), key=lambda x: -x[1]):
    print(f"  {rn}: {cnt}")

print("\n=== 7. 2+ RED LABELS ===")
print(f"ISRAELI_RED_LABELS_2_PLUS fired: {two_plus_red_labels_count}")

print("\n=== 8. GRADE BY CATEGORY ===")
for cat in sorted(grade_by_cat.keys()):
    gdict = grade_by_cat[cat]
    parts = []
    for g in ["A","B","C","D","E"]:
        if g in gdict:
            parts.append(f"{g}={gdict[g]}")
    print(f"  {cat}: {', '.join(parts)}")
