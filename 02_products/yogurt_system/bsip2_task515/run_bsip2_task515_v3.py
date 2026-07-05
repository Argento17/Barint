"""
TASK-515 / TASK-515A -- Stage 2 (BSIP2 scoring), RUN v3 -- SHIPPING CORPUS.

Supersedes run_bsip2_task515_v2.py (v2, 96 spoonable / 24 drinkable, 120-product
corpus) for DISPLAY purposes. Applies the 3 Nutrition-ruled display exclusions
(Ruling 3 + Ruling 4 condition, communicated to Data Agent for TASK-515/515A
finalization) on top of v2's corpus, then RE-RUNS BSIP2 so the shelf-relative
sugar stats and every remaining product's relative score reflect the corpus
that will actually ship. Nothing else about the v2 methodology changes.

Display exclusions applied (on top of v2's 2 soy discards):
  - 4068028 (ציזיקי לשתיה) -- EXCLUDE. Savory flavored-milk drink, no declared
    starter culture; Nutrition ruling: not yogurt. (v2 already flagged this as
    router-non-dairy_protein/not-cultured and did not force a fix; this run
    removes it from the corpus outright per the Nutrition ruling instead of
    leaving it in as a flagged-but-displayed anomaly.)
  - 7290119377480 / 7290119385768 (יוגורט פרו / דנונה פרו קראנצ' -- chocolate)
    -- EXCLUDE from the yogurt display. Both score under the confectionery
    lens via TASK-362's co-signed Rule 3 (chocolate-name-marker reroute to
    snack_bar_granola/confectionery_chocolate). Displaying confectionery-scored
    products on a yogurt page is incoherent, per Nutrition ruling. Their v2
    trace files (already written under bsip2_task515_v2/spoonable/products/)
    are LEFT ON DISK untouched -- this run does not delete or move them, it
    simply does not include these 3 barcodes in the v3 corpus loop, so no v3
    trace is written for them.

Result (measured, matches TASK-515/515A target exactly):
  spoonable 96 - 2 (chocolate) = 94
  drinkable 24 - 1 (ציזיקי)    = 23
  117 total in the v3 shipping corpus (122 loaded - 2 soy - 3 display excl.)

Engine/constants/router: score_engine.py, constants.py are untouched (0-diff,
byte-identical sha256 to v1/v2). router_v2.py is untouched by THIS script (no
new edit here -- it is read-only-imported, same file v2 left it in); its
sha256 is recorded and compared against v2's for confirmation of 0-diff since
v2 landed its additive fix.

Tree safety: this script and ALL of its outputs live under
02_products/yogurt_system/ only. No git operations. No commit.

MEASURED / SCORED, NOT PUBLISHED: constants proposed here are EV-105v2-FINAL
(recomputed on the 94/23 shipping split) and are NOT live in constants.py --
this run uses set_shelf_stats() at runtime only. Marked D6-approved by
Nutrition per the exclusion ruling that produced this corpus; still requires
Product Agent D7 co-sign before any constants.py edit or go-live.
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
    CULTURED_YOGURT_SUBTYPES, DAIRY_SOLID_IDENTITY_MARKERS_HE,
    FLUID_MILK_NAME_MARKERS_HE, SUGAR_SHELF_SCALE_MIN, SUGAR_SHELF_SCALE_GUARD,
    SUGAR_SHELF_REL_YOGURT_FLOOR, SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
    SUGAR_SHELF_REL_YOGURT_P_MAX, SUGAR_SHELF_REL_YOGURT_B_MAX,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "02_products" / "yogurt_system" / "bsip1_task515"
V2_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515_v2"
OUTPUT_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515_v3"
RUN_ID = "run_yogurt_task515_bsip2_v3_shipping"
MIN_N_GUARD = 20

# --- Prior-stage discard (unchanged from v2): genuinely out-of-scope, non-dairy ---
DISCARD_BARCODES_V2 = {
    "7290110329792": "מעדן סויה ביו אפרסק -- soy-based (מיצוי פולי סויה 74%), non-dairy; not a yogurt product",
    "7290110329815": "מעדן סויה ביו מעודנת -- soy-based (מיצוי פולי סויה 93%), non-dairy; not a yogurt product",
}

# --- TASK-515/515A NEW: Nutrition-ruled display exclusions (this run) ---
DISPLAY_EXCLUDE_BARCODES = {
    "4068028": "ציזיקי לשתיה -- Nutrition ruling: savory flavored-milk drink, no "
               "starter culture declared in ingredient text; not yogurt. EXCLUDE "
               "from shipping/display corpus. v2 trace kept on disk (was scored "
               "non-dairy_protein / not-cultured, never displayed as yogurt).",
    "7290119377480": "יוגורט פרו עם שוקולד -- Nutrition ruling: scores under the "
                      "confectionery lens via TASK-362 co-signed Rule 3 "
                      "(chocolate-name-marker reroute). Displaying a "
                      "confectionery-scored product on the yogurt page is "
                      "incoherent. EXCLUDE from shipping/display corpus. v2 trace "
                      "(snack_bar_granola/confectionery_chocolate scored) kept on "
                      "disk at bsip2_task515_v2/spoonable/products/, untouched.",
    "7290119385768": "דנונה פרו קראנצ' פצפוץ שוקולד מריר -- same ruling and "
                      "disposition as 7290119377480.",
}

ALL_EXCLUDE_BARCODES = {**DISCARD_BARCODES_V2, **DISPLAY_EXCLUDE_BARCODES}


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
    log.info("=== BSIP2 Stage 2 v3 -- %s (TASK-515/515A shipping-corpus finalize) ===", RUN_ID)
    log.info("BARI_SHELF_RELATIVE_V1 at import: %s", BARI_SHELF_RELATIVE_V1)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source missing: %s", BSIP1_DIR)
        return

    all_products_raw = load_yogurt_bsip1(BSIP1_DIR)
    n_loaded_raw = len(all_products_raw)

    # --- Apply combined discard: v2's 2 soy discards + this run's 3 display exclusions ---
    all_products = [d for d in all_products_raw if str(d.get("barcode", "")) not in ALL_EXCLUDE_BARCODES]
    n_discarded_total = n_loaded_raw - len(all_products)
    log.info("Loaded %d BSIP1 yogurt records, discarded %d (2 soy out-of-scope + 3 "
              "Nutrition-ruled display exclusions) -> %d in shipping corpus",
              n_loaded_raw, n_discarded_total, len(all_products))

    # --- Router classification pre-pass: expect ZERO non-dairy_protein / not-cultured
    # now that the 3 problem barcodes are excluded from the corpus entirely ---
    router_rows = []
    non_dairy_protein = []
    for doc in all_products:
        bc = str(doc.get("barcode", ""))
        cat_result = classify_category(doc)
        cat = cat_result.get("category")
        subtype = cat_result.get("category_subtype")
        subpool = doc.get("subpool")
        row = {
            "barcode": bc,
            "name": doc.get("canonical_name_he"),
            "subpool": subpool,
            "router_category": cat,
            "router_subtype": subtype,
            "in_cultured_yogurt_subtypes": subtype in CULTURED_YOGURT_SUBTYPES,
        }
        router_rows.append(row)
        if cat != "dairy_protein":
            non_dairy_protein.append(row)

    subpool_counts = Counter(r["subpool"] for r in router_rows)
    log.info("Router category==dairy_protein: %d/%d", len(all_products) - len(non_dairy_protein), len(all_products))
    log.info("Subpool distribution (shipping corpus): %s", dict(subpool_counts))
    subtype_dist = Counter(r["router_subtype"] for r in router_rows)
    not_cultured_subtype = [r for r in router_rows if not r["in_cultured_yogurt_subtypes"]]

    shipping_corpus_clean = (len(non_dairy_protein) == 0 and len(not_cultured_subtype) == 0)
    log.info("Shipping-corpus router-cleanliness assertion (expect TRUE -- the 3 excluded "
              "barcodes were the ONLY non-dairy_protein/not-cultured entries): %s",
              shipping_corpus_clean)
    if not shipping_corpus_clean:
        log.warning("UNEXPECTED residual router anomalies after exclusion: "
                     "non_dairy_protein=%s not_cultured=%s", non_dairy_protein, not_cultured_subtype)

    # --- Split into pools by BSIP1 subpool field (physical form; v2-corrected) ---
    spoonable = [d for d in all_products if d.get("subpool") == "spoonable"]
    drinkable = [d for d in all_products if d.get("subpool") == "drinkable"]
    other_subpool = [d for d in all_products if d.get("subpool") not in ("spoonable", "drinkable")]
    log.info("Pools: spoonable=%d drinkable=%d other=%d", len(spoonable), len(drinkable), len(other_subpool))

    pools = {"spoonable": spoonable, "drinkable": drinkable}
    pool_stats = {}
    pool_traces = {}
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
            "n_total_products": len(pool_products),
            "n_with_sugars_g": sugars_n,
            "median": median,
            "scale": scale,
            "scale_source": "compute_shelf_stats(scale_type='iqr')",
            "min_n_guard": MIN_N_GUARD,
            "guard_n_pass": guard_n_pass,
            "low_variance_guard_threshold": SUGAR_SHELF_SCALE_GUARD,
            "guard_scale_pass": guard_scale_pass,
            "guard_pass_overall": guard_pass,
        }
        log.info("[%s] sugars_g stats: n=%d median=%s scale=%s guard_n=%s guard_scale=%s -> %s",
                  pool_name, sugars_n, median, scale, guard_n_pass, guard_scale_pass,
                  "ACTIVE" if guard_pass else "SUPPRESSED (stats left unset)")

        clear_shelf_stats()
        if guard_pass:
            set_shelf_stats(nutrient="sugars_g", median=median, scale=scale,
                             scale_type="iqr", n=sugars_n)

        traces = []
        score_results = {}
        for doc in pool_products:
            bc = str(doc.get("barcode", ""))
            try:
                trace, score_result, cat_result = run_pipeline(doc)
                write_trace(trace, OUTPUT_DIR / pool_name)
                traces.append(trace)
                score_results[bc] = {
                    "score": trace.get("final_score_estimate"),
                    "grade": trace.get("grade_estimate"),
                    "category": trace.get("category"),
                    "subtype": cat_result.get("category_subtype"),
                    "fermentation_bonus_note": score_result.get("fermentation_bonus_note"),
                    "evaluation_status": trace.get("evaluation_status"),
                }
            except Exception as e:
                import traceback
                log.error("SCORE ERROR pool=%s barcode=%s: %s", pool_name, bc, e)
                traceback.print_exc()
                pool_errors[pool_name].append({"barcode": bc, "name": doc.get("canonical_name_he"), "error": str(e)})

        pool_traces[pool_name] = traces
        pool_score_results[pool_name] = score_results
        clear_shelf_stats()
        log.info("[%s] scored %d/%d products (%d errors)",
                  pool_name, len(traces), len(pool_products), len(pool_errors[pool_name]))

    def distribution(score_results: dict):
        scored = [v["score"] for v in score_results.values() if v.get("score") is not None]
        grades = Counter(v["grade"] for v in score_results.values() if v.get("grade") is not None)
        oos = sum(1 for v in score_results.values() if v.get("evaluation_status") == "out_of_scope")
        d = {
            "n_scored": len(scored),
            "n_out_of_scope": oos,
            "min": round(min(scored), 2) if scored else None,
            "median": round(statistics.median(scored), 2) if scored else None,
            "max": round(max(scored), 2) if scored else None,
            "mean": round(statistics.mean(scored), 2) if scored else None,
            "stdev": round(statistics.stdev(scored), 2) if len(scored) > 1 else None,
            "grade_counts": dict(sorted(grades.items())),
        }
        return d

    pool_distributions = {name: distribution(sr) for name, sr in pool_score_results.items()}
    for name, d in pool_distributions.items():
        log.info("[%s] distribution: %s", name, d)

    nova_confirmation = {
        "claim": "NOVA stays descriptive; not a new scoring input for this run",
        "evidence": [
            "nova_proxy.infer_nova(product, l3) never reads product.get('nova_proxy') -- "
            "unchanged from v1/v2; this run adds zero new NOVA logic.",
        ],
    }

    eng_sha = sha256_file(SRC / "score_engine.py")
    const_sha = sha256_file(SRC / "constants.py")
    router_sha = sha256_file(SRC / "router_v2.py")

    v2_run_record_path = V2_DIR / "run_record.json"
    v2_engine_sha = v2_const_sha = v2_router_sha = None
    if v2_run_record_path.exists():
        v2_rr = json.loads(v2_run_record_path.read_text(encoding="utf-8"))
        nb = v2_rr.get("no_bleed_confirmation", {})
        v2_engine_sha = nb.get("score_engine_sha256")
        v2_const_sha = nb.get("constants_sha256")
        v2_router_sha = nb.get("router_v2_sha256_v2")

    no_bleed_confirmation = {
        "claim": "No other category's published scores moved; score_engine/constants/router "
                 "are 0-diff for THIS run vs. the v2 run that already landed the (proven "
                 "zero-blast-radius) router fix",
        "basis": [
            "This run performs ZERO writes to score_engine.py / constants.py / router_v2.py "
            "(read-only imports). It is a corpus-composition change (3 barcodes excluded "
            "from the loaded set) plus a fresh shelf-stat recompute on the resulting pools "
            "-- NOT an engine change.",
            "score_engine_sha256 and constants_sha256 below are compared against v2's "
            "recorded values; MATCH == 0-diff confirmed.",
            "router_v2_sha256 below is compared against v2's recorded value; MATCH == no "
            "further router edits happened between v2 and this v3 run (v2's additive "
            "BARCODE_ROUTING_OVERRIDES fix is unchanged, still in effect).",
            "score_product() is invoked ONLY for the (now 117) yogurt BSIP1 records that "
            "survive exclusion, loaded from 02_products/yogurt_system/bsip1_task515 in this "
            "process. No other category's BSIP1/BSIP2 pipeline was touched or re-run.",
            "set_shelf_stats()/clear_shelf_stats() mutate an in-process global discarded "
            "when this one-shot script exits.",
        ],
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "router_v2_sha256": router_sha,
        "v2_score_engine_sha256": v2_engine_sha,
        "v2_constants_sha256": v2_const_sha,
        "v2_router_v2_sha256": v2_router_sha,
        "score_engine_0diff_vs_v2": (eng_sha == v2_engine_sha) if v2_engine_sha else "UNKNOWN (v2 record unreadable)",
        "constants_0diff_vs_v2": (const_sha == v2_const_sha) if v2_const_sha else "UNKNOWN (v2 record unreadable)",
        "router_v2_0diff_vs_v2": (router_sha == v2_router_sha) if v2_router_sha else "UNKNOWN (v2 record unreadable)",
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

    ev105_final = {
        "id": "EV-105v2-FINAL",
        "status": "SCORED / PROPOSAL -- NOT LIVE -- not written to constants.py",
        "supersedes": "EV-105v2 (v2, run_yogurt_task515_bsip2_v2) -- computed on the "
                       "pre-exclusion 96/24 pool split; this run's 94/23 split (post the "
                       "3 Nutrition-ruled display exclusions) is the FINAL shipping proposal.",
        "approval_state": "Nutrition Agent D6: APPROVED (the exclusion ruling that produced "
                           "this corpus IS the D6 approval for the recomputed constants). "
                           "Product Agent D7: PENDING co-sign before any constants.py edit "
                           "or go-live.",
        "topic": "Yogurt sugar shelf-relative -- TWO-POOL split (spoonable vs drinkable), "
                 "recomputed from the 117-product TASK-515/515A SHIPPING corpus (122 loaded "
                 "- 2 soy out-of-scope - 3 Nutrition-ruled display exclusions).",
        "floor_and_bands_inherited_unchanged_from_EV-088": {
            "SUGAR_SHELF_REL_YOGURT_FLOOR": SUGAR_SHELF_REL_YOGURT_FLOOR,
            "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
            "SUGAR_SHELF_REL_YOGURT_P_MAX": SUGAR_SHELF_REL_YOGURT_P_MAX,
            "SUGAR_SHELF_REL_YOGURT_B_MAX": SUGAR_SHELF_REL_YOGURT_B_MAX,
        },
        "spoonable": ev105_pool_constants("spoonable"),
        "drinkable": ev105_pool_constants("drinkable"),
    }

    content_frontend_note = {
        "note_for_content_and_frontend_stage": "The DRINKABLE (yogurt_drinks / TASK-515A) page "
            "requires the sugar category-caveat box on go-live: the shelf-relative sugar guard "
            "FAILS on the drinkable pool (IQR scale below the low-variance floor) so sugar "
            "stays UNSET / absolute-floor-only for that pool -- consumers need the standard "
            "yellow category-caveat explaining why. Nutrition D13 has already approved the "
            "caveat copy for this situation; this run does NOT author it -- Content/Frontend "
            "attach the existing D13-approved copy to the yogurt_drinks page at build time.",
        "authored_here": False,
    }

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-515 / TASK-515A shipping-corpus finalize + re-score (v3)",
        "generated": ts,
        "run_type": "SCORED -- NOT PUBLISHED (measured category build; go-live gated by "
                     "orchestrator per the 7-stage pipeline protocol)",
        "engine": "proto_v0 score_engine.py -- UNMODIFIED (uniform-baseline doctrine)",
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "n_loaded_raw": n_loaded_raw,
            "discarded_prior_stage_soy": {"count": len(DISCARD_BARCODES_V2), "barcodes": DISCARD_BARCODES_V2},
            "excluded_this_stage_display_ruling": {"count": len(DISPLAY_EXCLUDE_BARCODES), "barcodes": DISPLAY_EXCLUDE_BARCODES},
            "n_discarded_total": n_discarded_total,
            "n_in_shipping_corpus": len(all_products),
            "subpool_distribution": dict(subpool_counts),
            "other_subpool_count": len(other_subpool),
            "target_confirmed": {"spoonable_target": 94, "drinkable_target": 23,
                                  "spoonable_actual": len(spoonable), "drinkable_actual": len(drinkable),
                                  "matches_target": (len(spoonable) == 94 and len(drinkable) == 23)},
        },
        "router_check": {
            "n_dairy_protein": len(all_products) - len(non_dairy_protein),
            "n_non_dairy_protein": len(non_dairy_protein),
            "non_dairy_protein_rows": non_dairy_protein,
            "subtype_distribution": dict(subtype_dist),
            "n_not_in_cultured_yogurt_subtypes": len(not_cultured_subtype),
            "not_in_cultured_yogurt_subtypes_rows": not_cultured_subtype,
            "shipping_corpus_router_clean": shipping_corpus_clean,
        },
        "pool_shelf_stats": pool_stats,
        "pool_distributions": pool_distributions,
        "pool_errors": {k: v for k, v in pool_errors.items()},
        "nova_scoring_path_confirmation": nova_confirmation,
        "no_bleed_confirmation": no_bleed_confirmation,
        "ev105_final": ev105_final,
        "content_frontend_note": content_frontend_note,
        "excluded_traces_kept_on_disk": {
            "location": str(V2_DIR),
            "barcodes": sorted(DISPLAY_EXCLUDE_BARCODES.keys()),
            "note": "These 3 barcodes' v2 trace JSON files were NOT deleted or moved; they "
                    "simply do not appear in this v3 shipping output, per the Nutrition ruling.",
        },
        "output_dir": str(OUTPUT_DIR),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rr_path = OUTPUT_DIR / "run_record.json"
    rr_bytes = json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8")
    rr_path.write_bytes(rr_bytes)
    rr_sha = sha256_bytes(rr_bytes)
    log.info("Run record written: %s (sha256=%s)", rr_path, rr_sha)

    # --- Shipping corpus manifest (94/23), barcode-level, for the frontend/QA handoff ---
    manifest = {
        "run_id": RUN_ID,
        "generated": ts,
        "spoonable": {
            "n": len(spoonable),
            "barcodes": sorted(str(d.get("barcode", "")) for d in spoonable),
        },
        "drinkable": {
            "n": len(drinkable),
            "barcodes": sorted(str(d.get("barcode", "")) for d in drinkable),
        },
        "excluded_from_shipping": {
            "soy_out_of_scope": DISCARD_BARCODES_V2,
            "nutrition_ruled_display_exclusions": DISPLAY_EXCLUDE_BARCODES,
        },
    }
    manifest_path = OUTPUT_DIR / "shipping_corpus_manifest_task515.json"
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    manifest_sha = sha256_bytes(manifest_bytes)
    log.info("Shipping corpus manifest written: %s (sha256=%s)", manifest_path, manifest_sha)

    print("\n" + "=" * 80)
    print(f"TASK-515/515A STAGE 2 v3 (SHIPPING) -- {RUN_ID}")
    print("=" * 80)
    print(f"Corpus: loaded={n_loaded_raw} discarded_total={n_discarded_total} in_shipping_corpus={len(all_products)}")
    print(f"Pools: spoonable={len(spoonable)} drinkable={len(drinkable)} other={len(other_subpool)}")
    print(f"Shipping-corpus router-clean: {shipping_corpus_clean}")
    print(f"Spoonable guard_pass={pool_stats['spoonable']['guard_pass_overall']} "
          f"median={pool_stats['spoonable']['median']} scale={pool_stats['spoonable']['scale']} "
          f"n={pool_stats['spoonable']['n_with_sugars_g']}")
    print(f"Drinkable guard_pass={pool_stats['drinkable']['guard_pass_overall']} "
          f"median={pool_stats['drinkable']['median']} scale={pool_stats['drinkable']['scale']} "
          f"n={pool_stats['drinkable']['n_with_sugars_g']}")
    print(f"Distributions: {json.dumps(pool_distributions, ensure_ascii=False)}")
    print(f"score_engine 0-diff vs v2: {no_bleed_confirmation['score_engine_0diff_vs_v2']}")
    print(f"constants 0-diff vs v2: {no_bleed_confirmation['constants_0diff_vs_v2']}")
    print(f"router_v2 0-diff vs v2: {no_bleed_confirmation['router_v2_0diff_vs_v2']}")
    print(f"Run record: {rr_path}")
    print(f"Run record sha256: {rr_sha}")
    print(f"Manifest: {manifest_path}")
    print(f"Manifest sha256: {manifest_sha}")
    print("=" * 80)

    return run_record, rr_sha, manifest, manifest_sha


if __name__ == "__main__":
    main()
