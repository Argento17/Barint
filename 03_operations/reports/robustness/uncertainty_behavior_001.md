# Uncertainty Behavior — Confidence Band Analysis

Generated: 2026-05-25  |  Corpus: robustness_corpus_001

## How Confidence Bands Respond to Data Quality

This report verifies that confidence degrades appropriately when data quality drops.
The goal: confidence should drop FASTER than interpretive ambition.

---

## Band Distribution

### VERY_HIGH — 24 products

- **A1** קורנפלקס דגני בוקר קלאסי | score=60.0 | ic_score=95 | scenarios=[]
- **A2** חטיף גרנולה שיבולת שועל ודבש | score=41.0 | ic_score=95 | scenarios=[]
- **A3** לחמי קריספ שיפון מחמצת ויקינג | score=83.0 | ic_score=95 | scenarios=[]
- **B1** דגני בוקר מלאים עם סיבים | score=66.2 | ic_score=90 | scenarios=['missing_nutrition:dietary_fiber_g']
- **B3** לחם מחמצת כפרי שחור | score=70.6 | ic_score=95 | scenarios=['missing_nutrition:fat_saturated_g']
- **C2** דגני בוקר חיטה מלאה ופירות יבשים | score=55.0 | ic_score=95 | scenarios=['missing_ingredients:text_only']
- **D1** גרנולה לבוקר עם פירות ואגוזים | score=52.0 | ic_score=95 | scenarios=['routing:cereal_vs_snack_bar']
- **D2** יוגורט שתייה עשיר חלבון | score=72.4 | ic_score=95 | scenarios=['routing:dairy_vs_beverage']
- **D3** קרקר שיבולת שועל מתוק עם ציפוי שוקולד | score=30.0 | ic_score=95 | scenarios=['routing:cracker_vs_snack_bar']
- **D5** תערובת אגוזים וגרעינים קלויים | score=60.0 | ic_score=95 | scenarios=['routing:whole_food_fat_vs_snack_bar']
- **D6** קרם יוגורט שוקולד פרמיום | score=52.8 | ic_score=95 | scenarios=['routing:dairy_vs_dessert']
- **D7** משקה סויה בטעם יוגורט | score=60.5 | ic_score=95 | scenarios=['routing:beverage_vs_dairy']
- **D8** מוסלי פירות וגרעינים | score=55.0 | ic_score=95 | scenarios=['routing:muesli_anchor_cereal_vs_snack']
- **E2** לחם דגן מלא בריא | score=69.4 | ic_score=95 | scenarios=['claim:whole_grain_claim_refined_flour_first']
- **E4** יוגורט ללא תוספת סוכר עם פירות | score=63.2 | ic_score=95 | scenarios=['claim:no_sugar_with_concentrates']
- **E5** לחם מחמצת ביתי | score=70.3 | ic_score=95 | scenarios=['claim:sourdough_no_fermentation']
- **E6** לחם סיבים גבוה עשיר בסיבים 8g | score=75.7 | ic_score=95 | scenarios=['claim:high_fiber_isolated_sources']
- **E7** קרקר קל קלוריות דיאטה | score=54.0 | ic_score=95 | scenarios=['claim:light_high_calorie_density']
- **E8** חטיף ג'ל אנרגיה טבעי ספורט | score=N/A | ic_score=95 | scenarios=['claim:natural_energy_high_sugar']
- **F2** טחינה גולמית 100% | score=60.0 | ic_score=100 | scenarios=['missing_identity:brand_empty']
- **F3** מוצר דגנים לבוקר | score=59.7 | ic_score=95 | scenarios=['missing_identity:vague_name']
- **H1** חטיפי גרנולה לבוקר ולחטיף | score=52.0 | ic_score=95 | scenarios=['hybrid:cereal_and_snack_bar']
- **H2** לחם גבינה ועשבי תיבול | score=64.1 | ic_score=95 | scenarios=['hybrid:bread_with_dairy_ingredient']
- **H3** ממרח שקדים ותמרים | score=60.0 | ic_score=95 | scenarios=['hybrid:spread_vs_whole_food_fat']

### HIGH — 14 products

- **A4** משקה שיבולת שועל אוטלי | score=59.8 | ic_score=87 | scenarios=[]
- **A5** יוגורט 3% שומן דנונה | score=69.4 | ic_score=87 | scenarios=[]
- **B2** חטיף אנרגיה שקדים ותמרים | score=45.8 | ic_score=82 | scenarios=['missing_nutrition:sodium_mg']
- **B4** יוגורט יווני עשיר | score=58.3 | ic_score=85 | scenarios=['missing_nutrition:protein_g']
- **B7** חטיף דגנים שוקולד ואגוזים | score=36.0 | ic_score=77 | scenarios=['missing_nutrition:carbohydrates_g']
- **B8** לחם אחיד עם שיפון | score=52.0 | ic_score=75 | scenarios=['nutrition_inconsistency:sugar_le_carbs_violated']
- **C3** חטיף אנרגיה שיבולת שועל ותמרים | score=49.9 | ic_score=83 | scenarios=['ocr_corruption:mild_zws_insertion']
- **C5** יוגורט פירות יער 1.5% שומן | score=61.2 | ic_score=87 | scenarios=['ingredient_list:truncated_to_2_items']
- **E1** חטיף חלבון גבוה 30g | score=54.7 | ic_score=82 | scenarios=['claim:protein_claim_vs_reality']
- **E3** חטיף טבעי 100% טבע | score=38.0 | ic_score=87 | scenarios=['claim:natural_claim_with_additives']
- **F1** שיבולת שועל אורגנית מלאה | score=85.0 | ic_score=82 | scenarios=['missing_identity:barcode_null']
- **F5** חטיף דגנים בסיסי | score=60.7 | ic_score=85 | scenarios=['missing_identity:low_trust_single_source']
- **G3** אבקת חלבון ספורט וניל | score=66.7 | ic_score=75 | scenarios=['consistency:kcal_outside_plausible_range']
- **H4** אבקת שייק חלבון שוקולד | score=70.0 | ic_score=87 | scenarios=['hybrid:protein_powder_category_gap']

### MODERATE — 9 products

- **B6** משקה שיבולת שועל בטעם שוקולד | score=53.5 | ic_score=72 | scenarios=['missing_nutrition:energy_kcal']
- **C1** לחם מחמצת שיפון ארטיזנלי | score=80.8 | ic_score=65 | scenarios=['missing_ingredients:text_and_list']
- **C4** קרקר כוסמין מלוח | score=71.1 | ic_score=72 | scenarios=['ocr_corruption:moderate_char_substitution']
- **C6** לחמי קריספ דגן מלא שיפון | score=82.0 | ic_score=68 | scenarios=['ocr_corruption:severe_space_injection']
- **C7** חטיף פירות ואגוזים טבעי | score=55.0 | ic_score=60 | scenarios=['ocr_corruption:garbled_with_symbols']
- **D4** עוגיות שיבולת שועל וענבים ביסקוויט | score=33.0 | ic_score=62 | scenarios=['routing:snack_bar_vs_dessert']
- **F4** (no name) | score=55.0 | ic_score=62 | scenarios=['missing_identity:name_empty']
- **G1** חטיף מלטי-דגן בריא | score=55.0 | ic_score=55 | scenarios=['consistency:sugar_greater_than_carbs']
- **G2** גבינה צהובה 30% | score=45.0 | ic_score=55 | scenarios=['consistency:satfat_greater_than_fat']

### LOW — 3 products

- **B5** קרקר קמח שיפון מלוח | score=50.2 | ic_score=45 | scenarios=['missing_nutrition:all_fields']
- **C8** לחם קמח חיטה מלאה ושיפון | score=65.0 | ic_score=53 | scenarios=['ocr_corruption:complete_unreadable']
- **G4** שייק חלבון תחליף ארוחה | score=40.0 | ic_score=35 | scenarios=['consistency:multiple_failures']

### INSUFFICIENT_CONTEXT — 0 products

*(none)*

---

## Confidence Reduction Analysis

Products where interpretation_confidence dropped most from base confidence:

| ID | Base Score | IC Score | Drop | Reason |
|:---|:-----------|:---------|:-----|:-------|
| D4 | 87 | 62 | 25 | router_instability: top-2 delta=0.30: ce; category_confidence_low(0.57) |
| F4 | 87 | 62 | 25 | router_instability: top-2 delta=0.10: ce; category_confidence_low(0.55) |
| F1 | 100 | 82 | 18 | missing_barcode; ingredient_truncation_suspected: list ha |
| C6 | 80 | 68 | 12 | ingredient_text_quality=corrupted |
| C7 | 72 | 60 | 12 | ingredient_text_quality=corrupted |
| C8 | 65 | 53 | 12 | ingredient_text_quality=corrupted |
| A5 | 95 | 87 | 8 | ingredient_truncation_suspected: list ha |
| C4 | 80 | 72 | 8 | ingredient_text_quality=malformed |
| C5 | 95 | 87 | 8 | ingredient_truncation_suspected: list ha |
| B6 | 77 | 72 | 5 | category_confidence_low(0.61) |
| E1 | 87 | 82 | 5 | category_confidence_low(0.61) |
| C3 | 87 | 83 | 4 | ingredient_text_quality=partial |

---

## Confidence vs Expected Band Match

| ID | Expected Band | Actual Band | Match |
|:---|:--------------|:------------|:------|
| A1 | very_high | very_high | EXACT |
| A2 | high | very_high | CLOSE |
| A3 | very_high | very_high | EXACT |
| A4 | very_high | high | CLOSE |
| A5 | very_high | high | CLOSE |
| B1 | high | very_high | CLOSE |
| B2 | high | high | EXACT |
| B3 | high | very_high | CLOSE |
| B4 | high | high | EXACT |
| B5 | insufficient_context | low | CLOSE |
| B6 | high | moderate | CLOSE |
| B7 | high | high | EXACT |
| B8 | low | high | DRIFT (got high) |
| C1 | low | moderate | CLOSE |
| C2 | moderate | very_high | DRIFT (got very_high) |
| C3 | moderate | high | CLOSE |
| C4 | moderate | moderate | EXACT |
| C5 | moderate | high | CLOSE |
| C6 | low | moderate | CLOSE |
| C7 | low | moderate | CLOSE |
| C8 | low | low | EXACT |
| D1 | high | very_high | CLOSE |
| D2 | high | very_high | CLOSE |
| D3 | moderate | very_high | DRIFT (got very_high) |
| D4 | moderate | moderate | EXACT |
| D5 | moderate | very_high | DRIFT (got very_high) |
| D6 | moderate | very_high | DRIFT (got very_high) |
| D7 | moderate | very_high | DRIFT (got very_high) |
| D8 | high | very_high | CLOSE |
| E1 | high | high | EXACT |
| E2 | high | very_high | CLOSE |
| E3 | high | high | EXACT |
| E4 | high | very_high | CLOSE |
| E5 | high | very_high | CLOSE |
| E6 | high | very_high | CLOSE |
| E7 | high | very_high | CLOSE |
| E8 | high | very_high | CLOSE |
| F1 | high | high | EXACT |
| F2 | high | very_high | CLOSE |
| F3 | moderate | very_high | DRIFT (got very_high) |
| F4 | low | moderate | CLOSE |
| F5 | moderate | high | CLOSE |
| G1 | low | moderate | CLOSE |
| G2 | low | moderate | CLOSE |
| G3 | low | high | DRIFT (got high) |
| G4 | insufficient_context | low | CLOSE |
| H1 | high | very_high | CLOSE |
| H2 | high | very_high | CLOSE |
| H3 | high | very_high | CLOSE |
| H4 | moderate | high | CLOSE |

---
*Report generated by run_robustness_sprint.py*