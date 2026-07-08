"""
TASK-515/515A -- Re-score ONLY the 16 tapioca-modified-starch-affected products
through the now-fixed ingredient_taxonomy.py classifier (P510 fix, already committed).

Reuses the exact same pipeline and shelf stats as run_bsip2_task515_v3_remediation.py.
Only overwrites trace files for the 16 target barcodes; every other trace file on
disk is left untouched.

Per the co-sign record TAPIOCA_STARCH_FIX_COSIGN.md: both Nutrition + Product gates
are already GRANTED; this script implements, not decides.
"""
import os, sys, json, pathlib, logging

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
)
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    SUGAR_SHELF_SCALE_MIN, SUGAR_SHELF_SCALE_GUARD,
    SUGAR_SHELF_REL_YOGURT_FLOOR, SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
    SUGAR_SHELF_REL_YOGURT_P_MAX, SUGAR_SHELF_REL_YOGURT_B_MAX,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "02_products" / "yogurt_system" / "bsip1_task515"
V3_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_task515_v3"

TARGET_BARCODES = {
    # drinkable (3 of 20)
    "7290110573737": "drinkable",
    "7290110552244": "drinkable",
    "7290107938396": "drinkable",
    # spoonable (13 of 78)
    "408354":           "spoonable",
    "6664693":          "spoonable",
    "7290010471669":    "spoonable",
    "7290110578053":    "spoonable",
    "7290110578572":    "spoonable",
    "7290119370177":    "spoonable",
    "7290119370955":    "spoonable",
    "7290119372997":    "spoonable",
    "7290119377404":    "spoonable",
    "7290119377411":    "spoonable",
    "7290119380916":    "spoonable",
    "7290119384242":    "spoonable",
    "7290119386642":    "spoonable",
}

ALL_EXCLUDE_BARCODES = {
    "7290110329792": "soy", "7290110329815": "soy",
    "4068028": "display", "7290119377480": "display", "7290119385768": "display",
    "7290116936581": "dump", "43944": "dump", "45771": "dump", "5416415": "dump",
    "7290110321031": "dump", "7290110328788": "dump", "7290110329952": "dump",
    "7290116932484": "dump", "7290116934402": "dump", "7290116935614": "dump",
    "7290116935621": "dump", "7290116936123": "dump", "7290116936215": "dump",
    "7290116936222": "dump", "7290116934228": "dump", "7290116932774": "dump",
    "57149": "dedup", "7290014758117": "dedup", "6664655": "dedup",
}

MIN_N_GUARD = 20


def load_yogurt_bsip1(source_dir):
    paths = sorted(source_dir.glob("bsip1_yogurt_*.json"))
    products = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        data["_source_path"] = str(p)
        data["_load_errors"] = []
        products.append(data)
    return products


def get_sugars_g(doc):
    nn = doc.get("normalized_nutrition_per_100g") or {}
    return nn.get("sugars_g")


def run_pipeline(product):
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
    log.info("=== Tapioca starch fix rescore -- 16 target products only ===")

    all_products_raw = load_yogurt_bsip1(BSIP1_DIR)
    all_products = [d for d in all_products_raw
                    if str(d.get("barcode", "")) not in ALL_EXCLUDE_BARCODES]
    log.info("Loaded %d BSIP1 records, %d after exclusions (matching v3 remediation corpus)",
             len(all_products_raw), len(all_products))

    # Build lookups
    by_bc = {}
    for doc in all_products:
        by_bc[str(doc.get("barcode", ""))] = doc

    # Separate pools for shelf stats
    spoonable = [d for d in all_products if d.get("subpool") == "spoonable"]
    drinkable = [d for d in all_products if d.get("subpool") == "drinkable"]
    log.info("Pools: spoonable=%d drinkable=%d", len(spoonable), len(drinkable))

    # Compute shelf stats per pool (same as remediation script)
    for pool_name, pool_products in [("spoonable", spoonable), ("drinkable", drinkable)]:
        sugars_n = sum(1 for d in pool_products if get_sugars_g(d) is not None)
        median, scale = compute_shelf_stats(
            pool_products, "sugars_g", scale_type="iqr",
            nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
        )
        guard_n_pass = sugars_n >= MIN_N_GUARD
        guard_scale_pass = (scale is not None) and (scale >= SUGAR_SHELF_SCALE_GUARD)
        guard_pass = bool(median is not None and scale is not None and guard_n_pass and guard_scale_pass)
        log.info("[%s] sugars_g stats: n=%d median=%s scale=%s guard_n=%s guard_scale=%s -> %s",
                 pool_name, sugars_n, median, scale, guard_n_pass, guard_scale_pass,
                 "ACTIVE" if guard_pass else "SUPPRESSED")

        clear_shelf_stats()
        if guard_pass:
            set_shelf_stats(nutrient="sugars_g", median=median, scale=scale, scale_type="iqr", n=sugars_n)

        # Score only the target products in this pool
        target_in_pool = [bc for bc, p in TARGET_BARCODES.items() if p == pool_name]
        for bc in sorted(target_in_pool):
            doc = by_bc.get(bc)
            if doc is None:
                log.warning("  TARGET %s NOT FOUND in corpus -- skipping", bc)
                continue
            log.info("  Scoring %s (%s) ...", bc, doc.get("canonical_name_he", "?"))
            trace, score_result, cat_result = run_pipeline(doc)
            write_trace(trace, V3_DIR / pool_name)

            fs = trace.get("final_score_estimate")
            gr = trace.get("grade_estimate")
            tax = trace.get("taxonomical_additives", {})
            ms = tax.get("modified_starch", {})
            d4 = trace.get("d4_additives", {})
            d4ms = d4.get("modified_starch_stabilizer", {})
            log.info("    -> score=%s grade=%s tax_modified_starch=%s d4_penalty=%s delta=%s",
                     fs, gr, ms.get("detected"), d4ms.get("applied"), d4ms.get("delta"))

        clear_shelf_stats()

    log.info("=== DONE ===")


if __name__ == "__main__":
    main()
