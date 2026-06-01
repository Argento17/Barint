# Bread-Light — Structural Class Distribution

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Overview

Structural classes (A=Intact Whole Food → F=Structurally Void) are assigned
by structural_classifier_v1 based on trace signals.

| Class | Count | Share |
|-------|-------|-------|
| A     | 1     | 3%    |
| B     | 4     | 12%   |
| D     | 22    | 69%   |
| E     | 3     | 9%    |
| F     | 2     | 6%    |

## Product Assignments

| Grp | Product                           | SC | Conf | Notes                                              |
|-----|-----------------------------------|----|------|----------------------------------------------------|
| A   | עוגיות אורז ללא מלח               | A  | 0.75 | nova_1_signal, no_additives_detected, whole_food_i |
| A   | קרקר חיטה מלאה פשוט               | B  | 0.45 | nova_2_signal, no_additives_detected, moderate_pro |
| A   | לחמי קריספ שיפון פשוט             | B  | 0.45 | nova_2_signal, no_additives_detected, moderate_pro |
| A   | לחם לבן פרוס פשוט                 | D  | 0.44 | nova_3_signal, moderate_protein_quality            |
| A   | קרקר מלוח פריך                    | D  | 0.43 | nova_3_signal, moderate_protein_quality            |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | D  | 0.27 | nova_3_signal, no_additives_detected, moderate_pro |
| B   | לחם "100% חיטה מלאה" מעורב        | D  | 0.36 | nova_3_signal, moderate_protein_quality            |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | D  | 0.36 | nova_3_signal, moderate_protein_quality            |
| B   | קרקר "בטא-גלוקן" תומך בלב         | D  | 0.43 | nova_3_signal, moderate_protein_quality            |
| B   | קרקרים "5 דגנים" ושיפון           | D  | 0.44 | nova_3_signal, moderate_protein_quality            |
| B   | לחם "7 דגנים" תעשייתי             | E  | 0.41 | nova_3_signal, high_additive_load, moderate_protei |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | D  | 0.26 | nova_3_signal, no_additives_detected, high_protein |
| C   | לחם גרעינים אמיתי                 | D  | 0.26 | nova_3_signal, no_additives_detected, high_protein |
| C   | קרקרים "שבעת המינים" גרעינים      | D  | 0.48 | nova_3_signal, moderate_protein_quality            |
| C   | קרקר "גרעינים זהובים" פרמיום      | D  | 0.36 | nova_3_signal, moderate_protein_quality            |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | D  | 0.44 | nova_3_signal, moderate_protein_quality            |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | B  | 0.45 | nova_2_signal, no_additives_detected, moderate_pro |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | B  | 0.45 | nova_2_signal, no_additives_detected, moderate_pro |
| D   | לחם כפרי "מחמצת ושמרים"           | D  | 0.36 | nova_3_signal, moderate_protein_quality            |
| D   | קרקר "מחמצת" בייצור מהיר          | D  | 0.36 | nova_3_signal, moderate_protein_quality            |
| D   | לחם "בסגנון מחמצת" תעשייתי        | D  | 0.44 | nova_3_signal, moderate_protein_quality            |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | D  | 0.30 | nova_3_signal, high_protein_quality                |
| E   | לחם חלבון ואגוזים "נוטרישן"       | D  | 0.37 | nova_3_signal, high_protein_quality                |
| E   | קרקר "סיבים+" אינולין וסיליום     | D  | 0.44 | nova_3_signal, moderate_protein_quality            |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | D  | 0.44 | nova_3_signal, high_protein_quality                |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | D  | 0.40 | nova_3_signal, high_additive_load                  |
| E   | לחם "קטו" דל פחמימות              | F  | 0.35 | nova_4_signal, whole_food_integrity_low, moderate_ |
| F   | עוגיות אורז "חמאה" שמן דקל        | D  | 0.47 | nova_3_signal                                      |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | F  | 0.32 | nova_4_signal, whole_food_integrity_low            |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | E  | 0.46 | nova_4_signal, high_additive_load, whole_food_inte |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | D  | 0.52 | nova_3_signal                                      |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | E  | 0.38 | nova_4_signal, whole_food_integrity_low, moderate_ |

## Structural Class Coherence Assessment

### Group A (Baselines) — Expected: Mixed A-D

- Pure rye crispbread and whole-wheat cracker correctly classify as A or B
- White bread (refined flour dominant) should be C-D; check assignment
- Rice cakes (NOVA 1, single ingredient) correctly A
- Simple salty cracker: refined flour + salt only → should be D-E

### Group B (Wholegrain Halo) — Expected: C-D

Products with refined flour as first ingredient + minor whole-grain additions should
classify B-D, not A. If classifier assigns A-B to products with inulin + refined flour,
that is a classifier weakness: it cannot distinguish structural WG from label WG.

### Group E (Engineered Wellness) — Expected: E-F

Protein crackers (pea isolate + vital gluten), keto bread (almond flour + psyllium),
and fiber-bombs (inulin 17%) represent engineering-assembly, not food construction.
Structural class should be E-F. If classifier assigns B-C, it is being fooled by
high protein or low additive count, missing the assembly origin.

### Group F (Kids / Hyper-Palatable) — Expected: D-F

Chocolate rice cakes, kids crackers with sweeteners, corn puffs with BHA/BHT
should clearly classify F. Check whether palm oil + emulsifier pattern triggers F.