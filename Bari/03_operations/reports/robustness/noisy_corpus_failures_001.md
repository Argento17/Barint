# Noisy Corpus Failure Taxonomy

Generated: 2026-05-25

## Failure Categories in Corpus

| Failure Category | Count | Description |
|:-----------------|:------|:------------|
| INGREDIENT_TRUNCATION | 37 | Ingredient list appears cut off; downstream signals incomple |
| RETAILER_INCONSISTENCY | 10 | Conflicting values across retailer sources create uncertaint |
| MISSINGNESS | 8 | Critical fields absent — scoring operates on incomplete info |
| CATEGORY_LEAKAGE | 5 | Ingredient text signals cross-contaminate category routing |
| OCR_DEGRADATION | 5 | Corrupted or garbled text prevents reliable signal extractio |
| SEMANTIC_AMBIGUITY | 4 | Product semantics genuinely unclear from available signals |
| HYBRID_CONFLICT | 2 | Legitimate dual-category product; routing choice materially  |

| Severity | Count |
|:---------|:------|
| CRITICAL | 5 |
| HIGH | 9 |
| MEDIUM | 48 |
| LOW | 9 |

---

## Product-Level Failure Detail

### A1 — קורנפלקס דגני בוקר קלאסי

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### A2 — חטיף גרנולה שיבולת שועל ודבש

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### A3 — לחמי קריספ שיפון מחמצת ויקינג

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### A4 — משקה שיבולת שועל אוטלי

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B1 — דגני בוקר מלאים עם סיבים

**Risk:** LOW  | **Failures:** 2  | **Max severity:** MEDIUM

- **[LOW] MISSINGNESS**
  - Evidence: Missing nutrition field: dietary_fiber_g
  - Recommendation: Minor gap; affected dimension uses neutral 50
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B2 — חטיף אנרגיה שקדים ותמרים

**Risk:** MEDIUM  | **Failures:** 3  | **Max severity:** MEDIUM

- **[LOW] CATEGORY_LEAKAGE**
  - Evidence: 1 signal(s) suppressed: ['whole_food_fat:שמן קוקוס(suppressed:no_wff_context)']
  - Recommendation: Monitor for signal leakage in this product class
- **[LOW] MISSINGNESS**
  - Evidence: Missing nutrition field: sodium_mg
  - Recommendation: Minor gap; affected dimension uses neutral 50
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B3 — לחם מחמצת כפרי שחור

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B4 — יוגורט יווני עשיר

**Risk:** LOW  | **Failures:** 1  | **Max severity:** LOW

- **[LOW] MISSINGNESS**
  - Evidence: Missing nutrition field: protein_g
  - Recommendation: Minor gap; affected dimension uses neutral 50

### B5 — קרקר קמח שיפון מלוח

**Risk:** CRITICAL  | **Failures:** 2  | **Max severity:** CRITICAL

- **[CRITICAL] MISSINGNESS**
  - Evidence: Missing critical nutrition fields: ['energy_kcal', 'protein_g', 'fat_g', 'carbohydrates_g', 'dietary
  - Recommendation: Product cannot be reliably scored — flag for data collection priority
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B6 — משקה שיבולת שועל בטעם שוקולד

**Risk:** MEDIUM  | **Failures:** 3  | **Max severity:** MEDIUM

- **[MEDIUM] SEMANTIC_AMBIGUITY**
  - Evidence: category_confidence=0.61 — routing is uncertain
  - Recommendation: Review routing signal log for competing signals; consider dedicated anchor term
- **[LOW] MISSINGNESS**
  - Evidence: Missing nutrition field: energy_kcal
  - Recommendation: Minor gap; affected dimension uses neutral 50
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B7 — חטיף דגנים שוקולד ואגוזים

**Risk:** LOW  | **Failures:** 2  | **Max severity:** MEDIUM

- **[LOW] MISSINGNESS**
  - Evidence: Missing nutrition field: carbohydrates_g
  - Recommendation: Minor gap; affected dimension uses neutral 50
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### B8 — לחם אחיד עם שיפון

**Risk:** HIGH  | **Failures:** 2  | **Max severity:** HIGH

- **[HIGH] RETAILER_INCONSISTENCY**
  - Evidence: nutrition_consistency_status=suspicious
  - Recommendation: Cross-reference with physical product; flag for BSIP1 re-enrichment
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### C1 — לחם מחמצת שיפון ארטיזנלי

**Risk:** HIGH  | **Failures:** 1  | **Max severity:** HIGH

- **[HIGH] MISSINGNESS**
  - Evidence: No ingredient data available — signal extraction runs on nutrition only
  - Recommendation: Ingredient data required for NOVA, additive, fiber source, and fermentation signals

### C2 — דגני בוקר חיטה מלאה ופירות יבשים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] OCR_DEGRADATION**
  - Evidence: ingredient_text=0 chars but 4 items listed — text likely truncated by OCR
  - Recommendation: Cross-reference against physical product label or alternative retailer scrape

### C3 — חטיף אנרגיה שיבולת שועל ותמרים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### C4 — קרקר כוסמין מלוח

**Risk:** MEDIUM  | **Failures:** 2  | **Max severity:** MEDIUM

- **[MEDIUM] OCR_DEGRADATION**
  - Evidence: ingredient_text_quality=malformed — text structure is inconsistent
  - Recommendation: Manual review of ingredient text before re-processing
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### C6 — לחמי קריספ דגן מלא שיפון

**Risk:** HIGH  | **Failures:** 2  | **Max severity:** HIGH

- **[HIGH] OCR_DEGRADATION**
  - Evidence: ingredient_text_quality=corrupted — text contains garbled or unreadable sequences
  - Recommendation: Re-scrape product page or source ingredient data from alternative channel
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### C7 — חטיף פירות ואגוזים טבעי

**Risk:** HIGH  | **Failures:** 3  | **Max severity:** HIGH

- **[HIGH] OCR_DEGRADATION**
  - Evidence: ingredient_text_quality=corrupted — text contains garbled or unreadable sequences
  - Recommendation: Re-scrape product page or source ingredient data from alternative channel
- **[LOW] CATEGORY_LEAKAGE**
  - Evidence: 1 signal(s) suppressed: ['whole_food_fat:שקד(suppressed:wff_excluded)']
  - Recommendation: Monitor for signal leakage in this product class
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### C8 — לחם קמח חיטה מלאה ושיפון

**Risk:** HIGH  | **Failures:** 1  | **Max severity:** HIGH

- **[HIGH] OCR_DEGRADATION**
  - Evidence: ingredient_text_quality=corrupted — text contains garbled or unreadable sequences
  - Recommendation: Re-scrape product page or source ingredient data from alternative channel

### D1 — גרנולה לבוקר עם פירות ואגוזים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D2 — יוגורט שתייה עשיר חלבון

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D3 — קרקר שיבולת שועל מתוק עם ציפוי שוקולד

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D4 — עוגיות שיבולת שועל וענבים ביסקוויט

**Risk:** MEDIUM  | **Failures:** 3  | **Max severity:** MEDIUM

- **[MEDIUM] SEMANTIC_AMBIGUITY**
  - Evidence: category_confidence=0.57 — routing is uncertain
  - Recommendation: Review routing signal log for competing signals; consider dedicated anchor term
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients
- **[MEDIUM] HYBRID_CONFLICT**
  - Evidence: Hybrid routing: cereal(1.60) vs snack_bar_granola(1.30), delta=0.30
  - Recommendation: Score produced under 'cereal' interpretation; verify which context better matches consumer intent

### D5 — תערובת אגוזים וגרעינים קלויים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D6 — קרם יוגורט שוקולד פרמיום

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D7 — משקה סויה בטעם יוגורט

**Risk:** LOW  | **Failures:** 2  | **Max severity:** MEDIUM

- **[LOW] CATEGORY_LEAKAGE**
  - Evidence: 1 signal(s) suppressed: ['dairy_protein:יוגורט(flavor_suppressor)']
  - Recommendation: Monitor for signal leakage in this product class
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### D8 — מוסלי פירות וגרעינים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E1 — חטיף חלבון גבוה 30g

**Risk:** MEDIUM  | **Failures:** 2  | **Max severity:** MEDIUM

- **[MEDIUM] SEMANTIC_AMBIGUITY**
  - Evidence: category_confidence=0.61 — routing is uncertain
  - Recommendation: Review routing signal log for competing signals; consider dedicated anchor term
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E2 — לחם דגן מלא בריא

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E4 — יוגורט ללא תוספת סוכר עם פירות

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E5 — לחם מחמצת ביתי

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E6 — לחם סיבים גבוה עשיר בסיבים 8g

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E7 — קרקר קל קלוריות דיאטה

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### E8 — חטיף ג'ל אנרגיה טבעי ספורט

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### F1 — שיבולת שועל אורגנית מלאה

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] MISSINGNESS**
  - Evidence: barcode=null — product identity relies on name+brand matching only
  - Recommendation: Source barcode from packaging or alternative retailer

### F4 — (no name)

**Risk:** HIGH  | **Failures:** 4  | **Max severity:** MEDIUM

- **[MEDIUM] SEMANTIC_AMBIGUITY**
  - Evidence: category_confidence=0.55 — routing is uncertain
  - Recommendation: Review routing signal log for competing signals; consider dedicated anchor term
- **[MEDIUM] CATEGORY_LEAKAGE**
  - Evidence: 3 signals suppressed: ['whole_food_fat:שמן קוקוס(suppressed:no_wff_context)', 'whole_food_fat:אגוז(s
  - Recommendation: Review signal scope assignments; context_gated signals may need tighter gate conditions
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients
- **[MEDIUM] HYBRID_CONFLICT**
  - Evidence: Hybrid routing: cereal(0.35) vs whole_food_fat(0.25), delta=0.10
  - Recommendation: Score produced under 'cereal' interpretation; verify which context better matches consumer intent

### G1 — חטיף מלטי-דגן בריא

**Risk:** CRITICAL  | **Failures:** 4  | **Max severity:** CRITICAL

- **[LOW] CATEGORY_LEAKAGE**
  - Evidence: 2 signal(s) suppressed: ['whole_food_fat:אגוז(suppressed:no_wff_context)', 'whole_food_fat:אגוזים(su
  - Recommendation: Monitor for signal leakage in this product class
- **[HIGH] RETAILER_INCONSISTENCY**
  - Evidence: nutrition_consistency_status=suspicious
  - Recommendation: Cross-reference with physical product; flag for BSIP1 re-enrichment
- **[CRITICAL] RETAILER_INCONSISTENCY**
  - Evidence: sugar=45g > carbohydrates=30g — physically impossible
  - Recommendation: Data entry error — nutrition panel must be re-sourced before scoring is valid
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### G2 — גבינה צהובה 30%

**Risk:** CRITICAL  | **Failures:** 2  | **Max severity:** CRITICAL

- **[HIGH] RETAILER_INCONSISTENCY**
  - Evidence: nutrition_consistency_status=suspicious
  - Recommendation: Cross-reference with physical product; flag for BSIP1 re-enrichment
- **[CRITICAL] RETAILER_INCONSISTENCY**
  - Evidence: sat_fat=35g > fat=28g — physically impossible
  - Recommendation: Data entry error — fat values must be re-sourced

### G3 — אבקת חלבון ספורט וניל

**Risk:** HIGH  | **Failures:** 3  | **Max severity:** HIGH

- **[MEDIUM] RETAILER_INCONSISTENCY**
  - Evidence: nutrition_consistency_status=warnings — cross-retailer disagreement detected
  - Recommendation: Review specific disagreeing fields in BSIP1 conflicts_summary
- **[HIGH] RETAILER_INCONSISTENCY**
  - Evidence: energy_kcal=1800 outside plausible range (20-700 kcal/100g)
  - Recommendation: Verify per-100g basis; possible per-serving confusion
- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### G4 — שייק חלבון תחליף ארוחה

**Risk:** CRITICAL  | **Failures:** 3  | **Max severity:** CRITICAL

- **[HIGH] RETAILER_INCONSISTENCY**
  - Evidence: nutrition_consistency_status=suspicious
  - Recommendation: Cross-reference with physical product; flag for BSIP1 re-enrichment
- **[CRITICAL] RETAILER_INCONSISTENCY**
  - Evidence: sugar=55g > carbohydrates=20g — physically impossible
  - Recommendation: Data entry error — nutrition panel must be re-sourced before scoring is valid
- **[CRITICAL] RETAILER_INCONSISTENCY**
  - Evidence: sat_fat=8g > fat=5g — physically impossible
  - Recommendation: Data entry error — fat values must be re-sourced

### H1 — חטיפי גרנולה לבוקר ולחטיף

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### H2 — לחם גבינה ועשבי תיבול

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### H3 — ממרח שקדים ותמרים

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

### H4 — אבקת שייק חלבון שוקולד

**Risk:** LOW  | **Failures:** 1  | **Max severity:** MEDIUM

- **[MEDIUM] INGREDIENT_TRUNCATION**
  - Evidence: Ingredient text ends without closing punctuation — possible OCR or scraper truncation
  - Recommendation: Verify full ingredient list; truncated list may miss additives or key ingredients

---
*Report generated by run_robustness_sprint.py*