# -*- coding: utf-8 -*-
import json
from pathlib import Path

V1 = Path(r"c:\Bari\02_products\maadanim\maadanim_frontend_v1.json")
V2 = Path(r"c:\Bari\02_products\maadanim\maadanim_frontend_v2.json")
OUT = Path(r"c:\Users\HP\bari\scripts\maadanim-v1-v2-audit.json")

FALSE_FRUIT = "בסיס פרי נראה ברשימה — לא רק טעם מלאכותי"

def exp_fields(exp):
    return {
        "positiveSignals": exp.get("positiveSignals") or [],
        "limitingFactors": exp.get("limitingFactors") or [],
        "bottomLine": exp.get("bottomLine") or "",
        "comparisonContext": exp.get("comparisonContext") or "",
    }

def diff_exp(before, after):
    b, a = exp_fields(before), exp_fields(after)
    changes = {}
    for key in b:
        if b[key] != a[key]:
            changes[key] = {"before": b[key], "after": a[key]}
    return changes

with V1.open(encoding="utf-8") as f:
    v1 = json.load(f)
with V2.open(encoding="utf-8") as f:
    v2 = json.load(f)

v1_by_id = {p["id"]: p for p in v1["products"]}

score_changes = []
exp_only = []
unchanged = []

for p2 in v2["products"]:
    p1 = v1_by_id.get(p2["id"])
    if not p1:
        continue
    score_changed = p1["score"] != p2["score"] or p1.get("grade") != p2.get("grade")
    exp_diff = diff_exp(p1.get("expansion", {}), p2.get("expansion", {}))
    cal = p2.get("_calibration")

    if score_changed:
        score_changes.append({
            "name": p2["name"],
            "id": p2["id"],
            "before_score": p1["score"],
            "after_score": p2["score"],
            "before_grade": p1.get("grade"),
            "after_grade": p2.get("grade"),
            "calibration": cal,
            "expansion_diff": exp_diff,
        })
    elif exp_diff or cal:
        exp_only.append({
            "name": p2["name"],
            "id": p2["id"],
            "score": p2["score"],
            "grade": p2.get("grade"),
            "calibration": cal,
            "expansion_diff": exp_diff,
        })
    else:
        unchanged.append(p2["name"])

report = {
    "score_change_count": len(score_changes),
    "explanation_only_count": len(exp_only),
    "unchanged_count": len(unchanged),
    "score_changes": score_changes,
    "explanation_only": exp_only,
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
    "score_change_count": len(score_changes),
    "explanation_only_count": len(exp_only),
    "unchanged_count": len(unchanged),
}, ensure_ascii=False))
