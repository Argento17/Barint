# -*- coding: utf-8 -*-
"""TASK-429 canonical reproduction (score-neutral, read-only).
Re-score the 31 published hard_cheeses_frontend_v4 barcodes from a FRESH engine
invocation using the pinned canonical (flags + shelf-stats + corpus) and diff
against published. Writes nothing to scores/configs/frontend. JSON + stdout only.
"""
from __future__ import annotations
import importlib, json, os, sys
from pathlib import Path

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/bari_t429")
SRC = REPO / "03_operations/bsip2/proto_v0/src"
ANALYSIS = REPO / "03_operations/bsip2/proto_v0/analysis"
sys.path.insert(0, str(SRC)); sys.path.insert(0, str(ANALYSIS))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOL = 0.1

# ---- CANONICAL INVOCATION (pinned) --------------------------------------
CANONICAL_FLAGS = {
    "BARI_SHELF_RELATIVE_V1": "on",
    "BARI_FAT_TECH_V1": "on",
    "BARI_RECAL_P0": "on",
    "BARI_HC002_NOVA1": "off",
    "BARI_DAIRY_SAT_FAT_INFER": "on",
    "BARI_REDLABEL_V1": "on",
    "BARI_HC_DAIRY_SATFAT_V1": "on",
}
CANONICAL_SHELF_REL = {"nutrient": "fat_saturated_g", "median": 18.0, "scale": 1.4, "scale_type": "iqr"}
CORPUS_DIR = REPO / "02_products/hard_cheeses/bsip1_task412"
BASELINE_JSON = REPO / "bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json"

# Superset of flags the engine may read (from _reproduce_diag.py); default OFF.
ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1","BARI_SODIUM_SHELF_RELATIVE_V1","BARI_FAT_TECH_V1","BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM","BARI_GRAD_SODIUM_V1","BARI_DAIRY_PROTEIN_REWEIGHT_V1","BARI_REDLABEL_V1",
    "BARI_SODIUM_CEREAL","BARI_D4_SCORE_V1","BARI_HC002_NOVA1","BARI_GLASSBOX_W2","BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15","BARI_TASK144_FIXES","BARI_TASK250_CONF","BARI_DAIRY_SAT_FAT_INFER","BARI_W4_WFI_V1",
    "BARI_DECHAIN_V1","BARI_INGCONF_V1","BARI_HC_DAIRY_SATFAT_V1","BARI_GRAN_SUGAR_25G_V1","BARI_FAT_SENTINEL_V1",
    "BARI_ADDITIVE_PARSE_FIX_V1","BARI_PALM_HYDRO_V1","BARI_PROTEIN_BAR_V1","BARI_GLASSBOX_W4","BARI_FIBER_FERMENT_V1",
]

def load(p): return json.loads(Path(p).read_bytes().decode("utf-8","replace"))

def apply_flags(flags):
    for k in ALL_FLAGS: os.environ[k] = "off"
    os.environ["BARI_GLASSBOX_W4"] = "on"   # matches _reproduce_diag baseline
    for k, v in flags.items(): os.environ[k] = str(v)

def reload_engine():
    import score_engine, nova_proxy, signal_extractor
    importlib.reload(nova_proxy); importlib.reload(signal_extractor); importlib.reload(score_engine)
    return score_engine

def apply_shelf_rel(sr, eng):
    if sr.get("nutrient"):
        eng.set_shelf_stats(sr["nutrient"], sr["median"], sr["scale"], sr.get("scale_type","iqr"))

def make_scorer(eng):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    def score_one(rec):
        sig = extract_signals(rec); cat = classify_category(rec)
        nov = infer_nova(rec, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(rec, cat["category"])
        sr = eng.score_product(rec, sig, cat, nov, ev)
        return sr if isinstance(sr, dict) else None
    return score_one

def index_corpus(cd):
    idx = {}
    for f in sorted(Path(cd).glob("bsip1_hardcheese_*.json")):
        if "audit" in f.name: continue
        try: r = load(f)
        except Exception: continue
        if not isinstance(r, dict): continue
        bc = str(r.get("barcode","")).strip()
        if bc and bc not in idx: idx[bc] = r
    return idx

def main():
    pub = {str(p.get("barcode")).strip(): {"score": p.get("score"), "grade": p.get("grade"),
           "name": p.get("nameHe", p.get("name",""))} for p in load(BASELINE_JSON)["products"]}
    corpus = index_corpus(CORPUS_DIR)
    apply_flags(CANONICAL_FLAGS); eng = reload_engine(); apply_shelf_rel(CANONICAL_SHELF_REL, eng)
    score_one = make_scorer(eng)

    rows = []; repro = drift = grade_moves = nocorpus = err = 0
    for bc, pv in pub.items():
        ps, pg = pv["score"], pv["grade"]
        rec = corpus.get(bc)
        if rec is None:
            nocorpus += 1; rows.append({"bc": bc, "status": "NO_CORPUS", "pub": ps, "pub_g": pg}); continue
        try:
            res = score_one(rec)
        except Exception as e:
            err += 1; rows.append({"bc": bc, "status": "ERROR", "err": str(e)[:120]}); continue
        if not res or res.get("final_score_estimate") is None:
            err += 1; rows.append({"bc": bc, "status": "NO_SCORE", "pub": ps}); continue
        es = res["final_score_estimate"]; eg = res.get("grade_estimate")
        d = round(es - (ps or 0), 3)
        gm = bool(eg and pg and eg != pg)
        if gm: grade_moves += 1
        if abs(d) <= TOL: repro += 1; st = "REPRO"
        else: drift += 1; st = "DRIFT"
        rows.append({"bc": bc, "status": st, "pub": ps, "engine": round(es,2), "drift": d,
                     "pub_g": pg, "engine_g": eg, "grade_move": gm, "name": pv["name"]})

    summary = {
        "canonical": {"flags": CANONICAL_FLAGS, "shelf_rel": CANONICAL_SHELF_REL,
                      "corpus_dir": str(CORPUS_DIR), "baseline": str(BASELINE_JSON),
                      "glassbox_w4_forced_on": True, "rt4_fix_constant_expected": 67.0},
        "published_count": len(pub), "reproduced_pm0.1": repro, "drift": drift,
        "grade_moves": grade_moves, "missing_from_corpus": nocorpus, "errors": err,
        "PASS": (repro == len(pub) and drift == 0 and grade_moves == 0 and nocorpus == 0 and err == 0),
    }
    out = {"summary": summary, "rows": sorted(rows, key=lambda r: -abs(r.get("drift",0)))}
    Path(REPO / "_t429_reproduce_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("="*70)
    print(f"CANONICAL REPRODUCTION — hard_cheeses_frontend_v4  (n={len(pub)})")
    print("="*70)
    for r in sorted(rows, key=lambda r: -abs(r.get('drift',0))):
        if r["status"] in ("REPRO",):
            continue
        print(r)
    print(f"\nREPRODUCED(±0.1): {repro}/{len(pub)}   DRIFT: {drift}   "
          f"GRADE_MOVES: {grade_moves}   MISSING: {nocorpus}   ERRORS: {err}")
    print(f"PASS = {summary['PASS']}")
    print(f"wrote {REPO/'_t429_reproduce_result.json'}")

if __name__ == "__main__":
    main()
