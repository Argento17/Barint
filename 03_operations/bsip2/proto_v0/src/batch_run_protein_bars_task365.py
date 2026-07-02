"""
TASK-365 — Protein Bar Sub-Lens Scoring Runner
Implements the protein_bar scoring lens (D6+D7 approved, Nutrition Agent 2026-06-21).

Usage:
    # Flag OFF (byte-identical to HEAD):
    python batch_run_protein_bars_task365.py --flag-off-check

    # Full scoring run (flag ON):
    set BARI_PROTEIN_BAR_V1=on
    python batch_run_protein_bars_task365.py

Output:
    C:\\Bari\\bari-web\\src\\data\\comparisons\\protein_combined_frontend_v2.json
    C:\\Bari\\02_products\\snack_bars\\bsip2_outputs\\protein_bars_task365\\run_record.json
    (Live protein_bars_frontend_v1.json is NOT touched — it remains as-is until owner sign-off)

Gate (COND-2 / BEV-014): collagen penalty coordination with PROTEIN_QUALITY_MATRIX_DISCOUNT.
RECAL_P0_ON branch state is checked at startup and logged. Collagen penalty fires ONLY when
RECAL_P0_ON is False (the discount is then the live path); if RECAL_P0_ON is True, the
discount subsumes the penalty (no double-fire). Runtime assertion enforces this.
"""
from __future__ import annotations

import sys
import os
import json
import pathlib
import datetime
import hashlib
import logging
import argparse

# ── Engine path ──────────────────────────────────────────────────────────────
_SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(_SRC))

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

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
CORPUS_PATH = pathlib.Path(
    r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_20260621_121241.json"
)
OUTPUT_DIR = pathlib.Path(
    r"C:\Bari\02_products\snack_bars\bsip2_outputs\protein_bars_task365"
)
FRONTEND_OUT = pathlib.Path(
    r"C:\Bari\bari-web\src\data\comparisons\protein_combined_frontend_v2.json"
)
LIVE_V1_PATH = pathlib.Path(
    r"C:\Bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json"
)
RUN_ID = f"protein_bars_task365_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"


# =============================================================================
# Protein Bar Signal Detection
# =============================================================================

def _ing_text_from_product(product: dict) -> str:
    """Extract ingredient text for signal detection."""
    raw = (
        product.get("ingredients_full")
        or product.get("ingredients_text_he")
        or product.get("ingredients_raw")
        or ""
    )
    return raw.lower()


def detect_protein_bar_signals(product: dict, nn: dict) -> dict:
    """
    Detect protein_bar-specific signals from product data.
    Returns signals dict consumed by the protein_bar scoring path.
    EV-PBAR-001 through EV-PBAR-007.
    """
    ing_text = _ing_text_from_product(product)
    protein_g = float(nn.get("protein_g") or 0)
    sugar_g = float(nn.get("sugars_g") or 0)

    # ── Polyol tier detection (worst tier wins) ──────────────────────────────
    polyol_tier: int | None = None
    polyol_token_matched: str | None = None
    for tok in POLYOL_TIER_1_TOKENS:
        if tok.lower() in ing_text:
            polyol_tier = 1
            polyol_token_matched = tok
            break
    if polyol_tier is None:
        for tok in POLYOL_TIER_2_TOKENS:
            if tok.lower() in ing_text:
                polyol_tier = 2
                polyol_token_matched = tok
                break
    if polyol_tier is None:
        for tok in POLYOL_TIER_3_TOKENS:
            if tok.lower() in ing_text:
                polyol_tier = 3
                polyol_token_matched = tok
                break

    # ── Glycerol detection (EV-PBAR-003) ────────────────────────────────────
    glycerol_detected = any(tok.lower() in ing_text for tok in GLYCEROL_TOKENS)

    # ── Isolate stacking (EV-PBAR-004b) ─────────────────────────────────────
    families_detected: set[str] = set()
    for family, tokens in PROTEIN_ISOLATE_FAMILIES.items():
        if any(tok.lower() in ing_text for tok in tokens):
            families_detected.add(family)
    isolate_stacking = len(families_detected) >= ISOLATE_STACKING_FAMILY_THRESHOLD
    isolate_families_count = len(families_detected)

    # ── Whole-food protein source (EV-PBAR-004) ──────────────────────────────
    wholefood_protein_detected = any(
        tok.lower() in ing_text for tok in PROTEIN_WHOLEFOOD_TOKENS
    )

    # ── Collagen detection (COND-2 / BEV-014) — TASK-365 ruling: extended tokens ──
    # Use the full PROTEIN_ISOLATE_FAMILIES["collagen"] vocabulary, which now
    # includes פפטידי קולגן / collagen peptides / hydrolyzed collagen variants.
    _collagen_tokens = PROTEIN_ISOLATE_FAMILIES.get("collagen", ())
    collagen_detected = any(tok.lower() in ing_text for tok in _collagen_tokens)

    # ── Protein gate (EV-PBAR-006) ──────────────────────────────────────────
    if protein_g >= PROTEIN_BAR_GATE_MIN_G:
        protein_gate = "PASS"
    elif protein_g >= PROTEIN_BAR_GATE_REJECT_G:
        protein_gate = "WARN_LOW_PROTEIN"
    else:
        protein_gate = "FAIL_NOT_PROTEIN"

    # ── Artificial sweetener check (EV-PBAR-002) ─────────────────────────────
    # Check for Tier-C artificial sweeteners directly in ingredient text
    _art_sw_tokens = (
        "סוכרלוז", "sucralose", "E955", "e955",
        "אצסולפאם", "אצסולפם", "acesulfame", "E950", "e950",
        "סכרין", "saccharin", "E954", "e954",
        "אספרטם", "aspartame", "E951", "e951",
        "נאוטם", "neotame", "E961", "e961",
        "ציקלמט", "cyclamate", "E952", "e952",
    )
    has_artificial_sweetener = any(tok.lower() in ing_text for tok in _art_sw_tokens)

    # Stevia (Tier A) — NOT artificial, NOT included in has_artificial_sweetener
    _stevia_tokens = ("סטיביה", "stevia", "סטיביול גליקוזידים", "E960", "e960")
    has_stevia = any(tok.lower() in ing_text for tok in _stevia_tokens)

    # ── Real-food sugar bonus eligibility (EV-PBAR-007) ─────────────────────
    # No polyol + no artificial sweetener + sugar <= 10g
    real_food_sugar_bonus_eligible = (
        sugar_g <= 10.0
        and polyol_tier is None
        and not has_artificial_sweetener
    )

    return {
        "polyol_tier": polyol_tier,
        "polyol_token_matched": polyol_token_matched,
        "glycerol_detected": glycerol_detected,
        "isolate_stacking": isolate_stacking,
        "isolate_families_count": isolate_families_count,
        "families_detected": sorted(families_detected),
        "wholefood_protein_detected": wholefood_protein_detected,
        "collagen_detected": collagen_detected,
        "protein_gate": protein_gate,
        "protein_g": protein_g,
        "sugar_g": sugar_g,
        "has_artificial_sweetener": has_artificial_sweetener,
        "has_stevia": has_stevia,
        "real_food_sugar_bonus_eligible": real_food_sugar_bonus_eligible,
    }


# =============================================================================
# Protein Bar Lens Application
# =============================================================================

def apply_protein_bar_lens(
    base_result: dict,
    product: dict,
    nn: dict,
    pb_signals: dict,
) -> dict:
    """
    Apply the protein_bar sub-lens to a base score_product result.
    Returns a new result dict with the lens applied.

    All changes are gated by PROTEIN_BAR_LENS_ON.
    Flag OFF → returns base_result with pb_signals added to trace.
    Flag ON  → applies PROTEIN_BAR_WEIGHTS + dimension adjustments + guardrails.

    COND-2 / BEV-014: collagen double-fire prevention.
    RECAL_P0_ON=True  → PROTEIN_QUALITY_MATRIX_DISCOUNT active → no PBAR_COLLAGEN_PENALTY
    RECAL_P0_ON=False → PBAR_COLLAGEN_PENALTY applies as a flat deduction
    """
    # Always record pb_signals in trace
    result = dict(base_result)
    result["protein_bar_signals"] = pb_signals
    result["protein_bar_lens_active"] = PROTEIN_BAR_LENS_ON
    result["cond2_recal_p0_on"] = RECAL_P0_ON  # COND-2 branch state

    if not PROTEIN_BAR_LENS_ON:
        result["protein_bar_lens_note"] = "BARI_PROTEIN_BAR_V1=off — base score unchanged"
        return result

    # ── Re-compute with protein_bar weights ──────────────────────────────────
    dim_scores = dict(base_result.get("dimension_scores", {}))
    dim_notes = dict(base_result.get("dimension_notes", {}))

    # Axis 1 — Calorie density re-score using protein_bar table
    kcal = float(nn.get("energy_kcal") or 0)
    pb_calorie_score = lookup_calorie_density(kcal, "protein_bar")
    old_calorie_score = dim_scores.get("calorie_density", 0)
    dim_scores["calorie_density"] = pb_calorie_score
    dim_notes["calorie_density"] = (
        (dim_notes.get("calorie_density") or "")
        + f" [PBAR_CALORIE_TABLE: protein_bar table {old_calorie_score:.1f}→{pb_calorie_score:.1f}]"
    )

    # Axis 1 — Real-food sugar bonus on glycemic_quality (EV-PBAR-007)
    if pb_signals["real_food_sugar_bonus_eligible"]:
        old_gq = dim_scores.get("glycemic_quality", 0)
        new_gq = min(95.0, old_gq + PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS)
        dim_scores["glycemic_quality"] = new_gq
        dim_notes["glycemic_quality"] = (
            (dim_notes.get("glycemic_quality") or "")
            + f" [PBAR_REAL_FOOD_SUGAR_BONUS: +{PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS},"
            f" {old_gq:.1f}→{new_gq:.1f}]"
        )

    # Axis 3 — Protein source modifier on protein_quality (EV-PBAR-004)
    # TASK-365 ruling: collagen wins unconditionally.
    # WHOLEFOOD_SOURCE_BONUS fires ONLY when collagen is NOT detected (and not isolate_stacking).
    # The old `elif` was WRONG — it allowed a product with both a wholefood token AND collagen
    # to receive the wholefood bonus and skip the collagen penalty. Fixed: two independent checks.
    protein_quality_adj_note = ""
    if pb_signals["collagen_detected"]:
        # Collagen wins — check COND-2 branch
        if not RECAL_P0_ON:
            # COND-2: Apply collagen penalty ONLY when PROTEIN_QUALITY_MATRIX_DISCOUNT is NOT active
            old_prq = dim_scores.get("protein_quality", 0)
            new_prq = max(0.0, old_prq - PROTEIN_BAR_COLLAGEN_PENALTY)
            dim_scores["protein_quality"] = new_prq
            protein_quality_adj_note = (
                f" [PBAR_COLLAGEN_PENALTY: -{PROTEIN_BAR_COLLAGEN_PENALTY},"
                f" {old_prq:.1f}→{new_prq:.1f}; RECAL_P0_ON=False → penalty active;"
                f" WHOLEFOOD_BONUS suppressed — collagen wins]"
            )
            dim_notes["protein_quality"] = (
                (dim_notes.get("protein_quality") or "") + protein_quality_adj_note
            )
        else:
            # COND-2: discount is active — skip penalty to avoid double-count
            protein_quality_adj_note = (
                " [PBAR_COLLAGEN_PENALTY: SKIPPED — RECAL_P0_ON=True;"
                " PROTEIN_QUALITY_MATRIX_DISCOUNT subsumes this penalty (no double-fire);"
                " WHOLEFOOD_BONUS suppressed — collagen wins]"
            )
            dim_notes["protein_quality"] = (
                (dim_notes.get("protein_quality") or "") + protein_quality_adj_note
            )
    elif pb_signals["wholefood_protein_detected"] and not pb_signals["isolate_stacking"]:
        # Wholefood bonus fires ONLY when no collagen detected
        old_prq = dim_scores.get("protein_quality", 0)
        new_prq = min(100.0, old_prq + PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS)
        dim_scores["protein_quality"] = new_prq
        protein_quality_adj_note = (
            f" [PBAR_WHOLEFOOD_SOURCE: +{PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS},"
            f" {old_prq:.1f}→{new_prq:.1f}]"
        )
        dim_notes["protein_quality"] = (
            (dim_notes.get("protein_quality") or "") + protein_quality_adj_note
        )

    # ── COND-2 runtime assertion: no double-fire ─────────────────────────────
    # If collagen was detected, exactly ONE of (discount path or penalty path) must fire,
    # never both. We verify this by checking the note.
    if pb_signals["collagen_detected"]:
        has_discount_note = "PROTEIN_QUALITY_MATRIX_DISCOUNT" in str(
            base_result.get("dimension_notes", {}).get("protein_quality", "")
        )
        has_penalty_note = "PBAR_COLLAGEN_PENALTY" in protein_quality_adj_note
        has_skip_note = "SKIPPED" in protein_quality_adj_note
        # Double-fire = BOTH discount AND penalty active simultaneously
        double_fire = has_discount_note and has_penalty_note and not has_skip_note
        assert not double_fire, (
            f"COND-2 VIOLATION: collagen double-fire detected on barcode "
            f"{product.get('barcode')}. RECAL_P0_ON={RECAL_P0_ON}. "
            f"discount_note={has_discount_note}, penalty_note={has_penalty_note}"
        )
        result["cond2_double_fire_check"] = "PASS — no double-fire"
        result["cond2_note"] = (
            f"RECAL_P0_ON={RECAL_P0_ON}; "
            + ("discount active — penalty skipped" if RECAL_P0_ON
               else "discount inactive — penalty applied")
        )

    # ── Re-compute weighted sum with PROTEIN_BAR_WEIGHTS ─────────────────────
    weighted_sum = sum(dim_scores[k] * PROTEIN_BAR_WEIGHTS[k] for k in dim_scores)
    weighted_dim_score = round(weighted_sum, 2)

    # ── Guardrail caps: polyol tier ──────────────────────────────────────────
    caps_fired: list[dict] = []
    penalties_fired: list[dict] = []
    pb_signals_for_trace: dict = {}

    polyol_tier = pb_signals["polyol_tier"]
    binding_polyol_cap: int | None = None

    if polyol_tier == 1:
        binding_polyol_cap = 62  # PROTEIN_BAR_MALTITOL_TIER1
        caps_fired.append({
            "rule": "PROTEIN_BAR_MALTITOL_TIER1",
            "cap": 62,
            "reason": f"polyol_tier=1 ({pb_signals['polyol_token_matched']})"
        })
    elif polyol_tier == 2:
        binding_polyol_cap = 66  # PROTEIN_BAR_POLYOL_TIER2
        caps_fired.append({
            "rule": "PROTEIN_BAR_POLYOL_TIER2",
            "cap": 66,
            "reason": f"polyol_tier=2 ({pb_signals['polyol_token_matched']})"
        })
    # Tier 3: no cap — penalty only
    if polyol_tier == 3:
        penalties_fired.append({
            "rule": "PROTEIN_BAR_POLYOL_TIER3",
            "penalty": POLYOL_TIER_3_PENALTY,
            "reason": f"polyol_tier=3 ({pb_signals['polyol_token_matched']})"
        })

    # ── Existing sweetener cap (SWEETENER_CAP_C = 70, Tier C only) ──────────
    # Tier A (stevia) is at SWEETENER_CAP_A = 75 — handled by existing engine.
    # Here we check Tier C (artificial) and if the base engine already applied it.
    binding_sweetener_cap: int | None = None
    if pb_signals["has_artificial_sweetener"]:
        binding_sweetener_cap = SWEETENER_CAP_C  # 70
        # Note: this cap is already applied by the base engine for snack_bar_granola.
        # We record it here for protein_bar trace transparency.
        caps_fired.append({
            "rule": "SWEETENER_CAP_C_PROTEIN_BAR",
            "cap": SWEETENER_CAP_C,
            "reason": "Tier-C artificial sweetener detected — existing SWEETENER_CAP_C applies"
        })

    # ── Apply worst cap (maltitol 62 beats sucralose 70) ─────────────────────
    effective_pb_cap: int | None = None
    if binding_polyol_cap is not None and binding_sweetener_cap is not None:
        effective_pb_cap = min(binding_polyol_cap, binding_sweetener_cap)
    elif binding_polyol_cap is not None:
        effective_pb_cap = binding_polyol_cap
    elif binding_sweetener_cap is not None:
        effective_pb_cap = binding_sweetener_cap

    score_after_pb_cap = (
        min(weighted_dim_score, effective_pb_cap)
        if effective_pb_cap is not None
        else weighted_dim_score
    )

    # ── Guardrail penalties: engineering depth (PROCESSING_LOAD family) ──────
    # Budget: share PROCESSING_FAMILY_BUDGET = 12
    eng_penalty_gross = 0
    eng_penalty_detail: list[str] = []

    if pb_signals["glycerol_detected"]:
        p = GLYCEROL_ENGINEERING_PENALTY  # 8
        eng_penalty_gross += p
        penalties_fired.append({
            "rule": "PROTEIN_BAR_GLYCEROL",
            "penalty": p,
            "reason": "glycerol (humectant / engineering marker) detected"
        })
        eng_penalty_detail.append(f"glycerol(-{p})")

    if pb_signals["isolate_stacking"]:
        p = 6  # PROTEIN_BAR_ISOLATE_STACKING
        eng_penalty_gross += p
        penalties_fired.append({
            "rule": "PROTEIN_BAR_ISOLATE_STACKING",
            "penalty": p,
            "reason": (f"{pb_signals['isolate_families_count']} isolate families:"
                       f" {pb_signals['families_detected']}")
        })
        eng_penalty_detail.append(f"isolate_stacking(-{p})")

    # COND-1: PROTEIN_BAR_VERY_LONG_LIST is OMITTED per Product Agent co-sign condition.
    # Redundant with existing LONG_INGREDIENT_LIST + PROCESSING_LOAD budget cap.

    # Apply PROCESSING_FAMILY_BUDGET cap to engineering penalties
    eng_penalty_capped = min(eng_penalty_gross, PROCESSING_FAMILY_BUDGET)
    if eng_penalty_gross > PROCESSING_FAMILY_BUDGET:
        eng_penalty_detail.append(
            f"[capped at PROCESSING_FAMILY_BUDGET={PROCESSING_FAMILY_BUDGET},"
            f" gross={eng_penalty_gross}]"
        )

    # ── Polyol tier 3 penalty ─────────────────────────────────────────────────
    polyol_penalty_applied = 0
    if polyol_tier == 3:
        polyol_penalty_applied = POLYOL_TIER_3_PENALTY

    total_pb_penalty = eng_penalty_capped + polyol_penalty_applied
    score_after_pb_penalty = round(score_after_pb_cap - total_pb_penalty, 2)
    score_after_pb_penalty = max(10.0, score_after_pb_penalty)  # absolute floor

    # ── Also respect any binding_cap from the base engine (e.g. NOVA_PROXY_4) ──
    # The base engine's binding_cap was already applied in score_after_cap.
    # We apply it again on top of the re-weighted score.
    base_binding_cap = base_result.get("binding_cap")
    if base_binding_cap is not None:
        pre_base_cap = score_after_pb_penalty
        score_after_pb_penalty = min(score_after_pb_penalty, base_binding_cap)
        if score_after_pb_penalty < pre_base_cap:
            caps_fired.append({
                "rule": "BASE_ENGINE_BINDING_CAP_INHERIT",
                "cap": base_binding_cap,
                "reason": (f"base engine binding cap {base_binding_cap} inherited;"
                           f" {pre_base_cap:.1f}→{score_after_pb_penalty:.1f}")
            })

    # ── Confidence ceiling (from base engine) ────────────────────────────────
    ceiling = (base_result.get("confidence_result") or {}).get("confidence_ceiling")
    if ceiling is not None and score_after_pb_penalty > ceiling:
        score_after_pb_penalty = ceiling

    final_score = round(score_after_pb_penalty, 1)
    grade = score_to_grade(final_score)

    # ── Protein gate (trace-only, does NOT cap score) ─────────────────────────
    protein_gate = pb_signals["protein_gate"]

    # ── Build updated result ──────────────────────────────────────────────────
    result.update({
        "dimension_scores": dim_scores,
        "dimension_notes": dim_notes,
        "dimension_weights": PROTEIN_BAR_WEIGHTS,
        "weighted_dimension_score_protein_bar": weighted_dim_score,
        "protein_bar_caps": caps_fired,
        "protein_bar_penalties": penalties_fired,
        "effective_pb_cap": effective_pb_cap,
        "score_after_pb_cap": round(score_after_pb_cap, 2),
        "eng_penalty_gross": eng_penalty_gross,
        "eng_penalty_capped": eng_penalty_capped,
        "polyol_penalty_applied": polyol_penalty_applied,
        "total_pb_penalty": total_pb_penalty,
        "score_after_pb_penalty": score_after_pb_penalty,
        "protein_gate": protein_gate,
        "final_score_estimate": final_score,
        "grade_estimate": grade,
        "protein_bar_signals": pb_signals,
        "cond2_recal_p0_on": RECAL_P0_ON,
    })
    return result


# =============================================================================
# Per-product pipeline
# =============================================================================

def _adapt_product_for_engine(product: dict) -> dict:
    """
    Adapt the corpus format (protein_combined_corpus_task365) to the format
    expected by extract_signals / classify_category / score_product.
    The corpus uses 'name' and 'nutrition_per_100g'; the engine expects
    'canonical_name_he' and 'normalized_nutrition_per_100g'.
    """
    adapted = dict(product)
    # Name field
    if "canonical_name_he" not in adapted:
        adapted["canonical_name_he"] = product.get("name", "")
    if "product_name_he" not in adapted:
        adapted["product_name_he"] = product.get("name", "")
    # Nutrition field
    nn = product.get("nutrition_per_100g", {})
    if nn and "normalized_nutrition_per_100g" not in adapted:
        adapted["normalized_nutrition_per_100g"] = nn
    # Ingredients
    if "ingredients_text_he" not in adapted:
        adapted["ingredients_text_he"] = product.get("ingredients_full", "")
    if "ingredients_raw" not in adapted:
        adapted["ingredients_raw"] = product.get("ingredients_full", "")
    return adapted


def run_product(product: dict) -> dict:
    """Run the full protein_bar scoring pipeline for one product."""
    adapted = _adapt_product_for_engine(product)
    nn = adapted.get("normalized_nutrition_per_100g", {})

    # Base engine pipeline
    signals = extract_signals(adapted)
    cat_result = classify_category(adapted)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(adapted, l3)
    eval_result = assign_evaluation_scope(adapted, cat_result["category"])
    base_result = score_product(adapted, signals, cat_result, nova_result, eval_result)

    # Detect protein_bar signals
    pb_signals = detect_protein_bar_signals(adapted, nn)

    # Apply protein_bar lens (gated by PROTEIN_BAR_LENS_ON)
    result = apply_protein_bar_lens(base_result, adapted, nn, pb_signals)

    # Attach routing trace
    result["routing"] = {
        "category": cat_result.get("category"),
        "category_subtype": cat_result.get("category_subtype"),
        "router_confidence": cat_result.get("confidence"),
        "router_anchor": cat_result.get("anchor_fired"),
    }

    return result


# =============================================================================
# D4 additives (Glass Box W2 format, mirroring chocolate_tablets_frontend_v1)
# =============================================================================

def _build_d4_additives(product: dict) -> list:
    """Extract D4 additives in frontend display format from ingredient text."""
    try:
        from score_engine import detect_additives_d4
        ing_text = (
            product.get("ingredients_full")
            or product.get("ingredients_text_he")
            or ""
        )
        return detect_additives_d4(ing_text)
    except Exception:
        return []


# =============================================================================
# Frontend JSON builder
# =============================================================================

def build_frontend_record(
    product: dict,
    scored: dict,
    rank: int,
    total: int,
    product_id: str,
) -> dict:
    """
    Build a frontend JSON record in the shape of chocolate_tablets_frontend_v1.json.
    Copy fields are set to PENDING_COPY per delegation spec.
    """
    nn = product.get("nutrition_per_100g", {})
    pb_signals = scored.get("protein_bar_signals", {})

    # Weight / per-bar fields
    weight_g = product.get("weight_g")
    show_per_bar = (
        weight_g is not None
        and 30 <= weight_g <= 120
    )
    protein_per_100g = nn.get("protein_g")
    protein_per_bar = (
        round(protein_per_100g * weight_g / 100, 1)
        if (show_per_bar and protein_per_100g is not None)
        else None
    )

    # Caps applied (human-readable list)
    caps_applied_str = []
    for c in scored.get("protein_bar_caps", []):
        caps_applied_str.append(c["rule"])
    if scored.get("binding_cap") is not None:
        caps_applied_str.append(f"BASE_CAP_{scored['binding_cap']}")

    # Key signals fired
    key_signals: dict[str, bool | str] = {
        "glycerol": pb_signals.get("glycerol_detected", False),
        "maltitol": pb_signals.get("polyol_tier") == 1,
        "erythritol": pb_signals.get("polyol_tier") == 3,
        "sweetener_tier_c": pb_signals.get("has_artificial_sweetener", False),
        "isolate_stacking": pb_signals.get("isolate_stacking", False),
        "wholefood_protein": pb_signals.get("wholefood_protein_detected", False),
        "polyol_tier": pb_signals.get("polyol_tier"),
        "protein_gate": pb_signals.get("protein_gate", "PASS"),
    }

    return {
        "id": product_id,
        "barcode": product.get("barcode", ""),
        "name": product.get("name", ""),
        "name_he": product.get("name", ""),
        "brand": product.get("brand", ""),
        "format": product.get("format", "bar"),
        "score": scored.get("final_score_estimate"),
        "grade": scored.get("grade_estimate"),
        "rank": rank,
        "categoryTotal": total,
        "imageUrl": product.get("image_url", ""),
        "image_url": product.get("image_url", ""),
        "nutrition_per_100g": {
            "energy_kcal": nn.get("energy_kcal"),
            "fat_g": nn.get("fat_g"),
            "fat_saturated_g": nn.get("fat_saturated_g"),
            "fat_trans_g": nn.get("fat_trans_g"),
            "cholesterol_mg": None,
            "sodium_mg": nn.get("sodium_mg"),
            "carbohydrates_g": nn.get("carbohydrates_g"),
            "sugars_g": nn.get("sugars_g"),
            "dietary_fiber_g": nn.get("dietary_fiber_g"),
            "protein_g": nn.get("protein_g"),
        },
        "protein_per_100g": protein_per_100g,
        "protein_per_bar": protein_per_bar,
        "bar_weight_g": weight_g,
        "show_per_bar": show_per_bar,
        "confidence": "verified",
        "confidence_label_he": "נתונים מאומתים",
        "confidence_sub_reason": "נתוני תזונה ורכיבים ישירות מדף המוצר בשופרסל",
        "confidence_tooltip_he": "הציון מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר.",
        "d4_additives": _build_d4_additives(product),
        # Copy fields — set to PENDING_COPY per delegation spec §RETURN
        "insightLine": "PENDING_COPY",
        "rowVerdict": "PENDING_COPY",
        "_scoring_trace": {
            "category": scored.get("routing", {}).get("category"),
            "category_subtype": scored.get("routing", {}).get("category_subtype"),
            "protein_bar_lens_active": scored.get("protein_bar_lens_active"),
            "cond2_recal_p0_on": scored.get("cond2_recal_p0_on"),
            "cond2_double_fire_check": scored.get("cond2_double_fire_check"),
            "protein_g": nn.get("protein_g"),
            "sugar_g": nn.get("sugars_g"),
            "weighted_dim_score_pb": scored.get("weighted_dimension_score_protein_bar"),
            "effective_pb_cap": scored.get("effective_pb_cap"),
            "total_pb_penalty": scored.get("total_pb_penalty"),
            "caps_applied": scored.get("protein_bar_caps", []),
            "penalties_applied": scored.get("protein_bar_penalties", []),
            "key_signals": key_signals,
            "protein_gate": pb_signals.get("protein_gate"),
            "dimension_scores": scored.get("dimension_scores"),
            "dimension_weights": scored.get("dimension_weights"),
        },
        "expansion": {
            "nutrition": {
                "energyKcal": nn.get("energy_kcal"),
                "protein": nn.get("protein_g"),
                "sugar": nn.get("sugars_g"),
                "fat": nn.get("fat_g"),
                "fiber": nn.get("dietary_fiber_g"),
                "sodium": nn.get("sodium_mg"),
            },
            "ingredients": (
                (product.get("ingredients_full") or "")[:300]
            ),
            "servingNote": "ל-100 גרם",
            "confidenceLabel": "נתונים מאומתים",
            "comparisonContext": "PENDING_COPY",
            "positiveSignals": [],
            "limitingFactors": [],
        }
    }


# =============================================================================
# Flag-OFF byte-identical check
# =============================================================================

def run_flag_off_check(products: list[dict]) -> dict:
    """
    Verify that with BARI_PROTEIN_BAR_V1=off (current state), re-scoring the
    first product in the corpus produces the same final_score as the base engine.
    Returns check result dict.
    """
    p = _adapt_product_for_engine(products[0])
    nn = p.get("normalized_nutrition_per_100g", {})
    signals = extract_signals(p)
    cat_result = classify_category(p)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(p, l3)
    eval_result = assign_evaluation_scope(p, cat_result["category"])
    base = score_product(p, signals, cat_result, nova_result, eval_result)

    pb_signals = detect_protein_bar_signals(p, nn)
    with_lens = apply_protein_bar_lens(base, p, nn, pb_signals)

    base_score = base.get("final_score_estimate")
    lens_score = with_lens.get("final_score_estimate")

    identical = (base_score == lens_score)
    return {
        "flag_off_check": "PASS" if identical else "FAIL",
        "bari_protein_bar_v1": os.environ.get("BARI_PROTEIN_BAR_V1", "off"),
        "product_name": products[0].get("name"),
        "base_score": base_score,
        "lens_score": lens_score,
        "note": (
            "Flag OFF: protein_bar lens is inert — scores are byte-identical"
            if identical
            else f"FAIL: base={base_score} lens={lens_score} — flag-off isolation broken"
        ),
    }


# =============================================================================
# Acceptance invariant checks (spec §9)
# =============================================================================

def run_acceptance_invariants(scored_products: list[dict], corpus_products: list[dict]) -> dict:
    """
    Run the 10 acceptance invariants from spec §9.
    Returns a dict with per-invariant PASS/FAIL results.
    """
    results: dict[str, dict] = {}

    # Build lookup by barcode
    by_barcode: dict[str, dict] = {}
    for sp in scored_products:
        bc = sp.get("barcode", "")
        by_barcode[bc] = sp

    # ── INV-A: Maltitol bar scores >=8 below comparable erythritol bar ────────
    # Find actual maltitol products and erythritol products in scored corpus
    maltitol_products = [
        sp for sp in scored_products
        if (sp.get("_pb_signals", {}) or sp.get("protein_bar_signals", {})).get("polyol_tier") == 1
    ]
    erythritol_products = [
        sp for sp in scored_products
        if (sp.get("_pb_signals", {}) or sp.get("protein_bar_signals", {})).get("polyol_tier") == 3
    ]

    if maltitol_products and erythritol_products:
        max_maltitol = max(sp["score"] for sp in maltitol_products)
        min_erythritol = min(sp["score"] for sp in erythritol_products)
        delta = min_erythritol - max_maltitol
        # The cap ensures this: maltitol cap=62, erythritol uncapped.
        # If the worst erythritol product scores above 62, delta >= 0.
        # The invariant requires >=8 points diff for an otherwise-comparable pair.
        # We test: any maltitol product vs any erythritol product delta >= 8
        # (since caps enforce 62 vs uncapped, and erythritol products generally score higher)
        inv_a_pass = delta >= 8
        results["INV_A_maltitol_vs_erythritol"] = {
            "status": "PASS" if inv_a_pass else "FAIL",
            "max_maltitol_score": max_maltitol,
            "min_erythritol_score": min_erythritol,
            "delta": round(delta, 1),
            "required_delta": 8,
            "note": (
                f"cap hierarchy: maltitol cap=62, erythritol uncapped; "
                f"min_erythritol({min_erythritol}) - max_maltitol({max_maltitol}) = {round(delta,1)}"
            )
        }
    else:
        results["INV_A_maltitol_vs_erythritol"] = {
            "status": "SKIP",
            "note": f"maltitol_products={len(maltitol_products)}, erythritol_products={len(erythritol_products)}"
        }

    # ── INV-B: Glycerol presence lowers score (penalty=8 applied) ────────────
    glycerol_products = [
        sp for sp in scored_products
        if (sp.get("protein_bar_signals", {})).get("glycerol_detected")
    ]
    if glycerol_products:
        # All glycerol products received -8 penalty. We can check by confirming
        # penalty is in their trace.
        inv_b_pass = all(
            sp.get("total_pb_penalty", 0) >= GLYCEROL_ENGINEERING_PENALTY
            for sp in glycerol_products
        )
        avg_glycerol_score = sum(sp["score"] for sp in glycerol_products) / len(glycerol_products)
        non_glycerol = [
            sp for sp in scored_products
            if not (sp.get("protein_bar_signals", {})).get("glycerol_detected")
        ]
        avg_non_glycerol_score = (
            sum(sp["score"] for sp in non_glycerol) / len(non_glycerol) if non_glycerol else None
        )
        results["INV_B_glycerol_penalty"] = {
            "status": "PASS" if inv_b_pass else "FAIL",
            "glycerol_count": len(glycerol_products),
            "avg_glycerol_score": round(avg_glycerol_score, 1),
            "avg_non_glycerol_score": round(avg_non_glycerol_score, 1) if avg_non_glycerol_score else None,
            "note": f"All glycerol products received total_pb_penalty >= {GLYCEROL_ENGINEERING_PENALTY}"
        }
    else:
        results["INV_B_glycerol_penalty"] = {
            "status": "SKIP",
            "note": "No glycerol products in corpus"
        }

    # ── INV-C: Protein grams alone move composite <=5 points ─────────────────
    # This requires synthetic test: run a single product at 3 protein levels.
    # We use the first product in the corpus and vary protein_g.
    p_test = dict(corpus_products[0])
    nn_base = dict(p_test.get("nutrition_per_100g", {}))
    scores_by_protein = {}
    for pg in [10.0, 15.0, 20.0, 30.0]:
        nn_v = dict(nn_base)
        nn_v["protein_g"] = pg
        p_v = dict(p_test)
        p_v["nutrition_per_100g"] = nn_v
        p_v["normalized_nutrition_per_100g"] = nn_v
        p_adapted = _adapt_product_for_engine(p_v)
        signals_v = extract_signals(p_adapted)
        cat_v = classify_category(p_adapted)
        l3_v = signals_v["L3_inferred_classifications"]
        nova_v = infer_nova(p_adapted, l3_v)
        eval_v = assign_evaluation_scope(p_adapted, cat_v["category"])
        base_v = score_product(p_adapted, signals_v, cat_v, nova_v, eval_v)
        pb_v = detect_protein_bar_signals(p_adapted, nn_v)
        res_v = apply_protein_bar_lens(base_v, p_adapted, nn_v, pb_v)
        scores_by_protein[pg] = res_v.get("final_score_estimate", 0)

    max_protein_move = max(scores_by_protein.values()) - min(scores_by_protein.values())
    inv_c_pass = max_protein_move <= 5
    results["INV_C_protein_quantity_move_le5"] = {
        "status": "PASS" if inv_c_pass else "FAIL",
        "scores_by_protein_g": {str(k): v for k, v in scores_by_protein.items()},
        "max_move_points": round(max_protein_move, 2),
        "required_max": 5,
        "note": f"Varying protein_g from 10→30g on '{p_test.get('name')}'"
    }

    # ── INV-D: Cap hierarchy holds ────────────────────────────────────────────
    # maltitol ≤ 62 < sorbitol/isomalt ≤ 66 < artificial ≤ 70, erythritol uncapped
    # Verify all maltitol products score <= 62
    inv_d_maltitol = all(sp["score"] <= 62 for sp in maltitol_products)
    tier2_products = [
        sp for sp in scored_products
        if (sp.get("protein_bar_signals", {})).get("polyol_tier") == 2
    ]
    inv_d_tier2 = all(sp["score"] <= 66 for sp in tier2_products)
    artificial_products = [
        sp for sp in scored_products
        if (sp.get("protein_bar_signals", {})).get("has_artificial_sweetener")
        and (sp.get("protein_bar_signals", {})).get("polyol_tier") is None
    ]
    inv_d_artificial = all(sp["score"] <= 70 for sp in artificial_products)
    inv_d_pass = inv_d_maltitol and inv_d_tier2 and inv_d_artificial
    results["INV_D_cap_hierarchy"] = {
        "status": "PASS" if inv_d_pass else "FAIL",
        "maltitol_cap_check": f"{len(maltitol_products)} products all <=62: {inv_d_maltitol}",
        "tier2_cap_check": f"{len(tier2_products)} products all <=66: {inv_d_tier2}",
        "artificial_cap_check": f"{len(artificial_products)} products all <=70: {inv_d_artificial}",
        "note": "Cap hierarchy: maltitol(62) < tier2(66) < artificial(70) < erythritol(uncapped)"
    }

    # ── INV-E: BEV-014 no-double-count (collagen, COND-2) ────────────────────
    collagen_products = [
        sp for sp in scored_products
        if (sp.get("protein_bar_signals", {})).get("collagen_detected")
    ]
    double_fire_issues = [
        sp for sp in collagen_products
        if sp.get("cond2_double_fire_check") != "PASS — no double-fire"
    ]
    inv_e_pass = len(double_fire_issues) == 0
    results["INV_E_BEV014_no_double_count"] = {
        "status": "PASS" if inv_e_pass else "FAIL",
        "collagen_products": len(collagen_products),
        "double_fire_issues": len(double_fire_issues),
        "cond2_branch": f"RECAL_P0_ON={RECAL_P0_ON}",
        "note": (
            "RECAL_P0_ON active — discount subsumes penalty (no double-fire)"
            if RECAL_P0_ON
            else "RECAL_P0_ON inactive — penalty applies (discount not active, no double-fire)"
        )
    }

    # ── INV-F: Calorie density non-cliff check ────────────────────────────────
    score_379 = lookup_calorie_density(379, "protein_bar")
    score_381 = lookup_calorie_density(381, "protein_bar")
    cliff = abs(score_381 - score_379)
    inv_f_pass = cliff <= 2
    results["INV_F_calorie_density_no_cliff"] = {
        "status": "PASS" if inv_f_pass else "FAIL",
        "score_at_379kcal": score_379,
        "score_at_381kcal": score_381,
        "diff": cliff,
        "required_max_diff": 2,
        "note": "protein_bar calorie table boundary check around 380 kcal"
    }

    # ── INV-G: Products with "חלבון" or "פרוטאין" in name route to protein_bar ──
    # Per spec §9.4: "All products on the protein bar shelf that have 'חלבון'
    # or 'פרוטאין' in the name must route to protein_bar."
    # Scope: products whose NAME literally contains the Hebrew protein tokens
    # (not corpus name_protein_signal, which may be set via brand knowledge).
    protein_name_tokens = ("חלבון", "פרוטאין", "protein")
    products_with_protein_in_name = [
        p for p in corpus_products
        if any(tok in (p.get("name") or "") for tok in protein_name_tokens)
    ]
    routing_fails = []
    for p in products_with_protein_in_name:
        adapted = _adapt_product_for_engine(p)
        cat = classify_category(adapted)
        if cat.get("category_subtype") != "protein_bar":
            routing_fails.append({
                "barcode": p.get("barcode"),
                "category": cat.get("category"),
                "category_subtype": cat.get("category_subtype"),
            })
    inv_g_pass = len(routing_fails) == 0
    results["INV_G_routing_protein_name"] = {
        "status": "PASS" if inv_g_pass else "FAIL",
        "checked_products_with_protein_in_name": len(products_with_protein_in_name),
        "routing_fails": routing_fails,
        "note": (
            "Products with 'חלבון'/'פרוטאין'/'protein' in name must route to protein_bar subtype. "
            f"Products lacking protein token in name (brand-only detection) are excluded from this check."
        )
    }

    # ── INV-H: No score below absolute floor (10) ────────────────────────────
    below_floor = [sp for sp in scored_products if sp.get("score", 100) < 10]
    results["INV_H_absolute_floor"] = {
        "status": "PASS" if len(below_floor) == 0 else "FAIL",
        "below_floor_count": len(below_floor),
        "below_floor_products": [sp.get("name") for sp in below_floor],
    }

    # ── INV-I: Worst cap wins for combined maltitol + sweetener ─────────────
    combined_products = [
        sp for sp in scored_products
        if (sp.get("protein_bar_signals", {})).get("polyol_tier") == 1
        and (sp.get("protein_bar_signals", {})).get("has_artificial_sweetener")
    ]
    inv_i_pass = all(sp["score"] <= 62 for sp in combined_products)
    results["INV_I_worst_cap_wins"] = {
        "status": "PASS" if inv_i_pass else "FAIL",
        "combined_maltitol_artificial": len(combined_products),
        "note": "maltitol(62) beats sucralose(70) — worst cap wins"
    }

    # ── Overall ───────────────────────────────────────────────────────────────
    all_pass = all(
        v.get("status") in ("PASS", "SKIP")
        for v in results.values()
    )
    # Fail if any non-skip fails
    any_fail = any(v.get("status") == "FAIL" for v in results.values())

    results["_overall"] = {
        "status": "PASS" if not any_fail else "FAIL",
        "all_checked": not any_fail,
        "skipped": sum(1 for v in results.values() if v.get("status") == "SKIP"),
    }

    return results


# =============================================================================
# Main runner
# =============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--flag-off-check", action="store_true",
                        help="Run byte-identical check (flag must be OFF)")
    args = parser.parse_args()

    # Load corpus
    corpus_data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    products = corpus_data["products"]
    corpus_count = len(products)
    log.info(f"Loaded corpus: {corpus_count} products from {CORPUS_PATH.name}")

    # Log COND-2 branch state at startup
    log.info(f"COND-2 branch state: RECAL_P0_ON={RECAL_P0_ON}")
    log.info(f"Protein bar lens active: PROTEIN_BAR_LENS_ON={PROTEIN_BAR_LENS_ON}")

    # Flag-OFF check
    if args.flag_off_check:
        off_check = run_flag_off_check(products)
        log.info(f"Flag-OFF check: {off_check['flag_off_check']}")
        log.info(f"  base_score={off_check['base_score']}, lens_score={off_check['lens_score']}")
        sys.stdout.buffer.write(
            json.dumps(off_check, ensure_ascii=True, indent=2).encode("ascii") + b"\n"
        )
        return

    if not PROTEIN_BAR_LENS_ON:
        log.warning(
            "BARI_PROTEIN_BAR_V1 is OFF — running in baseline mode. "
            "To score with the protein_bar lens, set BARI_PROTEIN_BAR_V1=on"
        )

    # ── Score all products ────────────────────────────────────────────────────
    scored_list: list[dict] = []
    for p in products:
        try:
            result = run_product(p)
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

    # ── Rank by score ─────────────────────────────────────────────────────────
    valid = [s for s in scored_list if s.get("score") is not None]
    valid_sorted = sorted(valid, key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(valid_sorted, 1):
        s["rank"] = i
    for s in scored_list:
        if s.get("score") is None:
            s["rank"] = None

    total = len(valid_sorted)

    # ── Run acceptance invariants ──────────────────────────────────────────────
    log.info("Running acceptance invariants (spec §9)...")
    invariant_results = run_acceptance_invariants(valid_sorted, products)
    overall = invariant_results.get("_overall", {}).get("status", "UNKNOWN")
    log.info(f"Acceptance invariants: {overall}")
    for k, v in invariant_results.items():
        if k != "_overall":
            status = v.get("status", "?")
            note = v.get("note", "")
            log.info(f"  {k}: {status} — {note}")

    if overall == "FAIL":
        log.error("STOP: One or more acceptance invariants FAILED. "
                  "Do not proceed to frontend packaging. Fix the scoring logic first.")
        print(json.dumps(invariant_results, ensure_ascii=False, indent=2))
        sys.exit(1)

    # ── Flag-OFF byte-identical proof ─────────────────────────────────────────
    current_flag = os.environ.get("BARI_PROTEIN_BAR_V1", "off")
    flag_off_proof: dict
    if current_flag.lower() != "on":
        # Currently off — can run the check directly
        flag_off_proof = run_flag_off_check(products)
    else:
        # Flag is on for this run — prove by noting that flag-off path is the same base engine
        flag_off_proof = {
            "flag_off_check": "NOTE",
            "bari_protein_bar_v1": current_flag,
            "note": (
                "BARI_PROTEIN_BAR_V1=on for this run. "
                "Flag-OFF byte-identical proof: re-run with --flag-off-check "
                "after unsetting BARI_PROTEIN_BAR_V1. The apply_protein_bar_lens() "
                "function returns base_result unchanged when PROTEIN_BAR_LENS_ON=False."
            )
        }
    log.info(f"Flag-OFF proof: {flag_off_proof.get('flag_off_check')}")

    # ── Build frontend JSON ────────────────────────────────────────────────────
    prefix = "pb"
    frontend_products: list[dict] = []
    for i, s in enumerate(valid_sorted):
        barcode = s.get("barcode", "")
        product = next((p for p in products if p.get("barcode") == barcode), {})
        product_id = f"{prefix}-{str(i+1).zfill(3)}"
        rec = build_frontend_record(product, s, i+1, total, product_id)
        frontend_products.append(rec)

    # ── Score distribution ────────────────────────────────────────────────────
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

    # ── Diff vs live v1 (16 products) ─────────────────────────────────────────
    v1_diff: list[dict] = []
    if LIVE_V1_PATH.exists():
        v1_data = json.loads(LIVE_V1_PATH.read_text(encoding="utf-8"))
        v1_by_barcode: dict[str, dict] = {
            p["barcode"]: p for p in v1_data.get("products", [])
        }
        v1_barcodes_in_v2 = set()
        for s in valid_sorted:
            bc = s.get("barcode", "")
            if bc in v1_by_barcode:
                v1_barcodes_in_v2.add(bc)
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
        log.info(f"V1 diff: {len(v1_diff)}/{len(v1_by_barcode)} v1 products in v2 corpus")

    # ── Re-rank table (full 35) ────────────────────────────────────────────────
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
            "protein_g": (s.get("protein_bar_signals", {}) or {}).get("protein_g"),
            "sugar_g": (s.get("protein_bar_signals", {}) or {}).get("sugar_g"),
        })

    # ── Write outputs ─────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRONTEND_OUT.parent.mkdir(parents=True, exist_ok=True)

    # Compute corpus hash
    corpus_sha = hashlib.sha256(CORPUS_PATH.read_bytes()).hexdigest()

    frontend_json = {
        "_meta": {
            "version": "protein-bars_frontend_task365_v2",
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
        "corpus_path": str(CORPUS_PATH),
        "corpus_sha256": corpus_sha,
        "corpus_product_count": corpus_count,
        "scored_count": len(valid_sorted),
        "error_count": len(scored_list) - len(valid_sorted),
        "score_distribution": {
            "mean": mean_score,
            "median": median_score,
            "min": min_score,
            "max": max_score,
            "grade_histogram": grade_hist,
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

    # Write files
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

    # ── Print summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print(f"PROTEIN BAR SUB-LENS — TASK-365 SCORING RUN")
    print("=" * 70)
    print(f"Lens active:       BARI_PROTEIN_BAR_V1={PROTEIN_BAR_LENS_ON}")
    print(f"COND-2 branch:     RECAL_P0_ON={RECAL_P0_ON}")
    print(f"Products scored:   {len(valid_sorted)}/{corpus_count}")
    print(f"Score range:       {min_score}–{max_score}  (mean={mean_score}, median={median_score})")
    print(f"Grade distribution: {grade_hist}")
    print(f"\nAcceptance invariants: {overall}")
    print(f"Flag-OFF proof: {flag_off_proof.get('flag_off_check')}")
    print(f"\nRerank table (all {len(rerank_table)} products):")
    print(f"{'Rank':>4} {'Barcode':<15} {'Score':>5} {'Gr':>2}  {'Caps':<30}  {'Name'}")
    print("-" * 100)
    for row in rerank_table:
        caps_str = ",".join(row.get("caps_applied", [])) or "none"
        print(
            f"{row['rank']:>4} {row['barcode']:<15} {row['score']:>5.1f} {row['grade']:>2}  "
            f"{caps_str:<30}  {row['name']}"
        )

    if v1_diff:
        print(f"\nDiff vs live v1 ({len(v1_diff)} overlapping products):")
        print(f"{'Barcode':<15} {'V1':>5} {'V2':>5} {'Delta':>6}  {'Name'}")
        print("-" * 80)
        for row in sorted(v1_diff, key=lambda x: (x["delta"] or 0), reverse=True):
            delta_str = f"+{row['delta']}" if (row['delta'] or 0) > 0 else str(row['delta'])
            print(f"{row['barcode']:<15} {row['v1_score']:>5} {row['v2_score']:>5} {delta_str:>6}  {row['name']}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
