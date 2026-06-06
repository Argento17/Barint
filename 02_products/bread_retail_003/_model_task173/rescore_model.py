#!/usr/bin/env python3
"""
TASK-173 — Bread re-score MODEL (NOT LIVE)
==========================================
MODEL ONLY. Writes nothing to any live file, published score, or frontend JSON.
Output: _model_task173/rescore_model_result.json  (clearly labelled NOT LIVE)

Purpose
-------
For the 24 displayed bread products, empirically determine whether the
BSIP0->signal ingredient NON-PROPAGATION bug (TASK-164/172) DEPRESSED the
live score, by re-running the REAL BSIP2 pipeline twice per product:

  (A) WITH the genuine BSIP0 ingredient list  -> "corrected" (truth)
  (B) WITHOUT ingredients (stripped)           -> "non-propagated" (simulates the bug)

and comparing both to the LIVE frontend score in bread_frontend_v2.json.

If LIVE == A  -> live score already saw ingredients (text-only bug, score NOT depressed)
If LIVE == B  -> live score is the depressed/bugged value; A is the corrected re-score
"""
from __future__ import annotations
import sys, json, pathlib, copy

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Reuse the REAL runner's normalization + pipeline (no reimplementation).
import batch_run_bread_retail_003 as R

ROOT       = pathlib.Path(r"C:\Bari")
BSIP0_RAW  = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
LIVE_FE    = ROOT / "bari-web/src/data/comparisons/bread_frontend_v2.json"
OUT        = ROOT / "02_products/bread_retail_003/_model_task173/rescore_model_result.json"

raw_all = json.loads(BSIP0_RAW.read_text(encoding="utf-8"))
by_bc   = {str(r.get("barcode","")).strip(): r for r in raw_all}

live = json.loads(LIVE_FE.read_text(encoding="utf-8"))
live_by_id = {p["id"]: p for p in live["products"]}

def run_one(raw_item: dict, strip_ingredients: bool) -> dict:
    raw = copy.deepcopy(raw_item)
    if strip_ingredients:
        raw["ingredients_raw"] = ""        # simulate non-propagation to the signal layer
    p = R.normalize_to_bsip1(raw)
    p["_load_errors"] = []
    res = R.run_pipeline(p)
    l3 = res["signals"]["L3_inferred_classifications"]
    return {
        "final_score": res.get("final_score"),
        "final_grade": res.get("final_grade"),
        "has_whole_grain": l3.get("has_whole_grain"),
        "whole_grain_matches": l3.get("whole_grain_matches"),
        "has_fermentation": l3.get("has_fermentation"),
        "nova": res.get("nova_result", {}).get("nova_class") if isinstance(res.get("nova_result"), dict) else None,
        "degradation": res.get("degradation_level"),
    }

def grade(s):
    if s is None: return None
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"

rows = []
for pid, lp in live_by_id.items():
    bc = pid.replace("shufersal_", "")
    raw_item = by_bc.get(bc)
    if not raw_item:
        rows.append({"id": pid, "name": lp["name"], "error": "NOT IN RAW SCRAPE"})
        continue
    a = run_one(raw_item, strip_ingredients=False)   # corrected (with ingredients)
    b = run_one(raw_item, strip_ingredients=True)    # bug simulation (no ingredients)
    live_score = lp.get("score")
    live_grade = lp.get("grade")
    rows.append({
        "id": pid,
        "name": lp["name"],
        "live_score": live_score,
        "live_grade": live_grade,
        "corrected_score": round(a["final_score"],1) if a["final_score"] is not None else None,
        "corrected_grade": a["final_grade"],
        "nonprop_score": round(b["final_score"],1) if b["final_score"] is not None else None,
        "nonprop_grade": b["final_grade"],
        "delta_corrected_vs_nonprop": (round(a["final_score"]-b["final_score"],1)
                                       if (a["final_score"] is not None and b["final_score"] is not None) else None),
        "corrected_has_wg": a["has_whole_grain"],
        "corrected_wg_matches": a["corrected_wg_matches"] if "corrected_wg_matches" in a else a["whole_grain_matches"],
        "nonprop_has_wg": b["has_whole_grain"],
        "ingredients_raw_snippet": (raw_item.get("ingredients_raw","") or "")[:90],
    })

# Which baseline does the LIVE score track?
for r in rows:
    if "error" in r: continue
    ls, cs, ns = r["live_score"], r["corrected_score"], r["nonprop_score"]
    def near(x,y): return (x is not None and y is not None and abs(x-y) <= 1.0)
    r["live_tracks"] = ("corrected_with_ingredients" if near(ls,cs) and not near(ls,ns)
                        else "nonprop_no_ingredients" if near(ls,ns) and not near(ls,cs)
                        else "both_equal" if near(cs,ns)
                        else "neither")

payload = {
    "_LABEL": "TASK-173 RE-SCORE MODEL — NOT LIVE — DO NOT SHIP",
    "_meta": {
        "purpose": "empirical re-score: corrected(with ingredients) vs non-propagated(stripped) vs live",
        "engine_src": str(SRC),
        "run_id": "real_bread_retail_003_v1",
        "live_file": str(LIVE_FE),
        "note": "corrected_score = real BSIP2 pipeline with genuine BSIP0 ingredients; nonprop_score = same pipeline with ingredients stripped (bug sim)",
    },
    "rows": rows,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"WROTE {OUT}")
print(f"{'id':<26}{'live':>6}{'corr':>7}{'nonp':>7}{'dlt':>6}  tracks")
for r in rows:
    if "error" in r:
        print(f"{r['id']:<26}  {r['error']}"); continue
    print(f"{r['id']:<26}{str(r['live_score']):>6}{str(r['corrected_score']):>7}"
          f"{str(r['nonprop_score']):>7}{str(r['delta_corrected_vs_nonprop']):>6}  {r['live_tracks']}")
