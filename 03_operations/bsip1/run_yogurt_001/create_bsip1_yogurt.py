"""
BSIP1 Yogurt Product Generator — run_yogurt_001
45 canonical products across 12 subtype groups.
Designed to expose: routing failures, NOVA1 floor vs red-label cap tension,
vanilla = NOVA4 bug, sat_fat penalty on natural full-fat, sweetener caps,
plant-based routing to dairy_protein, drinkable yogurt routing ambiguity.
Output: C:\Bari\03_operations\bsip1\run_yogurt_001\output\
"""
import json
import pathlib

OUTPUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output")


def _p(barcode, name_he, brand, subtype,
       kcal, fat, sat_fat, sodium, carbs, sugar, fiber, protein,
       ingredients_text, ingredients_list,
       allergens=None, claims=None,
       trust_score=0.85, trust_level="high"):
    pid = f"bsip1_{barcode}"
    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "canonical_name_en": None,
        "brand": brand,
        "package_size_g": None,
        "unit_count": None,
        "unit_size_g": None,
        "serving_size_g": None,
        "country_of_origin": "ישראל",
        "kosher_certification": None,
        "image_url": None,
        "source_retailers": ["yohananof"],
        "normalized_nutrition_per_100g": {
            "energy_kcal": float(kcal),
            "fat_g": float(fat),
            "fat_saturated_g": float(sat_fat),
            "fat_trans_g": 0.0,
            "sodium_mg": float(sodium),
            "carbohydrates_g": float(carbs),
            "sugars_g": float(sugar),
            "dietary_fiber_g": float(fiber),
            "protein_g": float(protein),
            "cholesterol_mg": None,
        },
        "energy_source_unit": "kcal",
        "ingredients_text_he": ingredients_text,
        "ingredients_list": ingredients_list,
        "allergens_contains": allergens or [],
        "allergens_may_contain": [],
        "claims": claims or [],
        "confidence": {
            "identity_confidence": "high",
            "barcode_confidence": "confirmed",
            "nutrition_confidence": "confirmed_per_100g",
            "matched_by": "barcode_single_source",
            "observation_count": 1,
        },
        "barcode_validation_status": "retailer_confirmed",
        "barcode_confidence_reason": "Scraped from Yohananof on 2026-05-18.",
        "nutrition_basis_claimed": "ל-100 גרם",
        "nutrition_basis_detected": "per_100g",
        "nutrition_consistency_status": "consistent",
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality": "clean",
        "ingredient_warnings": [],
        "canonical_trust_score": trust_score,
        "canonical_trust_level": trust_level,
        "canonical_risk_flags": ["single_source_only"],
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields": [],
        "inferred_fields": [],
        "audit_ref": f"bsip1_audit_{barcode}.json",
        "bsip_yogurt_subtype": subtype,
    }


PRODUCTS = [

    # ── GROUP 1: Plain Natural Yogurt (NOVA 1 targets) ──────────────────────────
    # ingredients_list = ["חלב מפוסטר"] only — cultures in text → NOVA1 fast path
    # Expected: NOVA1, floor=85, A grade (unless red label fires)

    _p("7290200000001", "יוגורט טבעי 1.5% שומן", "טנובה", "plain_natural",
       60, 1.5, 1.0, 50, 4.5, 4.5, 0.0, 5.0,
       "חלב מפוסטר, תרבויות חיות (לקטובציל אסידופילוס, ביפידובקטריום)",
       ["חלב מפוסטר"],
       allergens=["חלב"], claims=["פרוביוטיקה"]),

    _p("7290200000002", "יוגורט טבעי 3% שומן", "טנובה", "plain_natural",
       75, 3.0, 2.0, 55, 4.8, 4.8, 0.0, 4.8,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),

    _p("7290200000003", "יוגורט טבעי 5% שומן יוטבתה", "יוטבתה", "plain_natural",
       100, 5.0, 3.3, 55, 4.5, 4.5, 0.0, 4.5,
       "חלב מפוסטר, שמנת, תרבויות חיות",
       ["חלב מפוסטר", "שמנת"],
       allergens=["חלב"]),
    # 2 ingredients → not NOVA1; NOVA2; no red labels

    _p("7290200000004", "יוגורט עיזים 9% שומן", "עיזי פסגה", "plain_natural",
       130, 9.0, 6.0, 55, 3.8, 3.8, 0.0, 4.5,
       "חלב עיזים מפוסטר, תרבויות חיות",
       ["חלב עיזים מפוסטר"],
       allergens=["חלב"]),
    # sat_fat=6.0g > 5.0 → red_label_sat_fat → cap=55 → C
    # NOVA1 (single ingredient) but cap overrides floor — stress test #9

    # ── GROUP 2: Greek Yogurt ───────────────────────────────────────────────────

    _p("7290200000005", "יוגורט יווני 0% שומן", "דנונה", "greek",
       57, 0.2, 0.1, 45, 4.0, 4.0, 0.0, 9.0,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # fat=0.2g → fat_quality structural emptiness gate → neutral 50; NOVA1; high protein

    _p("7290200000006", "יוגורט יווני 2% שומן", "דנונה", "greek",
       75, 2.0, 1.4, 45, 4.2, 4.2, 0.0, 8.5,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),

    _p("7290200000007", "יוגורט יווני 5% שומן", "דנונה", "greek",
       120, 5.0, 3.5, 45, 4.5, 4.5, 0.0, 8.0,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),

    _p("7290200000008", "יוגורט יווני 10% שומן פאג'", "פאג'", "greek",
       176, 10.0, 6.5, 40, 4.0, 4.0, 0.0, 8.5,
       "חלב מפוסטר, שמנת, תרבויות חיות",
       ["חלב מפוסטר", "שמנת"],
       allergens=["חלב"]),
    # sat_fat=6.5g → red_label_sat_fat → cap=55 → C — stress test #9 (full-fat Greek penalized)

    # ── GROUP 3: Probiotic Drinks (routing stress tests) ────────────────────────

    _p("7290200000009", "אקטימל משקה חלב פרוביוטי", "דנונה", "probiotic_drink",
       78, 1.5, 1.0, 55, 12.5, 12.5, 0.0, 3.5,
       "חלב מפוסטר, סוכר, תרבויות חיות (L. Casei), חומרי טעם וריח",
       ["חלב מפוסטר", "סוכר", "תרבויות חיות", "חומרי טעם וריח"],
       allergens=["חלב"]),
    # "משקה"(0.90) > "חלב"(0.70) → routes to BEVERAGE (error)
    # kcal=78 on beverage table → score=30 (devastating)
    # חומרי טעם וריח → flavor_enhancer → NOVA4

    _p("7290200000010", "יוגורט אקטיביה פרוביוטי", "דנונה", "probiotic_drink",
       88, 2.5, 1.7, 55, 13.5, 11.5, 0.0, 4.5,
       "חלב מפוסטר, שמנת, סוכר, עמילן שינוי, תרבויות חיות (בידפידוס)",
       ["חלב מפוסטר", "שמנת", "סוכר", "עמילן שינוי", "תרבויות חיות"],
       allergens=["חלב"]),
    # "יוגורט" → dairy_protein correct routing; עמילן שינוי → NOVA3 signal

    _p("7290200000011", "לבן שתייה 3% שומן", "טנובה", "probiotic_drink",
       70, 3.0, 2.0, 60, 4.5, 4.5, 0.0, 3.2,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # "שתייה"(0.90) > "לבן"(0.60) → routes to BEVERAGE (error)
    # NOVA1 (single ingredient) but routed to beverage → kcal=70 → score=50 on beverage table

    _p("7290200000012", "קפיר 2% שומן", "טנובה", "kefir",
       60, 2.0, 1.4, 50, 4.5, 4.5, 0.0, 3.5,
       "חלב מפוסטר, תרבויות קפיר",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # "קפיר"(0.95) → dairy_protein correct routing; NOVA1 → floor=85 → A

    # ── GROUP 4: Fruit Yogurt (NOVA 2-3) ────────────────────────────────────────

    _p("7290200000013", "יוגורט תות 1.5% שומן", "טנובה", "fruit",
       78, 1.5, 1.0, 55, 11.5, 10.5, 0.5, 4.5,
       "חלב מפוסטר, תות שדה 12%, סוכר, תרבויות חיות",
       ["חלב מפוסטר", "תות שדה 12%", "סוכר", "תרבויות חיות"],
       allergens=["חלב"]),

    _p("7290200000014", "יוגורט אוכמניות עם מייצב", "דנונה", "fruit",
       88, 2.0, 1.4, 60, 14.0, 12.0, 0.5, 4.0,
       "חלב מפוסטר, אוכמניות 8%, סוכר, מייצב (E-440), תרבויות חיות, חומרי טעם וריח",
       ["חלב מפוסטר", "אוכמניות 8%", "סוכר", "מייצב (E-440)", "תרבויות חיות", "חומרי טעם וריח"],
       allergens=["חלב"]),
    # חומרי טעם וריח → flavor_enhancer +3 → NOVA4 cap=68

    _p("7290200000015", "יוגורט פירות יוטבתה 1.5%", "יוטבתה", "fruit",
       82, 1.5, 1.0, 55, 13.0, 11.0, 0.5, 4.0,
       "חלב מפוסטר, פירות אמיתיים 10%, סוכר, עמילן שינוי, תרבויות חיות",
       ["חלב מפוסטר", "פירות אמיתיים 10%", "סוכר", "עמילן שינוי", "תרבויות חיות"],
       allergens=["חלב"]),

    _p("7290200000016", "יוגורט אפרסק עתיר סוכר", "יוטבתה", "fruit",
       105, 2.0, 1.4, 65, 18.5, 19.0, 0.3, 3.5,
       "חלב מפוסטר, אפרסק 8%, סוכר, מייצב (E-440), תרבויות חיות, חומרי טעם וריח",
       ["חלב מפוסטר", "אפרסק 8%", "סוכר", "מייצב (E-440)", "תרבויות חיות", "חומרי טעם וריח"],
       allergens=["חלב"]),
    # sugar=19g > 17.5 → red_label_sugar → cap=55 → C (binding)

    # ── GROUP 5: Kids Yogurt (NOVA 3-4) ─────────────────────────────────────────

    _p("7290200000017", "יוגורט ילדים תות ואניל", "טנובה", "kids",
       90, 2.0, 1.4, 70, 14.5, 13.0, 0.0, 4.0,
       "חלב מפוסטר, תות 10%, סוכר, ואניל, צבע (E-129), מייצב (E-1442), תרבויות חיות",
       ["חלב מפוסטר", "תות 10%", "סוכר", "ואניל", "צבע (E-129)", "מייצב (E-1442)", "תרבויות חיות"],
       allergens=["חלב"]),
    # ואניל → flavor_enhancer +3; E-129 → color +2 → nova4_score=5 → NOVA4 solid

    _p("7290200000018", "יוגורט ילדים שוקולד", "שטראוס", "kids",
       115, 3.5, 2.3, 80, 17.5, 16.0, 0.5, 4.5,
       "חלב מפוסטר, ממרח שוקולד 15% (סוכר, שמן דקל, אבקת קקאו, ונילין, מייצב E-322), סוכר, מייצב (E-440), חומרי טעם וריח, תרבויות חיות",
       ["חלב מפוסטר", "ממרח שוקולד 15%", "סוכר", "מייצב (E-440)", "חומרי טעם וריח", "תרבויות חיות"],
       allergens=["חלב", "סויה"]),
    # ונילין → flavor_enhancer; E-322 → emulsifier; additive_count high → NOVA4

    _p("7290200000019", "יוגורט ילדים תות טבעי", "יוטבתה", "kids",
       82, 1.5, 1.0, 65, 13.0, 11.5, 0.0, 4.0,
       "חלב מפוסטר, תות שדה 10%, סוכר, תרבויות חיות",
       ["חלב מפוסטר", "תות שדה 10%", "סוכר", "תרבויות חיות"],
       allergens=["חלב"]),
    # Clean — no additives → NOVA2; expected B

    _p("7290200000020", "שתייה חלב לילדים פרוביוטיקה", "טנובה", "kids",
       78, 2.0, 1.4, 60, 12.0, 10.0, 0.0, 3.5,
       "חלב מפוסטר, סוכר, תרבויות חיות, חומרי טעם וריח",
       ["חלב מפוסטר", "סוכר", "תרבויות חיות", "חומרי טעם וריח"],
       allergens=["חלב"]),
    # "שתייה"(0.90) > "חלב"(0.70) → routes to BEVERAGE (error)
    # חומרי טעם וריח → NOVA4; kcal=78 on beverage table → score=30

    # ── GROUP 6: Protein Yogurt (NOVA 3-4) ──────────────────────────────────────

    _p("7290200000021", "יוגורט חלבון 20 פרי יער", "דנונה", "protein",
       90, 0.5, 0.3, 55, 5.0, 4.5, 0.0, 18.0,
       "חלב מפוסטר, פרי יער 5%, חלבון מי גבינה, תרבויות חיות",
       ["חלב מפוסטר", "פרי יער 5%", "חלבון מי גבינה", "תרבויות חיות"],
       allergens=["חלב"], claims=["עשיר בחלבון"]),
    # חלבון מי גבינה → protein isolate marker; no flavor_enhancer → NOVA2-3; good protein

    _p("7290200000022", "יוגורט חלבון ואניל", "דנונה", "protein",
       85, 0.3, 0.2, 60, 6.0, 5.0, 0.0, 15.0,
       "חלב מפוסטר, חלבון מי גבינה, ואניל, ממתיק (סטביה), תרבויות חיות",
       ["חלב מפוסטר", "חלבון מי גבינה", "ואניל", "ממתיק (סטביה)", "תרבויות חיות"],
       allergens=["חלב"], claims=["עשיר בחלבון", "ללא סוכר"]),
    # ואניל → flavor_enhancer +3; סטביה → sweetener +2 → nova4_score=5 → NOVA4
    # sweetener_cap=70; NOVA4_cap=68 → binding=68 (vanilla bug: natural vanilla = NOVA4)

    _p("7290200000023", "יוגורט יווני חלבון 18 טהור", "יוטבתה", "protein",
       80, 0.5, 0.3, 45, 4.0, 3.5, 0.0, 18.0,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"], claims=["עשיר בחלבון"]),
    # NOVA1 (single ingredient!); protein=18g → S-tier candidate

    _p("7290200000024", "יוגורט חלבון ממרח שוקולד", "שטראוס", "protein",
       130, 4.5, 3.0, 80, 12.0, 9.0, 0.5, 12.0,
       "חלב מפוסטר, ממרח שוקולד (סוכר, שמן דקל, קקאו, ונילין, מייצב E-322), חלבון מי גבינה, תרבויות חיות",
       ["חלב מפוסטר", "ממרח שוקולד", "חלבון מי גבינה", "תרבויות חיות"],
       allergens=["חלב", "סויה"]),
    # ונילין → flavor_enhancer +3; E-322 → emulsifier +1 → nova4_score=4 → NOVA4

    # ── GROUP 7: Skyr (NOVA 1-2) ─────────────────────────────────────────────────

    _p("7290200000025", "סקיר טבעי 0.2% שומן", "ארלה", "skyr",
       60, 0.2, 0.1, 40, 3.5, 3.5, 0.0, 11.0,
       "חלב מפוסטר, תרבויות חיות, מיצוי קיבה",
       ["חלב מפוסטר", "תרבויות חיות", "מיצוי קיבה"],
       allergens=["חלב"]),
    # ing_count=3 → not NOVA1; clean → NOVA2; high protein; expected A or B

    _p("7290200000026", "סקיר ואניל", "ארלה", "skyr",
       65, 0.2, 0.1, 40, 5.0, 4.5, 0.0, 11.0,
       "חלב מפוסטר, תרבויות חיות, מיצוי קיבה, ואניל, ממתיק (אצסולפם K, אספרטם)",
       ["חלב מפוסטר", "תרבויות חיות", "מיצוי קיבה", "ואניל", "ממתיק (אצסולפם K, אספרטם)"],
       allergens=["חלב", "פנילאלנין"]),
    # ואניל → flavor_enhancer +3; אספרטם → sweetener +2 → nova4_score=5 → NOVA4
    # Nutritionally clean but NOVA4 cap=68 — vanilla bug on skyr confirms generality

    _p("7290200000027", "סקיר תות", "ארלה", "skyr",
       80, 0.2, 0.1, 45, 11.0, 9.0, 0.5, 10.0,
       "חלב מפוסטר, תות 12%, סוכר, תרבויות חיות, מיצוי קיבה, מייצב (E-440)",
       ["חלב מפוסטר", "תות 12%", "סוכר", "תרבויות חיות", "מיצוי קיבה", "מייצב (E-440)"],
       allergens=["חלב"]),
    # Stabilizer, no flavor_enhancer → NOVA2-3; expected B

    # ── GROUP 8: Dessert / Mousse Yogurt (NOVA 4, high penalties) ───────────────

    _p("7290200000028", "יוגורט מולר קורנר דבש אגוזים", "מולר", "dessert",
       165, 5.5, 3.5, 80, 24.0, 20.0, 0.5, 5.0,
       "יוגורט (חלב מפוסטר, תרבויות חיות), דבש 12%, אגוזים 8%, סוכר, חומרי טעם וריח, מייצב (E-1442)",
       ["יוגורט (חלב מפוסטר, תרבויות חיות)", "דבש 12%", "אגוזים 8%", "סוכר", "חומרי טעם וריח", "מייצב (E-1442)"],
       allergens=["חלב", "אגוזים"]),
    # sugar=20g → red_label_sugar → cap=55; חומרי טעם וריח → NOVA4 cap=68 → binding=55

    _p("7290200000029", "מוס שוקולד יוגורט", "שטראוס", "dessert",
       185, 8.0, 5.2, 90, 23.0, 21.0, 1.0, 4.5,
       "חלב מפוסטר, שמנת, ממרח שוקולד (סוכר, שמן דקל, קקאו 8%, ונילין, מייצב E-322), סוכר, מייצב (E-440), חומרי טעם וריח, תרבויות חיות, צבע (קרמל)",
       ["חלב מפוסטר", "שמנת", "ממרח שוקולד", "סוכר", "מייצב (E-440)", "חומרי טעם וריח", "תרבויות חיות", "צבע (קרמל)"],
       allergens=["חלב", "סויה"]),
    # sugar=21g → red_label_sugar; sat_fat=5.2g → red_label_sat_fat → 2 LABELS → cap=45!
    # ונילין → flavor_enhancer; קרמל → color; E-322 → emulsifier → NOVA4 → E grade

    _p("7290200000030", "יוגורט עם ריבת תות", "שטראוס", "dessert",
       155, 3.5, 2.3, 75, 26.0, 23.0, 0.5, 4.0,
       "חלב מפוסטר, ריבת תות (תות, סוכר, פקטין), סוכר, גלוקוז, מייצב (E-440), חומרי טעם וריח, תרבויות חיות",
       ["חלב מפוסטר", "ריבת תות", "סוכר", "גלוקוז", "מייצב (E-440)", "חומרי טעם וריח", "תרבויות חיות"],
       allergens=["חלב"]),
    # sugar=23g → red_label_sugar → cap=55; חומרי טעם וריח → NOVA4 → cap=68 → binding=55

    _p("7290200000031", "קרם יוגורט קרמל", "טנובה", "dessert",
       145, 4.0, 2.8, 70, 22.0, 18.5, 0.0, 4.5,
       "חלב מפוסטר, שמנת, סוכר, קרמל 5%, מייצב (E-1442), חומרי טעם וריח, תרבויות חיות",
       ["חלב מפוסטר", "שמנת", "סוכר", "קרמל 5%", "מייצב (E-1442)", "חומרי טעם וריח", "תרבויות חיות"],
       allergens=["חלב"]),
    # קרמל → color signal +2; חומרי טעם וריח → flavor_enhancer +3 → NOVA4
    # sugar=18.5g → red_label_sugar → cap=55 → binding=55

    # ── GROUP 9: Diet / Light Yogurt with Sweeteners ────────────────────────────

    _p("7290200000032", "יוגורט 0% ללא סוכר תות", "דנונה", "diet",
       42, 0.2, 0.1, 55, 5.0, 3.0, 0.5, 5.0,
       "חלב מפוסטר, תות שדה 8%, ממתיק (סוכרלוזה), מייצב (E-440), תרבויות חיות, חומרי טעם וריח",
       ["חלב מפוסטר", "תות שדה 8%", "ממתיק (סוכרלוזה)", "מייצב (E-440)", "תרבויות חיות", "חומרי טעם וריח"],
       allergens=["חלב"], claims=["ללא סוכר", "דל קלוריות"]),
    # סוכרלוזה → sweetener_cap=70; חומרי טעם וריח → NOVA4 cap=68 → binding=68

    _p("7290200000033", "יוגורט דיאט ואניל 0%", "יוטבתה", "diet",
       38, 0.1, 0.1, 50, 4.5, 2.5, 0.0, 5.5,
       "חלב מפוסטר, ממתיק (אספרטם, אצסולפם K), ואניל, מייצב (E-1442), תרבויות חיות",
       ["חלב מפוסטר", "ממתיק (אספרטם, אצסולפם K)", "ואניל", "מייצב (E-1442)", "תרבויות חיות"],
       allergens=["חלב", "פנילאלנין"], claims=["ללא סוכר"]),
    # אספרטם → sweetener; ואניל → flavor_enhancer → nova4_score=5 → NOVA4 cap=68

    _p("7290200000034", "יוגורט יווני 0% סטביה", "טנובה", "diet",
       52, 0.2, 0.1, 40, 4.0, 2.5, 0.0, 9.5,
       "חלב מפוסטר, ממתיק (סטביה), תרבויות חיות",
       ["חלב מפוסטר", "ממתיק (סטביה)", "תרבויות חיות"],
       allergens=["חלב"], claims=["ללא סוכר"]),
    # סטביה → sweetener → sweetener_cap=70; NOVA3 cap=82 → binding=70 → C or B

    # ── GROUP 10: Plant-based Yogurt (routing stress tests) ──────────────────────

    _p("7290200000035", "יוגורט סויה טבעי", "אלפרו", "plant_based",
       58, 2.5, 0.4, 30, 4.5, 2.0, 1.5, 5.5,
       "חלב סויה, תרבויות חיות",
       ["חלב סויה", "תרבויות חיות"],
       allergens=["סויה"], claims=["טבעוני", "ללא גלוטן"]),
    # "יוגורט" in name → dairy_protein routing — plant-based product misrouted to dairy

    _p("7290200000036", "יוגורט קוקוס", "קוקו יו", "plant_based",
       120, 8.0, 7.0, 15, 9.0, 5.0, 2.5, 1.5,
       "חלב קוקוס 85%, תרבויות חיות, עמילן טפיוקה",
       ["חלב קוקוס 85%", "תרבויות חיות", "עמילן טפיוקה"],
       allergens=[], claims=["טבעוני", "ללא לקטוז"]),
    # sat_fat=7.0g → red_label_sat_fat → cap=55 (coconut is naturally high in sat_fat — stress test)

    _p("7290200000037", "יוגורט שיבולת שועל", "אלפרו", "plant_based",
       72, 2.0, 0.3, 40, 11.5, 5.0, 2.5, 2.5,
       "חלב שיבולת שועל, תרבויות חיות, עמילן טפיוקה",
       ["חלב שיבולת שועל", "תרבויות חיות", "עמילן טפיוקה"],
       allergens=["גלוטן"], claims=["טבעוני"]),

    _p("7290200000038", "יוגורט שקדים ואניל", "אלפרו", "plant_based",
       90, 4.0, 0.4, 35, 10.0, 7.0, 1.5, 2.5,
       "חלב שקדים, תרבויות חיות, ואניל, מייצב (E-440)",
       ["חלב שקדים", "תרבויות חיות", "ואניל", "מייצב (E-440)"],
       allergens=["שקדים"], claims=["טבעוני"]),
    # ואניל → flavor_enhancer → NOVA4; plant-based product — double stress test

    # ── GROUP 11: Lactose-free Yogurt ───────────────────────────────────────────

    _p("7290200000039", "יוגורט נטול לקטוז 1.5%", "טנובה", "lactose_free",
       62, 1.5, 1.0, 50, 5.0, 5.0, 0.0, 5.0,
       "חלב מפוסטר נטול לקטוז, אנזים לקטאז, תרבויות חיות",
       ["חלב מפוסטר נטול לקטוז", "אנזים לקטאז", "תרבויות חיות"],
       allergens=["חלב"], claims=["ללא לקטוז"]),
    # ing_count=3 → not NOVA1; clean → NOVA2; expected B or A

    _p("7290200000040", "יוגורט יווני נטול לקטוז", "יוטבתה", "lactose_free",
       80, 2.0, 1.4, 45, 4.5, 4.5, 0.0, 9.0,
       "חלב מפוסטר נטול לקטוז, אנזים לקטאז, תרבויות חיות",
       ["חלב מפוסטר נטול לקטוז", "אנזים לקטאז", "תרבויות חיות"],
       allergens=["חלב"], claims=["ללא לקטוז"]),
    # NOVA2, high protein → A expected

    _p("7290200000041", "יוגורט נטול לקטוז תות", "יוטבתה", "lactose_free",
       88, 1.5, 1.0, 55, 14.0, 11.0, 0.5, 4.5,
       "חלב מפוסטר נטול לקטוז, תות 12%, סוכר, אנזים לקטאז, מייצב (E-440), תרבויות חיות",
       ["חלב מפוסטר נטול לקטוז", "תות 12%", "סוכר", "אנזים לקטאז", "מייצב (E-440)", "תרבויות חיות"],
       allergens=["חלב"], claims=["ללא לקטוז"]),

    # ── GROUP 12: Drinkable Yogurt (routing stress tests) ───────────────────────

    _p("7290200000042", "לבן שתייה 3% טנובה", "טנובה", "drinkable",
       72, 3.0, 2.0, 60, 4.5, 4.5, 0.0, 3.2,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # "שתייה"(0.90) > "לבן"(0.60) → routes to BEVERAGE (error)
    # NOVA1 (single ingredient!) but beverage table: kcal=72 → score=50 → D

    _p("7290200000043", "יוגורט שתייה תות", "דנונה", "drinkable",
       90, 1.5, 1.0, 60, 15.0, 13.0, 0.5, 4.0,
       "חלב מפוסטר, תות 10%, סוכר, מייצב (E-440), חומרי טעם וריח, תרבויות חיות",
       ["חלב מפוסטר", "תות 10%", "סוכר", "מייצב (E-440)", "חומרי טעם וריח", "תרבויות חיות"],
       allergens=["חלב"]),
    # "יוגורט"(0.95) > "שתייה"(0.90) → dairy_protein routing (CORRECT!)
    # חומרי טעם וריח → NOVA4 cap=68; sugar=13g < 17.5 so no red label → C

    _p("7290200000044", "קפיר שתייה 3%", "טנובה", "drinkable",
       65, 3.0, 2.0, 50, 4.5, 4.5, 0.0, 3.5,
       "חלב מפוסטר, תרבויות קפיר",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # "קפיר"(0.95) > "שתייה"(0.90) → dairy_protein routing (CORRECT!)
    # NOVA1 → floor=85 → A

    _p("7290200000045", "לבן 1.5% חלב טנובה", "טנובה", "drinkable",
       48, 1.5, 1.0, 50, 4.2, 4.2, 0.0, 3.5,
       "חלב מפוסטר, תרבויות חיות",
       ["חלב מפוסטר"],
       allergens=["חלב"]),
    # "לבן"(0.60) + "חלב"(0.70) → dairy_protein routing (correct); NOVA1 → floor=85 → A
]


def write_products():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for p in PRODUCTS:
        pid = p["canonical_product_id"]
        path = OUTPUT_DIR / f"{pid}.json"
        path.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
        written += 1

    print(f"Written: {written} products to {OUTPUT_DIR}")
    subtypes: dict = {}
    for p in PRODUCTS:
        st = p.get("bsip_yogurt_subtype", "?")
        subtypes[st] = subtypes.get(st, 0) + 1
    print("Subtype distribution:")
    for st, count in sorted(subtypes.items()):
        print(f"  {st:20s}: {count}")


if __name__ == "__main__":
    write_products()
