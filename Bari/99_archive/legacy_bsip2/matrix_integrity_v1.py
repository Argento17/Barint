"""
BSIP2 Matrix Integrity Engine v1 — ARCHIVE COPY
Kept for calibration comparison against v2. Do not modify.
Original implementation date: 2026-05-20.
"""

from __future__ import annotations
from typing import Optional

MODULE_VERSION = "matrix_integrity_v1_archive"

def _pos_weight(pos: Optional[int]) -> float:
    if pos is None: return 0.12
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

MATRIX_DEGRADATION_SCORES: dict[str, float] = {
    "oat_flakes": 20, "wheat_flakes": 28, "corn_flakes": 48, "flakes_generic": 30,
    "whole_wheat_flour": 52, "whole_rye_flour": 48, "spelt_flour": 55, "wheat_flour": 70,
    "rye_flour": 62, "oat_flour": 65, "rice_flour": 65, "corn_flour": 65, "flour_generic": 68,
    "potato_starch": 82, "corn_starch": 82, "wheat_starch": 82, "rice_starch": 80,
    "modified_starch": 90, "starch_generic": 78,
    "puffed_cereal": 80, "puffed_rice": 78, "puffed_barley": 76, "puffed_corn": 82,
    "puffed": 80, "expanded": 85, "crisped_cereal": 80, "rice_cakes": 62, "crunchy_pieces": 75,
    "maltodextrin": 92, "dextrin": 85, "dextrose": 88,
}

_GENERIC_MATRIX_CATEGORIES = frozenset({"flour_generic", "starch_generic", "puffed_cereal", "flakes_generic"})
_STRUCTURAL_VOID_SWEETENERS = frozenset({
    "glucose_syrup", "corn_syrup", "invert_sugar_syrup", "invert_sugar",
    "added_sugar", "brown_sugar", "maple_syrup", "date_syrup", "agave_syrup",
    "sugar_syrup", "rice_syrup", "malt_syrup", "molasses",
})

FERMENTATION_CREDITS: dict[str, float] = {
    "live_cultures": 38, "live_bacteria": 38, "lb_bulgaricus": 30, "lb_acidophilus": 30,
    "lactobacillus": 28, "bifidobacterium": 30, "st_thermophilus": 26, "streptococcus": 22,
    "lactococcus": 22, "lactic_fermentation": 28, "starter_cultures": 25, "sourdough_starter": 25,
    "fermented": 18, "fermentation": 14, "cultures_generic": 18, "yeast": 10, "bread_yeast": 10,
}
_STRONG_FERMENTATION = frozenset({
    "live_cultures", "live_bacteria", "lb_bulgaricus", "lb_acidophilus",
    "bifidobacterium", "st_thermophilus", "sourdough_starter", "lactic_fermentation",
})

PROTEIN_ENGINEERING_SCORES: dict[str, float] = {
    "hydrolyzed_protein": 88, "whey_protein_isolate": 85, "soy_protein_isolate": 88,
    "vital_wheat_gluten": 62, "wheat_gluten": 58, "whey_protein_concentrate": 65,
    "soy_protein_concentrate": 68, "pea_protein_concentrate": 65, "milk_protein_concentrate": 58,
    "rice_protein": 62, "potato_protein": 58, "pea_protein": 55, "casein": 45,
    "soy_protein": 55, "wheat_protein": 52, "whey_protein": 50, "soy_powder": 45,
    "skim_milk_powder": 42, "milk_powder": 38, "milk_protein": 32, "milk_solids": 25,
    "whey": 28, "lactalbumin": 30, "egg_albumen": 28, "albumin": 32, "egg_white": 18,
}
_HIGH_ENGINEERING_THRESHOLD = 55

ADDITIVE_ENGINEERING_SIGNALS: dict[str, float] = {
    "prebiotic_fiber": 22, "modified_starch": 16, "bulking_agent": 20, "humectant": 12,
    "flavor_enhancer": 15, "glazing_agent": 8, "emulsifier": 10, "stabilizer_thickener": 8,
}

_FORTIFICATION_TERMS_HE: list[str] = [
    "ניאצין", "ריבופלאבין", "תיאמין", "חומצה פולית", "ציאנוקובלמין",
    "פנטותנאט", "פירידוקסין", "ויטמין", "קולקלציפרול", "טוקופרול",
    "חומצה אסקורבית", "ברזל", "אבץ", "סידן", "ניאציינאמיד", "פריפוספט",
]

def _group_markers_by_position(markers):
    grouped = {}
    for m in markers:
        pos = m.get("position")
        grouped.setdefault(pos, []).append(m)
    return grouped

def _best_degradation_at_position(markers):
    categories = {m["category"] for m in markers}
    non_generic = categories - _GENERIC_MATRIX_CATEGORIES
    active_cats = non_generic if non_generic else categories
    best_score, best_cat = 0.0, ""
    for m in markers:
        if m["category"] not in active_cats:
            continue
        score = MATRIX_DEGRADATION_SCORES.get(m["category"], 0)
        if score > best_score:
            best_score, best_cat = score, m["category"]
    return best_score, best_cat

def _detect_fortification(ingredient_order):
    found, seen = [], set()
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

def _compute_matrix_degradation(matrix_markers, ingredient_order):
    if not ingredient_order:
        if not matrix_markers:
            return 0.0, 0.0, []
        n = max((m.get("position") or 1) for m in matrix_markers)
    else:
        n = len(ingredient_order)
    total_pos_weight = sum(_pos_weight(i + 1) for i in range(min(n, 15)))
    grouped = _group_markers_by_position(matrix_markers)
    degradation_mass, active_signals, pos1_degradation = 0.0, [], 0.0
    for pos, markers_at_pos in grouped.items():
        score, cat = _best_degradation_at_position(markers_at_pos)
        if score == 0:
            continue
        w = _pos_weight(pos)
        contribution = score * w
        degradation_mass += contribution
        active_signals.append({
            "position": pos, "category": cat,
            "degradation_score": round(score, 1),
            "position_weight": round(w, 3),
            "contribution": round(contribution, 2),
        })
        if pos == 1:
            pos1_degradation = score
    raw_degradation = (degradation_mass / total_pos_weight) if total_pos_weight > 0 else 0.0
    return round(raw_degradation, 2), round(pos1_degradation, 1), active_signals

def _compute_structural_void_penalty(sweeteners, matrix_markers, ingredient_order):
    notes, penalty = [], 0.0
    matrix_positions = {m.get("position") for m in matrix_markers}
    for check_pos in [1, 2]:
        if check_pos > len(ingredient_order):
            break
        if check_pos in matrix_positions:
            continue
        pos_sweeteners = [s for s in sweeteners
                          if s.get("position") == check_pos and s.get("category") in _STRUCTURAL_VOID_SWEETENERS]
        if pos_sweeteners:
            add = 22.0 if check_pos == 1 else 12.0
            penalty += add
            notes.append(f"pos{check_pos}_primary_sweetener:{pos_sweeteners[0]['category']}")
    return round(penalty, 1), notes

def _compute_fermentation_credit(fermentation_markers):
    if not fermentation_markers:
        return 0.0, []
    unique_cats = {}
    for m in fermentation_markers:
        cat, credit = m["category"], FERMENTATION_CREDITS.get(m["category"], 0)
        if cat not in unique_cats or credit > unique_cats[cat]:
            unique_cats[cat] = credit
    total_credit = sum(unique_cats.values())
    capped_credit = min(42.0, total_credit)
    factor = round(min(0.40, capped_credit / 105.0), 4)
    return factor, [c for c, _ in sorted(unique_cats.items(), key=lambda x: -x[1])]

def _compute_protein_engineering(protein_markers):
    if not protein_markers:
        return 0.0, []
    high_eng, low_eng = [], []
    for m in protein_markers:
        score = PROTEIN_ENGINEERING_SCORES.get(m["category"], 0)
        (high_eng if score >= _HIGH_ENGINEERING_THRESHOLD else low_eng).append((m["category"], score))
    if not high_eng:
        return round(min(20.0, len(low_eng) * 7.0), 1), [c for c, _ in low_eng]
    max_score = max(s for _, s in high_eng)
    component = min(100.0, max_score * 0.75 + min(22.0, max(0, len(high_eng) - 1) * 14.0))
    return round(component, 1), [c for c, _ in sorted(high_eng, key=lambda x: -x[1])]

def _compute_additive_engineering(additives):
    total, seen_cats, signals = 0.0, set(), []
    for a in additives:
        cat = a["category"]
        if cat in ADDITIVE_ENGINEERING_SIGNALS and cat not in seen_cats:
            total += ADDITIVE_ENGINEERING_SIGNALS[cat]
            signals.append(cat)
            seen_cats.add(cat)
    return round(min(60.0, total), 1), signals

def _compute_fortification_engineering(fortification):
    n = len(fortification)
    if n == 0:   return 0.0, 0
    if n >= 4:   return 28.0, n
    if n >= 2:   return 16.0, n
    return 8.0, n

def _compute_sweetener_stacking(sweeteners):
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
    if n_distinct >= 4:   return 40.0, ["heavy_sweetener_layering"]
    elif n_distinct == 3: return 32.0, ["triple_sweetener_system"]
    elif n_distinct == 2 and (has_intense or has_polyol): return 28.0, ["sugar_plus_intense_or_polyol"]
    elif n_distinct == 2: return 18.0, ["dual_sweetener_system"]
    elif has_syrup and added_sugar_count >= 1: return 14.0, ["syrup_plus_sugar"]
    return 0.0, []

def _compute_hp_reconstruction(sweeteners, flavors, additives):
    distinct_sweet_types = len(set(s["category"] for s in sweeteners))
    has_emulsifier = any(a["category"] == "emulsifier" for a in additives)
    has_stabilizer = any(a["category"] in {"stabilizer", "stabilizer_thickener"} for a in additives)
    has_humectant = any(a["category"] == "humectant" for a in additives)
    has_flavor = bool(flavors)
    has_flavor_enhancer = any(a["category"] == "flavor_enhancer" for a in additives)
    many_sweeteners = distinct_sweet_types >= 2
    score, signals = 0.0, []
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
    return round(score, 1), signals

def _determine_reconstruction_depth(matrix_integrity_score, fermentation_markers, protein_markers, hp_score, engineering_intensity):
    has_strong_ferm = any(m["category"] in _STRONG_FERMENTATION for m in fermentation_markers)
    has_high_eng_protein = any(PROTEIN_ENGINEERING_SCORES.get(m["category"], 0) >= _HIGH_ENGINEERING_THRESHOLD for m in protein_markers)
    if matrix_integrity_score >= 90:   depth = 0
    elif matrix_integrity_score >= 76: depth = 1
    elif matrix_integrity_score >= 58: depth = 2
    elif matrix_integrity_score >= 40: depth = 3
    elif matrix_integrity_score >= 22: depth = 4
    else:                              depth = 5
    if has_strong_ferm and not has_high_eng_protein and depth >= 2 and engineering_intensity < 40:
        depth = min(depth, 1)
    if has_high_eng_protein and engineering_intensity >= 50 and depth < 4:
        depth = 4
    return depth

_DEGRADATION_LEVEL_LABELS = {0: "minimal", 1: "low", 2: "moderate", 3: "high", 4: "severe", 5: "extreme"}
_DEPTH_DESCRIPTIONS = {
    0: "whole-food or single-ingredient — no observable structural transformation",
    1: "lightly transformed — traditional processing (rolling, roasting, fermentation)",
    2: "mechanically degraded — grain ground or flaked; matrix disrupted but familiar",
    3: "industrially restructured — puffed, extruded, or formed into new physical shape",
    4: "engineered composite — isolates + restructured matrix + functional additions",
    5: "hyper-reconstructed — multiple stacked engineering systems; origin unrecognizable",
}

def _build_integrity_summary(score, depth, fermentation_markers, dominant_signals, compensation_signals, hp_signals):
    level = _DEGRADATION_LEVEL_LABELS[depth]
    desc = _DEPTH_DESCRIPTIONS[depth]
    ferm_note = ""
    if fermentation_markers:
        strong = any(m["category"] in _STRONG_FERMENTATION for m in fermentation_markers)
        ferm_note = " Fermentation credit applied (traditional transformation)." if strong else ""
    comp_note = f" Compensation signals: {', '.join(compensation_signals[:3])}." if compensation_signals else ""
    hp_note = f" HP pattern: {hp_signals[0]}." if hp_signals else ""
    dom_note = f" Primary structural signal: {dominant_signals[0]}." if dominant_signals else ""
    return (f"Matrix integrity {score:.0f}/100 — {level} degradation. {desc}.{dom_note}{ferm_note}{comp_note}{hp_note}")


def compute_matrix_integrity(product: dict) -> dict:
    ingredient_order = product.get("ingredient_order") or []
    matrix_markers   = product.get("extracted_matrix_markers") or []
    additives        = product.get("extracted_additives") or []
    protein_markers  = product.get("extracted_protein_markers") or []
    sweeteners       = product.get("extracted_sweeteners") or []
    flavors          = product.get("extracted_flavors") or []
    ferm_markers     = product.get("extracted_fermentation_markers") or []
    roasting_markers = product.get("extracted_roasting_markers") or []
    summary          = product.get("enrichment_summary") or {}

    n_ingredients = len(ingredient_order)
    has_ingredient_data = n_ingredients > 0 or bool(product.get("ingredients_raw") or product.get("ingredients_text_he"))

    raw_form_deg, pos1_deg, active_deg_signals = _compute_matrix_degradation(matrix_markers, ingredient_order)
    void_penalty, void_notes = _compute_structural_void_penalty(sweeteners, matrix_markers, ingredient_order)

    if pos1_deg > 0:
        raw_degradation = pos1_deg * 0.60 + raw_form_deg * 0.40
    else:
        raw_degradation = raw_form_deg
    raw_degradation = min(100.0, raw_degradation + void_penalty)

    ferm_factor, ferm_cats = _compute_fermentation_credit(ferm_markers)
    adjusted_degradation = raw_degradation * (1.0 - ferm_factor)

    protein_eng, protein_signals = _compute_protein_engineering(protein_markers)
    additive_eng, additive_signals = _compute_additive_engineering(additives)
    fortification = _detect_fortification(ingredient_order)
    fortif_eng, fortif_count = _compute_fortification_engineering(fortification)
    sweet_stacking, sweet_signals = _compute_sweetener_stacking(sweeteners)

    engineering_total = (protein_eng * 0.42 + additive_eng * 0.28 + sweet_stacking * 0.18 + fortif_eng * 0.12)
    engineering_intensity = round(min(100.0, engineering_total), 1)

    hp_score, hp_signals = _compute_hp_reconstruction(sweeteners, flavors, additives)

    degradation_pull = adjusted_degradation * 0.55
    engineering_pull = engineering_intensity * 0.30
    hp_pull          = hp_score * 0.15
    raw_score = 100.0 - (degradation_pull + engineering_pull + hp_pull)
    matrix_integrity_score = round(max(0.0, min(100.0, raw_score)), 1)

    reconstruction_depth = _determine_reconstruction_depth(matrix_integrity_score, ferm_markers, protein_markers, hp_score, engineering_intensity)
    structural_degradation_level = _DEGRADATION_LEVEL_LABELS[reconstruction_depth]

    compensation_signals = []
    if summary.get("has_prebiotic_fiber"):
        compensation_signals.append("prebiotic_fiber_addition")
    if summary.get("has_protein_isolate_or_concentrate"):
        compensation_signals.append("protein_isolate_or_concentrate")
    if fortif_count > 0:
        compensation_signals.append(f"vitamin_mineral_fortification_x{fortif_count}")
    for cat in additive_signals:
        if cat in {"prebiotic_fiber", "bulking_agent", "modified_starch"}:
            compensation_signals.append(f"additive_{cat}")

    dominant_matrix_signals = []
    for sig in sorted(active_deg_signals, key=lambda x: -x["contribution"]):
        dominant_matrix_signals.append(f"{sig['category']} (pos {sig['position']}, deg={sig['degradation_score']:.0f})")
    if void_notes:
        dominant_matrix_signals = void_notes + dominant_matrix_signals
    dominant_matrix_signals = dominant_matrix_signals[:5]

    all_eng_signals = protein_signals + additive_signals + sweet_signals
    integrity_summary = _build_integrity_summary(matrix_integrity_score, reconstruction_depth, ferm_markers, dominant_matrix_signals, compensation_signals, hp_signals)

    trace = {
        "module_version": MODULE_VERSION, "ingredient_count": n_ingredients,
        "has_ingredient_data": has_ingredient_data,
        "raw_form_degradation": round(raw_form_deg, 2), "pos1_degradation_score": pos1_deg,
        "structural_void_penalty": void_penalty, "structural_void_notes": void_notes,
        "raw_degradation_blended": round(raw_degradation, 2),
        "fermentation_factor": round(ferm_factor, 4), "fermentation_categories": ferm_cats,
        "adjusted_degradation": round(adjusted_degradation, 2), "degradation_pull": round(degradation_pull, 2),
        "active_degradation_signals": active_deg_signals,
        "protein_engineering": protein_eng, "protein_signals": protein_signals,
        "additive_engineering": additive_eng, "additive_signals": additive_signals,
        "fortification_detected": fortification, "fortification_engineering": fortif_eng,
        "sweet_stacking_score": sweet_stacking, "sweetener_stacking_signals": sweet_signals,
        "engineering_intensity": engineering_intensity, "engineering_pull": round(engineering_pull, 2),
        "hp_reconstruction_score": hp_score, "hp_signals": hp_signals, "hp_pull": round(hp_pull, 2),
        "score_assembly": {
            "100 - degradation_pull": round(degradation_pull, 2),
            "  - engineering_pull":   round(engineering_pull, 2),
            "  - hp_pull":            round(hp_pull, 2),
            "= matrix_integrity_score": matrix_integrity_score,
        },
        "roasting_markers_detected": [m["category"] for m in roasting_markers],
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
