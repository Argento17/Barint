"""
BSIP2 Prototype v0 — Category Classifier
Rule-based category inference from Hebrew product name + nutritional profile.
Returns category, confidence, secondary candidate, and instability flag.
SRC-07 applies: confidence modulates category-specific cap thresholds downstream.

Beverage and dairy_protein signals are matched against the product NAME ONLY,
not ingredient text, to prevent false classification from ingredient presence.
A product that contains milk is not necessarily a dairy product;
a product that contains juice is not necessarily a beverage.
"""

CATEGORIES = [
    "whole_food_fat",
    "snack_bar_granola",
    "dessert",
    "beverage",
    "dairy_protein",
    "cereal",
    "sauce_spread",
    "default",
]

# Hebrew keyword signals matched against full text (name + ingredient text)
CATEGORY_SIGNALS = {
    "whole_food_fat": [
        ("שמן", 0.5), ("טחינה", 0.9), ("חמאה", 0.7), ("אגוז", 0.7),
        ("שקד", 0.7), ("גרעין", 0.6), ("אבוקדו", 0.9), ("זית", 0.5),
        ("שומשום", 0.7), ("כוסמת", 0.3), ("אגוזים", 0.7),
        ("שמן זית", 0.95), ("שמן קוקוס", 0.9), ("ממרח", 0.4),
        ("חמאת בוטנים", 0.9), ("חמאת שקדים", 0.9),
    ],
    "snack_bar_granola": [
        ("חטיף דגנים", 0.95), ("חטיף", 0.5), ("גרנולה", 0.9),
        ("קורני", 0.9), ("כורני", 0.9), ("מוסלי", 0.85), ("ברים", 0.7),
        ("בר", 0.4), ("צ'יה", 0.3), ("אנרגיה", 0.3),
        ("דגנים", 0.4), ("שוקולד", 0.3), ("קריספי", 0.4),
        ("פצפוצי", 0.6), ("ציפוי", 0.3), ("שוקו", 0.3),
        ("וופל", 0.4), ("ביסקוויט", 0.5),
        ("מילוי קרם", 0.5), ("מילוי", 0.3), ("שכבת", 0.3),
        ("קרמל", 0.3), ("בוטנים", 0.4),
    ],
    "dessert": [
        ("עוגה", 0.85), ("קינוח", 0.85), ("קרם", 0.5),
        ("פודינג", 0.8), ("מוס", 0.85), ("גלידה", 0.9),
        ("שוקולד", 0.3),  # weak signal — also in snack bars
        ("טארט", 0.9), ("מאפה", 0.8), ("סופגניה", 0.95),
        ("רולדה", 0.85), ("בראוניז", 0.9), ("פרלינה", 0.8),
    ],
    "cereal": [
        ("דגני בוקר", 0.95), ("קורנפלקס", 0.95), ("שיבולת שועל", 0.8),
        ("גרנולה לבוקר", 0.9), ("וולה", 0.9), ("קרנפלקס", 0.9),
        ("פתיתי", 0.5), ("אוברן", 0.7),
    ],
    "sauce_spread": [
        ("רוטב", 0.9), ("ממרח", 0.7), ("קטשופ", 0.95),
        ("חרדל", 0.9), ("מיונז", 0.95), ("חומוס", 0.85),
        ("טפנד", 0.9), ("ממרח שוקולד", 0.95), ("הלב", 0.4),
        ("פסטה", 0.4), ("ציר", 0.7),
    ],
}

# These signals are matched against the product NAME ONLY, not ingredient text.
# Rationale: a snack bar that contains milk is not a dairy product;
# a snack bar that contains juice is not a beverage.
CATEGORY_SIGNALS_NAME_ONLY = {
    "beverage": [
        ("משקה", 0.9), ("שתייה", 0.9), ("מיץ", 0.9),
        ("תה", 0.85), ("קפה", 0.85), ("מים", 0.7),
        ("לימונדה", 0.9), ("קולה", 0.95), ("סודה", 0.8),
        ("קוקטייל", 0.85), ("מיצוי", 0.6),
    ],
    "dairy_protein": [
        ("יוגורט", 0.95), ("קוטג'", 0.95), ("גבינה", 0.85),
        ("חלב", 0.7), ("לבן", 0.6), ("קפיר", 0.95),
        ("ריקוטה", 0.9), ("מסקרפונה", 0.9),
    ],
}

# Beverage must have at least one liquid-context keyword in the product name.
# Prevents tea-flavored or coffee-flavored snack bars from scoring as beverage.
BEVERAGE_LIQUID_GATE_KEYWORDS = [
    "ml", 'מ"ל', "ליטר", "בקבוק", "משקה", "שתייה", "שתיה", "מיץ", "קולה", "סודה",
]

# Fallback A: liquid unit in nutrition_basis_claimed (e.g. "ל1 ליטר")
LIQUID_BASIS_TERMS = ["ליטר", 'מ"ל', "מל"]

# Fallback B: known plant-milk brands that are exclusively liquid products
KNOWN_PLANT_MILK_BRANDS = {
    "אלפרו", "alpro",
    "oatly", "אוטלי",
    "vitariz", "ויטאריז",
    "silk", "provamel",
}

# Fallback C: plant-milk base ingredient terms found in the product NAME
PLANT_MILK_BASE_NAME_TERMS = [
    "שקדים",        # almonds
    "שיבולת שועל",  # oats
    "סויה",         # soy
    "אורז",         # rice
    "קוקוס",        # coconut
    "שומשום",       # sesame
    "קשיו",         # cashew
    "אפונה",        # pea
]

# Solid-food exclusions: if any of these appear in the name alongside a plant-milk
# base term, the product is not a beverage (e.g. almond butter, soy cheese, oat bars).
PLANT_MILK_SOLID_EXCLUSIONS = [
    "חמאה",   # butter
    "גבינה",  # cheese
    "יוגורט", # yogurt
    "גלידה",  # ice cream
    "קוטג",   # cottage
    "ממרח",   # spread
    "שמן",    # oil
    # Snack/bar form indicators — prevent oat bars, granola bars, etc. from matching
    "חטיף",   # snack bar
    "חטיפי",  # snack bars (plural construct)
    "ברים",   # bars
    "גרנולה", # granola
    "מצופה",  # coated (coated bars)
    "ציפוי",  # coating
    "ביסקוויט",  # biscuit
    "דגנים",  # cereal/grains (bar context)
]

# If any of these appear in the product name immediately before a dairy keyword,
# the match is a flavor descriptor rather than a dairy product ("בטעם יוגורט" = yogurt-flavored).
DAIRY_FLAVOR_SUPPRESSORS = [
    "בטעם",   # "in the flavor of"
    "טעם",    # "flavor" / "taste"
    "בניחוח", # "with aroma of"
]


# Nutritional profile heuristics for disambiguation
def _nutritional_hints(nn: dict) -> dict[str, float]:
    """Return score boosts per category based on nutritional profile."""
    hints = {cat: 0.0 for cat in CATEGORIES}
    kcal = nn.get("energy_kcal") or 0
    fat  = nn.get("fat_g") or 0
    prot = nn.get("protein_g") or 0

    # Very high fat → likely whole_food_fat
    if kcal > 600 and fat > 50:
        hints["whole_food_fat"] += 0.4
    # Very low kcal → likely beverage
    if kcal < 30:
        hints["beverage"] += 0.4
    # High protein, low kcal → likely dairy_protein
    if prot > 8 and kcal < 200:
        hints["dairy_protein"] += 0.3
    # Moderate kcal 350-500, likely snack bar
    if 350 <= kcal <= 520:
        hints["snack_bar_granola"] += 0.15
    # Very high kcal (500-700), high fat → whole_food_fat or snack bar
    if kcal >= 500 and fat >= 20:
        hints["whole_food_fat"] += 0.1

    return hints


def classify_category(product: dict) -> dict:
    """
    Classify product into a BSIP2 scoring category.
    Returns:
    {
        "category": str,
        "category_confidence": float,  # 0.0-1.0
        "secondary_category": str,
        "secondary_confidence": float,
        "category_instability_flag": bool,
        "classification_basis": list[str],
        "confidence_band": str,  # "high" / "medium" / "low"
    }
    """
    name = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()
    search_text = name + " " + ing_text
    nn = product.get("normalized_nutrition_per_100g") or {}

    # Score each category
    scores = {cat: 0.0 for cat in CATEGORIES}
    matched_signals = {cat: [] for cat in CATEGORIES}

    # Full-text signals (name + ingredient text)
    for cat, signals in CATEGORY_SIGNALS.items():
        for keyword, weight in signals:
            if keyword in search_text:
                scores[cat] += weight
                matched_signals[cat].append(keyword)

    # Name-only signals — beverage and dairy_protein to prevent ingredient-text leakage
    for cat, signals in CATEGORY_SIGNALS_NAME_ONLY.items():
        for keyword, weight in signals:
            if keyword in name:
                # For dairy_protein: suppress if the keyword appears after a flavor descriptor
                # ("בטעם יוגורט" = yogurt-flavored snack, not a dairy product)
                if cat == "dairy_protein":
                    idx = name.find(keyword)
                    prefix = name[max(0, idx - 10):idx].strip()
                    if any(sup in prefix for sup in DAIRY_FLAVOR_SUPPRESSORS):
                        scores[cat] += weight * 0.15   # near-zero contribution
                        matched_signals[cat].append(f"{keyword}(flavor_descriptor)")
                        continue
                scores[cat] += weight
                matched_signals[cat].append(keyword)

    # Apply nutritional hints
    hints = _nutritional_hints(nn)
    for cat, boost in hints.items():
        scores[cat] += boost

    # Beverage liquid gate: validates that beverage classification has a real liquid
    # context signal.  Runs unconditionally so fallback signals can also ESTABLISH
    # the beverage category for products whose short name omits volume/liquid cues.
    #
    # Primary check: explicit liquid keyword in the product name.
    has_liquid_signal = any(kw in name for kw in BEVERAGE_LIQUID_GATE_KEYWORDS)
    liquid_signal_boost = 0.0
    liquid_signal_basis: list[str] = []

    if not has_liquid_signal:
        # Fallback A: nutrition_basis_claimed contains a liquid volume unit.
        # "ל1 ליטר" in the BSIP1 field is unambiguous: the package is a 1-litre liquid.
        basis_claimed = (product.get("nutrition_basis_claimed") or "").lower()
        if any(term in basis_claimed for term in LIQUID_BASIS_TERMS):
            has_liquid_signal = True
            liquid_signal_boost = 0.85
            liquid_signal_basis.append("nutrition_basis_claimed_liquid_volume")

    if not has_liquid_signal:
        # Fallback B: product brand is a known plant-milk brand (exclusively liquid).
        brand_field = (product.get("brand") or "").lower()
        name_first = name.split()[0] if name else ""
        if brand_field in KNOWN_PLANT_MILK_BRANDS or name_first in KNOWN_PLANT_MILK_BRANDS:
            has_liquid_signal = True
            liquid_signal_boost = 0.75
            liquid_signal_basis.append("known_plant_milk_brand")

    if not has_liquid_signal:
        # Fallback C: plant-milk base ingredient term in name, no solid-food exclusion.
        has_plant_base = any(term in name for term in PLANT_MILK_BASE_NAME_TERMS)
        has_solid_exclusion = any(ex in name for ex in PLANT_MILK_SOLID_EXCLUSIONS)
        if has_plant_base and not has_solid_exclusion:
            has_liquid_signal = True
            liquid_signal_boost = 0.60
            liquid_signal_basis.append("plant_milk_name_heuristic")

    if has_liquid_signal:
        scores["beverage"] += liquid_signal_boost
        matched_signals["beverage"].extend(liquid_signal_basis)
    else:
        scores["beverage"] = 0.0
        matched_signals["beverage"] = []

    # Rank categories
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_cat, top_score = ranked[0]
    second_cat, second_score = ranked[1] if len(ranked) > 1 else ("default", 0.0)

    # Convert raw score to confidence
    total_signal = sum(s for _, s in ranked)
    if total_signal < 0.1:
        confidence = 0.35   # no signals: low confidence
        top_cat = "default"
    else:
        # Normalize: confidence proportional to top score vs field
        relative = top_score / max(total_signal, 0.1)
        confidence = min(0.95, max(0.30, relative + 0.15))

    # If top score is very low in absolute terms, cap confidence
    if top_score < 0.5:
        confidence = min(confidence, 0.55)
    if top_score < 0.3:
        confidence = min(confidence, 0.40)

    # Secondary confidence
    if total_signal > 0:
        second_conf = min(0.80, max(0.10, second_score / max(total_signal, 0.1)))
    else:
        second_conf = 0.20

    # Instability flag: secondary candidate within 10 score points of primary
    delta = top_score - second_score
    instability_flag = (delta < 0.3 and confidence < 0.80)

    # Confidence band (SRC-07)
    if confidence >= 0.80:
        band = "high"
    elif confidence >= 0.50:
        band = "medium"
    else:
        band = "low"

    basis = matched_signals[top_cat][:6] if matched_signals[top_cat] else ["nutritional_profile_heuristic"]

    return {
        "category":                top_cat,
        "category_confidence":     round(confidence, 2),
        "secondary_category":      second_cat if second_cat != top_cat else "default",
        "secondary_confidence":    round(second_conf, 2),
        "category_instability_flag": instability_flag,
        "classification_basis":    basis,
        "confidence_band":         band,
        "raw_category_scores":     {k: round(v, 3) for k, v in ranked},
    }
