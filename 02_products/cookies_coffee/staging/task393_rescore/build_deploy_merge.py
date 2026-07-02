# -*- coding: utf-8 -*-
"""TASK-393 deploy merge: start from LIVE (preserves array order, rank, all display fields,
no PENDING), apply ONLY the staged re-score (score+grade) + the intentional copy rewrites.
Produces the deploy artifact; does NOT touch bari-web or git."""
import json

LIVE = r"C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json"
STAGED = r"C:\Bari\02_products\cookies_coffee\staging\task393_rescore\cookies_coffee_task393_staged.json"
OUT = r"C:\Bari\02_products\cookies_coffee\staging\task393_rescore\cookies_coffee_DEPLOY.json"
COPY_FIELDS = ["rowVerdict", "insightLine", "consumerTakeaway", "comparisonContext"]

live = json.load(open(LIVE, encoding="utf-8"))
stg = json.load(open(STAGED, encoding="utf-8"))
sp = {p.get("barcode"): p for p in stg["products"]}

score_updates = 0; grade_updates = 0; copy_updates = {f: 0 for f in COPY_FIELDS}
audit = {"score_moved": [], "grade_moved": [], "copy_changed": []}

for p in live["products"]:
    bc = p.get("barcode")
    s = sp.get(bc)
    if not s:
        continue
    # 1) score + grade from staged (the re-score truth)
    if s.get("score") is not None and s.get("score") != p.get("score"):
        audit["score_moved"].append({"bc": bc, "old": p.get("score"), "new": s.get("score")})
        p["score"] = s["score"]; score_updates += 1
    if s.get("grade") and s.get("grade") != p.get("grade"):
        audit["grade_moved"].append({"bc": bc, "old": p.get("grade"), "new": s.get("grade")})
        p["grade"] = s["grade"]; grade_updates += 1
    # 2) intentional copy rewrites: staged non-PENDING and differs from live
    for f in COPY_FIELDS:
        sv = s.get(f)
        if isinstance(sv, str) and "PENDING" in sv:
            continue
        if sv is not None and sv != p.get(f):
            p[f] = sv; copy_updates[f] += 1
            audit["copy_changed"].append({"bc": bc, "field": f})

# refresh _meta provenance (TASK-406 discipline)
live.setdefault("_meta", {})
live["_meta"]["run_id"] = "run_cookies_task393_d4on"
live["_meta"]["task393_rescore"] = {
    "flag_change": "BARI_D4_SCORE_V1=on (cookies brought to live D4 state)",
    "grade_moves": audit["grade_moved"], "score_updates": score_updates,
    "copy_updates": copy_updates, "source_staging": STAGED,
}

json.dump(live, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("score_updates", score_updates, "| grade_updates", grade_updates, "| copy_updates", copy_updates)
print("grade moves:", audit["grade_moved"])
print("OUT:", OUT)
