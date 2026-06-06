"""
BSIP2 Prototype v0 — Butter Batch Runner (butter_run_002) — TASK-191 Phase B.

Input:   C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_merged.json
         (39 products: 16 confirmed high-trust + 23 candidate low-trust enriched)

Output:  C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_002\\products\\
         + C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_002_summary.json

Engine flags: BARI_RECAL_P0=off, BARI_GLASSBOX_W4=on (default-on), BARI_GLASSBOX_D5D6=off

What changed since run_001:
  - EV-047: KCAL_PLAUSIBLE_UPPER raised to 800 (butter 725-745 kcal is now plausible).
  - EV-048: ISRAELI_RED_LABEL_1_SAT_FAT cap suppressed when category==whole_food_fat
    AND sat_fat/fat >= 0.50. Plain dairy butter is exempt; emulsified spreads are not.
  - All 39 products now have nutrition data (run_001 had 23 products as insufficient).

Corpus classification:
  - "confirmed" = canonical_trust_level == "high" (16 products, original BSIP0 scraped)
  - "candidate"  = canonical_trust_level == "low"  (23 products, enriched via OFF/FDC)
    Candidate scores carry a confidence ceiling from trust_level=low deduction.
    Do NOT promote candidate scores to verified — QA gate required.

FDC source clustering note (data-driven, not an engine artefact):
  Multiple products share the same USDA FDC SR Legacy entry because they are the same
  type (e.g. unsalted butter → fdc_id=173430). Identical source → identical nutrition
  profile → identical score. See fdc_source_clusters in the summary.
"""
import sys
import json
import pathlib
import logging
import datetime
import statistics

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

BSIP1_PATH  = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs\butter_bsip1_merged.json")
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_002")
SUMMARY_PATH = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_002_summary.json")
RUN_ID      = "butter_run_002"
TASK_ID     = "TASK-191"

WHOLE_FOOD_FAT_EXPECTED = {"whole_food_fat"}

# Products known to be additive-heavy emulsified spreads — used for differentiation check.
ADDITIVE_SPREAD_BARCODES = {"7290108507997"}


def is_confirmed(product: dict) -> bool:
    """True for original BSIP0 scraped products (high trust = confirmed_per_100g)."""
    return product.get("canonical_trust_level") == "high"


def get_fdc_source_id(product: dict) -> str | None:
    """Extract FDC fdc_id from enrichment report notes if present in corpus."""
    prov = product.get("ingestion_provenance") or {}
    source = prov.get("source") or ""
    if "usda_fdc" in source or "fdc" in source.lower():
        # Try to get the fdc_id from enrichment notes embedded in the product
        notes = product.get("enrichment_notes") or []
        for note in notes:
            if "fdc_id=" in note:
                import re
                m = re.search(r"fdc_id=(\d+)", note)
                if m:
                    return m.group(1)
    return None


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

    traces       = []
    errors       = []
    misroutes    = []

    for product in raw_list:
        product["_source_path"] = str(BSIP1_PATH)
        product["_load_errors"] = validate_product(product)

        pid  = product.get("canonical_product_id", "unknown")
        name = product.get("canonical_name_he", "")
        conf = "confirmed" if is_confirmed(product) else "candidate"

        try:
            trace = run_pipeline(product)
            # Tag the trace with corpus classification for summary differentiation
            trace["_corpus_class"] = conf
            trace["_barcode"]      = product.get("barcode", "")
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)

            cat   = trace.get("category")
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            suff  = trace.get("data_sufficiency")

            if cat not in WHOLE_FOOD_FAT_EXPECTED:
                misroutes.append({"pid": pid, "name": name, "routed_to": cat, "expected": "whole_food_fat"})
                log.warning("  MISROUTE: %s → %s", name, cat)
            else:
                log.info("  %-12s  %-10s  %s | %s/%s | suff=%s",
                         conf, pid[-20:], name[:28], score, grade, suff)

        except Exception as e:
            log.error("  PIPELINE ERROR for %s (%s): %s", pid, name, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "name": name, "error": str(e)})

    # ── Aggregate stats ────────────────────────────────────────────────────────
    confirmed_traces = [t for t in traces if t.get("_corpus_class") == "confirmed"]
    candidate_traces = [t for t in traces if t.get("_corpus_class") == "candidate"]

    def grade_dist(trace_list: list) -> dict:
        d: dict[str, int] = {}
        for t in trace_list:
            g = t.get("grade_estimate") or "INSUFFICIENT"
            d[g] = d.get(g, 0) + 1
        return dict(sorted(d.items()))

    def score_range(trace_list: list) -> dict:
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

    all_grade_dist = grade_dist(traces)
    all_score_range = score_range(traces)

    confirmed_dist   = grade_dist(confirmed_traces)
    confirmed_range  = score_range(confirmed_traces)
    candidate_dist   = grade_dist(candidate_traces)
    candidate_range  = score_range(candidate_traces)

    # ── Floor activations ─────────────────────────────────────────────────────
    floor_activations = sum(
        1 for t in traces
        if any("floor_type" in f for f in (t.get("floors_applied") or []))
    )

    # ── Sat-fat cap fires ─────────────────────────────────────────────────────
    sat_fat_caps_fired = sum(
        1 for t in traces
        if any("SAT_FAT" in (c.get("rule") or "") for c in (t.get("caps_applied") or []))
    )

    # Distinguish: how many caps were considered-but-gated (EV-048) vs fired
    sat_fat_caps_gated = 0
    for t in traces:
        for c in (t.get("caps_considered") or []):
            if "ISRAELI_RED_LABEL_1_SAT_FAT" in (c.get("rule") or ""):
                note = c.get("note") or ""
                if "EV-048 endemic gate" in note and not c.get("fired", True):
                    sat_fat_caps_gated += 1
                    break

    # ── FLOOR_CAP_INTERACTION ─────────────────────────────────────────────────
    floor_cap_interactions = [
        {"pid": t.get("input_reference", {}).get("canonical_product_id"),
         "name": t.get("input_reference", {}).get("product_name_he"),
         "flags": [f for f in (t.get("unresolved_flags") or []) if "FLOOR_CAP_INTERACTION" in f]}
        for t in traces
        if any("FLOOR_CAP_INTERACTION" in (f or "") for f in (t.get("unresolved_flags") or []))
    ]

    # ── Additive spread differentiation check ─────────────────────────────────
    additive_spread_traces = [
        t for t in traces
        if t.get("_barcode") in ADDITIVE_SPREAD_BARCODES
    ]
    additive_spread_check = []
    plain_butter_scores   = [
        t["final_score_estimate"] for t in confirmed_traces
        if t.get("final_score_estimate") is not None
        and t.get("_barcode") not in ADDITIVE_SPREAD_BARCODES
    ]
    for t in additive_spread_traces:
        additive_spread_check.append({
            "barcode": t.get("_barcode"),
            "name": t.get("input_reference", {}).get("product_name_he"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "caps_applied": [c.get("rule") for c in (t.get("caps_applied") or [])],
            "differentiated_below_plain_butter": (
                t.get("final_score_estimate") is not None
                and plain_butter_scores
                and t["final_score_estimate"] < min(plain_butter_scores)
            ),
        })

    # ── FDC source clustering ──────────────────────────────────────────────────
    # Build from enrichment report data (stored in product records via ingestion_provenance)
    # Map fdc_id → list of product barcodes using the enrichment report we already read
    enrichment_report_path = pathlib.Path(
        r"C:\Bari\02_products\butter\bsip1_outputs\butter_enrichment_report_20260605.json"
    )
    fdc_clusters: dict[str, list] = {}
    if enrichment_report_path.exists():
        er = json.loads(enrichment_report_path.read_text(encoding="utf-8"))
        for p in er.get("products", []):
            fdc_result = p.get("fdc_result") or ""
            if "fdc_id=" in fdc_result:
                import re
                m = re.search(r"fdc_id=(\d+)", fdc_result)
                if m:
                    fdc_id = m.group(1)
                    if fdc_id not in fdc_clusters:
                        fdc_clusters[fdc_id] = []
                    fdc_clusters[fdc_id].append({
                        "barcode": p["barcode"],
                        "name": p["name"],
                        "brand": p.get("brand"),
                        "fdc_description": re.search(r"'(.+?)'", fdc_result).group(1) if "'" in fdc_result else fdc_result,
                    })

    fdc_cluster_summary = [
        {
            "fdc_id": fdc_id,
            "product_count": len(products),
            "description": products[0]["fdc_description"] if products else "",
            "products": products,
            "note": f"{len(products)} products share this USDA FDC entry — same nutrition profile → same score (data-driven, not engine artefact)"
                    if len(products) > 1 else "single product",
        }
        for fdc_id, products in sorted(fdc_clusters.items(), key=lambda x: -len(x[1]))
    ]

    # ── Build summary ─────────────────────────────────────────────────────────
    summary = {
        "run_id":     RUN_ID,
        "task":       TASK_ID,
        "phase":      "B",
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_version": "proto_v0 / algorithm_version 0.4.1",
        "engine_flags": {
            "BARI_RECAL_P0":    os.environ.get("BARI_RECAL_P0", "off"),
            "BARI_GLASSBOX_W4": "on",
            "BARI_GLASSBOX_D5D6": os.environ.get("BARI_GLASSBOX_D5D6", "off"),
        },
        "engine_fixes_active": {
            "EV_047_kcal_ceiling_800": True,
            "EV_048_sat_fat_cap_endemic_wff_fraction_0_50": True,
        },
        "bsip1_source": str(BSIP1_PATH),
        "total_products": len(raw_list),
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
            "score_range": confirmed_range,
        },
        "candidate_products": {
            "grade_distribution": candidate_dist,
            "score_range": candidate_range,
            "confidence_ceiling_note": (
                "trust_level=low deducts 10 confidence points. Combined with other "
                "deductions (nova_confidence=low), most candidates land at confidence<40 "
                "→ ceiling=50 (insufficient_data grade). A product with OFF-sourced "
                "ingredient data AND full nutrition may avoid this if nova_confidence lifts."
            ),
        },
        "sat_fat_caps_fired": sat_fat_caps_fired,
        "sat_fat_caps_gated_ev048": sat_fat_caps_gated,
        "sat_fat_note": (
            "EV-048: ISRAELI_RED_LABEL_1_SAT_FAT cap suppressed for whole_food_fat products "
            "where sat_fat/fat >= 0.50. Plain dairy butter is exempt; emulsified spreads that "
            "fail this fraction threshold still fire the cap. Regulatory annotation in "
            "regulatory_quality dimension is NOT gated."
        ),
        "floor_activations": floor_activations,
        "FLOOR_CAP_INTERACTION_count": len(floor_cap_interactions),
        "FLOOR_CAP_INTERACTION_detail": floor_cap_interactions,
        "FLOOR_CAP_INTERACTION_note": (
            "Expect 0 for plain dairy butter after EV-048 fix. "
            "A non-zero count here means the sat-fat cap still fired AND the floor overrode it."
        ),
        "additive_spread_differentiation": additive_spread_check,
        "routing_check": {
            "all_whole_food_fat": len(misroutes) == 0,
            "misrouted": misroutes,
        },
        "fdc_source_clusters": fdc_cluster_summary,
        "error_detail": errors,
    }

    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Console report ────────────────────────────────────────────────────────
    log.info("")
    log.info("=== Run %s complete ===", RUN_ID)
    log.info("  Total: %d  Confirmed: %d  Candidate: %d  Errors: %d",
             len(raw_list), len(confirmed_traces), len(candidate_traces), len(errors))
    log.info("  --- All products ---")
    log.info("  Grade distribution: %s", all_grade_dist)
    log.info("  Score range: %s–%s  mean=%s",
             all_score_range["min"], all_score_range["max"], all_score_range["mean"])
    log.info("  --- Confirmed (high-trust) ---")
    log.info("  Grade distribution: %s", confirmed_dist)
    log.info("  Score range: %s–%s  mean=%s",
             confirmed_range["min"], confirmed_range["max"], confirmed_range["mean"])
    log.info("  --- Candidate (low-trust, enriched) ---")
    log.info("  Grade distribution: %s", candidate_dist)
    log.info("  Score range: %s–%s  mean=%s",
             candidate_range["min"], candidate_range["max"], candidate_range["mean"])
    log.info("")
    log.info("  Floor activations: %d", floor_activations)
    log.info("  Sat-fat caps fired: %d  (gated by EV-048: %d)", sat_fat_caps_fired, sat_fat_caps_gated)
    log.info("  FLOOR_CAP_INTERACTION count: %d", len(floor_cap_interactions))
    if floor_cap_interactions:
        for fci in floor_cap_interactions:
            log.warning("    FLOOR_CAP_INTERACTION: %s (%s) — %s", fci["pid"], fci["name"], fci["flags"])
    log.info("  Additive spread check: %s", additive_spread_check)
    if misroutes:
        log.warning("  Misroutes: %s", [m["name"] for m in misroutes])
    if fdc_cluster_summary:
        log.info("  FDC source clusters:")
        for cl in fdc_cluster_summary:
            if cl["product_count"] > 1:
                log.info("    fdc_id=%s (%s) → %d products", cl["fdc_id"], cl["description"], cl["product_count"])
    log.info("  Summary: %s", SUMMARY_PATH)

    return summary


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
