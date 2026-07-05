"""
TASK-515 / TASK-515A -- Stage 2 (BSIP2 scoring), RUN v2 -- ROUTER-CLASSIFICATION
GAP FIX RE-SCORE.

Supersedes run_bsip2_task515.py (v1), which found 20/122 yogurt-shelf products
did not route to dairy_protein (mostly Actimel/Activia/Danone-drink brand
transliterations lacking a "יוגורט" marker), plus 3 already-dairy_protein
products with no CULTURED_YOGURT_SUBTYPES subtype -- 23/122 total not-cultured.

This run:
  1. Applies the TASK-515 BARCODE_ROUTING_OVERRIDES fix landed in router_v2.py
     (18 barcodes -- additive, barcode-keyed, last-resort Stage-5 overrides;
     proven zero-blast-radius against 213 products across 4 other live
     categories -- milk_and_alternatives/hard_cheeses/snack_bars/juices --
     0 diffs, 0 barcode collisions; see run_yogurt_task515_v2_tripwire_proof.json).
  2. DISCARDS 2 genuinely out-of-scope products (soy-based, non-dairy "מעדן
     סויה ביו" desserts -- barcodes 7290110329792 / 7290110329815) from the
     corpus entirely, per the missing-data/out-of-scope discard rule. They were
     already correctly NOT routed to dairy_protein; this just removes them from
     the 122-count so they don't appear as "yogurt" pages at all.
  3. Leaves 3 products UNFIXED / flagged, by design (not forced):
       - 4068028  (ציזיקי לשתיה) -- ambiguous cultured-dairy-drink vs. prepared
         cucumber salad-drink; no declared starter culture in ingredient text.
         Flagged to Nutrition Agent for a ruling.
       - 7290119377480 / 7290119385768 (יוגורט פרו / דנונה פרו קראנצ' + chocolate)
         -- genuine yogurt, but TASK-362's co-signed chocolate-lens Rule 3
         deliberately reroutes them to snack_bar_granola/confectionery_chocolate.
         Fixing requires touching Rule 3 (cross-category blast radius) --
         out of scope for a barcode-only fix. Flagged to Nutrition/Product.
  4. Corrects one BSIP1 data field: barcode 7290110552244's `subpool` was
     'spoonable' but the product name is "משקה דנונה פרו20 ללת"ס" (a physical
     drink) -- corrected to 'drinkable' in the source JSON before this run so
     the two-pool sugar shelf-relative split compares it against the right
     reference set.
  5. Otherwise BYTE-IDENTICAL methodology to v1: same flag config, same two
     shelf-relative pools recomputed fresh from the (now 120-product) corpus,
     same engine call sequence, same fermentation spot-check, same
     no-engine/no-constants-change guarantee (score_engine.py and constants.py
     are untouched, read-only imports).

Tree safety: this script and ALL of its outputs live under
02_products/yogurt_system/ only. No git operations. No commit.

MEASURED / SCORED, NOT PUBLISHED: constants proposed here are EV-105v2 and are
NOT live in constants.py -- this run uses set_shelf_stats() at runtime only.
Requires Nutrition-D6 + Product-D7 co-sign before any constants.py edit or
go-live.
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
OUTPUT_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515_v2"
RUN_ID = "run_yogurt_task515_bsip2_v2"
MIN_N_GUARD = 20

# --- TASK-515 discard list: genuinely out-of-scope (soy-based, non-dairy) ---
DISCARD_BARCODES = {
    "7290110329792": "מעדן סויה ביו אפרסק -- soy-based (מיצוי פולי סויה 74%), non-dairy; not a yogurt product",
    "7290110329815": "מעדן סויה ביו מעודנת -- soy-based (מיצוי פולי סויה 93%), non-dairy; not a yogurt product",
}

# --- TASK-515 flagged-not-fixed (kept in corpus, routing intentionally left as-is) ---
FLAGGED_NOT_FIXED = {
    "4068028": "ציזיקי לשתיה -- AMBIGUOUS: cultured-dairy-drink vs. prepared cucumber "
               "salad-drink; no declared starter culture in ingredient text (unlike "
               "every fixed entry). Flagged to Nutrition Agent, not forced.",
    "7290119377480": "יוגורט פרו עם שוקולד -- SCOPE CONFLICT: genuine yogurt, but "
                      "TASK-362 co-signed Rule 3 (chocolate-name-marker) deliberately "
                      "reroutes to snack_bar_granola/confectionery_chocolate. Fixing "
                      "requires touching a cross-category rule -- flagged to "
                      "Nutrition/Product for a scoped ruling, not force-fixed here.",
    "7290119385768": "דנונה פרו קראנצ' פצפוץ שוקולד מריר -- SCOPE CONFLICT: same as "
                      "7290119377480.",
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


def name_has(markers, name: str) -> bool:
    tokens = set(name.split())
    return any((" " in m and m in name) or (m in tokens) for m in markers)


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
    log.info("=== BSIP2 Stage 2 v2 -- %s (TASK-515/515A router-gap re-score) ===", RUN_ID)
    log.info("BARI_SHELF_RELATIVE_V1 at import: %s", BARI_SHELF_RELATIVE_V1)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source missing: %s", BSIP1_DIR)
        return

    all_products_raw = load_yogurt_bsip1(BSIP1_DIR)
    n_loaded_raw = len(all_products_raw)

    # --- Apply discard: remove genuinely out-of-scope products from the corpus ---
    all_products = [d for d in all_products_raw if str(d.get("barcode", "")) not in DISCARD_BARCODES]
    n_discarded = n_loaded_raw - len(all_products)
    log.info("Loaded %d BSIP1 yogurt records, discarded %d out-of-scope -> %d in corpus",
              n_loaded_raw, n_discarded, len(all_products))

    # --- Router classification pre-pass (post-fix) ---
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
            "flagged_not_fixed_reason": FLAGGED_NOT_FIXED.get(bc),
        }
        router_rows.append(row)
        if cat != "dairy_protein":
            non_dairy_protein.append(row)

    subpool_counts = Counter(r["subpool"] for r in router_rows)
    log.info("Router category==dairy_protein: %d/%d", len(all_products) - len(non_dairy_protein), len(all_products))
    log.info("Subpool distribution (post-load, post-correction): %s", dict(subpool_counts))
    if non_dairy_protein:
        log.warning("NON-dairy_protein router classifications (expected: exactly the 3 "
                     "flagged-not-fixed): %d -- %s", len(non_dairy_protein), non_dairy_protein)

    subtype_dist = Counter(r["router_subtype"] for r in router_rows)
    not_cultured_subtype = [r for r in router_rows if not r["in_cultured_yogurt_subtypes"]]
    log.info("Router subtype distribution: %s", dict(subtype_dist))
    if not_cultured_subtype:
        log.warning("Products with subtype NOT in CULTURED_YOGURT_SUBTYPES (expected: "
                     "exactly the 3 flagged-not-fixed): %d -- %s",
                    len(not_cultured_subtype),
                    [(r["barcode"], r["router_subtype"], r["name"]) for r in not_cultured_subtype])

    # --- Assert the fix worked as designed: non-dairy_protein / not-cultured sets
    # must be EXACTLY the 3 flagged-not-fixed barcodes, no more, no less. ---
    expected_unfixed = set(FLAGGED_NOT_FIXED.keys())
    actual_non_dairy_protein_bcs = {r["barcode"] for r in non_dairy_protein}
    actual_not_cultured_bcs = {r["barcode"] for r in not_cultured_subtype}
    router_fix_assertion = {
        "expected_unfixed_barcodes": sorted(expected_unfixed),
        "actual_non_dairy_protein_barcodes": sorted(actual_non_dairy_protein_bcs),
        "actual_not_cultured_subtype_barcodes": sorted(actual_not_cultured_bcs),
        "non_dairy_protein_matches_expected": actual_non_dairy_protein_bcs == expected_unfixed,
        "not_cultured_subtype_matches_expected": actual_not_cultured_bcs == expected_unfixed,
    }
    log.info("Router-fix assertion: %s", router_fix_assertion)

    # --- Split into pools by BSIP1 subpool field (physical form; corrected) ---
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

    # --- Fermentation spot-check on the (now 24) drinkable names ---
    ferm_check = []
    ferm_misfires = []
    for doc in drinkable:
        bc = str(doc.get("barcode", ""))
        name = doc.get("canonical_name_he") or ""
        cat_result = classify_category(doc)
        subtype = cat_result.get("category_subtype")
        router_cat = cat_result.get("category")
        has_solid = name_has(DAIRY_SOLID_IDENTITY_MARKERS_HE, name)
        is_fluid = name_has(FLUID_MILK_NAME_MARKERS_HE, name) and not has_solid
        is_yogurt_subtype = (router_cat == "yogurt") or (subtype in CULTURED_YOGURT_SUBTYPES)
        engine_would_credit = is_yogurt_subtype and router_cat == "dairy_protein"
        actual = pool_score_results.get("drinkable", {}).get(bc, {})
        actually_fired = bool(actual.get("fermentation_bonus_note")) and (
            "R7 v1.1 Path B" in (actual.get("fermentation_bonus_note") or ""))
        row = {
            "barcode": bc, "name": name, "router_category": router_cat,
            "router_subtype": subtype, "has_solid_identity_marker": has_solid,
            "would_be_excluded_as_fluid_milk_if_no_subtype_path": is_fluid,
            "qualifies_via_yogurt_subtype_path": is_yogurt_subtype,
            "engine_expected_to_credit": engine_would_credit,
            "engine_actually_fired": actually_fired,
            "fermentation_note": actual.get("fermentation_bonus_note"),
        }
        ferm_check.append(row)
        if router_cat != "dairy_protein" or (engine_would_credit and not actually_fired):
            ferm_misfires.append(row)

    log.info("Fermentation spot-check: %d/%d drinkable products checked, %d misfires",
              len(ferm_check), len(drinkable), len(ferm_misfires))
    if ferm_misfires:
        log.warning("MISFIRES: %s", ferm_misfires)

    nova_confirmation = {
        "claim": "NOVA stays descriptive; not a new scoring input for this run",
        "evidence": [
            "nova_proxy.infer_nova(product, l3) never reads product.get('nova_proxy') -- "
            "unchanged from v1; this run adds zero new NOVA logic.",
        ],
    }

    eng_sha = sha256_file(SRC / "score_engine.py")
    const_sha = sha256_file(SRC / "constants.py")
    router_sha = sha256_file(SRC / "router_v2.py")
    no_bleed_confirmation = {
        "claim": "No other category's published scores moved",
        "basis": [
            "This run performs ZERO writes to score_engine.py / constants.py (read-only "
            "imports, byte-identical to v1 -- see sha256 below matches v1 run_record).",
            "router_v2.py WAS edited (additive-only: 18 new BARCODE_ROUTING_OVERRIDES "
            "entries, barcode-exact-match, Stage 5 / last-resort). Proof of zero "
            "cross-category impact: classify_category() was captured before/after the "
            "edit over 213 products across 4 other LIVE categories (milk_and_alternatives "
            "n=8, hard_cheeses n=66, snack_bars n=106, juices n=33) -- 0 diffs, 0 barcode "
            "collisions with the 18 new keys. See "
            "run_yogurt_task515_v2_tripwire_proof.json.",
            "score_product() is invoked ONLY for the (now 120) yogurt BSIP1 records loaded "
            "from 02_products/yogurt_system/bsip1_task515 in this process.",
            "set_shelf_stats()/clear_shelf_stats() mutate an in-process global discarded "
            "when this one-shot script exits.",
        ],
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "router_v2_sha256_v2": router_sha,
        "note": "score_engine_sha256/constants_sha256 should be IDENTICAL to the v1 "
                "run_record (proves 0-diff on those two files); router_v2_sha256_v2 WILL "
                "differ from v1's router_v2_sha256 (the additive BARCODE_ROUTING_OVERRIDES "
                "edit) -- that is the intended, tripwire-proven change.",
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

    ev105_proposal = {
        "id": "EV-105v2",
        "status": "PROPOSAL -- NOT LIVE -- not written to constants.py",
        "supersedes": "EV-105 (v1, run_yogurt_task515_bsip2) -- stale, computed on the "
                       "pre-router-fix 99/23 pool split; this run's 96/24 split (post "
                       "discard + subpool correction + router fix) is the current proposal.",
        "requires": "Nutrition Agent D6 co-sign + Product Agent D7 co-sign before any "
                    "constants.py edit or go-live",
        "topic": "Yogurt sugar shelf-relative -- TWO-POOL split (spoonable vs drinkable), "
                 "recomputed from the 120-product TASK-515 v2 corpus (122 loaded - 2 "
                 "discarded soy products).",
        "floor_and_bands_inherited_unchanged_from_EV-088": {
            "SUGAR_SHELF_REL_YOGURT_FLOOR": SUGAR_SHELF_REL_YOGURT_FLOOR,
            "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
            "SUGAR_SHELF_REL_YOGURT_P_MAX": SUGAR_SHELF_REL_YOGURT_P_MAX,
            "SUGAR_SHELF_REL_YOGURT_B_MAX": SUGAR_SHELF_REL_YOGURT_B_MAX,
        },
        "spoonable": ev105_pool_constants("spoonable"),
        "drinkable": ev105_pool_constants("drinkable"),
    }

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-515 / TASK-515A router-classification-gap fix + re-score (v2)",
        "generated": ts,
        "run_type": "SCORED -- NOT PUBLISHED (measured category build; go-live gated by "
                     "orchestrator per the 7-stage pipeline protocol)",
        "engine": "proto_v0 score_engine.py -- UNMODIFIED (uniform-baseline doctrine)",
        "router_change": "router_v2.py BARCODE_ROUTING_OVERRIDES +18 entries (additive-only, "
                          "barcode-exact-match, Stage 5). See router_v2_sha256_v2.",
        "flag_config": {
            "BARI_RECAL_P0": "on", "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK144_FIXES": "off", "BARI_TASK250_CONF": "on",
            "BARI_SHELF_RELATIVE_V1": "on (engine default, unset by this script)",
        },
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "n_loaded_raw": n_loaded_raw,
            "discarded": {"count": n_discarded, "barcodes": DISCARD_BARCODES},
            "n_in_corpus": len(all_products),
            "subpool_distribution": dict(subpool_counts),
            "other_subpool_count": len(other_subpool),
            "subpool_correction_applied": {
                "7290110552244": "spoonable -> drinkable (name is a drink; see BSIP1 JSON "
                                  "field subpool_correction_task515)",
            },
        },
        "router_check": {
            "n_dairy_protein": len(all_products) - len(non_dairy_protein),
            "n_non_dairy_protein": len(non_dairy_protein),
            "non_dairy_protein_rows": non_dairy_protein,
            "subtype_distribution": dict(subtype_dist),
            "n_not_in_cultured_yogurt_subtypes": len(not_cultured_subtype),
            "not_in_cultured_yogurt_subtypes_rows": not_cultured_subtype,
            "flagged_not_fixed": FLAGGED_NOT_FIXED,
            "router_fix_assertion": router_fix_assertion,
        },
        "pool_shelf_stats": pool_stats,
        "pool_distributions": pool_distributions,
        "pool_errors": {k: v for k, v in pool_errors.items()},
        "fermentation_spot_check": {
            "n_checked": len(ferm_check),
            "n_misfires": len(ferm_misfires),
            "misfires": ferm_misfires,
            "rows": ferm_check,
        },
        "nova_scoring_path_confirmation": nova_confirmation,
        "no_bleed_confirmation": no_bleed_confirmation,
        "ev105_proposal": ev105_proposal,
        "output_dir": str(OUTPUT_DIR),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rr_path = OUTPUT_DIR / "run_record.json"
    rr_bytes = json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8")
    rr_path.write_bytes(rr_bytes)
    rr_sha = sha256_bytes(rr_bytes)
    log.info("Run record written: %s (sha256=%s)", rr_path, rr_sha)

    print("\n" + "=" * 80)
    print(f"TASK-515/515A STAGE 2 v2 -- {RUN_ID}")
    print("=" * 80)
    print(f"Corpus: loaded={n_loaded_raw} discarded={n_discarded} in_corpus={len(all_products)}")
    print(f"Router: dairy_protein {len(all_products) - len(non_dairy_protein)}/{len(all_products)}")
    print(f"Router-fix assertion: {router_fix_assertion}")
    print(f"Pools: spoonable={len(spoonable)} drinkable={len(drinkable)} other={len(other_subpool)}")
    print(f"Spoonable guard_pass={pool_stats['spoonable']['guard_pass_overall']} "
          f"median={pool_stats['spoonable']['median']} scale={pool_stats['spoonable']['scale']} "
          f"n={pool_stats['spoonable']['n_with_sugars_g']}")
    print(f"Drinkable guard_pass={pool_stats['drinkable']['guard_pass_overall']} "
          f"median={pool_stats['drinkable']['median']} scale={pool_stats['drinkable']['scale']} "
          f"n={pool_stats['drinkable']['n_with_sugars_g']}")
    print(f"Distributions: {json.dumps(pool_distributions, ensure_ascii=False)}")
    print(f"Fermentation misfires: {len(ferm_misfires)}")
    print(f"Run record: {rr_path}")
    print(f"Run record sha256: {rr_sha}")
    print("=" * 80)

    return run_record, rr_sha


if __name__ == "__main__":
    main()
