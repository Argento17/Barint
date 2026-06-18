# BSIP2 batch -- Cakes + Hard Cookies (run_cakes_001 / TASK-283, factory run #8).
# Same category-agnostic engine as cookies run_005; flags identical (all OFF) so no
# frozen invariant / published score is touched. OFF ban absolute.
import os, sys, json, pathlib, logging, datetime
from collections import Counter
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s"); log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
CORPUS_FILE = ROOT/"02_products"/"cakes_hard_cookies"/"factory_run_001"/"corpus_filter.json"
BSIP1_DIR = ROOT/"03_operations"/"bsip1"/"run_cakes_001"/"output"
BSIP2_OUT = ROOT/"02_products"/"cakes_hard_cookies"/"bsip2_outputs"/"run_cakes_001"
RUN_ID = "run_cakes_001"
(BSIP2_OUT/"products").mkdir(parents=True, exist_ok=True)


def run_pipeline(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    tr = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    return tr


def main():
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"] == "IN_SCORED"}
    log.info("=== BSIP2 run_cakes_001 — IN_SCORED=%d — flags ALL OFF ===", len(in_scored))
    recs = []
    for p in sorted(BSIP1_DIR.glob("bsip1_cakes_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if str(d.get("barcode", "")) in in_scored:
            recs.append(d)
    log.info("BSIP1 records: %d", len(recs))
    traces, errors, cats, phvo, brined = [], [], Counter(), 0, []
    for d in recs:
        bc, nm = str(d.get("barcode", "")), d.get("canonical_name_he", "")
        try:
            tr = run_pipeline(d)
            write_trace(tr, BSIP2_OUT)
            traces.append(tr)
            cats[tr.get("category")] += 1
            if (tr.get("L3_inferred_classifications") or {}).get("has_phvo"): phvo += 1
            if tr.get("context_flag") == "brined_food":
                brined.append(bc); log.error("  CRITICAL brined_food on %s %s", bc, nm)
        except Exception as e:
            errors.append({"barcode": bc, "error": str(e)})
            import traceback; traceback.print_exc()
    scores = [t["final_score_estimate"] for t in traces if t.get("final_score_estimate") is not None]
    gdist = Counter(t.get("grade_estimate", "?") for t in traces)
    n = len(scores)
    mean = sum(scores)/n if n else 0
    sd = (sum((x-mean)**2 for x in scores)/n)**0.5 if n else 0
    print(f"\n=== BSIP2 run_cakes_001 ===")
    print(f"scored={len(traces)} errors={len(errors)}")
    print(f"grade_dist={dict(sorted(gdist.items()))}")
    print(f"score: min={min(scores) if scores else '-'} max={max(scores) if scores else '-'} mean={mean:.1f} stdev={sd:.1f}")
    print(f"routing_categories={dict(cats)}")
    print(f"has_phvo (מרגרינה/שומן מוקשה fired)={phvo}")
    print(f"brined_food misfires={len(brined)} (MUST be 0)")
    print(f"traces: {BSIP2_OUT/'products'}")
    if errors: print("ERRORS:", errors[:5])
    # write a run summary
    (BSIP2_OUT/"run_summary.json").write_text(json.dumps({
        "run_id": RUN_ID, "scored": len(traces), "errors": len(errors),
        "grade_dist": dict(gdist), "score_min": min(scores) if scores else None,
        "score_max": max(scores) if scores else None, "score_mean": round(mean, 1), "score_stdev": round(sd, 1),
        "routing_categories": dict(cats), "has_phvo": phvo, "brined_misfires": len(brined),
        "flags": "all OFF", "off_used": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
