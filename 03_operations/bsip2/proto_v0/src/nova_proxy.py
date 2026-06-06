"""
BSIP2 Prototype v0 — NOVA Proxy Classifier
Infers NOVA level from ingredient signals. Not a validated classifier.
Confidence is explicit. Every inference is traceable.
"""
import os

# TASK-169 P0 (R4) — plain-dairy NOVA-3→2 demotion guard, gated by BARI_RECAL_P0.
# DEFAULT OFF → classifier byte-identical. See recalibration_p0_design_v1.md R4.
RECAL_P0_ON = os.environ.get("BARI_RECAL_P0", "off").lower() == "on"

# R4 v1.1 (TASK-169A) — flavored/seasoned-variant markers that disqualify the plain-dairy
# NOVA-3→2 demotion. Imported from constants so the list is single-sourced.
try:
    from constants import FLAVORED_VARIANT_MARKERS_HE
except Exception:  # pragma: no cover — defensive for alternate import paths
    FLAVORED_VARIANT_MARKERS_HE = ()

# Additive categories that mark genuine ultra-processing; presence of ANY blocks the
# R4 demotion (product stays NOVA 3). Benign culinary/culturing/fortification additions
# (salt, cultures, rennet, calcium, vitamins) emit no additive_category marker.
NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS = {
    "thickener", "stabilizer", "emulsifier", "humectant", "flavor_enhancer", "color",
}

# NOVA 4 requires evidence of industrial formulation:
# flavor enhancers, artificial colors, multiple additive systems, glucose syrups
NOVA4_STRONG_SIGNALS = [
    "flavor_enhancer",   # חומרי טעם וריח — strongest signal
    "color",             # צבע מאכל
]

# Additional NOVA 4 signals from additive categories
NOVA4_MODERATE_SIGNALS = [
    "humectant",         # e.g., גליצרין, סורביטול
    "emulsifier",        # מתחלב (multiple = stronger signal)
]

# NOVA 3 signals: processed but not ultra-processed
NOVA3_SIGNALS = [
    "preservative",
    "antioxidant",
    "acidity_regulator",
    "leavening_agent",
]

# Whole grain presence reduces NOVA level estimate
# Fermentation presence reduces NOVA level estimate
# Single ingredient is almost always NOVA 1

# EV-009 / EV-010: Extruded/shaped grain products are NOVA 3 (milling-disrupted matrix).
# "פתיתים אפויים" = Osem-style baked shaped pasta-cereal (extrusion + shaping + bake).
# This is the minimal name-detection component of EV-010 (extrusion_matrix_penalty).
# Gated to the specific product name prefix — does NOT apply to "פתיתים אורגנים" (rolled grain flakes).
# Backed by: Nutrition Agent ruling 2026-06-05 (TASK-140 QA-CER-W1); EV-009 (extruded shapes = disrupted);
# EV-010 (should_affect_score_now: true; risk-of-misuse: refined-grain extrusion penalized, whole-grain puffed exempt).
EXTRUDED_SHAPE_NAME_SIGNALS: list[str] = [
    "פתיתים אפויים",   # baked pasta-shaped flakes (Osem type: קוסקוס/כוכבים/טבעות/אורז)
]


def infer_nova(product: dict, l3_signals: dict) -> dict:
    """
    Infer NOVA proxy level (1-4) from L3 ingredient signals.
    Returns dict with nova_level, nova_confidence, and full trace.
    """
    # TASK-144 Fix1/EV-026 — prefer the sanitized ingredient count (OCR/nutrition-panel/
    # disclaimer bleed removed in signal_extractor). Falls back to the raw product list
    # for any legacy caller that does not supply the sanitized count, so behaviour is
    # unchanged where the field is absent.
    ingredients = product.get("ingredients_list") or []
    if l3_signals.get("sanitized_ingredient_count") is not None:
        ing_count = l3_signals["sanitized_ingredient_count"]
    else:
        ing_count = len(ingredients)
    additive_cats = set(l3_signals.get("additive_categories") or [])
    has_flavor_enhancer = l3_signals.get("has_flavor_enhancer", False)
    has_color = l3_signals.get("has_artificial_color", False)
    has_sweetener = l3_signals.get("sweetener_detected", False)
    has_whole_grain = l3_signals.get("has_whole_grain", False)
    has_fermentation = l3_signals.get("has_fermentation", False)
    additive_count = l3_signals.get("additive_marker_count", 0)
    added_sugar_ct = l3_signals.get("added_sugar_sources_count", 0)
    ing_quality = product.get("ingredient_text_quality", "unknown")

    evidence_for = []
    evidence_against = []
    confidence_penalties = []

    # ---------------------------------------------------------------------------
    # NOVA 1 check: single ingredient, no additives
    # ---------------------------------------------------------------------------
    # EV-030 guard: the single-ingredient fast-path must not fire when ingredient data is
    # degraded. Three degradation signals are checked:
    #   (a) explicit quality flag (corrupted/missing/malformed)
    #   (b) "ingredients_list" in missing_fields — BSIP1 failed to parse a real list
    #   (c) ingredients_raw_provenance.source == "bsip1_text_fallback" — list reconstructed
    #       from page marketing text, not a real ingredient declaration
    # When any signal fires, fall through to the main classifier with a confidence penalty
    # so the NOVA estimate reflects the actual uncertainty rather than a false 0.90.
    _mf = product.get("missing_fields") or []
    _prov_source = (product.get("ingredients_raw_provenance") or {}).get("source", "")
    _ingredient_data_degraded = (
        ing_quality in ("missing", "corrupted", "malformed")
        or "ingredients_list" in _mf
        or _prov_source == "bsip1_text_fallback"
    )
    if ing_count == 1 and additive_count == 0 and not has_sweetener and not _ingredient_data_degraded:
        return {
            "nova_level": 1,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_evidence_for": ["single_ingredient", "no_additives_detected"],
            "nova_evidence_against": [],
            "nova_uncertainty_notes": ["Single ingredient is strong NOVA 1 signal; undetected additives could change this"],
        }
    if _ingredient_data_degraded:
        confidence_penalties.append(
            f"EV-030: ingredient_data_degraded (quality={ing_quality}, "
            f"ingredients_list_missing={'ingredients_list' in _mf}, "
            f"provenance={_prov_source or 'unknown'}): NOVA 1 fast-path suppressed"
        )

    # ---------------------------------------------------------------------------
    # NOVA 4 assessment: ultra-processed
    # ---------------------------------------------------------------------------
    nova4_score = 0

    if has_flavor_enhancer:
        nova4_score += 3
        evidence_for.append("flavor_enhancer_detected (חומרי טעם וריח)")
    if has_color:
        nova4_score += 2
        evidence_for.append("artificial_color_detected (צבע מאכל)")
    if has_sweetener:
        nova4_score += 2
        evidence_for.append("sweetener_detected")
    if added_sugar_ct >= 3:
        nova4_score += 2
        evidence_for.append(f"multiple_added_sugar_sources: {added_sugar_ct}")
    if "emulsifier" in additive_cats and "humectant" in additive_cats:
        nova4_score += 1
        evidence_for.append("emulsifier+humectant combination")
    if additive_count >= 4:
        nova4_score += 1
        evidence_for.append(f"high_additive_category_count: {additive_count}")
    if ing_count > 15:
        nova4_score += 1
        evidence_for.append(f"very_long_ingredient_list: {ing_count}")

    # Signals that argue against NOVA 4
    if has_whole_grain:
        nova4_score -= 1
        evidence_against.append("whole_grain_present (consistent with NOVA 2-3)")
    if has_fermentation:
        nova4_score -= 1
        evidence_against.append("fermentation_markers (consistent with NOVA 1-2)")

    # EV-009 / EV-010: extruded-shape early detection.
    # If the product name matches an extruded/shaped cereal pattern, assert NOVA 3 immediately.
    # Runs before the full score-based classifier so a product with a missing ingredient list
    # (empty ingredient signals → nova4_score≈0 → would land at NOVA 2 by default) is still
    # correctly placed at NOVA 3 based on its production method.
    _product_name_he = (product.get("canonical_name_he") or product.get("product_name_he") or "").strip()
    _is_extruded_shape = any(sig in _product_name_he for sig in EXTRUDED_SHAPE_NAME_SIGNALS)
    if _is_extruded_shape:
        evidence_for.append(
            "EV-010: extruded_shape_name_signal fired ('פתיתים אפויים') — "
            "industrial extrusion + shaping + bake = NOVA 3 per EV-009 disrupted-grain classification; "
            "Nutrition ruling 2026-06-05"
        )
        return {
            "nova_level": 3,
            "nova_confidence": round(max(0.20, 0.55 - (0.25 if _ingredient_data_degraded else 0.0)), 2),
            "nova_confidence_band": "medium" if not _ingredient_data_degraded else "low",
            "nova_evidence_for": evidence_for,
            "nova_evidence_against": evidence_against,
            "nova_uncertainty_notes": confidence_penalties + [
                "EV-010 name-detection: 'פתיתים אפויים' confirms extrusion/shaping; "
                "EV-010 full scoring signal pending D7 co-sign (follow-up scope)",
                "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            ],
        }

    # ---------------------------------------------------------------------------
    # Classify by score
    # ---------------------------------------------------------------------------
    if nova4_score >= 4:
        level = 4
        base_conf = 0.80
    elif nova4_score >= 2:
        # Could be NOVA 3 or 4 — check for NOVA 3 signals
        nova3_cats = additive_cats & set(NOVA3_SIGNALS)
        if nova4_score >= 3:
            level = 4
            base_conf = 0.65
        else:
            level = 3
            base_conf = 0.60
    elif additive_count >= 1 or added_sugar_ct >= 1 or ing_count > 5:
        # Some processing signals but not ultra-processed
        level = 3
        base_conf = 0.55
        evidence_for.append(f"additive_categories: {additive_count}, added_sugars: {added_sugar_ct}")
    else:
        # Minimal processing signals
        level = 2
        base_conf = 0.50
        evidence_for.append("minimal_additives_and_processing_signals")

    # ---------------------------------------------------------------------------
    # Confidence adjustments
    # ---------------------------------------------------------------------------
    if ing_quality in ("corrupted", "missing", "malformed"):
        base_conf -= 0.20
        confidence_penalties.append(f"ingredient_quality={ing_quality}: confidence reduced")
    if _prov_source == "bsip1_text_fallback":
        base_conf -= 0.25
        confidence_penalties.append("provenance=bsip1_text_fallback: ingredient list reconstructed from page text, not label; NOVA inference unreliable")
    if ing_count == 0:
        base_conf -= 0.30
        confidence_penalties.append("no_ingredient_list: NOVA inference unreliable")

    nova_confidence = max(0.20, min(0.95, base_conf))

    # R4 — NOVA-3→2 demotion guard for PLAIN DAIRY (TASK-169, EV-024/026 lineage).
    # Demote a tentative 3 back to 2 ONLY when the product is a plain dairy base with no
    # flavor/sweetener/added-sugar and no genuine ultra-processing additive marker
    # (thickener/gum/emulsifier/humectant/flavor/color). Never promotes a 4. Gated.
    nova_demotion_applied = False
    product_type_dairy = l3_signals.get("product_type_dairy", False)
    if RECAL_P0_ON and level == 3 and product_type_dairy:
        # R4 v1.1 — a declared flavoring (even a whole-food one: garlic/dill/herbs/…) makes
        # this a FLAVORED VARIANT and forfeits the plain-dairy retention. This only blocks a
        # demotion (keeps tentative NOVA 3 at 3); it never promotes and never demotes new.
        name = (product.get("canonical_name_he") or product.get("product_name_he") or "")
        hay = name + " " + " ".join(str(i) for i in ingredients)
        has_flavor_variant = any(m in hay for m in FLAVORED_VARIANT_MARKERS_HE)
        is_plain = (added_sugar_ct == 0 and not has_sweetener
                    and not has_flavor_enhancer and not has_color
                    and not has_flavor_variant)
        blocking = set(additive_cats) & set(NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS)
        if is_plain and not blocking:
            level = 2
            nova_demotion_applied = True
            evidence_against.append(
                "R4 plain-dairy demotion 3→2: dairy base, no flavor/sweetener/added-sugar, "
                "no flavored-variant marker, no ultra-processing additive marker "
                "(salt/culture/rennet/calcium/vitamins only)")
        elif has_flavor_variant:
            evidence_for.append(
                "R4 v1.1: flavored/seasoned dairy variant → NOVA-2 retention forfeited (stays 3)")

    if nova_confidence >= 0.75:
        band = "high"
    elif nova_confidence >= 0.50:
        band = "medium"
    else:
        band = "low"

    return {
        "nova_level": level,
        "nova_r4_demotion_applied": nova_demotion_applied,
        "nova_confidence": round(nova_confidence, 2),
        "nova_confidence_band": band,
        "nova4_signal_score": nova4_score,
        "nova_evidence_for": evidence_for,
        "nova_evidence_against": evidence_against,
        "nova_uncertainty_notes": confidence_penalties + [
            "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            "Hebrew ingredient text keyword matching has limited coverage for novel additive names",
        ],
    }
