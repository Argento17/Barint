# Router Stability Under Noise

Generated: 2026-05-25

Tests whether the router produces stable, correct routing under conditions
that degrade routing signals: OCR, missing names, contaminated ingredients.

---

## Routing Results

| ID | Noise | Expected | Actual | Confidence | Match | Anchor? | Instability? |
|:---|:------|:---------|:-------|:-----------|:------|:--------|:-------------|
| A1 |  | cereal | cereal | 0.93 | PASS | yes | no |
| A2 |  | snack_bar_granola | snack_bar_granola | 0.90 | PASS | yes | no |
| A3 |  | crispbread | crispbread | 0.94 | PASS | yes | no |
| A4 |  | beverage | beverage | 0.74 | PASS | no | no |
| A5 |  | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| B1 | missing_nutrition:dietary_fiber_g | cereal | cereal | 0.92 | PASS | yes | no |
| B2 | missing_nutrition:sodium_mg | snack_bar_granola | snack_bar_granola | 0.67 | PASS | no | no |
| B3 | missing_nutrition:fat_saturated_g | bread | bread | 0.90 | PASS | yes | no |
| B4 | missing_nutrition:protein_g | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| B5 | missing_nutrition:all_fields | cracker | cracker | 0.93 | PASS | yes | no |
| B6 | missing_nutrition:energy_kcal | beverage | beverage | 0.61 | PASS | no | no |
| B7 | missing_nutrition:carbohydrates_g | snack_bar_granola | snack_bar_granola | 0.76 | PASS | no | no |
| B8 | nutrition_inconsistency:sugar_le_ca | bread | bread | 0.90 | PASS | yes | no |
| C1 | missing_ingredients:text_and_list | bread | bread | 0.90 | PASS | yes | no |
| C2 | missing_ingredients:text_only | cereal | cereal | 0.92 | PASS | yes | no |
| C3 | ocr_corruption:mild_zws_insertion | snack_bar_granola | snack_bar_granola | 0.69 | PASS | no | no |
| C4 | ocr_corruption:moderate_char_substi | cracker | cracker | 0.93 | PASS | yes | no |
| C5 | ingredient_list:truncated_to_2_item | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| C6 | ocr_corruption:severe_space_injecti | crispbread | crispbread | 0.94 | PASS | yes | no |
| C7 | ocr_corruption:garbled_with_symbols | snack_bar_granola | whole_food_fat | 0.74 | FAIL (got whole_food_fat) | no | no |
| C8 | ocr_corruption:complete_unreadable | bread | bread | 0.90 | PASS | yes | no |
| D1 | routing:cereal_vs_snack_bar | cereal | cereal | 0.90 | PASS | yes | no |
| D2 | routing:dairy_vs_beverage | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| D3 | routing:cracker_vs_snack_bar | snack_bar_granola | cracker | 0.93 | FAIL (got cracker) | yes | no |
| D4 | routing:snack_bar_vs_dessert | snack_bar_granola | cereal | 0.57 | FAIL (got cereal) | no | yes |
| D5 | routing:whole_food_fat_vs_snack_bar | whole_food_fat | whole_food_fat | 0.92 | PASS | no | no |
| D6 | routing:dairy_vs_dessert | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| D7 | routing:beverage_vs_dairy | beverage | beverage | 0.92 | PASS | no | no |
| D8 | routing:muesli_anchor_cereal_vs_sna | snack_bar_granola | snack_bar_granola | 0.88 | PASS | yes | no |
| E1 | claim:protein_claim_vs_reality | snack_bar_granola | snack_bar_granola | 0.61 | PASS | no | no |
| E2 | claim:whole_grain_claim_refined_flo | bread | bread | 0.90 | PASS | yes | no |
| E3 | claim:natural_claim_with_additives | snack_bar_granola | snack_bar_granola | 0.78 | PASS | no | no |
| E4 | claim:no_sugar_with_concentrates | dairy_protein | dairy_protein | 0.92 | PASS | yes | no |
| E5 | claim:sourdough_no_fermentation | bread | bread | 0.90 | PASS | yes | no |
| E6 | claim:high_fiber_isolated_sources | bread | bread | 0.90 | PASS | yes | no |
| E7 | claim:light_high_calorie_density | cracker | cracker | 0.93 | PASS | yes | no |
| E8 | claim:natural_energy_high_sugar | snack_bar_granola | snack_bar_granola | 0.92 | PASS | no | no |
| F1 | missing_identity:barcode_null | cereal | cereal | 0.88 | PASS | yes | no |
| F2 | missing_identity:brand_empty | whole_food_fat | whole_food_fat | 0.93 | PASS | yes | no |
| F3 | missing_identity:vague_name | cereal | snack_bar_granola | 0.92 | FAIL (got snack_bar_granola) | no | no |
| F4 | missing_identity:name_empty | default | cereal | 0.55 | FAIL (got cereal) | no | yes |
| F5 | missing_identity:low_trust_single_s | snack_bar_granola | snack_bar_granola | 0.92 | PASS | no | no |
| G1 | consistency:sugar_greater_than_carb | snack_bar_granola | snack_bar_granola | 0.85 | PASS | no | no |
| G2 | consistency:satfat_greater_than_fat | dairy_protein | dairy_protein | 0.92 | PASS | no | no |
| G3 | consistency:kcal_outside_plausible_ | snack_bar_granola | dairy_protein | 0.92 | FAIL (got dairy_protein) | no | no |
| G4 | consistency:multiple_failures | snack_bar_granola | dairy_protein | 0.92 | FAIL (got dairy_protein) | no | no |
| H1 | hybrid:cereal_and_snack_bar | snack_bar_granola | cereal | 0.90 | FAIL (got cereal) | yes | no |
| H2 | hybrid:bread_with_dairy_ingredient | bread | bread | 0.90 | PASS | yes | no |
| H3 | hybrid:spread_vs_whole_food_fat | whole_food_fat | whole_food_fat | 0.82 | PASS | no | no |
| H4 | hybrid:protein_powder_category_gap | snack_bar_granola | snack_bar_granola | 0.66 | PASS | no | no |

---

## Routing Failures Detail (8 products)

### C7 — חטיף פירות ואגוזים טבעי

- Expected: **snack_bar_granola**
- Actual: **whole_food_fat** (conf=0.74)
- Top signals: [('whole_food_fat', 2.2), ('snack_bar_granola', 1.3), ('cereal', 0.2)]
- Suppressed: ['whole_food_fat:שקד(suppressed:wff_excluded)']
- Test purpose: Severe OCR: special characters throughout. Hebrew keywords still partially present but extraction unreliable

### D3 — קרקר שיבולת שועל מתוק עם ציפוי שוקולד

- Expected: **snack_bar_granola**
- Actual: **cracker** (conf=0.93)
- Top signals: [('snack_bar_granola', 1.9), ('cereal', 1.6), ('whole_food_fat', 0.6)]
- Suppressed: []
- Test purpose: Sweet chocolate-covered cracker — 'קרקר' anchor fires but product profile is more snack_bar. Test anchor vs signal tension

### D4 — עוגיות שיבולת שועל וענבים ביסקוויט

- Expected: **snack_bar_granola**
- Actual: **cereal** (conf=0.57)
- Top signals: [('cereal', 1.6), ('snack_bar_granola', 1.3), ('cracker', 0.7)]
- Suppressed: []
- Test purpose: Oat biscuit — 'עוגיות' and 'ביסקוויט' both present; snack vs dessert ambiguity. Test if snack signals dominate

### F3 — מוצר דגנים לבוקר

- Expected: **cereal**
- Actual: **snack_bar_granola** (conf=0.92)
- Top signals: [('snack_bar_granola', 1.0), ('cereal', 0.2), ('whole_food_fat', 0.0)]
- Suppressed: []
- Test purpose: Vague name 'מוצר דגנים לבוקר' — no hard anchor; signal scoring must carry the routing

### F4 — (no name)

- Expected: **default**
- Actual: **cereal** (conf=0.55)
- Top signals: [('cereal', 0.35), ('whole_food_fat', 0.25), ('snack_bar_granola', 0.15)]
- Suppressed: ['whole_food_fat:שמן קוקוס(suppressed:no_wff_context)', 'whole_food_fat:אגוז(suppressed:no_wff_context)', 'whole_food_fat:אגוזים(suppressed:no_wff_context)']
- Test purpose: Product name is empty — no anchors can fire; routing based on signals from ingredient text only

### G3 — אבקת חלבון ספורט וניל

- Expected: **snack_bar_granola**
- Actual: **dairy_protein** (conf=0.92)
- Top signals: [('dairy_protein', 0.7), ('whole_food_fat', 0.0), ('snack_bar_granola', 0.0)]
- Suppressed: []
- Test purpose: 1800 kcal/100g is outside plausible solid food range (700 ceiling). kcal_plausible check should fire

### G4 — שייק חלבון תחליף ארוחה

- Expected: **snack_bar_granola**
- Actual: **dairy_protein** (conf=0.92)
- Top signals: [('dairy_protein', 0.7), ('whole_food_fat', 0.0), ('snack_bar_granola', 0.0)]
- Suppressed: []
- Test purpose: Multiple simultaneous consistency failures. System should reach INSUFFICIENT or very low confidence

### H1 — חטיפי גרנולה לבוקר ולחטיף

- Expected: **snack_bar_granola**
- Actual: **cereal** (conf=0.90)
- Top signals: [('snack_bar_granola', 3.1), ('cereal', 2.35), ('whole_food_fat', 0.25)]
- Suppressed: []
- Test purpose: Genuinely dual-use granola — marketed as both breakfast cereal and snack. 'גרנולה לבוקר' in name should anchor to cereal; without it, snack signals dominate

---

## Anchor Reliability

Products where a hard anchor fired:

- **A1** קורנפלקס דגני בוקר קלאסי[:30] → cereal via ['hard_anchor:קורנפלקס']
- **A2** חטיף גרנולה שיבולת שועל ודבש[:30] → snack_bar_granola via ['hard_anchor:גרנולה']
- **A3** לחמי קריספ שיפון מחמצת ויקינג[:30] → crispbread via ['hard_anchor:לחמי קריספ']
- **A5** יוגורט 3% שומן דנונה[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **B1** דגני בוקר מלאים עם סיבים[:30] → cereal via ['hard_anchor:דגני בוקר']
- **B3** לחם מחמצת כפרי שחור[:30] → bread via ['hard_anchor:לחם']
- **B4** יוגורט יווני עשיר[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **B5** קרקר קמח שיפון מלוח[:30] → cracker via ['hard_anchor:קרקר']
- **B8** לחם אחיד עם שיפון[:30] → bread via ['hard_anchor:לחם']
- **C1** לחם מחמצת שיפון ארטיזנלי[:30] → bread via ['hard_anchor:לחם']
- **C2** דגני בוקר חיטה מלאה ופירות יבשים[:30] → cereal via ['hard_anchor:דגני בוקר']
- **C4** קרקר כוסמין מלוח[:30] → cracker via ['hard_anchor:קרקר']
- **C5** יוגורט פירות יער 1.5% שומן[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **C6** לחמי קריספ דגן מלא שיפון[:30] → crispbread via ['hard_anchor:לחמי קריספ']
- **C8** לחם קמח חיטה מלאה ושיפון[:30] → bread via ['hard_anchor:לחם']
- **D1** גרנולה לבוקר עם פירות ואגוזים[:30] → cereal via ['hard_anchor:גרנולה לבוקר']
- **D2** יוגורט שתייה עשיר חלבון[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **D3** קרקר שיבולת שועל מתוק עם ציפוי שוקולד[:30] → cracker via ['hard_anchor:קרקר']
- **D6** קרם יוגורט שוקולד פרמיום[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **D8** מוסלי פירות וגרעינים[:30] → snack_bar_granola via ['hard_anchor:מוסלי']
- **E2** לחם דגן מלא בריא[:30] → bread via ['hard_anchor:לחם']
- **E4** יוגורט ללא תוספת סוכר עם פירות[:30] → dairy_protein via ['hard_anchor:יוגורט']
- **E5** לחם מחמצת ביתי[:30] → bread via ['hard_anchor:לחם']
- **E6** לחם סיבים גבוה עשיר בסיבים 8g[:30] → bread via ['hard_anchor:לחם']
- **E7** קרקר קל קלוריות דיאטה[:30] → cracker via ['hard_anchor:קרקר']
- **F1** שיבולת שועל אורגנית מלאה[:30] → cereal via ['hard_anchor:שיבולת שועל']
- **F2** טחינה גולמית 100%[:30] → whole_food_fat via ['hard_anchor:טחינה']
- **H1** חטיפי גרנולה לבוקר ולחטיף[:30] → cereal via ['hard_anchor:גרנולה לבוקר']
- **H2** לחם גבינה ועשבי תיבול[:30] → bread via ['hard_anchor:לחם']

---
*Report generated by run_robustness_sprint.py*