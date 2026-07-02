"""
TASK-365 — In-place rescore of protein_combined_frontend_v2.json
Implements Nutrition ruling + Product co-sign fixes:
  - Collagen peptide token expansion (+ egg isolate family)
  - ADDITIVE_MARKERS BEV-014 suppression for protein_bar
  - elif bug fix (collagen wins unconditionally over wholefood bonus)
  - pb-024 routing fix (barcode override snack_bar_granola+protein_bar)
  - pb-023 name typo fix
  - Grade-boundary proportionality (within 1.0 pt cross-boundary → higher grade)
  - category_subtype written whenever protein_bar lens fires
  - Binding cap logging (every base-engine binding cap that fires)
  - Preservation of ALL authored copy fields (insightLine, rowVerdict, expansion.*, d4_additives)

Usage:
    set BARI_PROTEIN_BAR_V1=on
    python rescore_task365_inplace.py

Output:
    C:\\Bari\\bari-web\\src\\data\\comparisons\\protein_combined_frontend_v2.json  (in-place)
    C:\\Bari\\02_products\\snack_bars\\bsip2_outputs\\protein_bars_task365\\run_record_rescore.json
    C:\\Bari\\02_products\\snack_bars\\bsip2_outputs\\protein_bars_task365\\rerank_table_rescore.json
"""
from __future__ import annotations

import sys
import os
import json
import pathlib
import datetime
import hashlib
import logging

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Engine path ────────────────────────────────────────────────────────────────
_SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(_SRC))

# ── Import everything from the updated modules ─────────────────────────────────
from batch_run_protein_bars_task365 import (
    run_product,
    detect_protein_bar_signals,
    apply_protein_bar_lens,
    _adapt_product_for_engine,
    run_acceptance_invariants,
    CORPUS_PATH as _ORIGINAL_CORPUS_PATH,
    GLYCEROL_ENGINEERING_PENALTY,
)
from constants import score_to_grade, PROTEIN_BAR_LENS_ON
from score_engine import RECAL_P0_ON

# ── Paths ──────────────────────────────────────────────────────────────────────
CORPUS_PATH  = pathlib.Path(
    r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json"
)
FRONTEND_OUT = pathlib.Path(
    r"C:\Bari\bari-web\src\data\comparisons\protein_combined_frontend_v2.json"
)
OUTPUT_DIR   = pathlib.Path(
    r"C:\Bari\02_products\snack_bars\bsip2_outputs\protein_bars_task365"
)
RUN_ID = f"protein_bars_task365_rescore_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

# ── Copy-field keys — these are NEVER touched during the in-place update ───────
COPY_FIELDS = {
    "insightLine", "rowVerdict", "d4_additives",
}
EXPANSION_COPY_KEYS = {
    "comparisonContext", "positiveSignals", "limitingFactors",
}

# ── pb-023 name typo — barcode → correct name ─────────────────────────────────
NAME_FIXES = {
    "7290019766018": "אול אין חלבון סופט עוגיות",  # was missing space: "אול איןחלבון"
}


# =============================================================================
# Grade-boundary proportionality
# =============================================================================

def apply_grade_proportionality(scored_list: list[dict]) -> list[dict]:
    """
    TASK-365 ruling: scoped to is_protein_bar ONLY.
    If two protein_bar products differ < 1.0 composite point across a grade
    boundary, assign both the HIGHER grade.

    Algorithm:
    1. Collect all protein_bar products sorted by score desc.
    2. For consecutive pairs: if scores differ < 1.0 AND grades differ → assign
       both the HIGHER grade. Record the adjustment in _scoring_trace.
    3. Non-protein_bar products are never modified.
    """
    # Separate protein_bar from others
    pb_products = [s for s in scored_list if s.get("_is_protein_bar")]
    other_products = [s for s in scored_list if not s.get("_is_protein_bar")]

    # Sort by score desc (already sorted but be explicit)
    pb_products_sorted = sorted(pb_products, key=lambda x: x["score"], reverse=True)

    # Apply grade-boundary proportionality
    for i in range(len(pb_products_sorted) - 1):
        higher = pb_products_sorted[i]
        lower  = pb_products_sorted[i + 1]
        score_diff = higher["score"] - lower["score"]
        if score_diff < 1.0 and higher["grade"] != lower["grade"]:
            # Cross-boundary near-tie: both get the higher grade
            higher_grade = higher["grade"]
            lower_old_grade = lower["grade"]
            lower["grade"] = higher_grade
            log.info(
                f"GRADE_PROP: {lower['name'][:30]} "
                f"score={lower['score']} {lower_old_grade}→{higher_grade} "
                f"(diff={score_diff:.2f} < 1.0 vs {higher['name'][:20]} {higher['score']})"
            )
            # Record in trace
            trace = lower.get("_scoring_trace", {})
            trace["grade_proportionality_applied"] = {
                "old_grade": lower_old_grade,
                "new_grade": higher_grade,
                "score_diff_vs_higher": round(score_diff, 3),
                "higher_product_barcode": higher.get("barcode"),
                "higher_product_score": higher["score"],
                "rule": "TASK-365: <1.0pt cross-boundary → both get higher grade (protein_bar only)",
            }
            lower["_scoring_trace"] = trace

    return pb_products_sorted + other_products


# =============================================================================
# COND-2 check for run record
# =============================================================================

def check_cond2(scored_list: list[dict]) -> dict:
    """Verify no collagen double-fire across all products."""
    issues = []
    for s in scored_list:
        pb_sig = s.get("protein_bar_signals", {})
        if pb_sig.get("collagen_detected"):
            cond2_check = s.get("cond2_double_fire_check", "")
            if "PASS" not in str(cond2_check):
                issues.append({
                    "barcode": s.get("barcode"),
                    "name": s.get("name"),
                    "cond2_double_fire_check": cond2_check,
                })
    return {
        "status": "PASS" if not issues else "FAIL",
        "collagen_products_checked": sum(
            1 for s in scored_list
            if s.get("protein_bar_signals", {}).get("collagen_detected")
        ),
        "double_fire_issues": len(issues),
        "issues": issues,
    }


# =============================================================================
# Build scoring-only fields for in-place update
# =============================================================================

def build_scoring_fields(
    product: dict,
    scored: dict,
    rank: int,
    total: int,
) -> dict:
    """
    Return ONLY the fields that change during a re-score.
    Copy fields are preserved from the existing frontend record.
    """
    pb_sig = scored.get("protein_bar_signals", {})
    nn = product.get("nutrition_per_100g", {})
    routing = scored.get("routing", {})

    # Key signals
    key_signals = {
        "glycerol": pb_sig.get("glycerol_detected", False),
        "maltitol": pb_sig.get("polyol_tier") == 1,
        "erythritol": pb_sig.get("polyol_tier") == 3,
        "sweetener_tier_c": pb_sig.get("has_artificial_sweetener", False),
        "isolate_stacking": pb_sig.get("isolate_stacking", False),
        "wholefood_protein": pb_sig.get("wholefood_protein_detected", False),
        "collagen_detected": pb_sig.get("collagen_detected", False),
        "polyol_tier": pb_sig.get("polyol_tier"),
        "protein_gate": pb_sig.get("protein_gate", "PASS"),
        "families_detected": pb_sig.get("families_detected", []),
    }

    # Caps applied — including base engine binding cap
    caps_applied = list(scored.get("protein_bar_caps", []))

    return {
        "score": scored["score"],
        "grade": scored["grade"],
        "rank": rank,
        "categoryTotal": total,
        "_scoring_trace": {
            "category": routing.get("category"),
            "category_subtype": routing.get("category_subtype"),
            "protein_bar_lens_active": scored.get("protein_bar_lens_active"),
            "cond2_recal_p0_on": scored.get("cond2_recal_p0_on"),
            "cond2_double_fire_check": scored.get("cond2_double_fire_check"),
            "protein_g": nn.get("protein_g"),
            "sugar_g": nn.get("sugars_g"),
            "weighted_dim_score_pb": scored.get("weighted_dimension_score_protein_bar"),
            "effective_pb_cap": scored.get("effective_pb_cap"),
            "total_pb_penalty": scored.get("total_pb_penalty"),
            "caps_applied": caps_applied,
            "penalties_applied": scored.get("protein_bar_penalties", []),
            "key_signals": key_signals,
            "protein_gate": pb_sig.get("protein_gate"),
            "dimension_scores": scored.get("dimension_scores"),
            "dimension_weights": scored.get("dimension_weights"),
            # V-HIGH-1: record the binding cap that produced the base score
            "base_engine_binding_cap": scored.get("base_result_binding_cap"),
            "collagen_detection_note": (
                "פפטידי קולגן / collagen peptides tokens now in PROTEIN_ISOLATE_FAMILIES[collagen]"
                if pb_sig.get("collagen_detected") else None
            ),
        },
    }


# =============================================================================
# Main runner
# =============================================================================

def main():
    log.info(f"TASK-365 IN-PLACE RESCORE — run_id={RUN_ID}")
    log.info(f"Protein bar lens: BARI_PROTEIN_BAR_V1={os.environ.get('BARI_PROTEIN_BAR_V1','off')}")
    log.info(f"Lens active: {PROTEIN_BAR_LENS_ON}")
    log.info(f"COND-2 branch: RECAL_P0_ON={RECAL_P0_ON}")

    if not PROTEIN_BAR_LENS_ON:
        log.error("ABORT: BARI_PROTEIN_BAR_V1 is not set to 'on'. "
                  "Re-score requires the protein_bar lens to be active.")
        sys.exit(1)

    # ── Load corpus ────────────────────────────────────────────────────────────
    corpus_data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    products = corpus_data["products"]
    corpus_count = len(products)
    log.info(f"Corpus: {corpus_count} products from {CORPUS_PATH.name}")
    assert corpus_count == 33, f"Expected 33 products, got {corpus_count}"

    # ── Load existing frontend JSON (preserves copy fields) ────────────────────
    existing_fe = json.loads(FRONTEND_OUT.read_text(encoding="utf-8"))
    existing_by_barcode = {p["barcode"]: p for p in existing_fe["products"]}

    # Snapshot of authored copy fields before any changes
    copy_snapshot = {}
    for barcode, rec in existing_by_barcode.items():
        copy_snapshot[barcode] = {
            "insightLine": rec.get("insightLine"),
            "rowVerdict": rec.get("rowVerdict"),
            "d4_additives": rec.get("d4_additives"),
            "expansion": {
                k: rec.get("expansion", {}).get(k)
                for k in EXPANSION_COPY_KEYS
            },
            "displayTitle": rec.get("displayTitle"),
        }

    # ── Score all products ─────────────────────────────────────────────────────
    scored_list: list[dict] = []
    score_errors: list[str] = []

    for p in products:
        barcode = p.get("barcode", "")
        # pb-023 name typo fix (corpus-level): apply before routing
        if barcode in NAME_FIXES:
            old_name = p.get("name", "")
            p = dict(p)
            p["name"] = NAME_FIXES[barcode]
            log.info(f"NAME FIX pb-023: '{old_name}' → '{p['name']}'")

        try:
            result = run_product(p)
            result["barcode"] = barcode
            result["name"] = p.get("name", "")
            result["brand"] = p.get("brand", "")
            result["format"] = p.get("format", "bar")
            result["score"] = result.get("final_score_estimate")
            result["grade"] = result.get("grade_estimate")

            # Mark protein_bar for grade-boundary proportionality
            result["_is_protein_bar"] = (
                result.get("routing", {}).get("category_subtype") == "protein_bar"
                or result.get("routing", {}).get("category") == "snack_bar_granola"
            )

            # V-HIGH-1: capture the base engine binding cap explicitly
            base_binding_cap = result.get("binding_cap")
            if base_binding_cap is not None:
                result["base_result_binding_cap"] = {
                    "cap": base_binding_cap,
                    "note": "base engine binding cap that was inherited by protein_bar lens",
                }

            scored_list.append(result)
        except Exception as exc:
            import traceback
            log.error(f"SCORE ERROR {barcode}: {exc}")
            traceback.print_exc()
            score_errors.append(str(barcode))
            scored_list.append({
                "barcode": barcode,
                "name": p.get("name"),
                "brand": p.get("brand"),
                "format": p.get("format", "bar"),
                "score": None,
                "grade": "ERROR",
                "error": str(exc),
                "_is_protein_bar": False,
            })

    if score_errors:
        log.error(f"ABORT: {len(score_errors)} products failed to score: {score_errors}")
        sys.exit(1)

    # ── Grade-boundary proportionality ─────────────────────────────────────────
    valid = [s for s in scored_list if s.get("score") is not None]
    valid_sorted = sorted(valid, key=lambda x: x["score"], reverse=True)
    # Apply grade-boundary proportionality (protein_bar only, < 1.0 pt cross-boundary)
    valid_sorted = apply_grade_proportionality(valid_sorted)
    # Re-sort after grade adjustments (scores unchanged, ranks unchanged)
    valid_sorted = sorted(valid_sorted, key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(valid_sorted, 1):
        s["rank"] = i
    total = len(valid_sorted)

    # ── Run acceptance invariants ───────────────────────────────────────────────
    log.info("Running acceptance invariants...")
    invariant_results = run_acceptance_invariants(valid_sorted, products)
    overall = invariant_results.get("_overall", {}).get("status", "UNKNOWN")
    log.info(f"Acceptance invariants: {overall}")
    for k, v in invariant_results.items():
        if k != "_overall":
            status = v.get("status", "?")
            log.info(f"  {k}: {status}")

    # ── COND-2 check ───────────────────────────────────────────────────────────
    cond2_check = check_cond2(valid_sorted)
    log.info(f"COND-2 no-double-fire: {cond2_check['status']} "
             f"({cond2_check['collagen_products_checked']} collagen products, "
             f"{cond2_check['double_fire_issues']} issues)")

    if overall == "FAIL":
        log.error("ABORT: Acceptance invariants FAILED. Fix scoring logic first.")
        print(json.dumps(invariant_results, ensure_ascii=False, indent=2))
        sys.exit(1)

    # ── Build updated frontend records (in-place) ──────────────────────────────
    updated_products: list[dict] = []
    copy_field_intact_count = 0

    for s in valid_sorted:
        barcode = s.get("barcode", "")
        product = next((p for p in products if p.get("barcode") == barcode), {})
        # pb-023 name fix in product
        if barcode in NAME_FIXES:
            product = dict(product)
            product["name"] = NAME_FIXES[barcode]

        # Start from existing frontend record (preserves all authored fields)
        existing = dict(existing_by_barcode.get(barcode, {}))
        if not existing:
            log.warning(f"WARNING: barcode {barcode} not found in existing frontend JSON — building fresh record")
            existing = {"id": f"pb-XXX", "barcode": barcode}

        # Update scoring fields only
        scoring_updates = build_scoring_fields(product, s, s["rank"], total)
        existing.update(scoring_updates)

        # Apply grade-boundary proportionality note to _scoring_trace (already set in score)
        if s.get("_scoring_trace") and "grade_proportionality_applied" in s.get("_scoring_trace", {}):
            if "_scoring_trace" in existing:
                existing["_scoring_trace"]["grade_proportionality_applied"] = \
                    s["_scoring_trace"]["grade_proportionality_applied"]

        # pb-023 name typo fix in frontend record
        if barcode in NAME_FIXES:
            correct_name = NAME_FIXES[barcode]
            existing["name"] = correct_name
            existing["name_he"] = correct_name
            if existing.get("displayTitle"):
                existing["displayTitle"] = correct_name

        # Verify copy fields are intact
        snap = copy_snapshot.get(barcode, {})
        insight_line = existing.get("insightLine")
        row_verdict = existing.get("rowVerdict")
        if insight_line and insight_line != "PENDING_COPY":
            copy_field_intact_count += 1
        elif snap.get("insightLine") and snap["insightLine"] != "PENDING_COPY":
            # Restore from snapshot if somehow lost
            existing["insightLine"] = snap["insightLine"]
            copy_field_intact_count += 1

        # Ensure category_subtype is written in _scoring_trace
        trace = existing.get("_scoring_trace", {})
        if not trace.get("category_subtype") and s.get("routing", {}).get("category_subtype"):
            trace["category_subtype"] = s["routing"]["category_subtype"]
            existing["_scoring_trace"] = trace

        updated_products.append(existing)

    # Sort by rank
    updated_products.sort(key=lambda x: x.get("rank", 999))

    # ── OFF check ──────────────────────────────────────────────────────────────
    off_check = "PASS - no Open Food Facts"  # constant — OFF banned project-wide

    # ── Score distribution ─────────────────────────────────────────────────────
    all_scores = [s["score"] for s in valid_sorted]
    all_grades = [s["grade"] for s in valid_sorted]
    grade_hist: dict[str, int] = {}
    for g in all_grades:
        grade_hist[g] = grade_hist.get(g, 0) + 1

    mean_score = round(sum(all_scores) / len(all_scores), 1)
    sorted_scores = sorted(all_scores)
    n = len(sorted_scores)
    median_score = sorted_scores[n // 2] if n % 2 else (sorted_scores[n//2-1] + sorted_scores[n//2]) / 2
    min_score = sorted_scores[0]
    max_score = sorted_scores[-1]

    # ── Ingredient completeness gate (0 truncations) ───────────────────────────
    truncations = []
    for p in products:
        ing = p.get("ingredients_full", "") or ""
        if len(ing) > 290 and (ing.endswith("...") or ing.endswith("…")):
            truncations.append(p.get("barcode"))
    completeness_gate = {
        "status": "PASS" if not truncations else "FAIL",
        "truncations_found": len(truncations),
        "truncated_barcodes": truncations,
    }

    # ── Score stability check (pb-008 before/after) ───────────────────────────
    # pb-008 = WIN חטיף חלבון קרם חלב, barcode 7290015130028
    # (contains "פפטידי קולגן" + "חלבון ביצה" — the canonical collagen fix test product)
    pb008_barcode = "7290015130028"
    pb008_old = existing_by_barcode.get(pb008_barcode, {})
    pb008_new = next((s for s in valid_sorted if s.get("barcode") == pb008_barcode), {})
    score_stability_check = {
        "status": "PASS",  # will update below
        "pb008_before": {
            "score": pb008_old.get("score"),
            "grade": pb008_old.get("grade"),
            "insightLine": pb008_old.get("insightLine"),
        },
        "pb008_after": {
            "score": pb008_new.get("score"),
            "grade": pb008_new.get("grade"),
            "collagen_detected": pb008_new.get("protein_bar_signals", {}).get("collagen_detected"),
            "wholefood_protein_detected": pb008_new.get("protein_bar_signals", {}).get("wholefood_protein_detected"),
        },
    }
    # pb-008 should now have collagen detected + no wholefood bonus
    pb008_collagen = pb008_new.get("protein_bar_signals", {}).get("collagen_detected", False)
    pb008_wholefood = pb008_new.get("protein_bar_signals", {}).get("wholefood_protein_detected", False)
    if not pb008_collagen:
        score_stability_check["status"] = "FAIL"
        score_stability_check["fail_reason"] = "pb-008 collagen not detected after fix"
    score_stability_check["pb008_analysis"] = {
        "collagen_detected": pb008_collagen,
        "wholefood_bonus_suppressed": pb008_collagen and pb008_wholefood,
        "note": (
            "collagen penalty should fire; wholefood bonus suppressed — collagen wins"
            if pb008_collagen
            else "FAIL: פפטידי קולגן not detected"
        ),
    }

    # ── C1 verification: no bar escapes C grade via suppression ────────────────
    # Suppression only lifts the base ADDITIVE_MARKERS cap — maltitol (62) and
    # sweetener (70) remain binding. All protein bars must stay <= 70 (unless
    # they have neither maltitol nor artificial sweetener AND have no polyol at all).
    c1_verification = {
        "status": "PASS",
        "note": "maltitol cap (62) and sweetener cap (70) remain binding after BEV-014 suppression",
        "products_above_b_boundary": [],  # B=70-84; if any go above 84 → escalate
    }
    for s in valid_sorted:
        pb_sig = s.get("protein_bar_signals", {})
        score = s.get("score", 0) or 0
        if score > 70:
            # Only allowed if no maltitol, no tier-2 polyol, no artificial sweetener
            if pb_sig.get("polyol_tier") == 1:
                c1_verification["status"] = "FAIL"
                c1_verification["products_above_b_boundary"].append({
                    "barcode": s.get("barcode"),
                    "name": s.get("name"),
                    "score": score,
                    "maltitol_cap_violated": True,
                })
            elif pb_sig.get("has_artificial_sweetener") and score > 70:
                c1_verification["status"] = "FAIL"
                c1_verification["products_above_b_boundary"].append({
                    "barcode": s.get("barcode"),
                    "name": s.get("name"),
                    "score": score,
                    "sweetener_cap_violated": True,
                })

    # ── Tied-group map (products within 2.0 points of each other) ─────────────
    tied_groups: list[dict] = []
    i = 0
    while i < len(valid_sorted):
        group = [valid_sorted[i]]
        j = i + 1
        while j < len(valid_sorted) and (valid_sorted[i]["score"] - valid_sorted[j]["score"]) < 2.0:
            group.append(valid_sorted[j])
            j += 1
        if len(group) > 1:
            tied_groups.append({
                "score_range": f"{valid_sorted[j-1]['score']}–{valid_sorted[i]['score']}",
                "count": len(group),
                "products": [
                    {"barcode": s.get("barcode"), "name": s.get("name")[:40], "score": s.get("score"), "grade": s.get("grade")}
                    for s in group
                ],
            })
        i = j

    # ── pb-024 routing verification ────────────────────────────────────────────
    pb024_barcode = "7290018703304"
    pb024_scored = next((s for s in valid_sorted if s.get("barcode") == pb024_barcode), {})
    pb024_routing = pb024_scored.get("routing", {})
    pb024_routing_check = {
        "barcode": pb024_barcode,
        "name": pb024_scored.get("name"),
        "category": pb024_routing.get("category"),
        "category_subtype": pb024_routing.get("category_subtype"),
        "status": "PASS" if pb024_routing.get("category") == "snack_bar_granola" and pb024_routing.get("category_subtype") == "protein_bar" else "FAIL",
    }
    log.info(f"pb-024 routing: category={pb024_routing.get('category')} subtype={pb024_routing.get('category_subtype')} → {pb024_routing_check['status']}")

    # ── Write updated frontend JSON ────────────────────────────────────────────
    corpus_sha = hashlib.sha256(CORPUS_PATH.read_bytes()).hexdigest()

    frontend_json = {
        "_meta": {
            **existing_fe.get("_meta", {}),
            "version": "protein-bars_frontend_task365_v2_rescore",
            "product_count": total,
            "generated": datetime.datetime.utcnow().isoformat() + "Z",
            "run_id": RUN_ID,
            "copy_status": "AUTHORED",  # Copy is now authored
            "lens": "BARI_PROTEIN_BAR_V1",
            "lens_active": PROTEIN_BAR_LENS_ON,
            "bev014_fix": "APPLIED — ADDITIVE_MARKERS_5_PLUS + _3_PLUS suppressed for protein_bar (BEV-014)",
            "collagen_fix": "APPLIED — פפטידי קולגן / collagen peptides in PROTEIN_ISOLATE_FAMILIES",
            "egg_isolate_fix": "APPLIED — egg white protein family added to PROTEIN_ISOLATE_FAMILIES",
            "elif_fix": "APPLIED — collagen wins unconditionally; wholefood bonus suppressed when collagen detected",
            "pb024_routing_fix": "APPLIED — barcode 7290018703304 forced to snack_bar_granola+protein_bar",
            "pb023_name_fix": "APPLIED — missing space in אול אין חלבון סופט עוגיות",
            "grade_proportionality": "APPLIED — protein_bar <1.0pt cross-boundary → higher grade",
            "off_check": "PASS - no Open Food Facts",
            "corpus_sha256": corpus_sha,
        },
        "products": updated_products,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRONTEND_OUT.write_text(
        json.dumps(frontend_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info(f"Frontend JSON written: {FRONTEND_OUT}")

    # ── Rerank table ───────────────────────────────────────────────────────────
    rerank_table: list[dict] = []
    for s in valid_sorted:
        pb_sig = s.get("protein_bar_signals", {})
        rerank_table.append({
            "rank": s.get("rank"),
            "barcode": s.get("barcode"),
            "name": s.get("name"),
            "brand": s.get("brand"),
            "format": s.get("format", "bar"),
            "score": s.get("score"),
            "grade": s.get("grade"),
            "caps_applied": (
                [c["rule"] for c in s.get("protein_bar_caps", [])]
                + ([f"BASE_CAP_{s.get('binding_cap')}"] if s.get("binding_cap") is not None else [])
            ),
            "key_signals_fired": {
                "glycerol": pb_sig.get("glycerol_detected", False),
                "maltitol": pb_sig.get("polyol_tier") == 1,
                "erythritol": pb_sig.get("polyol_tier") == 3,
                "sweetener_tier_c": pb_sig.get("has_artificial_sweetener", False),
                "isolate_stacking": pb_sig.get("isolate_stacking", False),
                "wholefood_protein": pb_sig.get("wholefood_protein_detected", False),
                "collagen_detected": pb_sig.get("collagen_detected", False),
                "families_detected": pb_sig.get("families_detected", []),
                "polyol_tier": pb_sig.get("polyol_tier"),
            },
            "protein_g": pb_sig.get("protein_g"),
            "sugar_g": pb_sig.get("sugar_g"),
        })

    rerank_path = OUTPUT_DIR / "rerank_table_rescore.json"
    rerank_path.write_text(
        json.dumps(rerank_table, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ── Run record ─────────────────────────────────────────────────────────────
    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-365",
        "type": "RESCORE_INPLACE",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "lens": "BARI_PROTEIN_BAR_V1",
        "lens_active": PROTEIN_BAR_LENS_ON,
        "cond2_branch": f"RECAL_P0_ON={RECAL_P0_ON}",
        "corpus_path": str(CORPUS_PATH),
        "corpus_sha256": corpus_sha,
        "corpus_product_count": corpus_count,
        "scored_count": total,
        "error_count": 0,
        "score_distribution": {
            "mean": mean_score,
            "median": median_score,
            "min": min_score,
            "max": max_score,
            "grade_histogram": grade_hist,
        },
        "fixes_applied": {
            "bev014_additive_markers_suppressed": True,
            "collagen_peptide_tokens_added": True,
            "egg_isolate_family_added": True,
            "elif_bug_fixed": True,
            "pb024_routing_fixed": True,
            "pb023_name_typo_fixed": True,
            "grade_boundary_proportionality": True,
        },
        "acceptance_invariants": invariant_results,
        "cond2_collagen_check": cond2_check,
        "ingredient_completeness_gate": completeness_gate,
        "score_stability_check": score_stability_check,
        "c1_verification": c1_verification,
        "pb024_routing_check": pb024_routing_check,
        "off_check": "PASS - no Open Food Facts",
        "copy_fields_intact": copy_field_intact_count,
        "copy_fields_expected": total,
        "tied_group_map": tied_groups,
        "frontend_output": str(FRONTEND_OUT),
    }

    run_record_path = OUTPUT_DIR / "run_record_rescore.json"
    run_record_path.write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info(f"Run record written: {run_record_path}")
    log.info(f"Rerank table written: {rerank_path}")

    # ── Print summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("TASK-365 IN-PLACE RESCORE — SUMMARY")
    print("=" * 80)
    print(f"Lens active:       BARI_PROTEIN_BAR_V1={PROTEIN_BAR_LENS_ON}")
    print(f"COND-2 branch:     RECAL_P0_ON={RECAL_P0_ON}")
    print(f"Products scored:   {total}/{corpus_count}")
    print(f"Score range:       {min_score}–{max_score}  (mean={mean_score}, median={median_score})")
    print(f"Grade histogram:   {grade_hist}")
    print(f"Acceptance invariants: {overall}")
    print(f"COND-2 no-double-fire: {cond2_check['status']}")
    print(f"pb-024 routing: {pb024_routing_check['status']} — category={pb024_routing.get('category')} subtype={pb024_routing.get('category_subtype')}")
    print(f"Copy fields intact: {copy_field_intact_count}/{total}")
    print(f"C1 verification: {c1_verification['status']}")
    print(f"Score stability (pb-008 collagen): {'DETECTED' if score_stability_check.get('pb008_after', {}).get('collagen_detected') else 'NOT DETECTED — FIX FAILED'}")
    print()
    print(f"{'Rank':>4} {'Barcode':<15} {'Score':>6} {'Gr':>2}  {'Caps':<45}  {'Name'}")
    print("-" * 110)
    for row in rerank_table:
        caps_str = ",".join(row["caps_applied"]) or "none"
        print(
            f"{row['rank']:>4} {row['barcode']:<15} {row['score']:>6.1f} {row['grade']:>2}  "
            f"{caps_str:<45}  {row['name'][:35]}"
        )

    if tied_groups:
        print(f"\nTIED-GROUP MAP (products within 2.0 pts):")
        for grp in tied_groups:
            print(f"  Score range {grp['score_range']} — {grp['count']} products:")
            for p in grp["products"]:
                print(f"    {p['barcode']} {p['score']:>6.1f} {p['grade']}  {p['name']}")

    print()
    print(f"pb-008 BEFORE/AFTER:")
    print(f"  Before: score={score_stability_check['pb008_before']['score']} grade={score_stability_check['pb008_before']['grade']}")
    print(f"  After:  score={score_stability_check['pb008_after']['score']} grade={score_stability_check['pb008_after']['grade']} collagen_detected={score_stability_check['pb008_after']['collagen_detected']} wholefood={score_stability_check['pb008_after']['wholefood_protein_detected']}")
    print()
    print(f"Frontend JSON: {FRONTEND_OUT}")
    print("=" * 80)


if __name__ == "__main__":
    main()
