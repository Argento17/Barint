"""
Dimension scoring. Pure functions. No double-counting with guardrails.
"""
from bsip2_models import DimensionScores
from bsip2_config import DIMENSION_PARAMS
from bsip2_calorie_engine import score_calorie_density


def clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))


def nz(x, default: float = 0.0) -> float:
    """Use only for scoring math; missingness is handled separately via known_fields."""
    return default if x is None else x


def calculate_dimensions(f) -> DimensionScores:
    P = DIMENSION_PARAMS

    known = f.get("known_fields", {})

    protein = nz(f.get("protein_g_100g"))
    fiber   = nz(f.get("fiber_g_100g"))
    sugar   = nz(f.get("sugars_g_100g"))
    sat_fat = nz(f.get("saturated_fat_g_100g"))
    sodium  = nz(f.get("sodium_mg_100g"))
    kcal    = nz(f.get("energy_kcal_100g"))
    carb    = nz(f.get("carbs_g_100g"))

    # ---- nutrient_density ----
    p = P["nutrient_density"]
    nd = p["base"]
    nd += min(protein * p["protein_coef"], p["protein_cap"])
    nd += min(fiber   * p["fiber_coef"],   p["fiber_cap"])
    nd -= max((sugar  - p["sugar_threshold"]) * p["sugar_penalty"], 0)
    nd -= max((sodium - p["sodium_threshold"]) / p["sodium_divisor"], 0)

    # ---- glycemic_quality ----
    p = P["glycemic_quality"]
    gq = p["base"]
    gq -= max((sugar - p["sugar_threshold"]) * p["sugar_penalty"], 0)
    gq -= max((carb  - p["carb_threshold"])  * p["carb_penalty"], 0)
    gq += min(fiber * p["fiber_coef"], p["fiber_cap"])

    # ---- processing_quality ----
    p = P["processing_quality"]
    pq = p["base"]

    nova_proxy = f.get("nova_proxy", 3)
    if nova_proxy == 4:
        pq -= p["nova_4_penalty"]
    elif nova_proxy == 3:
        pq -= p["nova_3_penalty"]

    ingredient_count = f.get("ingredient_count", 0) or 0
    pq -= max(ingredient_count - p["ingredient_count_threshold"], 0) * p["ingredient_count_penalty_per_extra"]

    if f.get("has_whole_food_marker"):
        pq += p["whole_food_bonus"]

    # Extra processing drag: low additives does NOT mean low processing
    if f.get("has_glucose_syrup") or f.get("has_maltodextrin"):
        pq -= 8
    if f.get("has_flavouring") or f.get("has_flavoring"):
        pq -= 6
    if f.get("has_emulsifier"):
        pq -= 6
    if f.get("has_chocolate_coating") or f.get("has_coating"):
        pq -= 8
    if f.get("has_extruded_or_puffed_grain"):
        pq -= 8

    # ---- protein_quality ----
    p = P["protein_quality"]
    prq = p["base"] + min(protein * p["protein_coef"], p["protein_cap"])
    if f.get("has_protein_isolate"):
        prq -= p["isolate_penalty"]

    # ---- fat_quality ----
    p = P["fat_quality"]
    fq = p["base"] - max((sat_fat - p["satfat_threshold"]) * p["satfat_penalty"], 0)

    if f.get("has_seed_oil"):
        fq -= p["seed_oil_penalty"]

    # Relief for nut/seed dominant bars
    if f.get("has_nut_or_seed_marker") and not f.get("has_hydrogenated_fat"):
        fq += 8

    # ---- additive_quality ----
    p = P["additive_quality"]
    aq = p["base"] - (f.get("additive_marker_count", 0) or 0) * p["per_marker_penalty"]
    if f.get("has_sweetener"):
        aq -= p["sweetener_penalty"]

    # ---- satiety_support ----
    p = P["satiety_support"]
    ss = p["base"]
    ss += min(protein * p["protein_coef"], p["protein_cap"])
    ss += min(fiber   * p["fiber_coef"],   p["fiber_cap"])
    ss -= max((sugar - p["sugar_threshold"]) * p["sugar_penalty"], 0)

    # Matrix-based satiety adjustments
    if f.get("has_nut_or_seed_marker"):
        ss += 6
    if f.get("has_whole_grain_marker"):
        ss += 4
    if f.get("has_chocolate_coating") or f.get("has_coating"):
        ss -= 5

    # ---- regulatory_quality ----
    p = P["regulatory_quality"]
    rq = p["base"] - (f.get("red_label_count", 0) or 0) * p["per_red_label_penalty"]

    # ---- whole_food_integrity ----
    p = P["whole_food_integrity"]
    wfi = p["base"]

    if f.get("has_whole_food_marker"):
        wfi += p["whole_food_bonus"]

    if nova_proxy == 4:
        wfi -= p["nova_4_penalty"]
    elif nova_proxy == 3:
        wfi -= p["nova_3_penalty"]

    wfi -= max(ingredient_count - p["ingredient_count_threshold"], 0) * p["per_extra_ingredient_penalty"]

    # Food matrix adjustments
    if f.get("has_nut_or_seed_marker"):
        wfi += 8
    if f.get("has_whole_grain_marker"):
        wfi += 5
    if f.get("has_glucose_syrup") or f.get("has_maltodextrin"):
        wfi -= 8
    if f.get("has_chocolate_coating") or f.get("has_coating"):
        wfi -= 8
    if f.get("has_extruded_or_puffed_grain"):
        wfi -= 8

    # ---- calorie_density_quality ----
    cdq = score_calorie_density(kcal, f.get("inferred_category", "unknown"))

    # ---- confidence ----
    confidence = 90

    critical_fields = [
        "energy_kcal_100g",
        "protein_g_100g",
        "carbs_g_100g",
        "fat_g_100g",
    ]

    critical_missing = sum(1 for k in critical_fields if not known.get(k, False))
    confidence -= critical_missing * 10

    if not f.get("ingredients_available", False):
        confidence -= 25

    if not known.get("fiber_g_100g", False):
        confidence -= 5

    if not known.get("sodium_mg_100g", False):
        confidence -= 5

    confidence -= int((1 - f.get("nova_proxy_confidence", 0.5)) * 10)

    # New: category uncertainty should lower confidence
    confidence -= int((1 - f.get("inferred_category_confidence", 0.5)) * 15)

    # Suspicious value checks
    if known.get("sugars_g_100g", False) and known.get("carbs_g_100g", False) and sugar > carb:
        confidence -= 20

    if known.get("saturated_fat_g_100g", False) and known.get("fat_g_100g", False):
        fat = nz(f.get("fat_g_100g"))
        if sat_fat > fat:
            confidence -= 20

    if known.get("energy_kcal_100g", False) and (kcal < 20 or kcal > 700):
        confidence -= 10

    return DimensionScores(
        nutrient_density=clamp(nd),
        processing_quality=clamp(pq),
        protein_quality=clamp(prq),
        glycemic_quality=clamp(gq),
        fat_quality=clamp(fq),
        additive_quality=clamp(aq),
        satiety_support=clamp(ss),
        regulatory_quality=clamp(rq),
        whole_food_integrity=clamp(wfi),
        calorie_density_quality=clamp(cdq),
        confidence=clamp(confidence),
    )