"""
BSIP2 — Juices & Fruit Drinks batch runner (run_juices_001, TASK-214).
Engine: BARI_RECAL_P0=on + BARI_GLASSBOX_W4=on (shipped 2026-06-05).
Category: beverage (router hard-anchor for juice/nectar/drink names).
CRITICAL: nutrition panels are per_100ml — the unit override is documented in
bsip1 records as nutrition_unit='per_100ml'; scoring engine uses these values
verbatim (beverage calorie table is already calibrated for per-100ml values).
Output: 02_products/juices/bsip2_outputs/run_juices_001/
"""
import sys, json, pathlib, logging, datetime, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_juices_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_juices_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\juices\reports")
RUN_ID       = "run_juices_001"
BEVERAGE_CATS = {"beverage", "default"}


def run_pipeline(product):
    signals = extract_signals(product)
    cat = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(product, l3)
    scope = assign_evaluation_scope(product, cat["category"])
    score = score_product(product, signals, cat, nova, scope)
    trace = assemble_trace(product, signals, cat, nova, scope, score)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_batch():
    flag = os.environ.get("BARI_RECAL_P0", "off")
    log.info("=== BSIP2 Juices batch — %s (BARI_RECAL_P0=%s) ===", RUN_ID, flag)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    pdir = OUTPUT_ROOT / "products"
    if pdir.exists():
        import shutil; shutil.rmtree(pdir)
    pdir.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces, errors, misroutes = [], [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            cat = trace.get("category")
            if cat not in BEVERAGE_CATS:
                ref = trace.get("input_reference") or {}
                misroutes.append({
                    "pid": pid,
                    "name": ref.get("product_name_he") or "",
                    "routed_to": cat,
                })
        except Exception as e:
            log.error("PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate"); dist[g] = dist.get(g, 0) + 1
    scores_list = sorted(t.get("final_score_estimate") for t in sufficient)

    log.info("Scored: %d | Errors: %d | Misroutes: %d", len(sufficient), len(errors), len(misroutes))
    log.info("Grade distribution: %s", dist)
    if scores_list:
        log.info("Score range: %.1f – %.1f", scores_list[0], scores_list[-1])

    if misroutes:
        log.warning("Misrouted products:")
        for m in misroutes:
            log.warning("  %s → %s (%s)", m["pid"], m["routed_to"], m["name"][:50])

    # Run summary
    nova_dist = {}
    for t in traces:
        n = t.get("nova_proxy"); nova_dist[n] = nova_dist.get(n, 0) + 1

    summary = {
        "run_id": RUN_ID,
        "run_date": datetime.datetime.now().isoformat(),
        "category": "juices",
        "bsip1_source": str(BSIP1_SOURCE),
        "output_root": str(OUTPUT_ROOT),
        "products_loaded": len(products),
        "products_scored": len(sufficient),
        "errors": errors,
        "misroutes": misroutes,
        "grade_distribution": dist,
        "nova_distribution": nova_dist,
        "score_range": {"min": scores_list[0] if scores_list else None,
                        "max": scores_list[-1] if scores_list else None},
        "engine_flags": {
            "BARI_RECAL_P0": flag,
            "BARI_GLASSBOX_W4": os.environ.get("BARI_GLASSBOX_W4", "on"),
        }
    }
    summary_path = REPORT_ROOT / f"{RUN_ID}_batch_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log.info("Summary written: %s", summary_path)

    return traces, errors, misroutes


if __name__ == "__main__":
    os.environ["BARI_RECAL_P0"] = "on"
    run_batch()
