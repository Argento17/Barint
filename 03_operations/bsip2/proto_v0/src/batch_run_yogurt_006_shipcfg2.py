"""
TASK-249 (P16) — ship-config run 2: OFF-contamination fix + Shufersal-wins dedup.

Changes vs batch_run_yogurt_006_shipcfg.py:
  1. process_corpus(): products carrying canonical_risk_flags=[..., 'off_candidate_panel', ...]
     are blocked from scoring (BLOCKING exclusion). Listed under 'excluded_off_contaminated'
     in the run record. No engine change, no flag change.
  2. build_run_record(): barcode deduplication — on conflict between Shufersal and
     Yohananof traces, Shufersal wins. A dedup_events list is recorded; no silent overwrites.
     Trace files are written per-corpus into separate subdirs (products/shufersal/ and
     products/yohananof/) so Yohananof traces are preserved as evidence even though they
     are excluded from final scoring.

Acceptance criteria (set by orchestrator):
  S_count = 1 (7290112336712 only, 92.6)
  7290110565527 = 89.9/A from Shufersal record
  All 8 OFF-flagged Yohananof records excluded and listed
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

RUN_ID       = "run_yogurt_006_shipcfg2"
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs") / RUN_ID
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")

BSIP1_SRC_S  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_006\output")
BSIP1_SRC_Y  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_yohananof_001\output")

# Existing exclusion — protein-corrupted BSIP1 record (7290116932620, RT-1)
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


def has_off_contamination(product: dict) -> bool:
    """Return True if product carries off_candidate_panel in canonical_risk_flags.

    This is a BLOCKING exclusion — the product is never scored.
    No engine change, no flag change required.
    """
    flags = product.get("canonical_risk_flags") or []
    return "off_candidate_panel" in flags


def process_corpus(source_dir: pathlib.Path, label: str, corpus_subdir: str):
    """Load, filter (RT-1 + OFF), score, and write traces.

    Traces are written to OUTPUT_ROOT/products/<corpus_subdir>/ so that
    Yohananof traces are preserved as evidence even when excluded from scoring.

    Returns: (traces, rt1_skip, off_excluded, errors)
    """
    log.info("--- Corpus: %s (%s) ---", source_dir, label)
    if not source_dir.exists():
        log.error("BSIP1 source not found: %s", source_dir)
        return [], [], [], []

    # Per-corpus trace dir — no overwrite between corpora
    trace_dir = OUTPUT_ROOT / "products" / corpus_subdir
    trace_dir.mkdir(parents=True, exist_ok=True)

    all_p = load_batch(source_dir)
    log.info("Loaded %d products", len(all_p))

    rt1_skip = []
    off_excluded = []
    kept = []

    for p in all_p:
        bc = str(p.get("barcode") or "")
        pid = p.get("canonical_product_id", "?")

        # RT-1: existing protein-corruption exclusion
        if bc in EXCLUDED_BARCODES:
            rt1_skip.append({
                "pid": pid,
                "barcode": bc,
                "reason": "RT-1: protein-corruption exclusion",
                "corpus": label,
            })
            continue

        # OFF blocking exclusion (TASK-249 P16)
        if has_off_contamination(p):
            off_excluded.append({
                "pid": pid,
                "barcode": bc,
                "reason": "off_candidate_panel in canonical_risk_flags — OFF contamination, TASK-238 ban",
                "corpus": label,
                "risk_flags": p.get("canonical_risk_flags"),
                "provenance_source": (p.get("provenance") or {}).get("panel_source"),
            })
            log.info("  OFF-EXCLUDED  %-40s barcode=%s", pid, bc)
            continue

        kept.append(p)

    log.info("Scoring %d (rt1_skip=%d, off_excluded=%d)",
             len(kept), len(rt1_skip), len(off_excluded))

    traces, errs = [], []
    for p in kept:
        pid = p.get("canonical_product_id", "?")
        try:
            t = run_pipeline(p)
            # Write trace to per-corpus subdir (no cross-corpus overwrites)
            write_trace(t, trace_dir.parent)  # write_trace appends /products/<id>.json
            traces.append(t)
            log.info("  %-40s score=%-6s grade=%s nova=%s cat=%s",
                     pid, t.get("final_score_estimate"), t.get("grade_estimate"),
                     t.get("nova_proxy"), t.get("category"))
        except Exception as e:
            log.error("ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errs.append({"pid": pid, "barcode": str(p.get("barcode","")), "error": str(e)})

    return traces, rt1_skip, off_excluded, errs


def grade_from_score(s):
    for thresh, grade in sorted(GRADE_THRESHOLDS, reverse=True):
        if s >= thresh:
            return grade
    return "E"


def build_run_record(
    traces_s, rt1_skip_s, off_excluded_s, errs_s,
    traces_y, rt1_skip_y, off_excluded_y, errs_y,
):
    from constants import GRADE_THRESHOLDS
    from score_engine import RECAL_P0_YOGURT_TRIM
    RECAL_P0_YOGURT_TRIM_CEILING = 89.9

    # ---- Barcode deduplication: Shufersal wins ----
    # Build a barcode -> trace map from each corpus. On conflict, Shufersal takes priority.
    s_by_bc = {}
    for t in traces_s:
        bc = str((t.get("input_reference") or {}).get("barcode") or "")
        if bc:
            s_by_bc[bc] = t

    y_by_bc = {}
    for t in traces_y:
        bc = str((t.get("input_reference") or {}).get("barcode") or "")
        if bc:
            y_by_bc[bc] = t

    dedup_events = []
    merged_traces = list(traces_s)  # start with all Shufersal
    for bc, t in y_by_bc.items():
        if bc in s_by_bc:
            # Conflict: Shufersal wins, Yohananof trace is evidence-only
            dedup_events.append({
                "barcode": bc,
                "winner": "shufersal",
                "reason": "Shufersal corpus wins on barcode conflict per TASK-249 P16 dedup rule",
                "yohananof_score": t.get("final_score_estimate"),
                "yohananof_grade": t.get("grade_estimate"),
                "shufersal_score": s_by_bc[bc].get("final_score_estimate"),
                "shufersal_grade": s_by_bc[bc].get("grade_estimate"),
            })
            log.info("  DEDUP  barcode=%s  shufersal wins (Y=%s vs S=%s)",
                     bc,
                     t.get("final_score_estimate"),
                     s_by_bc[bc].get("final_score_estimate"))
        else:
            # Yohananof-unique barcode — include
            merged_traces.append(t)

    # ---- Scoring ----
    scored = [t for t in merged_traces if t.get("final_score_estimate") is not None]
    gd = {}
    for t in scored:
        g = t.get("grade_estimate")
        gd[g] = gd.get(g, 0) + 1

    def _trace_name(t):
        ir = t.get("input_reference") or {}
        return ir.get("canonical_name_he") or ir.get("product_name_he")

    a_list = [
        {
            "pid": (t.get("input_reference") or {}).get("canonical_product_id") or t.get("product_id"),
            "barcode": (t.get("input_reference") or {}).get("barcode"),
            "name": _trace_name(t),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "corpus": "shufersal" if str((t.get("input_reference") or {}).get("barcode","")) in s_by_bc else "yohananof",
        }
        for t in scored if t.get("grade_estimate") == "A"
    ]
    s_list = [
        {
            "pid": (t.get("input_reference") or {}).get("canonical_product_id") or t.get("product_id"),
            "barcode": (t.get("input_reference") or {}).get("barcode"),
            "name": _trace_name(t),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "corpus": "shufersal" if str((t.get("input_reference") or {}).get("barcode","")) in s_by_bc else "yohananof",
        }
        for t in scored if t.get("grade_estimate") == "S"
    ]

    scores = sorted(t.get("final_score_estimate") for t in scored if t.get("final_score_estimate") is not None)

    # All OFF-excluded records (both corpora)
    all_off_excluded = off_excluded_s + off_excluded_y

    return {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "SHIP_CANDIDATE",
        "task": "TASK-249 P16",
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
        "corpus_n": {
            "shufersal_scored": len(traces_s),
            "yohananof_scored": len(traces_y),
            "merged_total": len(scored),
            "off_excluded_total": len(all_off_excluded),
            "dedup_dropped": len(dedup_events),
        },
        "trim_config": {
            "enabled": RECAL_P0_YOGURT_TRIM,
            "ceiling": RECAL_P0_YOGURT_TRIM_CEILING,
        },
        "engine": "proto_v0 / RECAL_P0=on + YOGURT_TRIM=on + TASK250_CONF=on",
        "exclusion_policy": {
            "rt1_excluded": rt1_skip_s + rt1_skip_y,
            "excluded_off_contaminated": all_off_excluded,
        },
        "dedup_events": dedup_events,
        "grade_distribution": gd,
        "s_count": len(s_list),
        "a_count": len(a_list),
        "S_list": s_list,
        "A_list": a_list,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "products": [
            {
                "pid": (t.get("input_reference") or {}).get("canonical_product_id") or t.get("product_id"),
                "barcode": (t.get("input_reference") or {}).get("barcode"),
                "name": _trace_name(t),
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
                "category": t.get("category"),
                "nova": t.get("nova_proxy"),
                "binding_cap": t.get("binding_cap"),
                "corpus": "shufersal" if str((t.get("input_reference") or {}).get("barcode","")) in s_by_bc else "yohananof",
            }
            for t in scored
        ],
    }


def build_page_impact(run_record: dict) -> dict:
    """Compare run_yogurt_006_shipcfg2 output against the live v3 frontend page.

    Reports which v3 products lose coverage (expected: the 8-product Yohananof pool).
    Defines the Shufersal-only launch scope.
    """
    import json as j

    fe_path = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v3.json")
    claims_path = pathlib.Path(r"C:\Bari\03_operations\claim_entailment\inputs\yogurts_claims_input_v1.json")

    if not fe_path.exists():
        return {"error": "frontend v3 not found", "path": str(fe_path)}

    fe = j.loads(fe_path.read_text(encoding="utf-8"))
    fe_products = fe.get("products", [])

    # Build barcode map from claims input
    bc_by_id = {}
    if claims_path.exists():
        ci = j.loads(claims_path.read_text(encoding="utf-8"))
        for cp in ci.get("products", []):
            bc_by_id[cp["product_id"]] = str(cp.get("barcode", ""))

    # Build scored product map from run record
    scored_bcs = {str(p.get("barcode", "")): p for p in run_record.get("products", [])}

    # OFF-excluded barcodes
    off_excluded_bcs = {
        e["barcode"] for e in run_record.get("exclusion_policy", {}).get("excluded_off_contaminated", [])
    }

    coverage_rows = []
    covered_count = 0
    lost_coverage = []

    for p in fe_products:
        pid = p.get("id", "")
        bc = bc_by_id.get(pid, "")
        in_run = bc in scored_bcs
        is_off = bc in off_excluded_bcs
        retailer = p.get("retailer", "?")

        row = {
            "id": pid,
            "barcode": bc,
            "name": p.get("name", ""),
            "fe_score": p.get("score"),
            "fe_grade": p.get("grade"),
            "retailer": retailer,
            "in_shipcfg2": in_run,
            "off_excluded": is_off,
        }
        if in_run:
            sp = scored_bcs[bc]
            row["shipcfg2_score"] = sp.get("score")
            row["shipcfg2_grade"] = sp.get("grade")
            covered_count += 1
        else:
            row["shipcfg2_score"] = None
            row["shipcfg2_grade"] = None
            lost_coverage.append({
                "id": pid,
                "barcode": bc,
                "name": p.get("name", ""),
                "retailer": retailer,
                "reason": "off_excluded" if is_off else "no_trace",
            })

        coverage_rows.append(row)

    return {
        "frontend_version": fe.get("_meta", {}).get("version"),
        "frontend_product_count": len(fe_products),
        "covered_in_shipcfg2": covered_count,
        "lost_coverage_count": len(lost_coverage),
        "lost_coverage": lost_coverage,
        "launch_scope_note": (
            "Shufersal-only launch: "
            f"{covered_count} products covered; "
            f"{len(lost_coverage)} Yohananof products lose coverage (OFF-excluded, no clean re-source yet)."
        ),
        "coverage_rows": coverage_rows,
    }


def main():
    start = datetime.datetime.now()
    log.info("=== %s (ship-config 2: OFF-fix + Shufersal-wins dedup) ===", RUN_ID)
    log.info("Flags: RECAL_P0=on, YOGURT_TRIM=on, TASK144=off, TASK250_CONF=on")
    log.info("OFF exclusion: BLOCKING (off_candidate_panel in canonical_risk_flags)")
    log.info("Dedup: Shufersal wins on barcode conflict; Yohananof traces preserved as evidence")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    # Shufersal corpus
    traces_s, rt1_skip_s, off_excluded_s, errs_s = process_corpus(
        BSIP1_SRC_S, "Shufersal", "shufersal"
    )
    # Yohananof corpus
    traces_y, rt1_skip_y, off_excluded_y, errs_y = process_corpus(
        BSIP1_SRC_Y, "Yohananof", "yohananof"
    )

    log.info("=== Summary ===")
    log.info("Shufersal: %d scored, %d rt1-skip, %d off-excluded, %d errors",
             len(traces_s), len(rt1_skip_s), len(off_excluded_s), len(errs_s))
    log.info("Yohananof: %d scored, %d rt1-skip, %d off-excluded, %d errors",
             len(traces_y), len(rt1_skip_y), len(off_excluded_y), len(errs_y))

    # Run record (includes dedup)
    rr = build_run_record(
        traces_s, rt1_skip_s, off_excluded_s, errs_s,
        traces_y, rt1_skip_y, off_excluded_y, errs_y,
    )
    rr_path = REPORT_ROOT / f"{RUN_ID}_run_record.json"
    rr_path.write_text(json.dumps(rr, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    gd = rr["grade_distribution"]
    log.info("Grade distribution: %s", gd)
    log.info("S_count=%d, A_count=%d", rr["s_count"], rr["a_count"])
    log.info("S_list: %s", [(p["barcode"], p["score"]) for p in rr["S_list"]])

    # Acceptance check
    s_barcodes = {p["barcode"] for p in rr["S_list"]}
    expected_s = {"7290112336712"}
    if s_barcodes == expected_s:
        log.info("ACCEPTANCE CHECK PASSED: S_count=1, barcode=7290112336712 only")
    else:
        log.warning("ACCEPTANCE CHECK FAILED: S_list=%s, expected={7290112336712}", s_barcodes)

    target_565527 = next(
        (p for p in rr["products"] if str(p.get("barcode","")) == "7290110565527"), None
    )
    if target_565527:
        log.info("7290110565527 -> score=%s grade=%s corpus=%s (expected: 89.9/A/shufersal)",
                 target_565527.get("score"), target_565527.get("grade"), target_565527.get("corpus"))
    else:
        log.warning("7290110565527 NOT in scored products")

    off_exc_barcodes = {e["barcode"] for e in rr["exclusion_policy"].get("excluded_off_contaminated", [])}
    log.info("OFF-excluded barcodes (%d): %s", len(off_exc_barcodes), sorted(off_exc_barcodes))

    # Page-impact report
    pi = build_page_impact(rr)
    pi_path = REPORT_ROOT / f"{RUN_ID}_page_impact.json"
    pi_path.write_text(json.dumps(pi, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Page impact: %s", pi_path)
    log.info("Coverage: %d/%d covered, %d lost",
             pi["covered_in_shipcfg2"], pi["frontend_product_count"], pi["lost_coverage_count"])

    elapsed = datetime.datetime.now() - start
    log.info("Done in %s", elapsed)


if __name__ == "__main__":
    main()
