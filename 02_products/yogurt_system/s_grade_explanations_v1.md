# S-Grade Explanations — Yogurts Category
## Status: APPROVED — Nutrition Agent audit complete 2026-06-12
## Source run: run_yogurt_006_shipcfg2
## Products: 7290112336712 (92.6/S) and 7290110565527 (90.6/S)

---

## AUDIT RECORD

### Product 7290110565527 — דנונה פרו 20 גרם חלבון (90.6/S)

**Trace file:** `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products/bsip1_yogurt_7290110565527/bsip2_trace.json`
**BSIP1 source:** `03_operations/bsip1/run_yogurt_006/output/bsip1_7290110565527.json`
**Source:** Shufersal only. No OFF contamination in this corpus entry (the Yohananof duplicate of this barcode was correctly excluded as off_candidate_panel per run_record exclusion list).

#### Per-Dimension Audit

| Dimension | Score | Trace Note | Verdict |
|---|---|---|---|
| processing_quality | 64.0 | NOVA 2, confidence=low (0.25): NOVA 2 base=85, scaled by confidence_scale=0.4 → 50+(85-50)×0.4 = 64.0. Low NOVA confidence is correctly reflected. | PASS |
| nutrient_density | 75.0 | protein=10.0g → 75.0; fiber not-applicable for dairy_protein (EV-027). Math: protein scale returns 75.0 at 10.0g. | PASS |
| calorie_density | 90.0 | energy_kcal=70.0, category=dairy_protein → 90 (lookup table, low-calorie dairy band). | PASS |
| glycemic_quality | 81.5 | 90 − sugar_penalty(8.5) + fiber(0) + wg(0) = 81.5. sugar_penalty at sugars=3.4g checks out (graduated bands). | PASS |
| protein_quality | 75.0 | protein=10.0g base=75.0, source=whole_food (no isolate markers) ×1.0 → 75.0. | PASS |
| additive_quality | 100 | additive_marker_count=0, sweetener_detected=false, sprint1_additives=0 → 100. Ingredient list has only 2 items (milk + cultures), no additive terms. | PASS |
| satiety_support | 100 | (10.0×3 + 0×5) / max(50, 70) × 400 = 30/70 × 400 = 171.4 → capped at 100. | PASS |
| fat_quality | 83.0 | R3 leanness: fat=1.5g, sat_fat absent (treated 0) → 83.0. Sat_fat null is handled correctly; confidence haircut applied separately. | PASS |
| regulatory_quality | 95.0 | red_label_count=0, no Israeli red labels fired. sodium=35mg well below 700mg threshold. | PASS |
| whole_food_integrity | 90 | NOVA 2 base=85, ing_count=2, complexity_pen=0, ferm_bonus=+5 → 90. | PASS |

**Weighted sum:** 64.0×0.15 + 75.0×0.15 + 90.0×0.15 + 81.5×0.12 + 75.0×0.10 + 100×0.10 + 100×0.06 + 83.0×0.08 + 95.0×0.05 + 90×0.04
= 9.6 + 11.25 + 13.5 + 9.78 + 7.5 + 10.0 + 6.0 + 6.64 + 4.75 + 3.6 = **82.62** ✓ (trace: 82.62 pre-bonus)

**Fermentation bonus (+8 Path A):** has_fermentation=true from BSIP1 (fermentation_marker "חיידקי יוגורט" at position 2). Path A fires directly (declared culture marker). Path A does NOT trigger the YOGURT_TRIM ceiling (trim only applies to Path B / r7_culture_credit). 82.62 + 8 = 90.62 → 90.6/S. **Math confirmed.**

**Caps/penalties:** No cap fired. No penalty fired. All 15 caps considered, all condition=false. All 7 penalty rules considered, all fired=false. Score passes straight through to 90.6.

**Confidence:** 80/high (base 100 − 5 missing dietary_fiber − 5 missing sat_fat − 10 low NOVA confidence). No confidence ceiling applied (80 ≥ sufficient threshold). Correct.

**Source data integrity:** ingredients_text_he = "חלב מפוסטר, מכיל חיידקי יוגורט" (clean, post-strip). ingredients_raw_full shows the correct strip: the 536-char disclaimer bleed (nutrition table + website boilerplate) was removed leaving only the two declared ingredients. No sweeteners, no additives, no fat markers in the declared ingredient list. Protein=10.0g, sodium=35mg confirmed from Shufersal label.

**Audit verdict: PASS. Score 90.6/S is honest and mechanically correct from clean Shufersal data.**

---

### Product 7290112336712 — דנונה פרו 21 חלבון 0% (92.6/S)
*(Reference — P13 audit already approved; recorded here for completeness.)*

Path A fires identically: ingredient_list ["חלב מפוסטר", "מכיל חיידקי יוגורט"], has_fermentation=true, nova=2, no additives, no caps. Weighted pre-bonus = 84.63 + 8 = 92.63 → 92.6/S. Distinguishing factor vs twin: fat_g=0 (fat_quality=92.0 vs 83.0) and protein=10.5g (nutrient_density=80.0 vs 75.0, protein_quality=80.0 vs 75.0), explaining the ~2pt gap.

---

## CONSUMER-FACING HEBREW EXPLANATIONS

---

### דנונה פרו 21 חלבון 0% — ציון 92.6/S

**הסבר מוצר (insight line):**

שני מרכיבים בלבד: חלב מפוסטר וחיידקי יוגורט. ללא חומרי טעם, ממתיקים או תוספות.

**הסבר ציון S (paragraph for product card):**

דנונה פרו 21 הוא אחד מיחידים בקטגוריית היוגורטים שקיבל ציון S. הציון נובע משלושה גורמים שמצטברים: הרכב מינימלי — רק חלב מפוסטר וחיידקי יוגורט, ללא כל תוסף, ממתיק או סמיכה; צפיפות קלורית נמוכה במיוחד — 58 קילוקלוריות ל-100 גרם ללא שומן; וריכוז חלבון גבוה — 10.5 גרם ל-100 גרם, כולו ממקור מלא. כל מרכיב ניקוד שנבחן — עיבוד, תוספות, טיב השומן, רמת הסוכר, תרומת חלבון — יצא נקי. לא הופעלה אף הגבלת ניקוד.

---

### דנונה פרו 20 גרם חלבון — ציון 90.6/S

**הסבר מוצר (insight line):**

שני מרכיבים: חלב מפוסטר וחיידקי יוגורט. ללא תוספות, ממתיקים או חומרי סמיכה.

**הסבר ציון S (paragraph for product card):**

דנונה פרו 20 קיבל ציון S על בסיס אותו עיקרון כמו תאומו ה-21 גרם: מרכיב יחיד — חלב מפוסטר עם חיידקי יוגורט — ללא שום תוספת. בהשוואה לגרסת ה-21 גרם, מוצר זה מכיל 1.5 גרם שומן ל-100 גרם (לעומת 0%) ו-10 גרם חלבון (לעומת 10.5 גרם), מה שמוריד אותו ב-2 נקודות. בכל שאר המרכיבים — עיבוד, תוספות, רמת הסוכר, רגולציה — אין הבדל: שני המוצרים עברו את כל שערי הניקוד ולא הופעל אף קנס.

---

## SHARED METHODOLOGY NOTE (category caveat)

**מתאים להוספה להערת הקטגוריה:**

שני מוצרי הדנונה פרו (20 ו-21 גרם חלבון) קיבלו ציון S — הציון הגבוה ביותר בסולם. שניהם מכילים שני מרכיבים בלבד ועברו את כל שערי הניתוח ללא קנסות. ציון S בקטגוריית יוגורטים נדיר: מתוך 87 מוצרים שנותחו, רק שניים הגיעו אליו. זהו ממצא מבנה — לא תקרה שהוטלה — ומשקף ניקוד אמיתי.

---

## FILE PROVENANCE

- Audit date: 2026-06-12
- Run: run_yogurt_006_shipcfg2
- Trace paths:
  - `C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006_shipcfg2\products\products\bsip1_yogurt_7290110565527\bsip2_trace.json`
  - `C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006_shipcfg2\products\products\bsip1_yogurt_7290112336712\bsip2_trace.json`
- BSIP1 source: `C:\Bari\03_operations\bsip1\run_yogurt_006\output\bsip1_7290110565527.json`
- Approved by: Nutrition Agent (TASK-249 P18)
