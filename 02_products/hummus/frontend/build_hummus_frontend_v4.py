#!/usr/bin/env python3
"""
TASK-169B — Hummus frontend v4 (BARI_RECAL_P0=ON recalibration), STAGED, NOT live.

Takes the live hummus_frontend_v3.json structure as the template and swaps in the
NEW recalibrated score/grade for each product from run_hummus_003 (engine 0.4.1 +
BARI_RECAL_P0=on, same corpus as the frozen run_hummus_002 baseline). EVERYTHING
else (nutrition panel, ingredients, confidence, insightLine, positiveSignals,
limitingFactors, unknowns, caveats, _product_type, ordering) is carried verbatim
from v3 — those are Content/explanation-layer concerns that TASK-169B hands off to
Content (insight lines referencing old positions/grades are now stale; see report).

Re-sorts the products by the NEW score (the VM contract is pre-ordered scored-desc;
UI never sorts). Writes a NEW versioned filename; does NOT change the page import.

Source of NEW scores : run_hummus_003 BSIP2 traces (keyed by canonical_product_id).
Template            : live hummus_frontend_v3.json (deployed).
Output              : C:\\bari\\bari-web\\src\\data\\comparisons\\hummus_frontend_v4.json
"""
import json, glob, os, io, datetime, collections, statistics

LIVE_V3 = r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v3.json"
TRACES  = r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_003\products\*\bsip2_trace.json"
OUT     = r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v4.json"
GENERATED = datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    v3 = json.load(io.open(LIVE_V3, encoding="utf-8"))

    # NEW recalibrated scores keyed by canonical_product_id (== VM id).
    new = {}
    for tf in glob.glob(TRACES):
        t = json.load(io.open(tf, encoding="utf-8"))
        pid = (t.get("input_reference") or {}).get("canonical_product_id")
        new[pid] = {
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "ds": t.get("data_sufficiency"),
        }

    changed = []
    missing = []
    for p in v3["products"]:
        pid = p["id"]
        nv = new.get(pid)
        if nv is None:
            missing.append(pid)
            continue
        old_score, old_grade = p.get("score"), p.get("grade")
        # Preserve the v3 confidence/insufficient display contract: products that were
        # score-unavailable in v3 (score is None) stay None — recal does not invent data.
        if old_score is None:
            continue
        ns = nv["score"]
        ns_disp = None if ns is None else int(round(ns + 1e-9)) if float(ns).is_integer() else round(ns)
        # ScoreChip renders Math.round (round-half-up). Mirror it.
        import math
        ns_disp = None if ns is None else int(math.floor(ns + 0.5))
        if ns_disp != old_score or nv["grade"] != old_grade:
            changed.append({
                "id": pid, "name": p.get("name"), "_product_type": p.get("_product_type"),
                "old_score": old_score, "old_grade": old_grade,
                "new_score": ns_disp, "new_grade": nv["grade"],
            })
        p["score"] = ns_disp
        p["grade"] = nv["grade"]

    # Re-order scored-desc, score=None last, stable by id.
    v3["products"].sort(key=lambda d: (-(d["score"] if d["score"] is not None else -1), str(d["id"])))

    scores = [p["score"] for p in v3["products"] if p["score"] is not None]
    grade_dist = collections.Counter(p["grade"] for p in v3["products"])

    m = v3["_meta"]
    m["generated"] = GENERATED
    m["version"] = "v4-recal_p0-staged"
    m["staged_not_live"] = True
    m["source_run_id"] = "run_hummus_003"
    m["recal_p0"] = "on"
    m["grade_distribution"] = dict(grade_dist)
    if scores:
        m["score_statistics"] = {
            "count": len(scores), "min": min(scores), "max": max(scores),
            "mean": round(statistics.mean(scores), 2), "median": round(statistics.median(scores), 2),
        }
    m["recal_provenance"] = {
        "task": "TASK-169B",
        "engine": "proto_v0 / 0.4.1 + BARI_RECAL_P0=on",
        "scores_swapped_from": "run_hummus_003 BSIP2 traces (R1 protein / R3 leanness / R5 sat-fat / R6 veg-spread)",
        "carried_verbatim_from_v3": ["nutrition", "ingredients", "confidence", "insightLine",
                                      "positiveSignals", "limitingFactors", "unknowns", "caveats", "_product_type"],
        "content_handoff": "insightLine / positiveSignals / limitingFactors reference OLD scores & positions and are now STALE — Content Agent must rewrite (TASK-169B report (b)).",
        "live_repoint": "NONE — page still imports hummus_frontend_v3.json.",
    }

    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(v3, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("WROTE", OUT)
    print(f"products {len(v3['products'])} | scored {len(scores)} | grade {dict(grade_dist)}")
    print(f"score/grade changed: {len(changed)} | missing-from-run_003: {len(missing)} {missing[:5]}")


if __name__ == "__main__":
    main()
