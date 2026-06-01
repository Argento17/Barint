"""
BSIP2 Sprint 1 — Signal Extractor v2

Approved modifications from TASK-042 Group A findings:
  EV-003  Emulsifier risk differentiation (three-tier model)
  EV-004  Allulose caloric/glycemic exemption
  EV-005  Polyol laxative potential (with humectant refinement — TASK-046B)
  EV-019  Prebiotic gum exemption

Changes from v1:
  - L3 gains: high_risk_emulsifier_detected, lecithin_detected, prebiotic_gum_detected
  - L3 gains: allulose_detected
  - L3 gains: polyol_count, detected_polyols
  - L3 gains: sprint1_humectant_polyols, sprint1_penalty_polyol_count, sprint1_penalty_polyols
  - L3 gains: sprint1_additive_count  (corrected additive count after EV-003/019)
  - Original additive_marker_count is preserved for audit comparison

EV-005 humectant refinement (TASK-046B):
  Polyols declared within a manufacturer-labelled humectant group
  ("חומרי הלחה (גליצרול, סורביטול)") are functional moisture-retention
  ingredients, not sweeteners. They carry no laxative-load penalty.
  sprint1_penalty_polyol_count excludes these; sprint1_polyol_count retains
  the full count for audit.

Not changed here (handled in score_engine_v2.py):
  EV-012  fat_quality_v2 (pure scoring formula change; no new signal fields needed)
"""

import re
import sys
import pathlib

# Import from original signal_extractor for everything we don't change
_SRC = pathlib.Path(__file__).resolve().parent.parent / "proto_v0" / "src"
sys.path.insert(0, str(_SRC))

from signal_extractor import (
    ADDED_SUGAR_MARKERS_HE, ADDED_SUGAR_MARKERS_EN,
    SWEETENER_TIER_A_HE, SWEETENER_TIER_A_E,
    SWEETENER_TIER_B_HE, SWEETENER_TIER_B_E,
    SWEETENER_TIER_C_HE, SWEETENER_TIER_C_E,
    ADDITIVE_MARKER_PATTERNS,
    SEED_OIL_MARKERS_HE, PALM_OIL_MARKERS_HE,
    WHOLE_GRAIN_MARKERS_HE, FERMENTATION_MARKERS_HE,
    PROTEIN_ISOLATE_MARKERS_HE, FORTIFICATION_EXPLICIT_HE, SYNTHETIC_VITAMIN_HE,
    FRUIT_CONCENTRATE_MARKERS_HE,
    _search, _search_re,
)
from input_loader import get_nutrition, get_ingredients, get_ingredients_text, get_trust

# ---------------------------------------------------------------------------
# Sprint 1 — New vocabulary: EV-003, EV-004, EV-005, EV-019
# ---------------------------------------------------------------------------

# EV-003 Tier 1 — High-risk emulsifiers (penalty INCREASED)
# These have strong evidence of gut barrier disruption.
HIGH_RISK_EMULSIFIER_PATTERNS = [
    "E466", "E-466", "carboxymethylcellulose", "carboxymethyl cellulose",
    "קרבוקסי מתיל צלולוזה", "קרבוקסי מתיל",
    "E433", "E-433", "polysorbate 80", "polysorbate-80",
    "פוליסורבט 80", "פוליסורבט-80",
    "E407", "E-407", "קרגינן", "carrageenan",
]

# EV-003 Tier 2 — Neutral emulsifiers (EXEMPT from additive penalty)
NEUTRAL_EMULSIFIER_PATTERNS = [
    "לציטין סויה", "לציטין חמניות", "לציטין חמניה", "סויה לציטין",
    "לציטין",          # generic lecithin — exempt if no E-number override
    "E322", "E-322",
]

# EV-019 Tier 3 — Prebiotic gums (EXEMPT from additive/stabilizer penalty)
PREBIOTIC_GUM_PATTERNS = [
    "גומי ערבי", "גומי אקאציה", "gum arabic", "acacia gum",
    "arabinogalactan",
    "E414", "E-414",
]

# EV-004 — Allulose detection
ALLULOSE_PATTERNS = [
    "allulose", "d-allulose", "psicose",
    "אלולוז", "d-אלולוז",
]

# EV-005 — Individual polyol type detection
# Maps polyol name → list of Hebrew/English detection terms
POLYOL_TYPE_MAP = {
    "sorbitol":  ["סורביטול", "sorbitol",   "E420", "E-420"],
    "mannitol":  ["מניטול",   "mannitol",   "E421", "E-421"],
    "xylitol":   ["קסיליטול", "xylitol",    "E967", "E-967"],
    "erythritol":["אריתריטול","erythritol", "E968", "E-968"],
    "maltitol":  ["מלטיטול",  "maltitol",   "E965", "E-965"],
    "isomalt":   ["איזומאלט", "isomalt",    "E953", "E-953"],
    "lactitol":  ["לקטיטול",  "lactitol",   "E966", "E-966"],
}

# Non-lecithin synthetic emulsifiers that SHOULD still trigger the emulsifier
# additive count (EV-003: mono/diglycerides, DATEM, etc.)
NON_LECITHIN_EMULSIFIER_RE = re.compile(
    r"E-?471|E-?472|E-?476|E-?481|DATEM|מונו.{0,5}גליצריד|דיגליצריד",
    re.IGNORECASE
)

# EV-005 humectant refinement (TASK-046B):
# Matches manufacturer-declared humectant groups that may contain polyols.
# Pattern: "חומרי הלחה (...)" or "חומר הלחה (...)" capturing the parenthetical content.
# When a polyol appears inside this group, it is a functional humectant (no penalty).
HUMECTANT_GROUP_RE = re.compile(
    r'חומר(?:י)?\s+הלח[הא]\s*\(([^)]+)\)',
    re.IGNORECASE | re.UNICODE
)


def _detect_high_risk_emulsifier(text: str) -> tuple[bool, list[str]]:
    found = [term for term in HIGH_RISK_EMULSIFIER_PATTERNS if term.lower() in text.lower()]
    return bool(found), found


def _detect_neutral_emulsifier(text: str) -> tuple[bool, list[str]]:
    found = [term for term in NEUTRAL_EMULSIFIER_PATTERNS if term.lower() in text.lower()]
    return bool(found), found


def _detect_prebiotic_gum(text: str) -> tuple[bool, list[str]]:
    found = [term for term in PREBIOTIC_GUM_PATTERNS if term.lower() in text.lower()]
    return bool(found), found


def _detect_allulose(text: str) -> bool:
    return any(p.lower() in text.lower() for p in ALLULOSE_PATTERNS)


def _count_polyol_types(text: str) -> tuple[int, list[str]]:
    detected = []
    for polyol_name, terms in POLYOL_TYPE_MAP.items():
        if any(t.lower() in text.lower() for t in terms):
            detected.append(polyol_name)
    return len(detected), detected


def _extract_humectant_group_polyols(text: str) -> set[str]:
    """
    Return the set of polyol names declared inside manufacturer-labelled
    humectant groups — e.g. "חומרי הלחה (גליצרול, סורביטול)".

    EV-005 humectant refinement (TASK-046B): these polyols are functional
    moisture-retention agents, not sweetener loads; they receive no penalty.
    """
    humectant_polyols: set[str] = set()
    for match in HUMECTANT_GROUP_RE.finditer(text):
        group_content = match.group(1)  # text inside the parentheses
        for polyol_name, terms in POLYOL_TYPE_MAP.items():
            if any(t.lower() in group_content.lower() for t in terms):
                humectant_polyols.add(polyol_name)
    return humectant_polyols


def extract_signals(product: dict) -> dict:
    """
    Extract all signal layers for a product.
    Sprint 1 version: adds EV-003/004/005/019 fields to L3.
    Preserves all v1 fields unchanged for comparison.
    """
    nn = get_nutrition(product)
    ingredients = get_ingredients(product)
    ing_text = get_ingredients_text(product)
    trust_level, trust_score = get_trust(product)

    # -------------------------------------------------------------------------
    # L1: Observed facts (unchanged from v1)
    # -------------------------------------------------------------------------
    l1 = {
        "energy_kcal":      nn["energy_kcal"],
        "fat_g":            nn["fat_g"],
        "fat_saturated_g":  nn["fat_saturated_g"],
        "fat_trans_g":      nn["fat_trans_g"],
        "sodium_mg":        nn["sodium_mg"],
        "carbohydrates_g":  nn["carbohydrates_g"],
        "sugars_g":         nn["sugars_g"],
        "dietary_fiber_g":  nn["dietary_fiber_g"],
        "protein_g":        nn["protein_g"],
        "ingredient_count": len(ingredients),
        "ingredient_list":  ingredients,
        "ingredient_text_quality": product.get("ingredient_text_quality"),
        "bsip1_trust_level":  trust_level,
        "bsip1_trust_score":  trust_score,
        "bsip1_risk_flags":   product.get("canonical_risk_flags") or [],
        "nutrition_consistency_status": product.get("nutrition_consistency_status"),
        "nutrition_consistency_warnings": product.get("nutrition_consistency_warnings") or [],
        "missing_nutrition_fields": [
            f for f in ["energy_kcal","fat_g","fat_saturated_g","sodium_mg",
                        "carbohydrates_g","sugars_g","dietary_fiber_g","protein_g"]
            if nn.get(f) is None
        ],
    }

    kcal  = nn["energy_kcal"]
    sugar = nn["sugars_g"]
    carbs = nn["carbohydrates_g"]
    sat_f = nn["fat_saturated_g"]
    fat   = nn["fat_g"]

    l1["consistency_checks"] = {
        "sugar_le_carbs":  None if (sugar is None or carbs is None) else (sugar <= carbs),
        "satfat_le_fat":   None if (sat_f is None or fat is None)   else (sat_f <= fat),
        "kcal_plausible":  None if kcal is None else (20 <= kcal <= 700),
    }

    # -------------------------------------------------------------------------
    # L2: Derived metrics (unchanged)
    # -------------------------------------------------------------------------
    fat_pct_kcal = (fat * 9 / kcal * 100) if (fat is not None and kcal and kcal > 0) else None
    sat_frac     = (sat_f / fat) if (sat_f is not None and fat and fat > 0) else None
    sugar_carb_r = (sugar / carbs) if (sugar is not None and carbs and carbs > 0) else None
    prot_per_kcal = (nn["protein_g"] / kcal) if (nn["protein_g"] is not None and kcal and kcal > 0) else None

    l2 = {
        "fat_pct_of_kcal":       round(fat_pct_kcal, 2) if fat_pct_kcal is not None else None,
        "saturated_fat_fraction": round(sat_frac, 3)     if sat_frac is not None else None,
        "sugar_to_carb_ratio":   round(sugar_carb_r, 3) if sugar_carb_r is not None else None,
        "protein_per_kcal":      round(prot_per_kcal, 4) if prot_per_kcal is not None else None,
        "derivation_notes": [
            "fat_pct_of_kcal = (fat_g * 9 / energy_kcal) * 100",
            "saturated_fat_fraction = fat_saturated_g / fat_g",
        ],
    }

    # -------------------------------------------------------------------------
    # L3: Inferred classifications — v1 fields + Sprint 1 additions
    # -------------------------------------------------------------------------
    full_text = ing_text + " " + " ".join(ingredients)

    # --- v1: Sweetener detection (unchanged) ---
    tier_a_he = _search(full_text, SWEETENER_TIER_A_HE)
    tier_a_e  = [e for e in SWEETENER_TIER_A_E if e.lower() in full_text.lower()]
    tier_b_he = _search(full_text, SWEETENER_TIER_B_HE)
    tier_b_e  = [e for e in SWEETENER_TIER_B_E if e.lower() in full_text.lower()]
    tier_c_he = _search(full_text, SWEETENER_TIER_C_HE)
    tier_c_e  = [e for e in SWEETENER_TIER_C_E if e.lower() in full_text.lower()]

    has_tier_a = bool(tier_a_he or tier_a_e)
    has_tier_b = bool(tier_b_he or tier_b_e)
    has_tier_c = bool(tier_c_he or tier_c_e)
    has_sweetener = has_tier_a or has_tier_b or has_tier_c

    if has_tier_c:
        sweetener_tier = "C"
    elif has_tier_b:
        sweetener_tier = "B"
    elif has_tier_a:
        sweetener_tier = "A"
    else:
        sweetener_tier = None

    sweetener_matches = tier_a_he + tier_a_e + tier_b_he + tier_b_e + tier_c_he + tier_c_e

    # --- v1: Additive marker detection (unchanged from v1) ---
    additive_categories_raw = _search_re(full_text, ADDITIVE_MARKER_PATTERNS)
    has_flavor_enhancer = additive_categories_raw.get("flavor_enhancer", False)
    has_color = additive_categories_raw.get("color", False)
    additive_marker_count_v1 = len(additive_categories_raw)  # preserved for audit
    additive_categories_list_v1 = sorted(additive_categories_raw.keys())

    # --- Sprint 1: EV-003/019 emulsifier tier detection ---
    high_risk_emuls_detected, high_risk_emuls_found = _detect_high_risk_emulsifier(full_text)
    neutral_emuls_detected, neutral_emuls_found = _detect_neutral_emulsifier(full_text)
    prebiotic_gum_detected, prebiotic_gum_found = _detect_prebiotic_gum(full_text)

    # Sprint 1: Compute corrected additive count
    # Logic:
    #   1. Start with v1 count
    #   2. If "emulsifier" fired, check if it fired solely due to lecithin
    #      → If lecithin detected AND no other synthetic emulsifier → subtract 1
    #   3. If gum arabic detected and "stabilizer" fired solely from gومي → subtract 1
    #   4. If high-risk emulsifier detected → add 2 (weighted penalty)
    sprint1_additive_correction = 0
    correction_notes = []

    if "emulsifier" in additive_categories_raw and neutral_emuls_detected:
        has_other_synthetic_emulsifier = bool(NON_LECITHIN_EMULSIFIER_RE.search(full_text))
        if not has_other_synthetic_emulsifier and not high_risk_emuls_detected:
            # Pure lecithin case: remove incorrect emulsifier penalty
            sprint1_additive_correction -= 1
            correction_notes.append("EV-003/019: lecithin-only emulsifier removed from additive count (-1)")

    if prebiotic_gum_detected and "stabilizer" in additive_categories_raw:
        # Check if a non-prebiotic stabilizer is also present
        OTHER_STABILIZER_RE = re.compile(r"E-?410|E-?412|E-?415|E-?440|מייצב(?!\s*גומי)", re.IGNORECASE)
        if not OTHER_STABILIZER_RE.search(full_text):
            sprint1_additive_correction -= 1
            correction_notes.append("EV-019: prebiotic gum (gum arabic) removed from stabilizer count (-1)")

    if high_risk_emuls_detected:
        sprint1_additive_correction += 2
        correction_notes.append(f"EV-003: high-risk emulsifier detected (+2): {high_risk_emuls_found[:2]}")

    sprint1_additive_count = max(0, additive_marker_count_v1 + sprint1_additive_correction)

    # --- Sprint 1: EV-004 allulose detection ---
    allulose_detected = _detect_allulose(full_text)

    # --- Sprint 1: EV-005 polyol count with humectant refinement (TASK-046B) ---
    polyol_count, detected_polyols = _count_polyol_types(full_text)
    humectant_polyols_detected = _extract_humectant_group_polyols(full_text)
    penalty_polyols    = [p for p in detected_polyols if p not in humectant_polyols_detected]
    penalty_polyol_count = len(penalty_polyols)

    # --- v1: remaining L3 fields (unchanged) ---
    seed_oil_matches = _search(full_text, SEED_OIL_MARKERS_HE)
    has_seed_oil = bool(seed_oil_matches)

    palm_oil_matches = _search(full_text, PALM_OIL_MARKERS_HE)
    has_palm_oil = bool(palm_oil_matches)

    whole_grain_matches = _search(full_text, WHOLE_GRAIN_MARKERS_HE)
    has_whole_grain = bool(whole_grain_matches)

    isolate_matches = _search(full_text, PROTEIN_ISOLATE_MARKERS_HE)
    if isolate_matches:
        protein_source = "mixed"
        protein_source_basis = isolate_matches
    elif nn["protein_g"] and nn["protein_g"] > 0:
        protein_source = "whole_food"
        protein_source_basis = ["no isolate markers detected"]
    else:
        protein_source = "unknown"
        protein_source_basis = ["insufficient protein signal"]

    added_sugar_matches = [m for m in ADDED_SUGAR_MARKERS_HE
                          if m in full_text and m != "דבש"]
    added_sugar_count = len(added_sugar_matches)

    fruit_conc_matches = _search(full_text, FRUIT_CONCENTRATE_MARKERS_HE)
    has_fruit_concentrate = bool(fruit_conc_matches)

    ferm_matches = _search(full_text, FERMENTATION_MARKERS_HE)
    has_fermentation = bool(ferm_matches)

    DAIRY_BASE_MARKERS_HE = ["חלב", "יוגורט", "גבינת", "מי גבינה", "קזאין"]
    first_three_text = " ".join(ingredients[:3]).lower() if ingredients else ing_text[:200].lower()
    product_type_dairy = any(m in first_three_text for m in DAIRY_BASE_MARKERS_HE)

    trans_fat_g = nn["fat_trans_g"]
    if trans_fat_g is not None and trans_fat_g > 1.0:
        trans_fat_status = "veto"
    elif trans_fat_g is not None and trans_fat_g > 0.5:
        trans_fat_status = "high_concern"
    elif trans_fat_g is not None and trans_fat_g == 0.5:
        trans_fat_status = "threshold_declaration"
    elif trans_fat_g is not None and trans_fat_g > 0.2:
        trans_fat_status = "present"
    else:
        trans_fat_status = "not_detected"

    has_fortification_explicit = any(m in full_text for m in FORTIFICATION_EXPLICIT_HE)
    vitamin_hits = [v for v in SYNTHETIC_VITAMIN_HE if v in full_text]
    has_fortification_inferred = len(set(vitamin_hits)) >= 2
    has_fortification = has_fortification_explicit or has_fortification_inferred

    red_labels = []
    if sugar is not None and sugar > 17.5:
        red_labels.append("sugar")
    if sat_f is not None and sat_f > 5.0:
        red_labels.append("sat_fat")
    if nn["sodium_mg"] is not None and nn["sodium_mg"] > 600:
        red_labels.append("sodium")

    fat_pct_calc = fat_pct_kcal
    hp_fat_sugar_raw = (
        fat_pct_calc is not None and fat_pct_calc >= 30 and
        sugar is not None and sugar >= 20
    )
    hp_fat_sodium_raw = (
        fat_pct_calc is not None and fat_pct_calc >= 25 and
        nn["sodium_mg"] is not None and nn["sodium_mg"] >= 300
    )

    l3 = {
        # v1 fields (preserved)
        "sweetener_detected":       has_sweetener,
        "sweetener_tier":           sweetener_tier,
        "sweetener_matches":        sweetener_matches,
        "additive_marker_count":    additive_marker_count_v1,   # v1 (preserved for audit)
        "additive_categories":      additive_categories_list_v1,
        "has_flavor_enhancer":      has_flavor_enhancer,
        "has_artificial_color":     has_color,
        "has_seed_oil":             has_seed_oil,
        "seed_oil_matches":         seed_oil_matches,
        "has_palm_oil":             has_palm_oil,
        "palm_oil_matches":         palm_oil_matches,
        "has_whole_grain":          has_whole_grain,
        "whole_grain_matches":      whole_grain_matches,
        "protein_source":           protein_source,
        "protein_source_basis":     protein_source_basis,
        "added_sugar_sources_count": added_sugar_count,
        "added_sugar_matches":      added_sugar_matches[:8],
        "has_fruit_concentrate":    has_fruit_concentrate,
        "has_fermentation":         has_fermentation,
        "product_type_dairy":       product_type_dairy,
        "has_fortification":        has_fortification,
        "fortification_evidence":   [],
        "trans_fat_status":         trans_fat_status,
        "trans_fat_threshold_declaration_possible": (trans_fat_g == 0.5),
        "red_labels":               red_labels,
        "red_label_count":          len(red_labels),
        "hp_fat_sugar_pattern_raw": hp_fat_sugar_raw,
        "hp_fat_sodium_pattern_raw": hp_fat_sodium_raw,
        # Sprint 1 additions
        "sprint1_high_risk_emulsifier_detected": high_risk_emuls_detected,
        "sprint1_high_risk_emulsifier_found":    high_risk_emuls_found,
        "sprint1_neutral_emulsifier_detected":   neutral_emuls_detected,
        "sprint1_neutral_emulsifier_found":      neutral_emuls_found,
        "sprint1_prebiotic_gum_detected":        prebiotic_gum_detected,
        "sprint1_prebiotic_gum_found":           prebiotic_gum_found,
        "sprint1_additive_count":                sprint1_additive_count,
        "sprint1_additive_correction":           sprint1_additive_correction,
        "sprint1_additive_correction_notes":     correction_notes,
        "sprint1_allulose_detected":             allulose_detected,
        "sprint1_polyol_count":                  polyol_count,           # total detected (audit)
        "sprint1_detected_polyols":              detected_polyols,       # all polyols found
        "sprint1_humectant_polyols":             sorted(humectant_polyols_detected),  # excluded from penalty
        "sprint1_penalty_polyol_count":          penalty_polyol_count,   # used for scoring
        "sprint1_penalty_polyols":               penalty_polyols,        # polyols that attract penalty
        "inference_confidence_notes": [
            "Sprint 1: EV-003/019/004/005 fields added",
            "sprint1_additive_count is the corrected count used for v2 scoring",
            "additive_marker_count is the original v1 count (preserved for rollback)",
            "EV-005 humectant refinement (TASK-046B): penalty uses sprint1_penalty_polyol_count",
        ],
    }

    l4 = {
        "note": "L4 interpreted concerns are evaluated in score_engine and written to caps_applied",
        "pre_evaluation_flags": [],
    }
    if l1["consistency_checks"]["sugar_le_carbs"] is False:
        l4["pre_evaluation_flags"].append("SUGAR_EXCEEDS_CARBS")
    if l1["consistency_checks"]["satfat_le_fat"] is False:
        l4["pre_evaluation_flags"].append("SATFAT_EXCEEDS_FAT")

    l5 = {"hypotheses_active": ["v1 hypotheses unchanged; see original signal_extractor.py"]}
    l6 = {"policy_commitments": ["v1 policy unchanged; see original signal_extractor.py"],
          "architecture_version": "bsip2_sprint1_v1"}

    return {
        "L1_observed_signals":         l1,
        "L2_derived_signals":          l2,
        "L3_inferred_classifications": l3,
        "L4_interpreted_concerns":     l4,
        "L5_behavioral_hypotheses":    l5,
        "L6_policy_decisions":         l6,
    }
