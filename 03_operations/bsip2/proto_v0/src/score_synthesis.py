"""
BSIP2 Score Synthesis Layer v1

Post-score calibration that integrates bakery semantics signals into the
final score synthesis. Called after score_engine.score_product() and
bakery_semantics.run_bakery_semantics().

Philosophy: coherence-weighted interpretation, not anti-fiber or anti-processing.
Nuance refines interpretation; it must NOT neutralize meaningful structural signals.
The system should produce clear gradients, coherent distinctions, and interpretable tradeoffs.

Input:  full assembled BSIP2 trace dict (includes bakery_semantics + structural_class)
Output: synthesis_result dict with synthesized_score and full adjustment trace

The synthesized_score is the preferred output in synthesis-aware runners.
The base score is preserved for comparison.
"""

from __future__ import annotations

SYNTHESIS_VERSION = "score_synthesis_v1"

# ---------------------------------------------------------------------------
# Global bounds
# ---------------------------------------------------------------------------

SYNTHESIS_MAX_UPWARD   = 10.0   # cap on positive synthesis adjustment
SYNTHESIS_MAX_DOWNWARD = 18.0   # cap on negative synthesis adjustment
SYNTHESIS_SCORE_FLOOR  =  8.0   # absolute minimum synthesized score
SYNTHESIS_SCORE_CEIL   = 97.0   # absolute maximum synthesized score


# ===========================================================================
# Component 1: Fiber source quality discount (bakery only)
# ===========================================================================

def _fiber_discount(bakery_semantics: dict, trace: dict) -> tuple[float, list[str]]:
    """
    Discount for isolated-fiber products that inflate fiber metrics
    without structural grain basis.

    Isolated extracted fiber (inulin, psyllium, cellulose, guar) misleads
    glycemic_quality and nutrient_density when the base matrix is refined.
    Discount is proportional to fiber load — more isolated fiber = more gaming.

    Does NOT penalize structural grain fiber.
    Hybrid systems (real grain + isolated additive) receive a mild discount.
    """
    fiber_result = bakery_semantics.get("fiber_source_quality") or {}
    fiber_q = fiber_result.get("fiber_source_quality", "unknown")

    l1 = trace.get("L1_observed_signals") or {}
    fiber_g = l1.get("dietary_fiber_g") or 0

    if fiber_q == "isolated":
        if fiber_g >= 6:
            disc = -14.0
            reason = f"isolated_fiber_high: {fiber_g}g entirely from extracted sources (inulin/psyllium/cellulose/guar) — no structural grain basis"
        elif fiber_g >= 4:
            disc = -10.0
            reason = f"isolated_fiber_moderate: {fiber_g}g from extracted sources — additive-origin fiber inflates nutrient scores"
        elif fiber_g >= 2:
            disc = -7.0
            reason = f"isolated_fiber_low_mod: {fiber_g}g from extracted sources"
        else:
            disc = -4.0
            reason = f"isolated_fiber_low: {fiber_g}g — additive-origin even at low quantity"
        return disc, [reason]

    if fiber_q == "hybrid":
        markers = fiber_result.get("isolated_fiber_markers") or []
        marker_str = ", ".join(markers[:3]) if markers else "unspecified"
        return -4.0, [
            f"hybrid_fiber: whole-grain base + isolated additives ({marker_str}) — partial inflation of fiber metrics"
        ]

    if fiber_q == "structural" and fiber_g >= 6:
        return 1.5, [
            f"structural_fiber_bonus: {fiber_g}g confirmed from grain matrix — genuine fiber, not additive compensation"
        ]

    return 0.0, []


# ===========================================================================
# Component 2: Fermentation quality credit (bakery only)
# ===========================================================================

def _fermentation_credit(bakery_semantics: dict) -> tuple[float, list[str]]:
    """
    Credit/penalty for fermentation quality.

    Traditional fermentation modestly supports structural coherence.
    Credit is gated on flour coherence: traditional ferm on refined flour
    earns less credit than the same ferm on whole-grain base.

    Does NOT over-reward mere מחמצת token presence.
    Flavor-only and theater sourdough receive synthesis penalties.
    """
    ferm_result = bakery_semantics.get("fermentation_quality") or {}
    ferm_q = ferm_result.get("fermentation_quality", "none")

    flour_result = bakery_semantics.get("flour_hierarchy") or {}
    fqc = flour_result.get("flour_quality_class", 3)  # 1=best grain, 5=refined only

    if ferm_q == "traditional":
        if fqc <= 2:
            return 6.0, [f"fermentation_traditional+coherent_flour: fqc={fqc} (whole-grain dominant) + genuine sourdough — full credit"]
        elif fqc == 3:
            return 4.0, [f"fermentation_traditional+mixed_flour: fqc={fqc} (mixed) + genuine sourdough"]
        else:
            return 2.0, [f"fermentation_traditional+refined_flour: fqc={fqc} (refined base) + genuine sourdough — reduced coherence credit"]

    if ferm_q == "mixed_industrial":
        return 1.5, ["fermentation_mixed_industrial: partial fermentation benefit (sourdough starter + commercial yeast)"]

    if ferm_q == "flavor_only":
        return -3.0, ["fermentation_flavor_only: sourdough is a flavor additive, not a leavening system — commercial yeast does actual leavening"]

    if ferm_q == "theater":
        return -5.0, ["fermentation_theater: name claims sourdough but no sourdough ingredient detected — deceptive signal"]

    return 0.0, []  # "none" — no adjustment


# ===========================================================================
# Component 3: GSS coherence adjustment (bakery only)
# ===========================================================================

def _gss_coherence_adjustment(bakery_semantics: dict, structural_class: dict) -> tuple[float, list[str]]:
    """
    Use Grain Structure Score to amplify structural gradients.

    Upward adjustments: reserved for class A/B/C products with high GSS.
    These products compress toward D-class in the base score despite
    genuinely superior structural construction.

    Downward adjustments: applied to class D/E/F with low GSS.
    Low GSS confirms structural incoherence — degraded matrix + isolated
    signals warrant stronger synthesis penalty.

    Class D products do NOT receive upward GSS adjustment —
    D-class structural issues are multifactorial beyond flour quality alone.
    """
    gss = bakery_semantics.get("grain_structure_score")
    if gss is None:
        return 0.0, []

    sc = (structural_class or {}).get("primary") or "D"

    if gss >= 85:
        if sc in ("A", "B"):
            return 6.0, [f"gss_coherence_high: gss={gss:.0f}, class={sc} → confirmed exceptional coherent structure"]
        elif sc == "C":
            return 3.0, [f"gss_coherence_high: gss={gss:.0f}, class=C → mechanically fragmented but structurally sound grain base"]
        else:
            return 0.0, []

    elif gss >= 70:
        if sc in ("A", "B"):
            return 4.0, [f"gss_coherence_good: gss={gss:.0f}, class={sc} → well-constructed grain product"]
        elif sc == "C":
            return 2.5, [f"gss_coherence_good: gss={gss:.0f}, class=C → good grain structure at C level"]
        else:
            return 0.0, []

    elif gss >= 55:
        if sc in ("A", "B"):
            return 2.0, [f"gss_coherence_moderate: gss={gss:.0f}, class={sc} → decent coherence"]
        elif sc == "C":
            return 0.5, [f"gss_coherence_moderate: gss={gss:.0f}, class=C → moderate coherence signal"]
        else:
            return 0.0, []

    elif gss >= 40:
        return 0.0, []  # neutral zone for all classes

    elif gss >= 25:
        if sc in ("D", "E", "F"):
            return -4.0, [f"gss_incoherence_moderate: gss={gss:.0f}, class={sc} → structural incoherence confirmed"]
        elif sc == "C":
            return -2.0, [f"gss_incoherence_moderate: gss={gss:.0f}, class=C — unexpected, possible signal tension"]
        else:
            return 0.0, []

    elif gss >= 12:
        if sc in ("D", "E", "F"):
            return -7.0, [f"gss_incoherence_high: gss={gss:.0f}, class={sc} → severe structural incoherence"]
        elif sc == "C":
            return -4.0, [f"gss_incoherence_high: gss={gss:.0f}, class=C — high for C class"]
        elif sc in ("A", "B"):
            return -3.0, [f"gss_class_contradiction: gss={gss:.0f} very low but class={sc} — conflicting signals, applying mild penalty"]
        else:
            return 0.0, []

    else:  # gss < 12
        if sc in ("D", "E", "F"):
            return -10.0, [f"gss_incoherence_severe: gss={gss:.0f}, class={sc} → structurally void / isolated-matrix system confirmed"]
        elif sc == "C":
            return -6.0, [f"gss_incoherence_severe: gss={gss:.0f}, class=C — extreme structural mismatch"]
        else:
            return -3.0, [f"gss_incoherence_severe: gss={gss:.0f}, class={sc} — contradiction, applying minimal flag penalty"]


# ===========================================================================
# Component 4: Engineering type nuance (all categories)
# ===========================================================================

def _engineering_nuance(trace: dict, bakery_semantics: dict | None, structural_class: dict | None) -> tuple[float, list[str]]:
    """
    Distinguish engineering intent: functional/therapeutic vs deceptive.

    Gluten-free and keto products have STRUCTURAL LIMITATIONS by necessity —
    they cannot use the same flour matrix as conventional products.
    Critically, when these products also use isolated fiber, the isolation is
    a DIETARY NECESSITY (psyllium in keto, starch substitutes in GF), NOT
    the same signal as fiber-laundering in a refined wheat cracker.

    The nuance credit is therefore scaled up when fiber_q=isolated AND the
    product is functionally engineered — partially offsetting the fiber discount.

    F-class hyper-palatable systems with sweetener stacking receive
    an additional synthesis penalty confirming the void interpretation.

    Applies to class D, E, and F only.
    """
    sc = (structural_class or {}).get("primary") or "D"
    if sc not in ("D", "E", "F"):
        return 0.0, []

    l3 = trace.get("L3_inferred_classifications") or {}
    l1 = trace.get("L1_observed_signals") or {}
    ref = trace.get("input_reference") or {}
    name = (ref.get("product_name_he") or ref.get("canonical_name_he") or "").lower()

    protein_src = l3.get("protein_source", "unknown")
    sweetener   = bool(l3.get("sweetener_detected", False))
    add_ct      = l3.get("additive_marker_count", 0)
    carbs_g     = l1.get("carbohydrates_g") or 0
    fat_g       = l1.get("fat_g") or 0
    fiber_g     = l1.get("dietary_fiber_g") or 0

    # Fiber context from bakery_semantics (if available)
    fiber_q = "unknown"
    if bakery_semantics:
        fiber_q = (bakery_semantics.get("fiber_source_quality") or {}).get("fiber_source_quality", "unknown")

    is_gluten_free = "ללא גלוטן" in name or "gluten free" in name or "gluten-free" in name
    is_keto = ("קטו" in name or "keto" in name or "דל פחמימות" in name or
               (carbs_g < 10 and fat_g > 20 and fiber_g > 5))
    is_protein_functional = (protein_src == "isolate" and not sweetener and add_ct <= 3)
    is_hyper_palatable = (sweetener and add_ct >= 3 and protein_src != "isolate")

    if sc in ("D", "E"):
        if is_gluten_free:
            if fiber_q == "isolated":
                # GF bread must use starch/fiber substitutes — isolated fiber is structural necessity
                return 7.0, [
                    f"engineering_nuance: gluten-free + isolated_fiber = structural necessity (class={sc}). "
                    "Fiber additives are format-required, not gaming — offsetting fiber discount."
                ]
            return 3.0, [f"engineering_nuance: gluten-free = structural limitation by dietary necessity (class={sc})"]

        if is_keto:
            if fiber_q == "isolated":
                # Keto baking requires psyllium/coconut fiber — not the same as refined-wheat fiber laundering
                return 8.0, [
                    f"engineering_nuance: keto + isolated_fiber = dietary structural necessity (class={sc}). "
                    "Psyllium/fiber additives are inherent to keto format — offsetting fiber discount."
                ]
            return 2.0, [f"engineering_nuance: keto/low-carb = therapeutic engineering purpose (class={sc})"]

    if sc == "E":
        if is_protein_functional:
            return 1.5, ["engineering_nuance: protein engineering = nutritional intent (isolate + no sweetener + clean label)"]
        return 0.0, []

    if sc == "F":
        if is_hyper_palatable:
            return -3.0, ["engineering_nuance: hyper-palatable reconstruction confirmed (sweetener+additives+non-protein) — amplifying void signal"]
        return 0.0, []

    return 0.0, []


# ===========================================================================
# Component 5: Synthesis confidence
# ===========================================================================

def _compute_synthesis_confidence(bakery_semantics: dict | None, trace: dict, category: str) -> dict:
    """
    Estimate certainty of the synthesis interpretation.

    High confidence: signals align clearly (coherent grain + structural fiber + traditional ferm,
    OR: incoherent base + isolated fiber + low GSS).

    Low confidence: conflicting signals (genuine fermentation but isolated fiber,
    high GSS but isolated fiber additive).

    Medium: everything else.
    """
    if bakery_semantics is None:
        return {
            "synthesis_confidence": "medium",
            "confidence_factors": ["non_bakery_category: synthesis limited to engineering nuance"],
        }

    gss     = bakery_semantics.get("grain_structure_score")
    ferm_q  = (bakery_semantics.get("fermentation_quality") or {}).get("fermentation_quality", "none")
    fiber_q = (bakery_semantics.get("fiber_source_quality") or {}).get("fiber_source_quality", "unknown")
    fqc     = (bakery_semantics.get("flour_hierarchy") or {}).get("flour_quality_class", 3)
    markers = (bakery_semantics.get("fiber_source_quality") or {}).get("isolated_fiber_markers") or []

    factors: list[str] = []

    # High confidence: clear coherent structure
    if (gss is not None and gss >= 70 and
            ferm_q in ("traditional", "none") and
            fiber_q in ("structural", "minimal") and
            fqc <= 3):
        return {"synthesis_confidence": "high",
                "confidence_factors": ["strong_alignment: high_gss + structural_fiber + coherent_flour"]}

    # High confidence: clear incoherent structure
    if (gss is not None and gss <= 20 and fiber_q == "isolated" and fqc >= 4):
        return {"synthesis_confidence": "high",
                "confidence_factors": ["strong_alignment: low_gss + isolated_fiber + refined_flour (structural incoherence clear)"]}

    # High confidence: classic traditional sourdough whole-grain
    if (ferm_q == "traditional" and fqc <= 2 and gss is not None and gss >= 75):
        return {"synthesis_confidence": "high",
                "confidence_factors": ["strong_alignment: traditional_fermentation + whole_grain_dominant + high_gss"]}

    # Low confidence: conflicting signals
    if ferm_q == "traditional" and fiber_q == "isolated":
        factors.append("signal_conflict: traditional_fermentation + isolated_fiber (unusual — fermentation may not offset additive fiber)")
        return {"synthesis_confidence": "low", "confidence_factors": factors}

    if gss is not None and gss >= 60 and fiber_q == "isolated":
        factors.append("signal_conflict: high_gss but isolated_fiber (FQC position proxy may overstate grain quality)")
        return {"synthesis_confidence": "low", "confidence_factors": factors}

    if ferm_q == "theater" and fiber_q == "structural":
        factors.append("signal_conflict: theater_fermentation but structural_fiber")
        return {"synthesis_confidence": "low", "confidence_factors": factors}

    # Medium: gather any notable conditions
    if gss is None:
        factors.append("gss_unavailable")
    if fiber_q == "hybrid":
        factors.append("fiber_ambiguity: hybrid system (structural + isolated)")
    if ferm_q == "mixed_industrial":
        factors.append("fermentation_ambiguity: mixed leavening system")
    if not factors:
        factors.append("standard_medium_confidence")

    return {"synthesis_confidence": "medium", "confidence_factors": factors}


# ===========================================================================
# Main synthesis function
# ===========================================================================

def run_synthesis(trace: dict) -> dict:
    """
    Run score synthesis calibration on an assembled BSIP2 trace.

    Input:  full trace dict (after score_engine + bakery_semantics + structural_class attached)
    Output: synthesis_result dict

    synthesized_score replaces final_score_estimate as the preferred output
    in synthesis-aware runners. The base score is preserved in synthesis_result.
    """
    base_score = trace.get("final_score_estimate")

    if base_score is None:
        return {
            "synthesized_score":        None,
            "synthesis_version":        SYNTHESIS_VERSION,
            "synthesis_skipped_reason": "no_base_score",
        }

    category        = trace.get("category") or "default"
    bakery_sem      = trace.get("bakery_semantics")
    structural_cls  = trace.get("structural_class")

    adjustments: list[dict] = []
    total_adj = 0.0

    # ── Bakery-specific synthesis components ──────────────────────────────
    if bakery_sem is not None:

        fiber_adj, fiber_drivers = _fiber_discount(bakery_sem, trace)
        if fiber_adj != 0.0:
            adjustments.append({"component": "fiber_source_quality",
                                 "adjustment": fiber_adj, "drivers": fiber_drivers})
            total_adj += fiber_adj

        ferm_adj, ferm_drivers = _fermentation_credit(bakery_sem)
        if ferm_adj != 0.0:
            adjustments.append({"component": "fermentation_quality",
                                 "adjustment": ferm_adj, "drivers": ferm_drivers})
            total_adj += ferm_adj

        gss_adj, gss_drivers = _gss_coherence_adjustment(bakery_sem, structural_cls)
        if gss_adj != 0.0:
            adjustments.append({"component": "gss_coherence",
                                 "adjustment": gss_adj, "drivers": gss_drivers})
            total_adj += gss_adj

    # ── Engineering nuance (all categories) ──────────────────────────────
    eng_adj, eng_drivers = _engineering_nuance(trace, bakery_sem, structural_cls)
    if eng_adj != 0.0:
        adjustments.append({"component": "engineering_nuance",
                             "adjustment": eng_adj, "drivers": eng_drivers})
        total_adj += eng_adj

    # ── Clamp total adjustment ────────────────────────────────────────────
    total_adj_raw = total_adj
    total_adj = max(-SYNTHESIS_MAX_DOWNWARD, min(SYNTHESIS_MAX_UPWARD, total_adj))
    was_clamped = abs(total_adj_raw - total_adj) > 0.01

    # ── Apply adjustment ──────────────────────────────────────────────────
    raw_synth = base_score + total_adj
    synthesized_score = round(
        max(SYNTHESIS_SCORE_FLOOR, min(SYNTHESIS_SCORE_CEIL, raw_synth)), 1
    )

    # ── Synthesis confidence ──────────────────────────────────────────────
    conf = _compute_synthesis_confidence(bakery_sem, trace, category)

    # ── Grade ─────────────────────────────────────────────────────────────
    from constants import score_to_grade  # local import to avoid circular dep
    synthesized_grade = score_to_grade(synthesized_score)
    base_grade        = score_to_grade(base_score)

    return {
        "base_score":             round(base_score, 1),
        "base_grade":             base_grade,
        "synthesized_score":      synthesized_score,
        "synthesized_grade":      synthesized_grade,
        "total_adjustment":       round(total_adj, 2),
        "total_adj_before_clamp": round(total_adj_raw, 2),
        "adjustment_clamped":     was_clamped,
        "synthesis_adjustments":  adjustments,
        "synthesis_confidence":   conf,
        "synthesis_version":      SYNTHESIS_VERSION,
    }
