"""
BSIP2 Prototype v0 — Evaluation Scope
Assigns evaluation_status before scoring runs. (SRC-03, evaluation_scope.md)
This gate runs first. out_of_scope products are not scored.
"""

OUT_OF_SCOPE_SIGNALS_HE = [
    "תחליף חלב אם",    # infant formula
    "תזונה רפואית",     # medical nutrition
    "מזון לתינוקות",    # baby food (strong signal)
    "הזנה קלינית",      # clinical nutrition
    "תוסף ספורט",       # sports supplement
    "ג'ל אנרגיה",       # energy gel
    "אבקת חלב לתינוק",  # infant milk powder
]

# Context-limited signals are checked against the PRODUCT NAME only, not ingredient text.
# A product that IS honey is context-limited. A product that CONTAINS honey is not.
# Nutritional thresholds are secondary validators to reduce false positives.
CONTEXT_LIMITED_SIGNALS = {
    "cooking_oil": {
        "name_keywords": [
            "שמן זית", "שמן קוקוס", "שמן חמניות", "שמן קנולה",
            "שמן תירס", "שמן סויה", "שמן שומשום",
            "שמן בישול", "שמן דקל",
            "חמאה",   # butter
            "גהי",    # ghee
            "מרגרינה",  # margarine
        ],
        "nutrition_validator": lambda nn: (nn.get("fat_g") or 0) > 50,  # must be predominantly fat
    },
    "condiment_high_concentration": {
        "name_keywords": [
            "רוטב סויה", "רוטב דגים", "חרדל",
            "מיסו", "רוטב ווסטרשייר",
        ],
        "nutrition_validator": lambda nn: (nn.get("sodium_mg") or 0) > 600,
    },
    "brined_food": {
        "name_keywords": [
            "זיתים", "זיתים כבושים", "חמוצים", "כרוב כבוש",
            "ירקות כבושים", "קיפר",
        ],
        "nutrition_validator": lambda nn: (nn.get("sodium_mg") or 0) > 500,
    },
    "concentrated_sweetener": {
        "name_keywords": [
            "דבש", "סירופ מייפל", "סירופ אגבה", "מולסה",
            "סירופ תמרים",
        ],
        "nutrition_validator": lambda nn: (nn.get("sugars_g") or 0) > 40,
    },
}

CONTEXT_NOTE_TEMPLATES = {
    "cooking_oil": (
        "Typically consumed in 10–20g portions. Per-100g calorie density and satiety metrics "
        "do not reflect dietary contribution from typical use. "
        "Fat composition evaluation remains meaningful. (SRC-03)"
    ),
    "condiment_high_concentration": (
        "Consumed in 5–15g portions. Sodium concentration per 100g does not reflect "
        "dietary sodium load from typical use. (SRC-03)"
    ),
    "brined_food": (
        "Sodium reflects preservation brine. Not all sodium in the per-100g figure is consumed; "
        "brine is typically not eaten. (SRC-03)"
    ),
    "concentrated_sweetener": (
        "Consumed in small quantities (5–20g). Per-100g sugar analysis reflects concentration, "
        "not typical consumption load. (SRC-03)"
    ),
    "standard": None,
}


def assign_evaluation_scope(product: dict, category: str) -> dict:
    """
    Determine evaluation_status for a product.
    Must run before any scoring.

    Returns:
    {
        "evaluation_status": "standard" | "context_limited" | "out_of_scope",
        "context_flag": str | None,
        "context_note": str | None,
        "scope_basis": list[str],
    }
    """
    name = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()
    search_text = name + " " + ing_text
    nn = product.get("normalized_nutrition_per_100g") or {}

    # --- Check out_of_scope first ---
    for signal in OUT_OF_SCOPE_SIGNALS_HE:
        if signal in search_text:
            return {
                "evaluation_status": "out_of_scope",
                "context_flag": "out_of_scope",
                "context_note": f"Product appears to be out of BSIP2 scope: detected signal '{signal}'. No score will be produced.",
                "scope_basis": [f"name/ingredient signal: {signal}"],
            }

    # --- No-data check: cannot evaluate if no nutrition at all ---
    kcal = nn.get("energy_kcal")
    has_any_nutrition = any(nn.get(f) is not None for f in
                            ["energy_kcal","fat_g","protein_g","carbohydrates_g"])
    if not has_any_nutrition:
        return {
            "evaluation_status": "context_limited",
            "context_flag": "no_nutrition_data",
            "context_note": "No nutrition data available. Score cannot be computed meaningfully. Confidence will be very low.",
            "scope_basis": ["all nutrition fields absent"],
        }

    # --- Check context_limited categories ---
    # Only check product NAME (not ingredient text) to avoid false positives from
    # products that merely contain a context-limited ingredient (e.g., a snack bar with honey).
    name_only = (product.get("canonical_name_he") or "").lower()

    for flag, spec in CONTEXT_LIMITED_SIGNALS.items():
        keywords = spec.get("name_keywords", [])
        validator = spec.get("nutrition_validator", lambda nn: True)
        for keyword in keywords:
            if keyword in name_only and validator(nn):
                return {
                    "evaluation_status": "context_limited",
                    "context_flag": flag,
                    "context_note": CONTEXT_NOTE_TEMPLATES.get(flag),
                    "scope_basis": [f"product name signal: '{keyword}' (nutrition validator passed)"],
                }

    # Category-based context limitation: whole_food_fat with extreme nutritional profile
    if category == "whole_food_fat":
        kcal_v = kcal or 0
        fat_v = nn.get("fat_g") or 0
        if fat_v > 80:
            return {
                "evaluation_status": "context_limited",
                "context_flag": "cooking_oil",
                "context_note": CONTEXT_NOTE_TEMPLATES["cooking_oil"],
                "scope_basis": [f"whole_food_fat category with fat={fat_v}g/100g: likely pure fat product"],
            }

    # --- Standard ---
    return {
        "evaluation_status": "standard",
        "context_flag": None,
        "context_note": None,
        "scope_basis": ["no out_of_scope or context_limited signals detected"],
    }
