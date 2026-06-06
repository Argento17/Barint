"""
BSIP2 — Multi-retailer cereals batch runner (run_cereals_multiretailer_001, TASK-184).
Engine: BARI_RECAL_P0=on + nova_proxy EV-044 — BYTE-IDENTICAL to run_cereals_005.
This run scores ONLY the 42 NEW (deduped) Carrefour/Yochananof products; the engine,
router, nova proxy and score logic are UNCHANGED (acquisition + curation only).
Source: BSIP1 run_cereals_multiretailer_001 (OFF candidate panels, EV-045/045b curated).
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001/
"""
import sys, json, pathlib, logging, datetime
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
RUN_ID       = "run_cereals_multiretailer_001"
CEREAL_OK = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}


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
    import os
    flag = os.environ.get("BARI_RECAL_P0", "off")
    log.info("=== BSIP2 multi-retailer cereals — %s (BARI_RECAL_P0=%s) ===", RUN_ID, flag)
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
    pmap = {p.get("canonical_product_id"): p for p in products}
    traces, errors, misroutes = [], [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            if trace.get("category") not in CEREAL_OK:
                ref = trace.get("input_reference") or {}
                misroutes.append({"pid": pid, "name": ref.get("product_name_he") or ref.get("canonical_name_he") or "",
                                  "routed_to": trace.get("category")})
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

    def subpool(pid):
        return ((pmap.get(pid, {}).get("cereals_governance") or {}).get("construct_1_granola_subpool") or {}).get("subpool")

    def retailer(pid):
        return (pmap.get(pid, {}).get("source_retailers") or ["?"])[0]

    def name(t):
        ref = t.get("input_reference") or {}
        return ref.get("product_name_he") or ref.get("canonical_name_he") or ""

    def leaderboard(pool):
        rows = [t for t in sufficient if (pool == "granola") == (subpool(t.get("canonical_product_id")) == "granola")]
        rows.sort(key=lambda t: -t.get("final_score_estimate"))
        return [{"name": name(t), "score": t.get("final_score_estimate"), "grade": t.get("grade_estimate"),
                 "retailer": retailer(t.get("canonical_product_id"))} for t in rows[:5]]

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": f"proto_v0 / BARI_RECAL_P0={flag} (byte-identical to run_cereals_005)",
        "source": "Carrefour + Yochananof price feeds + OFF candidate panels; EV-045/045b curated; deduped vs run_005",
        "processed": len(traces), "scored": len(sufficient), "errors": len(errors),
        "grade_distribution": dist, "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "misroute_count": len(misroutes), "misroutes": misroutes,
        "leaderboard_breakfast_cereals_top5": leaderboard("standard"),
        "leaderboard_granola_muesli_top5": leaderboard("granola"),
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", path)
    log.info("Grades=%s median=%s scored=%d misroute=%d", dist, median, len(sufficient), len(misroutes))
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
