"""
Infer broad product category from name, retailer category, and ingredients.
Used by calorie engine to apply category-aware thresholds.
"""
from typing import Dict, Any, Tuple
from bsip2_config import CATEGORY_KEYWORDS
from bsip2_hebrew import contains_any


def infer_category(product_raw: Dict[str, Any], features: Dict[str, Any]) -> Tuple[str, float]:
    """
    Returns (category, confidence 0..1).
    Resolution order: explicit category column → name match → retailer category → ingredient dominance → 'default'.
    """
    name_he = str(product_raw.get("product_name_he") or product_raw.get("product_name_heb") or "")
    name_en = str(product_raw.get("product_name_en") or product_raw.get("product_name") or "")
    retailer_cat = str(product_raw.get("retailer_category") or "")
    ingredients = features.get("ingredients_text", "")
    haystack_name = f"{name_he} {name_en} {retailer_cat}"

    scores: Dict[str, float] = {}
    for category, kw in CATEGORY_KEYWORDS.items():
        score = 0.0
        if contains_any(haystack_name, kw.get("name_he", []) + kw.get("name_en", [])):
            score += 0.7
        if "ingredient_dominance" in kw and contains_any(ingredients, kw["ingredient_dominance"]):
            score += 0.4
        if score > 0:
            scores[category] = score

    if not scores:
        return "default", 0.3

    best_cat = max(scores, key=scores.get)
    confidence = min(1.0, scores[best_cat])
    return best_cat, confidence