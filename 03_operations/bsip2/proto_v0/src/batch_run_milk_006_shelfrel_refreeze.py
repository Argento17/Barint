"""
BSIP2 Prototype v0 — Milk & Alternatives Shelf-Rel Re-freeze Runner (run_006_shelfrel_refreeze)
TASK-284E / TASK-275 FIX-1.

Re-freezes the milk corpus under the new engine defaults:
  BARI_SHELF_RELATIVE_V1 = on (default ON since commit 97a9213b)
  BARI_FAT_TECH_V1       = on (default ON since commit 97a9213b)

Milk is NOT enrolled in the shelf-relative differentiator (no set_shelf_stats call).
The two flags are score-neutral for single-ingredient dairy products.
Expected outcome = reproduce A:3/B:1/C:5/D:10/E:1, max=85/A (frozen invariant).

Root-cause note (FIX-1 diagnosis):
  The commit 4cf58ac0 claimed to have re-frozen milk in run_006_shelfrel_refreeze,
  but the 20 traces were generated with null/empty product dicts — bsip1_source_path=null
  and all nutrition null — producing context_limited/no_nutrition_data/score=50 across all 20.
  The runner that created run_006 did NOT call load_batch() from input_loader.py.
  This script is the correct fix: it loads from BSIP1 source properly and overwrites run_006.

SHIPS: bsip2_trace.json per product + run_record.json in run_006_shelfrel_refreeze.
       Does NOT touch frontend JSON.
       Does NOT modify run_005_headpin.
"""
import os
import sys
import json
import pathlib
import logging
import datetime

# Force flags to the new defaults (already defaults in engine, but explicit for reproducibility)
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "off"  # milk headpin never used RECAL_P0
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "off"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
HEADPIN_ROOT = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_006_shelfrel_refreeze")
RUN_ID       = "run_006_shelfrel_refreeze"

# Frozen invariant: A:3/B:1/C:5/D:10/E:1, max=85/A (CNO ruling 2026-05-30, re-affirmed TASK-284E)
INVARIANT_TOP = {
    "bsip1_7290000051352": ("whole 3.4% (taste of old days)", 85, "A"),
    "bsip1_7290019790259": ("natural 4%",                     85, "A"),
    "bsip1_7290102392094": ("goat milk",                      85, "A"),
}
INVARIANT_DIST = {"A": 3, "B": 1, "C": 5, "D": 10, "E": 1}


def run_pipeline(product: dict) -> dict:
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def load_headpin_baseline():
    """Load run_005_headpin scores for delta comparison."""
    pub = {}
    for d in (HEADPIN_ROOT / "products").iterdir():
        tf = d / "bsip2_trace.json"
        if tf.exists():
            t = json.loads(tf.read_text(encoding="utf-8"))
            pid = (t.get("input_reference") or {}).get("canonical_product_id") or d.name
            pub[pid] = t
    return pub


def main():
    log.info("=== %s: Milk re-freeze under BARI_SHELF_RELATIVE_V1=on + BARI_FAT_TECH_V1=on ===", RUN_ID)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source missing: %s", BSIP1_SOURCE)
        sys.exit(1)

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    # Load BSIP1 products using the proper loader (root cause fix: this was missing in the prior run)
    products = load_batch(BSIP1_SOURCE)
    log.info("BSIP1 products loaded: %d", len(products))

    if len(products) == 0:
        log.error("No products loaded from %s — aborting", BSIP1_SOURCE)
        sys.exit(1)

    # Load headpin baseline for delta comparison
    pub = load_headpin_baseline()
    log.info("Headpin baseline traces loaded: %d", len(pub))

    # Score all products
    head = {}
    errors = []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        # Only score products that are in the headpin set (20 published products)
        if pid not in pub:
            log.info("  Skipping %s (not in headpin set)", pid)
            continue
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            head[pid] = trace
            log.info("  %s: %s/%s [%s]",
                     pid,
                     trace.get("final_score_estimate"),
                     trace.get("grade_estimate"),
                     trace.get("evaluation_status"))
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            errors.append({"product_id": pid, "error": str(e)})
            head[pid] = {"_error": str(e)}

    # Grade distribution
    from collections import Counter
    gdist = Counter(v.get("grade_estimate", "?") for v in head.values() if "_error" not in v)
    scores = [v.get("final_score_estimate") for v in head.values()
              if "_error" not in v and v.get("final_score_estimate") is not None]

    log.info("Grade distribution: %s", dict(sorted(gdist.items())))
    log.info("Score range: min=%.1f max=%.1f (n=%d)",
             min(scores) if scores else 0, max(scores) if scores else 0, len(scores))

    # Invariant check — top trio must hold
    inv = []
    inv_held = True
    for pid, (label, exp_s, exp_g) in INVARIANT_TOP.items():
        ht = head.get(pid, {})
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        held = (hs == exp_s and hg == exp_g)
        inv_held = inv_held and held
        inv.append({
            "product_id": pid, "label": label,
            "expected": f"{exp_s}/{exp_g}", "got": f"{hs}/{hg}",
            "status": "HELD" if held else "BROKEN"
        })
        if not held:
            log.error("  INVARIANT BROKEN: %s expected %s/%s got %s/%s", pid, exp_s, exp_g, hs, hg)
        else:
            log.info("  INVARIANT HELD: %s = %s/%s", pid, hs, hg)

    # Distribution invariant check
    dist_held = dict(gdist) == INVARIANT_DIST
    if not dist_held:
        log.error("DISTRIBUTION MISMATCH: expected %s got %s", INVARIANT_DIST, dict(gdist))
    else:
        log.info("DISTRIBUTION HELD: %s", dict(gdist))

    max_score = max(scores) if scores else None
    max_held = (max_score == 85.0)
    if not max_held:
        log.error("MAX SCORE MISMATCH: expected 85 got %s", max_score)
    else:
        log.info("MAX SCORE HELD: 85")

    all_invariants_held = inv_held and dist_held and max_held

    if not all_invariants_held:
        log.error("=== FROZEN INVARIANT BROKEN — STOP. Do NOT update shadow registry. ===")
        log.error("Top trio held: %s | Dist held: %s | Max held: %s", inv_held, dist_held, max_held)
        sys.exit(2)

    # Build delta table vs run_005_headpin
    delta_rows = []
    for pid, ht in sorted(head.items()):
        if "_error" in ht:
            continue
        pt = pub.get(pid, {})
        ps = pt.get("final_score_estimate")
        pg = pt.get("grade_estimate")
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        name = (pt.get("input_reference") or {}).get("product_name_he", "")
        delta = round(hs - ps, 2) if (ps is not None and hs is not None) else None
        klass = "MATCH" if delta == 0 else ("GRADE_FLIP" if pg != hg else ("DRIFT>=2" if abs(delta or 0) >= 2 else "cosmetic"))
        delta_rows.append({
            "product_id": pid, "name_he": name,
            "run_005_score": ps, "run_005_grade": pg,
            "run_006_score": hs, "run_006_grade": hg,
            "delta": delta, "class": klass
        })

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-284E / TASK-275-FIX1",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "off",
        },
        "bsip1_source": str(BSIP1_SOURCE),
        "compared_against": "run_005_headpin",
        "headpin_count": len(pub),
        "scored_count": len([v for v in head.values() if "_error" not in v]),
        "error_count": len(errors),
        "grade_dist": dict(sorted(gdist.items())),
        "score_min": round(min(scores), 2) if scores else None,
        "score_max": round(max(scores), 2) if scores else None,
        "frozen_invariant": {
            "top_trio_held": inv_held,
            "distribution_held": dist_held,
            "max_held": max_held,
            "all_held": all_invariants_held,
            "expected_dist": INVARIANT_DIST,
            "actual_dist": dict(gdist),
            "trio": inv,
        },
        "delta_table": delta_rows,
        "note": ("FIX-1 (TASK-275): prior run_006 traces were null-nutrition stubs (bsip1_source_path=null). "
                 "Root cause: runner did not call load_batch() from input_loader.py. "
                 "This run correctly loads BSIP1 and reproduces the frozen invariant."),
    }

    rec_path = OUTPUT_ROOT / "run_record.json"
    rec_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rec_path)
    log.info("=== run_006_shelfrel_refreeze COMPLETE. Invariants: ALL HELD ===")
    return run_record


if __name__ == "__main__":
    main()
