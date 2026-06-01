# Matrix Integrity Engine v1 — Validation Report 001

**Engine version:** matrix_integrity_v1
**Run date:** 2026-05-20 05:03 UTC
**Products evaluated:** 163

---

## Category Summary

| Category   | N  | Min Score | Avg Score | Max Score | Avg Depth | Avg Eng |
|------------|----|-----------|-----------|-----------|-----------|---------|
| snack_bars | 53 | 36.9      | 70.6      | 100.0     | 1.81      | 14.0    |
| cereals    | 45 | 51.3      | 85.7      | 100.0     | 0.87      | 2.8     |
| yogurt     | 45 | 86.4      | 96.6      | 100.0     | 0.13      | 1.6     |
| milk       | 20 | 83.7      | 96.8      | 100.0     | 0.10      | 2.6     |

## Score Distribution (All Categories)

| Score Range       | Count |
|-------------------|-------|
| 90-100 (minimal)  | 89    |
| 75-89  (low)      | 22    |
| 58-74  (moderate) | 37    |
| 40-57  (high)     | 14    |
| 22-39  (severe)   | 1     |
| 0-21   (extreme)  | 0     |

## Strongest Matrix Integrity (top 12)

| Product                                  | Category   | Score | Depth | Level   | Primary Signal |
|------------------------------------------|------------|-------|-------|---------|----------------|
| חטיף תמרים במילוי חמאת שקדים             | snack_bars | 100.0 | 0     | minimal | none           |
| חטיף תמרים במילוי חמאת בוטנים            | snack_bars | 100.0 | 0     | minimal | none           |
| חטיף תמרים בציפוי שוקולד 100% קקאו       | snack_bars | 100.0 | 0     | minimal | none           |
| חטיף אגוזים וחמוציות רפאלס 5*30 גרם      | snack_bars | 100.0 | 0     | minimal | none           |
| חטיף פאי פקאן רפאלס 5*30 גרם             | snack_bars | 100.0 | 0     | minimal | none           |
| חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם | snack_bars | 100.0 | 0     | minimal | none           |
| חטיף דגנים מצופה שוקולד מריר סלים דליס   | snack_bars | 100.0 | 0     | minimal | none           |
| פתיתי כוסמין מלא 500 גרם                 | cereals    | 100.0 | 0     | minimal | none           |
| מוסלי שוויצרי קלאסי 500 גרם              | cereals    | 100.0 | 0     | minimal | none           |
| מוסלי בירכר בסיס 500 גרם                 | cereals    | 100.0 | 0     | minimal | none           |
| שיבולת שועל מהירה קוואקר 500 גרם         | cereals    | 100.0 | 0     | minimal | none           |
| שיבולת שועל גרוסה ספרוגרן 500 גרם        | cereals    | 100.0 | 0     | minimal | none           |

## Weakest Matrix Integrity (bottom 12)

| Product                                              | Category   | Score | Depth | Level  | Primary Signal                       |
|------------------------------------------------------|------------|-------|-------|--------|--------------------------------------|
| מרבה סלים דליס קריספי אוכמניות 125 גר                | snack_bars | 36.9  | 4     | severe | dextrose (pos 1, deg=88)             |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח'    | snack_bars | 44.8  | 3     | high   | pos2_primary_sweetener:glucose_syrup |
| קורני חטיפי דגנים שוקולד בננה                        | snack_bars | 44.9  | 3     | high   | wheat_flour (pos 1, deg=70)          |
| דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם         | cereals    | 51.3  | 3     | high   | pos2_primary_sweetener:added_sugar   |
| חטיף דגנים שוקו וניל נסטלה שישייה                    | snack_bars | 51.4  | 3     | high   | pos2_primary_sweetener:glucose_syrup |
| דגני בוקר קוקו פופס קלוגס 375 גרם                    | cereals    | 51.7  | 3     | high   | pos2_primary_sweetener:added_sugar   |
| דגני בוקר סמאקס דבש קלוגס 330 גרם                    | cereals    | 52.3  | 3     | high   | pos2_primary_sweetener:added_sugar   |
| שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם חל | snack_bars | 52.7  | 3     | high   | wheat_flour (pos 1, deg=70)          |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה             | snack_bars | 54.4  | 3     | high   | maltodextrin (pos 2, deg=92)         |
| דגני בוקר לייון נסטלה 400 גרם                        | cereals    | 54.4  | 3     | high   | corn_starch (pos 1, deg=82)          |
| חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה         | snack_bars | 55.6  | 3     | high   | pos1_primary_sweetener:glucose_syrup |
| חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם נוג | snack_bars | 57.1  | 3     | high   | corn_flour (pos 1, deg=65)           |

## Snack Bars — All Products

| Product                                          | Score | D | Level    | Eng  | HP | Ferm | Compensation                        |
|--------------------------------------------------|-------|---|----------|------|----|------|-------------------------------------|
| חטיף תמרים במילוי חמאת שקדים                     | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיף תמרים במילוי חמאת בוטנים                    | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיף תמרים בציפוי שוקולד 100% קקאו               | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיף אגוזים וחמוציות רפאלס 5*30 גרם              | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיף פאי פקאן רפאלס 5*30 גרם                     | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם         | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| חטיף דגנים מצופה שוקולד מריר סלים דליס           | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                   |
| פרי מארז 5 חטיפים תמרים ואגוזי לוז כשלפ          | 98.2  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                   |
| פרי מארז חטיפי תמרים ושברי קקאו 5+1              | 98.2  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                   |
| חטיפי דגנים פיטנס שוקולד מריר שישייה             | 78.2  | 1 | low      | 19.7 | 85 | 0.00 | vitamin_mineral_fortification_x7    |
| מרבה סלים דליס שוקולד מריר חדש                   | 77.4  | 1 | low      | 2.8  | 32 | 0.00 | —                                   |
| קורני חטיפי דגנים בוטנים מתוק מלוח               | 76.7  | 1 | low      | 12.9 | 45 | 0.00 | —                                   |
| קראנצ'י חטיף שיבולת שועל עם דבש חמישייה          | 76.5  | 1 | low      | 8.6  | 45 | 0.00 | —                                   |
| חטיפי דגנים פיטנס קלאסי שישייה                   | 75.8  | 2 | moderate | 16.7 | 85 | 0.00 | vitamin_mineral_fortification_x7    |
| חטיפי דגנים פיטנס שוקולד בננה שישייה             | 74.6  | 2 | moderate | 19.7 | 85 | 0.00 | vitamin_mineral_fortification_x7    |
| סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יו | 74.3  | 2 | moderate | 6.7  | 32 | 0.00 | vitamin_mineral_fortification_x1    |
| מרבה סלים דליס שוקולד חלב ללא גלוטן חדש          | 74.3  | 2 | moderate | 5.7  | 32 | 0.00 | —                                   |
| מרבה סלים דליס שוקולד לבן בטעם יוגורט            | 74.3  | 2 | moderate | 6.7  | 32 | 0.00 | vitamin_mineral_fortification_x1    |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמי | 74.2  | 2 | moderate | 25.0 | 85 | 0.00 | prebiotic_fiber_addition, vitamin_m |
| נייצר וואלי פרוטאין בוטנים ושבבי שוקולד רביעייה  | 73.9  | 2 | moderate | 36.3 | 85 | 0.00 | additive_bulking_agent              |
| חטיפי דגנים פיטנס שקדים ודבש שישייה              | 71.8  | 2 | moderate | 16.7 | 85 | 0.00 | vitamin_mineral_fortification_x7    |
| קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקולד ח | 71.4  | 2 | moderate | 6.0  | 85 | 0.00 | —                                   |
| קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה     | 70.6  | 2 | moderate | 8.6  | 85 | 0.00 | —                                   |
| חטיף דגנים עם אגוזים                             | 70.3  | 2 | moderate | 10.0 | 85 | 0.00 | —                                   |
| קראנצ'י חטיף שיבולת שועל מיקס חמישייה            | 70.2  | 2 | moderate | 10.0 | 85 | 0.00 | —                                   |
| קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישייה   | 70.1  | 2 | moderate | 10.0 | 85 | 0.00 | —                                   |
| חטיפי דגנים פיטנס קרם ועוגיות שישייה             | 69.5  | 2 | moderate | 28.2 | 85 | 0.00 | vitamin_mineral_fortification_x7, a |
| חטיף דגנים עם פירות יער                          | 68.4  | 2 | moderate | 28.2 | 85 | 0.00 | vitamin_mineral_fortification_x7, a |
| חטיפי פיטנס שיבולת שועל דבש 5*38 גרם             | 67.8  | 2 | moderate | 20.0 | 85 | 0.00 | prebiotic_fiber_addition, additive_ |
| מרבה סלים דליס שוקולד לבן חדש                    | 66.4  | 2 | moderate | 15.5 | 85 | 0.00 | vitamin_mineral_fortification_x1, a |
| חטיף דגנים שוגי שישייה 156 גרם                   | 65.9  | 2 | moderate | 15.8 | 32 | 0.00 | prebiotic_fiber_addition, vitamin_m |
| חטיף דגנים שוגי שוקו שישייה 156 גרם              | 65.9  | 2 | moderate | 15.8 | 32 | 0.00 | prebiotic_fiber_addition, vitamin_m |
| קורני חטיפי דגנים קוקוס שוקולד                   | 63.9  | 2 | moderate | 16.3 | 85 | 0.00 | —                                   |
| קורני חטיפי דגנים שוקולד מריר 58% קקאו           | 63.7  | 2 | moderate | 15.9 | 85 | 0.00 | —                                   |
| חטיף דגנים מלאים מצופה שוקולד חלב                | 63.5  | 2 | moderate | 22.4 | 85 | 0.00 | vitamin_mineral_fortification_x1, a |
| פיטנס בר גרנולה שוקולד מריר                      | 63.2  | 2 | moderate | 20.0 | 85 | 0.00 | prebiotic_fiber_addition, additive_ |
| מרבה סלים טופינג אגוזי לוז                       | 62.5  | 2 | moderate | 9.0  | 85 | 0.00 | —                                   |
| מרבה סלים דליס מהדורה מיוחדת שוקולד חלב          | 60.5  | 2 | moderate | 9.9  | 85 | 0.00 | vitamin_mineral_fortification_x1    |
| נייצר וואלי פרוטאין בוטנים בציפוי קרמל מלוח רביע | 59.8  | 2 | moderate | 36.3 | 85 | 0.00 | additive_bulking_agent              |
| מרבה סלים דליס לילדים עם שוקולד חלב חדש          | 59.6  | 2 | moderate | 9.0  | 85 | 0.00 | —                                   |
| מרבה סלים דליס קריספי תות 125 גר                 | 59.5  | 2 | moderate | 20.2 | 45 | 0.00 | vitamin_mineral_fortification_x1    |
| קורני חטיפי דגנים+שוקולד חלב                     | 58.9  | 2 | moderate | 12.9 | 85 | 0.00 | —                                   |
| קוקומן חטיף פצפוצי דגנים בטעם שוקולד 6 יח'       | 57.7  | 3 | high     | 15.8 | 32 | 0.00 | prebiotic_fiber_addition, vitamin_m |
| חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם | 57.1  | 3 | high     | 19.5 | 85 | 0.00 | prebiotic_fiber_addition, additive_ |
| חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישיי | 57.1  | 3 | high     | 19.5 | 85 | 0.00 | prebiotic_fiber_addition, additive_ |
| חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר שישייה | 57.1  | 3 | high     | 19.5 | 85 | 0.00 | prebiotic_fiber_addition, additive_ |
| חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה     | 55.6  | 3 | high     | 16.3 | 85 | 0.00 | —                                   |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה         | 54.4  | 3 | high     | 33.4 | 85 | 0.00 | prebiotic_fiber_addition, vitamin_m |
| שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קר | 52.7  | 3 | high     | 19.2 | 85 | 0.00 | —                                   |
| חטיף דגנים שוקו וניל נסטלה שישייה                | 51.4  | 3 | high     | 28.2 | 45 | 0.00 | vitamin_mineral_fortification_x7, a |
| קורני חטיפי דגנים שוקולד בננה                    | 44.9  | 3 | high     | 12.9 | 85 | 0.00 | —                                   |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח | 44.8  | 3 | high     | 28.2 | 85 | 0.00 | vitamin_mineral_fortification_x6, a |
| מרבה סלים דליס קריספי אוכמניות 125 גר            | 36.9  | 4 | severe   | 11.5 | 75 | 0.00 | vitamin_mineral_fortification_x1    |

## Cereals — All Products

| Product                                          | Score | D | Level    | Eng  | HP | Ferm | Compensation                     |
|--------------------------------------------------|-------|---|----------|------|----|------|----------------------------------|
| פתיתי כוסמין מלא 500 גרם                         | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| מוסלי שוויצרי קלאסי 500 גרם                      | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| מוסלי בירכר בסיס 500 גרם                         | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| שיבולת שועל מהירה קוואקר 500 גרם                 | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| שיבולת שועל גרוסה ספרוגרן 500 גרם                | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| שיבולת שועל גלגולה קוואקר 500 גרם                | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| שיבולת שועל מלאה תלמה 500 גרם                    | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| סובין שיבולת שועל 400 גרם                        | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| בסיס שיבולת שועל לילה עם זרעי צ'יה ופשתן 400 גרם | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| גרנולה דייטס ללא תוספת סוכר 400 גרם              | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם     | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| גרנולה זרעים עם שמן זית ודבש 350 גרם             | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| מוסלי פירות ואגוזים 500 גרם                      | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| דגני בוקר פתיתי דגנים מלאים מעורבים 375 גרם      | 100.0 | 0 | minimal  | 0.0  | 0  | 0.00 | —                                |
| וויטביקס דגני בוקר חיטה מלאה 430 גרם             | 99.4  | 0 | minimal  | 1.9  | 0  | 0.00 | vitamin_mineral_fortification_x2 |
| דגני בוקר ספשל K קלוגס 375 גרם                   | 99.4  | 0 | minimal  | 1.9  | 0  | 0.00 | vitamin_mineral_fortification_x2 |
| דגני בוקר ספשל K פירות אדומים קלוגס 375 גרם      | 98.2  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                |
| גרנולה עם אגוזים ודבש טבעי 400 גרם               | 98.2  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                |
| דגני בוקר שוקו-פיק נסטלה 375 גרם                 | 98.2  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                |
| דגני בוקר ספשל K חלבון קלוגס 320 גרם             | 93.0  | 0 | minimal  | 17.3 | 12 | 0.00 | —                                |
| דייסת שיבולת שועל מיידית בטעם וניל קוואקר 340 גר | 91.6  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                |
| גרנולה עם חמוציות 400 גרם                        | 91.6  | 0 | minimal  | 0.0  | 12 | 0.00 | —                                |
| דגני בוקר פיטנס נסטלה 375 גרם                    | 91.6  | 0 | minimal  | 1.9  | 0  | 0.00 | vitamin_mineral_fortification_x2 |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם             | 89.7  | 1 | low      | 0.0  | 12 | 0.00 | —                                |
| דגני בוקר אול-בראן פתיתי סובין קלוגס 375 גרם     | 88.3  | 1 | low      | 5.2  | 22 | 0.00 | vitamin_mineral_fortification_x2 |
| דגני בוקר פתיתי סובין קלוגס 375 גרם              | 88.1  | 1 | low      | 5.2  | 22 | 0.00 | vitamin_mineral_fortification_x2 |
| גרנולה עם שבבי שוקולד 400 גרם                    | 87.8  | 1 | low      | 2.8  | 32 | 0.00 | —                                |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם           | 87.4  | 1 | low      | 13.1 | 58 | 0.00 | —                                |
| דגני בוקר פיטנס חלבון נסטלה 320 גרם              | 87.0  | 1 | low      | 14.2 | 58 | 0.00 | —                                |
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם            | 83.7  | 1 | low      | 3.2  | 58 | 0.00 | —                                |
| דייסת שיבולת שועל מיידית בטעם דבש קוואקר 340 גרם | 83.7  | 1 | low      | 3.2  | 58 | 0.00 | —                                |
| גרנולה קלאסטרס קלוגס 400 גרם                     | 78.8  | 1 | low      | 6.0  | 85 | 0.00 | —                                |
| דגני בוקר חלבון מקסימום 27 גרם חלבון 300 גרם     | 73.9  | 2 | moderate | 17.0 | 85 | 0.00 | —                                |
| דגני בוקר פצפוצי חיטה מלאה 375 גרם               | 70.7  | 2 | moderate | 0.0  | 0  | 0.00 | —                                |
| דגני בוקר פרוט לופס קלוגס 375 גרם                | 70.5  | 2 | moderate | 0.0  | 12 | 0.00 | —                                |
| קורנפלקס דגנים מלאים קלוגס 375 גרם               | 68.2  | 2 | moderate | 1.0  | 0  | 0.00 | vitamin_mineral_fortification_x1 |
| קורנפלקס קלוגס 375 גרם                           | 67.8  | 2 | moderate | 3.4  | 0  | 0.00 | vitamin_mineral_fortification_x4 |
| קורנפלקס נסטלה 375 גרם                           | 67.8  | 2 | moderate | 3.4  | 0  | 0.00 | vitamin_mineral_fortification_x4 |
| קורנפלקס תלמה 500 גרם                            | 67.6  | 2 | moderate | 1.0  | 0  | 0.00 | vitamin_mineral_fortification_x1 |
| קורנפלקס אורגני ביו 300 גרם                      | 64.2  | 2 | moderate | 0.0  | 0  | 0.00 | —                                |
| דגני בוקר טבעות שוקולד תלמה 375 גרם              | 60.4  | 2 | moderate | 0.0  | 12 | 0.00 | —                                |
| דגני בוקר לייון נסטלה 400 גרם                    | 54.4  | 3 | high     | 6.0  | 85 | 0.00 | —                                |
| דגני בוקר סמאקס דבש קלוגס 330 גרם                | 52.3  | 3 | high     | 3.2  | 58 | 0.00 | —                                |
| דגני בוקר קוקו פופס קלוגס 375 גרם                | 51.7  | 3 | high     | 5.8  | 58 | 0.00 | —                                |
| דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם     | 51.3  | 3 | high     | 7.2  | 58 | 0.00 | —                                |

## Yogurt — All Products

| Product                      | Score | D | Level   | Eng  | HP | Ferm | Compensation             |
|------------------------------|-------|---|---------|------|----|------|--------------------------|
| יוגורט טבעי 1.5% שומן        | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט טבעי 3% שומן          | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט טבעי 5% שומן יוטבתה   | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט עיזים 9% שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני 0% שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני 2% שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני 5% שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני 10% שומן פאג'   | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| לבן שתייה 3% שומן            | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| קפיר 2% שומן                 | 100.0 | 0 | minimal | 0.0  | 0  | 0.17 | —                        |
| יוגורט תות 1.5% שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט ילדים תות טבעי        | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני חלבון 18 טהור   | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| סקיר טבעי 0.2% שומן          | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| סקיר תות                     | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט סויה טבעי             | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט נטול לקטוז 1.5%       | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט יווני נטול לקטוז      | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| לבן שתייה 3% טנובה           | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| קפיר שתייה 3%                | 100.0 | 0 | minimal | 0.0  | 0  | 0.17 | —                        |
| לבן 1.5% חלב טנובה           | 100.0 | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט אוכמניות עם מייצב     | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט אפרסק עתיר סוכר       | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט ילדים תות ואניל       | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט חלבון 20 פרי יער      | 98.2  | 0 | minimal | 5.9  | 0  | 0.40 | —                        |
| קרם יוגורט קרמל              | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט שקדים ואניל           | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט שתייה תות             | 98.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט נטול לקטוז תות        | 95.7  | 0 | minimal | 3.2  | 22 | 0.40 | —                        |
| יוגורט יווני 0% סטביה        | 95.2  | 0 | minimal | 5.0  | 22 | 0.40 | —                        |
| מוס שוקולד יוגורט            | 94.4  | 0 | minimal | 2.8  | 32 | 0.40 | —                        |
| אקטימל משקה חלב פרוביוטי     | 94.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| שתייה חלב לילדים פרוביוטיקה  | 94.2  | 0 | minimal | 0.0  | 12 | 0.40 | —                        |
| יוגורט אקטיביה פרוביוטי      | 94.0  | 0 | minimal | 4.5  | 0  | 0.40 | additive_modified_starch |
| יוגורט פירות יוטבתה 1.5%     | 94.0  | 0 | minimal | 4.5  | 0  | 0.40 | additive_modified_starch |
| יוגורט קוקוס                 | 93.0  | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט שיבולת שועל           | 93.0  | 0 | minimal | 0.0  | 0  | 0.40 | —                        |
| יוגורט ילדים שוקולד          | 90.4  | 0 | minimal | 2.8  | 32 | 0.40 | —                        |
| יוגורט מולר קורנר דבש אגוזים | 90.3  | 0 | minimal | 3.2  | 58 | 0.40 | —                        |
| סקיר ואניל                   | 89.6  | 1 | low     | 5.8  | 58 | 0.40 | —                        |
| יוגורט 0% ללא סוכר תות       | 89.6  | 1 | low     | 5.8  | 58 | 0.40 | —                        |
| יוגורט דיאט ואניל 0%         | 89.6  | 1 | low     | 5.8  | 58 | 0.40 | —                        |
| יוגורט חלבון ממרח שוקולד     | 88.6  | 1 | low     | 8.7  | 32 | 0.40 | —                        |
| יוגורט חלבון ואניל           | 88.0  | 1 | low     | 10.9 | 58 | 0.40 | —                        |
| יוגורט עם ריבת תות           | 86.4  | 1 | low     | 3.2  | 58 | 0.40 | —                        |

## Milk — All Products

| Product                                          | Score | D | Level   | Eng  | HP | Ferm | Compensation                        |
|--------------------------------------------------|-------|---|---------|------|----|------|-------------------------------------|
| חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן         | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| חלב טבעי 4% 1 ליטר                               | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| חלב עיזים בקרטון 1 ליטר                          | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר       | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה סויה ללא סוכרים 1 ליטר                      | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה בריסטה שיבולת שועל                          | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה שיבולת שועל ללא סוכר                        | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה בריסטה שיבולת שועל להקצפה                   | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה אורז אורגני                                 | 100.0 | 0 | minimal | 0.0  | 0  | 0.00 | —                                   |
| משקה סויה ללא תוספת סוכר                         | 99.7  | 0 | minimal | 1.0  | 0  | 0.00 | vitamin_mineral_fortification_x1    |
| משקה שיבולת שועל                                 | 99.7  | 0 | minimal | 1.0  | 0  | 0.00 | vitamin_mineral_fortification_x1    |
| אלפרו שיבולת שועל ללא סוכר                       | 99.4  | 0 | minimal | 1.9  | 0  | 0.00 | vitamin_mineral_fortification_x2    |
| חלב בבקבוק 1% מועשר- מהדרין                      | 99.4  | 0 | minimal | 1.9  | 0  | 0.00 | vitamin_mineral_fortification_x2    |
| משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ"ל    | 94.4  | 0 | minimal | 2.8  | 32 | 0.00 | —                                   |
| אלפרו שקדים ללא סוכר                             | 93.4  | 0 | minimal | 6.0  | 32 | 0.00 | vitamin_mineral_fortification_x1    |
| משקה אורז קוקוס אורגני                           | 93.0  | 0 | minimal | 17.3 | 12 | 0.00 | —                                   |
| משקה שקדים                                       | 92.3  | 0 | minimal | 3.8  | 0  | 0.00 | vitamin_mineral_fortification_x1    |
| אלפרו שוקו משקה סויה                             | 90.3  | 0 | minimal | 4.2  | 12 | 0.00 | vitamin_mineral_fortification_x2    |
| מולר פרוטאין משקה חלבון בטעם בננה 25גרם חלבון 0% | 89.8  | 1 | low     | 5.0  | 58 | 0.00 | —                                   |
| משקה סויה בריסטה אלפרו 500 מ"ל                   | 83.7  | 1 | low     | 8.1  | 12 | 0.00 | prebiotic_fiber_addition, vitamin_m |

## Edge Cases and Analytical Notes

### High Fermentation Credit (factor ≥ 0.30)

- **יוגורט טבעי 1.5% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט טבעי 3% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט טבעי 5% שומן יוטבתה** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט עיזים 9% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט יווני 0% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט יווני 2% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט יווני 5% שומן** (yogurt) — score=100, ferm_factor=0.40
- **יוגורט יווני 10% שומן פאג'** (yogurt) — score=100, ferm_factor=0.40

### Products with Engineered Compensation Signals

- **נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה** (snack_bars) — score=54, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x1, additive_bulking_agent, additive_prebiotic_fiber
- **נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישייה** (snack_bars) — score=74, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x1, additive_bulking_agent, additive_prebiotic_fiber
- **חטיף דגנים שוגי שישייה 156 גרם** (snack_bars) — score=66, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x1, additive_prebiotic_fiber
- **קוקומן חטיף פצפוצי דגנים בטעם שוקולד 6 יח'** (snack_bars) — score=58, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x1, additive_prebiotic_fiber
- **חטיף דגנים שוגי שוקו שישייה 156 גרם** (snack_bars) — score=66, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x1, additive_prebiotic_fiber
- **פיטנס בר גרנולה שוקולד מריר** (snack_bars) — score=63, signals: prebiotic_fiber_addition, additive_bulking_agent, additive_prebiotic_fiber
- **חטיפי פיטנס שיבולת שועל דבש 5*38 גרם** (snack_bars) — score=68, signals: prebiotic_fiber_addition, additive_bulking_agent, additive_prebiotic_fiber
- **משקה סויה בריסטה אלפרו 500 מ"ל** (milk) — score=84, signals: prebiotic_fiber_addition, vitamin_mineral_fortification_x3, additive_prebiotic_fiber
- **חטיפי דגנים פיטנס קרם ועוגיות שישייה** (snack_bars) — score=70, signals: vitamin_mineral_fortification_x7, additive_bulking_agent
- **חטיף דגנים שוקו וניל נסטלה שישייה** (snack_bars) — score=51, signals: vitamin_mineral_fortification_x7, additive_bulking_agent

### HP Reconstruction Pattern Detected (score ≥ 50)

- **קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה** (snack_bars) — integrity=71, hp=85, depth=2
- **קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישייה** (snack_bars) — integrity=70, hp=85, depth=2
- **קראנצ'י חטיף שיבולת שועל מיקס חמישייה** (snack_bars) — integrity=70, hp=85, depth=2
- **חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה** (snack_bars) — integrity=56, hp=85, depth=3
- **שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם חלב** (snack_bars) — integrity=53, hp=85, depth=3
- **קורני חטיפי דגנים+שוקולד חלב** (snack_bars) — integrity=59, hp=85, depth=2
- **חטיף דגנים עם אגוזים** (snack_bars) — integrity=70, hp=85, depth=2
- **קורני חטיפי דגנים שוקולד בננה** (snack_bars) — integrity=45, hp=85, depth=3
- **קורני חטיפי דגנים קוקוס שוקולד** (snack_bars) — integrity=64, hp=85, depth=2
- **קורני חטיפי דגנים שוקולד מריר 58% קקאו** (snack_bars) — integrity=64, hp=85, depth=2

### Traditional Foods Correctly Avoided Unfair Penalties

- **יוגורט טבעי 1.5% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט טבעי 3% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט טבעי 5% שומן יוטבתה** (yogurt) — score=100, fermentation properly credited
- **יוגורט עיזים 9% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט יווני 0% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט יווני 2% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט יווני 5% שומן** (yogurt) — score=100, fermentation properly credited
- **יוגורט יווני 10% שומן פאג'** (yogurt) — score=100, fermentation properly credited

## Known Limitations

1. **Hidden industrial processes**: Extrusion, expansion, and cooking are not declared in ingredient lists. Corn flakes made from extruded corn flour look the same as a product where corn flour is simply ground.

2. **No ingredient quantities** (except % when declared): We cannot distinguish a product that is 80% oat flour from one that is 5% oat flour — only position proxy.

3. **Vocabulary gaps**: The enricher's Hebrew dictionaries do not cover all ingredients. Ingredients that don't match any term are treated as neutral (no degradation signal), which may inflate integrity scores for complex products.

4. **Fortification detection is approximate**: The vitamin/mineral fortification detection relies on Hebrew term matching. Some fortification may be missed when described differently (e.g., 'enriched with X').

5. **Fermentation credit is categorical, not quantitative**: All live-culture yogurts receive the same fermentation credit regardless of whether they are simple natural yogurt or a heavily engineered dairy dessert with added cultures.

6. **Product name as proxy not used**: 'בטעם' (flavored) detection from ingredients is not directly connected to the HP reconstruction score here — it is captured via the flavor marker system.

7. **No cross-product comparison**: Score is absolute, not percentile-ranked. A score of 70 means 'moderate degradation' not '70th percentile of products'.

## Graduated Severity Behavior Examples

Demonstrating the engine's ability to distinguish structural stages:

**Oat family gradient (where present):**
- חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם — score=100, depth=0, signals: none
- שיבולת שועל מהירה קוואקר 500 גרם — score=100, depth=0, signals: none
- שיבולת שועל גרוסה ספרוגרן 500 גרם — score=100, depth=0, signals: none
- שיבולת שועל גלגולה קוואקר 500 גרם — score=100, depth=0, signals: none
- שיבולת שועל מלאה תלמה 500 גרם — score=100, depth=0, signals: none

**One example per reconstruction depth:**
- Depth 0 (minimal): **חטיף תמרים במילוי חמאת שקדים** — score=100, eng=0, hp=0
- Depth 1 (low): **מולר פרוטאין משקה חלבון בטעם בננה 25גרם חלבון 0%** — score=90, eng=5, hp=58
- Depth 2 (moderate): **קורני חטיפי דגנים+שוקולד חלב** — score=59, eng=13, hp=85
- Depth 3 (high): **דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם** — score=51, eng=7, hp=58
- Depth 4 (severe): **מרבה סלים דליס קריספי אוכמניות 125 גר** — score=37, eng=12, hp=75

---

*Generated by matrix_integrity_v1 — BSIP2 Matrix Integrity Engine*