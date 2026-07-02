"""
TASK-366 Round-2 verification script.
Checks: JSON parse validity for 5 target files, E476 char count.
Outputs ASCII only to avoid cp1252 issues.
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    r"C:\Bari\bari-web\src\data\comparisons\chocolate_tablets_frontend_v1.json",
    r"C:\Bari\bari-web\src\data\comparisons\chocolate_bars_frontend_v1.json",
    r"C:\Bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json",
    r"C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json",
    r"C:\Bari\bari-web\src\data\comparisons\cakes_hard_cookies_frontend_v1.json",
]

CANONICAL_E476 = "PGPR הוא חומר תחליב סינתטי להפחתת צמיגות בשוקולד; מאושר ברמות הנוכחיות, מותר גם ברטבים מתחלבים ותחליפי שומן."
CANONICAL_E322 = "לציטין הוא חומר תחליב טבעי המופק מסויה, חמניות או זרעי קנולה; זהה כימית לפוספוליפידים הטבעיים בגוף."
# "מסויה או חמניות" — old E322 variant
OLD_E322_VARIANT = "מסויה או חמניות"
# "נחשב בטוח לרוב האנשים"
OLD_SOFT_VERDICT = "נחשב בטוח לרוב האנשים"
# old false clause
OLD_FALSE_CLAUSE_1 = "מסווגים כה'לא מוגדר'"
# "אינו מוכר בשאר שימושי המזון"
OLD_FALSE_CLAUSE_2 = "אינו מוכר בשאר שימושי המזון"

print("=== TASK-366 Round-2 Verification ===")
print(f"E476 canonical char count: {len(CANONICAL_E476)}")
print(f"E322 canonical char count: {len(CANONICAL_E322)}")
print()

all_pass = True
results = {}

for fpath in FILES:
    fname = os.path.basename(fpath)
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            raw = f.read()
        data = json.loads(raw)
        json_ok = True
    except json.JSONDecodeError as e:
        json_ok = False
        all_pass = False
        results[fname] = {"json_ok": False, "error": str(e)}
        print(f"[{fname}] JSON parse: FAIL — {e}")
        continue

    e476_hits = raw.count(CANONICAL_E476)
    e322_canonical_hits = raw.count(CANONICAL_E322)
    old_e322_hits = raw.count(OLD_E322_VARIANT)
    old_soft_hits = raw.count(OLD_SOFT_VERDICT)
    old_false1_hits = raw.count(OLD_FALSE_CLAUSE_1)
    old_false2_hits = raw.count(OLD_FALSE_CLAUSE_2)

    results[fname] = {
        "json_ok": True,
        "e476_hits": e476_hits,
        "e322_canonical_hits": e322_canonical_hits,
        "old_e322_variant_hits": old_e322_hits,
        "old_soft_verdict_hits": old_soft_hits,
        "old_false_clause1_hits": old_false1_hits,
        "old_false_clause2_hits": old_false2_hits,
    }

    print(f"[{fname}]")
    print(f"  JSON parse: PASS")
    print(f"  E476 canonical hits: {e476_hits}")
    print(f"  E322 canonical hits (new): {e322_canonical_hits}")
    print(f"  OLD E322 variant hits: {old_e322_hits}")
    print(f"  OLD soft-verdict hits: {old_soft_hits}")
    print(f"  OLD false-clause1 hits: {old_false1_hits}")
    print(f"  OLD false-clause2 ('aino mokar') hits: {old_false2_hits}")
    print()

print(f"Overall JSON parse: {'ALL PASS' if all_pass else 'FAIL'}")

# E476 total across all files
total_e476 = sum(v.get("e476_hits", 0) for v in results.values())
print(f"Total E476 canonical hits across 5 files: {total_e476} (expected 19)")
total_old_e322 = sum(v.get("old_e322_variant_hits", 0) for v in results.values())
print(f"Total OLD E322 variant hits across 5 files: {total_old_e322} (expected 0)")
total_old_soft = sum(v.get("old_soft_verdict_hits", 0) for v in results.values())
print(f"Total OLD soft-verdict hits across 5 files: {total_old_soft} (expected 0)")
