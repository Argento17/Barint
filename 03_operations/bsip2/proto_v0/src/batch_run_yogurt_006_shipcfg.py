"""
TASK-249 pre-go-live reconciliation — re-score under EXACT ship config.
Flags: BARI_RECAL_P0=on, BARI_RECAL_P0_YOGURT_TRIM=on,
       BARI_TASK144_FIXES=off, BARI_TASK250_CONF=on
Corpora: run_yogurt_006 (88 Shufersal products) + run_yogurt_yohananof_001 (8 Yohananof)
Output: 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg/
"""
import os, sys, json, pathlib, logging, datetime

# === SHIP-CONFIG FLAGS (must be set before engine imports) ===
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "on"

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import GRADE_THRESHOLDS

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

RUN_ID       = "run_yogurt_006_shipcfg"
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs") / RUN_ID
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")

BSIP1_SRC_S  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_006\output")
BSIP1_SRC_Y  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_yohananof_001\output")

EXCLUDED_BARCODES = {"7290116932620"}

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

def process_corpus(source_dir, label):
    log.info("--- Corpus: %s (%s) ---", source_dir, label)
    if not source_dir.exists():
        log.error("BSIP1 source not found: %s", source_dir); return [], [], []
    all_p = load_batch(source_dir)
    log.info("Loaded %d products", len(all_p))
    kept, skip = [], []
    for p in all_p:
        bc = str(p.get("barcode") or "")
        if bc in EXCLUDED_BARCODES:
            skip.append({"pid": p.get("canonical_product_id"), "barcode": bc, "reason": "RT-1"})
        else:
            kept.append(p)
    log.info("Scoring %d (excluded %d)", len(kept), len(skip))
    traces, errs = [], []
    for p in kept:
        pid = p.get("canonical_product_id", "?")
        try:
            t = run_pipeline(p)
            write_trace(t, OUTPUT_ROOT)
            traces.append(t)
            log.info("  %-40s score=%-6s grade=%s nova=%s cat=%s",
                     pid, t.get("final_score_estimate"), t.get("grade_estimate"),
                     t.get("nova_proxy"), t.get("category"))
        except Exception as e:
            log.error("ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errs.append({"pid": pid, "error": str(e)})
    return traces, skip, errs

def grade_from_score(s):
    for thresh, grade in sorted(GRADE_THRESHOLDS, reverse=True):
        if s >= thresh: return grade
    return "E"

def build_run_record(traces_s, traces_y):
    from constants import GRADE_THRESHOLDS
    from score_engine import RECAL_P0_YOGURT_TRIM
    RECAL_P0_YOGURT_TRIM_CEILING = 89.9
    all_t = traces_s + traces_y
    scored = [t for t in all_t if t.get("final_score_estimate") is not None]
    gd = {}
    for t in scored:
        g = t.get("grade_estimate"); gd[g] = gd.get(g, 0) + 1
    a_list = [{"pid": t.get("product_id") or t.get("canonical_product_id"),
               "barcode": (t.get("input_reference") or {}).get("barcode"),
               "name": (t.get("input_reference") or {}).get("canonical_name_he"),
               "score": t.get("final_score_estimate"),
               "grade": t.get("grade_estimate")}
              for t in scored if t.get("grade_estimate") == "A"]
    s_list = [{"pid": t.get("product_id") or t.get("canonical_product_id"),
               "barcode": (t.get("input_reference") or {}).get("barcode"),
               "name": (t.get("input_reference") or {}).get("canonical_name_he"),
               "score": t.get("final_score_estimate"),
               "grade": t.get("grade_estimate")}
              for t in scored if t.get("grade_estimate") == "S"]
    scores = sorted(t.get("final_score_estimate") for t in scored)
    return {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "SHIP_CANDIDATE",
        "flags": {
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK144_FIXES": "off",
            "BARI_TASK250_CONF": "on",
        },
        "corpus": {
            "shufersal": str(BSIP1_SRC_S),
            "yohananof": str(BSIP1_SRC_Y),
        },
        "corpus_n": {"shufersal": len(traces_s), "yohananof": len(traces_y), "total": len(scored)},
        "trim_config": {
            "enabled": RECAL_P0_YOGURT_TRIM,
            "ceiling": RECAL_P0_YOGURT_TRIM_CEILING,
        },
        "engine": "proto_v0 / RECAL_P0=on + YOGURT_TRIM=on + TASK250_CONF=on",
        "grade_distribution": gd,
        "s_count": len(s_list),
        "a_count": len(a_list),
        "S_list": s_list,
        "A_list": a_list,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "products": [{
            "pid": t.get("product_id") or t.get("canonical_product_id"),
            "barcode": (t.get("input_reference") or {}).get("barcode"),
            "name": (t.get("input_reference") or {}).get("canonical_name_he"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "category": t.get("category"),
            "nova": t.get("nova_proxy"),
            "binding_cap": t.get("binding_cap"),
        } for t in scored],
    }

def build_comparison(traces_s, traces_y, frontend_path):
    import json as j
    # Load barcode map from claims input (v3 frontend has no barcode field)
    claims_path = r"C:\Bari\03_operations\claim_entailment\inputs\yogurts_claims_input_v1.json"
    bc_by_id = {}
    if pathlib.Path(claims_path).exists():
        ci = j.load(open(claims_path, encoding="utf-8"))
        for cp in ci.get("products", []):
            bc_by_id[cp["product_id"]] = cp.get("barcode", "")

    fe = j.load(open(frontend_path, encoding="utf-8"))
    fe_products = fe["products"]
    fe_map = {}
    for p in fe_products:
        pid = p.get("id", "")
        bc = bc_by_id.get(pid, "")
        fe_map[bc] = {"id": pid, "name": p.get("name"),
                      "score": p.get("score"), "grade": p.get("grade"),
                      "retailer": p.get("retailer", "?")}

    trace_map_s = {}
    for t in traces_s:
        bc = str((t.get("input_reference") or {}).get("barcode", ""))
        if bc:
            trace_map_s[bc] = {"score": t.get("final_score_estimate"), "grade": t.get("grade_estimate"),
                               "nova": t.get("nova_proxy"), "pool": "shufersal"}
    trace_map_y = {}
    for t in traces_y:
        bc = str((t.get("input_reference") or {}).get("barcode", ""))
        if bc:
            trace_map_y[bc] = {"score": t.get("final_score_estimate"), "grade": t.get("grade_estimate"),
                               "nova": t.get("nova_proxy"), "pool": "yohananof"}
    # Merge: Yohananof pool traces take precedence for Yohananof products
    trace_map = {**trace_map_s, **trace_map_y}

    rows = []
    match_count, mismatch_count = 0, 0
    for bc, p in fe_map.items():
        tr = trace_map.get(bc)
        if tr is None:
            rows.append({"barcode": bc, "name": p["name"], "id": p["id"],
                         "fe_score": p["score"], "fe_grade": p["grade"],
                         "ship_score": "NO_TRACE", "ship_grade": "NO_TRACE",
                         "match": "NO_TRACE", "retailer": p["retailer"]})
            mismatch_count += 1
            continue
        fe_s = p["score"]
        ship_s = tr["score"]
        fe_g = p["grade"]
        ship_g = tr["grade"]
        match = (round(fe_s) == round(ship_s) if (fe_s and ship_s) else False) and (fe_g == ship_g)
        if match: match_count += 1
        else: mismatch_count += 1
        rows.append({"barcode": bc, "name": p["name"], "id": p["id"],
                     "fe_score": fe_s, "fe_grade": fe_g,
                     "ship_score": ship_s, "ship_grade": ship_g,
                     "match": match, "retailer": p["retailer"]})
    return {"frontend": str(frontend_path), "frontend_version": fe.get("_meta", {}).get("version"),
            "total_page_products": len(fe_products), "in_trace_map": len(trace_map),
            "match": match_count, "mismatch": mismatch_count,
            "no_trace": sum(1 for r in rows if r["match"] == "NO_TRACE"),
            "rows": rows}

def main():
    start = datetime.datetime.now()
    log.info("=== %s (ship-config reconciliation) ===", RUN_ID)
    log.info("Flags: RECAL_P0=on, YOGURT_TRIM=on, TASK144=off, TASK250_CONF=on")
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    # Shufersal corpus
    traces_s, skip_s, errs_s = process_corpus(BSIP1_SRC_S, "Shufersal")
    # Yohananof corpus
    traces_y, skip_y, errs_y = process_corpus(BSIP1_SRC_Y, "Yohananof")

    log.info("=== Summary ===")
    log.info("Shufersal: %d scored, %d excluded, %d errors", len(traces_s), len(skip_s), len(errs_s))
    log.info("Yohananof: %d scored, %d excluded, %d errors", len(traces_y), len(skip_y), len(errs_y))

    # Run record
    rr = build_run_record(traces_s, traces_y)
    rr_path = REPORT_ROOT / f"{RUN_ID}_run_record.json"
    (rr_path).write_text(json.dumps(rr, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    # Run summary
    gd = rr["grade_distribution"]
    summary = {
        "run_id": RUN_ID, "generated": rr["generated"],
        "source": "Shufersal (run_yogurt_006 corpus) + Yohananof (run_yogurt_yohananof_001 corpus)",
        "engine": "proto_v0 / ship config (RECAL_P0=on, YOGURT_TRIM=on, TASK250_CONF=on)",
        "processed": len(traces_s) + len(traces_y),
        "scored": sum(gd.values()) if gd else 0,
        "s_count": rr["s_count"],
        "a_count": rr["a_count"],
        "grade_distribution": gd,
        "errors": len(errs_s) + len(errs_y),
    }
    summary_path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    (summary_path).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("Summary: %s", summary_path)

    # Comparison with v3 frontend
    v3_path = r"C:\Bari\02_products\yogurt_system\yogurts_frontend_v3.json"
    v3_path2 = r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v3.json"
    for fp in [v3_path, v3_path2]:
        if pathlib.Path(fp).exists():
            comp = build_comparison(traces_s, traces_y, fp)
            comp_path = REPORT_ROOT / f"{RUN_ID}_vs_v3_comparison.json"
            (comp_path).write_text(json.dumps(comp, ensure_ascii=False, indent=1), encoding="utf-8")
            log.info("Comparison vs v3: %s", comp_path)
            log.info("Match: %d/%d, Mismatch: %d, NO_TRACE: %d",
                     comp["match"], comp["total_page_products"],
                     comp["mismatch"], comp["no_trace"])
            break

    elapsed = datetime.datetime.now() - start
    log.info("Done in %s", elapsed)

if __name__ == "__main__":
    main()
