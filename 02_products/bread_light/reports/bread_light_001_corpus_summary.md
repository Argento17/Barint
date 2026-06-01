# Bread-Light Stress Test — Corpus Summary

**Run:** run_bread_light_001  **Date:** 2026-05-20  **Products:** 32

## Group Distribution

| Group | Count | Avg Score | Categories Assigned                                |
|-------|-------|-----------|----------------------------------------------------|
| A     | 5     | 67.8      | beverage, default, whole_food_fat                  |
| B     | 6     | 64.8      | cereal, default, snack_bar_granola, whole_food_fat |
| C     | 5     | 65.5      | default, snack_bar_granola, whole_food_fat         |
| D     | 5     | 70.8      | default, whole_food_fat                            |
| E     | 6     | 62.8      | dairy_protein, default, whole_food_fat             |
| F     | 5     | 43.4      | snack_bar_granola, whole_food_fat                  |

## Routing Distribution

**No bread/cracker category exists in router_v2.** All products route to grain-adjacent categories.

| Category          | Count | Share |
|-------------------|-------|-------|
| default           | 12    | 38%   |
| whole_food_fat    | 11    | 34%   |
| snack_bar_granola | 4     | 12%   |
| cereal            | 2     | 6%    |
| dairy_protein     | 2     | 6%    |
| beverage          | 1     | 3%    |

### Key Routing Finding

The router has no bread/cracker archetype. Bread products disperse across:
- `default` — plain bread, no dominant signal
- `whole_food_fat` — seeds/nuts in ingredient list contaminate routing
- `cereal` — grain tokens overlap (oats, multi-grain names)
- `snack_bar_granola` — sweet crackers or nutrition claims trigger snack signals
- `beverage` — rice cakes triggered plant_milk_name_heuristic (false positive on 'אורז')
- `dairy_protein` — protein crackers with whey/pea isolate contaminate routing

## Score Distribution

| Grp | Product                           | Score | Grade | Category          | SC |
|-----|-----------------------------------|-------|-------|-------------------|----|
| A   | עוגיות אורז ללא מלח               | 85    | A     | beverage          | A  |
| A   | קרקר חיטה מלאה פשוט               | 82.7  | A     | whole_food_fat    | B  |
| A   | לחמי קריספ שיפון פשוט             | 78.6  | B     | default           | B  |
| A   | לחם לבן פרוס פשוט                 | 56.9  | C     | default           | D  |
| A   | קרקר מלוח פריך                    | 36.0  | D     | whole_food_fat    | D  |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | 76.5  | B     | whole_food_fat    | D  |
| B   | לחם "100% חיטה מלאה" מעורב        | 68.9  | B     | default           | D  |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | 68.1  | B     | cereal            | D  |
| B   | קרקר "בטא-גלוקן" תומך בלב         | 63.5  | C     | cereal            | D  |
| B   | קרקרים "5 דגנים" ושיפון           | 58.9  | C     | snack_bar_granola | D  |
| B   | לחם "7 דגנים" תעשייתי             | 53.0  | C     | default           | E  |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | 81.6  | A     | whole_food_fat    | D  |
| C   | לחם גרעינים אמיתי                 | 76.5  | B     | default           | D  |
| C   | קרקרים "שבעת המינים" גרעינים      | 59.1  | C     | whole_food_fat    | D  |
| C   | קרקר "גרעינים זהובים" פרמיום      | 57.9  | C     | whole_food_fat    | D  |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | 52.6  | C     | snack_bar_granola | D  |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | 79.0  | B     | default           | B  |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | 78.6  | B     | default           | B  |
| D   | לחם כפרי "מחמצת ושמרים"           | 68.0  | B     | default           | D  |
| D   | קרקר "מחמצת" בייצור מהיר          | 65.8  | B     | whole_food_fat    | D  |
| D   | לחם "בסגנון מחמצת" תעשייתי        | 62.5  | C     | default           | D  |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | 71.1  | B     | dairy_protein     | D  |
| E   | לחם חלבון ואגוזים "נוטרישן"       | 70.9  | B     | default           | D  |
| E   | קרקר "סיבים+" אינולין וסיליום     | 69.0  | B     | whole_food_fat    | D  |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | 66.6  | B     | dairy_protein     | D  |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | 50.0  | C     | default           | D  |
| E   | לחם "קטו" דל פחמימות              | 49.0  | D     | default           | F  |
| F   | עוגיות אורז "חמאה" שמן דקל        | 60.4  | C     | whole_food_fat    | D  |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | 46.5  | D     | snack_bar_granola | F  |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | 45.8  | D     | whole_food_fat    | E  |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | 35.3  | D     | snack_bar_granola | D  |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | 29.0  | E     | whole_food_fat    | E  |