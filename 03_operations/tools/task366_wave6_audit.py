#!/usr/bin/env python3
"""TASK-366 Wave-6 additive sanity check: E322, E414 in 3 in-scope JSONs."""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

FILES = {
    "protein_bars": r"C:\bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json",
    "chocolate_bars": r"C:\bari\bari-web\src\data\comparisons\chocolate_bars_frontend_v1.json",
    "chocolate_tablets": r"C:\bari\bari-web\src\data\comparisons\chocolate_tablets_frontend_v1.json",
}

TARGET_ENUMBERS = {"E322", "E414", "E476"}

# Known expected explanation_he strings from w2_additive_copy_v1.md
EXPECTED = {
    "E322": "לציטין הוא חומר תחליב טבעי המופק מסויה, חמניות או זרעי קנולה; זהה כימית לפוספוליפידים הטבעיים בגוף.",
    "E414": "גומי ערבי הוא סיב טבעי מעץ השיטה המשמש לייצוב ולהסמכה; נחשב בטוח ונפוץ במזון.",
    "E476": "PGPR הוא חומר תחליב סינתטי להפחתת צמיגות בשוקולד; מאושר ברמות הנוכחיות, מותר גם בממרחים דלי-שומן ורטבים.",
}

print("=" * 70)
print("TASK-366 Wave-6 additive audit (E322, E414, E476)")
print("=" * 70)

for label, path in FILES.items():
    print(f"\n--- {label} ---")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    hits = {e: [] for e in TARGET_ENUMBERS}

    def walk(obj):
        if isinstance(obj, dict):
            e_num = obj.get("e_number", "")
            if e_num in TARGET_ENUMBERS:
                hits[e_num].append({
                    "explanation_he": obj.get("explanation_he", ""),
                    "function_he": obj.get("function_he", ""),
                    "tier": obj.get("tier", ""),
                    "name_he": obj.get("name_he", ""),
                })
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)

    for e_num in TARGET_ENUMBERS:
        entries = hits[e_num]
        expected = EXPECTED.get(e_num, "")
        print(f"\n  {e_num}: {len(entries)} entries")
        for i, entry in enumerate(entries):
            exp = entry["explanation_he"]
            char_count = len(exp)
            matches_expected = (exp == expected)
            print(f"    [{i+1}] name_he={entry['name_he']} tier={entry['tier']}")
            print(f"         function_he len={len(entry['function_he'])}")
            print(f"         explanation_he len={char_count} chars")
            print(f"         matches canonical: {matches_expected}")
            if not matches_expected:
                print(f"         ACTUAL repr: {repr(exp[:100])}")
                print(f"         EXPECTED repr: {repr(expected[:100])}")

print("\n[DONE]")
