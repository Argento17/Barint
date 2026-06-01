"""
BSIP2 Configuration v0.3.1
All thresholds, coefficients, and parameters live here.
"""

ALGORITHM_VERSION = "0.3.1"

GRADE_BANDS = [(85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "E")]

# ---------------------------------------------------------------------------
# DIMENSION WEIGHTS (must sum to 1.0)
# ---------------------------------------------------------------------------
DIMENSION_WEIGHTS = {
    "nutrient_density":         0.16,
    "processing_quality":       0.18,
    "calorie_density_quality":  0.12,
    "glycemic_quality":         0.11,
    "protein_quality":          0.09,
    "fat_quality":              0.06,
    "additive_quality":         0.07,
    "satiety_support":          0.06,
    "regulatory_quality":       0.04,
    "whole_food_integrity":     0.01,
    "hyper_palatability":       0.10,
}
assert abs(sum(DIMENSION_WEIGHTS.values()) - 1.0) < 1e-9, "Weights must sum to 1.0"

# ---------------------------------------------------------------------------
# DIMENSION PARAMETERS
# ---------------------------------------------------------------------------
DIMENSION_PARAMS = {
    "nutrient_density": {
        "base": 50,
        "protein_coef": 1.2,
        "protein_cap": 20,
        "fiber_coef": 2.0,
        "fiber_cap": 18,
        "sugar_threshold": 5,
        "sugar_penalty": 0.9,
        "sodium_threshold": 400,
        "sodium_divisor": 80,
    },
    "glycemic_quality": {
        "base": 80,
        "sugar_threshold": 5,
        "sugar_penalty": 1.4,
        "carb_threshold": 45,
        "carb_penalty": 0.35,
        "fiber_coef": 1.1,
        "fiber_cap": 10,
    },
    "processing_quality": {
        "base": 100,
        "nova_4_penalty": 24,
        "nova_3_penalty": 12,
        "ingredient_count_threshold": 8,
        "ingredient_count_penalty_per_extra": 1.2,
        "engineered_marker_penalty": 6,
        "matrix_marker_bonus": 2.5,
        "matrix_relief_cap": 8,
    },
    "protein_quality": {
        "base": 45,
        "protein_coef": 2.0,
        "protein_cap": 35,
        "isolate_penalty": 5,
    },
    "fat_quality": {
        "base": 70,
        "satfat_threshold": 2,
        "satfat_penalty": 4,
        "seed_oil_penalty": 8,
        "nut_seed_satfat_relief_multiplier": 0.75,
    },
    "additive_quality": {
        "base": 90,
        "per_marker_penalty": 12,
        "sweetener_penalty": 8,
    },
    "satiety_support": {
        "base": 45,
        "protein_coef": 1.4,
        "protein_cap": 25,
        "fiber_coef": 2.2,
        "fiber_cap": 25,
        "sugar_threshold": 15,
        "sugar_penalty": 0.5,
    },
    "regulatory_quality": {
        "base": 100,
        "per_red_label_penalty": 18,
    },
    "whole_food_integrity": {
        "base": 52,
        "matrix_marker_bonus": 7,
        "matrix_marker_cap": 24,
        "engineered_marker_penalty": 6,
        "engineered_marker_cap": 30,
        "nova_4_penalty": 14,
        "nova_3_penalty": 7,
        "ingredient_count_threshold": 6,
        "per_extra_ingredient_penalty": 1.2,
        "ingredients_missing_cap": 45,
    },
}

# ---------------------------------------------------------------------------
# PENALTY FAMILIES
# ---------------------------------------------------------------------------
PENALTY_FAMILIES = {
    "sugar":                  {"max_total_penalty": 10, "cap_floor": 45},
    "sodium":                 {"max_total_penalty": 8,  "cap_floor": 50},
    "fat_quality":            {"max_total_penalty": 8,  "cap_floor": 55},
    "processing":             {"max_total_penalty": 12, "cap_floor": 55},
    "additives":              {"max_total_penalty": 10, "cap_floor": 55},
    "regulatory":             {"max_total_penalty": 12, "cap_floor": 45},
    "calorie_density":        {"max_total_penalty": 8,  "cap_floor": 55},
    "hyper_palatability":     {"max_total_penalty": 12, "cap_floor": 50},
    "ingredient_complexity":  {"max_total_penalty": 5,  "cap_floor": 65},
    "general":                {"max_total_penalty": 6,  "cap_floor": 50},
}

# ---------------------------------------------------------------------------
# CALORIE DENSITY TIERS (kcal/100g → score)
# ---------------------------------------------------------------------------
CALORIE_DENSITY_TIERS = {
    "default": [
        (150, 90), (250, 80), (350, 65), (450, 50), (550, 35), (float("inf"), 20),
    ],
    "whole_food_fat": [
        (350, 90), (500, 85), (650, 75), (750, 65), (900, 55), (float("inf"), 45),
    ],
    "snack_bar_granola": [
        (150, 90), (250, 75), (350, 55), (430, 40), (500, 25), (float("inf"), 15),
    ],
    "dessert": [
        (150, 85), (250, 70), (350, 55), (430, 40), (520, 25), (float("inf"), 15),
    ],
    "beverage": [
        (10, 95), (25, 85), (45, 70), (70, 50), (100, 30), (float("inf"), 15),
    ],
    "dairy_protein": [
        (80, 90), (130, 80), (180, 70), (250, 55), (350, 40), (float("inf"), 25),
    ],
    "cereal": [
        (300, 85), (380, 70), (430, 55), (480, 40), (550, 25), (float("inf"), 15),
    ],
    "sauce_spread": [
        (150, 90), (300, 75), (450, 60), (600, 50), (750, 40), (float("inf"), 25),
    ],
}

# ---------------------------------------------------------------------------
# CATEGORY INFERENCE KEYWORDS
# ---------------------------------------------------------------------------
CATEGORY_KEYWORDS = {
    "whole_food_fat": {
        "name_he": [
            "שמן זית", "טחינה", "אבוקדו", "אגוזים", "שקדים", "בוטנים",
            "קשיו", "פיסטוק", "אגוזי מלך", "זרעים", "חמאת בוטנים", "חמאת שקדים"
        ],
        "name_en": [
            "olive oil", "tahini", "avocado", "nuts", "almonds", "peanuts",
            "cashew", "pistachio", "walnut", "seeds", "peanut butter", "almond butter"
        ],
        "ingredient_dominance": ["שמן זית", "טחינה", "olive oil", "tahini", "almonds", "שקדים"],
    },
    "snack_bar_granola": {
        "name_he": ["חטיף", "חטיפי", "גרנולה", "חטיף חלבון", "חטיף דגנים", "חטיף אנרגיה"],
        "name_en": ["bar", "granola", "protein bar", "energy bar", "cereal bar", "snack bar"],
    },
    "dessert": {
        "name_he": ["שוקולד", "גלידה", "עוגה", "עוגיות", "ופל", "ממתק", "סוכריות", "פודינג"],
        "name_en": ["chocolate", "ice cream", "cake", "cookie", "wafer", "candy", "pudding", "dessert"],
    },
    "beverage": {
        "name_he": ["משקה", "מיץ", "תה", "קפה", "סודה", "קולה"],
        "name_en": ["drink", "beverage", "juice", "tea", "coffee", "soda", "cola", "water"],
    },
    "dairy_protein": {
        "name_he": ["יוגורט", "קוטג'", "גבינה", "סקיר", "חלב"],
        "name_en": ["yogurt", "cottage", "cheese", "skyr", "milk", "kefir"],
    },
    "cereal": {
        "name_he": ["דגנים", "קורנפלקס", "שיבולת שועל", "מוזלי"],
        "name_en": ["cereal", "cornflakes", "oats", "muesli", "oatmeal"],
    },
    "sauce_spread": {
        "name_he": ["רוטב", "ממרח", "מיונז", "קטשופ", "חרדל"],
        "name_en": ["sauce", "spread", "mayo", "ketchup", "mustard", "dressing"],
    },
}

# ---------------------------------------------------------------------------
# HYPER-PALATABILITY THRESHOLDS
# ---------------------------------------------------------------------------
HYPER_PALATABILITY_RULES = {
    "fat_sodium": {
        "fat_kcal_pct_min": 25,
        "sodium_g_per_100g": 0.30,
        "weight": 1.0,
        "label": "FAT_SODIUM_COMBO",
        "rationale": "Engineered fat-and-salt combination (chips/savoury snack pattern)",
    },
    "fat_sugar": {
        "fat_kcal_pct_min": 20,
        "sugar_kcal_pct_min": 20,
        "weight": 1.0,
        "label": "FAT_SUGAR_COMBO",
        "rationale": "Engineered fat-and-sugar combination (dessert/pastry pattern)",
    },
    "refined_carb_fat": {
        "carb_kcal_pct_min": 40,
        "fat_kcal_pct_min": 15,
        "fiber_to_carb_max": 0.10,
        "weight": 0.9,
        "label": "REFINED_CARB_FAT_COMBO",
        "rationale": "Refined-carb + fat combination (cookie/cracker/pastry pattern)",
    },
    "crunch_sweet": {
        "carb_g_per_100g_min": 50,
        "sugar_g_per_100g_min": 20,
        "fiber_g_per_100g_max": 5,
        "fat_g_per_100g_max": 10,
        "weight": 0.8,
        "label": "CRUNCH_SWEET_COMBO",
        "rationale": "Sweet crispy combination (engineered cereal/candy pattern)",
    },
}

HP_DIMENSION_SCORING = {
    "base": 100,
    "per_combo_penalty": 28,
    "soft_match_factor": 0.5,
    "near_miss_band": 0.20,
}

HP_GUARDRAIL_RULES = {
    "single_combo_penalty": 5,
    "two_combos_cap": 60,
    "three_plus_combos_cap": 50,
}

# ---------------------------------------------------------------------------
# CONCERN GRAPH
# ---------------------------------------------------------------------------
CONCERNS = {
    "SUGAR_LOAD": {
        "rules": [
            "HIGH_SUGAR_25G_PLUS",
            "ISRAELI_RED_LABEL_1",
            "ISRAELI_RED_LABELS_2_PLUS",
            "MULTIPLE_ADDED_SUGAR_MARKERS",
            "HIGH_CAL_HIGH_SUGAR_SOFT",
            "HIGH_CAL_HIGH_SUGAR_MODERATE",
            "HIGH_CAL_HIGH_SUGAR_SEVERE",
            "SNACK_BAR_HIGH_CAL_SUGAR",
            "SNACK_BAR_RED_SUGAR_LABEL",
            "HP_FAT_SUGAR_COMBO",
            "HP_CRUNCH_SWEET_COMBO",
        ],
        "supporting_evidence_factor": 0.4,
    },
    "SODIUM_LOAD": {
        "rules": ["HIGH_SODIUM_700MG_PLUS", "HP_FAT_SODIUM_COMBO"],
        "supporting_evidence_factor": 0.4,
    },
    "PROCESSING_LOAD": {
        "rules": [
            "NOVA_PROXY_4_ULTRA_PROCESSED",
            "NOVA_PROXY_3_PROCESSED",
            "ADDITIVE_MARKERS_5_PLUS",
            "ADDITIVE_MARKERS_3_PLUS",
            "LONG_INGREDIENT_LIST",
        ],
        "supporting_evidence_factor": 0.5,
    },
    "CALORIE_LOAD": {
        "rules": [
            "SNACK_BAR_HIGH_CAL",
            "HIGH_CAL_LOW_SATIETY_SOFT",
            "HIGH_CAL_LOW_SATIETY_SEVERE",
        ],
        "supporting_evidence_factor": 0.5,
    },
    "FAT_QUALITY": {
        "rules": ["SEED_OIL_PRESENT"],
        "supporting_evidence_factor": 0.5,
    },
}

CONTEXT_AWARE_CONCERN_MAPPING = {
    "ISRAELI_RED_LABEL_1": {
        "concern_when": {
            "red_label_sugar": "SUGAR_LOAD",
            "red_label_sodium": "SODIUM_LOAD",
            "red_label_saturated_fat": "FAT_QUALITY",
        },
    },
}

# ---------------------------------------------------------------------------
# INGREDIENT MARKERS
# ---------------------------------------------------------------------------
INGREDIENT_MARKERS = {
    "added_sugar": [
        "סוכר", "גלוקוז", "פרוקטוז", "סירופ תירס", "סירופ גלוקוז",
        "דבש", "מולסה", "סירופ מייפל",
        "sugar", "glucose", "fructose", "corn syrup",
    ],
    "sweetener": [
        "ממתיק", "ממתיקים", "סוכרלוז", "אספרטיים", "אססולפאם",
        "מלטיטול", "סטיביה", "אריתריטול",
        "sweetener", "sucralose", "aspartame", "maltitol",
    ],
    "emulsifier": [
        "מתחלב", "לציטין", "E322", "E471",
        "emulsifier", "lecithin",
    ],
    "stabilizer": [
        "מייצב", "מייצבים", "גואר", "קסנטן", "קרגינן",
        "stabilizer", "xanthan", "carrageenan",
    ],
    "protein_isolate": [
        "חלבון מי גבינה", "חלבון חלב", "חלבון סויה", "איזולט",
        "whey protein", "milk protein", "soy protein", "protein isolate",
    ],
    "seed_oil": [
        "שמן חמניות", "שמן קנולה", "שמן סויה", "שמן תירס",
        "sunflower oil", "canola oil", "soybean oil", "corn oil",
    ],
    "whole_food_positive": [
        "שיבולת שועל", "שקדים", "אגוז", "בוטנים", "זרעים",
        "oats", "almonds", "nuts", "peanuts", "seeds",
    ],
    "nut_or_seed": [
        "אגוז", "אגוזים", "שקד", "שקדים", "בוטן", "בוטנים",
        "קשיו", "פקאן", "פיסטוק", "לוז", "אגוז לוז", "אגוזי מלך",
        "זרע", "זרעים", "גרעין", "גרעינים", "שומשום", "טחינה",
        "צ'יה", "פשתן", "חמניות", "דלעת",
        "nut", "nuts", "almond", "almonds", "peanut", "peanuts",
        "cashew", "pecan", "pistachio", "hazelnut", "walnut", "walnuts",
        "seed", "seeds", "sesame", "tahini", "chia", "flax", "flaxseed",
        "sunflower seed", "sunflower seeds", "pumpkin seed", "pumpkin seeds",
    ],
    "oat": [
        "שיבולת שועל", "קוואקר",
        "oat", "oats", "oatmeal", "rolled oats",
    ],
    "whole_grain": [
        "דגן מלא", "דגנים מלאים", "חיטה מלאה", "קמח חיטה מלאה",
        "קמח מלא", "שיבולת שועל מלאה", "שיפון מלא", "כוסמין מלא",
        "whole grain", "whole grains", "whole wheat", "whole wheat flour",
        "wholemeal", "whole oat", "whole oats", "whole rye", "whole spelt",
    ],
    "date_or_fruit_paste": [
        "תמר", "תמרים", "מחית תמרים", "רכז תמרים",
        "מחית פרי", "רכז פרי", "מחית תפוחים", "רכז תפוחים",
        "date", "dates", "date paste", "fruit paste", "fruit puree",
        "fruit purée", "fruit concentrate", "apple paste", "apple puree",
    ],
    "glucose_syrup": [
        "סירופ גלוקוז",
        "glucose syrup",
    ],
    "maltodextrin": [
        "מלטודקסטרין",
        "maltodextrin",
    ],
    "syrup_system": [
        "סירופ", "סירופ תירס", "סירופ אורז", "סירופ גלוקוז",
        "סירופ סוכר", "סירופ מלט",
        "syrup", "corn syrup", "rice syrup", "glucose syrup",
        "sugar syrup", "malt syrup",
    ],
    "chocolate_coating": [
        "ציפוי שוקולד", "מצופה שוקולד", "ציפוי בטעם שוקולד",
        "chocolate coating", "chocolate coated", "coated in chocolate",
    ],
    "coating": [
        "ציפוי", "מצופה",
        "coating", "coated",
    ],
    "extruded_or_puffed_grain": [
        "פצפוצי", "מנופח", "מנופחים", "אקסטרודד", "אקסטרוזיה",
        "puffed", "extruded", "popped",
    ],
    "crispy_cereal": [
        "קריספי", "פריך", "פריכים",
        "crispy", "crisp", "crunchy",
    ],
    "flavouring": [
        "חומרי טעם", "חומר טעם", "טעמים", "תמצית טעם",
        "flavour", "flavor", "flavouring", "flavoring", "natural flavor", "natural flavour",
    ],
    "hydrogenated_fat": [
        "שומן מוקשה", "שמן מוקשה", "מוקשה", "מוקשה חלקית",
        "hydrogenated", "hydrogenated fat", "hydrogenated oil",
        "partially hydrogenated", "partially hydrogenated oil",
    ],
}

HEBREW_NEGATION_PREFIXES = ["ללא", "בלי", "ללא תוספת", "ללא תוספת של", "נטול"]
ENGLISH_NEGATION_PREFIXES = ["no ", "without ", "free of ", "zero "]

# ---------------------------------------------------------------------------
# GUARDRAIL CONSTANTS
# ---------------------------------------------------------------------------
VETO_SCORE_FAIL = 20
CONFIDENCE_LOW_THRESHOLD = 60
CONFIDENCE_INSUFFICIENT_THRESHOLD = 40