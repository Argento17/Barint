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
    # R-05: yogurt archetype — plain 50–120 kcal, flavored/full-fat up to ~200
    "yogurt":            [(60,95),(100,88),(140,78),(180,65),(250,50),(1e9,30)],
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
    ("NOVA_PROXY_3_PROCESSED",       "nova==3",          87),  # R-01
]

# R-02: direct fermentation bonus (pre-cap, NOVA1–3 only)
FERMENTATION_DIRECT_BONUS = 8

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
# TASK-189 / EV-049 — BARI_SODIUM_CEREAL graduated sodium treatment.
# DEFAULT OFF. Scoped to snack_bar_granola + cereal only.
# Penalty bands (mg/100g): <150→0, 150–299→−2, 300–449→−5, 450–599→−8.
# Category cap: >=500mg → cap 75 (HIGH_SODIUM_CEREAL_500).
# Boundary fix: MoH red-label test changed from >600 to >=600 for this scope.
# All values are EV-049 bound values. D7 co-signed (Nutrition + Product, 2026-06-05).
# ---------------------------------------------------------------------------
SODIUM_CEREAL_CATEGORIES = {"snack_bar_granola", "cereal"}

# Graduated SODIUM_LOAD penalties (mg/100g bands → penalty points)
SODIUM_CEREAL_BANDS = [
    (600, None, 0),    # >=600: HIGH_SODIUM_700MG_PLUS cap takes over; penalty not stacked
    (450, 599, 8),     # 450–599 mg
    (300, 449, 5),     # 300–449 mg
    (150, 299, 2),     # 150–299 mg
    (0,   149, 0),     # <150 mg — clean band; no penalty
]

# Category cap for high-sodium cereals: fired at >=500mg
SODIUM_CEREAL_CAP_THRESHOLD = 500   # mg/100g
SODIUM_CEREAL_CAP_VALUE     = 75    # score cap

# MoH red-label boundary correction: >=600 (not >600) for cereal/granola scope
SODIUM_CEREAL_RED_LABEL_BOUNDARY = 600  # mg/100g (inclusive)

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

# EV-047 — kcal plausibility upper bound (archetype-conditional).
# Standard solid food range: 20–700 kcal/100g. whole_food_fat / cooking_oil archetypes
# contain structurally valid products at 725–745 kcal (butter, Atwater: 82g fat × 9 = 738)
# and up to ~900 kcal (ghee, edge case). 800 is the right ceiling for high-fat archetypes
# without passing genuine errors (1800 kcal robustness-corpus G3 still fires).
# At signal extraction time the router has not yet run, so a single raised global value
# of 800 is used — safe because no non-fat food reaches 800+ kcal/100g legitimately.
# Raised for whole_food_fat/cooking_oil archetypes (butter=725-745, ghee≈900 — EV-047)
KCAL_PLAUSIBLE_UPPER          = 800   # raised ceiling — see note above (EV-047)
KCAL_PLAUSIBLE_LOWER          = 20    # unchanged minimum
KCAL_PLAUSIBLE_UPPER_STANDARD = 700   # original standard-archetype bound (retained as reference)

# EV-048 — sat-fat cap endemic gate for intact dairy fat.
# ISRAELI_RED_LABEL_1_SAT_FAT (cap=55) fires on 100% of butter products because
# butter's sat-fat content (48–70g/100g) structurally guarantees exceeding the 5g/100g
# red-label threshold. The cap was designed to penalise reformulable excess sat-fat;
# butter cannot be reformulated. Gate suppresses the cap when:
#   category == "whole_food_fat" AND fat_saturated_g / fat_g >= 0.50
# A sat-fat fraction ≥ 0.50 identifies dairy fat composition (plain butter = 0.58–0.70).
# Palm-oil-laden spreadable fats or seed-oil-diluted products have a lower fraction
# and still hit the cap. The red label annotation in regulatory_quality is NOT gated.
# Gated for endemic whole-food sat-fat (dairy butter, pure cream products) — EV-048
SAT_FAT_CAP_ENDEMIC_WFF_FRACTION = 0.50   # sat-fat fraction threshold; ≥ this → cap gated (EV-048)

# ---------------------------------------------------------------------------
# SWEETENER caps and penalties by tier (independent — outside CONCERNS graph, SRC-03 note)
# Tier A: fermentation-derived / natural (stevia, monkfruit, thaumatin) — lightest penalty
# Tier B: sugar alcohols (erythritol, xylitol, sorbitol, maltitol, isomalt)
# Tier C: synthetic (aspartame, sucralose, acesulfame-K, saccharin) — full penalty
# Worst tier present in product applies.
# ---------------------------------------------------------------------------
SWEETENER_CAP_A     = 75
SWEETENER_CAP_B     = 73
SWEETENER_CAP_C     = 70
SWEETENER_PENALTY_A = 8
SWEETENER_PENALTY_B = 10
SWEETENER_PENALTY_C = 15

# ---------------------------------------------------------------------------
# TASK-133 — Evidence-Watch 2026-06-01 revisions (F2 / F1 / F4)
# ALL magnitudes below are placeholders gated by DEC-004 (calibration_signoff).
# The STRUCTURE is owner-approved; the NUMBERS are set in a dedicated calibration
# run against real corpora. See research/TASK-133_implementation_roadmap.md.
# ---------------------------------------------------------------------------

# ── F2 / TASK-133B — Protein Quality matrix discount ────────────────────────
# Discounts the protein-QUALITY contribution ONLY (DEC-004 G2 = quality-only).
# Protein MASS still feeds satiety_support + nutrient_density untouched.
# Applies to bar-format products whose protein is reconstructed (isolate-style) —
# the documented isolate-bar gaming hole. Empirical basis: bar-matrix DIAAS
# measured at 47–81% of label — a conservative BAND, not a per-product number;
# collagen is lowest (incomplete AA profile, no tryptophan).
# COORDINATION (top risk in roadmap): this is the SOLE owner of the
# reconstructed-protein penalty in the LIVE score path. matrix_integrity.py's
# degradation pull is NOT wired into the composite score, so there is no
# double-count today; if it is ever composited in, it must NOT re-penalize
# reconstructed protein (PROCESSING_LOAD-family coordination note).
PROTEIN_QUALITY_MATRIX_DISCOUNT = {
    "reconstructed": 0.80,   # bar-format isolate: placeholder ~midpoint of 47–81% band — DEC-004
    "collagen":      0.55,   # incomplete AA profile, lowest matrix DIAAS — DEC-004
}
# Bar-format scoring categories the F2 reconstructed discount applies to.
# Restriction to bar formats PROTECTS in-context whey isolate (protein puddings /
# Greek yogurt are not bar-format → unchanged). Collagen discounts in any format.
PROTEIN_MATRIX_DISCOUNT_BAR_CATEGORIES = ("snack_bar_granola",)

# ── F1 / TASK-133C — emulsifier identity tiering + native-starch exclusion ──
# DIRECTIONS ARE ALREADY LIVE via the EV-003 sprint1 correction in
# signal_extractor (carrageenan/CMC → +2 count = stronger penalty; lecithin-only
# → −1 count = relief) and native/modified starch are already correctly
# differentiated by ADDITIVE_MARKER_PATTERNS (native עמילן is not an additive;
# modified עמילן מוקשה/משונה counts as thickener). TASK-133A's taxonomy now
# supplies EXACT identity (carrageenan vs CMC vs lecithin, E-numbers).
# These per-identity point deltas on the additive_quality dimension default to
# NEUTRAL (no-op) so they do NOT double-count sprint1; the calibration run
# (DEC-004) sets the precise weights AND reconciles/retires the coarse sprint1
# nudges. No new caps (Tension-5 rule budget). Note: food-grade carrageenan
# (E407) is the modelled form; degraded poligeenan is not a food additive.
ADDITIVE_IDENTITY_DELTAS = {
    "emulsifier_concern_each":  0,   # carrageenan / CMC / P80 — DEC-004 (sprint1 already +2 count)
    "emulsifier_concern_cap":   0,   # max stacked concern delta — DEC-004
    "lecithin_relief":          0,   # soy/sunflower lecithin toward neutral — DEC-004 (sprint1 already −1)
    "native_starch_relief":     0,   # native starch already excluded from burden — DEC-004
}

# ── F4 / TASK-133D — BHA named penalty (BHT explicitly excluded) ────────────
# GATE PASSED (WebSearch 2026-06-01): FDA launched a post-market reassessment of
# BHA (E320) on 2026-02-10 (RFI closed 2026-04-13; no final GRAS rule has landed
# as of 2026-06); NTP lists BHA as "reasonably anticipated to be a human
# carcinogen." BHT (E321) is NOT yet under reassessment (FDA reassesses it only
# after BHA) → explicitly differentiated, no penalty. Small NAMED penalty on the
# additive_quality dimension, distinct from the generic antioxidant-category
# count (which BHA, BHT and benign tocopherol currently share). No
# regulatory-status tracking subsystem — a static named penalty is correct while
# no rule has landed. Magnitude gated by DEC-004.
BHA_NAMED_PENALTY = 5   # points on additive_quality — placeholder, DEC-004

# ---------------------------------------------------------------------------
# TASK-144 Fix 2 — Fiber "absent ≠ zero" for naturally fiber-free dairy categories
# ---------------------------------------------------------------------------
# Evidence registry: EV-027 (TASK-144). nutrient_density blends protein (65%) and fiber
# (35%); a MISSING fiber value is read as 0 and drags the dimension down even though the
# food category is not expected to contain fiber (parallel to the whole-food-fat-floor
# principle: do not penalize a food for not being something it isn't). For a fiber-free
# dairy matrix this mis-models a structural non-applicability as a deficiency.
#
# TIGHT GATE (highest-risk item): this re-normalization to protein-only applies ONLY to
# the categories below — categories where ~0g fiber is the correct, expected value. Any
# category where missing fiber is a GENUINE nutritional deficiency (bread, cereal, bars,
# crackers, crispbread, sauces/spreads, whole-food fats, beverages) is DELIBERATELY
# EXCLUDED and keeps the flat 65/35 blend with fiber-as-0. Membership is allowlist-only:
# a category must be explicitly listed here to receive the treatment.
FIBER_NOT_APPLICABLE_CATEGORIES = ("dessert", "dairy_protein", "yogurt")

# ---------------------------------------------------------------------------
# TASK-169 — P0 Recalibration (R1–R7), gated by env flag BARI_RECAL_P0 (default OFF).
# Source of truth: 01_framework/bsip2_framework/recalibration_p0_design_v1.md.
# Flag OFF → every constant/path below is inert and the engine is byte-identical to
# 0.4.1 (rollback + regression guard). Precedent: BARI_TASK144_FIXES.
# Evidence registry: EV-029 (R1), EV-027 ext (R2), EV-030 (R3), EV-024/026 ext (R4),
# EV-031 (R5), EV-032 (R6). R7 is a signal-extraction fix (see signal_extractor).
# ---------------------------------------------------------------------------

# R1 — category-relative protein mass scale. breakpoints: list of (protein_g_ceiling,
# score); first ceiling where g <= ceiling wins, linear-interpolated between adjacent
# breakpoints (same interpolation as the legacy single curve). Looked up like
# CALORIE_DENSITY_TABLES. Feeds BOTH score_nutrient_density and score_protein_quality.
# "default" + "snack_bar_granola" deliberately reproduce the legacy supplement curve so
# untouched / frozen-bar categories stay byte-identical even with the flag ON.
PROTEIN_SCALE_TABLES = {
    "dairy_protein":     [(0,0),(3,20),(5,35),(7,50),(9,65),(11,85),(13,95),(99,100)],
    "sauce_spread":      [(0,0),(2,12),(4,28),(6,45),(8,62),(11,82),(14,95),(99,100)],
    # --- FROZEN categories (modelled; require P2 owner sign-off before shipping) ---
    "milk_dairy":        [(0,0),(2,30),(3,55),(4,70),(6,88),(8,95),(99,100)],
    "yogurt":            [(0,0),(2,20),(3.5,40),(5,58),(7,75),(9,90),(11,95),(99,100)],
    "bread":             [(0,0),(4,30),(6,45),(8,60),(10,72),(13,85),(99,95)],
    "snack_bar_granola": [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],
    "default":           [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],
}

# Categories that receive R2 fiber-not-applicable treatment when RECAL_P0 is ON.
# Identical membership to the TASK-144 allowlist — R2 only ACTIVATES the existing
# EV-027 path for the cheese run; it adds no new category. sauce_spread is NOT here
# (hummus fiber is a genuine virtue). Kept as a named constant for traceability.
RECAL_P0_FIBER_NOT_APPLICABLE = FIBER_NOT_APPLICABLE_CATEGORIES

# R4 — NOVA-3→2 demotion guard for plain dairy. Additive categories that mark genuine
# ultra-processing; if ANY is present the product stays NOVA 3 (no demotion). The benign
# set (salt/culture/rennet/calcium/vitamins) leaves no additive_category marker, so the
# discriminator is simply "none of these present".
NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS = (
    "thickener", "stabilizer", "emulsifier", "humectant", "flavor_enhancer", "color",
)

# R6 — veg_spread archetype re-weighting (sums to 1.0). Applied only to a sauce_spread
# product detected as a whole-vegetable spread (protein < 3g, veg base, no tahini
# dominance). Anti-immunity guard enforced in engine: a veg_spread cannot exceed
# VEG_SPREAD_IMMUNITY_CEILING unless additives are clean AND sodium is sub-red-label.
VEG_SPREAD_WEIGHTS = {
    "processing_quality":   0.15,
    "nutrient_density":     0.08,
    "calorie_density":      0.18,
    "glycemic_quality":     0.12,
    "protein_quality":      0.03,
    "additive_quality":     0.16,
    "satiety_support":      0.06,
    "fat_quality":          0.08,
    "regulatory_quality":   0.08,
    "whole_food_integrity": 0.06,
}
VEG_SPREAD_IMMUNITY_CEILING = 80.0   # EV-032 anti-immunity guard (bari_usecase_guardrails_v2)

# ---------------------------------------------------------------------------
# R7 v1.1 (TASK-169A) — gate the live-culture +8 to GENUINELY cultured dairy only.
# Supersedes the v1 "product_type_dairy + plain ⇒ cultured" assumption (which leaked
# the +8 onto plain FLUID MILK and over-credited table-stakes fresh-cheese culturing).
# Design: recalibration_p0_design_v1.md § v1.1, R7 v1.1. EV-024/026 lineage (REVISED).
#
# Bonus fires when EITHER:
#   Path A — declared culture marker (has_fermentation==True). Unchanged from HEAD.
#   Path B — inherently-cultured product TYPE (yogurt subtypes; aged/specialty cultured
#            cheese by name marker) AND NOT a hard-excluded fluid-milk / plant drink /
#            uncultured-cream product, AND NOT a flavored variant.
#
# IMPLEMENTATION NOTE (router reconciliation, per v1.1 call #4): the live router
# (router_v2.py) does NOT emit a `milk_dairy` category nor a top-level `yogurt`
# category — fluid milk, cheese AND yogurt all route to `dairy_protein`. So the spec's
# `category=="milk_dairy"` / `category=="yogurt"` keys cannot be used verbatim. The
# INTENT (yogurt qualifies via Path B; fluid milk is hard-excluded; cottage/white-cheese
# fresh subtypes are excluded) is implemented here against the REAL router vocabulary:
#   - yogurt qualifies via the cultured yogurt SUBTYPES the router actually emits;
#   - fluid milk is hard-excluded by a fluid-milk NAME marker (חלב/משקה without a
#     cheese/yogurt identity), since it shares `dairy_protein` with cheese;
#   - cottage + white-cheese (גבינה לבנה/לבנה) fresh subtypes are DELIBERATELY excluded
#     so plain cottage lands at its R1+R2+R4 value (~90/A), not S.

# Path B — yogurt subtypes the router emits (router_v2 HARD_ANCHORS). Yogurt is cultured
# by definition → qualifies for the bonus even with a sparse panel.
CULTURED_YOGURT_SUBTYPES = (
    "yogurt", "greek_yogurt", "protein_yogurt", "bio_yogurt", "froop_yogurt",
    "yogurt_mixin", "bio",
)

# Path B — aged / specialty CULTURED-cheese NAME markers (the genuinely-cultured cheese
# identities whose culturing is a DIFFERENTIATING virtue, unlike table-stakes fresh
# cheese). Detected by name because the router does not emit dedicated subtypes for them
# in the current corpus. DELIBERATELY EXCLUDES cottage (קוטג') and white-cheese
# (גבינה לבנה / לבנה) fresh subtypes per the cottage ruling (§ v1.1 R7).
CULTURED_CHEESE_NAME_MARKERS_HE = (
    "קממבר", "ברי", "גאודה", "מוצרלה", "מוצארלה", "פרמזן", "פרמז'ן", "רוקפור",
    "גורגונזולה", "צ'דר", "צ׳דר", "אמנטל", "בולגרית", "פטה",
    "שמנת חמוצה", "קוואַרק", "קווארק", "מצרלה", "כחולה", "כבושה", "מיושנת",
)

# Hard-exclude: FLUID-MILK / drink name markers. A `dairy_protein` (or beverage) product
# whose identity is a fluid drink is NEVER cultured → never gets the Path-B bonus.
# Plant drinks (סויה/שקדים/שיבולת שועל/אורז/קוקוס) carry משקה and are caught here too.
FLUID_MILK_NAME_MARKERS_HE = (
    "חלב", "משקה", "שתייה", "לשתייה",
)
# Cheese/yogurt identity markers that OVERRIDE the fluid-milk exclusion when a product
# name contains both (e.g. "גבינת חלב עזים" is a cheese, not fluid milk). A product that
# matches a fluid-milk marker but ALSO carries one of these is NOT treated as fluid milk.
DAIRY_SOLID_IDENTITY_MARKERS_HE = (
    "גבינה", "גבינת", "קוטג", "לבנה", "לבנייה", "יוגורט", "קפיר", "שמנת",
    "מעדן", "ממרח גבינה",
)

# ---------------------------------------------------------------------------
# R4 v1.1 (TASK-169A) — flavored / seasoned-variant exclusion from the NOVA-3→2
# demotion. Whole-food culinary flavorings (garlic/dill/onion/herbs/chili/…) are NOT
# additive `flavor_enhancer` markers, so a seasoned cheese (e.g. napoleon שום שמיר, 16%
# fat) wrongly passed the v1 `is_plain` test, got demoted NOVA 3→2 and rode R1/R2 to A.
# A declared flavoring — even whole-food — makes a dairy product a FLAVORED VARIANT and
# forfeits the plain-dairy NOVA-2 retention. This only ever BLOCKS a demotion (keeps a
# tentative NOVA 3 at 3); it never promotes and never demotes anything new. Gated by
# BARI_RECAL_P0. Design: recalibration_p0_design_v1.md § v1.1, R4 v1.1.
FLAVORED_VARIANT_MARKERS_HE = (
    "שום", "שמיר", "בצל", "בצלים", "עירית", "פטרוזיליה", "כוסברה", "בזיליקום",
    "נענע", "תבלין", "תבלינים", "עשבי תיבול", "עשב תיבול", "זעתר", "פפריקה",
    "צ'ילי", "צ׳ילי", "חריף", "חלפיניו", "ג'לפינו", "ג׳לפינו", "פלפל",
    "עגבני", "עגבניות מיובשות", "זית", "זיתים", "פטריות", "ירקות", "בטעם",
    "תות", "וניל", "אגוז", "דבש", "קינמון", "מקורמל", "בייגלס",
)

# TASK-169D ship-prep — SERVING-SUGGESTION / MARKETING-PROSE markers.
# When BSIP0 is unavailable, BSIP1 sometimes falls back to a product's marketing copy and
# mis-captures a serving-suggestion sentence ("...with the addition of fresh fruit, granola,
# sweet honey, or just as-is. As it is. Perfect.") as an ingredient-list ITEM. Such prose
# can name an add-on (e.g. דבש/honey) that the product itself does NOT contain, falsely
# tripping the flavored-variant exclusion and stripping a plain cultured yogurt's +8.
# These markers identify an ingredient-list item that is consumption/serving prose, NOT a
# real ingredient. Used ONLY (and only when BARI_RECAL_P0_YOGURT_TRIM is ON) to drop such
# items before the flavored-variant scan. A genuine ingredient list never carries this
# consumer-facing language, so real seasoned/flavored variants (e.g. tzatziki's שום/שמיר in
# a real ingredient list) are unaffected.
SERVING_SUGGESTION_PROSE_MARKERS_HE = (
    "שמשתלב", "בטבעיות", "בכל רגע", "אם זה", "פשוט ככה", "כמו שהוא",
    "מושלם", "טריים או יבשים", "או פשוט",
)


def lookup_protein_scale(protein_g, category, recal_on):
    """R1 — category-relative protein mass score (0..100).
    recal_on False → legacy single supplement curve (byte-identical).
    """
    legacy = [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95)]
    if not recal_on:
        bps = legacy
    else:
        bps = PROTEIN_SCALE_TABLES.get(category, PROTEIN_SCALE_TABLES["default"])
    g = protein_g or 0
    for i in range(len(bps) - 1):
        lo_g, lo_s = bps[i]; hi_g, hi_s = bps[i + 1]
        if g <= hi_g:
            t = (g - lo_g) / (hi_g - lo_g) if hi_g > lo_g else 0
            return lo_s + t * (hi_s - lo_s)
    return bps[-1][1]

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
# TASK-179G — Glass Box D5 (transparency) + D6 (confidence) gate.
# Gated by env flag BARI_GLASSBOX_D5D6 (default OFF). Flag OFF → every constant
# below is inert and the engine is byte-identical to today. Source of truth:
# 01_framework/glass_box/d5_d6_rule_spec_v1.md §1–§2. Evidence registry:
# EV-035 (taxonomy), EV-036 (endemic-flavoring exclusion), EV-037 (band→confidence
# reduction), EV-038 (gate state machine + null floor), EV-039 (flag).
# All numeric thresholds are PROPOSALS pending Product D7 co-sign.
# ---------------------------------------------------------------------------

# EV-037 — D5-band → D6 confidence reduction (the ONLY new D6 input term).
# full/minor (structural-only) = 0; partial (closable gaps) = -10; severe = -20.
GLASSBOX_D5_CONF_REDUCTION = {"full": 0, "minor": 0, "partial": 10, "severe": 20}

# EV-038 — gate state machine thresholds.
# DEMOTE_CEILING_BOUND = 60 is a no-op restatement of the live High/Medium band edge
# (compute_confidence sets a ceiling only for bands below 60); it changes no behavior
# on its own. NULL_FLOOR = 30 is the NEW null-vs-cap boundary (withhold fires only when
# d6_confidence < 30 AND the D5-band is 'severe', OR the panel is absent).
GLASSBOX_DEMOTE_CEILING_BOUND = 60
GLASSBOX_NULL_FLOOR           = 30
GLASSBOX_WITHHELD_LABEL       = "לא נוקד"
GLASSBOX_PARTIAL_FLAG         = "ניתוח חלקי"

# EV-035 / EV-036 — D5 detector lexicons (P2-normalized Hebrew).
# Nutrition-table bleed anchors (P1 truncation): everything at/after these is not
# ingredients. Observed in every maadanim/hummus ingredients_raw string.
GLASSBOX_NUTRITION_BLEED_ANCHORS = (
    "ערכים תזונתיים", "הנתונים המדויקים", "מאפיינים נוספים", "ערך תזונתי",
)

# G4 generic-additive-class lexicon: a bare class term (NOT followed by '(' or ':'
# introducing an E-code/name) is a closable disclosure gap.
GLASSBOX_GENERIC_ADDITIVE_TERMS = (
    "מייצבים", "מייצב", "מתחלב", "חומרי שימור", "חומר משמר", "חומרים משמרים",
    "צבעי מאכל", "צבע מאכל", "חומרי תפיחה", "מגביר חוזק", "מווסתי חומציות",
    "מווסת חומציות", "מסמיך", "נוגד חמצון", "ממתיקים",
)
# Endemic flavoring (EV-036): detected + annotated, but EXCLUDED from band-raising
# and from the D6 reduction (bare in ~70% of maadanim panels).
GLASSBOX_ENDEMIC_FLAVORING_TERMS = (
    "חומרי טעם וריח", "חומר טעם וריח", "חומרי טעם ו ריח", "חומר טעם ו ריח",
)

# G2 compound-food lexicon: named compound expecting an internal '(...)' breakdown.
GLASSBOX_COMPOUND_TERMS = (
    "שוקולד", "עוגיות", "קרם", "ציפוי", "סירופ גלוקוזה", "נבט אורז", "ביסקוויט",
    "ופל", "קרמל", "מילוי", "ריבה",
)

# G3 protein-blend markers (structural blend) and named-source markers (no gap).
GLASSBOX_PROTEIN_BLEND_TERMS = (
    "תערובת חלבונים", "תערובת חלבון", "חלבון צמחי", "חלבונים צמחיים",
)
GLASSBOX_PROTEIN_NAMED_SOURCES = (
    "חלבוני מי גבינה", "חלבון מי גבינה", "רכיבי חלב", "גבינה לבנה", "חלבון חלב",
    "חלבון אפונה", "חלבון אורז", "חלבון סויה",
)
GLASSBOX_PROTEIN_INCOMPLETE_NAMED = ("קולגן", "ג'לטין", "ג׳לטין", "ג'לטינה", "ג׳לטינה")

# ---------------------------------------------------------------------------
# TASK-179P — Glass Box W1.5 DIAAS protein-quality signal.
# Gated by env flag BARI_GLASSBOX_W15 (default OFF). Flag OFF → engine is
# byte-identical to the BARI_GLASSBOX_D5D6 baseline. Source of truth:
# 01_framework/glass_box/diaas_source_table_v1.md §Nutrition Rule Definition.
# Evidence registry: EV-040 (BSIP2 evidence registry).
# Rule A magnitude (+3 raw D2 score points) requires Product D7 co-sign before
# engine activation. Flag remains OFF by default until that co-sign is received.
# ---------------------------------------------------------------------------
# Rule A — complete-protein whitelist (EV-040 / diaas_source_table_v1 Phase 2).
# Each tuple is (pattern_text, source_label). Pattern is matched against the
# P2-normalized ingredient text (Hebrew final-letter normalization applied).
# Only "מבודד" (isolate)-qualified soy qualifies (soy flour DIAAS ~55–65, below ≥75).
DIAAS_COMPLETE_SOURCES = (
    # Whey protein (WPI / whey proteins general)
    ("חלבון מי גבינה מבודד",  "whey_protein_isolate"),
    ("חלבוני מי גבינה",       "whey_proteins_general"),
    # Casein / milk protein
    ("קזאין",                  "casein"),
    ("חלבוני חלב",             "milk_protein"),
    ("חלבוני גבינה",           "cheese_protein"),
    ("casein",                 "casein_en"),
    ("milk protein",           "milk_protein_en"),
    # Egg / egg white
    ("חלבון ביצה",             "egg_white"),
    ("ביצה",                   "whole_egg"),
    ("egg white",              "egg_white_en"),
    ("whole egg",              "whole_egg_en"),
    # Soy protein ISOLATE only — NOT generic "סויה" or "קמח סויה"
    ("חלבון סויה מבודד",       "soy_protein_isolate"),
    ("soy protein isolate",    "soy_protein_isolate_en"),
    ("whey protein isolate",   "wpi_en"),
    ("whey protein concentrate", "wpc_en"),
)

# Rule B — disclosure-gap trigger patterns (EV-040).
# Generic protein declarations without a named complete source.
DIAAS_DISCLOSURE_GAP_TRIGGERS = (
    ("תערובת חלבונים",       "protein_blend_generic"),
    ("חלבון צמחי מבודד",     "plant_protein_isolated_generic"),
    ("חלבון צמחי",           "plant_protein_generic"),
)

# Rule A credit magnitude — bounded to ≤ 0.5 grade band on its own.
# Product D7 co-sign required before activation (TASK-179P Phase 3 note).
DIAAS_D2_CREDIT = 3

# D2 sub-score cap — protein_quality dimension is 0–100; credit cannot overflow.
DIAAS_D2_SCORE_CAP = 100

# ---------------------------------------------------------------------------
# Glass Box D4 additive tier lookup table.
# Gated by env flag BARI_GLASSBOX_W2 (default OFF). Flag OFF → every constant
# below is inert and the engine is byte-identical to the BARI_GLASSBOX_W15
# baseline. No score movement — D4 is presentation-only (annotate-only).
# Tier values: "functional" | "likely-neutral" | "dose-dependent" | "contested"
#              | "disclosure-gap" | "confirmed-negative" | "unclassified".
#
# W2 (TASK-179S): the original 20 entries sourced from
#   additive_prototype_set_v1.md §Nutrition Phase 3 Co-sign. Evidence registry EV-041.
# W3 (TASK-181D): EXTENDED to the full 36-additive tiered library. The 16 newly
#   added entries (E160a/E163/E162/E100/E141/E333/E331/E327/E296/E270/E401/E516/
#   E500/E575/E960 + E1412/E1414 folded into E1422) carry their EV-043 tier.
#   Tier source of truth: 01_framework/glass_box/additive_tiered_library_v1.md
#   (TASK-181B, Nutrition + Product D7 co-signed). Identity / Hebrew shelf labels:
#   01_framework/glass_box/additive_library_expanded_v1.md (TASK-181A). No detector
#   LOGIC change — EV-043 mechanism field confirms the existing detect_additives_d4()
#   reads these lookup values unchanged; W3 supplies values only.
#
# DO NOT add additives not in additive_tiered_library_v1.md; unlisted = "unclassified".
# ---------------------------------------------------------------------------
GLASSBOX_W2_ADDITIVES: dict = {
    "E330": {
        "name_he": "חומצת לימון",
        "name_en": "Citric acid",
        "tier": "functional",
        "function_he": "מווסת חומציות / מונע חמצון",
        "match_patterns_he": ["חומצת לימון", "חומצה ציטרית"],
    },
    "E202": {
        "name_he": "פוטסיום סורבט",
        "name_en": "Potassium sorbate",
        "tier": "likely-neutral",
        "function_he": "חומר משמר אנטי-מיקרוביאלי",
        "match_patterns_he": ["פוטסיום סורבט", "סורבט אשלגן", "סורבט פוטסיום"],
    },
    "E300": {
        "name_he": "חומצה אסקורבית",
        "name_en": "Ascorbic acid",
        "tier": "functional",
        "function_he": "נוגד חמצון / משפר בצק",
        "match_patterns_he": ["חומצה אסקורבית", "ויטמין C", "ויטמין c"],
    },
    "E1422": {
        # TASK-181D: E1412 / E1414 (distarch phosphate / acetylated distarch
        # phosphate) fold into this modified-starch tier per tiered library #36 —
        # same Hebrew term ("עמילן מעובד") + group ADI "not specified". The explicit
        # E-number variants are added to the match set so an "E1412"/"E1414"
        # declaration is detected as this same entry (no duplicate panel row).
        "name_he": "עמילן מעובד",
        "name_en": "Modified starch (incl. E1412/E1414/E1442)",
        "tier": "likely-neutral",
        "function_he": "מייצב מרקם / מונע הפרדת נוזלים",
        "match_patterns_he": [
            "עמילן מעובד", "עמילן שונה", "עמילן מוקשה", "עמילן משונה",
            "E1412", "e1412", "E1414", "e1414", "E1442", "e1442",
        ],
    },
    "E282": {
        "name_he": "פרופיונט סידן",
        "name_en": "Calcium propionate",
        "tier": "likely-neutral",
        "function_he": "חומר משמר נגד עובש בלחם",
        "match_patterns_he": ["פרופיונט סידן", "סידן פרופיונט", "קלציום פרופיונט"],
    },
    "E481": {
        "name_he": "נתרן סטארויל לקטילט",
        "name_en": "Sodium stearoyl lactylate",
        "tier": "likely-neutral",
        "function_he": "מרכך בצק / משפר נפח לחם",
        "match_patterns_he": ["נתרן סטארויל לקטילט", "SSL", "נתרן סטיארויל לקטילאט"],
    },
    "E407": {
        "name_he": "קרגינן",
        "name_en": "Carrageenan",
        "tier": "contested",
        "function_he": "מייצב / חומר מסמיך ממקור אצות",
        "match_patterns_he": ["קרגינן", "קרגינאן", "קאראגינן"],
    },
    "E471": {
        "name_he": "מונו ודיגליצרידים",
        "name_en": "Mono- and diglycerides of fatty acids",
        "tier": "likely-neutral",
        "function_he": "חומר תחליב — מרכך לחם ומייצב שומן",
        "match_patterns_he": [
            "מונו ודיגליצרידים של חומצות שומן",
            "מונו ודיגליצרידים",
            "מונוגליצרידים",
            "דיגליצרידים",
        ],
    },
    "E472e": {
        "name_he": "DATEM",
        "name_en": "Diacetyl tartaric acid esters of mono- and diglycerides",
        "tier": "likely-neutral",
        "function_he": "מרכך בצק / חומר תחליב לחם",
        "match_patterns_he": ["DATEM", "datem", "חומצה טרטרית מונו ודיגליצרידים"],
    },
    "E415": {
        "name_he": "קסנטן",
        "name_en": "Xanthan gum",
        "tier": "functional",
        "function_he": "מייצב / חומר מסמיך מתסיסה חיידקית",
        "match_patterns_he": ["קסנטן", "קסנטאן", "קסנתן"],
    },
    "E450": {
        "name_he": "פוספטים",
        "name_en": "Phosphates (E450/E451/E452)",
        "tier": "dose-dependent",
        "function_he": "מייצב חלבוני חלב / חומר תחליב",
        "match_patterns_he": ["פוספט", "פוספטים", "דיפוספט", "טריפוספט", "פוליפוספט"],
    },
    "E440": {
        "name_he": "פקטין",
        "name_en": "Pectin",
        "tier": "functional",
        "function_he": "חומר מסמיך / סיב תזונתי מסיס ממקור פירות",
        "match_patterns_he": ["פקטין"],
    },
    "E410": {
        "name_he": "לוקוסט-בין גאם",
        "name_en": "Locust bean gum",
        "tier": "functional",
        "function_he": "מייצב טבעי ממקור חרוב",
        "match_patterns_he": ["לוקוסט-בין גאם", "לוקוסט בין גאם", "קרוב בין גאם", "קרוב-בין גאם"],
    },
    "E412": {
        "name_he": "גואר",
        "name_en": "Guar gum",
        "tier": "functional",
        "function_he": "חומר מסמיך / מייצב מים ממקור קטניות",
        "match_patterns_he": ["גואר", "גואר גאם", "גואר גם"],
    },
    "E955": {
        "name_he": "סוכרלוז",
        "name_en": "Sucralose",
        "tier": "dose-dependent",
        "function_he": "ממתיק ללא קלוריות (פי ~600 מסוכרוז)",
        "match_patterns_he": ["סוכרלוז", "sucralose"],
    },
    "E950": {
        "name_he": "אצסולפאם K",
        "name_en": "Acesulfame potassium",
        "tier": "dose-dependent",
        "function_he": "ממתיק ללא קלוריות (פי ~200 מסוכרוז)",
        "match_patterns_he": ["אצסולפאם", "אצסולפם", "acesulfame", "אצסולפאם k", "אצסולפאם K"],
    },
    "E466": {
        "name_he": "קרבוקסי מתיל צלולוז",
        "name_en": "Carboxymethylcellulose",
        "tier": "contested",
        "function_he": "מייצב / מסמיך על בסיס צלולוז",
        "match_patterns_he": ["קרבוקסי מתיל צלולוז", "קרבוקסימתיל צלולוז", "CMC", "cmc"],
    },
    "E150": {
        "name_he": "צבע קרמל",
        "name_en": "Caramel color",
        "tier": "disclosure-gap",
        "function_he": "צבע חום — הסוג הספציפי (I–IV) אינו מצוין על תוויות ישראליות",
        "match_patterns_he": ["צבע קרמל", "קרמל"],
    },
    "E211": {
        "name_he": "נתרן בנזואט",
        "name_en": "Sodium benzoate",
        "tier": "dose-dependent",
        "function_he": "חומר משמר אנטי-מיקרוביאלי בסביבה חומצית",
        "match_patterns_he": ["נתרן בנזואט", "בנזואט נתרן"],
    },
    "E320": {
        "name_he": "BHA",
        "name_en": "Butylated hydroxyanisole",
        "tier": "contested",
        "function_he": "נוגד חמצון לשומנים — מסווג IARC 2B (בעלי חיים)",
        "match_patterns_he": ["BHA", "bha", "בוטילציאניזול", "בוטיל הידרוקסיאניזול"],
    },
    # -----------------------------------------------------------------------
    # TASK-181D — 16 newly added additives (observed on the displayed shelf,
    # absent from the W2 prototype 20). Tiers per additive_tiered_library_v1.md
    # (EV-043, §2.B). Hebrew shelf labels per additive_library_expanded_v1.md §3.B.
    # E1412/E1414 are NOT here — they fold into E1422 above (tiered library #36).
    # -----------------------------------------------------------------------
    "E160a": {
        "name_he": "בטא-קרוטן",
        "name_en": "Beta-carotene",
        "tier": "functional",
        "function_he": "צבע מאכל כתום/צהוב — קרוטנואיד פרו-ויטמין A",
        "match_patterns_he": ["בטא קרוטן", "בטא-קרוטן", "ביתא קרוטן", "ביתא-קרוטן"],
    },
    "E163": {
        "name_he": "אנטוציאנינים",
        "name_en": "Anthocyanins",
        "tier": "functional",
        "function_he": "צבע מאכל אדום/סגול ממקור צמחי (רכז גזר שחור)",
        "match_patterns_he": ["אנטוציאנין", "אנטוציאנינים", "רכז גזר שחור"],
    },
    "E162": {
        "name_he": "אדום סלק",
        "name_en": "Beetroot red / betanin",
        "tier": "functional",
        "function_he": "צבע מאכל אדום ממקור סלק",
        "match_patterns_he": ["אדום סלק", "רכז סלק", "בטנין"],
    },
    "E100": {
        "name_he": "כורכומין",
        "name_en": "Curcumin",
        "tier": "functional",
        "function_he": "צבע מאכל צהוב ממקור כורכום",
        "match_patterns_he": ["כורכומין", "כורכום"],
    },
    "E141": {
        "name_he": "תרכובות נחושת של כלורופיל",
        "name_en": "Copper complexes of chlorophylls",
        "tier": "unclassified",
        "function_he": "צבע מאכל ירוק נושא נחושת",
        "match_patterns_he": ["תרכובות נחושת של כלורופיל", "כלורופיל נחושת", "נחושת כלורופיל"],
    },
    "E333": {
        "name_he": "סידן ציטרט",
        "name_en": "Calcium citrate",
        "tier": "functional",
        "function_he": "מלח ציטרט — מקור סידן / מייצב",
        "match_patterns_he": ["טריקלציום ציטרט", "קלציום ציטרט", "סידן ציטרט", "סידן (טריקלציום ציטרט)"],
    },
    "E331": {
        "name_he": "סודיום ציטרט",
        "name_en": "Sodium citrate",
        "tier": "functional",
        "function_he": "מלח ציטרט — מווסת חומציות / מלח מתחלב",
        "match_patterns_he": ["סודיום ציטרט", "טרי סודיום ציטרט", "נתרן ציטרט", "ציטרט נתרן"],
    },
    "E327": {
        "name_he": "סידן לקטט",
        "name_en": "Calcium lactate",
        "tier": "functional",
        "function_he": "מלח לקטט — מקור סידן / מווסת חומציות",
        "match_patterns_he": ["סידן לקטט", "קלציום לקטט", "לקטט סידן"],
    },
    "E296": {
        "name_he": "חומצה מאלית",
        "name_en": "Malic acid",
        "tier": "functional",
        "function_he": "חומצת מאכל (חומצה מחזור קרבס)",
        "match_patterns_he": ["חומצה מאלית", "חומצת תפוח"],
    },
    "E270": {
        "name_he": "חומצה לקטית",
        "name_en": "Lactic acid",
        "tier": "functional",
        "function_he": "חומצת מאכל / משמר — תוצר תסיסה טבעי",
        "match_patterns_he": ["חומצה לקטית", "חומצת חלב", "חומצה לקטטית"],
    },
    "E401": {
        "name_he": "אלגינט נתרן",
        "name_en": "Sodium alginate",
        "tier": "functional",
        "function_he": "מסמיך / מייצב ממקור אצות חומות",
        "match_patterns_he": ["אלגינט נתרן", "נתרן אלגינט", "אלגינאט נתרן", "אלגינט"],
    },
    "E516": {
        "name_he": "גופרת סידן",
        "name_en": "Calcium sulphate",
        "tier": "functional",
        "function_he": "חומר מקשה / מקור סידן (גבס)",
        "match_patterns_he": ["גופרת סידן", "סולפט סידן", "קלציום סולפט", "גופרית סידן"],
    },
    "E500": {
        "name_he": "סודיום קרבונט",
        "name_en": "Sodium carbonates / bicarbonate",
        "tier": "functional",
        "function_he": "מווסת חומציות / חומר תפיחה",
        "match_patterns_he": ["סודיום קרבונט", "נתרן קרבונט", "סודה לשתייה", "ביקרבונט", "סודיום ביקרבונט", "סודה לאפייה"],
    },
    "E575": {
        "name_he": "גלוקונו דלתא לקטון",
        "name_en": "Glucono-delta-lactone (GDL)",
        "tier": "functional",
        "function_he": "חומצת מאכל / מקריש — מתפרק לחומצה גלוקונית",
        "match_patterns_he": ["גלוקונו דלתא לקטון", "גלוקונו-דלתא-לקטון", "GDL", "gdl"],
    },
    "E960": {
        "name_he": "סטיביול גליקוזידים",
        "name_en": "Steviol glycosides",
        "tier": "dose-dependent",
        "function_he": "ממתיק ללא קלוריות ממקור צמח הסטיביה",
        "match_patterns_he": ["סטיביול גליקוזידים", "סטיביול גליקוזיד", "סטיביה", "stevia"],
    },
}

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
