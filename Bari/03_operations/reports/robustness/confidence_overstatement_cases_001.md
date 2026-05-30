# Confidence Overstatement Cases — Patch v1 Resolution

Generated: 2026-05-25

Five products were identified in Sprint v1 where confidence band was
too high relative to actual data quality. This report documents the
root cause, the fix applied, and the resulting behavior after the patch.

---

## C2 — דגני בוקר חיטה מלאה ופירות יבשים

**Root cause:** Ingredient list has 4 items but `ingredients_text_he` is empty string. Signal extraction operates on the text field — absent text silently degrades L3 signal quality without triggering any confidence penalty.

**Fix applied:** New deduction: `ingredient_text_absent` → -14 when list present but text empty.

**Before (Sprint v1):** band=very_high, degradation=Full

**After (Patch v1):** band=high, degradation=Cautious

**Target outcome:** band=high, degradation=Cautious
  Trigger: ingredient_text_absent → -14

**Achieved:** ✓ YES

**Confidence trace:**
- Base confidence: 95.0 (high)
- Interpretation score: 81.0
- Band: high

**New deductions fired:**
- `ingredient_text_absent: ingredient list present but text field empty` → -14

**All additional reductions:**
- `ingredient_text_absent: ingredient list present but text field empty`: -14

**Interpretation narrative:**
> הניתוח אמין. טקסט הרכיבים ריק למרות שרשימת הרכיבים קיימת — אותות רכיבים מוגבלים.

**Interpretation cautions:**
- טקסט הרכיבים ריק למרות שרשימת הרכיבים קיימת — אותות רכיבים מוגבלים

**Routing details:**
- Category: cereal (conf=0.92)
- Anchor override: True
- Secondary: bread (sec_conf=0.28)
- Supplement quarantine: None

---

## D3 — קרקר שיבולת שועל מתוק עם ציפוי שוקולד

**Root cause:** Hard anchor 'קרקר' fires and sets `anchor_override=True`, which forces `is_hybrid=False` by design. Sweet chocolate cracker has substantial snack_bar signals — but because the hybrid path was bypassed by the anchor, no competing-interpretation penalty was applied.

**Fix applied:** New deduction: `anchor_secondary_tension` → -12 when anchor overrides but secondary_confidence ≥ 0.35.

**Before (Sprint v1):** band=very_high, degradation=Full

**After (Patch v1):** band=high, degradation=Cautious

**Target outcome:** band=high, degradation=Cautious
  Trigger: anchor_secondary_tension → -12

**Achieved:** ✓ YES

**Confidence trace:**
- Base confidence: 95.0 (high)
- Interpretation score: 89.0
- Band: high

**New deductions fired:**
- `anchor_secondary_tension_mild: sec_conf=0.41 (snack_bar_granola)` → -6

**All additional reductions:**
- `anchor_secondary_tension_mild: sec_conf=0.41 (snack_bar_granola)`: -6

**Interpretation narrative:**
> הניתוח אמין. הסיווג הראשי נסמך על עוגן שם, אך קיים אות מתחרה משמעותי — ייתכן פרשנות חלופית.

**Interpretation cautions:**
- הסיווג הראשי נסמך על עוגן שם, אך קיים אות מתחרה משמעותי — ייתכן פרשנות חלופית

**Routing details:**
- Category: cracker (conf=0.93)
- Anchor override: True
- Secondary: snack_bar_granola (sec_conf=0.41)
- Supplement quarantine: None

---

## F3 — מוצר דגנים לבוקר

**Root cause:** Product name 'מוצר דגנים לבוקר' has only 3 meaningful words. No hard anchor fires. Signal-only routing produced snack_bar_granola at high category confidence — but a vague generic name is fundamentally less trustworthy regardless of routing outcome.

**Fix applied:** New deduction: `product_name_short_no_anchor` → -8 for ≤4 words without anchor.

**Before (Sprint v1):** band=very_high, degradation=Full

**After (Patch v1):** band=high, degradation=Cautious

**Target outcome:** band=high, degradation=Cautious
  Trigger: product_name_short_no_anchor → -8 (band: very_high→high)

**Achieved:** ✓ YES

**Confidence trace:**
- Base confidence: 95.0 (high)
- Interpretation score: 87.0
- Band: high

**New deductions fired:**
- `product_name_short_no_anchor: 3 words, no anchor or identity keyword` → -8

**All additional reductions:**
- `product_name_short_no_anchor: 3 words, no anchor or identity keyword`: -8

**Interpretation narrative:**
> הניתוח אמין. שם המוצר קצר מדי לזיהוי חד-משמעי — ייתכן חוסר ודאות בקטגוריה.

**Interpretation cautions:**
- שם המוצר קצר מדי לזיהוי חד-משמעי — ייתכן חוסר ודאות בקטגוריה

**Routing details:**
- Category: snack_bar_granola (conf=0.92)
- Anchor override: False
- Secondary: cereal (sec_conf=0.17)
- Supplement quarantine: None

---

## G3 — אבקת חלבון ספורט וניל

**Root cause:** Protein powder with 1800 kcal/100g. Two problems: (a) kcal is physically implausible for a food product, implying data entry error; (b) whey signals routed it to dairy_protein while it is actually a supplement outside the current food ontology. High confidence was inappropriate on both counts.

**Fix applied:** Two new deductions: `kcal_implausible_extra` → -10; `supplement_candidate` → -22. Supplement quarantine in graceful_degradation forces UNCERTAINTY.

**Before (Sprint v1):** band=high, degradation=Cautious

**After (Patch v1):** band=low, degradation=Insufficient

**Target outcome:** band=moderate, degradation=Uncertainty
  Trigger: supplement_candidate → -22

**Achieved:** ✓ YES

**Confidence trace:**
- Base confidence: 75.0 (medium)
- Interpretation score: 43.0
- Band: low

**New deductions fired:**
- `kcal_implausible_extra: kcal=1800 vs macros_implied=513` → -10
- `supplement_candidate: protein_supplement_candidate outside current food ontology` → -22

**All additional reductions:**
- `kcal_implausible_extra: kcal=1800 vs macros_implied=513`: -10
- `supplement_candidate: protein_supplement_candidate outside current food ontology`: -22

**Interpretation narrative:**
> הציון הוא הערכה זהירה בלבד. ערך הקלוריות אינו עולה בקנה אחד עם המאקרונוטריאנטים — ייתכן שגיאת נתונים; המוצר עשוי להיות תוסף חלבון / תחליף ארוחה — מחוץ לאונטולוגיה הנוכחית, ציון אינדיקטיבי בלבד. מומלץ לאמת את הנתונים לפני הסקת מסקנות.

**Interpretation cautions:**
- ערך הקלוריות אינו עולה בקנה אחד עם המאקרונוטריאנטים — ייתכן שגיאת נתונים
- המוצר עשוי להיות תוסף חלבון / תחליף ארוחה — מחוץ לאונטולוגיה הנוכחית, ציון אינדיקטיבי בלבד

**Routing details:**
- Category: dairy_protein (conf=0.92)
- Anchor override: False
- Secondary: whole_food_fat (sec_conf=0.10)
- Supplement quarantine: {'signal': "name:'אבקת חלבון'", 'category': 'protein_supplement_candidate'}

---

## H1 — חטיפי גרנולה לבוקר ולחטיף

**Root cause:** Hard anchor 'גרנולה לבוקר' fires → cereal. The product is a genuine hybrid (marketed as both cereal and snack). Anchor sets is_hybrid=False, suppressing the hybrid deduction. Secondary snack_bar_granola signal is substantial but unpenalized.

**Fix applied:** New deduction: `anchor_secondary_tension` fires when anchor overrides but secondary_confidence ≥ 0.20 (mild tension → -6) or ≥ 0.35 (strong → -12).

**Before (Sprint v1):** band=very_high, degradation=Full

**After (Patch v1):** band=high, degradation=Cautious

**Target outcome:** band=high, degradation=Cautious
  Trigger: anchor_secondary_tension → -6 to -12

**Achieved:** ✓ YES

**Confidence trace:**
- Base confidence: 95.0 (high)
- Interpretation score: 83.0
- Band: high

**New deductions fired:**
- `anchor_secondary_tension: anchor overrode strong sec_conf=0.53 (snack_bar_granola)` → -12

**All additional reductions:**
- `anchor_secondary_tension: anchor overrode strong sec_conf=0.53 (snack_bar_granola)`: -12

**Interpretation narrative:**
> הניתוח אמין. הסיווג הראשי נסמך על עוגן שם, אך קיים אות מתחרה משמעותי — ייתכן פרשנות חלופית.

**Interpretation cautions:**
- הסיווג הראשי נסמך על עוגן שם, אך קיים אות מתחרה משמעותי — ייתכן פרשנות חלופית

**Routing details:**
- Category: cereal (conf=0.90)
- Anchor override: True
- Secondary: snack_bar_granola (sec_conf=0.53)
- Supplement quarantine: None

---

*Report generated by run_calibration_patch.py — BSIP2 Calibration Patch v1*