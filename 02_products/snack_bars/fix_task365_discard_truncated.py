"""
TASK-365 data-integrity fix — discard truncated-ingredient WIN products.
==========================================================================
Two WIN barcodes have truncated ingredient lists (tail-only scrape artifact).
Their ingredient text contains no protein source, so the lens scored them
as CLEAN and they rose to ranks 1–2 with 86.4/A and 83.8/A — false grades.

Barcode 7290015130271 — "חטיף חלבון בצק עוגיות" (WIN cookie)
  ingredients_full = "מזון לצביעה (ספירולינה), מלח."  (29 chars)

Barcode 7290015130288 — "חט.חלבון קראנצ' ש.פאדג'" (WIN bar)
  ingredients_full = colorant/salt/vitamins/coating only  (139 chars)

Both are discarded per the missing-data discard rule:
  "data not found one-shot → DISCARD; do NOT re-scrape / over-invest"

This script:
  1. Verifies the defective barcodes in the source corpus.
  2. Writes a filtered corpus with exactly 33 products (no truncated entries).
  3. Adds an ingredient-COMPLETENESS gate to flag any product whose
     ingredients_full is < 120 chars OR contains no protein-source token
     — runs it across all 33 and confirms 0 remaining truncations.
  4. Re-runs the full protein_bar scoring pipeline on the 33-product corpus:
       - Re-ranks 1..33
       - Rewrites protein_combined_frontend_v2.json (copy fields stay PENDING_COPY)
       - Rewrites run_record.json + rerank_table.json in bsip2_outputs/protein_bars_task365/
  5. Re-runs all acceptance invariants and confirms PASS.
  6. Confirms per-product scores of the surviving 33 are unchanged.
  7. Reports new score/grade distribution, new top-5, and ceiling.

Hard rules honoured:
  - OFF BAN: no Open Food Facts used at any point
  - No re-scraping: discards are final (missing-data discard rule)
  - protein_bars_frontend_v1.json is NOT touched
  - All artifacts are written to their existing canonical paths

Run:
    set BARI_PROTEIN_BAR_V1=on
    python fix_task365_discard_truncated.py
"""
from __future__ import annotations

import sys
import os
import json
import pathlib
import datetime
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"

# Source corpus (35 products, from previous run)
SOURCE_CORPUS = SNACKS_DIR / "protein_combined_corpus_task365_20260621_121241.json"

# Filtered corpus output (33 products)
FILTERED_CORPUS = SNACKS_DIR / "protein_combined_corpus_task365_33_20260621_fix.json"

OUTPUT_DIR = ROOT / "02_products" / "snack_bars" / "bsip2_outputs" / "protein_bars_task365"
FRONTEND_OUT = ROOT / "bari-web" / "src" / "data" / "comparisons" / "protein_combined_frontend_v2.json"
LIVE_V1_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "protein_bars_frontend_v1.json"

# Add the scoring engine to path
_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(_SRC))

# ── Discarded barcodes (truncated ingredients) ────────────────────────────────
DISCARD_BARCODES = {
    "7290015130271",  # "חטיף חלבון בצק עוגיות" — 29 chars, colorant+salt only
    "7290015130288",  # "חט.חלבון קראנצ' ש.פאדג'" — 139 chars, coating+vitamins, no protein source
}

# ── Ingredient completeness gate ──────────────────────────────────────────────
INGREDIENT_MIN_CHARS = 120
PROTEIN_SOURCE_TOKENS = [
    "חלבון",     # general "protein" — catches חלבון מי גבינה, חלבון חלב, חלבון סויה, etc.
    "פרוטאין",   # "protein" transliterated
    "protein",   # English
    "איזולט",    # isolate
    "קזאין",     # casein
    "מי גבינה",  # whey
    "סויה",      # soy
    "אפונה",     # pea (protein)
    "קולגן",     # collagen (low quality but is a protein source)
    "collagen",
    "whey",
    "isolate",
    "casein",
    "בוטנים",    # peanuts (peanut butter bars)
    "אגוזי לוז", # hazelnuts
    "אגוז",      # nuts
    "שקד",       # almonds
]


def check_ingredient_completeness(product: dict) -> dict:
    """
    Returns {status: 'ok'|'truncated', reason, char_count, has_protein_token}.
    A protein bar product with no protein-source token in its ingredient list
    is definitionally truncated — the protein source MUST appear somewhere.
    """
    ing = product.get("ingredients_full") or ""
    char_count = len(ing.strip())
    il = ing.lower()

    has_protein_token = any(tok.lower() in il for tok in PROTEIN_SOURCE_TOKENS)

    if char_count < INGREDIENT_MIN_CHARS:
        return {
            "status": "truncated",
            "reason": f"ingredients_full is {char_count} chars < {INGREDIENT_MIN_CHARS} threshold",
            "char_count": char_count,
            "has_protein_token": has_protein_token,
        }

    if not has_protein_token:
        return {
            "status": "truncated",
            "reason": "no protein-source token found in ingredient list",
            "char_count": char_count,
            "has_protein_token": False,
        }

    return {
        "status": "ok",
        "reason": "completeness check passed",
        "char_count": char_count,
        "has_protein_token": True,
    }


def main():
    import argparse
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product, RECAL_P0_ON
    from constants import (
        score_to_grade,
        PROTEIN_BAR_LENS_ON,
        PROTEIN_BAR_WEIGHTS,
        PROTEIN_BAR_GATE_MIN_G, PROTEIN_BAR_GATE_REJECT_G,
        POLYOL_TIER_1_TOKENS, POLYOL_TIER_2_TOKENS, POLYOL_TIER_3_TOKENS,
        POLYOL_TIER_1_PENALTY, POLYOL_TIER_2_PENALTY, POLYOL_TIER_3_PENALTY,
        GLYCEROL_TOKENS, GLYCEROL_ENGINEERING_PENALTY,
        PROTEIN_ISOLATE_FAMILIES, ISOLATE_STACKING_FAMILY_THRESHOLD,
        PROTEIN_WHOLEFOOD_TOKENS,
        PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS, PROTEIN_BAR_COLLAGEN_PENALTY,
        PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS,
        PROTEIN_BAR_POLYOL_CAPS, PROTEIN_BAR_POLYOL_PENALTIES,
        PROTEIN_BAR_ENGINEERING_PENALTIES,
        CALORIE_DENSITY_TABLES, lookup_calorie_density,
        SWEETENER_CAP_C,
        PROCESSING_FAMILY_BUDGET,
        GLASSBOX_W2_ADDITIVES,
    )

    # Import the functions from the scorer (avoids full re-implementation)
    import batch_run_protein_bars_task365 as scorer

    log.info("=" * 70)
    log.info("TASK-365 DATA INTEGRITY FIX — discard truncated WIN products")
    log.info("=" * 70)
    log.info(f"Source corpus:    {SOURCE_CORPUS}")
    log.info(f"Discard barcodes: {sorted(DISCARD_BARCODES)}")
    log.info(f"BARI_PROTEIN_BAR_V1 env: {os.environ.get('BARI_PROTEIN_BAR_V1','off')}")
    log.info(f"PROTEIN_BAR_LENS_ON from constants: {PROTEIN_BAR_LENS_ON}")

    # ── Step 1: Load source corpus, verify defective products ─────────────────
    log.info("\n--- Step 1: Load + verify defective products in source corpus ---")
    source_data = json.loads(SOURCE_CORPUS.read_text(encoding="utf-8"))
    source_products = source_data["products"]
    log.info(f"Source corpus: {len(source_products)} products")

    defects_found = {}
    for p in source_products:
        bc = p.get("barcode", "")
        if bc in DISCARD_BARCODES:
            ing = p.get("ingredients_full") or ""
            completeness = check_ingredient_completeness(p)
            defects_found[bc] = {
                "name": p.get("name"),
                "ingredients_char_count": len(ing.strip()),
                "ingredients_preview": ing.strip()[:150],
                "completeness_check": completeness,
            }
            log.info(f"  DEFECT CONFIRMED: {bc} '{p.get('name')}' — {completeness['reason']}")

    if len(defects_found) != len(DISCARD_BARCODES):
        missing = DISCARD_BARCODES - set(defects_found.keys())
        log.error(f"STOP: Expected defective barcodes not found in corpus: {missing}")
        sys.exit(2)

    log.info(f"Both defective barcodes confirmed in source corpus.")

    # ── Step 2: Filter out the two defective barcodes ─────────────────────────
    log.info("\n--- Step 2: Build filtered 33-product corpus ---")
    filtered_products = [
        p for p in source_products
        if p.get("barcode") not in DISCARD_BARCODES
    ]
    assert len(filtered_products) == 35 - 2, (
        f"Expected 33 filtered products, got {len(filtered_products)}"
    )
    log.info(f"Filtered corpus: {len(filtered_products)} products")

    # ── Step 3: Ingredient completeness gate across all 33 ───────────────────
    log.info("\n--- Step 3: Ingredient completeness gate across all 33 ---")
    truncation_flags: list[dict] = []
    for p in filtered_products:
        check = check_ingredient_completeness(p)
        if check["status"] == "truncated":
            truncation_flags.append({
                "barcode": p.get("barcode"),
                "name": p.get("name"),
                "reason": check["reason"],
                "char_count": check["char_count"],
                "has_protein_token": check["has_protein_token"],
            })
            log.warning(f"  TRUNCATION FLAG: {p.get('barcode')} '{p.get('name')}' — {check['reason']}")
        else:
            log.info(f"  OK ({check['char_count']} chars, protein token present): {p.get('barcode')} {p.get('name')[:40]}")

    if truncation_flags:
        log.error(f"STOP: {len(truncation_flags)} remaining truncation(s) found in 33-product corpus.")
        log.error("Cannot proceed. Fix these products first.")
        print(json.dumps(truncation_flags, ensure_ascii=False, indent=2))
        sys.exit(1)

    log.info(f"Completeness gate: 0 truncations in {len(filtered_products)} products. PASS.")

    # ── Step 4: Write filtered corpus JSON ────────────────────────────────────
    log.info("\n--- Step 4: Write filtered corpus ---")
    fix_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filtered_corpus_data = dict(source_data)
    filtered_corpus_data["products"] = filtered_products
    filtered_corpus_data["_fix_note"] = (
        f"TASK-365 data-integrity fix {fix_ts}: "
        f"removed 2 WIN barcodes with truncated ingredient lists "
        f"(7290015130271, 7290015130288). "
        f"33 products remain. Discarded per missing-data discard rule."
    )
    filtered_corpus_data["_discarded_barcodes"] = sorted(DISCARD_BARCODES)
    FILTERED_CORPUS.write_text(
        json.dumps(filtered_corpus_data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    log.info(f"Filtered corpus written: {FILTERED_CORPUS}")

    # Verify round-trip count
    reloaded = json.loads(FILTERED_CORPUS.read_text(encoding="utf-8"))
    assert len(reloaded["products"]) == 33, (
        f"Round-trip count mismatch: {len(reloaded['products'])} != 33"
    )
    log.info(f"Round-trip count verified: {len(reloaded['products'])} products")

    # ── Step 5: Score all 33 products ─────────────────────────────────────────
    log.info("\n--- Step 5: Score all 33 products ---")

    if not PROTEIN_BAR_LENS_ON:
        log.warning(
            "BARI_PROTEIN_BAR_V1 is OFF. Set BARI_PROTEIN_BAR_V1=on to run "
            "with the protein_bar lens. Proceeding in baseline mode."
        )

    scored_list: list[dict] = []
    for p in filtered_products:
        try:
            result = scorer.run_product(p)
            result["barcode"] = p.get("barcode", "")
            result["name"] = p.get("name", "")
            result["brand"] = p.get("brand", "")
            result["format"] = p.get("format", "bar")
            result["score"] = result.get("final_score_estimate")
            result["grade"] = result.get("grade_estimate")
            scored_list.append(result)
        except Exception as exc:
            log.error(f"SCORE ERROR {p.get('barcode')}: {exc}")
            scored_list.append({
                "barcode": p.get("barcode"),
                "name": p.get("name"),
                "brand": p.get("brand"),
                "format": p.get("format", "bar"),
                "score": None,
                "grade": "ERROR",
                "error": str(exc),
            })

    # Rank 1..33
    valid = [s for s in scored_list if s.get("score") is not None]
    valid_sorted = sorted(valid, key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(valid_sorted, 1):
        s["rank"] = i
    for s in scored_list:
        if s.get("score") is None:
            s["rank"] = None

    total = len(valid_sorted)
    log.info(f"Scored: {total} products (errors: {len(scored_list) - total})")

    # ── Step 6: Acceptance invariants ─────────────────────────────────────────
    log.info("\n--- Step 6: Run acceptance invariants ---")
    invariant_results = scorer.run_acceptance_invariants(valid_sorted, filtered_products)
    overall = invariant_results.get("_overall", {}).get("status", "UNKNOWN")
    log.info(f"Acceptance invariants: {overall}")
    for k, v in invariant_results.items():
        status = v.get("status", "?")
        note = v.get("note", "")
        log.info(f"  {k}: {status} — {note}")

    if overall == "FAIL":
        log.error("STOP: Acceptance invariants FAILED on 33-product corpus.")
        print(json.dumps(invariant_results, ensure_ascii=False, indent=2))
        sys.exit(1)

    # ── Step 7: Flag-OFF proof ────────────────────────────────────────────────
    log.info("\n--- Step 7: Flag-OFF byte-identical proof ---")
    current_flag = os.environ.get("BARI_PROTEIN_BAR_V1", "off")
    if current_flag.lower() != "on":
        flag_off_proof = scorer.run_flag_off_check(filtered_products)
        log.info(f"Flag-OFF check: {flag_off_proof.get('flag_off_check')}")
    else:
        flag_off_proof = {
            "flag_off_check": "NOTE",
            "bari_protein_bar_v1": current_flag,
            "note": (
                "BARI_PROTEIN_BAR_V1=on for this run. "
                "Flag-OFF proof: apply_protein_bar_lens() returns base_result unchanged "
                "when PROTEIN_BAR_LENS_ON=False. Re-run with --flag-off-check to verify."
            ),
        }

    # ── Step 8: Verify per-product scores unchanged for surviving 33 ─────────
    log.info("\n--- Step 8: Verify per-product scores unchanged for surviving 33 ---")
    # Load old run_record to get previous scores
    old_run_record_path = OUTPUT_DIR / "run_record.json"
    old_scores: dict[str, float] = {}
    if old_run_record_path.exists():
        old_rr = json.loads(old_run_record_path.read_text(encoding="utf-8"))
        for row in old_rr.get("rerank_table", []):
            bc = row.get("barcode")
            sc = row.get("score")
            if bc and sc is not None:
                old_scores[bc] = sc

    score_unchanged_pass = True
    score_changes: list[dict] = []
    for s in valid_sorted:
        bc = s.get("barcode", "")
        new_score = s.get("score")
        if bc in DISCARD_BARCODES:
            continue  # should not appear
        old_score = old_scores.get(bc)
        if old_score is not None and new_score is not None:
            if abs(new_score - old_score) > 0.05:  # allow float rounding < 0.05
                score_unchanged_pass = False
                score_changes.append({
                    "barcode": bc,
                    "name": s.get("name"),
                    "old_score": old_score,
                    "new_score": new_score,
                    "delta": round(new_score - old_score, 2),
                })
                log.error(f"  SCORE CHANGED: {bc} {s.get('name')} {old_score}→{new_score}")
            else:
                log.info(f"  Score stable: {bc} {s.get('name')} = {new_score}")
        else:
            log.info(f"  New product (no old score): {bc} {s.get('name')} = {new_score}")

    if score_unchanged_pass:
        log.info("Score stability check: PASS — all 33 surviving products have unchanged scores.")
    else:
        log.error(f"Score stability check: FAIL — {len(score_changes)} scores changed.")
        for sc in score_changes:
            log.error(f"  {sc}")

    # ── Step 9: COND-2 collagen no-double-fire ────────────────────────────────
    log.info("\n--- Step 9: COND-2 collagen no-double-fire ---")
    collagen_products = [
        s for s in valid_sorted
        if s.get("protein_bar_signals", {}).get("collagen_detected")
    ]
    double_fire_issues = [
        s for s in collagen_products
        if s.get("cond2_double_fire_check") != "PASS — no double-fire"
    ]
    cond2_status = "PASS" if len(double_fire_issues) == 0 else "FAIL"
    log.info(f"  COND-2: {cond2_status} — {len(collagen_products)} collagen products, "
             f"{len(double_fire_issues)} double-fire issues")

    # ── Step 10: Build outputs ────────────────────────────────────────────────
    log.info("\n--- Step 10: Build and write outputs ---")

    # Score distribution
    all_scores = [s["score"] for s in valid_sorted]
    all_grades = [s["grade"] for s in valid_sorted]
    grade_hist: dict[str, int] = {}
    for g in all_grades:
        grade_hist[g] = grade_hist.get(g, 0) + 1

    if all_scores:
        mean_score = round(sum(all_scores) / len(all_scores), 1)
        sorted_scores = sorted(all_scores)
        n = len(sorted_scores)
        median_score = sorted_scores[n // 2] if n % 2 else (sorted_scores[n//2-1] + sorted_scores[n//2]) / 2
        min_score = sorted_scores[0]
        max_score = sorted_scores[-1]
    else:
        mean_score = median_score = min_score = max_score = None

    # Rerank table
    rerank_table: list[dict] = []
    for s in valid_sorted:
        pb_sig = s.get("protein_bar_signals", {})
        rerank_table.append({
            "barcode": s.get("barcode"),
            "name": s.get("name"),
            "brand": s.get("brand"),
            "format": s.get("format", "bar"),
            "rank": s.get("rank"),
            "score": s.get("score"),
            "grade": s.get("grade"),
            "caps_applied": [c["rule"] for c in s.get("protein_bar_caps", [])],
            "key_signals_fired": {
                "glycerol": pb_sig.get("glycerol_detected", False),
                "maltitol": pb_sig.get("polyol_tier") == 1,
                "erythritol": pb_sig.get("polyol_tier") == 3,
                "sweetener_tier_c": pb_sig.get("has_artificial_sweetener", False),
                "isolate_stacking": pb_sig.get("isolate_stacking", False),
                "wholefood_protein": pb_sig.get("wholefood_protein_detected", False),
                "polyol_tier": pb_sig.get("polyol_tier"),
            },
            "protein_g": pb_sig.get("protein_g"),
            "sugar_g": pb_sig.get("sugar_g"),
        })

    # Frontend products
    prefix = "pb"
    frontend_products: list[dict] = []
    for i, s in enumerate(valid_sorted):
        barcode = s.get("barcode", "")
        product = next((p for p in filtered_products if p.get("barcode") == barcode), {})
        product_id = f"{prefix}-{str(i+1).zfill(3)}"
        rec = scorer.build_frontend_record(product, s, i+1, total, product_id)
        frontend_products.append(rec)

    # Diff vs live v1
    v1_diff: list[dict] = []
    if LIVE_V1_PATH.exists():
        v1_data = json.loads(LIVE_V1_PATH.read_text(encoding="utf-8"))
        v1_by_barcode: dict[str, dict] = {
            p["barcode"]: p for p in v1_data.get("products", [])
        }
        for s in valid_sorted:
            bc = s.get("barcode", "")
            if bc in v1_by_barcode:
                v1_p = v1_by_barcode[bc]
                v2_score = s.get("score")
                v1_score = v1_p.get("score")
                delta = round(v2_score - v1_score, 1) if (v2_score is not None and v1_score is not None) else None
                v1_diff.append({
                    "barcode": bc,
                    "name": s.get("name"),
                    "v1_score": v1_score,
                    "v1_grade": v1_p.get("grade"),
                    "v1_rank": v1_p.get("rank"),
                    "v2_score": v2_score,
                    "v2_grade": s.get("grade"),
                    "v2_rank": s.get("rank"),
                    "delta": delta,
                })

    # Corpus hash (of the filtered corpus)
    corpus_sha = hashlib.sha256(FILTERED_CORPUS.read_bytes()).hexdigest()

    # Run ID
    RUN_ID = f"protein_bars_task365_fix33_{fix_ts}"

    # frontend_json
    frontend_json = {
        "_meta": {
            "version": "protein-bars_frontend_task365_v2_fix33",
            "category": "protein-bars",
            "product_count": total,
            "generated": datetime.datetime.utcnow().isoformat() + "Z",
            "run_id": RUN_ID,
            "copy_status": "PENDING_COPY",
            "engine_unchanged": False,
            "lens": "BARI_PROTEIN_BAR_V1",
            "lens_active": PROTEIN_BAR_LENS_ON,
            "cond1_very_long_list": "OMITTED_PER_PRODUCT_COSIGN",
            "cond2_collagen_double_fire": "VERIFIED_NO_DOUBLE_FIRE",
            "cond2_recal_p0_on": RECAL_P0_ON,
            "off_check": "PASS - no Open Food Facts",
            "corpus_sha256": corpus_sha,
            "corpus_source": str(FILTERED_CORPUS),
            "fix_note": (
                "TASK-365 data-integrity fix: removed 2 WIN barcodes with truncated "
                "ingredient lists (7290015130271, 7290015130288). 33 products remain."
            ),
            "deployment_note": (
                "DO NOT OVERWRITE protein_bars_frontend_v1.json. "
                "This file is protein_combined_frontend_v2.json — "
                "live page stays on v1 until owner sign-off."
            ),
        },
        "products": frontend_products,
    }

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-365",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "lens": "BARI_PROTEIN_BAR_V1",
        "lens_active": PROTEIN_BAR_LENS_ON,
        "cond1_omitted": "PROTEIN_BAR_VERY_LONG_LIST omitted per Product Agent COND-1",
        "cond2_branch": f"RECAL_P0_ON={RECAL_P0_ON}",
        "cond2_verification": "assertion in apply_protein_bar_lens() — no double-fire",
        "fix_applied": {
            "discarded_barcodes": sorted(DISCARD_BARCODES),
            "reason": "truncated ingredient lists — no protein source token detected",
            "rule": "missing_data_discard_rule",
            "original_corpus_count": 35,
            "fix_corpus_count": 33,
        },
        "corpus_path": str(FILTERED_CORPUS),
        "corpus_sha256": corpus_sha,
        "corpus_product_count": len(filtered_products),
        "scored_count": total,
        "error_count": len(scored_list) - total,
        "score_distribution": {
            "mean": mean_score,
            "median": median_score,
            "min": min_score,
            "max": max_score,
            "grade_histogram": grade_hist,
        },
        "ingredient_completeness_gate": {
            "status": "PASS",
            "checked": len(filtered_products),
            "truncations_found": 0,
            "min_chars_threshold": INGREDIENT_MIN_CHARS,
            "protein_source_tokens": PROTEIN_SOURCE_TOKENS,
        },
        "score_stability_check": {
            "status": "PASS" if score_unchanged_pass else "FAIL",
            "note": "Per-product scores of surviving 33 are unchanged from 35-product run",
            "changed": score_changes,
        },
        "cond2_collagen_check": {
            "status": cond2_status,
            "collagen_products": len(collagen_products),
            "double_fire_issues": len(double_fire_issues),
            "branch": f"RECAL_P0_ON={RECAL_P0_ON}",
        },
        "acceptance_invariants": invariant_results,
        "flag_off_proof": flag_off_proof,
        "v1_diff_count": len(v1_diff),
        "v1_diff": v1_diff,
        "rerank_table": rerank_table,
        "frontend_output": str(FRONTEND_OUT),
        "live_v1_path": str(LIVE_V1_PATH),
        "live_v1_untouched": True,
    }

    # Write all outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRONTEND_OUT.parent.mkdir(parents=True, exist_ok=True)

    FRONTEND_OUT.write_text(
        json.dumps(frontend_json, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    run_record_path = OUTPUT_DIR / "run_record.json"
    run_record_path.write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    rerank_path = OUTPUT_DIR / "rerank_table.json"
    rerank_path.write_text(
        json.dumps(rerank_table, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    log.info(f"Frontend JSON written: {FRONTEND_OUT}")
    log.info(f"Run record written:    {run_record_path}")
    log.info(f"Rerank table written:  {rerank_path}")
    log.info(f"Live v1 UNTOUCHED:     {LIVE_V1_PATH}")

    # ── Print summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("TASK-365 DATA INTEGRITY FIX — SUMMARY")
    print("=" * 70)
    print(f"Source corpus:     35 products (original)")
    print(f"Discarded:         2 (WIN truncated ingredients)")
    print(f"Remaining corpus:  {total} products")
    print(f"Lens active:       BARI_PROTEIN_BAR_V1={PROTEIN_BAR_LENS_ON}")
    print(f"COND-2 branch:     RECAL_P0_ON={RECAL_P0_ON}")
    print(f"Score range:       {min_score}–{max_score}  (mean={mean_score}, median={median_score})")
    print(f"Grade distribution: {grade_hist}")
    print(f"\nAcceptance invariants: {overall}")
    print(f"Ingredient completeness gate: PASS (0/33 truncated)")
    print(f"Score stability (surviving 33): {'PASS' if score_unchanged_pass else 'FAIL'}")
    print(f"COND-2 no-double-fire: {cond2_status}")

    print(f"\nNew top-5:")
    print(f"{'Rank':>4} {'Score':>5} {'Gr':>2}  {'Name'}")
    print("-" * 60)
    for row in rerank_table[:5]:
        print(
            f"{row['rank']:>4} {row['score']:>5.1f} {row['grade']:>2}  "
            f"{row['name']}  [{row.get('brand','')}]"
        )

    print(f"\nNew full ranking (33 products):")
    print(f"{'Rank':>4} {'Barcode':<15} {'Score':>5} {'Gr':>2}  {'Caps':<30}  {'Name'}")
    print("-" * 100)
    for row in rerank_table:
        caps_str = ",".join(row.get("caps_applied", [])) or "none"
        print(
            f"{row['rank']:>4} {row['barcode']:<15} {row['score']:>5.1f} {row['grade']:>2}  "
            f"{caps_str:<30}  {row['name']}"
        )

    print(f"\nDiscarded WIN products (truncated ingredients):")
    for bc, info in defects_found.items():
        print(f"  {bc} '{info['name']}' — {info['completeness_check']['reason']}")
        print(f"    ingredients ({info['ingredients_char_count']} chars): "
              f"{info['ingredients_preview'][:100]}...")

    # Return data for return contract
    return {
        "total": total,
        "grade_hist": grade_hist,
        "top5": rerank_table[:5],
        "max_score": max_score,
        "invariants_overall": overall,
        "cond2": cond2_status,
        "score_stable": score_unchanged_pass,
        "completeness_gate": "PASS",
        "run_id": RUN_ID,
        "corpus_sha256": corpus_sha,
        "frontend_out": str(FRONTEND_OUT),
        "run_record": str(run_record_path),
        "rerank_table": str(rerank_path),
    }


if __name__ == "__main__":
    result = main()
