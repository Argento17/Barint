# False Positive Confidence Audit — Calibration Patch v1

Generated: 2026-05-25

## Audit Scope

Review of all new deductions introduced in Calibration Patch v1 for false positives.
Focus: `product_name_short_no_anchor`, `kcal_implausible_extra`, `anchor_secondary_tension_mild`.

A **false positive** is a confidence reduction that fires on a product with clear,
correct data — penalizing a legitimate product for having a short but unambiguous name,
or a product whose kcal appears implausible only because a macro field is missing.

---

## Root Cause: A4 Regression

**Product:** A4 — `משקה שיבולת שועל אוטלי` (Oatly oat drink)

**What happened (before fix):**
- Name has 4 words; no hard anchor fires (product routes via plant_milk_brand bypass,
  which does not set `anchor_override=True`).
- `product_name_short_no_anchor` condition: ≤4 words AND not anchor_override → fired.
- Deduction of −8 dropped IC score from the very_high threshold (95→87).
- `product_name_short_no_anchor` is in `_ROUTING_CONCERN_KW` → degradation High→Cautious.
- Result: A4 went from very_high/Full (Sprint v1) to high/Cautious (Patch v1).

**Root cause:**
The short-name penalty was designed for F3 (`מוצר דגנים לבוקר` = 'grain product for morning'),
a name with no category-identifying word. But A4's name starts with `משקה` (drink) —
a primary beverage identity keyword. A 4-word name that begins with `משקה` is NOT vague.

**Fix applied:**
Added an exemption set `_IDENTITY_EXEMPT` of category-identity keywords:
`משקה`, `שתייה`, `מיץ`, `קפה`, `תה`, `לימונדה` (beverages),
`חטיף`, `חטיפי` (snack bars),
`ממרח`, `טחינה`, `חומוס` (spreads),
`גבינה`, `חלב` (dairy without hard anchor).

If any exemption keyword appears in the name, `product_name_short_no_anchor` is suppressed.

---

## False Positives Found and Fixed

| ID | Name | Deduction | FP Reason | Fixed? |
|:---|:-----|:----------|:----------|:-------|
| A4 | משקה שיבולת שועל אוטלי | product_name_short_no_anchor | 'משקה' = explicit beverage identity | ✓ |
| D7 | משקה סויה בטעם יוגורט | product_name_short_no_anchor | 'משקה' = explicit beverage identity | ✓ |
| H3 | ממרח שקדים ותמרים | product_name_short_no_anchor | 'ממרח' = explicit spread identity | ✓ |
| B2 | חטיף אנרגיה שקדים ותמרים | product_name_short_no_anchor | 'חטיף' = explicit snack identity | ✓ |
| B7 | חטיף דגנים שוקולד ואגוזים | product_name_short_no_anchor | 'חטיף' = explicit snack identity | ✓ |
| E1 | חטיף חלבון גבוה 30g | product_name_short_no_anchor | 'חטיף' = explicit snack identity | ✓ |
| E3 | חטיף טבעי 100% טבע | product_name_short_no_anchor | 'חטיף' = explicit snack identity | ✓ |
| B4 | יוגורט יווני עשיר | kcal_implausible_extra | protein_g=None → expected_min underestimated | ✓ |
| B7 | חטיף דגנים שוקולד ואגוזים | kcal_implausible_extra | carbohydrates_g=None → expected_min underestimated | ✓ |

---

## kcal_implausible_extra — Missing Macro Guard

**Root cause:** The check used `nn.get('field') or 0` — treating `None` as `0`.
A product with protein_g=None and kcal=95 would compute expected_min from fat+carbs only,
underestimating by ~30 kcal. That makes kcal=95 appear '>1.5×' of the underestimate.

**Fix:** Gate the check on all three macros being non-None. If any macro is missing,
skip the implausibility check entirely — missing fields cannot provide a reliable baseline.

| ID | kcal | Missing Macro | Before Fix | After Fix |
|:---|:-----|:-------------|:-----------|:----------|
| B4 | 95 | protein_g=None | Fired (FP) | Suppressed ✓ |
| B7 | 450 | carbohydrates_g=None | Fired (FP) | Suppressed ✓ |
| G3 | 1800 | All present | Fires (TP) | Still fires ✓ |
| G4 | 600 | All present | Fires (TP) | Still fires ✓ |

---

## anchor_secondary_tension — No False Positives Confirmed

After pair-based restriction and raised thresholds (mild ≥ 0.35, strong ≥ 0.50),
no clean baseline products trigger anchor_secondary_tension.

| ID | Primary | Secondary | sec_conf | Verdict |
|:---|:--------|:----------|:---------|:--------|
| D3 | cracker | snack_bar_granola | 0.41 | TRUE POSITIVE — sweet oat cracker |
| H1 | cereal | snack_bar_granola | 0.53 | TRUE POSITIVE — hybrid granola product |
| D2 | dairy_protein | beverage | 0.49 | BORDERLINE — drinkable yogurt, D-group expected |
| D6 | dairy_protein | dessert | ~0.50 | BORDERLINE — cream yogurt, D-group expected |

Group A products: A2/A3 no longer trigger (pair check rejects sibling categories).

---

## Post-Fix: All Deduction Firings

| ID | Name | Deductions | Band | Deg | vs Sprint v1 |
|:---|:-----|:-----------|:-----|:----|:-------------|
| C2 | דגני בוקר חיטה מלאה ופ | `ingredient_text_absent: ingred`(-14) | high | Cautious | CHANGED |
| D2 | יוגורט שתייה עשיר חלבו | `anchor_secondary_tension_mild:`(-6) | high | Cautious | CHANGED |
| D3 | קרקר שיבולת שועל מתוק  | `anchor_secondary_tension_mild:`(-6) | high | Cautious | CHANGED |
| D5 | תערובת אגוזים וגרעינים | `product_name_short_no_anchor: `(-8) | high | Cautious | CHANGED |
| D6 | קרם יוגורט שוקולד פרמי | `anchor_secondary_tension_mild:`(-6) | high | Cautious | CHANGED |
| F3 | מוצר דגנים לבוקר | `product_name_short_no_anchor: `(-8) | high | Cautious | CHANGED |
| F4 |  | `product_name_empty: no meaning`(-20) | low | Uncertain | CHANGED |
| G1 | חטיף מלטי-דגן בריא | `kcal_implausible_extra: kcal=3`(-10) | low | Uncertain | CHANGED |
| G3 | אבקת חלבון ספורט וניל | `kcal_implausible_extra: kcal=1`(-10); `supplement_candidate: protein_`(-22) | low | Insufficient | CHANGED |
| G4 | שייק חלבון תחליף ארוחה | `kcal_implausible_extra: kcal=6`(-10); `supplement_candidate: protein_`(-22) | insufficient_context | Insufficient | CHANGED |
| H1 | חטיפי גרנולה לבוקר ולח | `anchor_secondary_tension: anch`(-12) | high | Cautious | CHANGED |
| H4 | אבקת שייק חלבון שוקולד | `supplement_candidate: protein_`(-22) | moderate | Insufficient | CHANGED |

---

## Group A Regression Check (Post-Fix)

| ID | Name | Band (Sprint v1) | Band (Post-Fix) | Deg | Status |
|:---|:-----|:----------------|:----------------|:----|:-------|
| A1 | קורנפלקס דגני בוקר קלאסי | very_high | very_high | Full | ✓ OK |
| A2 | חטיף גרנולה שיבולת שועל ו | very_high | very_high | Full | ✓ OK |
| A3 | לחמי קריספ שיפון מחמצת וי | very_high | very_high | Full | ✓ OK |
| A4 | משקה שיבולת שועל אוטלי | high | high | Full | ✓ OK |
| A5 | יוגורט 3% שומן דנונה | high | high | Full | ✓ OK |

---

## Remaining Intentional Deductions (True Positives)

These still fire after fixes — all are correct behavior:

| ID | Deduction | Reason |
|:---|:----------|:-------|
| C2 | ingredient_text_absent | Ingredient list present, text field empty |
| D3 | anchor_secondary_tension_mild | Sweet cracker with 41% secondary snack_bar signal |
| D5 | product_name_short_no_anchor | 'תערובת' (mix) is generic — 4 words, no identity keyword |
| F3 | product_name_short_no_anchor | 'מוצר דגנים לבוקר' — no category identity word |
| G3 | supplement_candidate + kcal_implausible_extra | Protein powder with 1800 kcal |
| G4 | supplement_candidate + kcal_implausible_extra | Protein shake — meal replacement |
| H1 | anchor_secondary_tension | Granola product — strong snack_bar secondary (0.53) |
| H4 | supplement_candidate | Whey shake — protein supplement |

---

*Report generated by run_calibration_patch.py — BSIP2 False Positive Audit v1*