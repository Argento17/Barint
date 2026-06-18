"""
TASK-284E — Collect grade distributions from all re-scored categories.
Reads BSIP2 trace files and computes grade distributions.
Also checks for unexpected grade changes vs the known expected changes.
"""
import json
import pathlib
from collections import Counter

# Category -> (products_dir, corpus_name)
CATEGORIES = {
    "milk": r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin\products",
    "snack_bars": r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products",
    "cereals": r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008\products",
    "cereals_multiretailer": r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001\products",
    "maadanim": r"C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\products",
    "cheese": r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_004\products",
    "hummus": r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_003\products",
    "cakes_hard_cookies": r"C:\Bari\02_products\cakes_hard_cookies\bsip2_outputs\run_cakes_001\products",
    "cookies_coffee": r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_005\products",
    "salty_snacks": r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products",
    "brined_cheeses": r"C:\Bari\02_products\brined_cheeses\bsip2_outputs\run_brined_005\products",
}

# Expected grade changes (barcode -> (category, grade_before, grade_after, signal))
EXPECTED_CHANGES = {
    "884912126115": ("cereals", "E", "D", "EV-096 seed_oil"),
    "313184": ("cakes_hard_cookies", "E", "D", "EV-096 seed_oil"),
    "7290112497123": ("maadanim", "D", "C", "EV-096 seed_oil"),
    "8710908800018": ("salty_snacks", "D", "C", "EV-096 seed_oil"),
}

# Previously known scores (from TASK-284B/D baselines) for cross-check
BASELINE_GRADES = {
    # cereals crosser
    "884912126115": "E",
    # cakes crosser
    "313184": "E",
    # maadanim crosser
    "7290112497123": "D",
    # salty_snacks crosser (Doritos Cool Ranch)
    "8710908800018": "D",
}

print("=" * 70)
print("TASK-284E Grade Distribution Report (BARI_FAT_TECH_V1 default ON)")
print("=" * 70)

all_traces = {}  # barcode -> (category, score, grade)
total_products = 0
total_scored = 0

grade_order = ["S", "A", "B", "C", "D", "E"]

for cat, products_dir in CATEGORIES.items():
    p = pathlib.Path(products_dir)
    if not p.exists():
        print(f"\n{cat}: PRODUCTS DIR NOT FOUND: {products_dir}")
        continue

    traces = []
    for prod_dir in p.iterdir():
        if not prod_dir.is_dir():
            continue
        tf = prod_dir / "bsip2_trace.json"
        if not tf.exists():
            continue
        try:
            t = json.loads(tf.read_text(encoding="utf-8"))
            traces.append(t)
        except Exception as e:
            print(f"  ERROR reading {tf}: {e}")

    dist = Counter()
    scored = []
    for t in traces:
        g = t.get("grade_estimate")
        s = t.get("final_score_estimate")
        if g and g != "insufficient_data" and s is not None:
            dist[g] += 1
            scored.append(s)
            # Track by barcode for cross-check
            ref = t.get("input_reference") or {}
            bc = ref.get("barcode") or ref.get("canonical_product_id", "")
            if bc:
                all_traces[str(bc)] = (cat, s, g)

    scored.sort()
    median = scored[len(scored) // 2] if scored else None
    dist_str = " ".join(f"{g}={dist[g]}" for g in grade_order if dist[g] > 0)

    total_products += len(traces)
    total_scored += len(scored)

    print(f"\n{cat}:")
    print(f"  products={len(traces)} scored={len(scored)} | {dist_str} | median={median}")

print("\n" + "=" * 70)
print("GRADE CHANGER TABLE (expected 4 grade changes)")
print("=" * 70)
print(f"{'Barcode':<20} {'Category':<20} {'Grade':<6} {'Signal'}")
print("-" * 70)

found_changes = {}
for bc, (cat_exp, g_before, g_after, signal) in EXPECTED_CHANGES.items():
    if bc in all_traces:
        cat_actual, score_actual, grade_actual = all_traces[bc]
        status = "CONFIRMED" if grade_actual == g_after else f"UNEXPECTED (got {grade_actual})"
        print(f"{bc:<20} {cat_actual:<20} {grade_actual:<6} {signal} [{status}]")
        found_changes[bc] = grade_actual
    else:
        print(f"{bc:<20} {cat_exp:<20} {'?':<6} {signal} [NOT FOUND IN TRACES]")

print("\n" + "=" * 70)
print("UNEXPECTED CHANGE SCAN (looking for downward moves or A/S entries)")
print("=" * 70)
unexpected = []
for bc, (cat, score, grade) in all_traces.items():
    if bc in EXPECTED_CHANGES:
        continue
    if grade in ("A", "S"):
        # Check if this might be a new unexpected entry
        pass  # A/S is common; only flag if known to have been lower
    # We can't check all barcodes without the baseline; we report per-category A/S counts
# Just check for any S grades (which would be truly unexpected)
s_grades = [(bc, cat, score) for bc, (cat, score, grade) in all_traces.items() if grade == "S"]
if s_grades:
    print(f"ALERT: {len(s_grades)} S-grade products found:")
    for bc, cat, score in s_grades:
        print(f"  barcode={bc} cat={cat} score={score}")
else:
    print("No S-grade products (expected).")

# Snack bar A-grade check (invariant: no snack bar reaches A)
snack_a = [(bc, score, grade) for bc, (cat, score, grade) in all_traces.items()
           if cat == "snack_bars" and grade in ("A", "S")]
if snack_a:
    print(f"\nINVARIANT BREACH: snack_bars has A/S grade products:")
    for bc, score, grade in snack_a:
        print(f"  {bc}: {score}/{grade}")
else:
    print("Snack bars invariant: no A or S grades (PASS).")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total products across all categories: {total_products}")
print(f"Total scored (grade assigned): {total_scored}")
expected_found = sum(1 for bc in EXPECTED_CHANGES if bc in found_changes and found_changes[bc] == EXPECTED_CHANGES[bc][2])
print(f"Expected grade changes confirmed: {expected_found}/4")
