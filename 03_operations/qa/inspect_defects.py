import json
import os
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

OUT_FILE = r"C:\Bari\03_operations\qa\beaver_content_audit_v1.json"

with open(OUT_FILE, encoding="utf-8") as f:
    report = json.load(f)

print("=" * 70)
print("GRADE MISMATCHES (high severity)")
print("=" * 70)
for cat, cd in report["categories"].items():
    mismatches = [d for d in cd["defects"] if d["field"] == "grade" and "mismatch" in d["issue"]]
    if mismatches:
        print(f"\n{cat.upper()}:")
        for d in mismatches:
            print(f"  {d['product_id']} | {d['product_name'][:40]} | {d['issue']}")

print()
print("=" * 70)
print("MISSING rowVerdict -- categories with ALL products missing")
print("=" * 70)
for cat, cd in report["categories"].items():
    s = cd["summary"]
    if s["missing_row_verdict"] == cd["n_products"]:
        print(f"  {cat}: ALL {cd['n_products']} products missing rowVerdict")
    elif s["missing_row_verdict"] > 0:
        print(f"  {cat}: {s['missing_row_verdict']}/{cd['n_products']} products missing rowVerdict")

print()
print("=" * 70)
print("BUTTER -- insightLine issues")
print("=" * 70)
butter = report["categories"]["butter"]
il_issues = [d for d in butter["defects"] if d["field"] == "insightLine" and d["product_id"] != "_category"]
for d in il_issues:
    print(f"  {d['product_id']} | {d['issue']}")

print()
print("=" * 70)
print("BUTTER -- rowVerdict issues")
print("=" * 70)
rv_issues = [d for d in butter["defects"] if d["field"] == "rowVerdict" and d["product_id"] != "_category"]
for d in rv_issues:
    print(f"  {d['product_id']} | {d['issue'][:80]}")

print()
print("=" * 70)
print("BUTTER -- template bleed details")
print("=" * 70)
bleed = [d for d in butter["defects"] if "template_bleed_summary" in d["issue"]]
for d in bleed:
    print(f"  {d['issue'][:120]}")

print()
print("=" * 70)
print("CONFIDENCE invalid values")
print("=" * 70)
for cat, cd in report["categories"].items():
    conf_issues = [d for d in cd["defects"] if d["field"] == "confidence" and "invalid" in d["issue"]]
    if conf_issues:
        print(f"\n{cat.upper()}:")
        for d in conf_issues:
            print(f"  {d['product_id']} | {d['issue']}")

print()
print("=" * 70)
print("BARCODE issues")
print("=" * 70)
for cat, cd in report["categories"].items():
    bc_issues = [d for d in cd["defects"] if d["field"] == "barcode" and d["product_id"] != "_category"]
    if bc_issues:
        print(f"\n{cat.upper()}:")
        for d in bc_issues:
            print(f"  {d['product_id']} | {d['issue']}")

print()
print("=" * 70)
print("SCORE CLUSTERS (low severity)")
print("=" * 70)
for cat, cd in report["categories"].items():
    clusters = cd["summary"]["score_clusters"]
    if clusters:
        print(f"  {cat}: {clusters}")

print()
print("=" * 70)
print("CEREALS -- missing image details")
print("=" * 70)
cereals = report["categories"]["cereals"]
img_issues = [d for d in cereals["defects"] if d["field"] == "imageUrl"]
for d in img_issues:
    print(f"  {d['product_id']} | {d['issue']}")

print()
print("=" * 70)
print("GRANOLA -- missing image details")
print("=" * 70)
granola = report["categories"]["granola"]
img_issues = [d for d in granola["defects"] if d["field"] == "imageUrl"]
for d in img_issues:
    print(f"  {d['product_id']} | {d['issue']}")

print()
print("=" * 70)
print("HUMMUS -- rowVerdict short/missing sample (first 5)")
print("=" * 70)
hummus = report["categories"]["hummus"]
rv_issues = [d for d in hummus["defects"] if d["field"] == "rowVerdict" and d["product_id"] != "_category"]
for d in rv_issues[:5]:
    print(f"  {d['product_id']} | {d['issue'][:80]}")
print(f"  ... and {len(rv_issues)-5} more" if len(rv_issues) > 5 else "")
