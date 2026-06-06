"""
BSIP2 Prototype v0 — Butter Batch Runner (butter_run_001) — TASK-191.

Input:   C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_merged.json
         (39 products: 16 sufficient + 23 insufficient)

Output:  C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_001\\
         + C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_001_summary.json

Engine flags: standard baseline (no BSIP_RECAL_P0, no GLASSBOX flags).
BARI_GLASSBOX_W4 defaults ON (shipped 2026-06-05 / TASK-181S).

Scoring notes for butter:
  - All pure butter → routed to `whole_food_fat` archetype via Stage 2 signal.
  - WHOLE_FOOD_FAT_FLOOR = 70 for NOVA 1-2 products (unprocessed milk fat).
  - Sat fat Class-B cap (ISRAELI_RED_LABEL_1_SAT_FAT) will reduce most products
    from the 70 floor → physiological moderation minimum applies.
  - Items with data_sufficiency="insufficient" → score_engine returns
    final_score_estimate=None, grade_estimate="INSUFFICIENT".
  - Item 10 (גבינות ניצן מתובלת, barcode 369709) has E-202 → appears in additive trace.
"""
import sys
import json
import pathlib
import logging
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_product, validate_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_PATH   = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs\butter_bsip1_merged.json")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_001")
RUN_ID       = "butter_run_001"
CATEGORY_TAG = "butter"

WHOLE_FOOD_FAT_OK = {"whole_food_fat"}


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_batch():
    import os
    log.info("=== BSIP2 Butter — %s ===", RUN_ID)
    log.info("  BSIP1 source: %s", BSIP1_PATH)
    log.info("  BARI_RECAL_P0=%s  BARI_GLASSBOX_W4=%s",
             os.environ.get("BARI_RECAL_P0", "off"),
             os.environ.get("BARI_GLASSBOX_W4", "on (default)"))

    if not BSIP1_PATH.exists():
        log.error("BSIP1 source not found: %s", BSIP1_PATH)
        return None

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_ROOT / "products"
    if prod_dir.exists():
        import shutil
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    # Load the flat BSIP1 array
    raw_list = json.loads(BSIP1_PATH.read_text(encoding="utf-8"))
    log.info("Products loaded: %d", len(raw_list))

    traces = []
    errors = []
    misroutes = []

    for product in raw_list:
        # Attach source path for traceability
        product["_source_path"] = str(BSIP1_PATH)
        product["_load_errors"] = validate_product(product)

        pid = product.get("canonical_product_id", "unknown")
        name = product.get("canonical_name_he", "")

        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)

            cat = trace.get("category")
            if cat not in WHOLE_FOOD_FAT_OK:
                misroutes.append({
                    "pid": pid,
                    "name": name,
                    "routed_to": cat,
                    "expected": "whole_food_fat",
                })
                log.warning("  MISROUTE: %s → %s", name, cat)
            else:
                score = trace.get("final_score_estimate")
                grade = trace.get("grade_estimate")
                suff  = trace.get("data_sufficiency")
                log.info("  OK  %s | %s | %s/%s | suff=%s",
                         pid[-20:], name[:30], score, grade, suff)

        except Exception as e:
            log.error("  PIPELINE ERROR for %s (%s): %s", pid, name, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "name": name, "error": str(e)})

    # ── Summary ───────────────────────────────────────────────────────────────
    scored = [t for t in traces if t.get("final_score_estimate") is not None]
    insufficient = [t for t in traces if t.get("grade_estimate") == "INSUFFICIENT"
                    or t.get("data_sufficiency") == "insufficient"]

    dist: dict[str, int] = {}
    for t in traces:
        g = t.get("grade_estimate") or "INSUFFICIENT"
        dist[g] = dist.get(g, 0) + 1

    scores_list = sorted([t["final_score_estimate"] for t in scored
                          if t["final_score_estimate"] is not None])
    score_min  = scores_list[0] if scores_list else None
    score_max  = scores_list[-1] if scores_list else None
    score_mean = round(sum(scores_list) / len(scores_list), 1) if scores_list else None

    # Floor activations
    floor_count = 0
    for t in traces:
        for f in (t.get("floors_applied") or []):
            if "floor_type" in f:
                floor_count += 1
                break

    # Sat-fat caps fired
    sat_fat_caps = 0
    for t in traces:
        for c in (t.get("caps_applied") or []):
            if "SAT_FAT" in (c.get("rule") or ""):
                sat_fat_caps += 1
                break

    all_wff = len(misroutes) == 0

    summary = {
        "run_id": RUN_ID,
        "task": "TASK-191",
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_flags": {
            "BARI_RECAL_P0": os.environ.get("BARI_RECAL_P0", "off"),
            "BARI_GLASSBOX_W4": "on",
            "BARI_GLASSBOX_D5D6": os.environ.get("BARI_GLASSBOX_D5D6", "off"),
        },
        "bsip1_source": str(BSIP1_PATH),
        "total_products": len(raw_list),
        "pipeline_errors": len(errors),
        "grade_distribution": dist,
        "score_range": {
            "min": score_min,
            "max": score_max,
            "mean": score_mean,
        },
        "routing_check": {
            "all_whole_food_fat": all_wff,
            "misrouted": misroutes,
        },
        "floor_activations": floor_count,
        "sat_fat_caps_fired": sat_fat_caps,
        "insufficient_count": len(insufficient),
        "error_detail": errors,
    }

    summary_path = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs") / "butter_run_001_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("=== Run complete ===")
    log.info("  Total: %d  Scored: %d  Insufficient: %d  Errors: %d",
             len(raw_list), len(scored), len(insufficient), len(errors))
    log.info("  Grade distribution: %s", dist)
    log.info("  Score range: %s–%s  mean=%s", score_min, score_max, score_mean)
    log.info("  All routed to whole_food_fat: %s", all_wff)
    if misroutes:
        log.warning("  Misroutes: %s", [m["name"] for m in misroutes])
    log.info("  Floor activations: %d  Sat-fat caps: %d", floor_count, sat_fat_caps)
    log.info("  Summary: %s", summary_path)

    return summary


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
