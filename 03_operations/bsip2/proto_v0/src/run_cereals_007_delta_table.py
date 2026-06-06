"""
TASK-189 — run_cereals_007_sodium delta table generator.
Compares run_cereals_006 (baseline) vs run_cereals_007_sodium (BARI_SODIUM_CEREAL=on).
Outputs JSON delta table + human-readable console summary.
"""

import sys
import json
import pathlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASELINE_ROOT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_006\products")
NEW_ROOT      = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_007_sodium\products")
REPORT_ROOT   = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")


def load_traces(root: pathlib.Path) -> dict:
    traces = {}
    for prod_dir in sorted(root.iterdir()):
        tpath = prod_dir / "bsip2_trace.json"
        if tpath.exists():
            with open(tpath, encoding="utf-8") as f:
                t = json.load(f)
            ref = t.get("input_reference") or {}
            pid = ref.get("canonical_product_id") or t.get("canonical_product_id")
            traces[pid] = t
    return traces


baseline = load_traces(BASELINE_ROOT)
new_run   = load_traces(NEW_ROOT)

print(f"Baseline products: {len(baseline)}")
print(f"New run products:  {len(new_run)}")

delta_rows = []
for pid, new_t in new_run.items():
    base_t = baseline.get(pid)
    if not base_t:
        continue
    ref = new_t.get("input_reference") or {}
    name = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
    old_score = base_t.get("final_score_estimate")
    new_score = new_t.get("final_score_estimate")
    old_grade = base_t.get("grade_estimate")
    new_grade = new_t.get("grade_estimate")
    if old_score is None or new_score is None:
        continue

    l1 = new_t.get("L1_observed_signals") or {}
    sodium_mg = l1.get("sodium_mg")
    category  = new_t.get("category")
    delta     = round(new_score - old_score, 1)
    grade_moved = (old_grade != new_grade)

    # What sodium rules fired in the new run?
    sodium_rules = []
    for p in new_t.get("penalties_considered", []):
        if "SODIUM" in p.get("rule", "") and p.get("fired"):
            sodium_rules.append(p["rule"])
    for c in new_t.get("caps_considered", []):
        if "SODIUM" in c.get("rule", "") and c.get("fired"):
            sodium_rules.append(c["rule"])

    delta_rows.append({
        "pid": pid,
        "name": name,
        "category": category,
        "sodium_mg": sodium_mg,
        "old_score": old_score,
        "new_score": new_score,
        "delta": delta,
        "old_grade": old_grade,
        "new_grade": new_grade,
        "grade_moved": grade_moved,
        "sodium_rules_fired": sodium_rules,
    })

delta_rows.sort(key=lambda r: r["delta"])

# Save
REPORT_ROOT.mkdir(parents=True, exist_ok=True)
delta_path = REPORT_ROOT / "run_cereals_007_sodium_delta.json"
delta_path.write_text(json.dumps(delta_rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nDelta table saved to: {delta_path}")

# Summarise
movers      = [r for r in delta_rows if r["delta"] != 0.0]
grade_movers = [r for r in delta_rows if r["grade_moved"]]

old_dist, new_dist = {}, {}
for r in delta_rows:
    old_dist[r["old_grade"]] = old_dist.get(r["old_grade"], 0) + 1
    new_dist[r["new_grade"]] = new_dist.get(r["new_grade"], 0) + 1

print("\n" + "="*80)
print("TASK-189 — run_cereals_007_sodium — Before/After Delta")
print("="*80)
print(f"\nProducts scored: {len(delta_rows)}")
print(f"Products with score change: {len(movers)} / {len(delta_rows)}")
print(f"Products with grade change: {len(grade_movers)}")
print(f"\nGrade distribution:")
for g in ["A", "B", "C", "D", "E"]:
    ob = old_dist.get(g, 0)
    nb = new_dist.get(g, 0)
    marker = " <-- CHANGED" if ob != nb else ""
    print(f"  {g}: {ob} → {nb}{marker}")

if movers:
    print(f"\nAll products with score change (sorted by delta, flag ON vs run_006):")
    print(f"{'Name':45s} {'Sod':6s} {'Before':8s} {'After':7s} {'Delta':6s} {'Grade':12s}")
    print("-"*92)
    for r in movers:
        name = r["name"][:43]
        sod = f"{r['sodium_mg']:.0f}" if r["sodium_mg"] is not None else "null"
        grade_str = f"{r['old_grade']}→{r['new_grade']}" if r["grade_moved"] else f"{r['old_grade']} (unchanged)"
        print(f"{name:45s} {sod:6s} {r['old_score']:8.1f} {r['new_score']:7.1f} {r['delta']:+6.1f} {grade_str}")
else:
    print("\nNo score changes detected.")
