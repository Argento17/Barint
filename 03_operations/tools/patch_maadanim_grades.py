# -*- coding: utf-8 -*-
import json, pathlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

src = pathlib.Path(r"C:\Bari\02_products\maadanim\maadanim_frontend_v2.json")

def expected_grade(score):
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"

data = json.loads(src.read_text(encoding="utf-8"))
fixed = 0
for p in data["products"]:
    s = p.get("score")
    g = p.get("grade")
    if s is not None and g is not None:
        exp = expected_grade(s)
        if exp != g:
            p["grade"] = exp
            fixed += 1

out = json.dumps(data, ensure_ascii=False, indent=2)
src.write_text(out, encoding="utf-8")
print(f"Fixed {fixed} product(s). Size: {src.stat().st_size:,} bytes")

# Verify
data2 = json.loads(src.read_text(encoding="utf-8"))
bad = [(p["name"], p["score"], p["grade"]) for p in data2["products"]
       if p.get("score") is not None and p.get("grade") is not None
       and expected_grade(p["score"]) != p["grade"]]
print(f"Remaining mismatches: {len(bad)}")
