"""
TASK-189 — Phase 1: Sodium independence analysis on run_cereals_006 traces.

For each of the 63 products in the clean run_006 corpus, extract:
  - product name, barcode, archetype (snack_bar_granola vs cereal)
  - sodium_mg
  - fat_pct_of_kcal
  - final_score_estimate, grade_estimate
  - HP_FAT_SODIUM_COMBO fired?
  - sodium band: <150, 150–299, 300–449, 450–599, >=600

Conclusion: for products in 300+ bands that are NOT caught by HP_FAT_SODIUM,
is there a meaningful scoring gap that the SODIUM_LOAD graduated treatment
would address?
"""

import json
import pathlib
import sys
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TRACE_ROOT = pathlib.Path(
    r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_006\products"
)

def sodium_band(mg):
    if mg is None:
        return "null"
    if mg < 150:
        return "<150"
    elif mg < 300:
        return "150-299"
    elif mg < 450:
        return "300-449"
    elif mg < 600:
        return "450-599"
    else:
        return ">=600"

records = []
for prod_dir in sorted(TRACE_ROOT.iterdir()):
    trace_path = prod_dir / "bsip2_trace.json"
    if not trace_path.exists():
        continue
    with open(trace_path, encoding="utf-8") as f:
        trace = json.load(f)

    ref = trace.get("input_reference", {})
    pid = trace.get("canonical_product_id") or ref.get("canonical_product_id", prod_dir.name)
    name = ref.get("product_name_he") or ref.get("canonical_name_he", "")
    category = trace.get("category", "")
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")

    l1 = trace.get("L1_observed_signals", {})
    l2 = trace.get("L2_derived_signals", {})
    sodium_mg = l1.get("sodium_mg")
    fat_pct = l2.get("fat_pct_of_kcal") or l1.get("fat_pct_of_kcal")

    # HP_FAT_SODIUM fired?
    hp_fat_sodium_fired = False
    for p in trace.get("penalties_considered", []):
        if p.get("rule") == "HP_FAT_SODIUM_COMBO":
            hp_fat_sodium_fired = p.get("fired", False)
            break

    # Also check penalties_applied
    hp_fat_sodium_applied = any(
        p.get("rule") == "HP_FAT_SODIUM_COMBO"
        for p in trace.get("penalties_applied", [])
    )

    # HIGH_SODIUM_700MG_PLUS cap fired?
    high_sodium_cap_fired = any(
        c.get("rule") == "HIGH_SODIUM_700MG_PLUS" and c.get("fired", False)
        for c in trace.get("caps_considered", [])
    )

    band = sodium_band(sodium_mg)

    records.append({
        "pid": pid,
        "name": name,
        "category": category,
        "sodium_mg": sodium_mg,
        "fat_pct": fat_pct,
        "score": score,
        "grade": grade,
        "band": band,
        "hp_fat_sodium_fired": hp_fat_sodium_fired or hp_fat_sodium_applied,
        "high_sodium_cap_fired": high_sodium_cap_fired,
    })

# Sort by sodium descending
records.sort(key=lambda r: (r["sodium_mg"] or -1), reverse=True)

print(f"\n{'='*80}")
print(f"TASK-189 — Sodium Independence Analysis — run_cereals_006 ({len(records)} products)")
print(f"{'='*80}\n")

# Band distribution
from collections import Counter
band_counts = Counter(r["band"] for r in records)
print("Sodium band distribution:")
for band in [">=600", "450-599", "300-449", "150-299", "<150", "null"]:
    count = band_counts.get(band, 0)
    print(f"  {band:10s}: {count:3d} products")

print()

# HP_FAT_SODIUM analysis for high-sodium bands
high_bands = ["300-449", "450-599", ">=600"]
high_sodium_records = [r for r in records if r["band"] in high_bands]
print(f"Products with sodium >= 300 mg/100g: {len(high_sodium_records)}")
print()

print("Detail for sodium >= 300 mg band (sorted by sodium desc):")
print(f"{'Name':40s} {'Sod':6s} {'Fat%':6s} {'Score':6s} {'Grd':4s} {'Band':10s} {'HP_Na':6s}")
print("-"*90)
for r in high_sodium_records:
    hp_flag = "YES" if r["hp_fat_sodium_fired"] else "no"
    fat_pct_str = f"{r['fat_pct']:.1f}" if r["fat_pct"] is not None else "null"
    sodium_str = f"{r['sodium_mg']:.0f}" if r["sodium_mg"] is not None else "null"
    score_str = f"{r['score']:.1f}" if r["score"] is not None else "null"
    name_trunc = r["name"][:38] if r["name"] else ""
    print(f"{name_trunc:40s} {sodium_str:6s} {fat_pct_str:6s} {score_str:6s} {r['grade']:4s} {r['band']:10s} {hp_flag:6s}")

print()

# Independence verdict
not_caught = [r for r in high_sodium_records if not r["hp_fat_sodium_fired"]]
caught = [r for r in high_sodium_records if r["hp_fat_sodium_fired"]]
print(f"High-sodium (>=300mg) products CAUGHT by HP_FAT_SODIUM: {len(caught)}")
print(f"High-sodium (>=300mg) products NOT CAUGHT by HP_FAT_SODIUM: {len(not_caught)}")
print()

if not_caught:
    print("Products in 300+ band NOT caught by HP_FAT_SODIUM (potential independent signal):")
    for r in not_caught:
        fat_str = f"{r['fat_pct']:.1f}%" if r["fat_pct"] is not None else "null"
        print(f"  {r['name'][:50]:50s} sodium={r['sodium_mg']:.0f} fat={fat_str} "
              f"score={r['score']:.1f}/{r['grade']}")
    print()
    print("=> SODIUM IS AN INDEPENDENT DRIVER.")
    print("   These products have real elevated sodium but escape HP_FAT_SODIUM because")
    print("   fat_pct is below the 25% threshold. The graduated SODIUM_LOAD treatment")
    print("   would penalize them where the current engine does not.")
else:
    print("=> ALL high-sodium products are already caught by HP_FAT_SODIUM.")
    print("   Graduated SODIUM_LOAD would be redundant — the fat fix did the job.")

print()
print("Full corpus sodium range:")
valid_sodium = [r["sodium_mg"] for r in records if r["sodium_mg"] is not None]
print(f"  min={min(valid_sodium):.0f}, max={max(valid_sodium):.0f}, "
      f"median={sorted(valid_sodium)[len(valid_sodium)//2]:.0f} mg/100g")
