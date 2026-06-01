# BSIP2 Prototype v0 — Batch Summary

**Run date:** 2026-05-17 11:11 UTC  
**Source:** `C:\Bari\03_operations\bsip1\run_001\output`  
**Specification:** bsip2_concept_v1 + score_resolution_contract_SRC-v1  

## Volumes

| Metric | Count |
|--------|-------|
| BSIP1 products loaded | 53 |
| Products processed | 53 |
| Pipeline errors | 0 |
| Products with sufficient data | 48 |
| Products with insufficient data (tentative score only) | 5 |
| Products with unresolved flags | 19 |
| Products with category instability | 9 |
| Products with structural emptiness | 0 |
| Products where floor was binding | 2 |
| Products where a cap was applied | 47 |

## Evaluation Status Distribution

| Status          | Count |
|-----------------|-------|
| context_limited | 5     |
| standard        | 48    |

## Score Statistics (sufficient-data products only)

| Metric | Value |
|--------|-------|
| Count | 48 |
| Average score | 35.2 |
| Median score | 36.8 |
| Min score | 12.4 |
| Max score | 65 |

## Grade Distribution (sufficient-data products only)

| Grade | Count |
|-------|-------|
| C     | 6     |
| D     | 14    |
| E     | 28    |

## Category Distribution

| Category          | Count |
|-------------------|-------|
| snack_bar_granola | 36    |
| whole_food_fat    | 10    |
| cereal            | 6     |
| dairy_protein     | 1     |

## NOVA Proxy Distribution

| NOVA Level | Count |
|------------|-------|
| 2          | 7     |
| 3          | 15    |
| 4          | 31    |

## Confidence Band Distribution

| Confidence Band | Count |
|-----------------|-------|
| high            | 34    |
| insufficient    | 5     |
| medium          | 14    |

## Top 10 Highest Scores (sufficient data only)

| #  | Product                                                            | Score | Grade | Category          | NOVA |
|----|--------------------------------------------------------------------|-------|-------|-------------------|------|
| 1  | bsip1_7290011498870 | חטיף תמרים במילוי חמאת שקדים                 | 65    | C     | whole_food_fat    | 2    |
| 2  | bsip1_8423207206495 | מרבה סלים דליס שוקולד מריר חדש               | 56.7  | C     | snack_bar_granola | 3    |
| 3  | bsip1_8423207208260 | מרבה סלים דליס שוקולד חלב ללא גלוטן חדש      | 56.7  | C     | whole_food_fat    | 3    |
| 4  | bsip1_7290011498948 | חטיף תמרים בציפוי שוקולד 100% קקאו           | 55.8  | C     | snack_bar_granola | 2    |
| 5  | bsip1_8423207210287 | מרבה סלים דליס שוקולד לבן בטעם יוגורט        | 55.5  | C     | dairy_protein     | 3    |
| 6  | bsip1_7290011498894 | חטיף תמרים במילוי חמאת בוטנים                | 55.0  | C     | snack_bar_granola | 2    |
| 7  | bsip1_16000548404 | קראנצ'י חטיף שיבולת שועל עם דבש חמישייה        | 51.4  | D     | cereal            | 3    |
| 8  | bsip1_16000548503 | קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישייה | 51.2  | D     | cereal            | 3    |
| 9  | bsip1_16000423534 | קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה   | 51.1  | D     | cereal            | 3    |
| 10 | bsip1_8423207207362 | מרבה סלים דליס שוקולד לבן חדש                | 50.0  | D     | snack_bar_granola | 3    |

## Top 10 Lowest Scores (sufficient data only)

| #  | Product                                                                  | Score | Grade | Category          | NOVA |
|----|--------------------------------------------------------------------------|-------|-------|-------------------|------|
| 1  | bsip1_4011800567613 | שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם  | 12.4  | E     | snack_bar_granola | 4    |
| 2  | bsip1_4011800632519 | קורני חטיפי דגנים קוקוס שוקולד                     | 14.2  | E     | snack_bar_granola | 4    |
| 3  | bsip1_4011800628512 | קורני חטיפי דגנים+שוקולד חלב                       | 15.4  | E     | snack_bar_granola | 4    |
| 4  | bsip1_7290107646147 | חטיף דגנים שוגי שישייה 156 גרם                     | 16.1  | E     | snack_bar_granola | 4    |
| 5  | bsip1_7290107646826 | חטיף דגנים שוגי שוקו שישייה 156 גרם                | 16.3  | E     | snack_bar_granola | 4    |
| 6  | bsip1_4011800630515 | קורני חטיפי דגנים שוקולד בננה                      | 16.8  | E     | snack_bar_granola | 4    |
| 7  | bsip1_4011800633516 | קורני חטיפי דגנים שוקולד מריר 58% קקאו             | 16.8  | E     | snack_bar_granola | 4    |
| 8  | bsip1_7290107947466 | חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם נ | 17.1  | E     | snack_bar_granola | 4    |
| 9  | bsip1_7290118427858 | פיטנס בר גרנולה שוקולד מריר                        | 17.1  | E     | snack_bar_granola | 4    |
| 10 | bsip1_7290107947480 | חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישייה  | 17.2  | E     | snack_bar_granola | 4    |

## Insufficient Data Products (tentative score, no grade)

- `bsip1_16000548909` | קראנצ'י חטיף שיבולת שועל מיקס חמישייה | tentative=32.3 conf=27
- `bsip1_7290018333952` | חטיף אגוזים וחמוציות רפאלס 5*30 גרם | tentative=50 conf=5
- `bsip1_7290019545545` | חטיף פאי פקאן רפאלס 5*30 גרם | tentative=50 conf=5
- `bsip1_7290118427872` | חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם | tentative=50 conf=5
- `bsip1_8423207208703` | חטיף דגנים מצופה שוקולד מריר סלים דליס | tentative=50 conf=5