# TASK-591: published-fat EV-026 audit

## Methodology and coverage

This was a local, read-only audit. No network source was used, and no Open Food
Facts material was used or consulted. The enumeration recursively inspected every
product object in every `bari-web/src/data/comparisons/*_frontend_v*.json` file,
recording numeric values exactly equal to `0.5` at a path containing `fat`.
The raw-text fallback was therefore covered by the recursive traversal of every
JSON value and path.

For evidence, each hit barcode was searched only in `02_products/**` and
`03_operations/bsip0/**`. A classification required a persisted captured panel:
`nutrition_raw_source.rows`. Those rows were replayed with
`parse_nutrition_rows` and then `parse_nutrition_numeric` from
`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`. The replay used this
mapping: `energy -> energy_kcal_raw`, `fat -> fat_raw`, `saturated_fat ->
saturated_fat_raw`, `sugar -> sugar_raw`, `carbs -> carbs_raw`, `fiber ->
fiber_raw`, `protein -> protein_raw`, `sodium -> sodium_raw`, and `trans_fat ->
trans_fat_raw`.

The served-file denominator is 757 product records in 20 files:

| File | Products scanned | `fat == 0.5` records |
|---|---:|---:|
| bread_frontend_v3.json | 29 | 2 |
| bread_frontend_v4.json | 23 | 2 |
| brined_cheeses_frontend_v2.json | 36 | 0 |
| cakes_hard_cookies_frontend_v1.json | 62 | 0 |
| cereals_frontend_v2.json | 20 | 15 |
| cheese_frontend_v4.json | 47 | 0 |
| cheese_frontend_v5.json | 47 | 0 |
| chocolate_bars_frontend_v1.json | 23 | 0 |
| chocolate_tablets_frontend_v1.json | 35 | 0 |
| cookies_coffee_frontend_v2.json | 117 | 0 |
| crackers_frontend_v1.json | 53 | 0 |
| granola_frontend_v2.json | 22 | 0 |
| hard_cheeses_frontend_v4.json | 31 | 0 |
| hummus_frontend_v5.json | 57 | 0 |
| juices_frontend_v3.json | 17 | 0 |
| milk_frontend_v1.json | 18 | 0 |
| protein_combined_frontend_v2.json | 32 | 0 |
| snacks_frontend_v5.json | 21 | 0 |
| yogurt_drinkable_frontend_v1.json | 17 | 2 |
| yogurt_spoonable_frontend_v1.json | 50 | 1 |

## Results

“same cereal raw capture” means the local evidence file
`02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json`.
`0.5` appears in `expansion.nutrition.fat` for every record below. One cereal
also has `expansion.nutrition.satFat = 0.5`; that is not the enumerated total-fat
value and is noted only to make the JSON location unambiguous. `NO_EVIDENCE`
means no permitted persisted raw panel was found; it is unknown, not an estimate.

| Product id | Barcode | Category file | Published fat / JSON location | Replayed evidence fat / evidence file | Classification |
|---|---|---|---|---|---|
| bsip1_bread_9398281 | 9398281 | bread_frontend_v3.json | 0.5 / `expansion.nutrition.fat` | — / no persisted raw panel | NO_EVIDENCE |
| bsip1_bread_1902325 | 1902325 | bread_frontend_v3.json | 0.5 / `expansion.nutrition.fat` | — / no persisted raw panel | NO_EVIDENCE |
| bsip1_bread_9398281 | 9398281 | bread_frontend_v4.json | 0.5 / `expansion.nutrition.fat` | — / no persisted raw panel | NO_EVIDENCE |
| bsip1_bread_1902325 | 1902325 | bread_frontend_v4.json | 0.5 / `expansion.nutrition.fat` | — / no persisted raw panel | NO_EVIDENCE |
| bsip1_cereal_5010029000061 | 5010029000061 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 2.0 / `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` | CONFIRMED_DISCREPANCY |
| bsip1_cereal_5900020012814 | 5900020012814 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 2.9 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_72968 | 72968 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 9.4 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_5900020036407 | 5900020036407 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 6.2 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7296073705550 | 7296073705550 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 4.0 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7290017894911 | 7290017894911 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` (also `satFat=0.5`) | 4.7 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7290112495433 | 7290112495433 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 10.8 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7296073705567 | 7296073705567 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 3.5 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7290017894928 | 7290017894928 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 6.0 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7290017894904 | 7290017894904 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 6.0 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7296073642022 | 7296073642022 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 2.3 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_8445291638839 | 8445291638839 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 3.7 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7296073705574 | 7296073705574 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 13.6 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_3387390525960 | 3387390525960 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 7.4 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_cereal_7613030979647 | 7613030979647 | cereals_frontend_v2.json | 0.5 / `expansion.nutrition.fat` | 5.4 / same cereal raw capture | CONFIRMED_DISCREPANCY |
| bsip1_yogurt_7290110325114 | 7290110325114 | yogurt_drinkable_frontend_v1.json | 0.5 / `expansion.nutrition.fat` | — / no permitted persisted raw panel | NO_EVIDENCE |
| bsip1_yogurt_7290110325121 | 7290110325121 | yogurt_drinkable_frontend_v1.json | 0.5 / `expansion.nutrition.fat` | — / no permitted persisted raw panel | NO_EVIDENCE |
| bsip1_yogurt_7290110323585 | 7290110323585 | yogurt_spoonable_frontend_v1.json | 0.5 / `expansion.nutrition.fat` | — / no persisted raw panel | NO_EVIDENCE |

## Distribution and scope note

Distribution across the 22 published-hit records: `CONFIRMED_DISCREPANCY=15`,
`CONSISTENT=0`, `NO_EVIDENCE=7` (most common: `CONFIRMED_DISCREPANCY`, 15).
The 22 records represent 20 unique barcodes because both bread hits are published
in two served versions. The confirmation threshold was an absolute difference
greater than 0.05 g; all 15 replayed results exceed it.

This audit authorizes no correction. Any correction that could move a published
score is a tripwire-1 owner decision.
