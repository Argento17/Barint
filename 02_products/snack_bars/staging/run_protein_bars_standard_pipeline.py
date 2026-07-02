"""
STAGING PIPELINE — Protein Bars Standard Path Rebuild
TASK: Rebuild protein-bars scoring onto the STANDARD pipeline.

Purpose:
  - Produce per-product bsip2_trace.json files (the standard format)
  - Produce bsip1_pb_{barcode}.json files (BSIP1-compatible records)
  - Run generate_page.py against those to produce a STAGING frontend JSON
  - Measure vs live protein_bars_frontend_v1.json by barcode

GUARDS:
  - Does NOT overwrite any file under bari-web/src/data/comparisons/
  - All output goes to C:\\Bari\\02_products\\snack_bars\\staging\\run_pb_standard_<timestamp>\\
  - Uses BARI_PROTEIN_BAR_V1=on (same scoring flags as live)
  - Same corpus: protein_combined_corpus_task365_33_20260621_fix.json
  - Nothing is published

This is a STAGING/MEASUREMENT run that prepares the co-sign packet.
"""
from __future__ import annotations

import sys
import os
import json
import pathlib
import datetime
import hashlib
import logging
import subprocess
import shutil

# ── Engine path ───────────────────────────────────────────────────────────────
_BSIP2_SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(_BSIP2_SRC))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, RECAL_P0_ON
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade, PROTEIN_BAR_LENS_ON

# Import protein_bar specific functions from the original runner
# (same file, same logic — we reuse the functions, not re-implement them)
_pb_runner = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_protein_bars_task365.py")
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("pb_runner", _pb_runner)
_pb_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_pb_mod)

detect_protein_bar_signals = _pb_mod.detect_protein_bar_signals
apply_protein_bar_lens = _pb_mod.apply_protein_bar_lens
_adapt_product_for_engine = _pb_mod._adapt_product_for_engine

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
CORPUS_PATH = pathlib.Path(
    r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json"
)
STAGING_BASE = pathlib.Path(r"C:\Bari\02_products\snack_bars\staging")
LIVE_V1_PATH = pathlib.Path(
    r"C:\Bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json"
)
PAGE_GENERATOR = pathlib.Path(
    r"C:\Bari\03_operations\page_generator\generate_page.py"
)

RUN_TS = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
RUN_ID = f"pb_standard_staging_{RUN_TS}"
RUN_DIR = STAGING_BASE / f"run_pb_standard_{RUN_TS}"

# Subdirs following the standard layout
BSIP1_DIR = RUN_DIR / "bsip1_corpus"   # bsip1_pb_{barcode}.json files
BSIP2_DIR = RUN_DIR / "bsip2_products" # products/{product_id}/bsip2_trace.json
STAGING_OUT = RUN_DIR / "staging_protein_bars_frontend.json"
STAGING_CONFIG = RUN_DIR / "staging_protein_bars_config.json"
RUN_RECORD_PATH = RUN_DIR / "run_record.json"


def sha256_path(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adapt_corpus_to_bsip1(product: dict) -> dict:
    """
    Convert a protein_combined_corpus record to a BSIP1-compatible record.

    The corpus uses:
      name -> canonical_name_he + product_name_he
      nutrition_per_100g -> normalized_nutrition_per_100g
      ingredients_full -> ingredients_text_he + ingredients_raw
      barcode -> barcode
      brand -> brand
      image_url -> image_url

    The BSIP1 format adds:
      canonical_product_id = "bsip1_pb_{barcode}"
      schema_version = "bsip1_v0_1"
      source_retailers = ["shufersal"]
    """
    barcode = str(product.get("barcode", ""))
    return {
        "canonical_product_id": f"bsip1_pb_{barcode}",
        "barcode": barcode,
        "canonical_name_he": product.get("name", ""),
        "product_name_he": product.get("name", ""),
        "brand": product.get("brand", ""),
        "image_url": product.get("image_url", ""),
        "source_retailers": ["shufersal"],
        "normalized_nutrition_per_100g": product.get("nutrition_per_100g", {}),
        "ingredients_text_he": product.get("ingredients_full", ""),
        "ingredients_raw": product.get("ingredients_full", ""),
        "schema_version": "bsip1_v0_1",
        "confidence_band": "high",
        # Carry through original fields for completeness
        "_protein_corpus_format": product.get("format", "bar"),
        "_weight_g": product.get("weight_g"),
        "_shufersal_code": product.get("shufersal_code"),
        "_provenance": product.get("provenance"),
        "_gate_verdict": product.get("gate_verdict"),
    }


def build_full_trace(product_bsip1: dict, base_result: dict, pb_signals: dict, lens_result: dict) -> dict:
    """
    Build a complete bsip2_trace.json that:
    1. Contains all standard BSIP2 fields (from assemble_trace)
    2. Has the protein_bar_lens fields injected (so score==trace round-trip holds)
    3. Uses the LENS final_score_estimate (not base engine score)
    """
    # Build signals for assemble_trace — use the adapted product
    adapted = _adapt_product_for_engine(product_bsip1)
    signals = extract_signals(adapted)
    cat_result = classify_category(adapted)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(adapted, l3)
    eval_result = assign_evaluation_scope(adapted, cat_result["category"])

    # Standard trace from base engine (before lens)
    trace = assemble_trace(
        product=product_bsip1,
        signals=signals,
        cat_result=cat_result,
        nova_result=nova_result,
        eval_result=eval_result,
        score_result=base_result,
    )

    # Inject protein_bar_lens fields — overwrite the score fields with lens values
    trace["protein_bar_lens_active"] = lens_result.get("protein_bar_lens_active")
    trace["protein_bar_signals"] = pb_signals
    trace["protein_bar_caps"] = lens_result.get("protein_bar_caps", [])
    trace["protein_bar_penalties"] = lens_result.get("protein_bar_penalties", [])
    trace["effective_pb_cap"] = lens_result.get("effective_pb_cap")
    trace["score_after_pb_cap"] = lens_result.get("score_after_pb_cap")
    trace["total_pb_penalty"] = lens_result.get("total_pb_penalty")
    trace["weighted_dimension_score_protein_bar"] = lens_result.get("weighted_dimension_score_protein_bar")
    trace["cond2_recal_p0_on"] = lens_result.get("cond2_recal_p0_on")
    trace["cond2_double_fire_check"] = lens_result.get("cond2_double_fire_check")
    trace["cond2_note"] = lens_result.get("cond2_note")
    trace["protein_gate"] = lens_result.get("protein_gate")

    # Overwrite the final score fields with LENS values (this is the score==trace round-trip)
    trace["final_score_estimate"] = lens_result.get("final_score_estimate")
    trace["grade_estimate"] = lens_result.get("grade_estimate")

    # Also update dimension_scores and weights to the lens-adjusted values
    # (so the trace reflects what actually produced the score)
    if lens_result.get("dimension_scores"):
        trace["dimension_scores"] = lens_result["dimension_scores"]
    if lens_result.get("dimension_weights"):
        trace["dimension_weights"] = lens_result["dimension_weights"]
    if lens_result.get("dimension_notes"):
        trace["dimension_notes"] = lens_result["dimension_notes"]

    return trace


def main():
    log.info(f"STAGING RUN: {RUN_ID}")
    log.info(f"BARI_PROTEIN_BAR_V1={os.environ.get('BARI_PROTEIN_BAR_V1', 'NOT SET')}")
    log.info(f"PROTEIN_BAR_LENS_ON={PROTEIN_BAR_LENS_ON}")
    log.info(f"RECAL_P0_ON={RECAL_P0_ON}")

    if not PROTEIN_BAR_LENS_ON:
        log.error("ABORT: BARI_PROTEIN_BAR_V1 must be ON for this staging run.")
        log.error("Set: $env:BARI_PROTEIN_BAR_V1='on'")
        sys.exit(1)

    # ── Create dirs ───────────────────────────────────────────────────────────
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    BSIP1_DIR.mkdir(parents=True, exist_ok=True)
    BSIP2_DIR.mkdir(parents=True, exist_ok=True)
    log.info(f"Staging run dir: {RUN_DIR}")

    # ── Load corpus ───────────────────────────────────────────────────────────
    corpus_raw = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    products = corpus_raw["products"]
    corpus_sha = sha256_path(CORPUS_PATH)
    log.info(f"Corpus: {len(products)} products, sha256={corpus_sha[:12]}...")

    # ── Step 1: Write bsip1_pb_{barcode}.json for each product ───────────────
    log.info("Step 1: Writing BSIP1-compatible records...")
    bsip1_records: dict[str, dict] = {}
    for product in products:
        bsip1_rec = adapt_corpus_to_bsip1(product)
        barcode = bsip1_rec["barcode"]
        bsip1_records[barcode] = bsip1_rec
        fname = f"bsip1_pb_{barcode}.json"
        (BSIP1_DIR / fname).write_text(
            json.dumps(bsip1_rec, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    log.info(f"  Written {len(bsip1_records)} BSIP1 records to {BSIP1_DIR}")

    # ── Step 2: Score each product + write per-product bsip2_trace.json ──────
    log.info("Step 2: Scoring + writing per-product bsip2_trace.json files...")
    scored_list: list[dict] = []
    trace_write_errors: list[str] = []

    for product in products:
        barcode = str(product.get("barcode", ""))
        bsip1_rec = bsip1_records[barcode]
        adapted = _adapt_product_for_engine(bsip1_rec)
        nn = adapted.get("normalized_nutrition_per_100g", {})

        try:
            signals = extract_signals(adapted)
            cat_result = classify_category(adapted)
            l3 = signals["L3_inferred_classifications"]
            nova_result = infer_nova(adapted, l3)
            eval_result = assign_evaluation_scope(adapted, cat_result["category"])
            base_result = score_product(adapted, signals, cat_result, nova_result, eval_result)

            # Detect protein_bar signals and apply lens
            pb_signals = detect_protein_bar_signals(adapted, nn)
            lens_result = apply_protein_bar_lens(base_result, adapted, nn, pb_signals)

            # Build full trace with lens data embedded
            trace = build_full_trace(bsip1_rec, base_result, pb_signals, lens_result)

            # Write the trace to the standard per-product subdir
            product_id = f"bsip1_pb_{barcode}"
            product_dir = BSIP2_DIR / "products" / product_id
            product_dir.mkdir(parents=True, exist_ok=True)
            trace_path = product_dir / "bsip2_trace.json"
            trace_path.write_text(
                json.dumps(trace, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            # Record for measurement
            scored_list.append({
                "barcode": barcode,
                "name": product.get("name", ""),
                "brand": product.get("brand", ""),
                "base_score": base_result.get("final_score_estimate"),
                "base_grade": base_result.get("grade_estimate"),
                "lens_score": lens_result.get("final_score_estimate"),
                "lens_grade": lens_result.get("grade_estimate"),
                "trace_path": str(trace_path),
                "protein_bar_signals": pb_signals,
                "lens_active": lens_result.get("protein_bar_lens_active"),
                "total_pb_penalty": lens_result.get("total_pb_penalty"),
                "effective_pb_cap": lens_result.get("effective_pb_cap"),
            })

        except Exception as exc:
            log.error(f"ERROR scoring {barcode}: {exc}")
            trace_write_errors.append(f"{barcode}: {exc}")

    log.info(f"  Scored {len(scored_list)}/{len(products)} products; errors={len(trace_write_errors)}")

    # ── Step 3: Write staging config for generate_page.py ────────────────────
    log.info("Step 3: Writing staging config...")
    staging_config = {
        "_comment": (
            f"STAGING CONFIG — protein_bars standard pipeline rebuild. "
            f"Run ID: {RUN_ID}. DO NOT deploy. "
            f"Corpus: protein_combined_corpus_task365_33_20260621_fix.json ({len(products)} products). "
            f"Scoring flags: BARI_PROTEIN_BAR_V1=on, all others off."
        ),
        "category": "protein_bars",
        "corpus_dirs": [str(BSIP1_DIR)],
        "run_products_dir": str(BSIP2_DIR / "products"),
        "baseline_json": str(LIVE_V1_PATH),
        "retailer_scope": ["shufersal"],
        "subpool_filter": None,
        "dedup": {
            "rule": "one_card_per_barcode",
            "keep": "highest_priority_corpus"
        },
        "scoring": {
            "flags": {
                "BARI_PROTEIN_BAR_V1": "on",
                "BARI_SHELF_RELATIVE_V1": "off",
                "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                "BARI_RECAL_P0": "off",
                "BARI_GRAD_SODIUM_V1": "off",
                "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
                "BARI_REDLABEL_V1": "off",
                "BARI_SODIUM_CEREAL": "off",
                "BARI_FAT_TECH_V1": "off",
                "BARI_GLASSBOX_W4": "off",
                "BARI_FIBER_FERMENT_V1": "off"
            },
            "_source": f"run_protein_bars_standard_pipeline.py (staging, run_id={RUN_ID})",
            "_corpus_path": str(CORPUS_PATH),
            "_corpus_sha256": corpus_sha
        },
        "exclusions": [],
        "extension_fields": [],
        "render_fields": [],
        "boundary_policy": r"C:\Bari\01_framework\governance\grade_boundary_policy_v1.json"
    }
    STAGING_CONFIG.write_text(
        json.dumps(staging_config, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    log.info(f"  Staging config written: {STAGING_CONFIG}")

    # ── Step 4: Run generate_page.py ─────────────────────────────────────────
    log.info("Step 4: Running generate_page.py against staging artifacts...")
    gen_result = subprocess.run(
        [
            sys.executable,
            str(PAGE_GENERATOR),
            "--config", str(STAGING_CONFIG),
            "--out", str(STAGING_OUT),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    log.info(f"  generate_page.py exit code: {gen_result.returncode}")
    if gen_result.stdout:
        for line in gen_result.stdout.strip().split("\n")[:30]:
            log.info(f"  [gen] {line}")
    if gen_result.stderr:
        for line in gen_result.stderr.strip().split("\n")[:20]:
            log.warning(f"  [gen-err] {line}")

    gen_ok = gen_result.returncode == 0
    if not gen_ok:
        log.warning("generate_page.py returned non-zero exit; continuing to measurement.")

    # ── Step 5: Load staging output and measure vs live v1 ───────────────────
    log.info("Step 5: Measuring staging vs live v1...")

    # Load live v1
    live_data = json.loads(LIVE_V1_PATH.read_text(encoding="utf-8"))
    live_products = live_data.get("products", [])
    live_by_barcode: dict[str, dict] = {str(p["barcode"]): p for p in live_products}
    log.info(f"  Live v1: {len(live_products)} products")

    # Load staging output (if generate_page succeeded)
    staging_products: list[dict] = []
    staging_by_barcode: dict[str, dict] = {}
    if STAGING_OUT.exists():
        staging_data = json.loads(STAGING_OUT.read_text(encoding="utf-8"))
        staging_products = staging_data.get("products", [])
        staging_by_barcode = {str(p["barcode"]): p for p in staging_products}
        log.info(f"  Staging output: {len(staging_products)} products")
    else:
        log.warning("  Staging output file not found — using scored_list for measurement")
        # Fall back to scored_list
        for s in scored_list:
            staging_by_barcode[s["barcode"]] = {
                "barcode": s["barcode"],
                "score": s["lens_score"],
                "grade": s["lens_grade"],
                "name": s["name"],
            }

    # Build per-barcode diff
    diff_table: list[dict] = []
    all_live_barcodes = set(live_by_barcode.keys())
    all_staging_barcodes = set(staging_by_barcode.keys())

    # Overlapping products
    overlap_barcodes = all_live_barcodes & all_staging_barcodes
    for bc in sorted(overlap_barcodes):
        live_p = live_by_barcode[bc]
        stg_p = staging_by_barcode[bc]
        v1_score = live_p.get("score")
        v2_score = stg_p.get("score")
        v1_grade = live_p.get("grade")
        v2_grade = stg_p.get("grade")
        delta = round(float(v2_score) - float(v1_score), 2) if (v2_score is not None and v1_score is not None) else None
        grade_move = None
        if v1_grade and v2_grade:
            grade_order = ["E", "D", "C", "B", "A", "S"]
            v1_idx = grade_order.index(v1_grade) if v1_grade in grade_order else -1
            v2_idx = grade_order.index(v2_grade) if v2_grade in grade_order else -1
            grade_move = v2_idx - v1_idx  # positive = up

        name = live_p.get("name") or stg_p.get("name") or ""
        diff_table.append({
            "barcode": bc,
            "name": name,
            "v1_score": v1_score,
            "v1_grade": v1_grade,
            "v2_score": v2_score,
            "v2_grade": v2_grade,
            "delta": delta,
            "grade_move": grade_move,
            "grade_move_direction": (
                "UP" if (grade_move and grade_move > 0)
                else "DOWN" if (grade_move and grade_move < 0)
                else "FLAT"
            ),
            "status": "OVERLAP",
        })

    # Live orphans (on live, not in corpus/staging)
    orphan_live = all_live_barcodes - all_staging_barcodes
    for bc in sorted(orphan_live):
        live_p = live_by_barcode[bc]
        diff_table.append({
            "barcode": bc,
            "name": live_p.get("name", ""),
            "v1_score": live_p.get("score"),
            "v1_grade": live_p.get("grade"),
            "v2_score": None,
            "v2_grade": None,
            "delta": None,
            "grade_move": None,
            "grade_move_direction": None,
            "status": "ORPHAN_LIVE",
        })

    # Corpus products not on live
    new_in_corpus = all_staging_barcodes - all_live_barcodes
    for bc in sorted(new_in_corpus):
        stg_p = staging_by_barcode[bc]
        diff_table.append({
            "barcode": bc,
            "name": stg_p.get("name", ""),
            "v1_score": None,
            "v1_grade": None,
            "v2_score": stg_p.get("score"),
            "v2_grade": stg_p.get("grade"),
            "delta": None,
            "grade_move": None,
            "grade_move_direction": None,
            "status": "CORPUS_NOT_LIVE",
        })

    # ── Step 6: Compute statistics ────────────────────────────────────────────
    overlap_rows = [r for r in diff_table if r["status"] == "OVERLAP"]
    deltas = [r["delta"] for r in overlap_rows if r["delta"] is not None]
    grade_movers_up = [r for r in overlap_rows if r.get("grade_move_direction") == "UP"]
    grade_movers_down = [r for r in overlap_rows if r.get("grade_move_direction") == "DOWN"]
    grade_movers_flat = [r for r in overlap_rows if r.get("grade_move_direction") == "FLAT"]

    mean_delta = round(sum(deltas) / len(deltas), 2) if deltas else None
    sorted_deltas = sorted(deltas) if deltas else []
    n = len(sorted_deltas)
    median_delta = sorted_deltas[n // 2] if (n % 2 == 1 and n > 0) else (
        (sorted_deltas[n // 2 - 1] + sorted_deltas[n // 2]) / 2 if n >= 2 else None
    )

    # Grade distribution before (live v1)
    from collections import Counter
    v1_dist = dict(Counter(p.get("grade") for p in live_products))
    v2_dist = dict(Counter(p.get("grade") for p in staging_products)) if staging_products else {}

    # ── Step 7: Score==Trace round-trip check ─────────────────────────────────
    log.info("Step 7: Score==Trace round-trip check...")
    roundtrip_results: list[dict] = []
    for s in scored_list:
        bc = s["barcode"]
        product_id = f"bsip1_pb_{bc}"
        trace_path = BSIP2_DIR / "products" / product_id / "bsip2_trace.json"
        if not trace_path.exists():
            roundtrip_results.append({"barcode": bc, "status": "TRACE_MISSING"})
            continue
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        trace_score = trace.get("final_score_estimate")
        computed_score = s["lens_score"]
        if trace_score == computed_score:
            roundtrip_results.append({"barcode": bc, "status": "PASS", "score": computed_score})
        else:
            roundtrip_results.append({
                "barcode": bc,
                "status": "FAIL",
                "computed": computed_score,
                "in_trace": trace_score
            })

    roundtrip_pass = sum(1 for r in roundtrip_results if r["status"] == "PASS")
    roundtrip_fail = sum(1 for r in roundtrip_results if r["status"] == "FAIL")
    roundtrip_overall = "PASS" if roundtrip_fail == 0 else "FAIL"

    # ── Build run record ──────────────────────────────────────────────────────
    run_record = {
        "run_id": RUN_ID,
        "run_type": "staging_standard_pipeline_rebuild",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "task": "TASK-374 (standard pipeline rebuild, co-sign packet)",
        "lens": "BARI_PROTEIN_BAR_V1",
        "lens_active": PROTEIN_BAR_LENS_ON,
        "recal_p0_on": RECAL_P0_ON,
        "corpus_path": str(CORPUS_PATH),
        "corpus_sha256": corpus_sha,
        "corpus_product_count": len(products),
        "scored_count": len(scored_list),
        "error_count": len(trace_write_errors),
        "trace_write_errors": trace_write_errors,
        "generate_page_exit_code": gen_result.returncode,
        "generate_page_ok": gen_ok,
        "staging_output": str(STAGING_OUT),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_DIR),
        "live_v1_path": str(LIVE_V1_PATH),
        "live_v1_product_count": len(live_products),
        "staging_product_count": len(staging_products),
        "roundtrip_check": {
            "status": roundtrip_overall,
            "pass": roundtrip_pass,
            "fail": roundtrip_fail,
            "total": len(roundtrip_results),
            "details": roundtrip_results,
        },
        "diff_summary": {
            "overlap_count": len(overlap_rows),
            "orphan_live_count": len(orphan_live),
            "corpus_not_live_count": len(new_in_corpus),
            "grade_movers_up": len(grade_movers_up),
            "grade_movers_down": len(grade_movers_down),
            "grade_movers_flat": len(grade_movers_flat),
            "mean_delta": mean_delta,
            "median_delta": round(median_delta, 2) if median_delta is not None else None,
            "min_delta": min(deltas) if deltas else None,
            "max_delta": max(deltas) if deltas else None,
        },
        "grade_distribution": {
            "live_v1": v1_dist,
            "staging": v2_dist,
        },
        "diff_table": sorted(diff_table, key=lambda x: (x["status"], -(x.get("delta") or 0))),
    }

    RUN_RECORD_PATH.write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    log.info(f"Run record written: {RUN_RECORD_PATH}")

    # ── Print summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 75)
    print(f"STAGING PIPELINE RESULT — {RUN_ID}")
    print("=" * 75)
    print(f"Corpus:              {len(products)} products (sha256={corpus_sha[:16]}...)")
    print(f"Scored:              {len(scored_list)} / {len(products)}")
    print(f"Errors:              {len(trace_write_errors)}")
    print(f"generate_page exit:  {gen_result.returncode} ({'OK' if gen_ok else 'FAIL'})")
    print(f"Staging output:      {len(staging_products)} products")
    print(f"Score==Trace RT:     {roundtrip_overall} ({roundtrip_pass}/{len(roundtrip_results)} PASS)")
    print()
    print(f"DIFF vs LIVE v1:")
    print(f"  Overlap:           {len(overlap_rows)}")
    print(f"  Orphan on live:    {len(orphan_live)}")
    print(f"  New in corpus:     {len(new_in_corpus)}")
    print(f"  Grade movers UP:   {len(grade_movers_up)}")
    print(f"  Grade movers DOWN: {len(grade_movers_down)}")
    print(f"  Grade movers FLAT: {len(grade_movers_flat)}")
    print(f"  Mean delta:        {mean_delta:+.2f}" if mean_delta is not None else "  Mean delta: N/A")
    print(f"  Median delta:      {round(median_delta, 2):+.2f}" if median_delta is not None else "  Median delta: N/A")
    print()
    print(f"Grade distribution:")
    print(f"  Live v1:   {v1_dist}")
    print(f"  Staging:   {v2_dist}")
    print()
    print(f"Per-barcode diff (OVERLAP, sorted by delta desc):")
    print(f"{'BC':<16} {'V1':>5}/Gr -> {'V2':>5}/Gr {'Delta':>7}  {'Dir':<5}  Name")
    print("-" * 90)
    for row in sorted(overlap_rows, key=lambda x: -(x.get("delta") or 0)):
        v1s = f"{row['v1_score']:>5.1f}" if row["v1_score"] is not None else "  N/A"
        v2s = f"{row['v2_score']:>5.1f}" if row["v2_score"] is not None else "  N/A"
        dlt = f"{row['delta']:+.2f}" if row["delta"] is not None else "   N/A"
        dir_ = row.get("grade_move_direction", "?")
        print(f"{row['barcode']:<16} {v1s}/{row.get('v1_grade','?'):<2} → {v2s}/{row.get('v2_grade','?'):<2} {dlt:>7}  {dir_:<5}  {row.get('name','')}")

    if orphan_live:
        print()
        print(f"ORPHAN_LIVE ({len(orphan_live)} — on live page, NOT in corpus):")
        for bc in sorted(orphan_live):
            p = live_by_barcode[bc]
            print(f"  {bc}  {p.get('score')}/{p.get('grade')}  {p.get('name','')}")

    if new_in_corpus:
        print()
        print(f"CORPUS_NOT_LIVE ({len(new_in_corpus)} — in corpus, NOT on live page):")
        for bc in sorted(new_in_corpus):
            p = staging_by_barcode[bc]
            print(f"  {bc}  {p.get('score')}/{p.get('grade')}  {p.get('name','')}")

    print()
    print(f"Artifacts:")
    print(f"  Staging frontend JSON: {STAGING_OUT}")
    print(f"  Run record:            {RUN_RECORD_PATH}")
    print(f"  BSIP1 corpus dir:      {BSIP1_DIR}")
    print(f"  BSIP2 traces dir:      {BSIP2_DIR}")
    print("=" * 75)

    return run_record


if __name__ == "__main__":
    main()
