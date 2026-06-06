"""
BSIP2 Prototype v0 — Butter Batch Runner (butter_run_003) — TASK-191 Phase B.2.

Input:   C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_merged.json
         (39 products: 16 confirmed high-trust + 23 candidate low-trust enriched)

Output:  C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_003\\products\\
         + C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_003_summary.json

Engine flags: BARI_RECAL_P0=off, BARI_GLASSBOX_W4=on, BARI_GLASSBOX_D5D6=off

Engine fixes active (all three):
  - EV-047: KCAL_PLAUSIBLE_UPPER=800 (kcal false-positive fix for high-fat products)
  - EV-048: SAT_FAT_CAP_ENDEMIC_WFF_FRACTION=0.50 (sat-fat cap gated for intact dairy fat)
  - EV-050: _natural_dairy_trans_exempt gate — trans fat veto exempt for whole_food_fat
            products with no PHVO markers (natural CLA/vaccenic acid in dairy butter).

What changed since run_002:
  - EV-050 now active in score_engine.py (committed prior to this run).
    The 6 OFF-sourced candidate salted butters that scored 0/E due to natural dairy
    trans fat (CLA/vaccenic acid, 3.28-3.7g/100g) should now score normally.
    Expected: ~50/C — same pattern as the 5 confirmed label-scanned salted butters.

Corpus classification:
  - "confirmed" = canonical_trust_level == "high" (16 products, BSIP0 label-scanned)
  - "candidate"  = canonical_trust_level == "low"  (23 products, enriched via OFF/FDC)
    Candidate scores carry a confidence ceiling from trust_level=low deduction.
    Do NOT promote candidate scores to verified — QA gate required.
"""
import sys
import json
import pathlib
import logging
import datetime
import statistics
import re

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
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_003")
SUMMARY_PATH = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_003_summary.json")
RUN_ID       = "butter_run_003"
TASK_ID      = "TASK-191"

WHOLE_FOOD_FAT_EXPECTED = {"whole_food_fat"}
ADDITIVE_SPREAD_BARCODES = {"7290108507997"}

# 6 candidate salted butters that scored 0/E in run_002 due to trans fat veto misfire.
# EV-050 should exempt these; we verify the fix by tracking them explicitly.
EV050_AFFECTED_PIDS = {
    "bsip1_butter_3161911229199",  # חמאה צרפתית רכה למריחה
    "bsip1_butter_5099460004132",  # חמאה קרי גולד מלוחה
    "bsip1_butter_9414544900022",  # חמאה אנקור מלוחה
    "bsip1_butter_5740900400238",  # חמאה לורפק מלוחה
    "bsip1_butter_7290000066035",  # חמאה טרה מלוחה
    "bsip1_butter_3412130012534",  # חמאה פיזן ברטון מלוחה
}


def is_confirmed(product: dict) -> bool:
    """True for original BSIP0 scraped products (high trust = confirmed_per_100g)."""
    return product.get("canonical_trust_level") == "high"


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
    log.info("  EV-047 active: KCAL_PLAUSIBLE_UPPER=800")
    log.info("  EV-048 active: SAT_FAT_CAP_ENDEMIC_WFF_FRACTION=0.50")
    log.info("  EV-050 active: _natural_dairy_trans_exempt (whole_food_fat + no PHVO)")
    log.info("  BARI_RECAL_P0=%s  BARI_GLASSBOX_W4=%s  BARI_GLASSBOX_D5D6=%s",
             os.environ.get("BARI_RECAL_P0", "off"),
             os.environ.get("BARI_GLASSBOX_W4", "on (default)"),
             os.environ.get("BARI_GLASSBOX_D5D6", "off"))

    if not BSIP1_PATH.exists():
        log.error("BSIP1 source not found: %s", BSIP1_PATH)
        return None

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_ROOT / "products"
    if prod_dir.exists():
        import shutil
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    raw_list = json.loads(BSIP1_PATH.read_text(encoding="utf-8"))
    log.info("Products loaded: %d", len(raw_list))

    traces    = []
    errors    = []
    misroutes = []
    ev050_resolved = []  # products from the previously-0/E group that now score > 0

    for product in raw_list:
        product["_source_path"] = str(BSIP1_PATH)
        product["_load_errors"] = validate_product(product)

        pid  = product.get("canonical_product_id", "unknown")
        name = product.get("canonical_name_he", "")
        conf = "confirmed" if is_confirmed(product) else "candidate"

        try:
            trace = run_pipeline(product)
            trace["_corpus_class"] = conf
            trace["_barcode"]      = product.get("barcode", "")
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)

            cat   = trace.get("category")
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            suff  = trace.get("data_sufficiency")

            if pid in EV050_AFFECTED_PIDS:
                ev050_resolved.append({
                    "pid": pid,
                    "name": name,
                    "score": score,
                    "grade": grade,
                    "ev050_fixed": score is not None and score > 0,
                })

            if cat not in WHOLE_FOOD_FAT_EXPECTED:
                misroutes.append({"pid": pid, "name": name, "routed_to": cat, "expected": "whole_food_fat"})
                log.warning("  MISROUTE: %s -> %s", name, cat)
            else:
                log.info("  %-12s  %-10s  %s | %s/%s | suff=%s",
                         conf, pid[-20:], name[:28], score, grade, suff)

        except Exception as e:
            log.error("  PIPELINE ERROR for %s (%s): %s", pid, name, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "name": name, "error": str(e)})

    # ── Per-product table for owner review ────────────────────────────────────
    per_product_table = []
    for t in traces:
        inp = t.get("input_reference") or {}
        score = t.get("final_score_estimate")
        grade = t.get("grade_estimate")
        conf  = t.get("_corpus_class", "?")
        barcode = t.get("_barcode", "")

        # Confidence band: derive from trace confidence score
        conf_score = t.get("confidence_score") or 0
        if conf_score >= 70:
            conf_band = "high"
        elif conf_score >= 40:
            conf_band = "partial"
        else:
            conf_band = "insufficient"

        per_product_table.append({
            "barcode":             barcode,
            "name":                inp.get("product_name_he") or t.get("product_name_he", ""),
            "brand":               inp.get("brand", ""),
            "score":               score,
            "grade":               grade,
            "confidence_band":     conf_band,
            "confidence_score":    conf_score,
            "verification_status": "confirmed" if conf == "confirmed" else "candidate",
            "pid":                 inp.get("canonical_product_id", ""),
            "caps_applied":        [c.get("rule") for c in (t.get("caps_applied") or [])],
            "floors_applied":      [f.get("floor_type") for f in (t.get("floors_applied") or [])],
        })

    # Sort by score descending for readability
    per_product_table.sort(key=lambda x: (x["score"] or -1), reverse=True)

    # ── Aggregate stats ────────────────────────────────────────────────────────
    confirmed_traces = [t for t in traces if t.get("_corpus_class") == "confirmed"]
    candidate_traces = [t for t in traces if t.get("_corpus_class") == "candidate"]

    def grade_dist(trace_list: list) -> dict:
        d: dict[str, int] = {}
        for t in trace_list:
            g = t.get("grade_estimate") or "INSUFFICIENT"
            d[g] = d.get(g, 0) + 1
        return dict(sorted(d.items()))

    def score_stats(trace_list: list) -> dict:
        scores = [t["final_score_estimate"] for t in trace_list
                  if t.get("final_score_estimate") is not None]
        if not scores:
            return {"min": None, "max": None, "mean": None, "count": 0}
        return {
            "min":   round(min(scores), 1),
            "max":   round(max(scores), 1),
            "mean":  round(statistics.mean(scores), 1),
            "count": len(scores),
        }

    all_grade_dist  = grade_dist(traces)
    all_score_range = score_stats(traces)
    confirmed_dist  = grade_dist(confirmed_traces)
    confirmed_range = score_stats(confirmed_traces)
    candidate_dist  = grade_dist(candidate_traces)
    candidate_range = score_stats(candidate_traces)

    # ── Trans fat veto fires ──────────────────────────────────────────────────
    trans_fat_vetoes_fired = sum(
        1 for t in traces
        if t.get("trans_fat_veto", False)
    )

    # ── Sat-fat cap fires ─────────────────────────────────────────────────────
    sat_fat_caps_fired = sum(
        1 for t in traces
        if any("SAT_FAT" in (c.get("rule") or "") for c in (t.get("caps_applied") or []))
    )
    sat_fat_caps_gated = 0
    for t in traces:
        for c in (t.get("caps_considered") or []):
            if "ISRAELI_RED_LABEL_1_SAT_FAT" in (c.get("rule") or ""):
                note = c.get("note") or ""
                if "EV-048 endemic gate" in note and not c.get("fired", True):
                    sat_fat_caps_gated += 1
                    break

    # ── Floor activations ─────────────────────────────────────────────────────
    floor_activations = sum(
        1 for t in traces
        if any("floor_type" in f for f in (t.get("floors_applied") or []))
    )

    # ── FLOOR_CAP_INTERACTION ─────────────────────────────────────────────────
    floor_cap_interactions = [
        {
            "pid":   t.get("input_reference", {}).get("canonical_product_id"),
            "name":  t.get("input_reference", {}).get("product_name_he"),
            "flags": [f for f in (t.get("unresolved_flags") or []) if "FLOOR_CAP_INTERACTION" in f],
        }
        for t in traces
        if any("FLOOR_CAP_INTERACTION" in (f or "") for f in (t.get("unresolved_flags") or []))
    ]

    # ── Additive spread differentiation ───────────────────────────────────────
    additive_spread_traces = [
        t for t in traces if t.get("_barcode") in ADDITIVE_SPREAD_BARCODES
    ]
    # Compare against UNSALTED plain butter (highest expected score = 70/B); use
    # confirmed traces only, excluding the spread itself.
    unsalted_confirmed_scores = [
        t["final_score_estimate"] for t in confirmed_traces
        if t.get("final_score_estimate") is not None
        and t.get("_barcode") not in ADDITIVE_SPREAD_BARCODES
        and not any("HIGH_SODIUM" in (c.get("rule") or "") for c in (t.get("caps_applied") or []))
    ]
    additive_spread_check = []
    for t in additive_spread_traces:
        spread_score = t.get("final_score_estimate")
        additive_spread_check.append({
            "barcode": t.get("_barcode"),
            "name":    t.get("input_reference", {}).get("product_name_he"),
            "score":   spread_score,
            "grade":   t.get("grade_estimate"),
            "caps_applied": [c.get("rule") for c in (t.get("caps_applied") or [])],
            "unsalted_plain_butter_max": round(max(unsalted_confirmed_scores), 1) if unsalted_confirmed_scores else None,
            "differentiated_below_unsalted": (
                spread_score is not None
                and unsalted_confirmed_scores
                and spread_score < min(unsalted_confirmed_scores)
            ),
        })

    # ── FDC source clustering ──────────────────────────────────────────────────
    enrichment_report_path = pathlib.Path(
        r"C:\Bari\02_products\butter\bsip1_outputs\butter_enrichment_report_20260605.json"
    )
    fdc_clusters: dict[str, list] = {}
    if enrichment_report_path.exists():
        er = json.loads(enrichment_report_path.read_text(encoding="utf-8"))
        for p in er.get("products", []):
            fdc_result = p.get("fdc_result") or ""
            if "fdc_id=" in fdc_result:
                m = re.search(r"fdc_id=(\d+)", fdc_result)
                if m:
                    fdc_id = m.group(1)
                    fdc_desc = re.search(r"'(.+?)'", fdc_result)
                    if fdc_id not in fdc_clusters:
                        fdc_clusters[fdc_id] = []
                    fdc_clusters[fdc_id].append({
                        "barcode":         p["barcode"],
                        "name":            p["name"],
                        "brand":           p.get("brand"),
                        "fdc_description": fdc_desc.group(1) if fdc_desc else fdc_result,
                    })

    fdc_cluster_summary = [
        {
            "fdc_id":        fdc_id,
            "product_count": len(products),
            "description":   products[0]["fdc_description"] if products else "",
            "products":      products,
            "note": (
                f"{len(products)} products share this USDA FDC entry — same nutrition profile "
                f"-> same score (data-driven, not engine artefact)"
                if len(products) > 1 else "single product"
            ),
        }
        for fdc_id, products in sorted(fdc_clusters.items(), key=lambda x: -len(x[1]))
    ]

    # ── EV-050 fix verification ────────────────────────────────────────────────
    ev050_all_fixed = all(r["ev050_fixed"] for r in ev050_resolved) if ev050_resolved else False

    # ── Build summary ─────────────────────────────────────────────────────────
    summary = {
        "run_id":         RUN_ID,
        "task":           TASK_ID,
        "phase":          "B.2",
        "generated_utc":  datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_version": "proto_v0 / algorithm_version 0.4.1",
        "engine_flags": {
            "BARI_RECAL_P0":    os.environ.get("BARI_RECAL_P0", "off"),
            "BARI_GLASSBOX_W4": "on",
            "BARI_GLASSBOX_D5D6": os.environ.get("BARI_GLASSBOX_D5D6", "off"),
        },
        "engine_fixes_active": {
            "EV_047_kcal_ceiling_800": True,
            "EV_048_sat_fat_cap_endemic_wff_fraction_0_50": True,
            "EV_050_natural_dairy_trans_exempt": True,
        },
        "bsip1_source":    str(BSIP1_PATH),
        "total_products":  len(raw_list),
        "pipeline_errors": len(errors),
        "corpus_breakdown": {
            "confirmed_products": len(confirmed_traces),
            "candidate_products": len(candidate_traces),
            "confirmed_note": "canonical_trust_level=high (original BSIP0 scraped, nutrition from label)",
            "candidate_note": "canonical_trust_level=low (enriched via OFF or USDA FDC; confidence ceiling applies; QA promotion required)",
        },
        "grade_distribution": all_grade_dist,
        "score_range": all_score_range,
        "confirmed_products": {
            "grade_distribution": confirmed_dist,
            "score_range":        confirmed_range,
        },
        "candidate_products": {
            "grade_distribution":      candidate_dist,
            "score_range":             candidate_range,
            "confidence_ceiling_note": (
                "trust_level=low deducts 10 confidence points. Combined with other "
                "deductions (nova_confidence=low), most candidates land at confidence<40 "
                "-> ceiling=50 (insufficient_data grade). A product with OFF-sourced "
                "ingredient data AND full nutrition may avoid this if nova_confidence lifts."
            ),
        },
        "sat_fat_caps_fired":      sat_fat_caps_fired,
        "sat_fat_caps_gated_ev048": sat_fat_caps_gated,
        "sat_fat_note": (
            "EV-048: ISRAELI_RED_LABEL_1_SAT_FAT cap suppressed for whole_food_fat products "
            "where sat_fat/fat >= 0.50. Plain dairy butter is exempt; emulsified spreads that "
            "fail this fraction threshold still fire the cap."
        ),
        "trans_fat_vetoes_fired": trans_fat_vetoes_fired,
        "trans_fat_note": (
            "EV-050: TRANS_FAT_VETO exempt for whole_food_fat products with no PHVO markers. "
            "Natural dairy trans fat (CLA/vaccenic acid) reported by USDA FDC / OFF must not "
            "trigger the industrial-trans veto. Expect 0 vetoes after EV-050 fix."
        ),
        "ev050_fix_verification": {
            "previously_0_E_products": len(EV050_AFFECTED_PIDS),
            "all_now_fixed": ev050_all_fixed,
            "detail": ev050_resolved,
        },
        "floor_activations":           floor_activations,
        "FLOOR_CAP_INTERACTION_count": len(floor_cap_interactions),
        "FLOOR_CAP_INTERACTION_detail": floor_cap_interactions,
        "FLOOR_CAP_INTERACTION_note": (
            "Expected: only salted butters with ISRAELI_RED_LABELS_2_PLUS + HIGH_SODIUM_700MG_PLUS "
            "where floor=50 overrides remaining cap. Sat-fat cap should not appear here (EV-048)."
        ),
        "additive_spread_differentiation": additive_spread_check,
        "routing_check": {
            "all_whole_food_fat": len(misroutes) == 0,
            "misrouted":         misroutes,
        },
        "fdc_source_clusters": fdc_cluster_summary,
        "per_product_table":   per_product_table,
        "error_detail":        errors,
    }

    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Console report ────────────────────────────────────────────────────────
    log.info("")
    log.info("=== Run %s complete ===", RUN_ID)
    log.info("  Total: %d  Confirmed: %d  Candidate: %d  Errors: %d",
             len(raw_list), len(confirmed_traces), len(candidate_traces), len(errors))
    log.info("  --- All products ---")
    log.info("  Grade distribution: %s", all_grade_dist)
    log.info("  Score range: %s-%s  mean=%s",
             all_score_range["min"], all_score_range["max"], all_score_range["mean"])
    log.info("  --- Confirmed (high-trust) ---")
    log.info("  Grade distribution: %s", confirmed_dist)
    log.info("  Score range: %s-%s  mean=%s",
             confirmed_range["min"], confirmed_range["max"], confirmed_range["mean"])
    log.info("  --- Candidate (low-trust, enriched) ---")
    log.info("  Grade distribution: %s", candidate_dist)
    log.info("  Score range: %s-%s  mean=%s",
             candidate_range["min"], candidate_range["max"], candidate_range["mean"])
    log.info("")
    log.info("  Floor activations: %d", floor_activations)
    log.info("  Sat-fat caps fired: %d  (gated by EV-048: %d)", sat_fat_caps_fired, sat_fat_caps_gated)
    log.info("  Trans fat vetoes fired: %d  (expect 0 after EV-050)", trans_fat_vetoes_fired)
    log.info("  FLOOR_CAP_INTERACTION count: %d", len(floor_cap_interactions))
    if floor_cap_interactions:
        for fci in floor_cap_interactions:
            log.info("    FLOOR_CAP_INTERACTION: %s (%s)", fci.get("name"), fci.get("flags"))
    log.info("  EV-050 fix: %d previously-0/E products — all_fixed=%s",
             len(EV050_AFFECTED_PIDS), ev050_all_fixed)
    for r in ev050_resolved:
        log.info("    %s  %s -> %s/%s  fixed=%s",
                 r["pid"][-20:], r["name"][:30], r["score"], r["grade"], r["ev050_fixed"])
    log.info("  Additive spread check: %s", additive_spread_check)
    if misroutes:
        log.warning("  Misroutes: %s", [m["name"] for m in misroutes])
    log.info("  Summary: %s", SUMMARY_PATH)

    # ── Per-product quick table ────────────────────────────────────────────────
    log.info("")
    log.info("  Per-product table (sorted by score desc):")
    log.info("  %-14s  %-36s  %-20s  %5s  %5s  %-11s  %-12s",
             "barcode", "name", "brand", "score", "grade", "conf_band", "vstatus")
    for row in per_product_table:
        log.info("  %-14s  %-36s  %-20s  %5s  %5s  %-11s  %-12s",
                 row["barcode"], (row["name"] or "")[:36], (row["brand"] or "")[:20],
                 row["score"], row["grade"], row["confidence_band"], row["verification_status"])

    return summary


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
