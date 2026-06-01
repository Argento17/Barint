"""
Feature extraction with proper missing-data handling and Hebrew-aware matching.
"""

from typing import Dict, Any
from bsip2_models import FoodProduct
from bsip2_config import INGREDIENT_MARKERS
from bsip2_hebrew import contains_any, count_terms
from bsip2_category_inference import infer_category


def _ingredients_text(product: FoodProduct) -> str:
    return " ".join([
        product.text("ingredients_raw_he"),
        product.text("ingredients_raw_en"),
        product.text("ingredients_raw"),
    ]).strip()


def _split_ingredients(ingredients: str) -> int:
    if not ingredients:
        return 0

    items = [
        x.strip()
        for x in ingredients.replace(";", ",").split(",")
        if x.strip()
    ]

    return len(items)


def extract_features(product: FoodProduct) -> Dict[str, Any]:

    ingredients = _ingredients_text(product)
    txt = ingredients.lower()

    # ---------------------------------------------------------
    # Missing-aware numeric extraction
    # ---------------------------------------------------------

    def n(key: str, fallback: str = None):
        v = product.num(key, None)

        if v is None and fallback:
            v = product.num(fallback, None)

        return v

    nutrition = {
        "energy_kcal_100g":     n("energy_kcal_100g", "energy_kcal"),
        "protein_g_100g":       n("protein_g_100g", "protein_g"),
        "sugars_g_100g":        n("sugars_g_100g", "sugars_g"),
        "carbs_g_100g":         n("carbs_g_100g", "carbs_g"),
        "fat_g_100g":           n("fat_g_100g", "fat_g"),
        "saturated_fat_g_100g": n("saturated_fat_g_100g", "saturated_fat_g"),
        "fiber_g_100g":         n("fiber_g_100g", "fiber_g"),
        "sodium_mg_100g":       n("sodium_mg_100g", "sodium_mg"),
    }

    known_fields = {
        k: v is not None
        for k, v in nutrition.items()
    }

    # Use safe compute fallback but preserve missingness separately
    nutrition_safe = {
        k: (v if v is not None else 0.0)
        for k, v in nutrition.items()
    }

    # ---------------------------------------------------------
    # Regulatory labels
    # ---------------------------------------------------------

    red_count = sum(
        1
        for k in [
            "red_label_sugar",
            "red_label_sodium",
            "red_label_saturated_fat",
        ]
        if product.boolish(k) is True
    )

    # ---------------------------------------------------------
    # Core features
    # ---------------------------------------------------------

    f: Dict[str, Any] = {
        **nutrition_safe,

        "known_fields": known_fields,

        "ingredients_text": ingredients,
        "ingredients_available": bool(ingredients),

        "ingredient_count": _split_ingredients(ingredients),

        "red_label_count": red_count,

        "red_label_sugar": product.boolish("red_label_sugar"),
        "red_label_sodium": product.boolish("red_label_sodium"),
        "red_label_saturated_fat": product.boolish("red_label_saturated_fat"),

        # -----------------------------------------------------
        # Existing ingredient markers
        # -----------------------------------------------------

        "has_added_sugar_marker":
            contains_any(ingredients, INGREDIENT_MARKERS["added_sugar"]),

        "added_sugar_marker_count":
            count_terms(ingredients, INGREDIENT_MARKERS["added_sugar"]),

        "has_sweetener":
            contains_any(ingredients, INGREDIENT_MARKERS["sweetener"]),

        "has_emulsifier":
            contains_any(ingredients, INGREDIENT_MARKERS["emulsifier"]),

        "has_stabilizer":
            contains_any(ingredients, INGREDIENT_MARKERS["stabilizer"]),

        "has_protein_isolate":
            contains_any(ingredients, INGREDIENT_MARKERS["protein_isolate"]),

        "has_seed_oil":
            contains_any(ingredients, INGREDIENT_MARKERS["seed_oil"]),

        "has_whole_food_marker":
            contains_any(ingredients, INGREDIENT_MARKERS["whole_food_positive"]),
    }

    # ---------------------------------------------------------
    # NEW STRUCTURAL / MATRIX FEATURES
    # ---------------------------------------------------------

    f["has_glucose_syrup"] = (
        "סירופ גלוקוז" in txt
        or "glucose syrup" in txt
    )

    f["has_maltodextrin"] = (
        "מלטודקסטרין" in txt
        or "maltodextrin" in txt
    )

    f["has_flavouring"] = (
        "חומרי טעם" in txt
        or "flavour" in txt
        or "flavor" in txt
    )

    f["has_emulsifier"] = (
        f["has_emulsifier"]
        or "מתחלב" in txt
        or "emulsifier" in txt
    )

    f["has_chocolate_coating"] = (
        "ציפוי" in txt
        or "שוקולד" in txt
        or "coating" in txt
    )

    f["has_coating"] = (
        "ציפוי" in txt
        or "coating" in txt
    )

    f["has_extruded_or_puffed_grain"] = (
        "פצפוצי" in txt
        or "crispy" in txt
        or "puffed" in txt
        or "extruded" in txt
    )

    f["has_crispy_cereal"] = (
        "קריספי" in txt
        or "crispy" in txt
    )

    f["has_nut_or_seed_marker"] = any(
        x in txt
        for x in [
            "שקד",
            "אגוז",
            "בוטן",
            "קשיו",
            "לוז",
            "פקאן",
            "פיסטוק",
            "זרע",
            "גרעין",
            "almond",
            "nut",
            "peanut",
            "cashew",
            "seed",
        ]
    )

    f["has_whole_grain_marker"] = (
        "דגן מלא" in txt
        or "מלא" in txt
        or "whole grain" in txt
    )

    f["has_date_or_fruit_paste"] = (
        "תמר" in txt
        or "date" in txt
        or "fruit paste" in txt
        or "רכז פרי" in txt
    )

    f["has_hydrogenated_fat"] = (
        "מוקשה" in txt
        or "hydrogenated" in txt
    )

    # ---------------------------------------------------------
    # Additive marker count
    # ---------------------------------------------------------

    f["additive_marker_count"] = sum([
        int(f["has_sweetener"]),
        int(f["has_emulsifier"]),
        int(f["has_stabilizer"]),
        int(f["has_protein_isolate"]),
    ])

    # ---------------------------------------------------------
    # NOVA proxy
    # ---------------------------------------------------------

    nova_class, nova_conf = _infer_nova(f)

    f["nova_proxy"] = nova_class
    f["nova_proxy_confidence"] = nova_conf

    # ---------------------------------------------------------
    # Category inference
    # ---------------------------------------------------------

    category, cat_conf = infer_category(product.raw, f)

    f["inferred_category"] = category
    f["inferred_category_confidence"] = cat_conf

    return f


def _infer_nova(f: Dict[str, Any]):

    """
    Returns:
        (nova_class, confidence)
    """

    engineered_markers = sum([
        int(f["has_glucose_syrup"]),
        int(f["has_maltodextrin"]),
        int(f["has_emulsifier"]),
        int(f["has_flavouring"]),
        int(f["has_extruded_or_puffed_grain"]),
        int(f["has_chocolate_coating"]),
    ])

    if engineered_markers >= 3:
        return 4, 0.90

    if engineered_markers >= 2 and f["ingredient_count"] >= 8:
        return 4, 0.80

    if (
        f["additive_marker_count"] >= 2
        or (
            f["has_sweetener"]
            and f["has_protein_isolate"]
        )
    ):
        return 4, 0.80

    if (
        f["ingredient_count"] >= 8
        or (
            f["has_added_sugar_marker"]
            and f["additive_marker_count"] >= 1
        )
    ):
        return 3, 0.65

    if (
        f["ingredient_count"] <= 2
        and f["has_whole_food_marker"]
    ):
        return 1, 0.85

    if f["ingredient_count"] <= 4:
        return 2, 0.55

    return 3, 0.45