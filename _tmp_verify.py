import json
from pathlib import Path
r = json.loads(Path("C:/Bari/_baselines/rescore_results_v1.json").read_text(encoding="utf-8"))
s = r["summary"]
total_products = sum(x["total"] for x in s)
total_matched = sum(x["matched"] for x in s)
total_movers = sum(x["movers"] for x in s)
total_grade_movers = sum(x["grade_movers"] for x in s)
print(f"Total products (denominator): {total_products}")
print(f"Total matched: {total_matched}")
print(f"Total movers: {total_movers}")
print(f"Total grade movers: {total_grade_movers}")
print()
for x in s:
    print(f"  {x['category']}: {x['matched']}/{x['total']} | movers={x['movers']} | grade_mv={x['grade_movers']} | up={x['up_moves']}")
