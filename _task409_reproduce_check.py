# -*- coding: utf-8 -*-
"""TASK-409 reproduce check. For each staged JSON, re-score from the same corpus
and verify staged score == engine score (within TOL=0.1). This proves published==reproduce."""
import sys, json, glob, os, importlib, statistics

WT = r"C:\Bari\.claude\worktrees\task409"
SRC = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "src")
ANALYSIS = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "analysis")
sys.path.insert(0, SRC); sys.path.insert(0, ANALYSIS)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
STAGING = os.path.join(WT, "_task409_staging")

ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1","BARI_SODIUM_SHELF_RELATIVE_V1","BARI_FAT_TECH_V1","BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM","BARI_GRAD_SODIUM_V1","BARI_DAIRY_PROTEIN_REWEIGHT_V1","BARI_REDLABEL_V1",
    "BARI_SODIUM_CEREAL","BARI_D4_SCORE_V1","BARI_HC002_NOVA1","BARI_GLASSBOX_W2","BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15","BARI_TASK144_FIXES","BARI_TASK250_CONF","BARI_DAIRY_SAT_FAT_INFER","BARI_W4_WFI_V1",
    "BARI_DECHAIN_V1","BARI_INGCONF_V1","BARI_HC_DAIRY_SATFAT_V1","BARI_GRAN_SUGAR_25G_V1","BARI_FAT_SENTINEL_V1",
    "BARI_ADDITIVE_PARSE_FIX_V1","BARI_PALM_HYDRO_V1","BARI_PROTEIN_BAR_V1","BARI_GLASSBOX_W4","BARI_FIBER_FERMENT_V1",
]

def remap(p):
    """Remap C:\\Bari prefix to worktree, handling single-backslash paths."""
    if not p: return p
    s = str(p)
    # Normalize to forward slashes first
    s_fwd = s.replace("\\", "/")
    if s_fwd.lower().startswith("c:/bari/") and "worktrees" not in s_fwd.lower():
        return WT.replace("\\", "/") + "/" + s_fwd[len("c:/bari/"):]
    return s

def apply_flags(flags):
    for k in ALL_FLAGS: os.environ[k] = "off"
    os.environ["BARI_GLASSBOX_W4"] = "on"
    for k, v in flags.items(): os.environ[k] = str(v)

def reload_engine():
    import score_engine, nova_proxy, signal_extractor
    importlib.reload(nova_proxy); importlib.reload(signal_extractor); importlib.reload(score_engine)
    return score_engine

def apply_shelf_rel(sr, eng):
    if not sr: return
    if sr.get("api") == "sodium_ev056": eng.set_shelf_sodium_stats(sr["median"], sr["scale"])
    elif sr.get("nutrient"): eng.set_shelf_stats(sr["nutrient"], sr["median"], sr["scale"], sr.get("scale_type","iqr"))

def score_one(eng, rec):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    try:
        sig = extract_signals(rec)
        cat = classify_category(rec)
        nov = infer_nova(rec, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(rec, cat["category"])
        sr = eng.score_product(rec, sig, cat, nov, ev)
        return sr if isinstance(sr, dict) else None
    except Exception: return None

def load_bsip1_safe(corpus_dirs, bsip1_glob="bsip1_*.json", excl=None):
    records = {}
    if excl is None: excl = set()
    for d in corpus_dirs:
        d = remap(d)
        for f in sorted(glob.glob(os.path.join(d, bsip1_glob))):
            if "audit" in os.path.basename(f): continue
            try: rec = json.load(open(f, encoding="utf-8"))
            except Exception: continue
            if not isinstance(rec, dict) or rec.get("file_type") != "product": continue
            bc = str(rec.get("barcode", "")).strip()
            if bc and bc not in excl and bc not in records:
                records[bc] = rec
    return records

TOL = 0.1

# Category -> config name and any special corpus handling
SPECS = {
    "cheese":              ("cheese",              None),
    "milk":                ("milk",                None),
    "cereals":             ("cereals",             None),
    "bread":               ("bread",               None),
    "cakes":               ("cakes",               "bsip1_cakes_*.json"),
    "chocolate_bars":      ("chocolate_bars",      None),
    "chocolate_tablets":   ("chocolate_tablets",   None),
    "brined_cheeses":      ("brined_cheeses",      None),
    "hummus_shelfrel_002": ("hummus_shelfrel_002", None),
    "cookies_coffee":      ("cookies_coffee",      None),
    "granola":             ("granola",             None),
    "juices":              ("juices",              None),
}

report = {}
print(f"{'Category':<25} {'repro':>7} {'drift':>6} {'ns':>4} {'max_d':>6} PASS?")
print("-" * 62)

for cat_key, (cfg_name, bsip1_glob_override) in SPECS.items():
    staged_path = os.path.join(STAGING, f"{cat_key}_frontend_staged.json")
    if not os.path.exists(staged_path):
        print(f"{cat_key:<25} MISSING STAGED"); continue

    staged = json.load(open(staged_path, encoding="utf-8"))
    products = staged.get("products", [])

    cfg_path = os.path.join(WT, "03_operations", "page_generator", "configs", f"{cfg_name}.json")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    sc = cfg.get("scoring", {})
    flags = {k: str(v) for k, v in (sc.get("flags") or {}).items()}
    sr_cfg = sc.get("shelf_rel")
    corpus_dirs = cfg.get("corpus_dirs") or []
    excl = {str(e["barcode"]) for e in (cfg.get("exclusions") or [])}
    bsip1_glob = bsip1_glob_override or "bsip1_*.json"

    corpus = load_bsip1_safe(corpus_dirs, bsip1_glob, excl)

    # Chocolate subpool: restrict to barcodes in staged
    if cat_key in ("chocolate_bars", "chocolate_tablets"):
        staged_bcs = {str(p["barcode"]) for p in products}
        corpus = {bc: r for bc, r in corpus.items() if bc in staged_bcs}

    apply_flags(flags)
    eng = reload_engine()
    if sr_cfg: apply_shelf_rel(sr_cfg, eng)

    scored = {bc: score_one(eng, rec) for bc, rec in corpus.items()}

    repro = drift = notscored = 0
    drifts = []
    for p in products:
        bc = str(p.get("barcode", ""))
        ps = p.get("score")
        if ps is None: continue
        res = scored.get(bc)
        if res is None:
            notscored += 1; continue
        es = res.get("final_score_estimate")
        if es is None: notscored += 1; continue
        if abs(float(es) - float(ps)) <= TOL: repro += 1
        else:
            drift += 1
            drifts.append({"bc": bc, "staged": float(ps), "engine": round(float(es),2), "d": round(float(es)-float(ps),2)})

    n = len([p for p in products if p.get("score") is not None])
    max_d = round(max(abs(x["d"]) for x in drifts), 2) if drifts else 0.0
    passes = drift == 0 and notscored == 0 and repro == n
    report[cat_key] = {"reproduced": repro, "total": n, "drift": drift, "not_scored": notscored,
                       "max_drift": max_d, "pass": passes, "drifters": drifts[:5]}
    print(f"{cat_key:<25} {repro:>4}/{n:<3} {drift:>6} {notscored:>4} {max_d:>6.2f} {'PASS' if passes else 'FAIL'}")
    if drifts:
        for d in drifts[:3]: print(f"  drift: {d['bc']} staged={d['staged']} engine={d['engine']} d={d['d']}")

out = os.path.join(WT, "_task409_reproduce_v2_clean.json")
json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nwrote {out}")
pass_count = sum(1 for v in report.values() if v.get("pass"))
print(f"PASS: {pass_count}/{len(report)}")
