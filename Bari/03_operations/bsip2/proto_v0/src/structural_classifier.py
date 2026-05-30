"""
BSIP2 Structural Classifier v1

Assigns structural food classes from a BSIP2 trace.
Structural classes describe HOW a food was physically constructed.
They are ontology anchors, not marketing labels, and are distinct from
BSIP2 v3 scoring archetypes (cereal_system, dairy_liquid, etc.).

Input:  assembled BSIP2 trace dict (or minimal signal bundle)
Output: soft assignment with primary/secondary structural class + confidence weights

A product may partially express multiple structural classes.
Classification uses trace signals: nova_proxy, dimension_scores, L1/L3 signals.
"""

from __future__ import annotations

MODULE_VERSION = "structural_classifier_v1"


# ---------------------------------------------------------------------------
# Structural class definitions
# ---------------------------------------------------------------------------

STRUCTURAL_CLASSES: dict[str, dict] = {
    "A": {
        "code": "A",
        "label": "Intact Whole Food",
        "description": "Minimal processing; original food structure fully preserved",
        "examples": ["whole milk", "plain nuts", "whole oats", "plain legumes", "single-ingredient produce"],
    },
    "B": {
        "code": "B",
        "label": "Lightly Transformed Traditional",
        "description": "Traditional processing; structure mostly intact; no industrial restructuring",
        "examples": ["plain yogurt", "rolled oats", "roasted nuts", "sourdough bread", "date-nut bars", "kefir"],
    },
    "C": {
        "code": "C",
        "label": "Mechanically Fragmented",
        "description": "Physical breakdown of whole foods; structure disrupted but not chemically restructured",
        "examples": ["oat flour products", "nut butters", "compressed fruit-nut bars", "stone-ground grain products"],
    },
    "D": {
        "code": "D",
        "label": "Industrially Reconstructed",
        "description": "Significant industrial processing; matrix disrupted, reassembled, emulsified, or stabilized",
        "examples": ["puffed cereals", "oat drinks with gums", "extruded snacks", "engineered granola clusters"],
    },
    "E": {
        "code": "E",
        "label": "Engineered Wellness System",
        "description": "Heavily engineered; nutritional compensation for stripped food matrix via isolates and fortification",
        "examples": ["protein bars with isolates", "high-protein dairy drinks", "fortified meal-replacement systems"],
    },
    "F": {
        "code": "F",
        "label": "Structurally Void System",
        "description": "Minimal food matrix; primarily engineered for palatability; high additive and sweetener load",
        "examples": ["syrup-dominant clusters", "candy-proximate bars", "hyper-sweetened puffed products"],
    },
}

# Expected score bands per structural class (informational — used in regression reports)
STRUCTURAL_CLASS_SCORE_BANDS: dict[str, tuple[float, float]] = {
    "A": (85.0, 100.0),
    "B": (72.0, 100.0),
    "C": (52.0, 84.0),
    "D": (35.0, 72.0),
    "E": (25.0, 65.0),
    "F": (10.0, 48.0),
}


# ---------------------------------------------------------------------------
# Core classification
# ---------------------------------------------------------------------------

def classify_structural_class(trace: dict, bakery_semantics: dict | None = None) -> dict:
    """
    Classify a product into structural classes from its BSIP2 trace.

    Returns:
        primary, primary_label, primary_confidence
        secondary, secondary_label, secondary_confidence (if meaningful)
        class_weights       — normalized fit scores for all 6 structural classes
        classification_notes — human-readable signal drivers
        classifier_version
    """
    # Guard: out-of-scope or no score
    if trace.get("evaluation_status") == "out_of_scope":
        return _unclassifiable("out_of_scope")
    if trace.get("final_score_estimate") is None and "signal_bundle" not in trace:
        return _unclassifiable("no_score")

    # Extract signals
    nova        = _safe_int(trace.get("nova_proxy"), default=2)
    dim         = trace.get("dimension_scores") or {}
    aq          = _safe_float(dim.get("additive_quality"), default=82.0)
    wfi         = _safe_float(dim.get("whole_food_integrity"), default=60.0)
    pq          = _safe_float(dim.get("protein_quality"), default=50.0)
    l3          = trace.get("L3_inferred_classifications") or {}
    l1          = trace.get("L1_observed_signals") or {}
    protein_src = l3.get("protein_source", "unknown")
    ing_count   = _safe_int(l1.get("ingredient_count"), default=5)
    sweetener   = bool(l3.get("sweetener_detected", False))
    add_ct      = _safe_int(l3.get("additive_marker_count"), default=0)

    # Compute raw fit scores
    raw = _compute_fits(nova, aq, wfi, pq, protein_src, ing_count, sweetener, add_ct)

    # Bakery semantics rebalancing (optional — only for bread/cracker/crispbread categories)
    if bakery_semantics:
        raw = _apply_bakery_rebalance(raw, bakery_semantics, trace)

    # Normalize
    total = sum(raw.values())
    if total <= 0:
        return _unclassifiable("zero_fit")
    weights = {k: round(v / total, 3) for k, v in raw.items()}

    # Primary: highest weight
    primary = max(weights, key=lambda k: weights[k])

    # Secondary: highest weight that is meaningfully different from primary
    remaining = {k: w for k, w in weights.items() if k != primary and w >= 0.18}
    secondary = max(remaining, key=lambda k: weights[k]) if remaining else None

    # Classification notes (human-readable signal drivers)
    notes = _build_notes(nova, aq, wfi, pq, protein_src, ing_count, sweetener, add_ct, primary)

    return {
        "primary":            primary,
        "primary_label":      STRUCTURAL_CLASSES[primary]["label"],
        "primary_confidence": weights[primary],
        "secondary":          secondary,
        "secondary_label":    STRUCTURAL_CLASSES[secondary]["label"] if secondary else None,
        "secondary_confidence": weights[secondary] if secondary else None,
        "class_weights":      weights,
        "is_between_worlds":  secondary is not None and weights.get(secondary, 0) >= 0.25,
        "classification_notes": notes,
        "classifier_version": MODULE_VERSION,
    }


def _compute_fits(
    nova: int,
    aq: float,
    wfi: float,
    pq: float,
    protein_src: str,
    ing_count: int,
    sweetener: bool,
    add_ct: int,
) -> dict[str, float]:
    """Return unnormalized fit scores for each structural class. Floor at 0."""

    A = B = C = D = E = F = 0.0

    # --- NOVA level (most important discriminator) ---
    if nova == 1:
        A += 0.45; B += 0.20
    elif nova == 2:
        A += 0.05; B += 0.35; C += 0.25
    elif nova == 3:
        C += 0.15; D += 0.35; E += 0.15
    else:  # 4
        D += 0.15; E += 0.20; F += 0.30

    # --- Additive quality (reflects additive load) ---
    if aq >= 100:      # no additives
        A += 0.25; B += 0.10
    elif aq >= 82:     # ≤1 additive category
        B += 0.20; C += 0.10
    elif aq >= 64:     # 1-2 categories
        C += 0.20; D += 0.10
    elif aq >= 46:     # 2-3 categories
        D += 0.25; E += 0.10
    else:              # 3+ categories
        D += 0.10; E += 0.25; F += 0.25

    # --- Whole food integrity ---
    if wfi >= 90:
        A += 0.20; B += 0.10
    elif wfi >= 75:
        B += 0.20; C += 0.10
    elif wfi >= 55:
        C += 0.15; D += 0.10
    elif wfi >= 35:
        D += 0.20; E += 0.10
    else:
        E += 0.15; F += 0.20

    # --- Protein source ---
    if protein_src == "isolate":
        E += 0.35
        A -= 0.10; B -= 0.10   # isolate = not a natural food matrix
    elif protein_src == "whole_food":
        A += 0.05; B += 0.05
    # "mixed" is neutral

    # --- Sweetener ---
    if sweetener:
        E += 0.05; F += 0.10
        A -= 0.15; B -= 0.10
    else:
        A += 0.03; B += 0.03

    # --- Additive marker count (finer-grained than aq) ---
    if add_ct == 0:
        A += 0.05; B += 0.05
    elif add_ct >= 5:
        E += 0.10; F += 0.10
    elif add_ct >= 3:
        D += 0.05; E += 0.10

    # --- Ingredient count ---
    if ing_count <= 1:
        A += 0.12
    elif ing_count <= 3:
        A += 0.05; B += 0.05; C += 0.02
    elif ing_count <= 8:
        B += 0.03; C += 0.05; D += 0.03
    elif ing_count <= 15:
        C += 0.03; D += 0.05; E += 0.03
    else:
        D += 0.03; E += 0.05; F += 0.05

    # --- Protein quality dimension (E vs F discriminator) ---
    # E is "engineering with nutritional intent"; F is "palatability without protein".
    if pq >= 35:
        E += 0.15        # meaningful protein = wellness signal
    if pq >= 55:
        E += 0.10        # additional boost for high protein scores

    # Heavy non-sweetener additive load → engineering intent (not palatability)
    if not sweetener and nova >= 3 and add_ct >= 4:
        E += 0.20

    # Sweetener + low protein + whole-food source = palatability-first (F, not E)
    if sweetener and pq < 30 and protein_src != "isolate":
        F += 0.15

    # Downweight E when protein is low and source is whole-food (not an engineered wellness product)
    if protein_src == "whole_food" and pq < 30:
        E *= 0.65

    # Downweight B when all strong A signals are present (fermented dairy is B, not A)
    if nova == 1 and aq >= 100 and wfi >= 90:
        B *= 0.45

    return {
        "A": max(0.0, A),
        "B": max(0.0, B),
        "C": max(0.0, C),
        "D": max(0.0, D),
        "E": max(0.0, E),
        "F": max(0.0, F),
    }


def _build_notes(nova, aq, wfi, pq, protein_src, ing_count, sweetener, add_ct, primary) -> list[str]:
    notes = []
    notes.append(f"nova_{nova}_signal")
    if aq >= 100:
        notes.append("no_additives_detected")
    elif aq < 46:
        notes.append("high_additive_load")
    if wfi >= 90:
        notes.append("whole_food_integrity_intact")
    elif wfi < 40:
        notes.append("whole_food_integrity_low")
    if protein_src == "isolate":
        notes.append("protein_isolate_detected")
    if pq >= 55:
        notes.append("high_protein_quality")
    elif pq >= 35:
        notes.append("moderate_protein_quality")
    if sweetener:
        notes.append("sweetener_detected")
    if ing_count <= 2:
        notes.append("minimal_ingredients")
    elif ing_count >= 15:
        notes.append("high_complexity_assembly")
    if add_ct == 0:
        notes.append("zero_additive_categories")
    return notes


def _unclassifiable(reason: str) -> dict:
    return {
        "primary":            None,
        "primary_label":      None,
        "primary_confidence": None,
        "secondary":          None,
        "secondary_label":    None,
        "secondary_confidence": None,
        "class_weights":      None,
        "is_between_worlds":  False,
        "classification_notes": [f"unclassifiable: {reason}"],
        "classifier_version": MODULE_VERSION,
    }


def _apply_bakery_rebalance(raw: dict, bakery_semantics: dict, trace: dict | None = None) -> dict:
    """
    Adjust structural class weights using bakery-specific semantic signals.
    Called only when bakery_semantics is not None (bread/cracker/crispbread).

    Principle: NOVA3 gravity is too strong for genuine whole-grain bakery products.
    Fermentation quality and flour hierarchy provide finer discrimination.
    """
    r = dict(raw)   # copy

    flour  = bakery_semantics.get("flour_hierarchy") or {}
    ferm   = bakery_semantics.get("fermentation_quality") or {}
    fiber  = bakery_semantics.get("fiber_source_quality") or {}

    fqc    = flour.get("flour_quality_class", 3)   # 1=best, 5=worst
    ferm_q = ferm.get("fermentation_quality", "none")
    fiber_q = fiber.get("fiber_source_quality", "unknown")

    # ── Flour quality rebalancing ─────────────────────────────────────────
    if fqc <= 2:
        # Dominant whole grain → reduce D gravity, boost B/C
        r["D"] = max(0.0, r["D"] - 0.12)
        r["B"] += 0.10
        r["C"] += 0.04
    elif fqc == 4:
        # Refined dominant (decorative WG) → boost D, reduce B
        r["D"] += 0.08
        r["B"] = max(0.0, r["B"] - 0.08)
    elif fqc == 5:
        # Pure refined → strong D/E signal
        r["D"] += 0.12
        r["C"] += 0.05
        r["B"] = max(0.0, r["B"] - 0.10)

    # ── Fermentation quality rebalancing ────────────────────────────────
    if ferm_q == "traditional":
        # Genuine sourdough — lightly transformed traditional food
        r["B"] += 0.22
        r["D"] = max(0.0, r["D"] - 0.15)
        r["C"] += 0.05
    elif ferm_q == "mixed_industrial":
        # Some fermentation benefit, but hybrid system
        r["C"] += 0.08
        r["D"] = max(0.0, r["D"] - 0.06)
    elif ferm_q == "flavor_only":
        # Sourdough as flavor additive — no fermentation benefit
        r["D"] += 0.08
        r["B"] = max(0.0, r["B"] - 0.06)
    elif ferm_q == "theater":
        # Pure marketing — no sourdough ingredient
        r["D"] += 0.10
        r["E"] += 0.05
        r["B"] = max(0.0, r["B"] - 0.08)

    # ── Fiber source rebalancing ──────────────────────────────────────────
    if fiber_q == "isolated":
        # Isolated fiber only — engineering, not grain structure
        r["E"] += 0.15
        r["B"] = max(0.0, r["B"] - 0.10)
        r["C"] = max(0.0, r["C"] - 0.05)
    elif fiber_q == "hybrid":
        # Mixed: some engineering alongside genuine grain
        r["D"] += 0.05
        r["E"] += 0.05
        r["B"] = max(0.0, r["B"] - 0.05)

    # ── E bias correction for non-engineered bakery products ─────────────────
    # _compute_fits uses "pq >= 35 → E += 0.15" as a proxy for wellness engineering.
    # That heuristic was calibrated for protein bars/shakes with isolates.
    # For bakery products with naturally high protein from whole grains or seeds,
    # the E class ("Engineered Wellness System") is inappropriate.
    # Reduce E when: flour is reasonable quality AND fiber is structural (not assembled).
    protein_src = (trace or {}).get("L3_inferred_classifications", {}).get("protein_source", "unknown") if trace else "unknown"
    if fqc <= 3 and fiber_q in ("structural", "minimal", "unknown") and protein_src == "whole_food":
        r["E"] = max(0.0, r["E"] - 0.18)
        r["B"] += 0.06
        r["C"] += 0.04

    # Ensure all values stay non-negative
    return {k: max(0.0, v) for k, v in r.items()}


def _safe_float(val, default: float = 0.0) -> float:
    try:
        return float(val) if val is not None else default
    except (TypeError, ValueError):
        return default


def _safe_int(val, default: int = 0) -> int:
    try:
        return int(val) if val is not None else default
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Corpus helper: classify a synthetic signal bundle (for regression testing)
# ---------------------------------------------------------------------------

def classify_from_bundle(bundle: dict) -> dict:
    """
    Classify from a minimal signal bundle dict (no full BSIP2 trace needed).
    Bundle keys: nova_proxy, additive_quality, whole_food_integrity, protein_quality,
                 protein_source, ingredient_count, sweetener_detected, additive_marker_count
    """
    synthetic_trace = {
        "evaluation_status": "standard",
        "final_score_estimate": 0,  # placeholder to avoid unclassifiable gate
        "nova_proxy": bundle.get("nova_proxy", 2),
        "dimension_scores": {
            "additive_quality":     bundle.get("additive_quality", 82.0),
            "whole_food_integrity": bundle.get("whole_food_integrity", 60.0),
            "protein_quality":      bundle.get("protein_quality", 50.0),
        },
        "L3_inferred_classifications": {
            "protein_source":        bundle.get("protein_source", "unknown"),
            "sweetener_detected":    bundle.get("sweetener_detected", False),
            "additive_marker_count": bundle.get("additive_marker_count", 0),
        },
        "L1_observed_signals": {
            "ingredient_count": bundle.get("ingredient_count", 5),
        },
    }
    return classify_structural_class(synthetic_trace)
