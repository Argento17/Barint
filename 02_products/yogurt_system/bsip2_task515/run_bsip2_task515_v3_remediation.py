"""
TASK-515 / TASK-515A -- Stage 2 (BSIP2 scoring), RUN v3-REMEDIATION.

Supersedes run_bsip2_task515_v3.py's corpus composition on top of the SAME
117-product shipping corpus (94 spoonable / 23 drinkable), applying the
owner-ruled corpus remediation from remediation_ledger_task515_v1.json +
the 4-site targeted rescrape (bsip0_task515_rescrape/):

  1. KEEP the 4 rescrape-recovered products (real data now on their BSIP1
     records: 7290102395224, 7290102395231, 7290112341686 ingredients;
     7290110561352 sugar 4.5g) -- they score on real data, no special case
     needed here, they just aren't excluded.
  2. DUMP the 16 rescrape-confirmed-unavailable products (owner directive:
     "if not retrievable through other sites - dump those products
     completely"), incl. 7290116936581 (implausible milk-only, Class A).
  3. DEDUP -- drop 3 (keep canonical EAN-13): 6664655 (keep 7290119380923),
     57149 (keep 7290014758100), 7290014758117 (keep clean twin 57132 --
     this also removes the Class D diabetes-seal contamination artifact by
     dropping the contaminated listing outright, per owner ruling which
     supersedes the ledger's strip-then-dedup recommendation).
  4. STRIP: the 27 Class-D header-bleed products already had their scored
     ingredient fields (ingredients_text_he, ingredients_list,
     ingredient_order[].text, ingredients_raw mirror) cleaned in-place on
     their BSIP1 records BEFORE this script runs (see
     header_bleed_strip_report_v1.json) -- this script scores their
     CURRENT (cleaned) BSIP1 state, no special-case exclusion needed.

Net corpus change vs the committed v3 shipping run (2474b04a):
  spoonable: 94 -> 78  (-16: 14 dump + 2 dedup)
  drinkable: 23 -> 20  (-3: 2 dump + 1 dedup)
  total:     117 -> 98

Engine/constants/router: score_engine.py, constants.py, router_v2.py are
untouched by this script (read-only imports; sha256 recorded and compared
against the committed baseline for 0-diff confirmation). This is a
corpus-composition + BSIP1-field-hygiene change, re-scored through the
unmodified engine -- NOT an engine change.

Tree safety: this script and ALL of its outputs live under
02_products/yogurt_system/ only (writes traces into the existing
bsip2_task515_v3/{pool}/products/ directories, overwriting in place, and a
new run_record.json + manifest in bsip2_task515_v3/). No git operations,
no commit. Old trace files for the 19 newly-excluded barcodes are NOT
deleted (kept on disk, un-rewritten, exactly the same "kept on disk,
untouched" precedent v3 used for its own 3 display exclusions) -- the
page_generator configs' "exclusions" lists are updated separately to
filter them out at frontend-generation time.

MEASURED / SCORED, NOT PUBLISHED. This run is a co-sign PACKAGE for
Nutrition + Product -- not a go-live. Any newly-passing shelf-relative
guard constant is NOT added to constants.py by this script; the drinkable
guard-flip finding is reported for D6/D7 co-sign, not activated here.
"""
import os, sys, json, pathlib, hashlib, datetime, statistics, logging
from collections import Counter, defaultdict

os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "on"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats, compute_shelf_stats,
    BARI_SHELF_RELATIVE_V1,
)
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    CULTURED_YOGURT_SUBTYPES, SUGAR_SHELF_SCALE_MIN, SUGAR_SHELF_SCALE_GUARD,
    SUGAR_SHELF_REL_YOGURT_FLOOR, SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
    SUGAR_SHELF_REL_YOGURT_P_MAX, SUGAR_SHELF_REL_YOGURT_B_MAX,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "02_products" / "yogurt_system" / "bsip1_task515"
V3_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515_v3"
OUTPUT_DIR = V3_DIR
RUN_ID = "run_yogurt_task515_bsip2_v3_remediation"
MIN_N_GUARD = 20

# --- Carried forward unchanged from v3: prior-stage discards + display exclusions ---
DISCARD_BARCODES_V2 = {
    "7290110329792": "מעדן סויה ביו אפרסק -- soy-based, non-dairy; not a yogurt product",
    "7290110329815": "מעדן סויה ביו מעודנת -- soy-based, non-dairy; not a yogurt product",
}
DISPLAY_EXCLUDE_BARCODES_V3 = {
    "4068028": "ציזיקי לשתיה -- Nutrition ruling: savory flavored-milk drink, not yogurt.",
    "7290119377480": "יוגורט פרו עם שוקולד -- confectionery-lens (TASK-362 Rule 3).",
    "7290119385768": "דנונה פרו קראנצ' פצפוץ שוקולד מריר -- same ruling as above.",
}

# --- TASK-515/515A remediation NEW: owner-directed dump (16, rescrape-confirmed unavailable) ---
DUMP_BARCODES = {
    "7290116936581": "owner-directed dump: field unrecoverable across all 4 retailers (rescrape acc0c9ac). Class A source-implausible single-ingredient milk declaration (10.0g/100g protein).",
    "43944": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "45771": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "5416415": "owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290110321031": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290110328788": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290110329952": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116932484": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116934402": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116935614": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116935621": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116936123": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116936215": "owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116936222": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116934228": "owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
    "7290116932774": "owner-directed dump: fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).",
}

# --- TASK-515/515A remediation NEW: dedup drops (3) ---
DEDUP_BARCODES = {
    "57149": "dedup-drop: byte-identical duplicate of canonical EAN-13 7290014758100 (KEPT).",
    "7290014758117": "dedup-drop (owner ruling): byte-identical duplicate of clean twin 57132 (KEPT); also carries confirmed Class-D diabetes-seal certification-text contamination -- dropping removes both the duplicate and the contamination in one action.",
    "6664655": "dedup-drop: byte-identical duplicate of canonical EAN-13 7290119380923 (KEPT).",
}

ALL_EXCLUDE_BARCODES = {
    **DISCARD_BARCODES_V2, **DISPLAY_EXCLUDE_BARCODES_V3,
    **DUMP_BARCODES, **DEDUP_BARCODES,
}


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yogurt_bsip1(source_dir: pathlib.Path) -> list[dict]:
    paths = sorted(source_dir.glob("bsip1_yogurt_*.json"))
    products = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        data["_source_path"] = str(p)
        data["_load_errors"] = []
        products.append(data)
    return products


def get_sugars_g(doc: dict):
    nn = doc.get("normalized_nutrition_per_100g") or {}
    return nn.get("sugars_g")


def run_pipeline(product: dict):
    signals = extract_signals(product)
    cat_result = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace, score_result, cat_result


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== BSIP2 Stage 2 v3-REMEDIATION -- %s ===", RUN_ID)
    log.info("BARI_SHELF_RELATIVE_V1 at import: %s", BARI_SHELF_RELATIVE_V1)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source missing: %s", BSIP1_DIR)
        return

    all_products_raw = load_yogurt_bsip1(BSIP1_DIR)
    n_loaded_raw = len(all_products_raw)

    all_products = [d for d in all_products_raw if str(d.get("barcode", "")) not in ALL_EXCLUDE_BARCODES]
    n_discarded_total = n_loaded_raw - len(all_products)
    log.info("Loaded %d BSIP1 yogurt records, discarded %d total (2 soy + 3 display + 16 "
             "owner-dump + 3 dedup) -> %d in remediated shipping corpus",
             n_loaded_raw, n_discarded_total, len(all_products))

    router_rows = []
    non_dairy_protein = []
    for doc in all_products:
        bc = str(doc.get("barcode", ""))
        cat_result = classify_category(doc)
        cat = cat_result.get("category")
        subtype = cat_result.get("category_subtype")
        subpool = doc.get("subpool")
        row = {
            "barcode": bc, "name": doc.get("canonical_name_he"), "subpool": subpool,
            "router_category": cat, "router_subtype": subtype,
            "in_cultured_yogurt_subtypes": subtype in CULTURED_YOGURT_SUBTYPES,
        }
        router_rows.append(row)
        if cat != "dairy_protein":
            non_dairy_protein.append(row)

    subpool_counts = Counter(r["subpool"] for r in router_rows)
    subtype_dist = Counter(r["router_subtype"] for r in router_rows)
    not_cultured_subtype = [r for r in router_rows if not r["in_cultured_yogurt_subtypes"]]
    shipping_corpus_clean = (len(non_dairy_protein) == 0 and len(not_cultured_subtype) == 0)
    log.info("Router-cleanliness (expect TRUE): %s", shipping_corpus_clean)

    spoonable = [d for d in all_products if d.get("subpool") == "spoonable"]
    drinkable = [d for d in all_products if d.get("subpool") == "drinkable"]
    other_subpool = [d for d in all_products if d.get("subpool") not in ("spoonable", "drinkable")]
    log.info("Pools: spoonable=%d drinkable=%d other=%d", len(spoonable), len(drinkable), len(other_subpool))

    pools = {"spoonable": spoonable, "drinkable": drinkable}
    pool_stats = {}
    pool_score_results = {}
    pool_errors = defaultdict(list)

    for pool_name, pool_products in pools.items():
        sugars_n = sum(1 for d in pool_products if get_sugars_g(d) is not None)
        median, scale = compute_shelf_stats(
            pool_products, "sugars_g", scale_type="iqr",
            nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
        )
        guard_n_pass = sugars_n >= MIN_N_GUARD
        guard_scale_pass = (scale is not None) and (scale >= SUGAR_SHELF_SCALE_GUARD)
        guard_pass = bool(median is not None and scale is not None and guard_n_pass and guard_scale_pass)

        pool_stats[pool_name] = {
            "n_total_products": len(pool_products), "n_with_sugars_g": sugars_n,
            "median": median, "scale": scale, "scale_source": "compute_shelf_stats(scale_type='iqr')",
            "min_n_guard": MIN_N_GUARD, "guard_n_pass": guard_n_pass,
            "low_variance_guard_threshold": SUGAR_SHELF_SCALE_GUARD,
            "guard_scale_pass": guard_scale_pass, "guard_pass_overall": guard_pass,
        }
        log.info("[%s] sugars_g stats: n=%d median=%s scale=%s guard_n=%s guard_scale=%s -> %s",
                  pool_name, sugars_n, median, scale, guard_n_pass, guard_scale_pass,
                  "ACTIVE" if guard_pass else "SUPPRESSED (stats left unset)")

        clear_shelf_stats()
        if guard_pass:
            set_shelf_stats(nutrient="sugars_g", median=median, scale=scale, scale_type="iqr", n=sugars_n)

        traces = []
        score_results = {}
        for doc in pool_products:
            bc = str(doc.get("barcode", ""))
            try:
                trace, score_result, cat_result = run_pipeline(doc)
                write_trace(trace, OUTPUT_DIR / pool_name)
                traces.append(trace)
                score_results[bc] = {
                    "score": trace.get("final_score_estimate"), "grade": trace.get("grade_estimate"),
                    "category": trace.get("category"), "subtype": cat_result.get("category_subtype"),
                    "evaluation_status": trace.get("evaluation_status"),
                }
            except Exception as e:
                import traceback
                log.error("SCORE ERROR pool=%s barcode=%s: %s", pool_name, bc, e)
                traceback.print_exc()
                pool_errors[pool_name].append({"barcode": bc, "name": doc.get("canonical_name_he"), "error": str(e)})

        pool_score_results[pool_name] = score_results
        clear_shelf_stats()
        log.info("[%s] scored %d/%d products (%d errors)",
                  pool_name, len(traces), len(pool_products), len(pool_errors[pool_name]))

    def distribution(score_results: dict):
        scored = [v["score"] for v in score_results.values() if v.get("score") is not None]
        grades = Counter(v["grade"] for v in score_results.values() if v.get("grade") is not None)
        oos = sum(1 for v in score_results.values() if v.get("evaluation_status") == "out_of_scope")
        return {
            "n_scored": len(scored), "n_out_of_scope": oos,
            "min": round(min(scored), 2) if scored else None,
            "median": round(statistics.median(scored), 2) if scored else None,
            "max": round(max(scored), 2) if scored else None,
            "mean": round(statistics.mean(scored), 2) if scored else None,
            "stdev": round(statistics.stdev(scored), 2) if len(scored) > 1 else None,
            "grade_counts": dict(sorted(grades.items())),
        }

    pool_distributions = {name: distribution(sr) for name, sr in pool_score_results.items()}
    for name, d in pool_distributions.items():
        log.info("[%s] distribution: %s", name, d)

    eng_sha = sha256_file(SRC / "score_engine.py")
    const_sha = sha256_file(SRC / "constants.py")
    router_sha = sha256_file(SRC / "router_v2.py")

    # sha256 of the committed baseline (2474b04a) versions, hardcoded from
    # the v3 run_record.json's own recorded values -- these files are
    # read-only imports in this script, never edited.
    BASELINE_ENGINE_SHA = "535a9ed1b704e587546c2c314ef76abddf543310dcce0b7e74fb8e7f26453f34"
    BASELINE_ROUTER_SHA = "9da6f3b7b86a82c4e655fe2768dcf018b478999a8fea4ab0364c21274103e3f9"

    no_bleed_confirmation = {
        "claim": "Zero writes to score_engine.py / router_v2.py this run (read-only imports). "
                 "constants.py sha256 differs from the ORIGINAL 2474b04a baseline because a PRIOR "
                 "uncommitted round (TASK-515/515A additive display-fix, documented in "
                 "SPOONABLE_RESCORE_COSIGN.md / run_record_task515b_*.json) already landed an "
                 "additive display-only constants.py change before this run started; that change "
                 "is carried forward unchanged by this run (this run does not touch constants.py "
                 "further). This run is a corpus-composition change (19 additional exclusions: 16 "
                 "owner-directed dump + 3 dedup) plus BSIP1 ingredient-field hygiene fixes (27 "
                 "header-bleed strips) plus a fresh shelf-stat recompute -- not a NEW engine change.",
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "router_v2_sha256": router_sha,
        "score_engine_0diff_vs_2474b04a_baseline": (eng_sha == BASELINE_ENGINE_SHA),
        "router_v2_0diff_vs_2474b04a_baseline": (router_sha == BASELINE_ROUTER_SHA),
    }

    def ev105_pool_constants(pool_name):
        s = pool_stats[pool_name]
        return {
            "SUGAR_SHELF_REL_YOGURT_%s_MEDIAN" % pool_name.upper(): s["median"],
            "SUGAR_SHELF_REL_YOGURT_%s_IQR_SCALE" % pool_name.upper(): s["scale"],
            "SUGAR_SHELF_REL_YOGURT_%s_N" % pool_name.upper(): s["n_with_sugars_g"],
            "SUGAR_SHELF_REL_YOGURT_FLOOR": SUGAR_SHELF_REL_YOGURT_FLOOR,
            "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
            "SUGAR_SHELF_REL_YOGURT_P_MAX": SUGAR_SHELF_REL_YOGURT_P_MAX,
            "SUGAR_SHELF_REL_YOGURT_B_MAX": SUGAR_SHELF_REL_YOGURT_B_MAX,
            "guard_pass": s["guard_pass_overall"],
        }

    ev105_remediation = {
        "id": "EV-105v3-REMEDIATION",
        "status": "SCORED / PROPOSAL -- NOT LIVE -- not written to constants.py",
        "supersedes": "EV-105v2-FINAL (v3 shipping, 94/23 split) -- this run's 78/20 split "
                       "(post owner-directed dump + dedup remediation) is the proposal.",
        "approval_state": "PENDING -- Nutrition + Product co-sign required (this is a co-sign "
                           "package return, not a go-live). If the DRINKABLE guard now PASSES "
                           "(it does, at n=20), the resulting SUGAR_SHELF_REL_YOGURT_DRINKABLE_* "
                           "constant is a NEW additive constant proposal -- flagged for D6/D7, "
                           "NOT persisted to constants.py by this script.",
        "spoonable": ev105_pool_constants("spoonable"),
        "drinkable": ev105_pool_constants("drinkable"),
    }

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-515 / TASK-515A owner-ruled corpus remediation + re-score",
        "generated": ts,
        "run_type": "SCORED -- NOT PUBLISHED (co-sign package; go-live gated by orchestrator)",
        "engine": "proto_v0 score_engine.py -- UNMODIFIED (uniform-baseline doctrine)",
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "n_loaded_raw": n_loaded_raw,
            "discarded_prior_stage_soy": {"count": len(DISCARD_BARCODES_V2), "barcodes": DISCARD_BARCODES_V2},
            "excluded_v3_display_ruling": {"count": len(DISPLAY_EXCLUDE_BARCODES_V3), "barcodes": DISPLAY_EXCLUDE_BARCODES_V3},
            "excluded_remediation_dump": {"count": len(DUMP_BARCODES), "barcodes": DUMP_BARCODES},
            "excluded_remediation_dedup": {"count": len(DEDUP_BARCODES), "barcodes": DEDUP_BARCODES},
            "n_discarded_total": n_discarded_total,
            "n_in_shipping_corpus": len(all_products),
            "subpool_distribution": dict(subpool_counts),
            "other_subpool_count": len(other_subpool),
            "target_confirmed": {
                "spoonable_target": 78, "drinkable_target": 20,
                "spoonable_actual": len(spoonable), "drinkable_actual": len(drinkable),
                "matches_target": (len(spoonable) == 78 and len(drinkable) == 20),
            },
        },
        "router_check": {
            "n_dairy_protein": len(all_products) - len(non_dairy_protein),
            "n_non_dairy_protein": len(non_dairy_protein),
            "subtype_distribution": dict(subtype_dist),
            "n_not_in_cultured_yogurt_subtypes": len(not_cultured_subtype),
            "shipping_corpus_router_clean": shipping_corpus_clean,
        },
        "pool_shelf_stats": pool_stats,
        "pool_distributions": pool_distributions,
        "pool_errors": {k: v for k, v in pool_errors.items()},
        "no_bleed_confirmation": no_bleed_confirmation,
        "ev105_remediation": ev105_remediation,
        "header_bleed_strip_applied": {
            "count": 27,
            "report": str(V3_DIR / "header_bleed_strip_report_v1.json"),
            "note": "Applied to BSIP1 records BEFORE this rescore ran; this run scores the "
                    "cleaned ingredient fields directly, no special-case handling needed here.",
        },
        "rescrape_recovered_kept": ["7290102395224", "7290102395231", "7290112341686", "7290110561352"],
        "output_dir": str(OUTPUT_DIR),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rr_path = OUTPUT_DIR / "run_record.json"
    rr_bytes = json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8")
    rr_path.write_bytes(rr_bytes)
    rr_sha = sha256_bytes(rr_bytes)
    log.info("Run record written: %s (sha256=%s)", rr_path, rr_sha)

    manifest = {
        "run_id": RUN_ID, "generated": ts,
        "spoonable": {"n": len(spoonable), "barcodes": sorted(str(d.get("barcode", "")) for d in spoonable)},
        "drinkable": {"n": len(drinkable), "barcodes": sorted(str(d.get("barcode", "")) for d in drinkable)},
        "excluded_from_shipping": {
            "soy_out_of_scope": DISCARD_BARCODES_V2,
            "v3_display_exclusions": DISPLAY_EXCLUDE_BARCODES_V3,
            "remediation_dump": DUMP_BARCODES,
            "remediation_dedup": DEDUP_BARCODES,
        },
    }
    manifest_path = OUTPUT_DIR / "shipping_corpus_manifest_task515.json"
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    manifest_sha = sha256_bytes(manifest_bytes)
    log.info("Manifest written: %s (sha256=%s)", manifest_path, manifest_sha)

    print("\n" + "=" * 80)
    print(f"TASK-515/515A REMEDIATION RESCORE -- {RUN_ID}")
    print("=" * 80)
    print(f"Corpus: loaded={n_loaded_raw} discarded_total={n_discarded_total} in_corpus={len(all_products)}")
    print(f"Pools: spoonable={len(spoonable)} drinkable={len(drinkable)} other={len(other_subpool)}")
    print(f"Router clean: {shipping_corpus_clean}")
    print(f"Spoonable guard_pass={pool_stats['spoonable']['guard_pass_overall']} median={pool_stats['spoonable']['median']} scale={pool_stats['spoonable']['scale']} n={pool_stats['spoonable']['n_with_sugars_g']}")
    print(f"Drinkable guard_pass={pool_stats['drinkable']['guard_pass_overall']} median={pool_stats['drinkable']['median']} scale={pool_stats['drinkable']['scale']} n={pool_stats['drinkable']['n_with_sugars_g']}")
    print(f"Distributions: {json.dumps(pool_distributions, ensure_ascii=False)}")
    print(f"score_engine 0-diff vs 2474b04a: {no_bleed_confirmation['score_engine_0diff_vs_2474b04a_baseline']}")
    print(f"router_v2 0-diff vs 2474b04a: {no_bleed_confirmation['router_v2_0diff_vs_2474b04a_baseline']}")
    print(f"Run record: {rr_path}  sha256={rr_sha}")
    print(f"Manifest: {manifest_path}  sha256={manifest_sha}")
    print("=" * 80)

    return run_record, rr_sha, manifest, manifest_sha


if __name__ == "__main__":
    main()
