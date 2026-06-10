"""
ECS-v1 Regression Test Runner — emulsifier_complexity_score validation.

Loads the _emulsifier_complexity function and tests all 22 canonical
regression examples from emulsifier_complexity_regression_v1.md.
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from score_engine import _emulsifier_complexity

PASS = "PASS"; FAIL = "FAIL"

examples = [
    # (name, l3_signals, expected_count, expected_highest, expected_complexity_tier, expected_total)
    # Example 1: Plain almond butter — no agents
    ("1. Plain almond butter",        {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":[]},
     0, 0, "none", 0),
    # Example 2: Peanut butter + lecithin
    ("2. Peanut butter + lecithin",   {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["soy_lecithin"]},
     1, 1, "simple", 1),
    # Example 3: Hummus + guar + xanthan
    ("3. Hummus + guar + xanthan",    {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["guar_gum","xanthan_gum"]},
     2, 1, "moderate", 2),
    # Example 4: Plain Greek yogurt
    ("4. Plain Greek yogurt",         {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":[]},
     0, 0, "none", 0),
    # Example 5: Flavored yogurt + modified starch + pectin
    ("5. Flavored yogurt + mod starch + pectin",
     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":["modified_starch_stabilizer"],"tax_emulsifier_low":["pectin"]},
     2, 3, "moderate", 4),
    # Example 6: Ice cream + CMC + carrageenan + mono/di
    ("6. Ice cream + CMC + carra + mono/di",
     {"tax_emulsifier_concern":["cmc","carrageenan"],"tax_emulsifier_medium":["mono_diglyceride"],"tax_emulsifier_low":[]},
     3, 5, "high", 8),
    # Example 7: Diet shake + CMC + lecithin + gum arabic
    ("7. Diet shake + CMC + lecithin + gum arabic",
     {"tax_emulsifier_concern":["cmc"],"tax_emulsifier_medium":[],"tax_emulsifier_low":["soy_lecithin","gum_arabic"]},
     3, 5, "high", 8),
    # Example 8: Whole milk
    ("8. Whole milk",                 {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":[]},
     0, 0, "none", 0),
    # Example 9: Plain bread
    ("9. Plain bread",                {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":[]},
     0, 0, "none", 0),
    # Example 10: Bread light + E471 + E481 + E466
    ("10. Bread light + E471 + E481 + E466",
     {"tax_emulsifier_concern":["cmc"],"tax_emulsifier_medium":["mono_diglyceride","ssl"],"tax_emulsifier_low":[]},
     3, 5, "high", 8),
    # Example 11: Mayo + guar + xanthan
    ("11. Mayo + guar + xanthan",     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["guar_gum","xanthan_gum"]},
     2, 1, "moderate", 2),
    # Example 12: Snack bar + lecithin + guar
    ("12. Snack bar + lecithin + guar",
     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["soy_lecithin","guar_gum"]},
     2, 1, "moderate", 2),
    # Example 13: Snack bar + P80 + E471 + lecithin + xanthan
    ("13. Snack bar + P80 + E471 + lecithin + xanthan",
     {"tax_emulsifier_concern":["polysorbate_80"],"tax_emulsifier_medium":["mono_diglyceride"],"tax_emulsifier_low":["soy_lecithin","xanthan_gum"]},
     4, 5, "high", 8),
    # Example 14: Cream cheese + carrageenan + LBG
    ("14. Cream cheese + carra + LBG",
     {"tax_emulsifier_concern":["carrageenan"],"tax_emulsifier_medium":[],"tax_emulsifier_low":["locust_bean_gum"]},
     2, 3, "moderate", 4),
    # Example 15: Instant pudding + CMC + carra + guar + DATEM + mod starch
    ("15. Instant pudding + CMC + carra + guar + DATEM + mod starch",
     {"tax_emulsifier_concern":["cmc","carrageenan"],"tax_emulsifier_medium":["datem","modified_starch_stabilizer"],"tax_emulsifier_low":["guar_gum"]},
     5, 5, "high", 8),
    # Example 16: Oat milk + CMC + gum arabic
    ("16. Oat milk + CMC + gum arabic",
     {"tax_emulsifier_concern":["cmc"],"tax_emulsifier_medium":[],"tax_emulsifier_low":["gum_arabic"]},
     2, 5, "moderate", 6),
    # Example 17: Coconut milk + guar only
    ("17. Coconut milk + guar only",  {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["guar_gum"]},
     1, 1, "simple", 1),
    # Example 18: Sugar-free gum + CMC + carra + gum arabic + lecithin
    ("18. Sugar-free gum + CMC + carra + gum arabic + lecithin",
     {"tax_emulsifier_concern":["cmc","carrageenan"],"tax_emulsifier_medium":[],"tax_emulsifier_low":["gum_arabic","soy_lecithin"]},
     4, 5, "high", 8),
    # Example 19: Ketchup + xanthan only
    ("19. Ketchup + xanthan only",    {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":["xanthan_gum"]},
     1, 1, "simple", 1),
    # Example 20: Plant yogurt + mod starch + pectin + guar + gellan
    ("20. Plant yogurt + mod starch + pectin + guar + gellan",
     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":["modified_starch_stabilizer"],"tax_emulsifier_low":["pectin","guar_gum","gellan_gum"]},
     4, 3, "high", 6),
    # Example 21: Plain bread + modified starch (position 3, no light/diet) — excluded by gate
    ("21. Bread + mod starch (pos 3, structural)",
     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":[],"tax_emulsifier_low":[]},
     0, 0, "none", 0),
    # Example 22: Bread light + mod starch (pos 8) + E471
    ("22. Bread light + mod starch (pos 8) + E471",
     {"tax_emulsifier_concern":[],"tax_emulsifier_medium":["modified_starch_stabilizer","mono_diglyceride"],"tax_emulsifier_low":[]},
     2, 3, "moderate", 4),
]

results = []
passed = 0; failed = 0

for name, signals, exp_count, exp_highest, exp_tier, exp_total in examples:
    total, note, detail = _emulsifier_complexity(signals)
    checks = []
    # Check agent count
    if detail["distinct_agent_count"] == exp_count:
        checks.append(f"count={exp_count}")
    else:
        checks.append(f"COUNT FAIL: got {detail['distinct_agent_count']} expected {exp_count}")
    # Check highest penalty
    if detail["highest_individual_penalty"] == exp_highest:
        checks.append(f"highest={exp_highest}")
    else:
        checks.append(f"HIGHEST FAIL: got {detail['highest_individual_penalty']} expected {exp_highest}")
    # Check complexity tier
    if detail["complexity_tier"] == exp_tier:
        checks.append(f"tier={exp_tier}")
    else:
        checks.append(f"TIER FAIL: got {detail['complexity_tier']} expected {exp_tier}")
    # Check total
    if total == exp_total:
        checks.append(f"total={exp_total}")
    else:
        checks.append(f"TOTAL FAIL: got {total} expected {exp_total}")

    ok = all("FAIL" not in c for c in checks)
    status = PASS if ok else FAIL
    results.append((name, status, checks, detail))
    if ok: passed += 1
    else: failed += 1

# Report
print("=" * 72)
print("ECS-v1 Regression Results (22 examples)")
print("=" * 72)
for name, status, checks, detail in results:
    mark = "+" if status == PASS else "!"
    print(f"  [{mark}] {name}")
    for c in checks:
        print(f"         {c}")

print("-" * 72)
print(f"  Total: {passed} passed, {failed} failed out of {len(examples)}")
print("=" * 72)

# Summary table
print()
print("Summary table:")
print(f"  {'#' :<5} {'Scenario':<55} {'Count':<7} {'Highest':<8} {'Tier':<12} {'Total':<7} {'Status':<7}")
print(f"  {'-'*5} {'-'*55} {'-'*7} {'-'*8} {'-'*12} {'-'*7} {'-'*7}")
for i, (name, status, checks, detail) in enumerate(results, 1):
    total = detail["total_capped"]
    highest = detail["highest_individual_penalty"]
    tier = detail["complexity_tier"]
    count = detail["distinct_agent_count"]
    short_name = name.split(". ", 1)[1] if ". " in name else name
    print(f"  {i:<5} {short_name:<55} {count:<7} {highest:<8} {tier:<12} {total:<7} {PASS if status==PASS else FAIL}")

sys.exit(0 if failed == 0 else 1)
