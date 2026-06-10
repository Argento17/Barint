# -*- coding: utf-8 -*-
"""
BSIP2 Prototype v0 — Juices & Fruit Drinks Batch Runner (run_juices_yohananof_002)
TASK-217 / BEV-084 — re-run with juice_100 NOVA-1 floor gate active.

Changes from run_juices_yohananof_001:
  - juice_100 NOVA-1 floor gate implemented in score_engine.apply_floors()
  - Four scope-excluded products excluded from this run:
      bsip1_juice_7290013608680  (jc-015 — מיץ עגבניות, tomato juice, fruit_drink)
      bsip1_juice_5411188115434  (jc-018 — אלפרו בריסטה סויה, soy drink, fruit_drink)
      bsip1_juice_7290110558420  (jc-020 — אלפרו שיבולת שועל, oat drink, fruit_drink)
      bsip1_juice_7290110325893  (jc-024 — תנובה גו אייס קפה, coffee-milk drink, fruit_drink)

Source: BSIP1 run_juices_yohananof_001 (bsip1_outputs/)
Engine: 0.4.1 + BARI_RECAL_P0=on + TASK-217 juice_100 floor gate
Evidence: BEV-084 (evidence_registry_v1.md)

Output: 02_products/juices/bsip2_outputs/run_juices_yohananof_002/
"""
import sys
import os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("BARI_RECAL_P0", "on")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

import json
import pathlib
import logging
import datetime

SRC = pathlib.Path(__file__).parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from input_loader import load_batch
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_juices_yohananof_002")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\juices\reports")
RUN_ID       = "run_juices_yohananof_002"

# TASK-217: scope-excluded products (non-juice or non-comparable sub-categories).
# These four products are excluded from the 28-product juice_100+juice-adjacent corpus.
EXCLUDED_PIDS = {
    "bsip1_juice_7290013608680",   # jc-015 מיץ עגבניות (tomato juice — fruit_drink)
    "bsip1_juice_5411188115434",   # jc-018 אלפרו בריסטה סויה (soy drink — fruit_drink)
    "bsip1_juice_7290110558420",   # jc-020 אלפרו שיבולת שועל (oat drink — fruit_drink)
    "bsip1_juice_7290110325893",   # jc-024 תנובה גו אייס קפה (coffee-milk — fruit_drink)
}

BEVERAGE_OK_CATEGORIES = {"beverage", "juice", "juices", "fruit_drink", "soft_drink"}

EXPECTED_SCORE_MIN = 10
EXPECTED_SCORE_MAX = 75


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    try:
        trace["structural_class"] = classify_structural_class(trace)
    except Exception:
        trace["structural_class"] = None
    return trace


def run_batch():
    log.info("=== BSIP2 Juices — %s (engine 0.4.1, BARI_RECAL_P0=on, TASK-217 floor gate) ===", RUN_ID)
    log.info("BEV-084: juice_100 NOVA-1 floor gate ACTIVE")
    log.info("Excluded PIDs: %s", EXCLUDED_PIDS)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_ROOT / "products"
    if prod_dir.exists():
        import shutil
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    all_products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d (before exclusion filter)", len(all_products))

    # Apply TASK-217 scope exclusion
    products = [
        p for p in all_products
        if p.get("canonical_product_id") not in EXCLUDED_PIDS
    ]
    skipped = [p.get("canonical_product_id") for p in all_products
               if p.get("canonical_product_id") in EXCLUDED_PIDS]
    log.info("Products after exclusion: %d  (excluded: %s)", len(products), skipped)

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(traces, errors, products, skipped)
    return traces, errors


def _write_summary(traces, errors, products, skipped_pids):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("final_score_estimate") is not None]
    n = len(traces)

    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1

    scores_list_raw = sorted([t["final_score_estimate"] for t in sufficient])
    median = scores_list_raw[len(scores_list_raw)//2] if scores_list_raw else None

    pmap = {p.get("canonical_product_id"): p for p in products}
    subpool_stats = {}
    anomalies = []

    # Track TASK-217 floor gate outcomes
    gate_blocked = []
    gate_passed  = []

    for t in sufficient:
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id")
        p = pmap.get(pid, {})
        pool = p.get("juice_subpool", "unknown")
        ps = subpool_stats.setdefault(pool, {"count": 0, "scores": [], "grades": {}})
        ps["count"] += 1
        score = t.get("final_score_estimate")
        ps["scores"].append(score)
        g = t.get("grade_estimate")
        ps["grades"][g] = ps["grades"].get(g, 0) + 1

        ref_name = (t.get("input_reference") or {}).get("canonical_name_he") or pid

        # Capture floor gate outcomes for the summary
        floors_considered = t.get("floors_considered") or []
        for fc in floors_considered:
            if isinstance(fc, dict) and fc.get("gate") == "juice100_nova1_floor_gate":
                if fc.get("result") == "blocked":
                    gate_blocked.append({"pid": pid, "name": ref_name, "score": score,
                                         "grade": g, "reason": fc.get("reason","")})
                elif fc.get("result") == "passed":
                    gate_passed.append({"pid": pid, "name": ref_name, "score": score,
                                        "grade": g})

        if score is not None and score > EXPECTED_SCORE_MAX:
            anomalies.append({
                "pid": pid, "name": ref_name, "score": score, "grade": g,
                "flag": f"SCORE_ABOVE_EXPECTED_MAX_{EXPECTED_SCORE_MAX}",
                "subpool": pool,
            })
        if pool == "fruit_drink" and g in ("A", "B", "C"):
            anomalies.append({
                "pid": pid, "name": ref_name, "score": score, "grade": g,
                "flag": f"FRUIT_DRINK_TOO_HIGH: expected D–E, got {g}",
                "subpool": pool,
            })

    for ps in subpool_stats.values():
        sc = sorted(s for s in ps["scores"] if s is not None)
        ps["score_median"] = sc[len(sc)//2] if sc else None
        ps["score_range"] = [sc[0], sc[-1]] if sc else None
        del ps["scores"]

    scores_with_info = [
        {
            "pid": (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id"),
            "name": (t.get("input_reference") or {}).get("canonical_name_he") or "",
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
        }
        for t in sufficient
    ]
    scores_with_info.sort(key=lambda x: (x["score"] or 0), reverse=True)

    summary = {
        "run_id":           RUN_ID,
        "generated":        run_dt,
        "engine":           "proto_v0 / 0.4.1 + BARI_RECAL_P0=on + TASK-217 juice_100 floor gate (BEV-084)",
        "source":           "Yohananof storefront scrape → BSIP1 run_juices_yohananof_001",
        "task_ref":         "TASK-217",
        "evidence_ref":     "BEV-084",
        "processed":        n,
        "scored":           len(sufficient),
        "errors":           len(errors),
        "excluded_pids":    sorted(EXCLUDED_PIDS),
        "skipped_pids":     skipped_pids,
        "grade_distribution": dist,
        "score_median":     median,
        "score_range":      [scores_list_raw[0], scores_list_raw[-1]] if scores_list_raw else None,
        "grade_thresholds": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
        "subpool_stats":    subpool_stats,
        "scores":           scores_with_info,
        "task217_floor_gate": {
            "gate_blocked_count": len(gate_blocked),
            "gate_passed_count":  len(gate_passed),
            "gate_blocked":       gate_blocked,
            "gate_passed":        gate_passed,
        },
        "anomalies":        anomalies,
        "error_detail":     errors,
        "plausibility_check": {
            "expected_score_range": [EXPECTED_SCORE_MIN, EXPECTED_SCORE_MAX],
            "anomaly_count": len(anomalies),
        },
    }
    path = OUTPUT_ROOT / "run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)

    log.info("Scores (top→bottom):")
    for s in scores_with_info:
        log.info("  %s  %s/%-2s  %s", s["pid"], s["score"], s["grade"], s["name"][:55])
    log.info("Grades=%s  median=%s  anomalies=%d", dist, median, len(anomalies))
    log.info("TASK-217 floor gate: blocked=%d  passed=%d", len(gate_blocked), len(gate_passed))
    if gate_blocked:
        log.info("Floor gate BLOCKED products:")
        for gb in gate_blocked:
            log.info("  %s  %s/%s  %s", gb["pid"], gb["score"], gb["grade"], gb.get("reason",""))
    if anomalies:
        log.warning("ANOMALIES FLAGGED: %d", len(anomalies))
        for a in anomalies:
            log.warning("  %s", a)


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
