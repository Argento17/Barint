"""
BSIP2 — Salty snacks rescore batch runner (run_salty_snacks_002, TASK-216).
Engine: BARI_RECAL_P0=on (standard production engine).
Change: EV-043 industrial-extrusion NOVA 4 signal added to nova_proxy.py.
Source: same BSIP1 corpus as run_001 (54 products).
Output: 02_products/salty_snacks/bsip2_outputs/run_salty_snacks_002/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\reports")
RUN_ID       = "run_salty_snacks_002"


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
    log.info("=== BSIP2 salty snacks — %s (BARI_RECAL_P0=%s) ===", RUN_ID, flag)
    if flag.lower() != "on":
        log.warning("BARI_RECAL_P0 != on — run with BARI_RECAL_P0=on for live consistency.")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    pdir = OUTPUT_ROOT / "products"
    if pdir.exists():
        import shutil; shutil.rmtree(pdir)
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
        except Exception as e:
            log.error("PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate"); dist[g] = dist.get(g, 0) + 1

    scores = sorted(t.get("final_score_estimate") for t in sufficient)
    median = scores[len(scores)//2] if scores else None

    def name(t):
        ref = t.get("input_reference") or {}
        return ref.get("product_name_he") or ref.get("canonical_name_he") or ""

    top5 = sorted(sufficient, key=lambda t: -(t.get("final_score_estimate") or 0))[:5]
    bottom5 = sorted(sufficient, key=lambda t: (t.get("final_score_estimate") or 0))[:5]

    nova_dist = {}
    for t in traces:
        nova = t.get("nova_proxy")
        nova_dist[str(nova)] = nova_dist.get(str(nova), 0) + 1

    # Delta vs run_001
    run001_dir = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_001\products")
    run001_scores = {}
    run001_nova = {}
    if run001_dir.exists():
        for pid_dir in run001_dir.iterdir():
            tp = pid_dir / "bsip2_trace.json"
            if tp.exists():
                t001 = json.loads(tp.read_text("utf-8"))
                ref001 = t001.get("input_reference") or {}
                pid001 = ref001.get("canonical_product_id") or t001.get("canonical_product_id") or ""
                run001_scores[pid001] = t001.get("final_score_estimate")
                run001_nova[pid001] = t001.get("nova_proxy")

    delta_rows = []
    for t in sufficient:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id") or ""
        s002 = t.get("final_score_estimate")
        s001 = run001_scores.get(pid)
        n002 = t.get("nova_proxy")
        n001 = run001_nova.get(pid)
        if s001 != s002 or n001 != n002:
            delta_rows.append({
                "pid": pid,
                "name": name(t),
                "score_001": s001,
                "score_002": s002,
                "score_delta": round((s002 or 0) - (s001 or 0), 1),
                "nova_001": n001,
                "nova_002": n002,
                "grade_001": t.get("input_reference", {}).get("grade_001"),
                "grade_002": t.get("grade_estimate"),
            })

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": f"proto_v0 / BARI_RECAL_P0={flag}",
        "change": "EV-043 industrial-extrusion NOVA 4 signal (TASK-216)",
        "source": "Shufersal + Yohananof + Carrefour; deduped by barcode",
        "processed": len(traces),
        "scored": len(sufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "nova_distribution": nova_dist,
        "top5": [{"name": name(t), "score": t.get("final_score_estimate"),
                  "grade": t.get("grade_estimate")} for t in top5],
        "bottom5": [{"name": name(t), "score": t.get("final_score_estimate"),
                     "grade": t.get("grade_estimate")} for t in bottom5],
        "delta_from_run_001": delta_rows,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", path)
    log.info("Grades=%s median=%s scored=%d", dist, median, len(sufficient))
    log.info("Products changed: %d", len(delta_rows))
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
