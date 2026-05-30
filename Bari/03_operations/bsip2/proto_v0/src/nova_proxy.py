"""
BSIP2 Prototype v0 — NOVA Proxy Classifier
Infers NOVA level from ingredient signals. Not a validated classifier.
Confidence is explicit. Every inference is traceable.
"""

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


def infer_nova(product: dict, l3_signals: dict) -> dict:
    """
    Infer NOVA proxy level (1-4) from L3 ingredient signals.
    Returns dict with nova_level, nova_confidence, and full trace.
    """
    ingredients = product.get("ingredients_list") or []
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
    if ing_count == 1 and additive_count == 0 and not has_sweetener:
        return {
            "nova_level": 1,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_evidence_for": ["single_ingredient", "no_additives_detected"],
            "nova_evidence_against": [],
            "nova_uncertainty_notes": ["Single ingredient is strong NOVA 1 signal; undetected additives could change this"],
        }

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
    if ing_count == 0:
        base_conf -= 0.30
        confidence_penalties.append("no_ingredient_list: NOVA inference unreliable")

    nova_confidence = max(0.20, min(0.95, base_conf))

    if nova_confidence >= 0.75:
        band = "high"
    elif nova_confidence >= 0.50:
        band = "medium"
    else:
        band = "low"

    return {
        "nova_level": level,
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
