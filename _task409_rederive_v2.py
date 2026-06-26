# -*- coding: utf-8 -*-
"""TASK-409 re-derive v2 -- FIXED: excludes bsip1_audit_*.json files, reads file_type==product only.
Scores clean BSIP1 corpus, updates frontend JSONs to staging dir.
Fix: load_bsip1_dir now skips files with 'audit' in name AND checks file_type=='product'.
"""
import sys, json, glob, os, importlib, datetime, subprocess, collections

WT = r"C:\Bari\.claude\worktrees\task409"
SRC = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "src")
ANALYSIS = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "analysis")
sys.path.insert(0, SRC)
sys.path.insert(0, ANALYSIS)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STAGING = os.path.join(WT, "_task409_staging")
os.makedirs(STAGING, exist_ok=True)

NOW = datetime.datetime.now().isoformat(timespec="seconds")
TODAY = datetime.datetime.now().strftime("%Y%m%d")

ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1","BARI_SODIUM_SHELF_RELATIVE_V1","BARI_FAT_TECH_V1","BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM","BARI_GRAD_SODIUM_V1","BARI_DAIRY_PROTEIN_REWEIGHT_V1","BARI_REDLABEL_V1",
    "BARI_SODIUM_CEREAL","BARI_D4_SCORE_V1","BARI_HC002_NOVA1","BARI_GLASSBOX_W2","BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15","BARI_TASK144_FIXES","BARI_TASK250_CONF","BARI_DAIRY_SAT_FAT_INFER","BARI_W4_WFI_V1",
    "BARI_DECHAIN_V1","BARI_INGCONF_V1","BARI_HC_DAIRY_SATFAT_V1","BARI_GRAN_SUGAR_25G_V1","BARI_FAT_SENTINEL_V1",
    "BARI_ADDITIVE_PARSE_FIX_V1","BARI_PALM_HYDRO_V1","BARI_PROTEIN_BAR_V1","BARI_GLASSBOX_W4","BARI_FIBER_FERMENT_V1",
]

def apply_flags(flags):
    for k in ALL_FLAGS:
        os.environ[k] = "off"
    os.environ["BARI_GLASSBOX_W4"] = "on"
    for k, v in flags.items():
        os.environ[k] = str(v)

def reload_engine():
    import score_engine, nova_proxy, signal_extractor
    importlib.reload(nova_proxy)
    importlib.reload(signal_extractor)
    importlib.reload(score_engine)
    return score_engine

def apply_shelf_rel(sr, eng):
    if not sr:
        return
    if sr.get("api") == "sodium_ev056":
        eng.set_shelf_sodium_stats(sr["median"], sr["scale"])
    elif sr.get("nutrient"):
        eng.set_shelf_stats(sr["nutrient"], sr["median"], sr["scale"], sr.get("scale_type", "iqr"))

def score_one_product(eng, rec):
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
    except Exception:
        return None

def update_product(live_prod, engine_result, render_fields):
    """Update score/grade and render_fields only. Preserve all other fields."""
    updated = dict(live_prod)
    new_score = engine_result.get("final_score_estimate")
    new_grade = engine_result.get("grade_estimate")
    if new_score is not None:
        updated["score"] = round(new_score, 1)
    if new_grade is not None:
        updated["grade"] = new_grade
    rf = render_fields or []
    if "novaGroup" in rf:
        nova = engine_result.get("nova_proxy") or engine_result.get("nova_group")
        if nova is not None:
            updated["novaGroup"] = nova
    if "d4_additives" in rf:
        d4 = engine_result.get("d4_additives") or engine_result.get("detect_additives_d4")
        if d4 is not None:
            updated["d4_additives"] = d4
    if "confidence_level" in rf:
        conf = engine_result.get("data_sufficiency") or engine_result.get("confidence_level")
        if conf is not None:
            updated["confidence_level"] = conf
    return updated

def load_bsip1_dir(corpus_dirs, bsip1_glob="bsip1_*.json", exclusions=None):
    """Load bsip1 records from list of corpus dirs.
    CRITICAL: skip 'audit' files; only accept file_type=='product'.
    Dedup by barcode (first-wins to match reproduce_diag behavior).
    """
    records = {}
    if exclusions is None:
        exclusions = set()
    for d in corpus_dirs:
        # Remap C:\Bari prefix to worktree
        if "worktrees" not in str(d):
            d = str(d).replace("C:\\Bari", WT).replace("C:/Bari", WT)
        files = sorted(glob.glob(os.path.join(d, bsip1_glob)))
        for f in files:
            bn = os.path.basename(f)
            # FIXED: skip audit files (reproduce_diag does this too)
            if "audit" in bn:
                continue
            try:
                rec = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            # FIXED: only product records
            if not isinstance(rec, dict) or rec.get("file_type") != "product":
                continue
            bc = str(rec.get("barcode", bn.replace("bsip1_", "").replace(".json", ""))).strip()
            if not bc or bc in exclusions:
                continue
            # first-wins dedup (same as reproduce_diag)
            if bc not in records:
                records[bc] = rec
    return records

def get_engine_sha():
    try:
        r = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return "unknown"

def load_frontend(path):
    if "worktrees" not in str(path):
        path = str(path).replace("C:\\Bari", WT).replace("C:/Bari", WT)
    j = json.load(open(path, encoding="utf-8"))
    if isinstance(j, dict) and "products" in j:
        return j, list(j["products"])
    elif isinstance(j, list):
        return {"products": j}, list(j)
    return j, []

def save_staged(cat_key, frontend_data, products_list):
    out_path = os.path.join(STAGING, f"{cat_key}_frontend_staged.json")
    out = dict(frontend_data)
    out["products"] = products_list
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return out_path

engine_sha = get_engine_sha()
print(f"Engine SHA: {engine_sha}")

# ---------------------------------------------------------------------------
# Category definitions: flags read directly from configs (source of truth)
# ---------------------------------------------------------------------------
def load_cfg(name):
    p = os.path.join(WT, "03_operations", "page_generator", "configs", f"{name}.json")
    return json.load(open(p, encoding="utf-8"))

# Build CATEGORIES from configs
CATEGORY_SPECS = {
    # (rederive=True, cfg_name, corpus_dirs override or None, bsip1_glob override or None, exclusions override or None)
    "cheese":           (True,  "cheese",              None, None, None),
    "milk":             (True,  "milk",                None, None, None),
    "cereals":          (True,  "cereals",             None, None, None),
    "bread":            (True,  "bread",               None, None, None),
    "cakes":            (True,  "cakes",               None, "bsip1_cakes_*.json", None),
    "chocolate_bars":   (True,  "chocolate_bars",      None, None, None),
    "chocolate_tablets":(True,  "chocolate_tablets",   None, None, None),
    # confirm-no-move
    "brined_cheeses":       (False, "brined_cheeses",      None, None, None),
    "hummus_shelfrel_002":  (False, "hummus_shelfrel_002", None, None, None),
    "cookies_coffee":       (False, "cookies_coffee",      None, None, None),
    "granola":              (False, "granola",             None, None, None),
    "juices":               (False, "juices",              None, None, None),
}

# chocolate_bars and chocolate_tablets share the same corpus dir but need subpool filtering
# Build barcode sets from their respective live frontends
def get_choc_barcode_set(cat_key):
    live_files = {
        "chocolate_bars":    os.path.join(WT, "bari-web", "src", "data", "comparisons", "chocolate_bars_frontend_v1.json"),
        "chocolate_tablets": os.path.join(WT, "bari-web", "src", "data", "comparisons", "chocolate_tablets_frontend_v1.json"),
    }
    j = json.load(open(live_files[cat_key], encoding="utf-8"))
    return {str(p["barcode"]) for p in j.get("products", [])}

CHOC_BARS_BC = get_choc_barcode_set("chocolate_bars")
CHOC_TABS_BC = get_choc_barcode_set("chocolate_tablets")

results = {}
grade_moves_all = {}
discard_candidates = {}  # cat -> list of {bc, name, old_grade}

for cat_key, (rederive, cfg_name, corpus_dirs_override, bsip1_glob_override, excl_override) in CATEGORY_SPECS.items():
    label = "REDERIVE" if rederive else "CONFIRM-NO-MOVE"
    print(f"\n=== {cat_key}: {label} ===")

    cfg = load_cfg(cfg_name)
    sc = cfg.get("scoring", {})
    flags = {k: str(v) for k, v in (sc.get("flags") or {}).items()}
    sr_cfg = sc.get("shelf_rel")
    render_fields = cfg.get("render_fields", [])

    corpus_dirs = corpus_dirs_override or cfg.get("corpus_dirs") or []
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    bsip1_glob = bsip1_glob_override or "bsip1_*.json"

    # Build exclusion set from config
    exclusions = excl_override
    if exclusions is None:
        exclusions = {str(e["barcode"]) for e in (cfg.get("exclusions") or [])}

    # For chocolate: further filter by subpool barcode set
    choc_filter = None
    if cat_key == "chocolate_bars":
        choc_filter = CHOC_BARS_BC
    elif cat_key == "chocolate_tablets":
        choc_filter = CHOC_TABS_BC

    # Apply flags and reload engine
    apply_flags(flags)
    eng = reload_engine()
    if sr_cfg:
        apply_shelf_rel(sr_cfg, eng)

    # Load corpus (audit-file-safe)
    corpus = load_bsip1_dir(corpus_dirs, bsip1_glob, exclusions)

    # Additional filter for chocolate subpools
    if choc_filter is not None:
        corpus = {bc: rec for bc, rec in corpus.items() if bc in choc_filter}

    print(f"  corpus: {len(corpus)} records")

    if not corpus:
        results[cat_key] = {"status": "NO_CORPUS"}
        continue

    # Score all
    engine_results = {}
    failed = []
    for bc, rec in corpus.items():
        sr = score_one_product(eng, rec)
        if sr:
            engine_results[bc] = sr
        else:
            failed.append(bc)
    print(f"  scored: {len(engine_results)} | failed: {len(failed)}")

    # Load live frontend
    baseline_json = cfg.get("baseline_json")
    if not baseline_json:
        results[cat_key] = {"status": "NO_BASELINE_JSON"}
        continue
    frontend_path = str(baseline_json).replace("C:\\Bari", WT).replace("C:/Bari", WT)
    if not os.path.exists(frontend_path):
        results[cat_key] = {"status": "BASELINE_NOT_FOUND", "path": frontend_path}
        print(f"  MISSING baseline: {frontend_path}")
        continue

    frontend_data, products = load_frontend(frontend_path)

    # Update products
    updated_products = []
    grade_moves = []
    not_in_corpus = []
    scored_count = 0
    cat_discards = []

    for p in products:
        bc = str(p.get("barcode", ""))
        if bc in engine_results:
            er = engine_results[bc]
            old_score = p.get("score")
            old_grade = p.get("grade")
            updated = update_product(p, er, render_fields)
            new_score = updated.get("score")
            new_grade = updated.get("grade")
            updated_products.append(updated)
            scored_count += 1
            if old_grade != new_grade:
                gm = {
                    "bc": bc,
                    "name_he": p.get("name_he") or p.get("nameHe") or p.get("name") or "",
                    "old_score": old_score,
                    "new_score": new_score,
                    "old_grade": old_grade,
                    "new_grade": new_grade,
                }
                grade_moves.append(gm)
                if new_grade == "insufficient_data":
                    cat_discards.append(gm)
        else:
            updated_products.append(p)
            not_in_corpus.append(bc)

    print(f"  updated: {scored_count} | not_in_corpus: {len(not_in_corpus)} | grade_moves: {len(grade_moves)}")
    for gm in grade_moves:
        print(f"    GRADE MOVE: {gm['bc']} {gm['old_grade']}->{gm['new_grade']} {gm['old_score']}->{gm['new_score']}")

    if cat_discards:
        discard_candidates[cat_key] = cat_discards
        print(f"  DISCARD CANDIDATES (insufficient_data): {[x['bc'] for x in cat_discards]}")

    # Add meta
    if isinstance(frontend_data, dict):
        frontend_data["_meta"] = {
            "run_id": f"task409_rederive_{cat_key}_{TODAY}",
            "corpus_dirs": corpus_dirs,
            "flag_vector": flags,
            "engine_sha": engine_sha,
            "task": "TASK-409 clean+traceable re-derive v2",
            "ts": NOW,
            "corpus_records": len(corpus),
            "scored": len(engine_results),
            "failed_barcodes": failed[:20],
        }

    staged_path = save_staged(cat_key, frontend_data, updated_products)
    print(f"  staged: {staged_path}")

    grade_moves_all[cat_key] = grade_moves
    results[cat_key] = {
        "status": label,
        "corpus_records": len(corpus),
        "scored": len(engine_results),
        "failed": failed[:20],
        "not_in_corpus": not_in_corpus[:20],
        "grade_moves": grade_moves,
        "grade_moves_count": len(grade_moves),
    }

# Grade distribution per category from staged files
print("\n=== Grade distributions (staged) ===")
grade_dists = {}
for cat_key in CATEGORY_SPECS:
    staged_path = os.path.join(STAGING, f"{cat_key}_frontend_staged.json")
    if not os.path.exists(staged_path):
        continue
    j = json.load(open(staged_path, encoding="utf-8"))
    prods = j.get("products", [])
    dist = collections.Counter(p.get("grade") for p in prods)
    scores = [p.get("score") for p in prods if isinstance(p.get("score"), (int, float))]
    import statistics
    grade_dists[cat_key] = {
        "dist": dict(sorted(dist.items())),
        "count": len(prods),
        "scored_count": len(scores),
        "score_min": round(min(scores), 1) if scores else None,
        "score_max": round(max(scores), 1) if scores else None,
        "score_mean": round(statistics.mean(scores), 1) if scores else None,
        "score_median": round(statistics.median(scores), 1) if scores else None,
        "score_stdev": round(statistics.stdev(scores), 2) if len(scores) > 1 else None,
    }
    print(f"  {cat_key}: {dict(sorted(dist.items()))} n={len(prods)} min={grade_dists[cat_key]['score_min']} max={grade_dists[cat_key]['score_max']}")

# Write summary
summary = {
    "run_ts": NOW,
    "engine_sha": engine_sha,
    "results": results,
    "grade_moves_all": grade_moves_all,
    "discard_candidates": discard_candidates,
    "grade_distributions": grade_dists,
}
outf = os.path.join(WT, "_task409_rederive_v2_result.json")
json.dump(summary, open(outf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n=== DONE. Results: {outf} ===")
