# Bread-Light — Bakery Semantics Layer v1 Validation

**Run:** run_bread_light_002  **Date:** 2026-05-20

## Overview

The Bakery Semantics Layer adds 4 interpretation modules for bread/cracker/crispbread:
1. **Flour hierarchy** — dominant flour type, whole-grain dominance, quality class (1-5)
2. **Fermentation quality** — traditional / mixed_industrial / flavor_only / theater / none
3. **Fiber source quality** — structural / isolated / hybrid / minimal
4. **Seed semantics** — structural / halo / decorative / none

These signals feed a composite `grain_structure_score` (0-100) and rebalance the
structural classifier via `_apply_bakery_rebalance`.

## Full Bakery Semantics Table

| Grp | Product                           | Cat        | FQC | WG Dom   | Ferm       | Fiber      | Seed       | GSS   | SC | Score |
|-----|-----------------------------------|------------|-----|----------|------------|------------|------------|-------|----|-------|
| A   | עוגיות אורז ללא מלח               | cracker    | 3   | none     | none       | structural | none       | 57.0  | A  | 85    |
| A   | קרקר חיטה מלאה פשוט               | cracker    | 2   | high     | none       | structural | none       | 69.5  | B  | 79.7  |
| A   | לחמי קריספ שיפון פשוט             | crispbread | 1   | high     | none       | structural | none       | 82.0  | B  | 79.3  |
| A   | לחם לבן פרוס פשוט                 | bread      | 5   | none     | none       | structural | none       | 32.0  | D  | 59.2  |
| A   | קרקר מלוח פריך                    | cracker    | 5   | none     | none       | structural | none       | 32.0  | D  | 36.0  |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | crispbread | 2   | high     | none       | hybrid     | none       | 61.5  | D  | 73.5  |
| B   | לחם "100% חיטה מלאה" מעורב        | bread      | 3   | partial  | none       | structural | none       | 57.0  | C  | 71.1  |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | cracker    | 5   | none     | none       | isolated   | none       | 16.0  | D  | 68.1  |
| B   | קרקר "בטא-גלוקן" תומך בלב         | cracker    | 5   | none     | none       | isolated   | none       | 16.0  | D  | 65.8  |
| B   | קרקרים "5 דגנים" ושיפון           | cracker    | 3   | partial  | none       | structural | none       | 57.0  | D  | 63.4  |
| B   | לחם "7 דגנים" תעשייתי             | bread      | 3   | partial  | none       | structural | none       | 57.0  | E  | 53.0  |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | crispbread | 2   | high     | none       | structural | halo       | 69.5  | C  | 79.4  |
| C   | לחם גרעינים אמיתי                 | bread      | 2   | high     | none       | structural | halo       | 69.5  | C  | 77.2  |
| C   | קרקרים "שבעת המינים" גרעינים      | cracker    | 4   | decorati | none       | structural | decorative | 44.5  | D  | 55.2  |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | cracker    | 5   | none     | none       | structural | decorative | 32.0  | D  | 54.8  |
| C   | קרקר "גרעינים זהובים" פרמיום      | cracker    | 5   | none     | none       | structural | halo       | 32.0  | D  | 53.4  |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | crispbread | 1   | high     | traditiona | structural | none       | 100.0 | B  | 79.4  |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | bread      | 2   | high     | traditiona | structural | none       | 87.5  | B  | 79.0  |
| D   | לחם כפרי "מחמצת ושמרים"           | bread      | 3   | partial  | flavor_onl | structural | none       | 51.0  | D  | 70.3  |
| D   | לחם "בסגנון מחמצת" תעשייתי        | bread      | 5   | none     | flavor_onl | structural | none       | 26.0  | D  | 64.8  |
| D   | קרקר "מחמצת" בייצור מהיר          | cracker    | 5   | none     | traditiona | structural | none       | 50.0  | C  | 63.5  |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | crispbread | 2   | high     | none       | structural | halo       | 69.5  | C  | 74.9  |
| E   | לחם חלבון ואגוזים "נוטרישן"       | bread      | 3   | partial  | none       | structural | none       | 57.0  | D  | 71.7  |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | cracker    | 5   | none     | none       | structural | none       | 32.0  | D  | 69.0  |
| E   | קרקר "סיבים+" אינולין וסיליום     | cracker    | 5   | none     | none       | isolated   | none       | 16.0  | D  | 67.0  |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | bread      | 5   | none     | none       | isolated   | none       | 16.0  | D  | 52.3  |
| E   | לחם "קטו" דל פחמימות              | bread      | 3   | none     | none       | isolated   | none       | 41.0  | E  | 49.0  |
| F   | עוגיות אורז "חמאה" שמן דקל        | cracker    | 3   | none     | none       | structural | none       | 57.0  | D  | 58.1  |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | cracker    | 3   | none     | none       | structural | none       | 57.0  | F  | 51.0  |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | crispbread | 5   | none     | none       | structural | none       | 32.0  | E  | 40.6  |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | cracker    | 5   | none     | none       | structural | none       | 32.0  | E  | 28.4  |

## Flour Hierarchy Analysis

FQC scale: 1=grain_compressed (pure whole grain) → 5=refined_only.

| FQC | Count | Avg Score | Examples                                   |
|-----|-------|-----------|--------------------------------------------|
| 1   | 2     | 79.3      | לחמי קריספ שיפון פשו; לחמי קריספ מחמצת שיפ |
| 2   | 6     | 77.3      | קרקר חיטה מלאה פשוט; לחמי קריספ "14 גרם ס  |
| 3   | 9     | 63.6      | עוגיות אורז ללא מלח; לחם "100% חיטה מלאה"  |
| 4   | 1     | 55.2      | קרקרים "שבעת המינים"                       |
| 5   | 13    | 55.6      | לחם לבן פרוס פשוט; קרקר מלוח פריך          |

## Fermentation Quality Analysis

| Quality | Count | Avg Score | Avg GSS | Notes |
|---------|-------|-----------|---------|-------|
| traditional | 3 | 74.0 | 79.2 | |
| flavor_only | 2 | 67.5 | 38.5 | |
| none | 26 | 62.2 | 45.9 | |

## Fiber Source Quality Analysis

| Fiber Quality | Count | Avg Score |
|---------------|-------|-----------|
| structural    | 25    | 63.9      |
| hybrid        | 1     | 73.5      |
| isolated      | 5     | 60.4      |

## Seed Semantics Analysis

| Seed Role  | Count | Avg Score |
|------------|-------|-----------|
| halo       | 4     | 71.2      |
| decorative | 2     | 55.0      |
| none       | 25    | 63.1      |