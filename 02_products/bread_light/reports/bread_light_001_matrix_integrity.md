# Bread-Light — Matrix Integrity Observations

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Purpose

Matrix integrity engine v2 interprets structural food composition: intact grain vs
flour degradation, whole-grain presence vs refining, additive scaffolding.
This report documents how it performs on bread/cracker products.

## NOVA Distribution

| NOVA Proxy | Count |
|------------|-------|
| 1          | 1     |
| 2          | 4     |
| 3          | 23    |
| 4          | 4     |

## Product-Level Matrix Signal Summary

| Grp | Product                           | NOVA | WG? | Ferm? | Additives | Matrix Markers                 |
|-----|-----------------------------------|------|-----|-------|-----------|--------------------------------|
| A   | עוגיות אורז ללא מלח               | 1    | YES | no    | 0         | —                              |
| A   | קרקר חיטה מלאה פשוט               | 2    | YES | YES   | 0         | —                              |
| A   | לחמי קריספ שיפון פשוט             | 2    | no  | no    | 0         | —                              |
| A   | לחם לבן פרוס פשוט                 | 3    | no  | YES   | 3         | —                              |
| A   | קרקר מלוח פריך                    | 3    | no  | YES   | 3         | —                              |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | 3    | YES | YES   | 0         | סיבי תאית                      |
| B   | לחם "100% חיטה מלאה" מעורב        | 3    | YES | YES   | 2         | —                              |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | 3    | no  | no    | 2         | אינולין                        |
| B   | קרקר "בטא-גלוקן" תומך בלב         | 3    | no  | no    | 3         | אינולין, בטא-גלוקן             |
| B   | קרקרים "5 דגנים" ושיפון           | 3    | no  | no    | 3         | —                              |
| B   | לחם "7 דגנים" תעשייתי             | 3    | YES | YES   | 5         | —                              |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | 3    | no  | YES   | 0         | —                              |
| C   | לחם גרעינים אמיתי                 | 3    | YES | YES   | 0         | —                              |
| C   | קרקרים "שבעת המינים" גרעינים      | 3    | no  | no    | 3         | —                              |
| C   | קרקר "גרעינים זהובים" פרמיום      | 3    | no  | no    | 2         | —                              |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | 3    | no  | no    | 3         | —                              |
| D   | לחם מחמצת אמיתי ממחיטה מלאה       | 2    | YES | YES   | 0         | —                              |
| D   | לחמי קריספ מחמצת שיפון מסורתי     | 2    | no  | YES   | 0         | —                              |
| D   | לחם כפרי "מחמצת ושמרים"           | 3    | YES | YES   | 2         | —                              |
| D   | קרקר "מחמצת" בייצור מהיר          | 3    | no  | YES   | 2         | —                              |
| D   | לחם "בסגנון מחמצת" תעשייתי        | 3    | no  | YES   | 3         | —                              |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | 3    | YES | YES   | 1         | —                              |
| E   | לחם חלבון ואגוזים "נוטרישן"       | 3    | YES | YES   | 2         | —                              |
| E   | קרקר "סיבים+" אינולין וסיליום     | 3    | no  | no    | 3         | אינולין, psyllium, psyllium hu |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | 3    | no  | no    | 3         | —                              |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | 3    | no  | YES   | 4         | גואר, קסנטן                    |
| E   | לחם "קטו" דל פחמימות              | 4    | no  | no    | 1         | אינולין, psyllium, psyllium hu |
| F   | עוגיות אורז "חמאה" שמן דקל        | 3    | no  | no    | 3         | —                              |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | 4    | no  | no    | 2         | —                              |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | 4    | no  | no    | 4         | —                              |
| F   | פצפוצי דגנים "פצ'פץ'" בטעם דבש    | 3    | no  | no    | 3         | —                              |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | 4    | no  | no    | 3         | —                              |

## Key Matrix Integrity Observations

### Whole-Grain Detection

The whole_grain signal fires on Hebrew terms (חיטה מלאה, שיפון מלא, שיבולת שועל מלאה).
This correctly captures genuine whole-grain products but cannot distinguish:
- Whole grain as primary flour (>50%) vs minor ingredient
- Structural whole grain (milled into dough) vs decorative inclusions

Group B products (wholegrain halo) all trigger `has_whole_grain=True` despite
refined flour being the first ingredient in 4/6 products.

### Fermentation Detection

Fermentation markers (מחמצת) correctly fire on Group D products.
However, the engine cannot distinguish:
- Genuine live-culture sourdough (mchmatset with long fermentation)
- Dehydrated sourdough powder (2-5% as flavor agent, no leavening function)
- Industrial bread with a small percentage of sourdough for flavor

Group D products D3-D4 (industrial sourdough-style) contain 'מחמצת שייפון' as a
minor flavor additive but receive the same fermentation signal as D1-D2 (genuine).

### Additive Categories

Additive detection works correctly across Group F. The NOVA proxy correctly assigns
NOVA 4 to products with emulsifiers + palm oil + artificial flavors.

### Matrix Markers (Isolated Fiber)

Products with extracted_matrix_markers (inulin, psyllium, cellulose) are correctly
flagged. However, the matrix integrity engine does not currently penalize the
COMBINATION of: isolated fiber + refined flour + whole_grain claim.
This fiber laundering pattern is present in products B4, B5, B6, E5.
These products score higher than their structural integrity warrants.