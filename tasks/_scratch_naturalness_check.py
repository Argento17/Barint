"""Run the Layer-1 naturalness gate over every Hebrew string in the magnesium page-data."""
import re, sys, json
sys.path.insert(0, r"C:\Bari")
from integrations.clients.naturalness_gate import analyze

src = open(r"C:\bari\bari-web\src\lib\comparisons\magnesium-page-data.ts", encoding="utf-8").read()

# Extract double-quoted string literals that contain Hebrew letters.
heb = re.compile(r'"((?:[^"\\]|\\.)*)"')
strings = []
for m in heb.finditer(src):
    s = m.group(1)
    if re.search(r'[֐-׿]', s):
        # unescape \n and \" for analysis
        s2 = s.replace('\\n', ' ').replace('\\"', '"')
        strings.append(s2)

# de-dup, keep order
seen = set(); uniq = []
for s in strings:
    if s not in seen:
        seen.add(s); uniq.append(s)

print(f"Hebrew strings analyzed: {len(uniq)}")
high = []
medium = []
for s in uniq:
    r = analyze(s)
    d = r.to_dict()
    flags = d.get("flags", [])
    highs = [f for f in flags if f.get("severity") == "HIGH"]
    meds = [f for f in flags if f.get("severity") == "MEDIUM"]
    if highs:
        high.append((s, highs))
    if meds:
        medium.append((s, meds))

out = {
  "total": len(uniq),
  "high_count": len(high),
  "medium_count": len(medium),
  "high": [{"flags": fl, "text": s} for s, fl in high],
  "medium": [{"flags": fl, "text": s} for s, fl in medium],
}
open(r"C:\Bari\tasks\_scratch_naturalness_result.json","w",encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=2))
print(f"SUMMARY: {len(uniq)} strings | HIGH={len(high)} | MEDIUM={len(medium)} -> wrote _scratch_naturalness_result.json")
