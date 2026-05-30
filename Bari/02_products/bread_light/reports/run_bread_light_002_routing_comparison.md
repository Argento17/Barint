# Bread-Light — Routing Comparison: run_001 vs run_002

**Date:** 2026-05-20

## Change Summary

| Change | Description |
|--------|-------------|
| Router upgrade | v1→v2 (3-stage anchor/signal/resolution) |
| New categories | `bread`, `cracker`, `crispbread` hard anchors and signal sets |
| WFF gate extended | Bakery exclusions added to WFF context gate |
| Beverage gate | `עוגיות`/`קרקר`/`לחם` added to solid-food exclusion list |
| Bakery Semantics Layer | Flour hierarchy, fermentation, fiber, seed analysis |

## Per-Product Routing Change

| Grp | Product                           | Cat v1            | Cat v2            | Changed? | Score v1 | Score v2 | Δ Score |
|-----|-----------------------------------|-------------------|-------------------|----------|----------|----------|---------|
| A   | עוגיות אורז ללא מלח               | beverage          | cracker           | CHANGED  | 85       | 85       | 0       |
| A   | קרקר חיטה מלאה פשוט               | whole_food_fat    | cracker           | CHANGED  | 82.7     | 79.7     | -3.0    |
| A   | לחמי קריספ שיפון פשוט             | default           | crispbread        | CHANGED  | 78.6     | 79.3     | +0.7    |
| A   | לחם לבן פרוס פשוט                 | default           | bread             | CHANGED  | 56.9     | 59.2     | +2.3    |
| A   | קרקר מלוח פריך                    | whole_food_fat    | cracker           | CHANGED  | 36.0     | 36.0     | 0.0     |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | whole_food_fat    | crispbread        | CHANGED  | 76.5     | 73.5     | -3.0    |
| B   | לחם "100% חיטה מלאה" מעורב        | default           | bread             | CHANGED  | 68.9     | 71.1     | +2.2    |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | cereal            | cracker           | CHANGED  | 68.1     | 68.1     | 0.0     |
| B   | קרקר "בטא-גלוקן" תומך בלב         | cereal            | cracker           | CHANGED  | 63.5     | 65.8     | +2.3    |
| B   | קרקרים "5 דגנים" ושיפון           | snack_bar_granola | cracker           | CHANGED  | 58.9     | 63.4     | +4.5    |
| B   | לחם "7 דגנים" תעשייתי             | default           | bread             | CHANGED  | 53.0     | 53.0     | 0.0     |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | whole_food_fat    | crispbread        | CHANGED  | 81.6     | 79.4     | -2.2    |
| C   | לחם גרעינים אמיתי                 | default           | bread             | CHANGED  | 76.5     | 77.2     | +0.7    |
| C   | קרקרים "שבעת המינים" גרעינים      | whole_food_fat    | cracker           | CHANGED  | 59.1     | 55.2     | -3.9    |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | snack_bar_granola | cracker           | CHANGED  | 52.6     | 54.8     | +2.2    |
| C   | קרקר "גרעינים זהובים" פרמיום      | whole_food_fat    | cracker           | CHANGED  | 57.9     | 53.4     | -4.5    |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | default           | crispbread        | CHANGED  | 78.6     | 79.4     | +0.8    |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | default           | bread             | CHANGED  | 79.0     | 79.0     | 0.0     |
| D   | לחם כפרי "מחמצת ושמרים"           | default           | bread             | CHANGED  | 68.0     | 70.3     | +2.3    |
| D   | לחם "בסגנון מחמצת" תעשייתי        | default           | bread             | CHANGED  | 62.5     | 64.8     | +2.3    |
| D   | קרקר "מחמצת" בייצור מהיר          | whole_food_fat    | cracker           | CHANGED  | 65.8     | 63.5     | -2.3    |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | dairy_protein     | crispbread        | CHANGED  | 71.1     | 74.9     | +3.8    |
| E   | לחם חלבון ואגוזים "נוטרישן"       | default           | bread             | CHANGED  | 70.9     | 71.7     | +0.8    |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | dairy_protein     | cracker           | CHANGED  | 66.6     | 69.0     | +2.4    |
| E   | קרקר "סיבים+" אינולין וסיליום     | whole_food_fat    | cracker           | CHANGED  | 69.0     | 67.0     | -2.0    |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | default           | bread             | CHANGED  | 50.0     | 52.3     | +2.3    |
| E   | לחם "קטו" דל פחמימות              | default           | bread             | CHANGED  | 49.0     | 49.0     | 0.0     |
| F   | עוגיות אורז "חמאה" שמן דקל        | whole_food_fat    | cracker           | CHANGED  | 60.4     | 58.1     | -2.3    |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | snack_bar_granola | cracker           | CHANGED  | 46.5     | 51.0     | +4.5    |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | whole_food_fat    | crispbread        | CHANGED  | 45.8     | 40.6     | -5.2    |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | snack_bar_granola | snack_bar_granola | same     | 35.3     | 35.3     | 0.0     |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | whole_food_fat    | cracker           | CHANGED  | 29.0     | 28.4     | -0.6    |

## Summary

- **Total products:** 32
- **Routing changed:** 31 products
- **Now correctly in bakery category:** 31 products
- **Remaining non-bakery:** 1

## Non-Bakery Remaining Cases

- **פצפוצי דגנים "פצ'פץ'" בטעם דבש** [Grp F]: cat=`snack_bar_granola`, score=35.3
  - Design note: STRUCTURAL VOID — corn puff product. Honey at 2% is a flavor token justifying 'natural honey taste' marketing. BHA/BHT antioxidants (E-320/E-321) in cheap oil. Trans fat from palm. 'ללא קולורנטים מלאכותיים' claim but has artificial flavoring. Classic hyper-palatable corn snack in bakery format.

## Routing Failure Modes Resolved

### 1. WFF Contamination — RESOLVED

Router v2 adds `עוגיות`, `קרקר`, `לחם`, `פריכיות`, `בגט`, `לחמנייה`, `פיתה`
to the WFF context gate exclusion list. Seed/nut signals in ingredient text are now
suppressed when the product name contains a bakery solid-food term.

### 2. Beverage False Positive (rice cakes) — RESOLVED

`עוגיות` is now in `_PLANT_MILK_SOLID_EXCL`. 'עוגיות אורז' no longer triggers the
plant-milk name heuristic. Rice cakes route to `cracker` via the 'פריכיות'/'עוגיות אורז'
hard anchors.

### 3. Dairy-Protein Contamination — RESOLVED

Protein crackers now anchor to `cracker` before protein/dairy signals fire.
Hard anchors take priority over signal scoring, preventing cross-category contamination.

### 4. Default Routing Dispersion — RESOLVED

Products that previously accumulated no dominant signal and fell to `default` now
anchor via `לחם`/`קרקר`/`לחמי קריספ`/`פריכיות` terms in their names.