# TASK-601 BSIP0 Capture Census

- Total captures: 2680 (manifest records).
- Canonical captures: 1364 (manifest records).
- Duplicates superseded: 1316 (manifest records).
- Distinct GTINs: 1112 (canonical records with GTIN).

## Per-retailer capture breakdown

- shufersal: 1735/2680 captures
- tiv_taam: 18/2680 captures
- unknown: 869/2680 captures
- yohananof: 58/2680 captures

## Served-product coverage

| Shelf | Served products | HAS_CANONICAL_CAPTURE | NO_CAPTURE |
|---|---:|---:|---:|
| bread_frontend_v3 | 29 | 23 | 6 |
| bread_frontend_v4 | 23 | 23 | 0 |
| brined_cheeses_frontend_v2 | 36 | 36 | 0 |
| cakes_hard_cookies_frontend_v1 | 62 | 55 | 7 |
| cereals_frontend_v2 | 20 | 20 | 0 |
| cheese_frontend_v4 | 47 | 10 | 37 |
| chocolate_bars_frontend_v1 | 23 | 23 | 0 |
| chocolate_tablets_frontend_v1 | 35 | 35 | 0 |
| cookies_coffee_frontend_v2 | 117 | 96 | 21 |
| crackers_frontend_v1 | 53 | 34 | 19 |
| granola_frontend_v2 | 22 | 22 | 0 |
| hard_cheeses_frontend_v4 | 31 | 0 | 31 |
| hummus_frontend_v5 | 57 | 57 | 0 |
| juices_frontend_v3 | 17 | 14 | 3 |
| milk_frontend_v1 | 18 | 17 | 1 |
| protein_combined_frontend_v2 | 32 | 15 | 17 |
| snacks_frontend_v5 | 21 | 21 | 0 |
| yogurt_drinkable_frontend_v1 | 17 | 17 | 0 |
| yogurt_drinkable_frontend_v1_redteam_ledger | 0 | 0 | 0 |
| yogurt_spoonable_frontend_v1 | 50 | 49 | 1 |
| yogurt_spoonable_frontend_v1_redteam_ledger | 0 | 0 | 0 |

Total served products: 710; HAS_CANONICAL_CAPTURE: 567/710; NO_CAPTURE: 143/710.

## Replay distribution marker

- Replay rows: 8070 (canonical captures × 10 fields).
- Flagged rows: 38/8070; most_common flag: [('comma_ambiguous', 37)].
- Flag histogram: {'comma_ambiguous': 37, 'out_of_bound': 1}.
