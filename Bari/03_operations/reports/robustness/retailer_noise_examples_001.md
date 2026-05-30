# Retailer Noise Examples — Concrete Case Studies

Generated: 2026-05-25

Worst-case failure examples with full pipeline trace.
Each case shows what the system received and how it responded.

---

## Critical Failures

### B5 — קרקר קמח שיפון מלוח

**Test purpose:** All nutrition fields absent — should reach INSUFFICIENT degradation level

**Noise applied:** missing_nutrition:all_fields

**Pipeline output:**
- Category: cracker (conf=0.93, anchor=True)
- Base confidence: 45 (low)
- Interpretation confidence: 45 (low)
- Final score: 50.2
- Degradation level: **INSUFFICIENT**
- Presented to consumer: score=None, grade=None, provisional=False

**Failures detected:**
- [CRITICAL] **MISSINGNESS**: Missing critical nutrition fields: ['energy_kcal', 'protein_g', 'fat_g', 'carboh
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> הציון הוא הערכה זהירה בלבד. ערך הקלוריות חסר — ציון צפיפות הקלוריות הוחלף בנייטרל 50; ערך החלבון חסר — ניתוח מקור חלבון אינו זמין. מומלץ לאמת את הנתונים לפני הסקת מסקנות.

**Recommendation:**
> Product cannot be reliably scored — flag for data collection priority

### G1 — חטיף מלטי-דגן בריא

**Test purpose:** sugar(45g) > carbs(30g): physically impossible. Critical consistency failure should trigger RETAILER_INCONSISTENCY

**Noise applied:** consistency:sugar_greater_than_carbs

**Pipeline output:**
- Category: snack_bar_granola (conf=0.85, anchor=False)
- Base confidence: 55 (low)
- Interpretation confidence: 55 (moderate)
- Final score: 55.0
- Degradation level: **UNCERTAINTY**
- Presented to consumer: score=None, grade=None, provisional=True

**Failures detected:**
- [LOW] **CATEGORY_LEAKAGE**: 2 signal(s) suppressed: ['whole_food_fat:אגוז(suppressed:no_wff_context)', 'whol
- [HIGH] **RETAILER_INCONSISTENCY**: nutrition_consistency_status=suspicious
- [CRITICAL] **RETAILER_INCONSISTENCY**: sugar=45g > carbohydrates=30g — physically impossible
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> הניתוח שמיש אך כולל אי-ודאות. שגיאת עקביות: סוכר רשום גבוה מפחמימות — ייתכן שגיאת נתונים. כמו כן: פרטי התזונה מעוררים חשד (ייתכן בלבול בין ל-100 גרם ל-מנה) — הציון זהיר יותר.

**Recommendation:**
> Monitor for signal leakage in this product class

### G2 — גבינה צהובה 30%

**Test purpose:** sat_fat(35g) > fat(28g): physically impossible. Critical consistency failure in dairy product

**Noise applied:** consistency:satfat_greater_than_fat

**Pipeline output:**
- Category: dairy_protein (conf=0.92, anchor=False)
- Base confidence: 55 (low)
- Interpretation confidence: 55 (moderate)
- Final score: 45.0
- Degradation level: **UNCERTAINTY**
- Presented to consumer: score=None, grade=None, provisional=True

**Failures detected:**
- [HIGH] **RETAILER_INCONSISTENCY**: nutrition_consistency_status=suspicious
- [CRITICAL] **RETAILER_INCONSISTENCY**: sat_fat=35g > fat=28g — physically impossible

**Interpretation narrative:**
> הניתוח שמיש אך כולל אי-ודאות. שגיאת עקביות: שומן רווי רשום גבוה מהשומן הכולל — ייתכן שגיאת נתונים. כמו כן: פרטי התזונה מעוררים חשד (ייתכן בלבול בין ל-100 גרם ל-מנה) — הציון זהיר יותר.

**Recommendation:**
> Cross-reference with physical product; flag for BSIP1 re-enrichment

## OCR Degradation Cases

### C2 — דגני בוקר חיטה מלאה ופירות יבשים

**Test purpose:** Ingredient list present but no text — L3 extraction works but claims analysis limited

**Noise applied:** missing_ingredients:text_only

**Pipeline output:**
- Category: cereal (conf=0.92, anchor=True)
- Base confidence: 95 (high)
- Interpretation confidence: 95 (very_high)
- Final score: 55.0
- Degradation level: **FULL**
- Presented to consumer: score=55.0, grade=C, provisional=False

**Failures detected:**
- [MEDIUM] **OCR_DEGRADATION**: ingredient_text=0 chars but 4 items listed — text likely truncated by OCR

**Interpretation narrative:**
> נתוני המוצר שלמים ועקביים. הניתוב הקטגורי יציב. הציון מבוסס על מלוא הנתונים הזמינים.

**Recommendation:**
> Cross-reference against physical product label or alternative retailer scrape

### C4 — קרקר כוסמין מלוח

**Test purpose:** Moderate OCR: character substitutions in ingredient text simulate scanner artifacts

**Noise applied:** ocr_corruption:moderate_char_substitution

**Pipeline output:**
- Category: cracker (conf=0.93, anchor=True)
- Base confidence: 80 (high)
- Interpretation confidence: 72 (moderate)
- Final score: 71.1
- Degradation level: **CAUTIOUS**
- Presented to consumer: score=71.1, grade=B, provisional=True

**Failures detected:**
- [MEDIUM] **OCR_DEGRADATION**: ingredient_text_quality=malformed — text structure is inconsistent
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> הניתוח שמיש אך כולל אי-ודאות.

**Recommendation:**
> Manual review of ingredient text before re-processing

### C6 — לחמי קריספ דגן מלא שיפון

**Test purpose:** Severe OCR: spaces injected throughout text. Hard anchor on name still routes correctly; ingredient signals degraded

**Noise applied:** ocr_corruption:severe_space_injection

**Pipeline output:**
- Category: crispbread (conf=0.94, anchor=True)
- Base confidence: 80 (high)
- Interpretation confidence: 68 (moderate)
- Final score: 82.0
- Degradation level: **CAUTIOUS**
- Presented to consumer: score=82.0, grade=A, provisional=True

**Failures detected:**
- [HIGH] **OCR_DEGRADATION**: ingredient_text_quality=corrupted — text contains garbled or unreadable sequence
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> הניתוח שמיש אך כולל אי-ודאות. טקסט הרכיבים נראה פגום — ייתכן שחלק מהאותות אינם מדויקים. כמו כן: הטקסט של הרכיבים פגום — ניתוח הרכיבים מוגבל.

**Recommendation:**
> Re-scrape product page or source ingredient data from alternative channel

## Claim vs Reality Cases

### E1 — חטיף חלבון גבוה 30g

**Test purpose:** Packaging says '30g protein' but nutrition panel shows 8g. Test that BSIP2 uses actual nutrition, not marketing

**Noise applied:** claim:protein_claim_vs_reality

**Pipeline output:**
- Category: snack_bar_granola (conf=0.61, anchor=False)
- Base confidence: 87 (high)
- Interpretation confidence: 82 (high)
- Final score: 54.7
- Degradation level: **FULL**
- Presented to consumer: score=54.7, grade=C, provisional=False

**Failures detected:**
- [MEDIUM] **SEMANTIC_AMBIGUITY**: category_confidence=0.61 — routing is uncertain
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> הניתוח אמין — פערים קלים בנתונים אינם משפיעים על האיכות הכוללת של הציון.

**Recommendation:**
> Review routing signal log for competing signals; consider dedicated anchor term

### E2 — לחם דגן מלא בריא

**Test purpose:** Claims 'whole grain' but refined flour (68%) is first ingredient. GSS should be low; bakery semantics should discount

**Noise applied:** claim:whole_grain_claim_refined_flour_first

**Pipeline output:**
- Category: bread (conf=0.90, anchor=True)
- Base confidence: 95 (high)
- Interpretation confidence: 95 (very_high)
- Final score: 69.4
- Degradation level: **FULL**
- Presented to consumer: score=69.4, grade=B, provisional=False

**Failures detected:**
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> נתוני המוצר שלמים ועקביים. הניתוב הקטגורי יציב. הציון מבוסס על מלוא הנתונים הזמינים.

**Recommendation:**
> Verify full ingredient list; truncated list may miss additives or key ingredients

### E3 — חטיף טבעי 100% טבע

**Test purpose:** '100% natural' claim but 5+ additive E-numbers. Additive_quality should drop significantly

**Noise applied:** claim:natural_claim_with_additives

**Pipeline output:**
- Category: snack_bar_granola (conf=0.78, anchor=False)
- Base confidence: 87 (high)
- Interpretation confidence: 87 (high)
- Final score: 38.0
- Degradation level: **FULL**
- Presented to consumer: score=38.0, grade=D, provisional=False

**Failures detected:**

**Interpretation narrative:**
> הניתוח אמין — פערים קלים בנתונים אינם משפיעים על האיכות הכוללת של הציון.

**Recommendation:**

### E4 — יוגורט ללא תוספת סוכר עם פירות

**Test purpose:** 'No added sugar' but contains 3 fruit concentrates. SC classification should detect SC-4; cap behavior tested

**Noise applied:** claim:no_sugar_with_concentrates

**Pipeline output:**
- Category: dairy_protein (conf=0.92, anchor=True)
- Base confidence: 95 (high)
- Interpretation confidence: 95 (very_high)
- Final score: 63.2
- Degradation level: **FULL**
- Presented to consumer: score=63.2, grade=C, provisional=False

**Failures detected:**
- [MEDIUM] **INGREDIENT_TRUNCATION**: Ingredient text ends without closing punctuation — possible OCR or scraper trunc

**Interpretation narrative:**
> נתוני המוצר שלמים ועקביים. הניתוב הקטגורי יציב. הציון מבוסס על מלוא הנתונים הזמינים.

**Recommendation:**
> Verify full ingredient list; truncated list may miss additives or key ingredients

---

## Graceful Degradation Showcase

Products demonstrating each degradation level:

| Level | ID | Name | Score | Grade | Provisional |
|:------|:---|:-----|:------|:------|:------------|
| FULL | A1 | קורנפלקס דגני בוקר קלאסי[:25] | 60.0 | C | no |
| FULL | A2 | חטיף גרנולה שיבולת שועל ודבש[:25] | 41.0 | D | no |
| CAUTIOUS | B6 | משקה שיבולת שועל בטעם שוקולד[:25] | 53.5 | C | yes |
| CAUTIOUS | B8 | לחם אחיד עם שיפון[:25] | 52.0 | C | yes |
| UNCERTAINTY | C8 | לחם קמח חיטה מלאה ושיפון[:25] | N/A | N/A | yes |
| UNCERTAINTY | G1 | חטיף מלטי-דגן בריא[:25] | N/A | N/A | yes |
| INSUFFICIENT | B5 | קרקר קמח שיפון מלוח[:25] | N/A | N/A | no |
| INSUFFICIENT | G4 | שייק חלבון תחליף ארוחה[:25] | N/A | N/A | no |

---
*Report generated by run_robustness_sprint.py*