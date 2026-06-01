"""
BSIP2 Robustness Sprint v1 — Corpus Generator

Creates 50 synthetic test products covering:
  Group A: Clean baselines (5)
  Group B: Missing/partial nutrition (8)
  Group C: Missing/corrupted ingredients (8)
  Group D: Routing instability — borderline categories (8)
  Group E: Claim vs reality — marketing gap (8)
  Group F: Missing identity fields (5)
  Group G: Data consistency failures (4)
  Group H: Hybrid / edge cases (4)

Output: C:/Bari/03_operations/bsip2/proto_v0/src/robustness_corpus_001.json

Each product includes a '_robustness_meta' key with test metadata.
This key is NOT part of the BSIP1 schema and is stripped before real pipeline use.
"""

import json
import pathlib
import copy

OUTPUT_PATH = pathlib.Path(__file__).parent / "robustness_corpus_001.json"

# ---------------------------------------------------------------------------
# Product factory
# ---------------------------------------------------------------------------

_TEMPLATE = {
    "schema_version":         "bsip1_v0_1",
    "file_type":              "product",
    "canonical_name_en":      None,
    "package_size_g":         None,
    "unit_count":             None,
    "unit_size_g":            None,
    "serving_size_g":         None,
    "country_of_origin":      "ישראל",
    "kosher_certification":   "הרבנות הראשית",
    "image_url":              None,
    "source_retailers":       ["synthetic_robustness_test"],
    "energy_source_unit":     "kcal",
    "allergens_contains":     [],
    "allergens_may_contain":  [],
    "claims":                 [],
    "confidence": {
        "identity_confidence":  "high",
        "barcode_confidence":   "synthetic",
        "nutrition_confidence": "confirmed_per_100g",
        "matched_by":           "synthetic_test",
        "observation_count":    1,
    },
    "barcode_validation_status":    "synthetic",
    "nutrition_basis_claimed":      "ל-100 גרם",
    "nutrition_basis_detected":     "per_100g",
    "nutrition_consistency_status": "consistent",
    "nutrition_consistency_warnings": [],
    "ingredient_text_quality":      "clean",
    "ingredient_warnings":          [],
    "canonical_trust_score":        0.88,
    "canonical_trust_level":        "high",
    "canonical_risk_flags":         [],
    "conflicts_summary": {
        "count": 0, "has_unresolved": False,
        "fields_in_conflict": [], "identity_conflicts": [],
        "nutrition_conflicts": [], "ingredient_conflicts": [],
        "labeling_conflicts": [], "completeness_conflicts": [],
    },
    "missing_fields":   [],
    "inferred_fields":  [],
    "audit_ref":        "robustness_sprint_v1",
    "ingredients_raw":  "",
    "ingredients_raw_provenance": {
        "source": "synthetic_test",
        "bsip0_status": "synthetic",
        "populated_at": "robustness_sprint_v1",
        "missing": False,
    },
}


def _make(
    pid, barcode, name_he, brand, nutrition, ingredients_text, ingredients_list,
    noise_profile="clean_baseline", noise_scenarios=None, expected_routing="",
    expected_conf_band="high", test_purpose="", failure_risk=None,
    **overrides,
):
    """Create a complete synthetic product with robustness metadata."""
    p = copy.deepcopy(_TEMPLATE)
    p["canonical_product_id"] = f"robustness_{pid}"
    p["barcode"]              = barcode
    p["canonical_name_he"]    = name_he
    p["brand"]                = brand
    p["normalized_nutrition_per_100g"] = nutrition
    p["ingredients_text_he"]  = ingredients_text
    p["ingredients_list"]     = ingredients_list
    p["ingredients_raw"]      = ingredients_text
    p.update(overrides)

    p["_robustness_meta"] = {
        "test_id":                pid,
        "noise_scenarios":        noise_scenarios or [],
        "noise_profile":          noise_profile,
        "expected_routing":       expected_routing,
        "expected_confidence_band": expected_conf_band,
        "test_purpose":           test_purpose,
        "failure_risk_categories": failure_risk or [],
    }
    return p


def _nn(kcal=None, fat=None, sat=None, trans=None, sodium=None,
        carbs=None, sugar=None, fiber=None, protein=None):
    return {
        "energy_kcal":    kcal,
        "fat_g":          fat,
        "fat_saturated_g": sat,
        "fat_trans_g":    trans,
        "sodium_mg":      sodium,
        "carbohydrates_g": carbs,
        "sugars_g":       sugar,
        "dietary_fiber_g": fiber,
        "protein_g":      protein,
    }


# ---------------------------------------------------------------------------
# GROUP A — Clean baselines
# ---------------------------------------------------------------------------

_A1 = _make(
    "A1", "7290000001001",
    "קורנפלקס דגני בוקר קלאסי", "תלמה",
    _nn(370, 1.2, 0.3, 0.0, 710, 84, 8, 3.2, 8),
    "תירס מלא (98%), ויטמינים ומינרלים (תיאמין, ריבופלאבין, נקוטינאמיד, ויטמין B6, חומצה פולית, ויטמין B12, ויטמין D), מלח",
    ["תירס מלא (98%)", "ויטמינים ומינרלים", "מלח"],
    noise_profile="clean_baseline", expected_routing="cereal",
    expected_conf_band="very_high",
    test_purpose="Baseline clean cereal — expects confident routing + high score",
)

_A2 = _make(
    "A2", "7290000001002",
    "חטיף גרנולה שיבולת שועל ודבש", "תלמה",
    _nn(440, 16, 2.8, 0.0, 95, 64, 22, 5.5, 9),
    "שיבולת שועל מלאה (55%), סוכר חום, שמן קנולה, דבש (4%), גרעיני חמניות, גרעיני דלעת, מלח, חומר טעם וריח",
    ["שיבולת שועל מלאה (55%)", "סוכר חום", "שמן קנולה", "דבש (4%)", "גרעיני חמניות", "גרעיני דלעת", "מלח", "חומר טעם וריח"],
    noise_profile="clean_baseline", expected_routing="snack_bar_granola",
    expected_conf_band="high",
    test_purpose="Baseline clean granola bar — expects snack_bar routing",
)

_A3 = _make(
    "A3", "7394376621451",
    "לחמי קריספ שיפון מחמצת ויקינג", "ויקינג",
    _nn(340, 2.1, 0.3, 0.0, 510, 71, 1.2, 12, 12),
    "שיפון מלא (95%), מחמצת שיפון (שיפון, מים, שמרי בר), מים, מלח",
    ["שיפון מלא (95%)", "מחמצת שיפון (שיפון, מים, שמרי בר)", "מים", "מלח"],
    noise_profile="clean_baseline", expected_routing="crispbread",
    expected_conf_band="very_high",
    test_purpose="Baseline clean crispbread — hard anchor should fire on 'לחמי קריספ'",
)

_A4 = _make(
    "A4", "7394376620000",
    "משקה שיבולת שועל אוטלי", "אוטלי",
    _nn(47, 1.5, 0.2, 0.0, 100, 6.5, 4.0, 0.8, 1.0),
    "מים, שיבולת שועל (10%), שמן חמניות, ויטמינים (ויטמין D, ריבופלאבין, ויטמין B12), מלח",
    ["מים", "שיבולת שועל (10%)", "שמן חמניות", "ויטמינים", "מלח"],
    noise_profile="clean_baseline", expected_routing="beverage",
    expected_conf_band="very_high",
    test_purpose="Baseline clean oat milk — known plant milk brand should activate beverage gate",
    brand_override=None,
)
_A4["brand"] = "אוטלי"

_A5 = _make(
    "A5", "7290000001005",
    "יוגורט 3% שומן דנונה", "דנונה",
    _nn(67, 3.2, 2.0, 0.0, 45, 4.8, 4.5, 0.0, 4.5),
    "חלב מפוסטר, חיידקי חמצת (Lactobacillus bulgaricus, Streptococcus thermophilus)",
    ["חלב מפוסטר", "חיידקי חמצת (Lactobacillus bulgaricus, Streptococcus thermophilus)"],
    noise_profile="clean_baseline", expected_routing="dairy_protein",
    expected_conf_band="very_high",
    test_purpose="Baseline clean yogurt — hard anchor on 'יוגורט' should fire",
)


# ---------------------------------------------------------------------------
# GROUP B — Missing / partial nutrition
# ---------------------------------------------------------------------------

_B1 = _make(
    "B1", "7290000002001",
    "דגני בוקר מלאים עם סיבים", "קלוגס",
    _nn(360, 2.0, 0.5, 0.0, 580, 74, 6, None, 10),  # fiber missing
    "חיטה מלאה (65%), סוכר, מלח, ויטמינים ומינרלים",
    ["חיטה מלאה (65%)", "סוכר", "מלח", "ויטמינים ומינרלים"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:dietary_fiber_g"],
    expected_routing="cereal", expected_conf_band="high",
    test_purpose="Fiber value absent — fiber-driven dimensions should fall back to 0",
    failure_risk=["MISSINGNESS"],
)

_B2 = _make(
    "B2", "7290000002002",
    "חטיף אנרגיה שקדים ותמרים", "טבעי טעים",
    _nn(430, 18, 1.8, 0.0, None, 55, 28, 4.5, 8),  # sodium missing
    "תמרים (45%), שקדים (22%), שיבולת שועל, גרעיני דלעת, קוקוס טחון, שמן קוקוס",
    ["תמרים (45%)", "שקדים (22%)", "שיבולת שועל", "גרעיני דלעת", "קוקוס טחון", "שמן קוקוס"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:sodium_mg"],
    expected_routing="snack_bar_granola", expected_conf_band="high",
    test_purpose="Sodium absent — red label check for sodium cannot fire; score should not be penalized for absent value",
    failure_risk=["MISSINGNESS"],
)

_B3 = _make(
    "B3", "7290000002003",
    "לחם מחמצת כפרי שחור", "אחלה",
    _nn(240, 2.8, None, 0.0, 440, 46, 1.5, 5.5, 8),  # sat_fat missing
    "קמח שיפון מלא (52%), מחמצת שיפון (5%), מים, קמח חיטה, גרעיני כוסמת, מלח, שמרים",
    ["קמח שיפון מלא (52%)", "מחמצת שיפון (5%)", "מים", "קמח חיטה", "גרעיני כוסמת", "מלח", "שמרים"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:fat_saturated_g"],
    expected_routing="bread", expected_conf_band="high",
    test_purpose="Saturated fat absent — fat_quality dimension should return neutral 50",
    failure_risk=["MISSINGNESS"],
)

_B4 = _make(
    "B4", "7290000002004",
    "יוגורט יווני עשיר", "שטראוס",
    _nn(95, 5.0, 3.5, 0.0, 50, 4.2, 4.0, 0.0, None),  # protein missing
    "חלב מפוסטר, שמנת, חיידקי חמצת (Lactobacillus bulgaricus, Streptococcus thermophilus)",
    ["חלב מפוסטר", "שמנת", "חיידקי חמצת"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:protein_g"],
    expected_routing="dairy_protein", expected_conf_band="high",
    test_purpose="Protein absent — protein_quality and nutrient_density dimensions degraded",
    failure_risk=["MISSINGNESS"],
)

_B5 = _make(
    "B5", "7290000002005",
    "קרקר קמח שיפון מלוח", "ריץ",
    _nn(None, None, None, None, None, None, None, None, None),  # all nutrition missing
    "קמח שיפון (80%), שמן צמחי, מלח, שמרים",
    ["קמח שיפון (80%)", "שמן צמחי", "מלח", "שמרים"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:all_fields"],
    expected_routing="cracker", expected_conf_band="insufficient_context",
    test_purpose="All nutrition fields absent — should reach INSUFFICIENT degradation level",
    failure_risk=["MISSINGNESS"],
)
_B5["missing_fields"] = ["energy_kcal", "fat_g", "fat_saturated_g", "fat_trans_g",
                          "sodium_mg", "carbohydrates_g", "sugars_g", "dietary_fiber_g", "protein_g"]

_B6 = _make(
    "B6", "7290000002006",
    "משקה שיבולת שועל בטעם שוקולד", "אלפרו",
    _nn(None, 1.8, 0.3, 0.0, 95, 7.2, 5.5, 0.8, 1.5),  # kcal missing
    "מים, שיבולת שועל (9.7%), סוכר, קקאו, שמן חמניות, מלח, ויטמינים",
    ["מים", "שיבולת שועל (9.7%)", "סוכר", "קקאו", "שמן חמניות", "מלח", "ויטמינים"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:energy_kcal"],
    expected_routing="beverage", expected_conf_band="high",
    test_purpose="Energy absent — calorie_density dimension returns neutral 50",
    failure_risk=["MISSINGNESS"],
)
_B6["brand"] = "אלפרו"

_B7 = _make(
    "B7", "7290000002007",
    "חטיף דגנים שוקולד ואגוזים", "בריגס",
    _nn(450, 20, 7.5, 0.5, 130, None, 22, 3.5, 9),  # carbs missing
    "שיבולת שועל (35%), שוקולד חלב (20%), אגוזי לוז, סוכר, שמן דקלים, מלח, לציטין",
    ["שיבולת שועל (35%)", "שוקולד חלב (20%)", "אגוזי לוז", "סוכר", "שמן דקלים", "מלח", "לציטין"],
    noise_profile="missing_nutrition", noise_scenarios=["missing_nutrition:carbohydrates_g"],
    expected_routing="snack_bar_granola", expected_conf_band="high",
    test_purpose="Carbs absent — sugar-over-carbs consistency check cannot run; SC classification ambiguous",
    failure_risk=["MISSINGNESS"],
)

_B8 = _make(
    "B8", "7290000002008",
    "לחם אחיד עם שיפון", "אנגל",
    _nn(265, 2.5, 0.4, 0.0, 590, 48, 30, 4.0, 8),  # sugar=30 > carbs=48 is valid but suspicious
    "קמח חיטה, קמח שיפון (15%), מים, שמרים, מלח, סוכר, שמן קנולה",
    ["קמח חיטה", "קמח שיפון (15%)", "מים", "שמרים", "מלח", "סוכר", "שמן קנולה"],
    noise_profile="data_inconsistency",
    noise_scenarios=["nutrition_inconsistency:sugar_le_carbs_violated"],
    expected_routing="bread", expected_conf_band="low",
    test_purpose="sugar (30g) < carbs (48g) is valid here, but high ratio creates suspicious flag; test confidence impact",
    failure_risk=["RETAILER_INCONSISTENCY"],
    nutrition_consistency_status="suspicious",
    nutrition_consistency_warnings=["sugar_g=30 is 62% of carbohydrates_g=48 — possible per-serving confusion"],
)
_B8["nutrition_consistency_status"] = "suspicious"
_B8["nutrition_consistency_warnings"] = ["sugar_g=30 is 62% of carbohydrates_g=48 — possible per-serving confusion"]


# ---------------------------------------------------------------------------
# GROUP C — Missing / corrupted ingredients
# ---------------------------------------------------------------------------

_C1 = _make(
    "C1", "7290000003001",
    "לחם מחמצת שיפון ארטיזנלי", "לחמיה",
    _nn(235, 1.8, 0.3, 0.0, 480, 44, 1.8, 7.5, 9),
    "",   # empty ingredient text
    [],   # empty list
    noise_profile="missing_ingredients", noise_scenarios=["missing_ingredients:text_and_list"],
    expected_routing="bread", expected_conf_band="low",
    test_purpose="No ingredient data at all — NOVA, additive, fiber source signals all absent",
    failure_risk=["MISSINGNESS"],
)

_C2 = _make(
    "C2", "7290000003002",
    "דגני בוקר חיטה מלאה ופירות יבשים", "קלוגס",
    _nn(350, 1.5, 0.3, 0.0, 500, 72, 18, 8, 10),
    "",   # empty text but list present
    ["חיטה מלאה (62%)", "פירות יבשים (12%)", "סוכר", "מלח"],
    noise_profile="missing_ingredients", noise_scenarios=["missing_ingredients:text_only"],
    expected_routing="cereal", expected_conf_band="moderate",
    test_purpose="Ingredient list present but no text — L3 extraction works but claims analysis limited",
    failure_risk=["MISSINGNESS"],
)

_C3 = _make(
    "C3", "7290000003003",
    "חטיף אנרגיה שיבולת שועל ותמרים", "ספורטמיקס",
    _nn(415, 14, 2.1, 0.0, 85, 62, 30, 5.5, 7),
    "ש‌י‌ב‌ו‌ל‌ת ש‌ו‌ע‌ל (3‌5‌%)‌, ת‌מ‌ר‌י‌ם (2‌5‌%)‌, ג‌ר‌ע‌י‌נ‌י‌ם‌, ס‌ו‌כ‌ ‌ר‌ ‌ח‌ ‌ו‌ ‌מ‌ ‌ג‌ ‌ר‌",
    ["שיבולת שועל (35%)", "תמרים (25%)", "גרעינים", "סוכר"],
    noise_profile="ocr_mild", noise_scenarios=["ocr_corruption:mild_zws_insertion"],
    expected_routing="snack_bar_granola", expected_conf_band="moderate",
    test_purpose="Mild OCR: zero-width space insertions between characters simulate OCR artifact",
    failure_risk=["OCR_DEGRADATION"],
    ingredient_text_quality="partial",
)
_C3["ingredient_text_quality"] = "partial"

_C4 = _make(
    "C4", "7290000003004",
    "קרקר כוסמין מלוח", "אנה",
    _nn(410, 12, 1.8, 0.0, 620, 66, 2.5, 4.5, 11),
    "קמח כוס מ1ן מ?אה (50%!), שמן זPת, מלח, שמN ים צמ@חיים, מ$ח",
    ["קמח כוסמין מלא (50%)", "שמן זית", "מלח", "שמנים צמחיים"],
    noise_profile="ocr_moderate", noise_scenarios=["ocr_corruption:moderate_char_substitution"],
    expected_routing="cracker", expected_conf_band="moderate",
    test_purpose="Moderate OCR: character substitutions in ingredient text simulate scanner artifacts",
    failure_risk=["OCR_DEGRADATION"],
    ingredient_text_quality="malformed",
)
_C4["ingredient_text_quality"] = "malformed"

_C5 = _make(
    "C5", "7290000003005",
    "יוגורט פירות יער 1.5% שומן", "תנובה",
    _nn(72, 1.5, 1.0, 0.0, 55, 11, 10, 0.0, 4.2),
    "חלב מפוסטר, פירות יער (תות, אוכמנית), סוכר, עמילן, מייצב, חומצת לקטית",
    ["חלב מפוסטר", "פירות יער"],  # truncated to 2 items (full list has 6)
    noise_profile="ingredient_truncation", noise_scenarios=["ingredient_list:truncated_to_2_items"],
    expected_routing="dairy_protein", expected_conf_band="moderate",
    test_purpose="Ingredient list truncated — stabilizers and additives invisible; NOVA likely under-estimated",
    failure_risk=["INGREDIENT_TRUNCATION"],
)

_C6 = _make(
    "C6", "7290000003006",
    "לחמי קריספ דגן מלא שיפון", "פינבו",
    _nn(330, 1.8, 0.3, 0.0, 480, 70, 0.8, 14, 11),
    "שי פ ון מ לא ( 9 8% ), מ ח מ צ ת ש י פ ו ן ( שיפון, מי ם, ש מ ר י ב ר ), מ ל ח",
    ["שיפון מלא (98%)", "מחמצת שיפון", "מלח"],
    noise_profile="ocr_severe", noise_scenarios=["ocr_corruption:severe_space_injection"],
    expected_routing="crispbread", expected_conf_band="low",
    test_purpose="Severe OCR: spaces injected throughout text. Hard anchor on name still routes correctly; ingredient signals degraded",
    failure_risk=["OCR_DEGRADATION"],
    ingredient_text_quality="corrupted",
)
_C6["ingredient_text_quality"] = "corrupted"

_C7 = _make(
    "C7", "7290000003007",
    "חטיף פירות ואגוזים טבעי", "רייזינבראן",
    _nn(380, 12, 1.5, 0.0, 60, 55, 38, 7.5, 6),
    "##$$תמ(רים)&& אג%%וזי לוז, @#!שקדים%%,  כ-ל-ו-ב-ר-ג-נ-ז, פרי יב{ש},,, שמן",
    ["תמרים", "אגוזי לוז", "שקדים"],
    noise_profile="ocr_severe", noise_scenarios=["ocr_corruption:garbled_with_symbols"],
    expected_routing="snack_bar_granola", expected_conf_band="low",
    test_purpose="Severe OCR: special characters throughout. Hebrew keywords still partially present but extraction unreliable",
    failure_risk=["OCR_DEGRADATION", "INGREDIENT_TRUNCATION"],
    ingredient_text_quality="corrupted",
)
_C7["ingredient_text_quality"] = "corrupted"

_C8 = _make(
    "C8", "7290000003008",
    "לחם קמח חיטה מלאה ושיפון", "בריד'ס",
    _nn(252, 2.1, 0.4, 0.0, 510, 48, 3.5, 6.8, 8.5),
    "XXXXXXXXXXXXXXXXXXXXXXXXX",  # OCR complete failure — unreadable
    [],
    noise_profile="ocr_complete_failure", noise_scenarios=["ocr_corruption:complete_unreadable"],
    expected_routing="bread", expected_conf_band="low",
    test_purpose="Complete OCR failure — ingredient text is garbage. Routing from name only",
    failure_risk=["OCR_DEGRADATION", "MISSINGNESS"],
    ingredient_text_quality="corrupted",
)
_C8["ingredient_text_quality"] = "corrupted"


# ---------------------------------------------------------------------------
# GROUP D — Routing instability (borderline categories)
# ---------------------------------------------------------------------------

_D1 = _make(
    "D1", "7290000004001",
    "גרנולה לבוקר עם פירות ואגוזים", "שחר",
    _nn(395, 13, 2.5, 0.0, 110, 60, 18, 6, 9),
    "שיבולת שועל (45%), אגוזים מעורבים (18%), פירות יבשים (15%), דבש, שמן קנולה, מלח",
    ["שיבולת שועל (45%)", "אגוזים מעורבים (18%)", "פירות יבשים (15%)", "דבש", "שמן קנולה", "מלח"],
    noise_profile="routing_instability", noise_scenarios=["routing:cereal_vs_snack_bar"],
    expected_routing="cereal",  # 'גרנולה לבוקר' anchor
    expected_conf_band="high",
    test_purpose="'גרנולה לבוקר' hard anchor routes to cereal; product is genuinely on the cereal/granola boundary. Test anchor dominance",
    failure_risk=["SEMANTIC_AMBIGUITY"],
)

_D2 = _make(
    "D2", "7290000004002",
    "יוגורט שתייה עשיר חלבון", "דנונה",
    _nn(82, 2.0, 1.3, 0.0, 65, 7.5, 6.8, 0.0, 8.5),
    "חלב מפוסטר, שמנת, חיידקי חמצת, ויטמין D",
    ["חלב מפוסטר", "שמנת", "חיידקי חמצת", "ויטמין D"],
    noise_profile="routing_instability", noise_scenarios=["routing:dairy_vs_beverage"],
    expected_routing="dairy_protein",
    expected_conf_band="high",
    test_purpose="'יוגורט שתייה' — contains 'יוגורט' (dairy anchor) AND 'שתייה' (beverage signal). Dairy anchor must prevail",
    failure_risk=["HYBRID_CONFLICT", "SEMANTIC_AMBIGUITY"],
)

_D3 = _make(
    "D3", "7290000004003",
    "קרקר שיבולת שועל מתוק עם ציפוי שוקולד", "גוברניץ",
    _nn(470, 22, 12, 0.5, 115, 60, 28, 3.5, 6),
    "קמח שיבולת שועל (40%), שוקולד חלב (22%) (סוכר, חמאת קקאו, חלב, קקאו), שמן דקלים, סוכר, מלח",
    ["קמח שיבולת שועל (40%)", "שוקולד חלב (22%)", "שמן דקלים", "סוכר", "מלח"],
    noise_profile="routing_instability", noise_scenarios=["routing:cracker_vs_snack_bar"],
    expected_routing="snack_bar_granola",
    expected_conf_band="moderate",
    test_purpose="Sweet chocolate-covered cracker — 'קרקר' anchor fires but product profile is more snack_bar. Test anchor vs signal tension",
    failure_risk=["HYBRID_CONFLICT", "SEMANTIC_AMBIGUITY"],
)

_D4 = _make(
    "D4", "7290000004004",
    "עוגיות שיבולת שועל וענבים ביסקוויט", "פרינגלס",
    _nn(430, 16, 7.5, 0.0, 280, 66, 25, 3.8, 7),
    "קמח חיטה, שיבולת שועל (25%), שמן צמחי מוקשה, סוכר, ענבים מיובשים, מלח, לציטין, חומר תפיחה",
    ["קמח חיטה", "שיבולת שועל (25%)", "שמן צמחי מוקשה", "סוכר", "ענבים מיובשים", "מלח", "לציטין", "חומר תפיחה"],
    noise_profile="routing_instability", noise_scenarios=["routing:snack_bar_vs_dessert"],
    expected_routing="snack_bar_granola",
    expected_conf_band="moderate",
    test_purpose="Oat biscuit — 'עוגיות' and 'ביסקוויט' both present; snack vs dessert ambiguity. Test if snack signals dominate",
    failure_risk=["SEMANTIC_AMBIGUITY", "HYBRID_CONFLICT"],
)

_D5 = _make(
    "D5", "7290000004005",
    "תערובת אגוזים וגרעינים קלויים", "שבת שלום",
    _nn(580, 48, 6.5, 0.0, 5, 18, 5, 7.5, 18),
    "שקדים (35%), אגוזי קשיו (25%), גרעיני חמניות, גרעיני דלעת, בוטנים קלויים",
    ["שקדים (35%)", "אגוזי קשיו (25%)", "גרעיני חמניות", "גרעיני דלעת", "בוטנים קלויים"],
    noise_profile="routing_instability", noise_scenarios=["routing:whole_food_fat_vs_snack_bar"],
    expected_routing="whole_food_fat",
    expected_conf_band="moderate",
    test_purpose="Nut mix — whole_food_fat vs snack_bar boundary. High fat% + name 'תערובת' should tip WFF",
    failure_risk=["SEMANTIC_AMBIGUITY", "CATEGORY_LEAKAGE"],
)

_D6 = _make(
    "D6", "7290000004006",
    "קרם יוגורט שוקולד פרמיום", "אלית",
    _nn(155, 7.5, 5.5, 0.0, 60, 19, 17, 0.5, 5),
    "חלב מפוסטר, שמנת (15%), סוכר, קקאו (3%), מייצב (קרגינן E407), חיידקי חמצת",
    ["חלב מפוסטר", "שמנת (15%)", "סוכר", "קקאו (3%)", "מייצב (קרגינן E407)", "חיידקי חמצת"],
    noise_profile="routing_instability", noise_scenarios=["routing:dairy_vs_dessert"],
    expected_routing="dairy_protein",
    expected_conf_band="moderate",
    test_purpose="'קרם יוגורט' — 'קרם' is a dessert signal; 'יוגורט' is a dairy anchor. Anchor must override 'קרם'",
    failure_risk=["HYBRID_CONFLICT"],
)

_D7 = _make(
    "D7", "7290000004007",
    "משקה סויה בטעם יוגורט", "אלפרו",
    _nn(60, 1.8, 0.3, 0.0, 80, 5.8, 4.5, 0.5, 3.5),
    "מים, סויה (7%), סוכר, תרכיז לימון, חיידקי חמצת, ויטמינים",
    ["מים", "סויה (7%)", "סוכר", "תרכיז לימון", "חיידקי חמצת", "ויטמינים"],
    noise_profile="routing_instability", noise_scenarios=["routing:beverage_vs_dairy"],
    expected_routing="beverage",
    expected_conf_band="moderate",
    test_purpose="'משקה סויה בטעם יוגורט' — plant milk brand + 'משקה' both point beverage. 'בטעם יוגורט' should be suppressed as flavor",
    failure_risk=["HYBRID_CONFLICT", "SEMANTIC_AMBIGUITY"],
)
_D7["brand"] = "אלפרו"

_D8 = _make(
    "D8", "7290000004008",
    "מוסלי פירות וגרעינים", "ברביקן",
    _nn(375, 8.5, 1.5, 0.0, 55, 67, 25, 7.5, 9),
    "שיבולת שועל מלאה (45%), פירות יבשים (20%), גרעינים (10%), דבש, שמן קוקוס מזוקק",
    ["שיבולת שועל מלאה (45%)", "פירות יבשים (20%)", "גרעינים (10%)", "דבש", "שמן קוקוס מזוקק"],
    noise_profile="routing_instability", noise_scenarios=["routing:muesli_anchor_cereal_vs_snack"],
    expected_routing="snack_bar_granola",  # 'מוסלי' anchor
    expected_conf_band="high",
    test_purpose="'מוסלי' anchor routes snack_bar_granola; test whether WFF signals from coconut oil contaminate routing",
    failure_risk=["CATEGORY_LEAKAGE"],
)


# ---------------------------------------------------------------------------
# GROUP E — Claim vs reality
# ---------------------------------------------------------------------------

_E1 = _make(
    "E1", "7290000005001",
    "חטיף חלבון גבוה 30g", "גולדר",
    _nn(390, 12, 4.5, 0.0, 280, 45, 15, 3.5, 8),  # claims 30g protein, has 8g
    "שיבולת שועל (40%), מי גבינה (10%), סוכר, שמן קנולה, מלח, חומר טעם",
    ["שיבולת שועל (40%)", "מי גבינה (10%)", "סוכר", "שמן קנולה", "מלח", "חומר טעם"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:protein_claim_vs_reality"],
    expected_routing="snack_bar_granola", expected_conf_band="high",
    test_purpose="Packaging says '30g protein' but nutrition panel shows 8g. Test that BSIP2 uses actual nutrition, not marketing",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["עשיר בחלבון", "30g חלבון"],
)
_E1["claims"] = ["עשיר בחלבון", "30g חלבון"]

_E2 = _make(
    "E2", "7290000005002",
    "לחם דגן מלא בריא", "אנגל",
    _nn(265, 3.5, 0.6, 0.0, 550, 50, 4.5, 4.5, 9),
    "קמח חיטה (68%), מים, קמח חיטה מלאה (12%), שמרים, שמן קנולה, מלח, גלוטן, סוכר",
    ["קמח חיטה (68%)", "מים", "קמח חיטה מלאה (12%)", "שמרים", "שמן קנולה", "מלח", "גלוטן", "סוכר"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:whole_grain_claim_refined_flour_first"],
    expected_routing="bread", expected_conf_band="high",
    test_purpose="Claims 'whole grain' but refined flour (68%) is first ingredient. GSS should be low; bakery semantics should discount",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["דגן מלא"],
)
_E2["claims"] = ["דגן מלא"]

_E3 = _make(
    "E3", "7290000005003",
    "חטיף טבעי 100% טבע", "ביו-נייטשר",
    _nn(440, 22, 8.5, 0.5, 220, 52, 18, 4.5, 8),
    "שיבולת שועל, שוקולד חלב (E471, E476), שמן דקלים, סוכר, גלוקוז, מולסה, שמרי בירה, E250, E220, E202, לציטין (E322)",
    ["שיבולת שועל", "שוקולד חלב", "שמן דקלים", "סוכר", "גלוקוז", "מולסה", "שמרי בירה", "E250", "E220", "E202", "לציטין (E322)"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:natural_claim_with_additives"],
    expected_routing="snack_bar_granola", expected_conf_band="high",
    test_purpose="'100% natural' claim but 5+ additive E-numbers. Additive_quality should drop significantly",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["100% טבעי", "ללא מלאכותי"],
)
_E3["claims"] = ["100% טבעי", "ללא מלאכותי"]

_E4 = _make(
    "E4", "7290000005004",
    "יוגורט ללא תוספת סוכר עם פירות", "תנובה",
    _nn(78, 2.5, 1.8, 0.0, 50, 9.5, 9.2, 0.0, 4.5),
    "חלב מפוסטר, רכז תפוחים (8%), רכז פרות יער, מחית פטל, חיידקי חמצת",
    ["חלב מפוסטר", "רכז תפוחים (8%)", "רכז פרות יער", "מחית פטל", "חיידקי חמצת"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:no_sugar_with_concentrates"],
    expected_routing="dairy_protein", expected_conf_band="high",
    test_purpose="'No added sugar' but contains 3 fruit concentrates. SC classification should detect SC-4; cap behavior tested",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["ללא תוספת סוכר"],
)
_E4["claims"] = ["ללא תוספת סוכר"]

_E5 = _make(
    "E5", "7290000005005",
    "לחם מחמצת ביתי", "מגדל",
    _nn(255, 3.2, 0.6, 0.0, 560, 49, 3.5, 5.5, 9),
    "קמח חיטה (72%), מים, שמרים (2%), מלח, חומץ (1%), שמן קנולה, גלוטן",
    ["קמח חיטה (72%)", "מים", "שמרים (2%)", "מלח", "חומץ (1%)", "שמן קנולה", "גלוטן"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:sourdough_no_fermentation"],
    expected_routing="bread", expected_conf_band="high",
    test_purpose="Name says 'מחמצת' but ingredients list has commercial yeast + vinegar (not sourdough). Bakery semantics should classify as sourdough_theater",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["מחמצת"],
)

_E6 = _make(
    "E6", "7290000005006",
    "לחם סיבים גבוה עשיר בסיבים 8g", "שפע",
    _nn(220, 2.8, 0.4, 0.0, 520, 40, 2, 8.5, 9.5),
    "קמח חיטה (55%), מים, אינולין (7%), גסטרוגן (פסיליום), שמרים, מלח, שמן, E422, סוכר",
    ["קמח חיטה (55%)", "מים", "אינולין (7%)", "גסטרוגן (פסיליום)", "שמרים", "מלח", "שמן", "E422", "סוכר"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:high_fiber_isolated_sources"],
    expected_routing="bread", expected_conf_band="high",
    test_purpose="Claims '8g fiber' but all fiber from inulin+psyllium on refined base. Synthesis fiber discount should fire",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["עשיר בסיבים", "8g סיבים"],
)
_E6["claims"] = ["עשיר בסיבים", "8g סיבים"]

_E7 = _make(
    "E7", "7290000005007",
    "קרקר קל קלוריות דיאטה", "שדמות",
    _nn(455, 18, 3.5, 0.0, 720, 64, 2, 3.5, 8),  # 455kcal is not 'light'
    "קמח חיטה (60%), שמן קנולה, מלח, שמרים, סוכר",
    ["קמח חיטה (60%)", "שמן קנולה", "מלח", "שמרים", "סוכר"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:light_high_calorie_density"],
    expected_routing="cracker", expected_conf_band="high",
    test_purpose="Claims 'light/diet' but 455kcal/100g. Calorie density score should not be relaxed by misleading label",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["קלוריות מופחתות", "מוצר לדיאטה"],
)
_E7["claims"] = ["קלוריות מופחתות", "מוצר לדיאטה"]

_E8 = _make(
    "E8", "7290000005008",
    "חטיף ג'ל אנרגיה טבעי ספורט", "גו-נייטשר",
    _nn(280, 0.5, 0.1, 0.0, 55, 68, 65, 0.5, 1.5),  # 65g sugar — extremely high
    "סירופ גלוקוז-פרוקטוז (42%), מיץ תפוחים מרוכז, ג'ל מלתודקסטרין, מלח ים, ויטמין C",
    ["סירופ גלוקוז-פרוקטוז (42%)", "מיץ תפוחים מרוכז", "ג'ל מלתודקסטרין", "מלח ים", "ויטמין C"],
    noise_profile="claim_vs_reality", noise_scenarios=["claim:natural_energy_high_sugar"],
    expected_routing="snack_bar_granola", expected_conf_band="high",
    test_purpose="'Natural energy gel' with 65g/100g sugar. Multiple sugar guardrails should fire. Tests SC classification with glucose-fructose syrup",
    failure_risk=["WEAK_SUPPRESSION"],
    claims=["100% טבעי", "אנרגיה מיידית"],
)
_E8["claims"] = ["100% טבעי", "אנרגיה מיידית"]


# ---------------------------------------------------------------------------
# GROUP F — Missing identity fields
# ---------------------------------------------------------------------------

_F1 = _make(
    "F1", None,  # missing barcode
    "שיבולת שועל אורגנית מלאה", "אורגני פלוס",
    _nn(375, 7.5, 1.5, 0.0, 5, 61, 1.5, 10, 13),
    "שיבולת שועל אורגנית מלאה (100%)",
    ["שיבולת שועל אורגנית מלאה (100%)"],
    noise_profile="missing_identity", noise_scenarios=["missing_identity:barcode_null"],
    expected_routing="cereal", expected_conf_band="high",
    test_purpose="Barcode is null — identity rests on name+brand only. Confidence penalized for missing barcode",
    failure_risk=["MISSINGNESS"],
)

_F2 = _make(
    "F2", "7290000006002",
    "טחינה גולמית 100%", "",  # missing brand
    _nn(570, 48, 7.0, 0.0, 40, 25, 0.5, 10, 20),
    "שומשום (100%)",
    ["שומשום (100%)"],
    noise_profile="missing_identity", noise_scenarios=["missing_identity:brand_empty"],
    expected_routing="whole_food_fat", expected_conf_band="high",
    test_purpose="Brand is empty — 'טחינה' hard anchor still fires; test that missing brand doesn't break routing",
    failure_risk=["MISSINGNESS"],
)

_F3 = _make(
    "F3", "7290000006003",
    "מוצר דגנים לבוקר", "כוכב",  # vague name, no category hint
    _nn(360, 2.5, 0.5, 0.0, 610, 76, 12, 4, 8),
    "קמח תירס, סוכר, מלח, ויטמינים",
    ["קמח תירס", "סוכר", "מלח", "ויטמינים"],
    noise_profile="missing_identity", noise_scenarios=["missing_identity:vague_name"],
    expected_routing="cereal", expected_conf_band="moderate",
    test_purpose="Vague name 'מוצר דגנים לבוקר' — no hard anchor; signal scoring must carry the routing",
    failure_risk=["SEMANTIC_AMBIGUITY"],
)

_F4 = _make(
    "F4", "7290000006004",
    "", "תמרסל",  # empty name
    _nn(420, 14, 2.0, 0.0, 180, 65, 24, 5, 8),
    "שיבולת שועל (50%), תמרים (20%), אגוזים, שמן קוקוס, דבש",
    ["שיבולת שועל (50%)", "תמרים (20%)", "אגוזים", "שמן קוקוס", "דבש"],
    noise_profile="missing_identity", noise_scenarios=["missing_identity:name_empty"],
    expected_routing="default", expected_conf_band="low",
    test_purpose="Product name is empty — no anchors can fire; routing based on signals from ingredient text only",
    failure_risk=["MISSINGNESS", "SEMANTIC_AMBIGUITY"],
)

_F5 = _make(
    "F5", "7290000006005",
    "חטיף דגנים בסיסי", "כללי",
    _nn(400, 10, 2.0, 0.0, 350, 68, 14, 4.5, 8),
    "שיבולת שועל, סוכר, שמן, מלח",
    ["שיבולת שועל", "סוכר", "שמן", "מלח"],
    noise_profile="missing_identity", noise_scenarios=["missing_identity:low_trust_single_source"],
    expected_routing="snack_bar_granola", expected_conf_band="moderate",
    test_purpose="Low trust level (single-source, unvalidated). Confidence reduction for trust=low",
    failure_risk=["MISSINGNESS"],
    canonical_trust_level="low",
    canonical_trust_score=0.45,
)
_F5["canonical_trust_level"] = "low"
_F5["canonical_trust_score"]  = 0.45


# ---------------------------------------------------------------------------
# GROUP G — Data consistency failures
# ---------------------------------------------------------------------------

_G1 = _make(
    "G1", "7290000007001",
    "חטיף מלטי-דגן בריא", "ברנד",
    _nn(380, 8.5, 2.0, 0.0, 160, 30, 45, 5, 9),  # sugar=45 > carbs=30: impossible
    "שיבולת שועל, סוכר, דבש, אגוזים, מלח",
    ["שיבולת שועל", "סוכר", "דבש", "אגוזים", "מלח"],
    noise_profile="data_inconsistency", noise_scenarios=["consistency:sugar_greater_than_carbs"],
    expected_routing="snack_bar_granola", expected_conf_band="low",
    test_purpose="sugar(45g) > carbs(30g): physically impossible. Critical consistency failure should trigger RETAILER_INCONSISTENCY",
    failure_risk=["RETAILER_INCONSISTENCY"],
    nutrition_consistency_status="suspicious",
)
_G1["nutrition_consistency_status"] = "suspicious"

_G2 = _make(
    "G2", "7290000007002",
    "גבינה צהובה 30%", "תנובה",
    _nn(360, 28, 35, 0.0, 680, 1.5, 0.5, 0.0, 25),  # sat_fat=35 > fat=28: impossible
    "חלב מפוסטר, מלח, חיידקי חמצת, נוגד חמצון (לקטט)",
    ["חלב מפוסטר", "מלח", "חיידקי חמצת", "נוגד חמצון (לקטט)"],
    noise_profile="data_inconsistency", noise_scenarios=["consistency:satfat_greater_than_fat"],
    expected_routing="dairy_protein", expected_conf_band="low",
    test_purpose="sat_fat(35g) > fat(28g): physically impossible. Critical consistency failure in dairy product",
    failure_risk=["RETAILER_INCONSISTENCY"],
    nutrition_consistency_status="suspicious",
)
_G2["nutrition_consistency_status"] = "suspicious"

_G3 = _make(
    "G3", "7290000007003",
    "אבקת חלבון ספורט וניל", "מקסי",
    _nn(1800, 5, 1.5, 0.0, 350, 45, 12, 2, 72),  # 1800 kcal: implausible for solid
    "מי גבינה, קקאו, ממתיק (סוכרלוזה), ויטמינים, מינרלים",
    ["מי גבינה", "קקאו", "ממתיק (סוכרלוזה)", "ויטמינים", "מינרלים"],
    noise_profile="data_inconsistency", noise_scenarios=["consistency:kcal_outside_plausible_range"],
    expected_routing="snack_bar_granola", expected_conf_band="low",
    test_purpose="1800 kcal/100g is outside plausible solid food range (700 ceiling). kcal_plausible check should fire",
    failure_risk=["RETAILER_INCONSISTENCY"],
    nutrition_consistency_status="warnings",
)
_G3["nutrition_consistency_status"] = "warnings"

_G4 = _make(
    "G4", "7290000007004",
    "שייק חלבון תחליף ארוחה", "קמפו",
    _nn(600, 5, 8, 0.0, 1200, 20, 55, 0.5, 30),  # sat_fat > fat, sugar > carbs, sodium very high
    "מי גבינה, ממתיקים, ויטמינים",
    ["מי גבינה", "ממתיקים", "ויטמינים"],
    noise_profile="data_inconsistency", noise_scenarios=["consistency:multiple_failures"],
    expected_routing="snack_bar_granola", expected_conf_band="insufficient_context",
    test_purpose="Multiple simultaneous consistency failures. System should reach INSUFFICIENT or very low confidence",
    failure_risk=["RETAILER_INCONSISTENCY", "MISSINGNESS"],
    nutrition_consistency_status="suspicious",
)
_G4["nutrition_consistency_status"] = "suspicious"
_G4["normalized_nutrition_per_100g"]["fat_saturated_g"] = 8   # sat > fat OK here (both valid), but sugar > carbs
_G4["normalized_nutrition_per_100g"]["sugars_g"]        = 55  # > carbs=20


# ---------------------------------------------------------------------------
# GROUP H — Hybrid / edge cases
# ---------------------------------------------------------------------------

_H1 = _make(
    "H1", "7290000008001",
    "חטיפי גרנולה לבוקר ולחטיף", "ויטה",
    _nn(410, 14, 3.5, 0.0, 125, 60, 20, 7.5, 9.5),
    "שיבולת שועל מלאה (52%), אגוזים, פירות יבשים, דבש, שמן קנולה",
    ["שיבולת שועל מלאה (52%)", "אגוזים", "פירות יבשים", "דבש", "שמן קנולה"],
    noise_profile="hybrid_product", noise_scenarios=["hybrid:cereal_and_snack_bar"],
    expected_routing="snack_bar_granola",
    expected_conf_band="high",
    test_purpose="Genuinely dual-use granola — marketed as both breakfast cereal and snack. 'גרנולה לבוקר' in name should anchor to cereal; without it, snack signals dominate",
    failure_risk=["HYBRID_CONFLICT"],
)

_H2 = _make(
    "H2", "7290000008002",
    "לחם גבינה ועשבי תיבול", "בייקרס",
    _nn(285, 8.5, 4.5, 0.0, 580, 42, 2.5, 3.5, 11),
    "קמח חיטה (55%), גבינה צהובה (15%), מים, שמרים, מלח, שמן קנולה, עשבי תיבול",
    ["קמח חיטה (55%)", "גבינה צהובה (15%)", "מים", "שמרים", "מלח", "שמן קנולה", "עשבי תיבול"],
    noise_profile="hybrid_product", noise_scenarios=["hybrid:bread_with_dairy_ingredient"],
    expected_routing="bread",
    expected_conf_band="high",
    test_purpose="Bread with 15% cheese — 'לחם' anchor fires. Dairy ingredient (cheese) in text must not trigger dairy_protein routing",
    failure_risk=["CATEGORY_LEAKAGE"],
)

_H3 = _make(
    "H3", "7290000008003",
    "ממרח שקדים ותמרים", "רוגל",
    _nn(480, 30, 3.5, 0.0, 20, 38, 28, 7, 12),
    "שקדים (52%), תמרים (35%), שמן קוקוס, מלח",
    ["שקדים (52%)", "תמרים (35%)", "שמן קוקוס", "מלח"],
    noise_profile="hybrid_product", noise_scenarios=["hybrid:spread_vs_whole_food_fat"],
    expected_routing="whole_food_fat",
    expected_conf_band="high",
    test_purpose="'ממרח שקדים' — spread signal + nut content. Test whether 'ממרח' is correctly weighted with nut anchor",
    failure_risk=["SEMANTIC_AMBIGUITY"],
)

_H4 = _make(
    "H4", "7290000008004",
    "אבקת שייק חלבון שוקולד", "טרמינייטור",
    _nn(390, 6, 2.5, 0.0, 420, 45, 10, 4, 35),
    "מי גבינה (60%), קקאו, מלתודקסטרין, ממתיק (סוכרלוזה E955), חומצה אסקורבית, ויטמינים, מינרלים",
    ["מי גבינה (60%)", "קקאו", "מלתודקסטרין", "ממתיק (סוכרלוזה E955)", "חומצה אסקורבית", "ויטמינים", "מינרלים"],
    noise_profile="hybrid_product", noise_scenarios=["hybrid:protein_powder_category_gap"],
    expected_routing="snack_bar_granola",
    expected_conf_band="moderate",
    test_purpose="Protein powder — no specific category for this product type. Routes to snack_bar_granola by default; tests ONTOLOGY_GAP exposure",
    failure_risk=["ONTOLOGY_GAP", "HYBRID_CONFLICT"],
)


# ---------------------------------------------------------------------------
# Assemble corpus
# ---------------------------------------------------------------------------

CORPUS = [
    # Group A — Clean baselines
    _A1, _A2, _A3, _A4, _A5,
    # Group B — Missing nutrition
    _B1, _B2, _B3, _B4, _B5, _B6, _B7, _B8,
    # Group C — Missing/corrupted ingredients
    _C1, _C2, _C3, _C4, _C5, _C6, _C7, _C8,
    # Group D — Routing instability
    _D1, _D2, _D3, _D4, _D5, _D6, _D7, _D8,
    # Group E — Claim vs reality
    _E1, _E2, _E3, _E4, _E5, _E6, _E7, _E8,
    # Group F — Missing identity
    _F1, _F2, _F3, _F4, _F5,
    # Group G — Data consistency failures
    _G1, _G2, _G3, _G4,
    # Group H — Hybrid/edge cases
    _H1, _H2, _H3, _H4,
]


def main():
    output = {
        "corpus_id":    "robustness_corpus_001",
        "sprint":       "BSIP2 Robustness & Uncertainty Sprint v1",
        "created":      "2026-05-25",
        "product_count": len(CORPUS),
        "groups": {
            "A_clean_baselines":         5,
            "B_missing_nutrition":       8,
            "C_missing_corrupted_ingredients": 8,
            "D_routing_instability":     8,
            "E_claim_vs_reality":        8,
            "F_missing_identity":        5,
            "G_data_consistency_failures": 4,
            "H_hybrid_edge_cases":       4,
        },
        "products": CORPUS,
    }
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Corpus written: {OUTPUT_PATH} ({len(CORPUS)} products)")


if __name__ == "__main__":
    main()
