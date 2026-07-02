"""TASK-378: Scan copy fields for almond milk and other products needing revision."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

data = json.load(open(r"C:\bari\bari-web\src\data\comparisons\milk_frontend_v1.json", encoding="utf-8"))
products = data["products"]

am = [p for p in products if p["barcode"] == "7290014760141"][0]

print("=== ALMOND MILK COPY FIELDS ===")
print(f"score: {am['score']}, grade: {am['grade']}, rank: {am['rank']}")
print(f"insightLine: {am.get('insightLine','')!r}")
print(f"rowVerdict: {am.get('rowVerdict','')!r}")
exp = am.get("expansion", {})
print("positiveSignals:")
for s in exp.get("positiveSignals", []):
    print(f"  - {s!r}")
print("limitingFactors:")
for s in exp.get("limitingFactors", []):
    print(f"  - {s!r}")
print(f"comparisonContext: {exp.get('comparisonContext','')!r}")

# Check for copy inconsistencies in almond milk
print()
print("=== COPY ISSUES IN ALMOND MILK ===")
issues = []

rv = am.get("rowVerdict", "")
# rowVerdict says "55 (בינוני)" — old score was 51.5 displayed as 55? Actually it says ‏55
# which is wrong anyway; now score is 49.7/D
if "55" in rv or "בינוני" in rv:
    issues.append(("rowVerdict", rv, "references old score '55' and grade label 'בינוני' (C-tier); now 49.7/D"))
if "C" in rv or "ציון C" in rv:
    issues.append(("rowVerdict", rv, "explicit C grade reference — now D"))

# positiveSignals: check for any 'no sugar' / 'low sugar' framing
for s in exp.get("positiveSignals", []):
    if "סוכר" in s and ("נמוך" in s or "אין" in s or "פחות" in s):
        issues.append(("positiveSignals", s, "claims low/no sugar — product has 6g sugar (2nd ingredient)"))

# insightLine: empty, ok
# Check other products that might reference almond milk's old position
print()
print("=== OTHER PRODUCTS: CHECK FOR ALMOND-MILK-RELATIVE LINES ===")
almond_refs = []
for p in products:
    if p["barcode"] == "7290014760141":
        continue
    pexp = p.get("expansion", {})
    for field in ["comparisonContext", "insightLine", "rowVerdict"]:
        val = pexp.get(field, "") if field != "rowVerdict" and field != "insightLine" else p.get(field, "")
        if "שקד" in (val or "") or "almond" in (val or "").lower():
            almond_refs.append((p["barcode"], p["name"], field, val))
    for s in pexp.get("positiveSignals", []):
        if "שקד" in s or "almond" in s.lower():
            almond_refs.append((p["barcode"], p["name"], "positiveSignals", s))
    for s in pexp.get("limitingFactors", []):
        if "שקד" in s or "almond" in s.lower():
            almond_refs.append((p["barcode"], p["name"], "limitingFactors", s))

if almond_refs:
    for bc, name, field, val in almond_refs:
        print(f"  barcode={bc} ({name}), field={field}: {val!r}")
else:
    print("  None found.")

print()
print("=== SUMMARY OF COPY ISSUES ===")
if issues:
    for field, text, reason in issues:
        print(f"  FIELD: {field}")
        print(f"  TEXT: {text!r}")
        print(f"  REASON: {reason}")
        print()
else:
    print("  None found in positiveSignals. Checking rowVerdict...")
    print(f"  rowVerdict (full): {rv!r}")
    print("  Note: rowVerdict contains old score figure and grade label - needs revision")
