# -*- coding: utf-8 -*-
"""DIAGNOSTIC ONLY (score-neutral). Round-trip reproduce check across live categories.
For each config: resolve corpus (corpus_dirs glob, with protein_bars ad-hoc special-case),
re-score at the config's own flags+shelf_rel, compare engine score to the PUBLISHED score in
the config's baseline_json (by barcode). Reports per-category reproduced(±0.1) / drift / not-scored.
Writes nothing to scores, configs, or frontend. Output JSON only."""
from __future__ import annotations
import importlib, json, os, statistics, sys
from pathlib import Path

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/Bari")
SRC = REPO / "03_operations/bsip2/proto_v0/src"
ANALYSIS = REPO / "03_operations/bsip2/proto_v0/analysis"
CONFIG_DIR = REPO / "03_operations/page_generator/configs"
sys.path.insert(0, str(SRC)); sys.path.insert(0, str(ANALYSIS))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOL = 0.1
ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1","BARI_SODIUM_SHELF_RELATIVE_V1","BARI_FAT_TECH_V1","BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM","BARI_GRAD_SODIUM_V1","BARI_DAIRY_PROTEIN_REWEIGHT_V1","BARI_REDLABEL_V1",
    "BARI_SODIUM_CEREAL","BARI_D4_SCORE_V1","BARI_HC002_NOVA1","BARI_GLASSBOX_W2","BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15","BARI_TASK144_FIXES","BARI_TASK250_CONF","BARI_DAIRY_SAT_FAT_INFER","BARI_W4_WFI_V1",
    "BARI_DECHAIN_V1","BARI_INGCONF_V1","BARI_HC_DAIRY_SATFAT_V1","BARI_GRAN_SUGAR_25G_V1","BARI_FAT_SENTINEL_V1",
    "BARI_ADDITIVE_PARSE_FIX_V1","BARI_PALM_HYDRO_V1","BARI_PROTEIN_BAR_V1","BARI_GLASSBOX_W4","BARI_FIBER_FERMENT_V1",
]
# live configs to check (stem -> config file); excludes _generated_* duplicates
CONFIGS = ["bread","brined_cheeses","cakes","cereals","cheese","chocolate_bars","chocolate_tablets",
           "cookies_coffee","granola","hard_cheeses","milk","snacks","juices","protein_bars",
           "hummus_shelfrel_002"]

def load(p): return json.loads(Path(p).read_bytes().decode("utf-8","replace"))

def remap(p):
    """Remap a hardcoded C:\\Bari absolute path to REPO (for worktree runs)."""
    if not p: return p
    s = str(p).replace("\\", "/")
    low = s.lower()
    for pref in ("c:/bari/",):
        if low.startswith(pref):
            return str(REPO / s[len(pref):])
    return s

def apply_flags(flags):
    for k in ALL_FLAGS: os.environ[k] = "off"
    os.environ["BARI_GLASSBOX_W4"] = "on"
    for k,v in flags.items(): os.environ[k] = str(v)

def reload_engine():
    import score_engine, nova_proxy, signal_extractor
    importlib.reload(nova_proxy); importlib.reload(signal_extractor); importlib.reload(score_engine)
    return score_engine

def apply_shelf_rel(sr, eng):
    if not sr: return
    if sr.get("api") == "sodium_ev056": eng.set_shelf_sodium_stats(sr["median"], sr["scale"])
    elif sr.get("nutrient"): eng.set_shelf_stats(sr["nutrient"], sr["median"], sr["scale"], sr.get("scale_type","iqr"))

def make_scorer(eng):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    def score_one(rec):
        try:
            sig = extract_signals(rec); cat = classify_category(rec)
            nov = infer_nova(rec, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(rec, cat["category"])
            sr = eng.score_product(rec, sig, cat, nov, ev)
            return sr if isinstance(sr, dict) else None
        except Exception:
            return None
    return score_one

STAMP = {}  # barcode -> bool (carries _task405_clean)

def resolve_records(cfg):
    """barcode -> bsip1 record. Standard: glob corpus_dirs. Ad-hoc protein: load _corpus_path."""
    by_bc = {}
    cp = remap(cfg.get("scoring", {}).get("_corpus_path"))
    dirs = cfg.get("corpus_dirs") or []
    if isinstance(dirs, str): dirs = [dirs]
    dirs = [remap(d) for d in dirs]
    globbed = False
    for d in dirs:
        dp = Path(d)
        if not dp.is_dir(): continue
        for f in sorted(dp.glob("bsip1_*.json")):
            if "audit" in f.name: continue
            try: rec = load(f)
            except Exception: continue
            if not isinstance(rec, dict) or rec.get("file_type") != "product": continue
            bc = str(rec.get("barcode","")).strip()
            if bc and bc not in by_bc:
                by_bc[bc] = rec; globbed = True
                STAMP[bc] = "_task405_clean" in rec
    if not by_bc and cp and Path(cp).is_file():   # ad-hoc fallback (protein_bars)
        data = load(cp)
        prods = data.get("products", data) if isinstance(data, dict) else data
        for rec in (prods or []):
            bc = str(rec.get("barcode","")).strip()
            if bc and bc not in by_bc: by_bc[bc] = rec
        return by_bc, "adhoc_corpus_json"
    return by_bc, ("glob" if globbed else "none")

def published_scores(cfg):
    bj = remap(cfg.get("baseline_json"))
    if not bj or not Path(bj).is_file(): return {}, None
    data = load(bj)
    out = {}
    for p in data.get("products", []):
        bc = str(p.get("barcode","")).strip()
        if bc: out[bc] = {"score": p.get("score"), "grade": p.get("grade")}
    return out, Path(bj).name

def main():
    report = {}
    for stem in CONFIGS:
        cfgp = CONFIG_DIR / f"{stem}.json"
        if not cfgp.is_file(): report[stem] = {"error": "config_missing"}; continue
        cfg = load(cfgp)
        flags = {k: str(v) for k,v in (cfg.get("scoring",{}).get("flags") or {}).items()}
        sr = cfg.get("scoring",{}).get("shelf_rel")
        recs, corpus_mode = resolve_records(cfg)
        pub, pub_file = published_scores(cfg)
        apply_flags(flags); eng = reload_engine(); apply_shelf_rel(sr, eng)
        score_one = make_scorer(eng)
        scored = {bc: score_one(rec) for bc, rec in recs.items()}
        repro = drift = notscored = nocorpus = grade_moves = 0
        drifts = []; gmoves = []
        for bc, pv in pub.items():
            ps = pv.get("score"); pg = pv.get("grade")
            if ps is None: continue
            res = scored.get(bc)
            if res is None:
                if bc not in recs: nocorpus += 1
                else: notscored += 1
                continue
            es = res.get("final_score_estimate"); eg = res.get("grade_estimate")
            if es is None: notscored += 1; continue
            if eg and pg and eg != pg:
                grade_moves += 1
                gmoves.append({"bc": bc, "pub_g": pg, "new_g": eg, "pub_s": ps, "new_s": round(es,2)})
            if abs(es - ps) <= TOL: repro += 1
            else:
                drift += 1
                drifts.append({"bc": bc, "pub": ps, "engine": round(es,2), "d": round(es-ps,2),
                               "cleaned": STAMP.get(bc, False)})
        n_pub = sum(1 for v in pub.values() if v.get("score") is not None)
        deltas = [abs(x["d"]) for x in drifts]
        report[stem] = {
            "published_file": pub_file, "corpus_mode": corpus_mode,
            "corpus_records": len(recs), "published_scored": n_pub,
            "reproduced_±0.1": repro, "drift": drift, "not_scored": notscored,
            "missing_from_corpus": nocorpus,
            "max_drift": round(max(deltas),2) if deltas else 0.0,
            "drifters_cleaned": sum(1 for d in drifts if d["cleaned"]),
            "drift_all_positive": all(d["d"] > 0 for d in drifts) if drifts else None,
            "grade_moves": grade_moves, "grade_move_detail": gmoves,
            "drift_detail": sorted(drifts, key=lambda x: -abs(x["d"]))[:8],
        }
        print(f"{stem:18s} pub={n_pub:3d} repro={repro:3d} drift={drift:2d} "
              f"GRADE_MOVES={grade_moves:2d} drifters_cleaned={report[stem]['drifters_cleaned']:2d} "
              f"nocorpus={nocorpus:2d} maxd={report[stem]['max_drift']:>4} [{corpus_mode}]")
    out = Path("C:/Bari/03_operations/page_generator/provenance/_reproduce_diag_result.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")

if __name__ == "__main__":
    main()
