"""
TASK-515A -- Stage 2 (BSIP2 scoring), D7 SUPPRESSION rescore, DRINKABLE POOL ONLY.

Product Agent (D7) ruling on the v3-REMEDIATION finding (run_yogurt_task515_bsip2_v3_remediation,
run_record.json): the drinkable pool's sugar shelf-relative low-variance guard flipped from FAIL
(scale=1.85 at n=23, EV-105v2-FINAL) to PASS (scale=3.11 at n=20, EV-105v3-REMEDIATION) -- but
D7 ruled this PASS is NOT ROBUST: adding any single product to the pool flips it back to FAIL
(C3 stress test). D7 = CONSERVATIVE: treat the guard as FAIL for yogurt_drinkable this cycle.
Sugar must contribute ONLY via the absolute floor (EV-088, sugars_g>=12.0g -> cap 62), never via
the shelf-relative surcharge/relief (SUGAR_SHELF_REL_V1, P_max=6/B_max=3 bands).

MECHANISM (no score_engine.py edit -- tripwire-1 respected):
  score_engine.py's EV-088 yogurt x sugar shelf-relative surcharge/relief block (line ~2458-2481)
  calls shelf_relative_differentiator(nutrient="sugars_g", ...), which reads the module-level
  _SHELF_STATS dict via _SHELF_STATS.get("sugars_g"). If that key is absent, the function returns
  (0, "sugars_g: shelf stats not set") -- i.e. NO penalty/relief, unconditionally -- BEFORE it ever
  reaches the low-variance-guard check on the caller-supplied stats. This early-return branch is
  the score_engine.py's own EXISTING behavior, exercised here purely by NEVER calling
  set_shelf_stats("sugars_g", ...) while scoring the drinkable pool.
  The EV-088 FLOOR (line ~3976-3997) reads nn.get("sugars_g") directly and compares it to the flat
  SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G=12.0 constant -- it does NOT read _SHELF_STATS at all --
  so it is completely unaffected by this suppression and continues to fire normally.

  The suppression itself lives ENTIRELY in this run script (D7_SUPPRESS_SHELF_REL_POOLS below): a
  per-pool override that forces the pool's "effective" guard decision to False regardless of the
  computed guard_pass_overall, for the drinkable pool only. Per D7: do NOT write a
  SUGAR_SHELF_REL_YOGURT_DRINKABLE_* constant to constants.py this cycle (that would be the
  opposite of suppression -- it would activate the mechanism this ruling suppresses).

SCOPE: drinkable pool ONLY. Spoonable is untouched by this script -- it is not loaded, not scored,
its trace files are not written, and constants.py/score_engine.py/router_v2.py are read-only
imports (sha256 recorded + compared to the committed 2474b04a baseline for 0-diff proof).

Corpus: IDENTICAL to run_bsip2_task515_v3_remediation.py's 98-product remediated shipping corpus
(78 spoonable / 20 drinkable) -- same exclusion sets, copied verbatim from that script so the
drinkable pool membership (n=20) is byte-identical. This script re-scores ONLY the 20 drinkable
members through the SAME unmodified engine, with ONLY the shelf-stats call suppressed for
"sugars_g" during that pool's scoring loop.

Tree safety: writes ONLY into
02_products/yogurt_system/bsip2_task515_v3/drinkable/products/*/bsip2_trace.json (overwriting the
20 currently-shipping drinkable traces in place -- same "overwrite in place" precedent the v3 and
v3-remediation runs used) and a new run_record_task515a_d7_suppress_drinkable.json in
bsip2_task515_v3/. Does not touch spoonable/, does not touch bari-web, no git operations.
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
RUN_ID = "run_yogurt_task515_bsip2_v3a_d7_suppress_drinkable"
MIN_N_GUARD = 20

# D7 (Product Agent) ruling, 2026-07-05: treat the drinkable pool's sugar shelf-relative
# low-variance guard as FAIL this cycle, regardless of the computed guard_pass_overall value.
# Spoonable is NOT in this set -- unaffected, not processed by this script at all.
D7_SUPPRESS_SHELF_REL_POOLS = frozenset({"drinkable"})

# --- Carried forward VERBATIM from run_bsip2_task515_v3_remediation.py so the drinkable
# pool membership (n=20) is byte-identical to the committed remediation run. ---
DISCARD_BARCODES_V2 = {
    "7290110329792": "מעדן סויה ביו אפרסק -- soy-based, non-dairy; not a yogurt product",
    "7290110329815": "מעדן סויה ביו מעודנת -- soy-based, non-dairy; not a yogurt product",
}
DISPLAY_EXCLUDE_BARCODES_V3 = {
    "4068028": "ציזיקי לשתיה -- Nutrition ruling: savory flavored-milk drink, not yogurt.",
    "7290119377480": "יוגורט פרו עם שוקולד -- confectionery-lens (TASK-362 Rule 3).",
    "7290119385768": "דנונה פרו קראנצ' פצפוץ שוקולד מריר -- same ruling as above.",
}
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
DEDUP_BARCODES = {
    "57149": "dedup-drop: byte-identical duplicate of canonical EAN-13 7290014758100 (KEPT).",
    "7290014758117": "dedup-drop (owner ruling): byte-identical duplicate of clean twin 57132 (KEPT); also carries confirmed Class-D diabetes-seal certification-text contamination -- dropping removes both the duplicate and the contamination in one action.",
    "6664655": "dedup-drop: byte-identical duplicate of canonical EAN-13 7290119380923 (KEPT).",
}
ALL_EXCLUDE_BARCODES = {
    **DISCARD_BARCODES_V2, **DISPLAY_EXCLUDE_BARCODES_V3, **DUMP_BARCODES, **DEDUP_BARCODES,
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
    log.info("=== BSIP2 Stage 2 v3a D7-SUPPRESS (drinkable only) -- %s ===", RUN_ID)
    log.info("BARI_SHELF_RELATIVE_V1 at import: %s", BARI_SHELF_RELATIVE_V1)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source missing: %s", BSIP1_DIR)
        return

    all_products_raw = load_yogurt_bsip1(BSIP1_DIR)
    n_loaded_raw = len(all_products_raw)
    all_products = [d for d in all_products_raw if str(d.get("barcode", "")) not in ALL_EXCLUDE_BARCODES]
    n_discarded_total = n_loaded_raw - len(all_products)

    spoonable_count = sum(1 for d in all_products if d.get("subpool") == "spoonable")
    drinkable = [d for d in all_products if d.get("subpool") == "drinkable"]
    log.info("Loaded %d, discarded %d -> %d in remediated shipping corpus (spoonable=%d "
             "[NOT PROCESSED -- untouched] / drinkable=%d [scored below])",
             n_loaded_raw, n_discarded_total, len(all_products), spoonable_count, len(drinkable))

    # --- Compute the pool's sugars_g shelf stats for the RECORD (transparency) only. ---
    sugars_n = sum(1 for d in drinkable if get_sugars_g(d) is not None)
    median, scale = compute_shelf_stats(
        drinkable, "sugars_g", scale_type="iqr", nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
    )
    guard_n_pass = sugars_n >= MIN_N_GUARD
    guard_scale_pass = (scale is not None) and (scale >= SUGAR_SHELF_SCALE_GUARD)
    computed_guard_pass = bool(median is not None and scale is not None and guard_n_pass and guard_scale_pass)

    d7_suppressed = "drinkable" in D7_SUPPRESS_SHELF_REL_POOLS
    effective_guard_pass = False if d7_suppressed else computed_guard_pass

    pool_stats = {
        "n_total_products": len(drinkable), "n_with_sugars_g": sugars_n,
        "median": median, "scale": scale, "scale_source": "compute_shelf_stats(scale_type='iqr')",
        "min_n_guard": MIN_N_GUARD, "guard_n_pass": guard_n_pass,
        "low_variance_guard_threshold": SUGAR_SHELF_SCALE_GUARD,
        "guard_scale_pass": guard_scale_pass,
        "computed_guard_pass_overall": computed_guard_pass,
        "d7_suppression_applied": d7_suppressed,
        "d7_suppression_rationale": (
            "Product Agent (D7) ruled the computed PASS (scale=3.11 at n=20, margin 0.11 above "
            "the 3.0 guard) is NOT ROBUST -- C3 showed adding any single product flips it to FAIL. "
            "D7 = CONSERVATIVE: treat as FAIL this cycle. Sugar contributes ONLY via the EV-088 "
            "absolute floor (sugars_g>=12.0g -> cap 62), never via the shelf-relative "
            "surcharge/relief. No SUGAR_SHELF_REL_YOGURT_DRINKABLE_* constant is written."
        ) if d7_suppressed else None,
        "effective_guard_pass_used_for_scoring": effective_guard_pass,
    }
    log.info("[drinkable] sugars_g stats: n=%d median=%s scale=%s computed_guard_pass=%s "
             "d7_suppressed=%s -> effective=%s (%s)",
             sugars_n, median, scale, computed_guard_pass, d7_suppressed, effective_guard_pass,
             "ACTIVE (set_shelf_stats called)" if effective_guard_pass else
             "SUPPRESSED (stats left UNSET -- surcharge/relief cannot fire; floor unaffected)")

    clear_shelf_stats()
    if effective_guard_pass:
        set_shelf_stats(nutrient="sugars_g", median=median, scale=scale, scale_type="iqr", n=sugars_n)
    # else: _SHELF_STATS has no "sugars_g" entry for the whole drinkable scoring loop below ->
    # shelf_relative_differentiator("sugars_g", ...) returns (0, "sugars_g: shelf stats not set")
    # for every drinkable product, unconditionally. EV-088 floor is untouched (reads nn directly).

    traces = []
    score_results = {}
    errors = []
    for doc in drinkable:
        bc = str(doc.get("barcode", ""))
        try:
            trace, score_result, cat_result = run_pipeline(doc)
            write_trace(trace, OUTPUT_DIR / "drinkable")
            traces.append(trace)
            score_results[bc] = {
                "score": trace.get("final_score_estimate"), "grade": trace.get("grade_estimate"),
                "category": trace.get("category"), "subtype": cat_result.get("category_subtype"),
                "evaluation_status": trace.get("evaluation_status"),
                "penalties_applied": trace.get("penalties_applied"),
            }
        except Exception as e:
            import traceback
            log.error("SCORE ERROR barcode=%s: %s", bc, e)
            traceback.print_exc()
            errors.append({"barcode": bc, "name": doc.get("canonical_name_he"), "error": str(e)})

    clear_shelf_stats()
    log.info("[drinkable] scored %d/%d products (%d errors)", len(traces), len(drinkable), len(errors))

    def distribution(sr: dict):
        scored = [v["score"] for v in sr.values() if v.get("score") is not None]
        grades = Counter(v["grade"] for v in sr.values() if v.get("grade") is not None)
        oos = sum(1 for v in sr.values() if v.get("evaluation_status") == "out_of_scope")
        return {
            "n_scored": len(scored), "n_out_of_scope": oos,
            "min": round(min(scored), 2) if scored else None,
            "median": round(statistics.median(scored), 2) if scored else None,
            "max": round(max(scored), 2) if scored else None,
            "mean": round(statistics.mean(scored), 2) if scored else None,
            "stdev": round(statistics.stdev(scored), 2) if len(scored) > 1 else None,
            "grade_counts": dict(sorted(grades.items())),
        }

    dist = distribution(score_results)
    log.info("[drinkable] distribution: %s", dist)

    eng_sha = sha256_file(SRC / "score_engine.py")
    const_sha = sha256_file(SRC / "constants.py")
    router_sha = sha256_file(SRC / "router_v2.py")
    BASELINE_ENGINE_SHA = "535a9ed1b704e587546c2c314ef76abddf543310dcce0b7e74fb8e7f26453f34"
    BASELINE_ROUTER_SHA = "9da6f3b7b86a82c4e655fe2768dcf018b478999a8fea4ab0364c21274103e3f9"
    # constants.py sha differs from the ORIGINAL 2474b04a baseline for the same documented reason
    # as v3-remediation (a prior additive display-only change landed before that run) -- this
    # script does not touch constants.py at all (read-only import), so its sha must match
    # v3-remediation's own recorded constants_sha256 exactly (0-diff vs THAT baseline).
    V3_REMEDIATION_CONST_SHA = "e70689a7f901dd26919444054fea1964ebb895e2117c788f6a7c5bea3d962e6c"

    no_bleed_confirmation = {
        "claim": "Zero writes to score_engine.py / constants.py / router_v2.py this run "
                 "(read-only imports). The suppression mechanism lives entirely in THIS run "
                 "script (D7_SUPPRESS_SHELF_REL_POOLS gating whether set_shelf_stats('sugars_g', "
                 "...) is called before the drinkable scoring loop) -- score_engine.py's own "
                 "existing 'stats not set -> delta=0' early-return branch (shelf_relative_"
                 "differentiator, ~line 478-480) does the rest, unmodified.",
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "router_v2_sha256": router_sha,
        "score_engine_0diff_vs_2474b04a_baseline": (eng_sha == BASELINE_ENGINE_SHA),
        "router_v2_0diff_vs_2474b04a_baseline": (router_sha == BASELINE_ROUTER_SHA),
        "constants_0diff_vs_v3_remediation_run": (const_sha == V3_REMEDIATION_CONST_SHA),
    }

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-515A D7 suppression rescore -- drinkable pool sugar shelf-relative "
                "surcharge/relief forced OFF (guard treated as FAIL per Product Agent D7 ruling), "
                "absolute floor (EV-088) unaffected. Spoonable NOT processed by this script.",
        "generated": ts,
        "run_type": "SCORED -- NOT PUBLISHED (co-sign package; go-live gated by orchestrator)",
        "engine": "proto_v0 score_engine.py -- UNMODIFIED (uniform-baseline doctrine)",
        "supersedes_for_drinkable_only": "run_yogurt_task515_bsip2_v3_remediation (same 20-product "
                                          "drinkable pool membership; ONLY the sugar shelf-relative "
                                          "surcharge/relief mechanism differs -- forced OFF here)",
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "n_loaded_raw": n_loaded_raw,
            "n_discarded_total": n_discarded_total,
            "n_in_shipping_corpus_all_pools": len(all_products),
            "drinkable_n": len(drinkable),
            "drinkable_target": 20,
            "drinkable_matches_target": len(drinkable) == 20,
            "spoonable_n_present_but_not_processed": spoonable_count,
        },
        "drinkable_sugar_shelf_rel_stats": pool_stats,
        "drinkable_distribution": dist,
        "drinkable_errors": errors,
        "no_bleed_confirmation": no_bleed_confirmation,
        "d7_ruling": {
            "decision": "CONSERVATIVE -- suppress shelf-relative sugar for the drinkable pool",
            "mechanism": "run-script-level per-pool override (D7_SUPPRESS_SHELF_REL_POOLS); "
                         "set_shelf_stats('sugars_g', ...) never called while scoring drinkable "
                         "-> EV-088 surcharge/relief returns delta=0 for every drinkable product "
                         "(score_engine.py's own existing 'stats not set' branch); EV-088 floor "
                         "(flat 12.0g threshold, cap 62) is untouched and continues to fire.",
            "constant_written_to_constants_py": False,
            "note": "Per instruction: do NOT write SUGAR_SHELF_REL_YOGURT_DRINKABLE_* this cycle.",
        },
        "output_dir": str(OUTPUT_DIR / "drinkable"),
    }

    rr_path = OUTPUT_DIR / "run_record_task515a_d7_suppress_drinkable.json"
    rr_bytes = json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8")
    rr_path.write_bytes(rr_bytes)
    rr_sha = sha256_bytes(rr_bytes)
    log.info("Run record written: %s (sha256=%s)", rr_path, rr_sha)

    print("\n" + "=" * 80)
    print(f"TASK-515A D7-SUPPRESS RESCORE (drinkable only) -- {RUN_ID}")
    print("=" * 80)
    print(f"Drinkable n={len(drinkable)} (target 20, match={len(drinkable) == 20})")
    print(f"Computed guard_pass={computed_guard_pass} median={median} scale={scale} n={sugars_n}")
    print(f"D7 suppression applied: {d7_suppressed} -> effective_guard_pass={effective_guard_pass}")
    print(f"Distribution: {json.dumps(dist, ensure_ascii=False)}")
    print(f"score_engine 0-diff vs 2474b04a: {no_bleed_confirmation['score_engine_0diff_vs_2474b04a_baseline']}")
    print(f"router_v2 0-diff vs 2474b04a: {no_bleed_confirmation['router_v2_0diff_vs_2474b04a_baseline']}")
    print(f"constants.py 0-diff vs v3-remediation run: {no_bleed_confirmation['constants_0diff_vs_v3_remediation_run']}")
    print(f"Run record: {rr_path}  sha256={rr_sha}")
    print("=" * 80)

    return run_record, rr_sha


if __name__ == "__main__":
    main()
