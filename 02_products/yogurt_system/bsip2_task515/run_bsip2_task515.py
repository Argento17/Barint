"""
TASK-515 / TASK-515A -- Stage 2 (BSIP2 scoring) for the yogurt build.

Implements Nutrition's methodology ruling on the 122 BSIP1 records
(99 spoonable / 23 drinkable), through the SAME BSIP2 engine used for
milk/cheese (uniform-baseline doctrine -- zero engine-source changes).

Ruling implemented:
  1. TWO separate shelf-relative pools for sugars_g -- spoonable (99) scored
     against a spoonable-only reference set, drinkable (23) against a
     drinkable-only reference set. Never pooled together.
  2. Fresh median/IQR/scale computed FROM THIS 122-corpus, per pool, via the
     engine's own compute_shelf_stats() (IQR-primary, MAD, floor=SUGAR_SHELF_SCALE_MIN).
     The existing SUGAR_SHELF_REL_YOGURT_* / EV-088 constants (median=5.45,
     n=74, run_yogurt_006) are NOT reused -- they are stale (pre-subpool corpus).
  3. Drinkable pool (n=23) is run through the engine's own low-variance /
     min-n guard (shelf_relative_differentiator: n>=20 AND scale>=SUGAR_SHELF_SCALE_GUARD).
     If it fails, shelf stats are left UNSET for that pool so the engine itself
     suppresses the term (no forced number) -- this script does not override
     that behavior.
  4. Same dimension set for both pools -- this script calls the identical
     score_product() used for milk/cheese/every other category. No new
     scoring code is added. The ONLY thing this script varies between the
     two passes is the global shelf-relative reference stats for "sugars_g"
     (via score_engine.set_shelf_stats / clear_shelf_stats), read by the
     PRE-EXISTING EV-088 call site in score_engine.py (score_product() body,
     gated on category=="dairy_protein" and cat_subtype in CULTURED_YOGURT_SUBTYPES).
     fat quality/sat-fat, sodium, additives/emulsifiers, protein and
     fermentation dimensions are NOT touched -- they run through their
     existing, uniform, non-shelf-relative logic identically for both pools
     (verified by code read: FATSAT_SHELF_REL_SCOPE is empty/inert and no
     yogurt-subtype-gated sat-fat SR branch exists -- only cream_cheese/
     hard_cheese have one; see EV-089/EV-090).
  5. Fermentation spot-check performed on the 23 drinkable names against the
     DAIRY_SOLID_IDENTITY_MARKERS_HE / FLUID_MILK_NAME_MARKERS_HE logic used
     by the engine's Path-B cultured-bonus code (score_engine.py ~3814-3861).
  6. NOVA is read from the engine's OWN infer_nova() (independent of BSIP1's
     descriptive nova_proxy field, which infer_nova() never reads) -- same
     path used for every other category; confirmed NOT a new scoring input.

Tree safety: this script and ALL of its outputs live under
02_products/yogurt_system/ only. It imports (read-only) from
03_operations/bsip2/proto_v0/src -- no file there is modified.
No git operations. No commit.

MEASURED / SCORED, NOT PUBLISHED: constants proposed here are EV-105 and are
NOT live in constants.py -- this run uses set_shelf_stats() at runtime only.
Requires Nutrition-D6 + Product-D7 co-sign before any constants.py edit or
go-live.
"""
import os, sys, json, pathlib, hashlib, datetime, statistics, logging
from collections import Counter, defaultdict

# --- Flag config: BYTE-IDENTICAL to the current live yogurt ship-config
# (batch_run_yogurt_006_shipcfg2.py) -- must be set BEFORE any engine imports.
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "on"
# BARI_SHELF_RELATIVE_V1 intentionally NOT set here -- inherits the engine
# default ("on"), exactly as run_yogurt_006_shipcfg2 does. This is required
# for both the EV-088 absolute floor (unchanged, always active for any
# yogurt-subtype product with sugars_g>=12g) and the shelf-relative call
# site this script feeds via set_shelf_stats().

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
OUTPUT_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515"
RUN_ID = "run_yogurt_task515_bsip2"
MIN_N_GUARD = 20  # matches shelf_relative_differentiator default min_n


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yogurt_bsip1(source_dir: pathlib.Path) -> list[dict]:
    """Explicit glob -- deliberately narrower than input_loader.load_batch's
    'bsip1_*.json', which would also match bsip1_run_report_task515.json in
    this directory (a report file, not a product) and corrupt the corpus."""
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
    """Same call sequence as every live batch_run_*.py -- zero deviation."""
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
    log.info("=== BSIP2 Stage 2 -- %s (TASK-515/515A) ===", RUN_ID)
    log.info("BARI_SHELF_RELATIVE_V1 at import: %s", BARI_SHELF_RELATIVE_V1)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source missing: %s", BSIP1_DIR)
        return

    all_products = load_yogurt_bsip1(BSIP1_DIR)
    log.info("Loaded %d BSIP1 yogurt records", len(all_products))

    # --- Router classification pre-pass: confirm category==dairy_protein for
    # all 122, and confirm subpool split (BSIP1 field, physical form) is
    # still 99/23 after load. Also captures category_subtype per product for
    # the CULTURED_YOGURT_SUBTYPES gate and the fermentation spot-check.
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
    log.info("Subpool distribution (post-load): %s", dict(subpool_counts))
    if non_dairy_protein:
        log.warning("NON-dairy_protein router classifications found: %d -- %s",
                    len(non_dairy_protein), non_dairy_protein)

    subtype_dist = Counter(r["router_subtype"] for r in router_rows)
    not_cultured_subtype = [r for r in router_rows if not r["in_cultured_yogurt_subtypes"]]
    log.info("Router subtype distribution: %s", dict(subtype_dist))
    if not_cultured_subtype:
        log.warning("Products with subtype NOT in CULTURED_YOGURT_SUBTYPES: %d -- %s",
                    len(not_cultured_subtype), [(r["barcode"], r["router_subtype"], r["name"]) for r in not_cultured_subtype])

    # --- Split into pools by BSIP1 subpool field (physical form) ---
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
        # Reproduce the n>=min_n AND scale>=guard check performed inside
        # shelf_relative_differentiator, so the run_record documents the
        # guard result explicitly (not just implicitly via 0-penalties).
        guard_n_pass = sugars_n >= MIN_N_GUARD
        guard_scale_pass = (scale is not None) and (scale >= SUGAR_SHELF_SCALE_GUARD)
        guard_pass = bool(median is not None and scale is not None and guard_n_pass and guard_scale_pass)

        pool_stats[pool_name] = {
            "n_total_products": len(pool_products),
            "n_with_sugars_g": sugars_n,
            "median": median,
            "scale": scale,          # max(IQR/1.349, 1.4826*MAD, SUGAR_SHELF_SCALE_MIN)
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
        # else: leave unset -- shelf_relative_differentiator will itself
        # return "shelf stats not set" / suppressed for every product in
        # this pool; the pre-existing absolute floor (EV-088, unchanged
        # constants) still fires independently since it does not read
        # _SHELF_STATS at all.

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

    # --- Distributions per pool ---
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

    # --- Fermentation spot-check on the 23 drinkable names ---
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
        # Engine's actual Path-B.1 logic: a confirmed yogurt subtype qualifies
        # OUTRIGHT and is NOT gated by the fluid-milk name check (that check
        # only applies to the Path-B.2 cultured-cheese-by-name branch).
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

    # --- NOVA-not-in-scoring-path confirmation (code-level, documented not re-derived) ---
    nova_confirmation = {
        "claim": "NOVA stays descriptive; not a new scoring input for this run",
        "evidence": [
            "nova_proxy.infer_nova(product, l3) never reads product.get('nova_proxy') "
            "(grep of nova_proxy.py: zero references) -- the engine independently "
            "re-derives its own NOVA proxy from ingredient/signal data, identical to "
            "every other live category (milk, cheese, etc.); BSIP1 Stage-1's "
            "'nova_proxy' field is informational only and is not consumed here.",
            "nova_level (engine-derived) already gates guardrail caps and the "
            "fermentation-credit eligibility check (nova_level<=3) inside score_engine.py "
            "for ALL categories uniformly -- this is pre-existing engine architecture, "
            "not something introduced or modified by this run.",
            "This script adds zero new NOVA-based logic and does not modify score_engine.py.",
        ],
    }

    # --- No-bleed / no-other-category-moved confirmation ---
    eng_sha = sha256_file(SRC / "score_engine.py")
    const_sha = sha256_file(SRC / "constants.py")
    router_sha = sha256_file(SRC / "router_v2.py")
    no_bleed_confirmation = {
        "claim": "No other category's published scores moved",
        "basis": [
            "This run performs ZERO writes to any file under 03_operations/bsip2/proto_v0/src "
            "(score_engine.py, constants.py, router_v2.py are read-only imports).",
            "score_product() is invoked ONLY for the 122 yogurt BSIP1 records loaded from "
            "02_products/yogurt_system/bsip1_task515 -- no milk/cheese/other-category product "
            "is scored in this process.",
            "set_shelf_stats()/clear_shelf_stats() mutate an in-process global (_SHELF_STATS) "
            "that is discarded when this one-shot script process exits; it cannot affect any "
            "other (separate-process) category run, past or future.",
        ],
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "router_v2_sha256": router_sha,
        "note": "These sha256 values are recorded so a future diff can prove the engine "
                "source was byte-identical to whatever milk/cheese were last scored against.",
    }

    # --- EV-105 PROPOSAL (NOT live; requires Nutrition-D6 + Product-D7 co-sign) ---
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
        "id": "EV-105",
        "status": "PROPOSAL -- NOT LIVE -- not written to constants.py",
        "requires": "Nutrition Agent D6 co-sign + Product Agent D7 co-sign before any "
                    "constants.py edit or go-live",
        "topic": "Yogurt sugar shelf-relative -- TWO-POOL split (spoonable vs drinkable), "
                 "recomputed from the 122-product TASK-515 corpus. Supersedes the single-pool "
                 "EV-088 constants (median=5.45, n=74, run_yogurt_006), which are STALE for "
                 "this corpus and must not be reused.",
        "floor_and_bands_inherited_unchanged_from_EV-088": {
            "SUGAR_SHELF_REL_YOGURT_FLOOR": SUGAR_SHELF_REL_YOGURT_FLOOR,
            "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
            "SUGAR_SHELF_REL_YOGURT_P_MAX": SUGAR_SHELF_REL_YOGURT_P_MAX,
            "SUGAR_SHELF_REL_YOGURT_B_MAX": SUGAR_SHELF_REL_YOGURT_B_MAX,
            "note": "The absolute anti-immunity floor and the surcharge/relief band caps are "
                    "NOT part of the 'recompute median/IQR' instruction and are left untouched.",
        },
        "spoonable": ev105_pool_constants("spoonable"),
        "drinkable": ev105_pool_constants("drinkable"),
    }

    # --- run_record.json ---
    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-515 / TASK-515A Stage 2 (BSIP2 scoring)",
        "generated": ts,
        "run_type": "SCORED -- NOT PUBLISHED (measured category build; go-live gated by "
                     "orchestrator per the 7-stage pipeline protocol)",
        "engine": "proto_v0 score_engine.py -- UNMODIFIED (uniform-baseline doctrine, no "
                  "engine change, no bespoke loader)",
        "flag_config": {
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK144_FIXES": "off",
            "BARI_TASK250_CONF": "on",
            "BARI_SHELF_RELATIVE_V1": "on (engine default, unset by this script -- "
                                      "byte-identical to run_yogurt_006_shipcfg2)",
        },
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "n_loaded": len(all_products),
            "subpool_distribution": dict(subpool_counts),
            "other_subpool_count": len(other_subpool),
        },
        "router_check": {
            "n_dairy_protein": len(all_products) - len(non_dairy_protein),
            "n_non_dairy_protein": len(non_dairy_protein),
            "non_dairy_protein_rows": non_dairy_protein,
            "subtype_distribution": dict(subtype_dist),
            "n_not_in_cultured_yogurt_subtypes": len(not_cultured_subtype),
            "not_in_cultured_yogurt_subtypes_rows": not_cultured_subtype,
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

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_bytes = json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8")
    rr_path.write_bytes(rr_bytes)
    rr_sha = sha256_bytes(rr_bytes)
    log.info("Run record written: %s (sha256=%s)", rr_path, rr_sha)

    # Console summary
    print("\n" + "=" * 80)
    print(f"TASK-515/515A STAGE 2 -- {RUN_ID}")
    print("=" * 80)
    print(f"Router: dairy_protein {len(all_products) - len(non_dairy_protein)}/{len(all_products)}")
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
