"""
BSIP2 — Yohananof Cheese batch runner (run_cheese_yohananof_001, TASK-210 Phase B).
Scores ONLY the new Yohananof cheese products (not re-scoring Shufersal baseline).
Engine: same as run_cheese_003 (proto_v0, BARI_RECAL_P0=on).
Source: BSIP1 run_cheese_yohananof_001 (il_prices + OFF candidate panels).
Output: 02_products/cheese_spreads/bsip2_outputs/run_cheese_yohananof_001/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_yohananof_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_yohananof_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\reports")
RUN_ID       = "run_cheese_yohananof_001"


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


def run_batch():
    flag = os.environ.get("BARI_RECAL_P0", "off")
    log.info("=== BSIP2 Yohananof Cheese — %s (BARI_RECAL_P0=%s) ===", RUN_ID, flag)

    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    import shutil
    pdir = OUTPUT_ROOT / "products"
    if pdir.exists():
        shutil.rmtree(pdir)
    pdir.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))
    traces, errors = [], []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            log.info("  %-30s score=%-5s grade=%s cat=%s",
                     pid[-30:],
                     trace.get("final_score_estimate"),
                     trace.get("grade_estimate"),
                     trace.get("category"))
        except Exception as e:
            log.error("PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces if t.get("final_score_estimate") is not None]
    grades = {}
    for t in sufficient:
        g = t.get("grade_estimate"); grades[g] = grades.get(g, 0) + 1
    scores = sorted(t.get("final_score_estimate") for t in sufficient)

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "engine": f"proto_v0 / BARI_RECAL_P0={flag}",
        "source": "Yohananof il_prices + OFF candidate panels; BSIP0 filtered + curated",
        "processed": len(traces), "scored": len(sufficient), "errors": len(errors),
        "grade_distribution": grades,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", path)
    log.info("Grades=%s scored=%d errors=%d", grades, len(sufficient), len(errors))
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
