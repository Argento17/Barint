"""
BSIP2 Prototype v0 — Scoring Constants
Source: bsip2_concept_v1 specification + score_resolution_contract.md (SRC-v1)
These are preliminary prototype values. Calibration is a separate phase.
"""

# ---------------------------------------------------------------------------
# Dimension weights (must sum to 1.0)
# ---------------------------------------------------------------------------
DIMENSION_WEIGHTS = {
    "processing_quality":   0.15,
    "nutrient_density":     0.15,
    "calorie_density":      0.15,
    "glycemic_quality":     0.12,
    "protein_quality":      0.10,
    "additive_quality":     0.10,
    "satiety_support":      0.06,
    "fat_quality":          0.08,
    "regulatory_quality":   0.05,
    "whole_food_integrity": 0.04,
}

# ---------------------------------------------------------------------------
# Calorie density lookup tables: list of (kcal_ceiling, score) pairs
# Lookup: first tier where kcal <= ceiling wins
# ---------------------------------------------------------------------------
CALORIE_DENSITY_TABLES = {
    "whole_food_fat":    [(350,90),(500,85),(650,75),(750,65),(900,55),(1e9,45)],
    "snack_bar_granola": [(150,90),(250,75),(350,55),(430,40),(500,25),(1e9,15)],
    "dessert":           [(150,85),(250,70),(350,55),(430,40),(520,25),(1e9,15)],
    "beverage":          [(10,95),(25,85),(45,70),(70,50),(100,30),(1e9,15)],
    "dairy_protein":     [(80,90),(130,80),(180,70),(250,55),(350,40),(1e9,25)],
    "cereal":            [(300,85),(380,70),(430,55),(480,40),(550,25),(1e9,15)],
    "sauce_spread":      [(150,90),(300,75),(450,60),(600,50),(750,40),(1e9,25)],
    # Bakery archetypes — calibrated to typical kcal ranges for the format
    # Bread: 200-330 kcal/100g is normal (whole-grain loaf ~240, white loaf ~270, enriched ~320)
    "bread":             [(200,90),(280,80),(330,70),(400,55),(480,35),(1e9,20)],
    # Cracker: 380-480 kcal/100g is normal (denser than bread, less water)
    "cracker":           [(250,90),(350,80),(420,70),(480,55),(550,35),(1e9,20)],
    # Crispbread: 300-380 kcal/100g (compressed grain, low moisture)
    "crispbread":        [(200,90),(300,85),(380,70),(450,50),(520,30),(1e9,15)],
    "default":           [(150,90),(250,80),(350,65),(450,50),(550,35),(1e9,20)],
}

# ---------------------------------------------------------------------------
# NOVA proxy scoring (Processing Quality and Whole Food Integrity dimensions)
# ---------------------------------------------------------------------------
NOVA_PROCESSING_SCORES = {1: 95, 2: 85, 3: 65, 4: 35}
NOVA_WFI_SCORES        = {1: 100, 2: 85, 3: 60, 4: 30}
NOVA_HP_WEIGHTS        = {1: 0.0, 2: 0.0, 3: 0.5, 4: 1.0}  # SRC-06

# ---------------------------------------------------------------------------
# Israeli red label thresholds (Ministry of Health, solids)
# ---------------------------------------------------------------------------
RED_LABEL_THRESHOLDS = {
    "sugar":    17.5,   # g/100g
    "sat_fat":  5.0,    # g/100g
    "sodium":   600.0,  # mg/100g
}

# ---------------------------------------------------------------------------
# Guardrail caps — SUGAR_LOAD family
# ---------------------------------------------------------------------------
SUGAR_CAPS = [
    # (rule_id, condition_fn, cap_value)
    # Conditions receive a signals dict; defined in score_engine
    ("HIGH_CAL_HIGH_SUGAR_SEVERE",   "kcal>=500 AND sugar>=25",  50),
    ("HIGH_CAL_HIGH_SUGAR_MODERATE", "kcal>=470 AND sugar>=20",  60),
    ("HIGH_SUGAR_25G_PLUS",          "sugar>=25",                60),
    ("SNACK_BAR_HIGH_CAL_SUGAR",     "snack_bar AND kcal>=470 AND sugar>=15", 60),
    ("SNACK_BAR_RED_SUGAR_LABEL",    "snack_bar AND red_label_sugar", 55),
    ("ISRAELI_RED_LABEL_1_SUGAR",    "red_label_sugar",          55),
    ("ISRAELI_RED_LABELS_2_PLUS",    "red_labels>=2",            45),
]

SUGAR_PENALTIES = [
    ("MULTIPLE_ADDED_SUGAR_MARKERS", "added_sugar_sources>=2",   5),
    ("HIGH_CAL_HIGH_SUGAR_SOFT",     "kcal>=430 AND sugar>=15",  5),
    # HP penalties handled separately via HP engine
]

SUGAR_FAMILY_BUDGET = 10

# ---------------------------------------------------------------------------
# Guardrail caps — CALORIE_LOAD family
# ---------------------------------------------------------------------------
CALORIE_CAPS = [
    ("HIGH_CAL_LOW_SATIETY_SEVERE",  "kcal>=500 AND protein<6 AND fiber<3",  55),
    ("SNACK_BAR_HIGH_CAL",           "snack_bar AND kcal>=430",              70),
]

CALORIE_PENALTIES = [
    ("HIGH_CAL_LOW_SATIETY_SOFT",    "kcal>=450 AND protein<8 AND fiber<5",  6),
]

CALORIE_FAMILY_BUDGET = 8

# ---------------------------------------------------------------------------
# Guardrail caps — PROCESSING_LOAD family
# ---------------------------------------------------------------------------
PROCESSING_CAPS = [
    ("NOVA_PROXY_4_ULTRA_PROCESSED", "nova==4",          68),
    ("ADDITIVE_MARKERS_5_PLUS",      "additives>=5",     60),
    ("ADDITIVE_MARKERS_3_PLUS",      "additives>=3",     72),
    ("NOVA_PROXY_3_PROCESSED",       "nova==3",          82),
]

PROCESSING_PENALTIES = [
    ("LONG_INGREDIENT_LIST",         "ingredients>12",   4),
]

PROCESSING_FAMILY_BUDGET = 12

# ---------------------------------------------------------------------------
# Guardrail caps — SODIUM_LOAD family
# ---------------------------------------------------------------------------
SODIUM_CAPS = [
    ("HIGH_SODIUM_700MG_PLUS",       "sodium>=700",      60),
]

SODIUM_FAMILY_BUDGET = 8

# ---------------------------------------------------------------------------
# Guardrail caps — FAT_QUALITY family
# ---------------------------------------------------------------------------
FAT_QUALITY_CAPS = [
    ("ISRAELI_RED_LABEL_1_SAT_FAT",  "red_label_sat_fat", 55),
]

FAT_QUALITY_PENALTIES = [
    ("SEED_OIL_PRESENT",             "seed_oil",          3),
]

FAT_QUALITY_FAMILY_BUDGET = 8

# ---------------------------------------------------------------------------
# SWEETENER cap (independent — outside CONCERNS graph, SRC-03 note)
# ---------------------------------------------------------------------------
SWEETENER_CAP = 70

# ---------------------------------------------------------------------------
# Trans fat veto threshold
# > 1.0g/100g: veto (score = 0)
# 0.5-1.0g: high_trans_fat_concern flag (no veto)
# 0.2-0.5g: trans_fat_present flag
# ---------------------------------------------------------------------------
TRANS_FAT_VETO_THRESHOLD = 1.0
TRANS_FAT_HIGH_THRESHOLD = 0.5
TRANS_FAT_FLAG_THRESHOLD = 0.2

# ---------------------------------------------------------------------------
# HP pattern thresholds
# ---------------------------------------------------------------------------
HP_FAT_SUGAR_FAT_PCT   = 30.0  # % kcal from fat
HP_FAT_SUGAR_SUGAR_G   = 20.0  # g sugar
HP_FAT_SODIUM_FAT_PCT  = 25.0  # % kcal from fat
HP_FAT_SODIUM_SODIUM_G = 300.0 # mg sodium
HP_CRUNCH_SWEET_SUGAR  = 20.0  # g sugar
HP_CRUNCH_SWEET_FIBER  = 3.0   # g fiber (must be ≤)

# HP penalties (before NOVA weight applied)
HP_FAT_SUGAR_PENALTY   = 8
HP_FAT_SODIUM_PENALTY  = 6
HP_CRUNCH_SWEET_PENALTY = 5

HP_FAMILY_BUDGET = 12

# ---------------------------------------------------------------------------
# Floor values (SRC-01)
# ---------------------------------------------------------------------------
NOVA1_SINGLE_FLOOR      = 85   # NOVA 1 single-ingredient whole food
WHOLE_FOOD_FAT_FLOOR    = 70   # NOVA 1-2 whole food fat products
PHYSIO_MODERATION_MIN   = 60   # When Class B cap fires on NOVA 1 single-ingredient
PHYSIO_2PLUS_LABELS_MIN = 50   # When 2+ red labels fire on NOVA 1

# ---------------------------------------------------------------------------
# Confidence ceiling thresholds
# ---------------------------------------------------------------------------
CONFIDENCE_INSUFFICIENT_CEILING = 50   # confidence < 40
CONFIDENCE_LOW_CEILING          = 75   # confidence 40-59

# ---------------------------------------------------------------------------
# Structural emptiness gate thresholds (SRC-04)
# ---------------------------------------------------------------------------
SE_KCAL_THRESHOLD    = 80.0   # kcal/100g
SE_BEVERAGE_KCAL     = 10.0   # kcal/100g for beverages — plain plant milks (15 kcal) are exempt
SE_PROTEIN_THRESHOLD = 3.0    # g/100g
SE_FIBER_THRESHOLD   = 1.5    # g/100g
SE_FAT_THRESHOLD     = 2.0    # g/100g

# ---------------------------------------------------------------------------
# Penalty-on-low-base relative budget (SRC-05)
# ---------------------------------------------------------------------------
RELATIVE_PENALTY_FACTOR_HIGH = 0.50   # pre-penalty score >= 30
RELATIVE_PENALTY_FACTOR_LOW  = 0.45   # pre-penalty score < 30
ABSOLUTE_SCORE_FLOOR         = 10     # No non-veto product scores below this
GRADE_E_FLOOR_STANDARD       = 15     # Without compound veto conditions

# ---------------------------------------------------------------------------
# Category confidence thresholds (SRC-07)
# ---------------------------------------------------------------------------
CAT_CONF_HIGH   = 0.80
CAT_CONF_MEDIUM = 0.50
CAT_MEDIUM_THRESHOLD_RELAX = 0.10  # 10% threshold relaxation

# ---------------------------------------------------------------------------
# Grade thresholds
# ---------------------------------------------------------------------------
GRADE_THRESHOLDS = [
    (90, "S"),
    (80, "A"),
    (65, "B"),
    (50, "C"),
    (35, "D"),
    (0,  "E"),
]

def score_to_grade(score):
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "E"

def lookup_calorie_density(kcal, category):
    table = CALORIE_DENSITY_TABLES.get(category, CALORIE_DENSITY_TABLES["default"])
    for ceiling, score in table:
        if kcal <= ceiling:
            return score
    return table[-1][1]
