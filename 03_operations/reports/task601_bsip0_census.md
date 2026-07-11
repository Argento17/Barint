# TASK-601 BSIP0 Capture Census

- Total captures: 893 (manifest records).
- Canonical captures: 807 (manifest records).
- Duplicates superseded: 86 (manifest records).
- Distinct GTINs: 652 (canonical records with GTIN).

## Per-retailer capture breakdown

- shufersal: 242/893 captures
- unknown: 651/893 captures

## Served-product coverage

| Shelf | Served products | HAS_CANONICAL_CAPTURE | NO_CAPTURE |
|---|---:|---:|---:|
| bread_frontend_v3 | 29 | 0 | 29 |
| bread_frontend_v4 | 23 | 0 | 23 |
| brined_cheeses_frontend_v2 | 36 | 36 | 0 |
| cakes_hard_cookies_frontend_v1 | 62 | 55 | 7 |
| cereals_frontend_v2 | 20 | 20 | 0 |
| cheese_frontend_v4 | 47 | 0 | 47 |
| cheese_frontend_v5 | 47 | 0 | 47 |
| chocolate_bars_frontend_v1 | 23 | 0 | 23 |
| chocolate_tablets_frontend_v1 | 35 | 0 | 35 |
| cookies_coffee_frontend_v2 | 117 | 95 | 22 |
| crackers_frontend_v1 | 53 | 34 | 19 |
| granola_frontend_v2 | 22 | 22 | 0 |
| hard_cheeses_frontend_v4 | 31 | 0 | 31 |
| hummus_frontend_v5 | 57 | 57 | 0 |
| juices_frontend_v3 | 17 | 0 | 17 |
| milk_frontend_v1 | 18 | 0 | 18 |
| protein_combined_frontend_v2 | 32 | 15 | 17 |
| snacks_frontend_v5 | 21 | 21 | 0 |
| yogurt_drinkable_frontend_v1 | 17 | 0 | 17 |
| yogurt_spoonable_frontend_v1 | 50 | 4 | 46 |

Total served products: 757; HAS_CANONICAL_CAPTURE: 359/757; NO_CAPTURE: 398/757.

## Replay distribution marker

- Replay rows: 8070 (canonical captures × 10 fields).
- Flagged rows: 38/8070; most_common flag: [('comma_ambiguous', 37)].
- Flag histogram: {'comma_ambiguous': 37, 'out_of_bound': 1}.
