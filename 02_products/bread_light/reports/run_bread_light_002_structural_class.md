# Bread-Light — Structural Class: Bakery Rebalancing Effect (run_002)

**Date:** 2026-05-20

## Overview

The Bakery Semantics Layer feeds `_apply_bakery_rebalance` in structural_classifier_v1,
which adjusts class weights for bread/cracker/crispbread products before normalization.

Rebalancing rules (simplified):
- FQC ≤ 2 (whole grain dominant): reduce D, boost B/C
- FQC 4-5 (refined dominant): boost D, reduce B
- Fermentation=traditional: boost B +0.22, reduce D -0.15
- Fermentation=flavor_only/theater: boost D, reduce B
- Fiber=isolated: boost E +0.15, reduce B/C
- E bias correction: reduce E for natural-protein bakery products

## Per-Product SC Change (001 vs 002)

| Grp | Product                           | SC v1 | SC v2 | Changed? | FQC | Ferm     | GSS   |
|-----|-----------------------------------|-------|-------|----------|-----|----------|-------|
| A   | עוגיות אורז ללא מלח               | A     | A     | same     | 3   | none     | 57.0  |
| A   | קרקר חיטה מלאה פשוט               | B     | B     | same     | 2   | none     | 69.5  |
| A   | לחמי קריספ שיפון פשוט             | B     | B     | same     | 1   | none     | 82.0  |
| A   | לחם לבן פרוס פשוט                 | D     | D     | same     | 5   | none     | 32.0  |
| A   | קרקר מלוח פריך                    | D     | D     | same     | 5   | none     | 32.0  |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | D     | D     | same     | 2   | none     | 61.5  |
| B   | לחם "100% חיטה מלאה" מעורב        | D     | C     | CHANGED  | 3   | none     | 57.0  |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | D     | D     | same     | 5   | none     | 16.0  |
| B   | קרקר "בטא-גלוקן" תומך בלב         | D     | D     | same     | 5   | none     | 16.0  |
| B   | קרקרים "5 דגנים" ושיפון           | D     | D     | same     | 3   | none     | 57.0  |
| B   | לחם "7 דגנים" תעשייתי             | E     | E     | same     | 3   | none     | 57.0  |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | D     | C     | CHANGED  | 2   | none     | 69.5  |
| C   | לחם גרעינים אמיתי                 | D     | C     | CHANGED  | 2   | none     | 69.5  |
| C   | קרקרים "שבעת המינים" גרעינים      | D     | D     | same     | 4   | none     | 44.5  |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | D     | D     | same     | 5   | none     | 32.0  |
| C   | קרקר "גרעינים זהובים" פרמיום      | D     | D     | same     | 5   | none     | 32.0  |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | B     | B     | same     | 1   | traditio | 100.0 |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | B     | B     | same     | 2   | traditio | 87.5  |
| D   | לחם כפרי "מחמצת ושמרים"           | D     | D     | same     | 3   | flavor_o | 51.0  |
| D   | לחם "בסגנון מחמצת" תעשייתי        | D     | D     | same     | 5   | flavor_o | 26.0  |
| D   | קרקר "מחמצת" בייצור מהיר          | D     | C     | CHANGED  | 5   | traditio | 50.0  |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | D     | C     | CHANGED  | 2   | none     | 69.5  |
| E   | לחם חלבון ואגוזים "נוטרישן"       | D     | D     | same     | 3   | none     | 57.0  |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | D     | D     | same     | 5   | none     | 32.0  |
| E   | קרקר "סיבים+" אינולין וסיליום     | D     | D     | same     | 5   | none     | 16.0  |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | D     | D     | same     | 5   | none     | 16.0  |
| E   | לחם "קטו" דל פחמימות              | F     | E     | CHANGED  | 3   | none     | 41.0  |
| F   | עוגיות אורז "חמאה" שמן דקל        | D     | D     | same     | 3   | none     | 57.0  |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | F     | F     | same     | 3   | none     | 57.0  |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | E     | E     | same     | 5   | none     | 32.0  |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | D     | D     | same     | —   | —        | —     |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | E     | E     | same     | 5   | none     | 32.0  |

**SC assignments changed:** 6/32 products

## SC Distribution: Before vs After

| SC | Count v1 | Count v2 | Δ  |
|----|----------|----------|----|
| A  | 1        | 1        | 0  |
| B  | 4        | 4        | 0  |
| C  | 0        | 5        | 5  |
| D  | 22       | 17       | -5 |
| E  | 3        | 4        | 1  |
| F  | 2        | 1        | -1 |

## Assessment by Structural Class

### Class A (Intact Whole Food) — Expected: NOVA 1 single-ingredient

- **עוגיות אורז ללא מלח** [Grp A]: NOVA=1 FQC=3 Score=85

### Class B (Lightly Transformed Traditional) — Expected: genuine sourdough, simple WG

- **קרקר חיטה מלאה פשוט** [Grp A]: NOVA=2 FQC=2 Ferm=none Score=79.7
- **לחמי קריספ שיפון פשוט** [Grp A]: NOVA=2 FQC=1 Ferm=none Score=79.3
- **לחמי קריספ מחמצת שיפון מסורתי** [Grp D]: NOVA=2 FQC=1 Ferm=traditional Score=79.4
- **לחם מחמצת אמיתי ממחיטה מלאה** [Grp D]: NOVA=2 FQC=2 Ferm=traditional Score=79.0

### Class E (Engineered Wellness) — Expected: protein isolates, keto, fiber bombs

- **לחם "7 דגנים" תעשייתי** [Grp B]: NOVA=3 FQC=3 Ferm=none Score=53.0
- **לחם "קטו" דל פחמימות** [Grp E]: NOVA=4 FQC=3 Ferm=none Score=49.0
- **לחמי קריספ "שום ועשבים" תעשייתי** [Grp F]: NOVA=4 FQC=5 Ferm=none Score=40.6
- **קרקרים מתוקים לילדים "גולדה קידס"** [Grp F]: NOVA=4 FQC=5 Ferm=none Score=28.4

### Class F (Structurally Void) — Expected: NOVA 4, high additive, sweetener

- **עוגיות אורז שוקולד "בלה שוקו"** [Grp F]: NOVA=4 FQC=3 Score=51.0