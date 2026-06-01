"""
BSIP2 Matrix Integrity Engine v2
Calibration + Provenance Hardening sprint.

Changes from v1:
  - Supplemental mechanical transform scan: soft-degradation signals for
    rolled oats, granola, flaked grains not captured by BSIP1 MATRIX_TERMS.
  - Assembly complexity drag (0-12 flat penalty): ingredient count + diversity.
  - Fortification nuance: basic_restoration vs wellness_engineering.
  - HP triad v2: position weighting, matrix-weakness amplification,
    single-flavor false-positive suppression.
  - Transformation type classification (A/B/C/D).
  - Rich provenance trace block (degradation / engineering / compensation /
    protective signal lists in human-readable form).
  - Score formula: 100 - deg*0.55 - eng*0.30 - hp*0.15 - assembly_drag

Consumes:
  ingredient_order, extracted_matrix_markers, extracted_additives,
  extracted_protein_markers, extracted_sweeteners, extracted_flavors,
  extracted_fermentation_markers, extracted_roasting_markers

Output fields: unchanged from v1 (matrix_integrity_trace gains new keys).
"""

from __future__ import annotations
from typing import Optional

MODULE_VERSION = "matrix_integrity_v2"


# ---------------------------------------------------------------------------
# Position weight function (unchanged from v1)
# ---------------------------------------------------------------------------

def _pos_weight(pos: Optional[int]) -> float:
    if pos is None:
        return 0.12
    if pos == 1:  return 1.00
    if pos == 2:  return 0.82
    if pos == 3:  return 0.68
    if pos == 4:  return 0.55
    if pos == 5:  return 0.44
    if pos == 6:  return 0.35
    if pos == 7:  return 0.28
    if pos == 8:  return 0.22
    if pos == 9:  return 0.17
    if pos == 10: return 0.13
    if pos <= 15: return max(0.08, 0.13 * (0.85 ** (pos - 10)))
    return 0.08


# ---------------------------------------------------------------------------
# Matrix degradation scores (unchanged from v1)
# ---------------------------------------------------------------------------

MATRIX_DEGRADATION_SCORES: dict[str, float] = {
    "oat_flakes":        20,
    "wheat_flakes":      28,
    "corn_flakes":       48,
    "flakes_generic":    30,
    "whole_wheat_flour": 52,
    "whole_rye_flour":   48,
    "spelt_flour":       55,
    "wheat_flour":       70,
    "rye_flour":         62,
    "oat_flour":         65,
    "rice_flour":        65,
    "corn_flour":        65,
    "flour_generic":     68,
    "potato_starch":     82,
    "corn_starch":       82,
    "wheat_starch":      82,
    "rice_starch":       80,
    "modified_starch":   90,
    "starch_generic":    78,
    "puffed_cereal":     80,
    "puffed_rice":       78,
    "puffed_barley":     76,
    "puffed_corn":       82,
    "puffed":            80,
    "expanded":          85,
    "crisped_cereal":    80,
    "rice_cakes":        62,
    "crunchy_pieces":    75,
    "maltodextrin":      92,
    "dextrin":           85,
    "dextrose":          88,
}

_GENERIC_MATRIX_CATEGORIES = frozenset({
    "flour_generic", "starch_generic", "puffed_cereal", "flakes_generic",
})

_STRUCTURAL_VOID_SWEETENERS = frozenset({
    "glucose_syrup", "corn_syrup", "invert_sugar_syrup", "invert_sugar",
    "added_sugar", "brown_sugar", "maple_syrup", "date_syrup", "agave_syrup",
    "sugar_syrup", "rice_syrup", "malt_syrup", "molasses",
})

_INDUSTRIAL_MATRIX_CATEGORIES = frozenset({
    "puffed_cereal", "puffed_rice", "puffed_barley", "puffed_corn",
    "puffed", "expanded", "crisped_cereal",
})

_MECHANICAL_MATRIX_CATEGORIES = frozenset({
    "wheat_flour", "whole_wheat_flour", "whole_rye_flour", "spelt_flour",
    "oat_flour", "rice_flour", "corn_flour", "rye_flour", "flour_generic",
    "corn_starch", "wheat_starch", "potato_starch", "rice_starch",
    "modified_starch", "starch_generic", "maltodextrin", "dextrin", "dextrose",
})


# ---------------------------------------------------------------------------
# NEW v2: Supplemental mechanical transformation patterns
# Scanned directly in ingredient_order text for signals the BSIP1 enricher
# does not capture. Applied only where no matrix_marker was already detected.
# Scores are intentionally low — these are mild structural friction signals.
# ---------------------------------------------------------------------------

_MECHANICAL_TRANSFORM_PATTERNS: list[tuple[str, float, str]] = [
    # (Hebrew substring in ingredient text, soft_degradation_score, label)
    ("שיבולת שועל",  6.0, "rolled_oats"),         # Mechanically flattened oat kernel
    ("פתיתי",       10.0, "flaked_grain"),          # Flaking of grain (generic)
    ("גרנולה",      16.0, "granola_clusters"),      # Oil + heat + syrup binding of oat clusters
    ("מוזלי",        8.0, "muesli_blend"),           # Mixed flake assembly, gentle
    ("פופקורן",     52.0, "popcorn"),                # Heat-expanded popped corn
    ("תירס מוגש",   28.0, "processed_sweetcorn"),   # Processed sweet corn form
]


# ---------------------------------------------------------------------------
# Fermentation credits (unchanged from v1)
# ---------------------------------------------------------------------------

FERMENTATION_CREDITS: dict[str, float] = {
    "live_cultures":      38,
    "live_bacteria":      38,
    "lb_bulgaricus":      30,
    "lb_acidophilus":     30,
    "lactobacillus":      28,
    "bifidobacterium":    30,
    "st_thermophilus":    26,
    "streptococcus":      22,
    "lactococcus":        22,
    "lactic_fermentation": 28,
    "starter_cultures":   25,
    "sourdough_starter":  25,
    "fermented":          18,
    "fermentation":       14,
    "cultures_generic":   18,
    "yeast":              10,
    "bread_yeast":        10,
}

_STRONG_FERMENTATION = frozenset({
    "live_cultures", "live_bacteria", "lb_bulgaricus", "lb_acidophilus",
    "bifidobacterium", "st_thermophilus", "sourdough_starter", "lactic_fermentation",
})


# ---------------------------------------------------------------------------
# Protein engineering scores (unchanged from v1)
# ---------------------------------------------------------------------------

PROTEIN_ENGINEERING_SCORES: dict[str, float] = {
    "hydrolyzed_protein":       88,
    "whey_protein_isolate":     85,
    "soy_protein_isolate":      88,
    "vital_wheat_gluten":       62,
    "wheat_gluten":             58,
    "whey_protein_concentrate": 65,
    "soy_protein_concentrate":  68,
    "pea_protein_concentrate":  65,
    "milk_protein_concentrate": 58,
    "rice_protein":             62,
    "potato_protein":           58,
    "pea_protein":              55,
    "casein":                   45,
    "soy_protein":              55,
    "wheat_protein":            52,
    "whey_protein":             50,
    "soy_powder":               45,
    "skim_milk_powder":         42,
    "milk_powder":              38,
    "milk_protein":             32,
    "milk_solids":              25,
    "whey":                     28,
    "lactalbumin":              30,
    "egg_albumen":              28,
    "albumin":                  32,
    "egg_white":                18,
}

_HIGH_ENGINEERING_THRESHOLD = 55


# ---------------------------------------------------------------------------
# Additive engineering signals (unchanged from v1)
# ---------------------------------------------------------------------------

ADDITIVE_ENGINEERING_SIGNALS: dict[str, float] = {
    "prebiotic_fiber":        22,
    "modified_starch":        16,
    "bulking_agent":          20,
    "humectant":              12,
    "flavor_enhancer":        15,
    "glazing_agent":           8,
    "emulsifier":             10,
    "stabilizer_thickener":    8,
}

_FORTIFICATION_TERMS_HE: list[str] = [
    "ניאצין", "ריבופלאבין", "תיאמין", "חומצה פולית", "ציאנוקובלמין",
    "פנטותנאט", "פירידוקסין", "ויטמין", "קולקלציפרול", "טוקופרול",
    "חומצה אסקורבית", "ברזל", "אבץ", "סידן", "ניאציינאמיד", "פריפוספט",
]


# ---------------------------------------------------------------------------
# Internal helpers — unchanged from v1
# ---------------------------------------------------------------------------

def _group_markers_by_position(markers: list[dict]) -> dict[Optional[int], list[dict]]:
    grouped: dict[Optional[int], list[dict]] = {}
    for m in markers:
        pos = m.get("position")
        grouped.setdefault(pos, []).append(m)
    return grouped


def _best_degradation_at_position(markers: list[dict]) -> tuple[float, str]:
    """
    Returns (score, category) for the highest-degradation specific marker at this position.
    v2: checks for explicit 'degradation_score' field first (supplemental signals);
        falls back to MATRIX_DEGRADATION_SCORES dict lookup.
    """
    categories = {m["category"] for m in markers}
    non_generic = categories - _GENERIC_MATRIX_CATEGORIES
    active_cats = non_generic if non_generic else categories

    best_score = 0.0
    best_cat = ""
    for m in markers:
        if m["category"] not in active_cats:
            continue
        # Supplemental signals carry an explicit score; dict markers use the lookup
        score = m.get("degradation_score") or MATRIX_DEGRADATION_SCORES.get(m["category"], 0)
        if score > best_score:
            best_score = score
            best_cat = m["category"]
    return best_score, best_cat


def _detect_fortification(ingredient_order: list[dict]) -> list[dict]:
    found = []
    seen: set[str] = set()
    for item in ingredient_order:
        text_lower = item["text"].lower()
        for term in _FORTIFICATION_TERMS_HE:
            if term.lower() in text_lower and term not in seen:
                if "e300" in text_lower or "e-300" in text_lower:
                    if term == "חומצה אסקורבית":
                        continue
                found.append({"term": term, "position": item["position"], "category": "fortification"})
                seen.add(term)
    return found


def _compute_matrix_degradation(
    matrix_markers: list[dict],
    ingredient_order: list[dict],
) -> tuple[float, float, list[dict]]:
    if not ingredient_order:
        if not matrix_markers:
            return 0.0, 0.0, []
        n = max((m.get("position") or 1) for m in matrix_markers)
    else:
        n = len(ingredient_order)

    total_pos_weight = sum(_pos_weight(i + 1) for i in range(min(n, 15)))
    grouped = _group_markers_by_position(matrix_markers)
    degradation_mass = 0.0
    active_signals = []
    pos1_degradation = 0.0

    for pos, markers_at_pos in grouped.items():
        score, cat = _best_degradation_at_position(markers_at_pos)
        if score == 0:
            continue
        w = _pos_weight(pos)
        contribution = score * w
        degradation_mass += contribution
        active_signals.append({
            "position": pos,
            "category": cat,
            "degradation_score": round(score, 1),
            "position_weight": round(w, 3),
            "contribution": round(contribution, 2),
        })
        if pos == 1:
            pos1_degradation = score

    raw_degradation = (degradation_mass / total_pos_weight) if total_pos_weight > 0 else 0.0
    return round(raw_degradation, 2), round(pos1_degradation, 1), active_signals


def _compute_structural_void_penalty(
    sweeteners: list[dict],
    matrix_markers: list[dict],
    ingredient_order: list[dict],
) -> tuple[float, list[str]]:
    notes = []
    penalty = 0.0
    matrix_positions = {m.get("position") for m in matrix_markers}

    for check_pos in [1, 2]:
        if check_pos > len(ingredient_order):
            break
        if check_pos in matrix_positions:
            continue
        pos_sweeteners = [
            s for s in sweeteners
            if s.get("position") == check_pos and s.get("category") in _STRUCTURAL_VOID_SWEETENERS
        ]
        if pos_sweeteners:
            add = 22.0 if check_pos == 1 else 12.0
            penalty += add
            notes.append(f"pos{check_pos}_primary_sweetener:{pos_sweeteners[0]['category']}")

    return round(penalty, 1), notes


def _compute_fermentation_credit(fermentation_markers: list[dict]) -> tuple[float, list[str]]:
    if not fermentation_markers:
        return 0.0, []
    unique_cats: dict[str, float] = {}
    for m in fermentation_markers:
        cat = m["category"]
        credit = FERMENTATION_CREDITS.get(cat, 0)
        if cat not in unique_cats or credit > unique_cats[cat]:
            unique_cats[cat] = credit
    total_credit = sum(unique_cats.values())
    capped_credit = min(42.0, total_credit)
    factor = round(capped_credit / 105.0, 4)
    factor = min(0.40, factor)
    detected_cats = [cat for cat, _ in sorted(unique_cats.items(), key=lambda x: -x[1])]
    return factor, detected_cats


def _compute_protein_engineering(protein_markers: list[dict]) -> tuple[float, list[str]]:
    if not protein_markers:
        return 0.0, []
    high_eng = []
    low_eng = []
    for m in protein_markers:
        score = PROTEIN_ENGINEERING_SCORES.get(m["category"], 0)
        if score >= _HIGH_ENGINEERING_THRESHOLD:
            high_eng.append((m["category"], score))
        else:
            low_eng.append((m["category"], score))
    if not high_eng:
        component = min(20.0, len(low_eng) * 7.0)
        return round(component, 1), [cat for cat, _ in low_eng]
    max_score = max(s for _, s in high_eng)
    extra_count = max(0, len(high_eng) - 1)
    component = max_score * 0.75 + min(22.0, extra_count * 14.0)
    component = min(100.0, component)
    signal_cats = [cat for cat, _ in sorted(high_eng, key=lambda x: -x[1])]
    return round(component, 1), signal_cats


def _compute_additive_engineering(additives: list[dict]) -> tuple[float, list[str]]:
    total = 0.0
    seen_cats: set[str] = set()
    signals = []
    for a in additives:
        cat = a["category"]
        if cat in ADDITIVE_ENGINEERING_SIGNALS and cat not in seen_cats:
            total += ADDITIVE_ENGINEERING_SIGNALS[cat]
            signals.append(cat)
            seen_cats.add(cat)
    return round(min(60.0, total), 1), signals


def _compute_sweetener_stacking(sweeteners: list[dict]) -> tuple[float, list[str]]:
    if not sweeteners:
        return 0.0, []
    added_sugar_cats = {
        "added_sugar", "brown_sugar", "invert_sugar", "invert_sugar_syrup",
        "glucose_syrup", "corn_syrup", "sugar_syrup", "rice_syrup",
        "malt_syrup", "molasses", "honey", "fructose", "glucose",
        "maltose", "sucrose", "date_syrup", "maple_syrup", "agave_syrup",
    }
    intense_cats = {"aspartame", "sucralose", "stevia", "acesulfame_k", "saccharin", "sweetener_generic"}
    polyol_cats = {"sorbitol", "maltitol", "xylitol", "erythritol", "mannitol", "lactitol", "polyols_generic"}

    distinct_types = set(s["category"] for s in sweeteners)
    n_distinct = len(distinct_types)
    has_intense = bool(distinct_types & intense_cats)
    has_polyol = bool(distinct_types & polyol_cats)
    has_syrup = any("syrup" in s["category"] for s in sweeteners)
    added_sugar_count = sum(1 for s in sweeteners if s["category"] in added_sugar_cats)

    score = 0.0
    signals = []
    if n_distinct >= 4:
        score, signals = 40.0, ["heavy_sweetener_layering"]
    elif n_distinct == 3:
        score, signals = 32.0, ["triple_sweetener_system"]
    elif n_distinct == 2 and (has_intense or has_polyol):
        score, signals = 28.0, ["sugar_plus_intense_or_polyol"]
    elif n_distinct == 2:
        score, signals = 18.0, ["dual_sweetener_system"]
    elif has_syrup and added_sugar_count >= 1:
        score, signals = 14.0, ["syrup_plus_sugar"]
    return round(score, 1), signals


# ---------------------------------------------------------------------------
# NEW v2: Supplemental mechanical transformation scan
# ---------------------------------------------------------------------------

def _compute_supplemental_mechanical(
    ingredient_order: list[dict],
    existing_matrix_positions: set,
) -> tuple[list[dict], list[str]]:
    """
    Scan ingredient texts for soft mechanical transformation signals not in MATRIX_TERMS.
    Suppressed at positions where a matrix_marker was already detected.
    Returns (virtual_signals, provenance_notes).
    """
    found: list[dict] = []
    notes: list[str] = []
    seen_positions: set = set()

    for item in ingredient_order:
        pos = item.get("position")
        if pos in existing_matrix_positions:
            continue
        if pos in seen_positions:
            continue
        text = item.get("text", "").lower()
        for pattern_text, score, label in _MECHANICAL_TRANSFORM_PATTERNS:
            if pattern_text.lower() in text:
                found.append({
                    "position": pos,
                    "category": label,
                    "degradation_score": score,
                    "source": "supplemental_scan",
                })
                notes.append(f"{label} at position {pos} (text match: '{pattern_text}')")
                seen_positions.add(pos)
                break

    return found, notes


# ---------------------------------------------------------------------------
# NEW v2: Assembly complexity drag
# ---------------------------------------------------------------------------

def _compute_assembly_drag(
    n_ingredients: int,
    n_matrix_types: int,
    n_additive_types: int,
    n_sweetener_types: int,
) -> float:
    """
    Mild flat penalty (0-12) for assembled products.
    Captures cumulative reconstruction effort even when no single signal is severe.
    Products with 1-2 ingredients are exempt — this is a whole-food guarantee.
    """
    if n_ingredients <= 2:
        return 0.0
    if n_ingredients <= 4:
        base = 1.0
    elif n_ingredients <= 6:
        base = 2.5
    elif n_ingredients <= 9:
        base = 4.5
    elif n_ingredients <= 12:
        base = 6.5
    elif n_ingredients <= 15:
        base = 8.5
    else:
        base = min(11.0, 8.5 + (n_ingredients - 15) * 0.20)

    diversity = min(2.5, (n_matrix_types + n_additive_types + n_sweetener_types) * 0.4)
    return round(min(12.0, base + diversity), 1)


# ---------------------------------------------------------------------------
# MODIFIED v2: Fortification engineering — restoration vs wellness
# ---------------------------------------------------------------------------

def _compute_fortification_engineering(
    fortification: list[dict],
    protein_markers: list[dict],
    additives: list[dict],
    sweeteners: list[dict],
) -> tuple[float, int, str]:
    """
    v2: Distinguishes basic_restoration from wellness_engineering.
    Regulatory vitamin/mineral enrichment of staple cereals is treated differently
    from an engineered supplement profile stacked on isolates and fiber.
    Returns (score, count, fortification_type).
    """
    n = len(fortification)
    if n == 0:
        return 0.0, 0, "none"

    has_isolate = any(
        PROTEIN_ENGINEERING_SCORES.get(m["category"], 0) >= 75
        for m in protein_markers
    )
    has_fiber_addition = any(a["category"] == "prebiotic_fiber" for a in additives)
    distinct_sweetener_types = len(set(s["category"] for s in sweeteners))
    has_sweet_stack = distinct_sweetener_types >= 2

    wellness_flags = sum([has_isolate, has_fiber_addition, has_sweet_stack])

    if wellness_flags >= 2:
        base = min(28.0, 8.0 + n * 4.5)
        fortif_type = "wellness_engineering"
    elif wellness_flags == 1 and n >= 4:
        base = min(20.0, 5.0 + n * 3.0)
        fortif_type = "partial_compensation"
    else:
        base = min(10.0, 2.0 + n * 1.5)
        fortif_type = "basic_restoration"

    return round(base, 1), n, fortif_type


# ---------------------------------------------------------------------------
# MODIFIED v2: HP reconstruction — position weighting + false-positive guard
# ---------------------------------------------------------------------------

def _compute_hp_reconstruction(
    sweeteners: list[dict],
    flavors: list[dict],
    additives: list[dict],
    ingredient_order: list[dict],
    raw_matrix_degradation: float,
) -> tuple[float, list[str]]:
    """
    v2 additions vs v1:
    - Position weighting: sweetener/flavor in first 3 positions amplify score.
    - Additive density amplification: ≥4 distinct functional additive types.
    - Matrix weakness amplification: degraded matrix + HP = stronger industrial signal.
    - False-positive suppression: single-flavor signal on clean matrix halved.
    """
    distinct_sweet_types = len(set(s["category"] for s in sweeteners))
    has_emulsifier = any(a["category"] == "emulsifier" for a in additives)
    has_humectant  = any(a["category"] == "humectant" for a in additives)
    has_flavor     = bool(flavors)
    has_flavor_enhancer = any(a["category"] == "flavor_enhancer" for a in additives)
    many_sweeteners = distinct_sweet_types >= 2

    distinct_additive_types = len(set(a["category"] for a in additives))
    dense_additives = distinct_additive_types >= 4

    score = 0.0
    signals: list[str] = []

    if many_sweeteners and has_flavor and has_emulsifier:
        score, signals = 85.0, ["sweetener_flavor_emulsifier_triad"]
    elif many_sweeteners and has_flavor and has_humectant:
        score, signals = 75.0, ["sweetener_flavor_humectant_triad"]
    elif many_sweeteners and has_flavor:
        score, signals = 58.0, ["sweetener_flavor_combo"]
    elif many_sweeteners and has_emulsifier:
        score, signals = 45.0, ["sweetener_emulsifier_combo"]
    elif has_flavor_enhancer and has_emulsifier:
        score, signals = 42.0, ["flavor_enhancer_emulsifier"]
    elif has_flavor and has_emulsifier:
        score, signals = 32.0, ["flavor_emulsifier_combo"]
    elif many_sweeteners:
        score, signals = 22.0, ["dual_sweetener_system"]
    elif has_flavor:
        score, signals = 12.0, ["flavor_only"]

    if score == 0.0:
        return 0.0, []

    # False-positive suppression FIRST: single-flavor on clean-matrix product
    # Captures mildly flavored yogurt, vanilla milk, simple flavored dairy.
    if signals == ["flavor_only"] and raw_matrix_degradation < 15.0:
        return round(score * 0.50, 1), ["flavor_only", "natural_flavor_suppressed"]

    # Position weighting: early signals are stronger HP evidence
    early_sweetener = any(
        s.get("position") is not None and s["position"] <= 3 for s in sweeteners
    )
    early_flavor = any(
        f.get("position") is not None and f["position"] <= 3 for f in flavors
    )
    if early_sweetener and early_flavor:
        score = min(100.0, score * 1.20)
        signals.append("early_position_amplified")
    elif early_sweetener or early_flavor:
        score = min(100.0, score * 1.10)

    # Additive density amplification
    if dense_additives and score > 30.0:
        score = min(100.0, score * 1.15)
        signals.append("dense_additive_system")

    # Matrix weakness amplification: degraded base + HP pattern = clear industrial design
    if raw_matrix_degradation >= 50.0 and score >= 40.0:
        score = min(100.0, score * 1.12)
        signals.append("matrix_weakness_amplified")

    return round(score, 1), signals


# ---------------------------------------------------------------------------
# NEW v2: Transformation type classification
# ---------------------------------------------------------------------------

def _classify_transformation_type(
    active_deg_signals: list[dict],
    supp_signals: list[dict],
    ferm_markers: list[dict],
    protein_markers: list[dict],
    fortification: list[dict],
) -> str:
    """
    Assigns dominant transformation type A/B/C/D based on detected signals.
    Priority: industrial (C) > reconstruction (D) > mechanical (B) > traditional (A) > minimal.
    """
    deg_cats = {s["category"] for s in active_deg_signals}

    if deg_cats & _INDUSTRIAL_MATRIX_CATEGORIES:
        return "industrial_restructuring"

    has_high_eng_protein = any(
        PROTEIN_ENGINEERING_SCORES.get(m["category"], 0) >= 75
        for m in protein_markers
    )
    if has_high_eng_protein or (len(fortification) >= 4 and (deg_cats & _MECHANICAL_MATRIX_CATEGORIES)):
        return "reconstruction_compensation"

    if deg_cats & _MECHANICAL_MATRIX_CATEGORIES:
        return "mechanical_degradation"

    has_strong_ferm = any(m["category"] in _STRONG_FERMENTATION for m in ferm_markers)
    if has_strong_ferm or supp_signals:
        return "traditional_transformation"

    return "minimal_transformation"


# ---------------------------------------------------------------------------
# NEW v2: Provenance trace builder
# ---------------------------------------------------------------------------

def _build_provenance(
    active_deg_signals: list[dict],
    supp_signals: list[dict],
    supp_notes: list[str],
    protein_signals: list[str],
    additive_signals: list[str],
    sweet_signals: list[str],
    fortif_detected: list[dict],
    fortif_type: str,
    ferm_cats: list[str],
    roasting_markers: list[dict],
    void_notes: list[str],
    assembly_drag: float,
    n_ingredients: int,
    transformation_type: str,
) -> dict:
    deg_human: list[str] = []
    for s in sorted(active_deg_signals, key=lambda x: -x.get("contribution", 0)):
        pos_str = f"position {s['position']}" if s.get("position") else "unknown position"
        source_tag = " [supplemental]" if s.get("source") == "supplemental_scan" else ""
        deg_human.append(
            f"{s['category']} at {pos_str} (deg={s['degradation_score']:.0f}){source_tag}"
        )
    for note in supp_notes:
        if not any(note.split(" at ")[0] in d for d in deg_human):
            deg_human.append(note + " [soft signal]")
    for v in void_notes:
        deg_human.append(f"structural void: {v}")

    eng_human: list[str] = []
    for cat in protein_signals:
        eng_human.append(f"protein engineering: {cat}")
    for cat in additive_signals:
        eng_human.append(f"additive: {cat}")
    for cat in sweet_signals:
        eng_human.append(f"sweetener system: {cat}")

    comp_human: list[str] = []
    if fortif_detected:
        comp_human.append(
            f"vitamin/mineral fortification ×{len(fortif_detected)} ({fortif_type})"
        )

    prot_human: list[str] = []
    for cat in ferm_cats:
        prot_human.append(f"fermentation: {cat}")
    for m in roasting_markers:
        prot_human.append(f"traditional roasting: {m.get('category', 'roasting')}")

    return {
        "degradation_signals":   deg_human[:8],
        "engineering_signals":   eng_human[:8],
        "compensation_signals":  comp_human[:5],
        "protective_signals":    prot_human[:5],
        "transformation_type":   transformation_type,
        "transformation_description": {
            "minimal_transformation":      "whole-food or single-ingredient — no observable structural transformation",
            "traditional_transformation":  "traditional (A) — fermentation, gentle rolling, roasting",
            "mechanical_degradation":      "mechanical (B) — milling, starch isolation, powderization",
            "industrial_restructuring":    "industrial (C) — extrusion, puffing, crisping, expanded grains",
            "reconstruction_compensation": "reconstruction (D) — isolates + fortification + functional additions",
        }.get(transformation_type, transformation_type),
        "assembly_drag_note": f"{n_ingredients} ingredients → complexity drag {assembly_drag:.1f} pts",
    }


# ---------------------------------------------------------------------------
# Reconstruction depth + degradation labels (unchanged from v1)
# ---------------------------------------------------------------------------

def _determine_reconstruction_depth(
    matrix_integrity_score: float,
    fermentation_markers: list[dict],
    protein_markers: list[dict],
    hp_score: float,
    engineering_intensity: float,
) -> int:
    has_strong_ferm = any(m["category"] in _STRONG_FERMENTATION for m in fermentation_markers)
    has_high_eng_protein = any(
        PROTEIN_ENGINEERING_SCORES.get(m["category"], 0) >= _HIGH_ENGINEERING_THRESHOLD
        for m in protein_markers
    )
    if matrix_integrity_score >= 90:   depth = 0
    elif matrix_integrity_score >= 76: depth = 1
    elif matrix_integrity_score >= 58: depth = 2
    elif matrix_integrity_score >= 40: depth = 3
    elif matrix_integrity_score >= 22: depth = 4
    else:                              depth = 5

    if has_strong_ferm and not has_high_eng_protein and depth >= 2:
        if engineering_intensity < 40:
            depth = min(depth, 1)

    if has_high_eng_protein and engineering_intensity >= 50 and depth < 4:
        depth = 4

    return depth


_DEGRADATION_LEVEL_LABELS = {
    0: "minimal", 1: "low", 2: "moderate", 3: "high", 4: "severe", 5: "extreme",
}

_DEPTH_DESCRIPTIONS = {
    0: "whole-food or single-ingredient — no observable structural transformation",
    1: "lightly transformed — traditional processing (rolling, roasting, fermentation)",
    2: "mechanically degraded — grain ground or flaked; matrix disrupted but familiar",
    3: "industrially restructured — puffed, extruded, or formed into new physical shape",
    4: "engineered composite — isolates + restructured matrix + functional additions",
    5: "hyper-reconstructed — multiple stacked engineering systems; origin unrecognizable",
}


def _build_integrity_summary(
    score: float,
    depth: int,
    fermentation_markers: list[dict],
    dominant_signals: list[str],
    compensation_signals: list[str],
    hp_signals: list[str],
    assembly_drag: float,
    transformation_type: str,
) -> str:
    level = _DEGRADATION_LEVEL_LABELS[depth]
    desc = _DEPTH_DESCRIPTIONS[depth]
    ferm_note = ""
    if fermentation_markers:
        strong = any(m["category"] in _STRONG_FERMENTATION for m in fermentation_markers)
        ferm_note = " Fermentation credit applied." if strong else ""
    comp_note = f" Compensation: {', '.join(compensation_signals[:2])}." if compensation_signals else ""
    hp_note = f" HP pattern: {hp_signals[0]}." if hp_signals else ""
    dom_note = f" Primary signal: {dominant_signals[0]}." if dominant_signals else ""
    drag_note = f" Assembly drag: {assembly_drag:.1f} pts ({transformation_type})."
    return (
        f"Matrix integrity {score:.0f}/100 — {level} degradation. "
        f"{desc}.{dom_note}{ferm_note}{comp_note}{hp_note}{drag_note}"
    )


# ---------------------------------------------------------------------------
# Main engine function
# ---------------------------------------------------------------------------

def compute_matrix_integrity(product: dict) -> dict:
    """
    Compute the full Matrix Integrity Engine v2 output for a BSIP1 enriched product.
    Interface is identical to v1. Trace block gains new keys.
    """
    ingredient_order  = product.get("ingredient_order") or []
    matrix_markers    = product.get("extracted_matrix_markers") or []
    additives         = product.get("extracted_additives") or []
    protein_markers   = product.get("extracted_protein_markers") or []
    sweeteners        = product.get("extracted_sweeteners") or []
    flavors           = product.get("extracted_flavors") or []
    ferm_markers      = product.get("extracted_fermentation_markers") or []
    roasting_markers  = product.get("extracted_roasting_markers") or []
    summary           = product.get("enrichment_summary") or {}

    n_ingredients = len(ingredient_order)
    has_ingredient_data = n_ingredients > 0 or bool(
        product.get("ingredients_raw") or product.get("ingredients_text_he")
    )

    # ── 1: Supplemental mechanical transform scan ─────────────────────────────
    existing_matrix_positions = {m.get("position") for m in matrix_markers}
    supp_signals, supp_notes = _compute_supplemental_mechanical(
        ingredient_order, existing_matrix_positions
    )
    all_matrix_for_deg = matrix_markers + supp_signals

    # ── 2: Structural form degradation (on merged markers) ────────────────────
    raw_form_deg, pos1_deg, active_deg_signals = _compute_matrix_degradation(
        all_matrix_for_deg, ingredient_order
    )

    # ── 3: Structural void penalty ────────────────────────────────────────────
    void_penalty, void_notes = _compute_structural_void_penalty(
        sweeteners, all_matrix_for_deg, ingredient_order
    )

    # ── 4: Position-1 anchoring blend ────────────────────────────────────────
    if pos1_deg > 0:
        raw_degradation = pos1_deg * 0.60 + raw_form_deg * 0.40
    else:
        raw_degradation = raw_form_deg
    raw_degradation = min(100.0, raw_degradation + void_penalty)

    # ── 5: Fermentation credit ────────────────────────────────────────────────
    ferm_factor, ferm_cats = _compute_fermentation_credit(ferm_markers)
    adjusted_degradation = raw_degradation * (1.0 - ferm_factor)

    # ── 6: Engineering components ─────────────────────────────────────────────
    protein_eng, protein_signals     = _compute_protein_engineering(protein_markers)
    additive_eng, additive_signals   = _compute_additive_engineering(additives)
    fortification                    = _detect_fortification(ingredient_order)
    fortif_eng, fortif_count, fortif_type = _compute_fortification_engineering(
        fortification, protein_markers, additives, sweeteners
    )
    sweet_stacking, sweet_signals    = _compute_sweetener_stacking(sweeteners)

    engineering_total = (
        protein_eng    * 0.42
        + additive_eng * 0.28
        + sweet_stacking * 0.18
        + fortif_eng   * 0.12
    )
    engineering_intensity = round(min(100.0, engineering_total), 1)

    # ── 7: Assembly complexity drag ───────────────────────────────────────────
    n_matrix_types   = len({m["category"] for m in all_matrix_for_deg})
    n_additive_types = len({a["category"] for a in additives
                            if a["category"] in ADDITIVE_ENGINEERING_SIGNALS})
    n_sweetener_types = len({s["category"] for s in sweeteners})
    assembly_drag = _compute_assembly_drag(
        n_ingredients, n_matrix_types, n_additive_types, n_sweetener_types
    )

    # ── 8: HP reconstruction (v2: passes raw_degradation + ingredient_order) ─
    hp_score, hp_signals = _compute_hp_reconstruction(
        sweeteners, flavors, additives, ingredient_order, raw_degradation
    )

    # ── 9: Final score ────────────────────────────────────────────────────────
    degradation_pull  = adjusted_degradation * 0.55
    engineering_pull  = engineering_intensity * 0.30
    hp_pull           = hp_score * 0.15

    raw_score = 100.0 - degradation_pull - engineering_pull - hp_pull - assembly_drag
    matrix_integrity_score = round(max(0.0, min(100.0, raw_score)), 1)

    # ── 10: Reconstruction depth ──────────────────────────────────────────────
    reconstruction_depth = _determine_reconstruction_depth(
        matrix_integrity_score, ferm_markers, protein_markers,
        hp_score, engineering_intensity,
    )
    structural_degradation_level = _DEGRADATION_LEVEL_LABELS[reconstruction_depth]

    # ── 11: Transformation type classification ────────────────────────────────
    transformation_type = _classify_transformation_type(
        active_deg_signals, supp_signals, ferm_markers, protein_markers, fortification
    )

    # ── 12: Provenance trace ──────────────────────────────────────────────────
    provenance = _build_provenance(
        active_deg_signals, supp_signals, supp_notes,
        protein_signals, additive_signals, sweet_signals,
        fortification, fortif_type,
        ferm_cats, roasting_markers,
        void_notes, assembly_drag, n_ingredients,
        transformation_type,
    )

    # ── 13: Compensation signals ──────────────────────────────────────────────
    compensation_signals: list[str] = []
    if summary.get("has_prebiotic_fiber"):
        compensation_signals.append("prebiotic_fiber_addition")
    if summary.get("has_protein_isolate_or_concentrate"):
        compensation_signals.append("protein_isolate_or_concentrate")
    if fortif_count > 0:
        compensation_signals.append(f"vitamin_mineral_fortification_x{fortif_count}_{fortif_type}")
    for cat in additive_signals:
        if cat in {"prebiotic_fiber", "bulking_agent", "modified_starch"}:
            compensation_signals.append(f"additive_{cat}")

    # ── 14: Dominant signals ──────────────────────────────────────────────────
    dominant_matrix_signals: list[str] = []
    for sig in sorted(active_deg_signals, key=lambda x: -x["contribution"]):
        src_tag = " [soft]" if sig.get("source") == "supplemental_scan" else ""
        dominant_matrix_signals.append(
            f"{sig['category']} (pos {sig['position']}, deg={sig['degradation_score']:.0f}){src_tag}"
        )
    if void_notes:
        dominant_matrix_signals = void_notes + dominant_matrix_signals
    dominant_matrix_signals = dominant_matrix_signals[:5]

    # ── 15: Integrity summary ─────────────────────────────────────────────────
    integrity_summary = _build_integrity_summary(
        matrix_integrity_score, reconstruction_depth,
        ferm_markers, dominant_matrix_signals, compensation_signals, hp_signals,
        assembly_drag, transformation_type,
    )

    # ── Trace ──────────────────────────────────────────────────────────────────
    trace = {
        "module_version":              MODULE_VERSION,
        "ingredient_count":            n_ingredients,
        "has_ingredient_data":         has_ingredient_data,
        # Degradation
        "raw_form_degradation":        round(raw_form_deg, 2),
        "pos1_degradation_score":      pos1_deg,
        "supplemental_signals":        supp_signals,
        "supplemental_provenance":     supp_notes,
        "structural_void_penalty":     void_penalty,
        "structural_void_notes":       void_notes,
        "raw_degradation_blended":     round(raw_degradation, 2),
        "fermentation_factor":         round(ferm_factor, 4),
        "fermentation_categories":     ferm_cats,
        "adjusted_degradation":        round(adjusted_degradation, 2),
        "degradation_pull":            round(degradation_pull, 2),
        "active_degradation_signals":  active_deg_signals,
        # Engineering
        "protein_engineering":         protein_eng,
        "protein_signals":             protein_signals,
        "additive_engineering":        additive_eng,
        "additive_signals":            additive_signals,
        "fortification_detected":      fortification,
        "fortification_engineering":   fortif_eng,
        "fortification_type":          fortif_type,
        "sweet_stacking_score":        sweet_stacking,
        "sweetener_stacking_signals":  sweet_signals,
        "engineering_intensity":       engineering_intensity,
        "engineering_pull":            round(engineering_pull, 2),
        # Assembly drag
        "assembly_drag":               assembly_drag,
        # HP
        "hp_reconstruction_score":     hp_score,
        "hp_signals":                  hp_signals,
        "hp_pull":                     round(hp_pull, 2),
        # Transformation type
        "transformation_type":         transformation_type,
        # Score assembly
        "score_assembly": {
            "100 - degradation_pull":      round(degradation_pull, 2),
            "  - engineering_pull":        round(engineering_pull, 2),
            "  - hp_pull":                 round(hp_pull, 2),
            "  - assembly_drag":           assembly_drag,
            "= matrix_integrity_score":    matrix_integrity_score,
        },
        # Provenance
        "provenance":                  provenance,
        # Misc
        "roasting_markers_detected":   [m.get("category") for m in roasting_markers],
    }

    return {
        "matrix_integrity_score":       matrix_integrity_score,
        "reconstruction_depth":         reconstruction_depth,
        "structural_degradation_level": structural_degradation_level,
        "engineering_intensity":        engineering_intensity,
        "compensation_signals":         compensation_signals,
        "dominant_matrix_signals":      dominant_matrix_signals,
        "integrity_summary":            integrity_summary,
        "matrix_integrity_trace":       trace,
    }
