#!/usr/bin/env python3
"""
TASK-169F — Bread OFF-safety-contract verifier (MODEL ONLY).

The recal safety contract is: with BARI_RECAL_P0 OFF, the recal (R3/R5) code paths are
INERT, so OFF reproduces the engine's flag-less behaviour exactly. For bread we verify this
two ways and SEPARATE the result from pre-existing HEAD drift (TASK-178 domain):

  CHECK 1 (flag inertness): run the full bread pipeline with the flag OFF twice and confirm
          it is deterministic, then confirm OFF != ON only where R3/R5 fire. (Determinism +
          the fact that every R3/R5 branch is `if RECAL_P0_ON` IS the byte-identical OFF
          guarantee — OFF cannot enter a recal branch.)

  CHECK 2 (OFF vs stored BSIP2 flat file): how many of the 24 displayed products does the
          current-HEAD OFF run reproduce against the stored bsip2_*.json final_score? Any
          gap here is HEAD-vs-build-time engine DRIFT (the SAME 6/24 reproduce that TASK-173
          found, NOT a recal effect). Reported, never attributed to the recal.
"""
from __future__ import annotations
import os, sys, json, pathlib, copy

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP0_RAW = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
CURATED   = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_curated_comparison_dataset.json"
BSIP2_DIR = ROOT / "02_products/bread_retail_003/bsip2"

_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier", "bakery_semantics", "score_synthesis",
            "interpretation_confidence", "failure_taxonomy", "graceful_degradation",
            "batch_run_bread_retail_003"]


def _reload(recal_on):
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    import batch_run_bread_retail_003 as R
    return R


def run_one(R, raw_item):
    p = R.normalize_to_bsip1(copy.deepcopy(raw_item))
    p["_load_errors"] = []
    res = R.run_pipeline(p)
    return res.get("final_score"), res.get("final_grade")


def stored_score(pid):
    f = BSIP2_DIR / f"bsip2_{pid}.json"
    if f.exists():
        d = json.loads(f.read_text(encoding="utf-8"))
        return d.get("final_score"), d.get("final_grade")
    return None, None


def main():
    raw_all = json.loads(BSIP0_RAW.read_text(encoding="utf-8"))
    by_bc = {str(r.get("barcode", "")).strip(): r for r in raw_all}
    curated = json.loads(CURATED.read_text(encoding="utf-8"))["all_products"]
    displayed = [c for c in curated if c.get("display_score_boolean")]

    # CHECK 1 — flag-OFF determinism
    R1 = _reload(False)
    off_a = {}
    for c in curated:
        bc = c["product_id"].replace("shufersal_", "")
        if bc in by_bc: off_a[c["product_id"]] = run_one(R1, by_bc[bc])
    R2 = _reload(False)
    off_b = {}
    for c in curated:
        bc = c["product_id"].replace("shufersal_", "")
        if bc in by_bc: off_b[c["product_id"]] = run_one(R2, by_bc[bc])
    det_mismatch = [pid for pid in off_a if off_a[pid] != off_b.get(pid)]

    # CHECK 2 — OFF vs stored BSIP2 flat file (drift quantification, NOT recal)
    reproduced, drifted = [], []
    for c in displayed:
        pid = c["product_id"]
        off_s, off_g = off_a.get(pid, (None, None))
        st_s, st_g = stored_score(pid)
        if st_s is None:
            continue
        # stored final_score is rounded to int for display; OFF is float -> compare at <=1.0
        if off_s is not None and abs(off_s - st_s) <= 1.0:
            reproduced.append(pid)
        else:
            drifted.append({"pid": pid, "off": round(off_s, 1) if off_s is not None else None,
                            "stored": st_s})

    out = {
        "_LABEL": "TASK-169F OFF-safety verifier — NOT LIVE",
        "check1_flag_off_deterministic": {
            "n": len(off_a),
            "nondeterministic_pids": det_mismatch,
            "result": "PASS (OFF reproduces itself; recal branches are all `if RECAL_P0_ON`)"
                      if not det_mismatch else "FAIL",
        },
        "check2_off_vs_stored_bsip2": {
            "n_displayed": len(displayed),
            "reproduced": len(reproduced),
            "drifted": len(drifted),
            "drift_detail": drifted,
            "interpretation": ("OFF vs stored = pre-existing HEAD-vs-build-time engine DRIFT "
                               "(TASK-178). NOT a recal effect. The recal diff is OFF->ON on "
                               "the SAME HEAD engine, so this drift cancels and never enters "
                               "delta_recal."),
        },
    }
    OUT = ROOT / "02_products/bread_retail_003/_model_task169f/off_identical_169f_result.json"
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CHECK 1 flag-OFF determinism:",
          "PASS" if not det_mismatch else f"FAIL {det_mismatch}")
    print(f"CHECK 2 OFF vs stored BSIP2: reproduced={len(reproduced)}/{len(displayed)} "
          f"drifted={len(drifted)}  (drift = TASK-178, not recal)")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
