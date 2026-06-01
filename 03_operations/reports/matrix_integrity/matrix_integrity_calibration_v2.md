# Matrix Integrity Engine — Calibration Comparison Report

**v1 (baseline):** `matrix_integrity_v1_archive`
**v2 (calibrated):** `matrix_integrity_v2`
**Run date:** 2026-05-20 05:46 UTC
**Products evaluated:** 163

## What Changed in v2

| Change | Effect |
|--------|--------|
| Supplemental mechanical scan | Rolled oats, granola, muesli now get soft degradation signals |
| Assembly complexity drag (0–12) | Products with 3+ ingredients accumulate mild drag |
| Fortification nuance | basic_restoration ≤10 pts; wellness_engineering up to 28 pts |
| HP triad: position weighting | Early-position signals amplified ×1.1–1.2 |
| HP triad: false-positive guard | Single flavor on clean matrix halved |
| HP triad: matrix amplification | Degraded matrix + HP amplified ×1.12 |
| Transformation type classification | New A/B/C/D taxonomy in trace |
| Provenance trace block | Human-readable signal lists per product |

---

## Overall Score Distribution: v1 vs v2

| Score Range      | v1 Count | v2 Count | Δ   |
|------------------|----------|----------|-----|
| 90-100 (minimal) | 89       | 75       | -14 |
| 75-89 (low)      | 22       | 29       | 7   |
| 58-74 (moderate) | 37       | 26       | -11 |
| 40-57 (high)     | 14       | 29       | 15  |
| 22-39 (severe)   | 1        | 4        | 3   |
| 0-21 (extreme)   | 0        | 0        | 0   |

**Products at score = 100:** v1 = 51,  v2 = 24  (-27 change)

**Products at score ≥ 95:** v1 = 71,   v2 = 51  (-20 change)

## Per-Category Score Summary

| Category   | N  | v1 Min | v1 Avg | v1 Max | v2 Min | v2 Avg | v2 Max | Avg Δ |
|------------|----|--------|--------|--------|--------|--------|--------|-------|
| snack_bars | 53 | 36.9   | 70.6   | 100.0  | 30.8   | 61.5   | 100.0  | -9.0  |
| cereals    | 45 | 51.3   | 85.7   | 100.0  | 42.4   | 80.0   | 100.0  | -5.7  |
| yogurt     | 45 | 86.4   | 96.6   | 100.0  | 80.2   | 94.8   | 100.0  | -1.9  |
| milk       | 20 | 83.7   | 96.8   | 100.0  | 83.7   | 93.4   | 100.0  | -3.3  |

## Largest Score Changes (v2 vs v1)

### Products Most Reduced (top 10 largest drops)

| Product                                            | Category   | v1 Score | v2 Score | Δ     | Drag | Transform Type              |
|----------------------------------------------------|------------|----------|----------|-------|------|-----------------------------|
| מרבה סלים דליס קריספי תות 125 גר                   | snack_bars | 59.5     | 44.8     | -14.7 | 12.0 | mechanical_degradation      |
| חטיף דגנים עם פירות יער                            | snack_bars | 68.4     | 54.0     | -14.4 | 12.0 | reconstruction_compensation |
| חטיפי דגנים פיטנס קרם ועוגיות שישייה               | snack_bars | 69.5     | 55.2     | -14.3 | 12.0 | reconstruction_compensation |
| פיטנס בר גרנולה שוקולד מריר                        | snack_bars | 63.2     | 48.9     | -14.3 | 12.0 | mechanical_degradation      |
| שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם  | snack_bars | 52.7     | 38.6     | -14.1 | 11.8 | mechanical_degradation      |
| חטיף דגנים שוקו וניל נסטלה שישייה                  | snack_bars | 51.4     | 37.3     | -14.1 | 11.6 | reconstruction_compensation |
| חטיפי דגנים פיטנס שוקולד בננה שישייה               | snack_bars | 74.6     | 60.5     | -14.1 | 12.0 | reconstruction_compensation |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישי | snack_bars | 74.2     | 60.1     | -14.1 | 12.0 | mechanical_degradation      |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח'  | snack_bars | 44.8     | 30.8     | -14.0 | 12.0 | reconstruction_compensation |
| חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם נ | snack_bars | 57.1     | 43.3     | -13.8 | 11.6 | mechanical_degradation      |

### Products Most Increased (should be rare)

| Product            | Category | v1 Score | v2 Score | Δ    | Fortif Type |
|--------------------|----------|----------|----------|------|-------------|
| יוגורט שיבולת שועל | yogurt   | 93.0     | 93.9     | +0.9 | none        |

## A. Soft Degradation Ladder

Products with soft supplemental signals detected — showing how rolling, flaking, and clustering now introduce mild structural friction.

| Product                                          | Category | v1    | v2   | Δ    | Supplemental Signal                           |
|--------------------------------------------------|----------|-------|------|------|-----------------------------------------------|
| שיבולת שועל מהירה קוואקר 500 גרם                 | cereals  | 100.0 | 96.7 | -3.3 | rolled_oats at position 1 (text match: 'שיבול |
| שיבולת שועל גרוסה ספרוגרן 500 גרם                | cereals  | 100.0 | 96.7 | -3.3 | rolled_oats at position 1 (text match: 'שיבול |
| שיבולת שועל גלגולה קוואקר 500 גרם                | cereals  | 100.0 | 96.7 | -3.3 | rolled_oats at position 1 (text match: 'שיבול |
| שיבולת שועל מלאה תלמה 500 גרם                    | cereals  | 100.0 | 96.7 | -3.3 | rolled_oats at position 1 (text match: 'שיבול |
| סובין שיבולת שועל 400 גרם                        | cereals  | 100.0 | 96.7 | -3.3 | rolled_oats at position 1 (text match: 'שיבול |
| בסיס שיבולת שועל לילה עם זרעי צ'יה ופשתן 400 גרם | cereals  | 100.0 | 96.1 | -3.9 | rolled_oats at position 1 (text match: 'שיבול |
| מוסלי בירכר בסיס 500 גרם                         | cereals  | 100.0 | 94.7 | -5.3 | rolled_oats at position 1 (text match: 'שיבול |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם     | cereals  | 100.0 | 94.4 | -5.6 | rolled_oats at position 1 (text match: 'שיבול |
| משקה בריסטה שיבולת שועל                          | milk     | 100.0 | 94.4 | -5.6 | rolled_oats at position 2 (text match: 'שיבול |
| משקה שיבולת שועל ללא סוכר                        | milk     | 100.0 | 94.4 | -5.6 | rolled_oats at position 2 (text match: 'שיבול |
| משקה בריסטה שיבולת שועל להקצפה                   | milk     | 100.0 | 94.4 | -5.6 | rolled_oats at position 2 (text match: 'שיבול |
| דגני בוקר פתיתי דגנים מלאים מעורבים 375 גרם      | cereals  | 100.0 | 94.2 | -5.8 | rolled_oats at position 3 (text match: 'שיבול |

### Assembly Drag Examples (products previously at 100)

| Product                           | Category   | v1 (was 100) | v2 Score | Drag | Transform Type            |
|-----------------------------------|------------|--------------|----------|------|---------------------------|
| חטיף תמרים במילוי חמאת שקדים      | snack_bars | 100.0        | 99.0     | 1.0  | minimal_transformation    |
| חטיף תמרים במילוי חמאת בוטנים     | snack_bars | 100.0        | 99.0     | 1.0  | minimal_transformation    |
| יוגורט טבעי 5% שומן יוטבתה        | yogurt     | 100.0        | 99.0     | 1.0  | traditional_transformatio |
| יוגורט יווני 10% שומן פאג'        | yogurt     | 100.0        | 99.0     | 1.0  | traditional_transformatio |
| סקיר טבעי 0.2% שומן               | yogurt     | 100.0        | 99.0     | 1.0  | traditional_transformatio |
| משקה אורז אורגני                  | milk       | 100.0        | 99.0     | 1.0  | minimal_transformation    |
| יוגורט תות 1.5% שומן              | yogurt     | 100.0        | 98.6     | 1.4  | traditional_transformatio |
| יוגורט ילדים תות טבעי             | yogurt     | 100.0        | 98.6     | 1.4  | traditional_transformatio |
| יוגורט נטול לקטוז 1.5%            | yogurt     | 100.0        | 98.6     | 1.4  | traditional_transformatio |
| יוגורט יווני נטול לקטוז           | yogurt     | 100.0        | 98.6     | 1.4  | traditional_transformatio |
| סקיר תות                          | yogurt     | 100.0        | 97.1     | 2.9  | traditional_transformatio |
| שיבולת שועל מהירה קוואקר 500 גרם  | cereals    | 100.0        | 96.7     | 0.0  | traditional_transformatio |
| שיבולת שועל גרוסה ספרוגרן 500 גרם | cereals    | 100.0        | 96.7     | 0.0  | traditional_transformatio |
| שיבולת שועל גלגולה קוואקר 500 גרם | cereals    | 100.0        | 96.7     | 0.0  | traditional_transformatio |
| שיבולת שועל מלאה תלמה 500 גרם     | cereals    | 100.0        | 96.7     | 0.0  | traditional_transformatio |

## B. Traditional Transformation — Correctly Handled

Products where strong fermentation or traditional processing is recognized and does NOT receive unfair penalty.

| Product                    | Category | v1    | v2    | Δ    | Ferm Factor | Transform Type            |
|----------------------------|----------|-------|-------|------|-------------|---------------------------|
| יוגורט טבעי 1.5% שומן      | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט טבעי 3% שומן        | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט עיזים 9% שומן       | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט יווני 0% שומן       | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט יווני 2% שומן       | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט יווני 5% שומן       | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| לבן שתייה 3% שומן          | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט יווני חלבון 18 טהור | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| יוגורט סויה טבעי           | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |
| לבן שתייה 3% טנובה         | yogurt   | 100.0 | 100.0 | +0.0 | 0.40        | traditional_transformatio |

## C. Engineered Wellness Halo — Correctly Penalized

Products with high integrity scores that also carry engineering signals — potential 'clean' appearance masking compensation systems.

_No wellness_engineering fortification detected._

## D. Structural Void — Primary Position Occupied by Refined Sweetener

| Product                                          | Category   | v1   | v2   | Δ     | Primary Signal                       |
|--------------------------------------------------|------------|------|------|-------|--------------------------------------|
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח | snack_bars | 44.8 | 30.8 | -14.0 | pos2_primary_sweetener:glucose_syrup |
| חטיף דגנים שוקו וניל נסטלה שישייה                | snack_bars | 51.4 | 37.3 | -14.1 | pos2_primary_sweetener:glucose_syrup |
| דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם     | cereals    | 51.3 | 42.4 | -8.9  | pos2_primary_sweetener:added_sugar   |
| דגני בוקר קוקו פופס קלוגס 375 גרם                | cereals    | 51.7 | 43.2 | -8.5  | pos2_primary_sweetener:added_sugar   |
| חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה     | snack_bars | 55.6 | 43.4 | -12.2 | pos1_primary_sweetener:glucose_syrup |
| דגני בוקר סמאקס דבש קלוגס 330 גרם                | cereals    | 52.3 | 44.2 | -8.1  | pos2_primary_sweetener:added_sugar   |
| קוקומן חטיף פצפוצי דגנים בטעם שוקולד 6 יח'       | snack_bars | 57.7 | 46.5 | -11.2 | pos2_primary_sweetener:added_sugar   |
| פיטנס בר גרנולה שוקולד מריר                      | snack_bars | 63.2 | 48.9 | -14.3 | pos2_primary_sweetener:added_sugar   |
| מרבה סלים דליס מהדורה מיוחדת שוקולד חלב          | snack_bars | 60.5 | 49.4 | -11.1 | pos1_primary_sweetener:added_sugar   |
| קורני חטיפי דגנים שוקולד מריר 58% קקאו           | snack_bars | 63.7 | 51.0 | -12.7 | pos1_primary_sweetener:added_sugar   |

## HP Triad Behaviour Changes

| Product                                          | Category   | v1 HP | v2 HP | HP Δ | v1 Score | v2 Score |
|--------------------------------------------------|------------|-------|-------|------|----------|----------|
| מרבה סלים דליס קריספי אוכמניות 125 גר            | snack_bars | 75    | 100   | +25  | 36.9     | 33.3     |
| חטיף דגנים שוקו וניל נסטלה שישייה                | snack_bars | 45    | 64    | +19  | 51.4     | 37.3     |
| מרבה סלים דליס קריספי תות 125 גר                 | snack_bars | 45    | 64    | +19  | 59.5     | 44.8     |
| שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קר | snack_bars | 85    | 100   | +15  | 52.7     | 38.6     |
| קורני חטיפי דגנים שוקולד בננה                    | snack_bars | 85    | 100   | +15  | 44.9     | 42.6     |
| חטיפי דגנים פיטנס קרם ועוגיות שישייה             | snack_bars | 85    | 100   | +15  | 69.5     | 55.2     |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח | snack_bars | 85    | 100   | +15  | 44.8     | 30.8     |
| חטיף דגנים עם פירות יער                          | snack_bars | 85    | 100   | +15  | 68.4     | 54.0     |
| חטיפי דגנים פיטנס שוקולד בננה שישייה             | snack_bars | 85    | 100   | +15  | 74.6     | 60.5     |
| חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם | snack_bars | 85    | 100   | +15  | 57.1     | 43.3     |
| חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישיי | snack_bars | 85    | 100   | +15  | 57.1     | 43.9     |
| חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר שישייה | snack_bars | 85    | 100   | +15  | 57.1     | 43.9     |

## Fortification Nuance: restoration vs wellness_engineering

| Product                                          | Category   | v1   | v2   | Δ     | Fortification Type |
|--------------------------------------------------|------------|------|------|-------|--------------------|
| מרבה סלים דליס קריספי תות 125 גר                 | snack_bars | 59.5 | 44.8 | -14.7 | basic_restoration  |
| מרבה סלים דליס קריספי אוכמניות 125 גר            | snack_bars | 36.9 | 33.3 | -3.6  | basic_restoration  |
| חטיף דגנים שוגי שישייה 156 גרם                   | snack_bars | 65.9 | 56.1 | -9.8  | basic_restoration  |
| קוקומן חטיף פצפוצי דגנים בטעם שוקולד 6 יח'       | snack_bars | 57.7 | 46.5 | -11.2 | basic_restoration  |
| חטיף דגנים שוגי שוקו שישייה 156 גרם              | snack_bars | 65.9 | 56.1 | -9.8  | basic_restoration  |
| חטיף דגנים מלאים מצופה שוקולד חלב                | snack_bars | 63.5 | 55.4 | -8.1  | basic_restoration  |
| סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יו | snack_bars | 74.3 | 67.0 | -7.3  | basic_restoration  |
| מרבה סלים דליס שוקולד לבן חדש                    | snack_bars | 66.4 | 53.5 | -12.9 | basic_restoration  |
| מרבה סלים דליס מהדורה מיוחדת שוקולד חלב          | snack_bars | 60.5 | 49.4 | -11.1 | basic_restoration  |
| מרבה סלים דליס שוקולד לבן בטעם יוגורט            | snack_bars | 74.3 | 67.0 | -7.3  | basic_restoration  |
| וויטביקס דגני בוקר חיטה מלאה 430 גרם             | cereals    | 99.4 | 97.3 | -2.1  | basic_restoration  |
| קורנפלקס קלוגס 375 גרם                           | cereals    | 67.8 | 62.8 | -5.0  | basic_restoration  |
| קורנפלקס דגנים מלאים קלוגס 375 גרם               | cereals    | 68.2 | 62.7 | -5.5  | basic_restoration  |
| דגני בוקר ספשל K קלוגס 375 גרם                   | cereals    | 99.4 | 96.9 | -2.5  | basic_restoration  |
| דגני בוקר אול-בראן פתיתי סובין קלוגס 375 גרם     | cereals    | 88.3 | 79.9 | -8.4  | basic_restoration  |

## Snack Bars — Full Comparison

| Product                                      | v1    | v2    | Δ     | L1  | L2  | Drag | Transform              | Supp Signal                    |
|----------------------------------------------|-------|-------|-------|-----|-----|------|------------------------|--------------------------------|
| חטיף תמרים בציפוי שוקולד 100% קקאו           | 100.0 | 100.0 | +0.0  | min | min | 0.0  | minimal_transformation | —                              |
| חטיף אגוזים וחמוציות רפאלס 5*30 גרם          | 100.0 | 100.0 | +0.0  | min | min | 0.0  | minimal_transformation | —                              |
| חטיף פאי פקאן רפאלס 5*30 גרם                 | 100.0 | 100.0 | +0.0  | min | min | 0.0  | minimal_transformation | —                              |
| חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם     | 100.0 | 100.0 | +0.0  | min | min | 0.0  | minimal_transformation | —                              |
| חטיף דגנים מצופה שוקולד מריר סלים דליס       | 100.0 | 100.0 | +0.0  | min | min | 0.0  | minimal_transformation | —                              |
| חטיף תמרים במילוי חמאת שקדים                 | 100.0 | 99.0  | -1.0  | min | min | 1.0  | minimal_transformation | —                              |
| חטיף תמרים במילוי חמאת בוטנים                | 100.0 | 99.0  | -1.0  | min | min | 1.0  | minimal_transformation | —                              |
| פרי מארז 5 חטיפים תמרים ואגוזי לוז כשלפ      | 98.2  | 96.6  | -1.6  | min | min | 2.5  | minimal_transformation | —                              |
| פרי מארז חטיפי תמרים ושברי קקאו 5+1          | 98.2  | 94.6  | -3.6  | min | min | 4.5  | minimal_transformation | —                              |
| מרבה סלים דליס שוקולד מריר חדש               | 77.4  | 72.8  | -4.6  | low | mod | 4.1  | mechanical_degradation | —                              |
| קראנצ'י חטיף שיבולת שועל עם דבש חמישייה      | 76.5  | 68.9  | -7.6  | low | mod | 6.9  | minimal_transformation | —                              |
| סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטע | 74.3  | 67.0  | -7.3  | mod | mod | 6.5  | mechanical_degradation | —                              |
| מרבה סלים דליס שוקולד לבן בטעם יוגורט        | 74.3  | 67.0  | -7.3  | mod | mod | 6.5  | mechanical_degradation | —                              |
| מרבה סלים דליס שוקולד חלב ללא גלוטן חדש      | 74.3  | 66.8  | -7.5  | mod | mod | 6.5  | mechanical_degradation | —                              |
| חטיפי דגנים פיטנס שוקולד מריר שישייה         | 78.2  | 66.5  | -11.7 | low | mod | 12.0 | reconstruction_compens | —                              |
| קורני חטיפי דגנים בוטנים מתוק מלוח           | 76.7  | 64.6  | -12.1 | low | mod | 11.2 | mechanical_degradation | rolled_oats at position 6 (tex |
| חטיפי דגנים פיטנס קלאסי שישייה               | 75.8  | 64.6  | -11.2 | mod | mod | 11.2 | reconstruction_compens | rolled_oats at position 5 (tex |
| נייצר וואלי פרוטאין בוטנים ושבבי שוקולד רביע | 73.9  | 62.3  | -11.6 | mod | mod | 11.6 | mechanical_degradation | —                              |
| חטיפי דגנים פיטנס שוקולד בננה שישייה         | 74.6  | 60.5  | -14.1 | mod | mod | 12.0 | reconstruction_compens | rolled_oats at position 11 (te |
| קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה | 70.6  | 60.4  | -10.2 | mod | mod | 8.9  | minimal_transformation | —                              |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים | 74.2  | 60.1  | -14.1 | mod | mod | 12.0 | mechanical_degradation | —                              |
| קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישי | 70.1  | 59.8  | -10.3 | mod | mod | 9.0  | minimal_transformation | —                              |
| קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקו | 71.4  | 59.6  | -11.8 | mod | mod | 10.5 | minimal_transformation | —                              |
| חטיפי דגנים פיטנס שקדים ודבש שישייה          | 71.8  | 58.1  | -13.7 | mod | mod | 12.0 | reconstruction_compens | —                              |
| חטיף דגנים עם אגוזים                         | 70.3  | 58.0  | -12.3 | mod | mod | 11.0 | mechanical_degradation | flaked_grain at position 9 (te |
| קראנצ'י חטיף שיבולת שועל מיקס חמישייה        | 70.2  | 56.9  | -13.3 | mod | hig | 12.0 | traditional_transforma | rolled_oats at position 12 (te |
| חטיף דגנים שוגי שישייה 156 גרם               | 65.9  | 56.1  | -9.8  | mod | hig | 9.0  | mechanical_degradation | —                              |
| חטיף דגנים שוגי שוקו שישייה 156 גרם          | 65.9  | 56.1  | -9.8  | mod | hig | 9.0  | mechanical_degradation | —                              |
| חטיף דגנים מלאים מצופה שוקולד חלב            | 63.5  | 55.4  | -8.1  | mod | hig | 7.0  | mechanical_degradation | —                              |
| חטיפי דגנים פיטנס קרם ועוגיות שישייה         | 69.5  | 55.2  | -14.3 | mod | hig | 12.0 | reconstruction_compens | rolled_oats at position 4 (tex |
| חטיף דגנים עם פירות יער                      | 68.4  | 54.0  | -14.4 | mod | hig | 12.0 | reconstruction_compens | rolled_oats at position 3 (tex |
| חטיפי פיטנס שיבולת שועל דבש 5*38 גרם         | 67.8  | 54.0  | -13.8 | mod | hig | 11.8 | mechanical_degradation | rolled_oats at position 9 (tex |
| נייצר וואלי פרוטאין בוטנים בציפוי קרמל מלוח  | 59.8  | 54.0  | -5.8  | mod | hig | 3.5  | mechanical_degradation | —                              |
| מרבה סלים דליס שוקולד לבן חדש                | 66.4  | 53.5  | -12.9 | mod | hig | 11.8 | mechanical_degradation | —                              |
| מרבה סלים טופינג אגוזי לוז                   | 62.5  | 53.2  | -9.3  | mod | hig | 7.0  | mechanical_degradation | —                              |
| קורני חטיפי דגנים+שוקולד חלב                 | 58.9  | 52.6  | -6.3  | mod | hig | 5.0  | mechanical_degradation | —                              |
| מרבה סלים דליס לילדים עם שוקולד חלב חדש      | 59.6  | 52.4  | -7.2  | mod | hig | 5.0  | mechanical_degradation | —                              |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה     | 54.4  | 52.0  | -2.4  | hig | hig | 0.0  | mechanical_degradation | —                              |
| קורני חטיפי דגנים קוקוס שוקולד               | 63.9  | 51.2  | -12.7 | mod | hig | 11.0 | mechanical_degradation | rolled_oats at position 4 (tex |
| קורני חטיפי דגנים שוקולד מריר 58% קקאו       | 63.7  | 51.0  | -12.7 | mod | hig | 11.0 | mechanical_degradation | flaked_grain at position 8 (te |
| מרבה סלים דליס מהדורה מיוחדת שוקולד חלב      | 60.5  | 49.4  | -11.1 | mod | hig | 9.0  | mechanical_degradation | —                              |
| פיטנס בר גרנולה שוקולד מריר                  | 63.2  | 48.9  | -14.3 | mod | hig | 12.0 | mechanical_degradation | rolled_oats at position 9 (tex |
| קוקומן חטיף פצפוצי דגנים בטעם שוקולד 6 יח'   | 57.7  | 46.5  | -11.2 | hig | hig | 10.9 | mechanical_degradation | —                              |
| מרבה סלים דליס קריספי תות 125 גר             | 59.5  | 44.8  | -14.7 | mod | hig | 12.0 | mechanical_degradation | —                              |
| חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים ש | 57.1  | 43.9  | -13.2 | hig | hig | 11.0 | mechanical_degradation | —                              |
| חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר שי | 57.1  | 43.9  | -13.2 | hig | hig | 11.0 | mechanical_degradation | —                              |
| חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה | 55.6  | 43.4  | -12.2 | hig | hig | 11.0 | mechanical_degradation | —                              |
| חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל  | 57.1  | 43.3  | -13.8 | hig | hig | 11.6 | mechanical_degradation | —                              |
| קורני חטיפי דגנים שוקולד בננה                | 44.9  | 42.6  | -2.3  | hig | hig | 0.0  | mechanical_degradation | —                              |
| שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילו | 52.7  | 38.6  | -14.1 | hig | sev | 11.8 | mechanical_degradation | —                              |
| חטיף דגנים שוקו וניל נסטלה שישייה            | 51.4  | 37.3  | -14.1 | hig | sev | 11.6 | reconstruction_compens | —                              |
| מרבה סלים דליס קריספי אוכמניות 125 גר        | 36.9  | 33.3  | -3.6  | sev | sev | 0.0  | mechanical_degradation | —                              |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב  | 44.8  | 30.8  | -14.0 | hig | sev | 12.0 | reconstruction_compens | rolled_oats at position 6 (tex |

## Cereals — Full Comparison

| Product                                      | v1    | v2    | Δ    | L1  | L2  | Drag | Transform              | Supp Signal                    |
|----------------------------------------------|-------|-------|------|-----|-----|------|------------------------|--------------------------------|
| פתיתי כוסמין מלא 500 גרם                     | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| וויטביקס דגני בוקר חיטה מלאה 430 גרם         | 99.4  | 97.3  | -2.1 | min | min | 2.5  | minimal_transformation | —                              |
| דגני בוקר ספשל K קלוגס 375 גרם               | 99.4  | 96.9  | -2.5 | min | min | 2.9  | minimal_transformation | —                              |
| שיבולת שועל מהירה קוואקר 500 גרם             | 100.0 | 96.7  | -3.3 | min | min | 0.0  | traditional_transforma | rolled_oats at position 1 (tex |
| שיבולת שועל גרוסה ספרוגרן 500 גרם            | 100.0 | 96.7  | -3.3 | min | min | 0.0  | traditional_transforma | rolled_oats at position 1 (tex |
| שיבולת שועל גלגולה קוואקר 500 גרם            | 100.0 | 96.7  | -3.3 | min | min | 0.0  | traditional_transforma | rolled_oats at position 1 (tex |
| שיבולת שועל מלאה תלמה 500 גרם                | 100.0 | 96.7  | -3.3 | min | min | 0.0  | traditional_transforma | rolled_oats at position 1 (tex |
| סובין שיבולת שועל 400 גרם                    | 100.0 | 96.7  | -3.3 | min | min | 0.0  | traditional_transforma | rolled_oats at position 1 (tex |
| בסיס שיבולת שועל לילה עם זרעי צ'יה ופשתן 400 | 100.0 | 96.1  | -3.9 | min | min | 1.4  | traditional_transforma | rolled_oats at position 1 (tex |
| מוסלי בירכר בסיס 500 גרם                     | 100.0 | 94.7  | -5.3 | min | min | 2.9  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם | 100.0 | 94.4  | -5.6 | min | min | 3.3  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר ספשל K פירות אדומים קלוגס 375 גרם  | 98.2  | 94.2  | -4.0 | min | min | 4.9  | minimal_transformation | —                              |
| דגני בוקר פתיתי דגנים מלאים מעורבים 375 גרם  | 100.0 | 94.2  | -5.8 | min | min | 5.3  | traditional_transforma | rolled_oats at position 3 (tex |
| דגני בוקר שוקו-פיק נסטלה 375 גרם             | 98.2  | 94.2  | -4.0 | min | min | 4.9  | minimal_transformation | —                              |
| מוסלי שוויצרי קלאסי 500 גרם                  | 100.0 | 92.8  | -7.2 | min | min | 4.9  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה דייטס ללא תוספת סוכר 400 גרם          | 100.0 | 92.8  | -7.2 | min | min | 4.9  | traditional_transforma | rolled_oats at position 1 (tex |
| מוסלי פירות ואגוזים 500 גרם                  | 100.0 | 92.8  | -7.2 | min | min | 4.9  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה זרעים עם שמן זית ודבש 350 גרם         | 100.0 | 92.4  | -7.6 | min | min | 5.3  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה עם אגוזים ודבש טבעי 400 גרם           | 98.2  | 91.5  | -6.7 | min | min | 5.3  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר ספשל K חלבון קלוגס 320 גרם         | 93.0  | 89.0  | -4.0 | min | low | 4.9  | minimal_transformation | —                              |
| דייסת שיבולת שועל מיידית בטעם וניל קוואקר 34 | 91.6  | 85.8  | -5.8 | min | low | 3.3  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר פיטנס נסטלה 375 גרם                | 91.6  | 84.3  | -7.3 | min | low | 7.7  | mechanical_degradation | —                              |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם         | 89.7  | 84.0  | -5.7 | low | low | 5.7  | mechanical_degradation | —                              |
| גרנולה עם חמוציות 400 גרם                    | 91.6  | 83.8  | -7.8 | min | low | 5.3  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר פתיתי סובין קלוגס 375 גרם          | 88.1  | 81.7  | -6.4 | low | low | 6.5  | mechanical_degradation | —                              |
| דגני בוקר פיטנס חלבון נסטלה 320 גרם          | 87.0  | 81.3  | -5.7 | low | low | 5.7  | minimal_transformation | —                              |
| דגני בוקר אול-בראן פתיתי סובין קלוגס 375 גרם | 88.3  | 79.9  | -8.4 | low | low | 8.5  | mechanical_degradation | —                              |
| גרנולה עם שבבי שוקולד 400 גרם                | 87.8  | 79.3  | -8.5 | low | low | 5.7  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם       | 87.4  | 77.7  | -9.7 | low | low | 6.5  | traditional_transforma | rolled_oats at position 1 (tex |
| דייסת שיבולת שועל מיידית בטעם דבש קוואקר 340 | 83.7  | 76.8  | -6.9 | low | low | 3.7  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם        | 83.7  | 74.9  | -8.8 | low | mod | 5.7  | traditional_transforma | rolled_oats at position 1 (tex |
| גרנולה קלאסטרס קלוגס 400 גרם                 | 78.8  | 69.2  | -9.6 | low | mod | 6.1  | traditional_transforma | rolled_oats at position 1 (tex |
| דגני בוקר פצפוצי חיטה מלאה 375 גרם           | 70.7  | 68.5  | -2.2 | mod | mod | 2.2  | mechanical_degradation | —                              |
| דגני בוקר חלבון מקסימום 27 גרם חלבון 300 גרם | 73.9  | 67.0  | -6.9 | mod | mod | 6.9  | mechanical_degradation | —                              |
| דגני בוקר פרוט לופס קלוגס 375 גרם            | 70.5  | 64.3  | -6.2 | mod | mod | 6.1  | mechanical_degradation | —                              |
| קורנפלקס אורגני ביו 300 גרם                  | 64.2  | 64.2  | +0.0 | mod | mod | 0.0  | mechanical_degradation | —                              |
| קורנפלקס תלמה 500 גרם                        | 67.6  | 64.0  | -3.6 | mod | mod | 3.7  | mechanical_degradation | —                              |
| קורנפלקס קלוגס 375 גרם                       | 67.8  | 62.8  | -5.0 | mod | mod | 5.7  | reconstruction_compens | —                              |
| קורנפלקס נסטלה 375 גרם                       | 67.8  | 62.8  | -5.0 | mod | mod | 5.7  | reconstruction_compens | —                              |
| קורנפלקס דגנים מלאים קלוגס 375 גרם           | 68.2  | 62.7  | -5.5 | mod | mod | 5.7  | mechanical_degradation | —                              |
| דגני בוקר טבעות שוקולד תלמה 375 גרם          | 60.4  | 54.5  | -5.9 | mod | hig | 5.7  | mechanical_degradation | —                              |
| דגני בוקר לייון נסטלה 400 גרם                | 54.4  | 45.6  | -8.8 | hig | hig | 6.5  | mechanical_degradation | —                              |
| דגני בוקר סמאקס דבש קלוגס 330 גרם            | 52.3  | 44.2  | -8.1 | hig | hig | 6.1  | mechanical_degradation | —                              |
| דגני בוקר קוקו פופס קלוגס 375 גרם            | 51.7  | 43.2  | -8.5 | hig | hig | 6.5  | mechanical_degradation | —                              |
| דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם | 51.3  | 42.4  | -8.9 | hig | hig | 6.9  | mechanical_degradation | —                              |

## Yogurt — Full Comparison

| Product                      | v1    | v2    | Δ    | L1  | L2  | Drag | Transform              | Supp Signal                    |
|------------------------------|-------|-------|------|-----|-----|------|------------------------|--------------------------------|
| יוגורט טבעי 1.5% שומן        | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט טבעי 3% שומן          | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט עיזים 9% שומן         | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט יווני 0% שומן         | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט יווני 2% שומן         | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט יווני 5% שומן         | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| לבן שתייה 3% שומן            | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| קפיר 2% שומן                 | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| יוגורט יווני חלבון 18 טהור   | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט סויה טבעי             | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| לבן שתייה 3% טנובה           | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| קפיר שתייה 3%                | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| לבן 1.5% חלב טנובה           | 100.0 | 100.0 | +0.0 | min | min | 0.0  | traditional_transforma | —                              |
| יוגורט טבעי 5% שומן יוטבתה   | 100.0 | 99.0  | -1.0 | min | min | 1.0  | traditional_transforma | —                              |
| יוגורט יווני 10% שומן פאג'   | 100.0 | 99.0  | -1.0 | min | min | 1.0  | traditional_transforma | —                              |
| סקיר טבעי 0.2% שומן          | 100.0 | 99.0  | -1.0 | min | min | 1.0  | traditional_transforma | —                              |
| יוגורט תות 1.5% שומן         | 100.0 | 98.6  | -1.4 | min | min | 1.4  | traditional_transforma | —                              |
| יוגורט ילדים תות טבעי        | 100.0 | 98.6  | -1.4 | min | min | 1.4  | traditional_transforma | —                              |
| יוגורט נטול לקטוז 1.5%       | 100.0 | 98.6  | -1.4 | min | min | 1.4  | traditional_transforma | —                              |
| יוגורט יווני נטול לקטוז      | 100.0 | 98.6  | -1.4 | min | min | 1.4  | traditional_transforma | —                              |
| יוגורט שקדים ואניל           | 98.2  | 98.1  | -0.1 | min | min | 1.0  | traditional_transforma | —                              |
| יוגורט חלבון 20 פרי יער      | 98.2  | 97.2  | -1.0 | min | min | 1.0  | traditional_transforma | —                              |
| סקיר תות                     | 100.0 | 97.1  | -2.9 | min | min | 2.9  | traditional_transforma | —                              |
| יוגורט אוכמניות עם מייצב     | 98.2  | 96.2  | -2.0 | min | min | 2.9  | traditional_transforma | —                              |
| יוגורט אפרסק עתיר סוכר       | 98.2  | 96.2  | -2.0 | min | min | 2.9  | traditional_transforma | —                              |
| יוגורט שתייה תות             | 98.2  | 96.2  | -2.0 | min | min | 2.9  | traditional_transforma | —                              |
| יוגורט ילדים תות ואניל       | 98.2  | 94.2  | -4.0 | min | min | 4.9  | traditional_transforma | —                              |
| קרם יוגורט קרמל              | 98.2  | 94.2  | -4.0 | min | min | 4.9  | traditional_transforma | —                              |
| יוגורט שיבולת שועל           | 93.0  | 93.9  | +0.9 | min | min | 1.8  | mechanical_degradation | rolled_oats at position 1 (tex |
| אקטימל משקה חלב פרוביוטי     | 94.2  | 93.7  | -0.5 | min | min | 1.4  | traditional_transforma | —                              |
| שתייה חלב לילדים פרוביוטיקה  | 94.2  | 93.7  | -0.5 | min | min | 1.4  | traditional_transforma | —                              |
| יוגורט יווני 0% סטביה        | 95.2  | 93.1  | -2.1 | min | min | 1.8  | traditional_transforma | —                              |
| יוגורט נטול לקטוז תות        | 95.7  | 92.1  | -3.6 | min | min | 3.3  | traditional_transforma | —                              |
| יוגורט קוקוס                 | 93.0  | 91.6  | -1.4 | min | min | 1.4  | mechanical_degradation | —                              |
| יוגורט אקטיביה פרוביוטי      | 94.0  | 89.9  | -4.1 | min | low | 4.1  | mechanical_degradation | —                              |
| יוגורט פירות יוטבתה 1.5%     | 94.0  | 89.9  | -4.1 | min | low | 4.1  | mechanical_degradation | —                              |
| מוס שוקולד יוגורט            | 94.4  | 88.1  | -6.3 | min | low | 5.3  | traditional_transforma | —                              |
| יוגורט מולר קורנר דבש אגוזים | 90.3  | 86.2  | -4.1 | min | low | 3.3  | traditional_transforma | —                              |
| יוגורט ילדים שוקולד          | 90.4  | 86.1  | -4.3 | min | low | 3.3  | traditional_transforma | —                              |
| יוגורט חלבון ממרח שוקולד     | 88.6  | 85.9  | -2.7 | low | low | 1.8  | traditional_transforma | —                              |
| סקיר ואניל                   | 89.6  | 85.9  | -3.7 | low | low | 3.7  | traditional_transforma | —                              |
| יוגורט 0% ללא סוכר תות       | 89.6  | 85.0  | -4.6 | low | low | 3.7  | traditional_transforma | —                              |
| יוגורט דיאט ואניל 0%         | 89.6  | 84.1  | -5.5 | low | low | 3.7  | traditional_transforma | —                              |
| יוגורט חלבון ואניל           | 88.0  | 83.9  | -4.1 | low | low | 3.3  | traditional_transforma | —                              |
| יוגורט עם ריבת תות           | 86.4  | 80.2  | -6.2 | low | low | 5.3  | traditional_transforma | —                              |

## Milk — Full Comparison

| Product                                      | v1    | v2    | Δ    | L1  | L2  | Drag | Transform              | Supp Signal                    |
|----------------------------------------------|-------|-------|------|-----|-----|------|------------------------|--------------------------------|
| חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן     | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| חלב טבעי 4% 1 ליטר                           | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| חלב עיזים בקרטון 1 ליטר                      | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר   | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| משקה סויה ללא סוכרים 1 ליטר                  | 100.0 | 100.0 | +0.0 | min | min | 0.0  | minimal_transformation | —                              |
| משקה אורז אורגני                             | 100.0 | 99.0  | -1.0 | min | min | 1.0  | minimal_transformation | —                              |
| משקה סויה ללא תוספת סוכר                     | 99.7  | 98.9  | -0.8 | min | min | 1.0  | minimal_transformation | —                              |
| חלב בבקבוק 1% מועשר- מהדרין                  | 99.4  | 98.8  | -0.6 | min | min | 1.0  | minimal_transformation | —                              |
| משקה בריסטה שיבולת שועל                      | 100.0 | 94.4  | -5.6 | min | min | 4.9  | traditional_transforma | rolled_oats at position 2 (tex |
| משקה שיבולת שועל ללא סוכר                    | 100.0 | 94.4  | -5.6 | min | min | 4.9  | traditional_transforma | rolled_oats at position 2 (tex |
| משקה בריסטה שיבולת שועל להקצפה               | 100.0 | 94.4  | -5.6 | min | min | 4.9  | traditional_transforma | rolled_oats at position 2 (tex |
| אלפרו שיבולת שועל ללא סוכר                   | 99.4  | 92.6  | -6.8 | min | min | 4.9  | traditional_transforma | rolled_oats at position 1 (tex |
| משקה שיבולת שועל                             | 99.7  | 90.7  | -9.0 | min | min | 6.9  | traditional_transforma | rolled_oats at position 1 (tex |
| משקה אורז קוקוס אורגני                       | 93.0  | 89.4  | -3.6 | min | low | 4.5  | minimal_transformation | —                              |
| אלפרו שקדים ללא סוכר                         | 93.4  | 88.2  | -5.2 | min | low | 5.3  | minimal_transformation | —                              |
| משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ" | 94.4  | 87.8  | -6.6 | min | low | 5.3  | minimal_transformation | —                              |
| אלפרו שוקו משקה סויה                         | 90.3  | 86.4  | -3.9 | min | low | 5.3  | minimal_transformation | —                              |
| משקה שקדים                                   | 92.3  | 85.1  | -7.2 | min | low | 7.3  | minimal_transformation | —                              |
| מולר פרוטאין משקה חלבון בטעם בננה 25גרם חלבו | 89.8  | 84.5  | -5.3 | low | low | 5.3  | minimal_transformation | —                              |
| משקה סויה בריסטה אלפרו 500 מ"ל               | 83.7  | 83.7  | +0.0 | low | low | 0.0  | minimal_transformation | —                              |

## Provenance Trace Examples (top 6 most interesting)

Sample provenance blocks from v2 for selected products. These show the human-readable signal decomposition.

### מרבה סלים דליס קריספי תות 125 גר (snack_bars)

v1 score: **60** → v2 score: **45** (Δ -14.7)
Transform type: `mechanical_degradation`  |  Assembly drag: 12.0

**Degradation signals:**
- wheat_flour at position 1 (deg=70)
- dextrose at position 6 (deg=88)
- starch_generic at position 23 (deg=78)

**Engineering signals:**
- protein engineering: whole_milk_powder
- protein engineering: milk_powder
- additive: humectant
- additive: emulsifier
- sweetener system: heavy_sweetener_layering

**Compensation signals:**
- vitamin/mineral fortification ×1 (basic_restoration)

### חטיף דגנים עם פירות יער (snack_bars)

v1 score: **68** → v2 score: **54** (Δ -14.4)
Transform type: `reconstruction_compensation`  |  Assembly drag: 12.0

**Degradation signals:**
- wheat_flour at position 7 (deg=70)
- maltodextrin at position 11 (deg=92)
- rice_flour at position 16 (deg=65)
- rolled_oats at position 3 (deg=6)
- structural void: pos2_primary_sweetener:glucose_syrup

**Engineering signals:**
- protein engineering: skim_milk_powder
- protein engineering: milk_powder
- additive: bulking_agent
- additive: humectant
- additive: emulsifier
- sweetener system: heavy_sweetener_layering

**Compensation signals:**
- vitamin/mineral fortification ×7 (partial_compensation)

### יוגורט טבעי 1.5% שומן (yogurt)

v1 score: **100** → v2 score: **100** (Δ +0.0)
Transform type: `traditional_transformation`  |  Assembly drag: 0.0


**Protective signals:**
- fermentation: live_cultures
- fermentation: lb_acidophilus
- fermentation: bifidobacterium
- fermentation: lactobacillus
- fermentation: cultures_generic

### יוגורט טבעי 3% שומן (yogurt)

v1 score: **100** → v2 score: **100** (Δ +0.0)
Transform type: `traditional_transformation`  |  Assembly drag: 0.0


**Protective signals:**
- fermentation: live_cultures
- fermentation: cultures_generic

### שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם חלב (snack_bars)

v1 score: **53** → v2 score: **39** (Δ -14.1)
Transform type: `mechanical_degradation`  |  Assembly drag: 11.8

**Degradation signals:**
- wheat_flour at position 1 (deg=70)
- corn_flakes at position 3 (deg=48)
- dextrose at position 7 (deg=88)
- oat_flakes at position 8 (deg=20)

**Engineering signals:**
- protein engineering: whole_milk_powder
- protein engineering: milk_powder
- additive: humectant
- additive: emulsifier
- sweetener system: heavy_sweetener_layering

**Protective signals:**
- traditional roasting: roasted

### קורני חטיפי דגנים שוקולד בננה (snack_bars)

v1 score: **45** → v2 score: **43** (Δ -2.3)
Transform type: `mechanical_degradation`  |  Assembly drag: 0.0

**Degradation signals:**
- wheat_flour at position 1 (deg=70)

**Engineering signals:**
- protein engineering: milk_powder
- additive: emulsifier
- sweetener system: heavy_sweetener_layering

**Protective signals:**
- traditional roasting: roasted

---

*Generated by matrix_integrity_v2 vs matrix_integrity_v1_archive — BSIP2 Matrix Integrity Calibration Sprint*