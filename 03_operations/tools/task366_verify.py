#!/usr/bin/env python3
"""TASK-366 Track-V verification script. Run read-only; never modifies files."""
import json
import sys
import os

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

FILES = {
    "protein_bars": r"C:\bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json",
    "chocolate_bars": r"C:\bari\bari-web\src\data\comparisons\chocolate_bars_frontend_v1.json",
    "chocolate_tablets": r"C:\bari\bari-web\src\data\comparisons\chocolate_tablets_frontend_v1.json",
    "cookies_coffee": r"C:\bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json",
}

NEW_CLAUSE = "PGPR הוא חומר תחליב סינתטי להפחתת צמיגות בשוקולד; מאושר ברמות הנוכחיות, מותר גם בממרחים דלי-שומן ורטבים."
OLD_CLAUSE = "אינו מוכר בשאר שימושי המזון"

print("=" * 70)
print("TASK-366 Track-V verification")
print("=" * 70)

# 1. Character count of new clause
char_count = len(NEW_CLAUSE)
print(f"\n[CHECK-5] Character count of new clause: {char_count}")
print(f"  Limit: 120  Status: {'PASS' if char_count <= 120 else 'FAIL'}")

# 2. JSON parse validity + E476 audit
for label, path in FILES.items():
    print(f"\n[JSON-PARSE] {label}")
    if not os.path.exists(path):
        print(f"  FILE NOT FOUND: {path}")
        continue
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  Parse: PASS")
    except json.JSONDecodeError as e:
        print(f"  Parse: FAIL -- {e}")
        continue

    # Walk all E476 additive entries
    e476_hits = []

    def walk(obj, path_trace=""):
        if isinstance(obj, dict):
            e_num = obj.get("e_number", "")
            if e_num == "E476":
                exp = obj.get("explanation_he", "")
                func = obj.get("function_he", "")
                e476_hits.append({"explanation_he": exp, "function_he": func, "path": path_trace})
            for k, v in obj.items():
                walk(v, path_trace + f".{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, path_trace + f"[{i}]")

    e476_hits.clear()
    walk(data)

    print(f"  E476 entries found: {len(e476_hits)}")
    old_count = 0
    new_count = 0
    other_count = 0
    for i, hit in enumerate(e476_hits):
        exp = hit["explanation_he"]
        has_new = NEW_CLAUSE in exp
        has_old = OLD_CLAUSE in exp
        if has_old:
            old_count += 1
        if has_new:
            new_count += 1
        if not has_new and not has_old:
            other_count += 1
            print(f"  [HIT {i+1}] NEITHER new nor old clause -- explanation_he length={len(exp)}")
            # Print ASCII-safe repr
            print(f"    repr: {repr(exp[:80])}")
    print(f"  hits with NEW clause: {new_count}")
    print(f"  hits with OLD clause: {old_count} {'FAIL' if old_count > 0 else 'PASS'}")
    print(f"  hits with OTHER explanation: {other_count} {'WARN' if other_count > 0 else 'ok'}")

print("\n[DONE]")
