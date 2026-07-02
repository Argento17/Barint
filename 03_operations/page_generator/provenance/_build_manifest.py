# -*- coding: utf-8 -*-
"""TASK-406 provenance reconciliation. For every LIVE served comparison frontend, persist a
full provenance record (run_id + COMPLETE flag vector incl D4 + engine version + backing
source) by matching each served file to its shelf config. Read-only over the corpus; writes
ONE sidecar manifest (does not mutate the live frontend files). No re-scoring."""
import json, glob, os, subprocess, re

ROOT = r"C:\Bari"
CONFIGS = glob.glob(os.path.join(ROOT, r"03_operations\page_generator\configs", "*.json"))
COMP = os.path.join(ROOT, r"bari-web\src\data\comparisons")

# 15 live served files (from route imports)
LIVE = [
 "bread_frontend_v3.json","brined_cheeses_frontend_v2.json","cakes_hard_cookies_frontend_v1.json",
 "cereals_frontend_v2.json","cheese_frontend_v4.json","chocolate_bars_frontend_v1.json",
 "chocolate_tablets_frontend_v1.json","cookies_coffee_frontend_v2.json","granola_frontend_v2.json",
 "hard_cheeses_frontend_v2.json","hummus_frontend_v5.json","juices_frontend_v3.json",
 "milk_frontend_v1.json","protein_combined_frontend_v2.json","snacks_frontend_v5.json",
]

def norm(p): return os.path.normcase(os.path.abspath(p))
def lead_token(s):
    """Leading alpha token of a normalized stem/category (hyphens->underscores)."""
    s = str(s or "").lower().replace("-", "_")
    return s.split("_")[0] if s else ""

# index configs by their baseline_json (served file) AND by category leading-token (fallback).
# The baseline_json index alone false-flags served files whose config points its baseline at a
# DIFFERENT version (granola config->v1 but route serves v2; protein_bars config->v1 but route
# serves protein_combined_v2). That bug produced the "NO_CONFIG_BOUND" rows in the original
# "175 untraceable" screenshot. The category-token fallback resolves them.
cfg_by_served, cfg_by_token = {}, {}
for c in CONFIGS:
    if os.path.basename(c).startswith("_generated_"): continue
    try: d = json.load(open(c, encoding="utf-8"))
    except Exception: continue
    entry = {"config": os.path.relpath(c, ROOT), "data": d}
    bj = d.get("baseline_json")
    if bj:
        cfg_by_served[norm(bj)] = entry
    tok = lead_token(d.get("category")) or lead_token(os.path.basename(c)[:-5])
    if tok:
        cfg_by_token.setdefault(tok, []).append(entry)

def head():
    try: return subprocess.run(["git","rev-parse","--short","HEAD"],cwd=ROOT,capture_output=True,text=True).stdout.strip()
    except Exception: return None

ENGINE_HEAD = head()
D4_PATCH_COMMIT = "361748722"  # BARI_D4_SCORE_V1 applied to live (de-chain Finding 2)

manifest = {"_doc":"TASK-406 per-published-file provenance. Round-trip score verification = de-chain re-shadow.",
            "engine_head_at_record": ENGINE_HEAD, "d4_patch_commit": D4_PATCH_COMMIT, "records": {}}
gaps = []
for fn in LIVE:
    served = os.path.join(COMP, fn)
    rec = {"served_file": fn, "exists": os.path.exists(served)}
    if os.path.exists(served):
        d = json.load(open(served, encoding="utf-8"))
        meta = d.get("_meta", {}) if isinstance(d.get("_meta"), dict) else {}
        rec["meta_run_id"] = meta.get("run_id")
        rec["n_products"] = len(d.get("products", []) if isinstance(d.get("products"), list) else [])
    cfg = cfg_by_served.get(norm(served))
    rec["config_match"] = "baseline_json" if cfg else None
    if not cfg:  # fallback: unique config whose category leading-token matches the served stem
        tok = lead_token(fn.split("_frontend_")[0])
        cands = cfg_by_token.get(tok, [])
        if len(cands) == 1:
            cfg = cands[0]; rec["config_match"] = "category_token"
    if not cfg:
        rec["config"] = None; rec["status"] = "NO_CONFIG_BOUND"; gaps.append((fn,"no config baseline_json or category matches"))
    else:
        cd = cfg["data"]; sc = cd.get("scoring", {})
        bsip1 = sc.get("bsip1_dir"); rpd = cd.get("run_products_dir")
        corpus = cd.get("corpus_dirs") or []
        if isinstance(corpus, str): corpus = [corpus]
        if isinstance(rpd, list): rpd = rpd[0] if rpd else None
        if isinstance(bsip1, list): bsip1 = bsip1[0] if bsip1 else None
        flags = sc.get("flags", {})
        rec["config"] = cfg["config"]
        # corpus_dirs is the PRIMARY reproducibility basis (bsip1_dir is null-by-design on
        # multi-source shelves; keying on it false-flagged every such shelf as "bsip1_dir_missing").
        rec["corpus_dirs"] = corpus
        rec["corpus_exists"] = any(os.path.isdir(x) for x in corpus)
        rec["bsip1_dir"] = bsip1
        rec["bsip1_dir_exists"] = bool(bsip1 and os.path.isdir(bsip1))
        rec["run_products_dir"] = rpd
        rec["run_products_dir_exists"] = bool(rpd and os.path.isdir(rpd))
        # run_id: config-declared first, then served _meta, then run_products_dir basename
        rec["run_id_resolved"] = (cd.get("run_id") or sc.get("run_id") or rec.get("meta_run_id")
                                  or (os.path.basename(rpd.rstrip("\\/")) if rpd else None))
        rec["flag_vector"] = flags
        rec["d4_in_flags"] = ("BARI_D4_SCORE_V1" in flags)
        # HARD problems block reproducibility; SOFT are cosmetic (mirrors provenance_gate R-severity)
        hard, soft = [], []
        if not rec["corpus_exists"]: hard.append("corpus_dirs_missing")
        if not flags: hard.append("no_flag_vector_in_config")
        if not rec["run_id_resolved"]: hard.append("no_resolvable_run_id")
        if not rec.get("meta_run_id"): soft.append("NULL_meta_run_id")  # closed by generate_page self-stamp
        rec["problems_hard"], rec["problems_soft"] = hard, soft
        if hard: rec["status"] = "GAP_HARD:" + ",".join(hard)
        elif soft: rec["status"] = "GAP_SOFT:" + ",".join(soft)
        else: rec["status"] = "REPRODUCIBLE_PENDING_RESHADOW"
        if hard: gaps.append((fn, rec["status"]))
    manifest["records"][fn] = rec

out = os.path.join(ROOT, r"03_operations\page_generator\provenance\provenance_manifest.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
recs = manifest["records"].values()
print("live files:", len(LIVE),
      "| with config:", sum(1 for r in recs if r.get("config")),
      "| no_config:", sum(1 for r in recs if not r.get("config")),
      "| HARD gaps:", len(gaps),
      "| SOFT-only:", sum(1 for r in recs if r.get("status","").startswith("GAP_SOFT")),
      "| clean:", sum(1 for r in recs if r.get("status")=="REPRODUCIBLE_PENDING_RESHADOW"))
for fn, s in gaps: print("  HARD", fn, "->", s)
