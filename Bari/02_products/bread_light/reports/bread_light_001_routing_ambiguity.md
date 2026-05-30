# Bread-Light — Routing Ambiguity Report

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Overview

Router v2 has no bread/cracker category. This report documents every routing
decision that reflects an ontological gap — not a bug, but a missing archetype.

## Routing by Product

| Grp | Product                           | Category          | Struct.Class | Unstable? | Secondary         |
|-----|-----------------------------------|-------------------|--------------|-----------|-------------------|
| A   | עוגיות אורז ללא מלח               | beverage          | A            | no        | —                 |
| A   | קרקר חיטה מלאה פשוט               | whole_food_fat    | B            | YES       | snack_bar_granola |
| A   | לחמי קריספ שיפון פשוט             | default           | B            | YES       | —                 |
| A   | לחם לבן פרוס פשוט                 | default           | D            | no        | dairy_protein     |
| A   | קרקר מלוח פריך                    | whole_food_fat    | D            | YES       | snack_bar_granola |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | whole_food_fat    | D            | YES       | snack_bar_granola |
| B   | לחם "100% חיטה מלאה" מעורב        | default           | D            | no        | whole_food_fat    |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | cereal            | D            | YES       | whole_food_fat    |
| B   | קרקר "בטא-גלוקן" תומך בלב         | cereal            | D            | YES       | whole_food_fat    |
| B   | קרקרים "5 דגנים" ושיפון           | snack_bar_granola | D            | no        | cereal            |
| B   | לחם "7 דגנים" תעשייתי             | default           | E            | no        | snack_bar_granola |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | whole_food_fat    | D            | no        | —                 |
| C   | לחם גרעינים אמיתי                 | default           | D            | no        | whole_food_fat    |
| C   | קרקרים "שבעת המינים" גרעינים      | whole_food_fat    | D            | no        | —                 |
| C   | קרקר "גרעינים זהובים" פרמיום      | whole_food_fat    | D            | no        | —                 |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | snack_bar_granola | D            | YES       | whole_food_fat    |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | default           | B            | no        | —                 |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | default           | B            | YES       | —                 |
| D   | לחם כפרי "מחמצת ושמרים"           | default           | D            | no        | whole_food_fat    |
| D   | קרקר "מחמצת" בייצור מהיר          | whole_food_fat    | D            | YES       | snack_bar_granola |
| D   | לחם "בסגנון מחמצת" תעשייתי        | default           | D            | no        | —                 |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | dairy_protein     | D            | no        | —                 |
| E   | לחם חלבון ואגוזים "נוטרישן"       | default           | D            | no        | whole_food_fat    |
| E   | קרקר "סיבים+" אינולין וסיליום     | whole_food_fat    | D            | YES       | snack_bar_granola |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | dairy_protein     | D            | no        | —                 |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | default           | D            | no        | whole_food_fat    |
| E   | לחם "קטו" דל פחמימות              | default           | F            | no        | whole_food_fat    |
| F   | עוגיות אורז "חמאה" שמן דקל        | whole_food_fat    | D            | no        | —                 |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | snack_bar_granola | F            | no        | —                 |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | whole_food_fat    | E            | YES       | snack_bar_granola |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | snack_bar_granola | D            | no        | —                 |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | whole_food_fat    | E            | YES       | snack_bar_granola |

## Specific Failure Modes

### 1. WFF Contamination (whole_food_fat false positives)

Products with seeds or nuts in the ingredient list receive whole_food_fat WFF signals.
For bread products, seeds are a secondary ingredient (5-20%) not the structural identity.

- **קרקר חיטה מלאה פשוט** [Grp A]: `קמח חיטה מלאה (75%), קמח חיטה, מלח, שמרים, שמן זית (3%)...`
- **קרקר מלוח פריך** [Grp A]: `קמח חיטה, שמן דקל, מלח, סוכר, שמרים, לציטין סויה (E-322), E-471, נתרן ביקרבונט (E-500)...`
- **לחמי קריספ "14 גרם סיבים" תאית** [Grp B]: `קמח חיטה מלאה (60%), קמח חיטה (20%), סיבי תאית (8%), מלח, שמרים, שמן צמחי...`
- **לחמי קריספ שיפון וגרעינים נורדי** [Grp C]: `קמח שיפון מלא (65%), זרעי חמנייה (12%), זרעי פשתן (8%), זרעי שומשום (5%), מלח, שמרים...`
- **קרקרים "שבעת המינים" גרעינים** [Grp C]: `קמח חיטה, שמן סויה, מלח, גרגרי שיבולת שועל (4%), שומשום (3%), כוסמין (2%), זרעי פשתן (2%), זרעי חמנייה (2%), לציטין (E-3...`
- **קרקר "גרעינים זהובים" פרמיום** [Grp C]: `קמח חיטה, שמן קנולה, זרעי שומשום מזהב (5%), מלח, דבש (2%), לציטין (E-322), E-471, E-481...`
- **קרקר "מחמצת" בייצור מהיר** [Grp D]: `קמח חיטה (65%), קמח שיפון (20%), מחמצת (5%), מלח, שמן קנולה, E-450, E-500, חומצה לקטית...`
- **קרקר "סיבים+" אינולין וסיליום** [Grp E]: `קמח חיטה (50%), אינולין מצ'יקורי (12%), קמח שיפון (15%), psyllium husk (5%), מלח, שמן קנולה, לציטין (E-322), E-450, E-50...`
- **עוגיות אורז "חמאה" שמן דקל** [Grp F]: `אורז (80%), שמן דקל (8%), ארומה חמאה, מלח, לציטין (E-322), E-471, מעכב חמצון E-320...`
- **לחמי קריספ "שום ועשבים" תעשייתי** [Grp F]: `קמח חיטה (65%), שמן קנולה (10%), אבקת גבינה (3%), ארומה שום (0.5%), E-621, E-627, E-631, מלח, לציטין (E-322), E-471, E-5...`
- **קרקרים מתוקים לילדים "גולדה קידס"** [Grp F]: `קמח חיטה, שמן דקל, עמילן תפוחי אדמה, מלח, אבקת גבינה (5%), חלב אבקה, E-621, צבע: E-160c, לציטין (E-322), E-471, E-481, ו...`

### 2. Beverage False Positive (rice cake routing)

- **עוגיות אורז ללא מלח** routed to `beverage` via `plant_milk_name_heuristic`.
  - Trigger: 'אורז' (rice) in name matched plant-milk brand heuristic
  - This is a false positive: rice cake ≠ rice milk
  - NOVA 1 floor rescued the score (85, A), but category is wrong
  - **Fix needed:** Add 'אורז' exclusion to plant-milk heuristic when product is solid
    (cracker/crispbread/עוגיות signal in name should suppress beverage bypass)

### 3. Dairy-Protein Contamination (protein crackers)

Products 022 and 024 (protein crackers with whey/pea isolate) routed to `dairy_protein`.
The protein isolate signals are real but the product is still a bread/cracker form.
Dairy_protein routing applies incorrect calorie_density interpretation for a cracker.

- **לחמי קריספ חלבון ופשתן "17 גרם"** [Grp E]: `קמח שיפון מלא (45%), חלבון מי גבינה מרוכז (15%), קמח חיטה מלאה (20%), פשתן (8%), מלח, שמרים, לציטין (E-322)...`
- **קרקר חלבון 30 "פרוטין קריספ"** [Grp E]: `קמח שיפון (35%), חלבון אפונה מבודד (20%), קמח חיטה (20%), גלוטן חיטה (10%), שמן קנולה, מלח, לציטין (E-322), E-471, E-450...`

### 4. Snack-Bar Routing (sweet crackers)

Sweet crackers and kids products route to snack_bar_granola. This is partially correct
(they share the snack consumption context) but loses the grain-structure interpretation.

- **קרקרים "5 דגנים" ושיפון** [Grp B]: score=58.9, grade=C
- **קרקר "פשתן וצ'יה" סופר-פוד** [Grp C]: score=52.6, grade=C
- **עוגיות אורז שוקולד "בלה שוקו"** [Grp F]: score=46.5, grade=D
- **פצפוצי דגנים "פצ'פץ'" בטעם דבש** [Grp F]: score=35.3, grade=D

## Routing Gap: Missing 'bread' Archetype

**Root cause:** Router v2 was designed for snack bars, cereals, yogurt, and milk.
Bread/crackers have no dedicated archetype. Required additions for a proper bread expansion:

1. `bread` — yeasted/sourdough loaves (refined and whole grain)
2. `cracker` — baked flat crisp (savory and sweet)
3. `crispbread` / `knäckebröd` — leavened-free grain-compressed formats

Until these exist, bread products will continue to disperse across existing categories.
This is expected behavior for a stress test, not a scoring error.