#!/usr/bin/env python3
"""
TASK-169F — Bread retail_003 wired into the BARI_RECAL_P0 recal harness (MODEL ONLY).
=====================================================================================
MODEL ONLY. Writes nothing to any live file, published score, or frontend JSON.
Output: _model_task169f/bread_recal_169f_result.json  (clearly labelled NOT LIVE)

Why this file exists
--------------------
real_bread_retail_003_v1 uses a BESPOKE inline BSIP0->BSIP1 normalizer + a multi-stage
pipeline (signal -> router -> nova -> score -> confidence-ceiling -> bakery_semantics ->
structural -> SYNTHESIS). Its final published score is the SYNTHESIS score, not the raw
score_engine output. It was therefore never wired into run_recal_p0_blast_radius.py (a
load_batch dir harness). TASK-169A could only ESTIMATE bread's R3/R5 blast radius.

This runner reuses the REAL runner as a module (same pattern as TASK-173 rescore_model.py)
and runs the ENTIRE bread pipeline twice per product, toggling ONLY BARI_RECAL_P0:
  OFF -> current-HEAD flag-OFF baseline (the recal safety contract reference)
  ON  -> intended R3/R5 recalibration
The delta OFF->ON is therefore PURELY the recal effect on THIS engine. Engine drift vs the
PUBLISHED build-time score is held constant (it appears identically in both OFF and ON) and
is quantified separately (live column) so recal-intended moves are not confused with the
pre-existing HEAD drift that TASK-178 owns.

Corpus = the 31 curated products (24 scored/displayed + 7 transparency-only) from
real_bread_retail_003_v1_curated_comparison_dataset.json.
"""
from __future__ import annotations
import os, sys, json, pathlib, copy, importlib

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP0_RAW = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
CURATED   = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_curated_comparison_dataset.json"
LIVE_FE   = ROOT / "bari-web/src/data/comparisons/bread_frontend_v2.json"
OUTDIR    = ROOT / "02_products/bread_retail_003/_model_task169f"
OUT       = OUTDIR / "bread_recal_169f_result.json"
OUTDIR.mkdir(parents=True, exist_ok=True)

# modules to reload when the flag flips (mirror run_recal_p0_blast_radius._MODULES + bread deps)
_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier", "bakery_semantics", "score_synthesis",
            "interpretation_confidence", "failure_taxonomy", "graceful_degradation",
            "batch_run_bread_retail_003"]


def _reload_engine(recal_on: bool):
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_TASK144_FIXES"] = "off"          # match the published bread build
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"   # bread-irrelevant; keep deterministic
    for m in _MODULES:
        sys.modules.pop(m, None)
    import batch_run_bread_retail_003 as R
    return R


def run_one(R, raw_item: dict) -> dict:
    raw = copy.deepcopy(raw_item)
    p = R.normalize_to_bsip1(raw)
    p["_load_errors"] = []
    res = R.run_pipeline(p)
    sr = res.get("score_result", {}) or {}
    dims = sr.get("dimension_scores", {}) or {}
    notes = sr.get("dimension_notes", {}) or sr.get("notes", {}) or {}
    l3 = res["signals"]["L3_inferred_classifications"]
    return {
        "final_score": res.get("final_score"),
        "final_grade": res.get("final_grade"),
        "engine_score_pre_synth": sr.get("final_score_estimate"),
        "fat_quality_dim": dims.get("fat_quality"),
        "fat_quality_note": notes.get("fat_quality") if isinstance(notes, dict) else None,
        "nova_level": (res.get("nova_result") or {}).get("nova_level"),
        "has_whole_grain": l3.get("has_whole_grain"),
        "red_labels": l3.get("red_labels"),
        "red_label_count": l3.get("red_label_count"),
        "degradation": res.get("degradation_level"),
        "fat_g": (res.get("nutrition") or {}).get("fat_g"),
        "fat_saturated_g": (res.get("nutrition") or {}).get("fat_saturated_g"),
    }


def grade_of(s):
    if s is None: return None
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


def main():
    raw_all = json.loads(BSIP0_RAW.read_text(encoding="utf-8"))
    by_bc = {str(r.get("barcode", "")).strip(): r for r in raw_all}

    curated = json.loads(CURATED.read_text(encoding="utf-8"))["all_products"]
    live = json.loads(LIVE_FE.read_text(encoding="utf-8"))
    live_by_id = {p["id"]: p for p in live["products"]}

    # Run the whole corpus once per flag state (reload engine between states).
    R_off = _reload_engine(False)
    off = {}
    for c in curated:
        pid = c["product_id"]; bc = pid.replace("shufersal_", "")
        ri = by_bc.get(bc)
        off[pid] = run_one(R_off, ri) if ri else {"error": "NOT IN RAW"}

    R_on = _reload_engine(True)
    on = {}
    for c in curated:
        pid = c["product_id"]; bc = pid.replace("shufersal_", "")
        ri = by_bc.get(bc)
        on[pid] = run_one(R_on, ri) if ri else {"error": "NOT IN RAW"}

    rows = []
    for c in curated:
        pid = c["product_id"]
        o, n = off[pid], on[pid]
        lp = live_by_id.get(pid, {})
        if o.get("error") or n.get("error"):
            rows.append({"pid": pid, "error": o.get("error") or n.get("error"),
                         "transparency_only": not c.get("display_score_boolean")})
            continue
        os_, ns_ = o["final_score"], n["final_score"]
        delta = round(ns_ - os_, 1) if (os_ is not None and ns_ is not None) else None
        og, ng = o["final_grade"], n["final_grade"]
        rows.append({
            "pid": pid,
            "display": bool(c.get("display_score_boolean")),
            "transparency_only": not c.get("display_score_boolean"),
            # published (calibrated) live score — for drift separation, NOT the recal baseline
            "live_score": lp.get("score"),
            "live_grade": lp.get("grade"),
            # recal baseline + recal result (same HEAD engine, only flag flips)
            "off_score": round(os_, 1) if os_ is not None else None,
            "off_grade": og,
            "on_score": round(ns_, 1) if ns_ is not None else None,
            "on_grade": ng,
            "delta_recal": delta,
            "grade_affecting": (og != ng) if (og and ng) else False,
            "cosmetic_lt2": (delta is not None and abs(delta) < 2.0 and og == ng),
            # head-drift separation (off vs published) — TASK-178 territory, reported not attributed
            "head_drift_vs_live": (round(os_ - lp.get("score"), 1)
                                   if (os_ is not None and isinstance(lp.get("score"), (int, float))) else None),
            "fat_quality_off": o["fat_quality_dim"],
            "fat_quality_on": n["fat_quality_dim"],
            "fat_quality_note_on": n["fat_quality_note"],
            "fat_g": o["fat_g"],
            "fat_saturated_g": o["fat_saturated_g"],
            "red_labels_on": n["red_labels"],
            "nova_off": o["nova_level"],
            "nova_on": n["nova_level"],
            "has_whole_grain": n["has_whole_grain"],
            "degradation": o["degradation"],
        })

    scored = [r for r in rows if not r.get("error") and r.get("off_score") is not None]
    grade_moves = [r for r in scored if r["grade_affecting"]]
    cosmetic = [r for r in scored if r.get("delta_recal") not in (None, 0) and not r["grade_affecting"]]
    nonzero = [r for r in scored if r.get("delta_recal") not in (None, 0)]

    payload = {
        "_LABEL": "TASK-169F BREAD RECAL HARNESS MODEL — NOT LIVE — DO NOT SHIP",
        "_meta": {
            "run_id": "real_bread_retail_003_v1",
            "flag": "BARI_RECAL_P0",
            "engine_src": str(SRC),
            "baseline": "OFF = current-HEAD flag-OFF (NOT the published build-time score)",
            "recal_vectors_in_scope": ["R3 leanness reward (fat_quality)", "R5 graded sat-fat penalty"],
            "drift_note": ("off_score vs live_score = pre-existing HEAD engine drift (TASK-178 "
                           "domain) — reported in head_drift_vs_live, never attributed to the recal. "
                           "delta_recal = on_score - off_score on the SAME engine = pure recal effect."),
            "corpus": "31 curated (24 displayed + 7 transparency-only)",
        },
        "summary": {
            "n_curated": len(rows),
            "n_scored": len(scored),
            "n_recal_nonzero": len(nonzero),
            "n_grade_affecting": len(grade_moves),
            "n_cosmetic_lt2": len(cosmetic),
            "grade_moves": [{"pid": r["pid"], "off": f"{r['off_score']}/{r['off_grade']}",
                             "on": f"{r['on_score']}/{r['on_grade']}", "delta": r["delta_recal"]}
                            for r in grade_moves],
        },
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE", OUT)
    print(f"\n{'pid':<26}{'live':>6}{'off':>7}{'on':>7}{'dRcl':>6}  {'fatQ off->on':>16}  ga")
    for r in rows:
        if r.get("error"):
            print(f"{r['pid']:<26}  {r['error']}"); continue
        fq = f"{r['fat_quality_off']}->{r['fat_quality_on']}"
        print(f"{r['pid']:<26}{str(r['live_score']):>6}{str(r['off_score']):>7}"
              f"{str(r['on_score']):>7}{str(r['delta_recal']):>6}  {fq:>16}  "
              f"{'GRADE' if r['grade_affecting'] else ''}")
    print(f"\nscored={len(scored)} recal_nonzero={len(nonzero)} "
          f"grade_affecting={len(grade_moves)} cosmetic_lt2={len(cosmetic)}")


if __name__ == "__main__":
    main()
