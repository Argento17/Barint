# BSIP2 Robustness Calibration Patch v1

Generated: 2026-05-25  |  Corpus: robustness_corpus_001 (50 products)

## What Changed

Five new deduction types added to `interpretation_confidence.py`:

| Deduction | Amount | Trigger |
|:----------|:-------|:--------|
| `ingredient_text_absent` | -14 | Ingredient list present but text field empty |
| `product_name_empty` | -20 | Product name is blank or whitespace only |
| `product_name_very_short` | -14 | Name has ≤2 meaningful words |
| `product_name_short_no_anchor` | -8 | Name has ≤4 words and no hard anchor fired |
| `anchor_secondary_tension` | -12 | Anchor overrode routing but sec_conf ≥ 0.35 |
| `anchor_secondary_tension_mild` | -6 | Anchor overrode routing but sec_conf ≥ 0.20 |
| `kcal_implausible_extra` | -10 | Kcal outside ±40% of macro-implied range |
| `supplement_candidate` | -22 | Protein powder / meal replacement detected |

Two new rules added to `graceful_degradation.py`:

- Supplement candidates → UNCERTAINTY (if high/very_high) or INSUFFICIENT
- High band + routing concern in `additional_reductions` → CAUTIOUS

Additive field in `router_v2.py`:

- `supplement_quarantine` — non-null for protein_supplement_candidate products

---

## Before / After — Band Distribution

| Band | Before (Sprint v1) | After (Patch v1) | Delta |
|:-----|:------------------|:-----------------|:------|
| very_high | 24 | 17 | -7 |
| high | 14 | 19 | +5 |
| moderate | 9 | 8 | -1 |
| low | 3 | 5 | +2 |
| insufficient_context | 0 | 1 | +1 |

| Degradation | Before | After | Delta |
|:------------|:-------|:------|:------|
| FULL | 36 | 28 | -8 |
| CAUTIOUS | 9 | 14 | +5 |
| UNCERTAINTY | 3 | 4 | +1 |
| INSUFFICIENT | 2 | 4 | +2 |

---

## Full Product Table — Patch Results

Columns: ID | Name | Band (before → after) | Deg (before → after) | New Deductions

| ID | Name | Band | ∆Band | Deg | ∆Deg | New Deductions |
|:---|:-----|:-----|:------|:----|:-----|:---------------|
| A1 | קורנפלקס דגני בוקר קלאסי | very_high | = | Full | = | — |
| A2 | חטיף גרנולה שיבולת שועל ו | very_high | = | Full | = | — |
| A3 | לחמי קריספ שיפון מחמצת וי | very_high | = | Full | = | — |
| A4 | משקה שיבולת שועל אוטלי | high | = | Full | = | — |
| A5 | יוגורט 3% שומן דנונה | high | = | Full | = | — |
| B1 | דגני בוקר מלאים עם סיבים | very_high | = | Full | = | — |
| B2 | חטיף אנרגיה שקדים ותמרים | high | = | Full | = | — |
| B3 | לחם מחמצת כפרי שחור | very_high | = | Full | = | — |
| B4 | יוגורט יווני עשיר | high | = | Full | = | — |
| B5 | קרקר קמח שיפון מלוח | low | = | Insufficient | = | — |
| B6 | משקה שיבולת שועל בטעם שוק | moderate | = | Cautious | = | — |
| B7 | חטיף דגנים שוקולד ואגוזים | high | = | Full | = | — |
| B8 | לחם אחיד עם שיפון | high | = | Cautious | = | — |
| C1 | לחם מחמצת שיפון ארטיזנלי | moderate | = | Cautious | = | — |
| C2 ★ | דגני בוקר חיטה מלאה ופירו | high | →high | Cautious | →Cautious | ingredient_text_absent: ingredient  |
| C3 | חטיף אנרגיה שיבולת שועל ו | high | = | Full | = | — |
| C4 | קרקר כוסמין מלוח | moderate | = | Cautious | = | — |
| C5 | יוגורט פירות יער 1.5% שומ | high | = | Full | = | — |
| C6 | לחמי קריספ דגן מלא שיפון | moderate | = | Cautious | = | — |
| C7 | חטיף פירות ואגוזים טבעי | moderate | = | Cautious | = | — |
| C8 | לחם קמח חיטה מלאה ושיפון | low | = | Uncertain | = | — |
| D1 | גרנולה לבוקר עם פירות ואג | very_high | = | Full | = | — |
| D2 | יוגורט שתייה עשיר חלבון | high | →high | Cautious | →Cautious | anchor_secondary_tension_mild: sec_ |
| D3 ★ | קרקר שיבולת שועל מתוק עם  | high | →high | Cautious | →Cautious | anchor_secondary_tension_mild: sec_ |
| D4 | עוגיות שיבולת שועל וענבים | moderate | = | Cautious | = | — |
| D5 | תערובת אגוזים וגרעינים קל | high | →high | Cautious | →Cautious | product_name_short_no_anchor: 4 wor |
| D6 | קרם יוגורט שוקולד פרמיום | high | →high | Cautious | →Cautious | anchor_secondary_tension_mild: sec_ |
| D7 | משקה סויה בטעם יוגורט | very_high | = | Full | = | — |
| D8 | מוסלי פירות וגרעינים | very_high | = | Full | = | — |
| E1 | חטיף חלבון גבוה 30g | high | = | Full | = | — |
| E2 | לחם דגן מלא בריא | very_high | = | Full | = | — |
| E3 | חטיף טבעי 100% טבע | high | = | Full | = | — |
| E4 | יוגורט ללא תוספת סוכר עם  | very_high | = | Full | = | — |
| E5 | לחם מחמצת ביתי | very_high | = | Full | = | — |
| E6 | לחם סיבים גבוה עשיר בסיבי | very_high | = | Full | = | — |
| E7 | קרקר קל קלוריות דיאטה | very_high | = | Full | = | — |
| E8 | חטיף ג'ל אנרגיה טבעי ספור | very_high | = | Full | = | — |
| F1 | שיבולת שועל אורגנית מלאה | high | = | Full | = | — |
| F2 | טחינה גולמית 100% | very_high | = | Full | = | — |
| F3 ★ | מוצר דגנים לבוקר | high | →high | Cautious | →Cautious | product_name_short_no_anchor: 3 wor |
| F4 |  | low | →low | Uncertain | →Uncertain | product_name_empty: no meaningful p |
| F5 | חטיף דגנים בסיסי | high | = | Full | = | — |
| G1 | חטיף מלטי-דגן בריא | low | →low | Uncertain | = | kcal_implausible_extra: kcal=380 vs |
| G2 | גבינה צהובה 30% | moderate | = | Uncertain | = | — |
| G3 ★ | אבקת חלבון ספורט וניל | low | →low | Insufficient | →Insufficient | kcal_implausible_extra: kcal=1800 v; supplement_candidate: protein_suppl |
| G4 | שייק חלבון תחליף ארוחה | insufficient_context | →insufficient_context | Insufficient | = | kcal_implausible_extra: kcal=600 vs; supplement_candidate: protein_suppl |
| H1 ★ | חטיפי גרנולה לבוקר ולחטיף | high | →high | Cautious | →Cautious | anchor_secondary_tension: anchor ov |
| H2 | לחם גבינה ועשבי תיבול | very_high | = | Full | = | — |
| H3 | ממרח שקדים ותמרים | very_high | = | Full | = | — |
| H4 | אבקת שייק חלבון שוקולד | moderate | →moderate | Insufficient | →Insufficient | supplement_candidate: protein_suppl |

★ = target overconfident case

---

## Regression Check — Clean Baselines (Group A)

These products should not degrade from patch changes:

| ID | Band (before) | Band (after) | Degradation | Status |
|:---|:-------------|:------------|:------------|:-------|
| A1 | very_high | very_high | Full | OK |
| A2 | very_high | very_high | Full | OK |
| A3 | very_high | very_high | Full | OK |
| A4 | high | high | Full | OK |
| A5 | high | high | Full | OK |

---

*Report generated by run_calibration_patch.py — BSIP2 Calibration Patch v1*