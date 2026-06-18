"""
Check if milk C10 was already failing BEFORE my changes by looking at the golive summary.
"""
import json, pathlib

# Check the shelfrel golive summary to see if C10 passed there
golive_summary = pathlib.Path(r"C:\Bari\03_operations\bsip2\runs\shelfrel_golive_001_summary.json")
if golive_summary.exists():
    d = json.loads(golive_summary.read_text(encoding="utf-8"))
    print("Golive summary:", json.dumps(d, indent=2, ensure_ascii=False))
else:
    print("Golive summary not found:", golive_summary)

# Also check the hummus shelfrel_001 summary
hum_sum = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_shelfrel_001\run_summary.json")
d = json.loads(hum_sum.read_text(encoding="utf-8"))
print("\nHummus shelfrel_001 c10_milk_pass:", d.get("c10_milk_pass"))
