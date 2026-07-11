# TASK-595 ? Published Nutrition vs Raw Evidence Damage Scan

## Scope and methodology

- Scanned 20 published shelf files under `bari-web/src/data/comparisons/*_frontend_v*.json`, containing 757 product records.
- Searched every JSON under `02_products/**` and `03_operations/bsip0/**`; found `nutrition_raw_source.rows` for 652 distinct barcodes across 893 captures in 7238 JSON files.
- Duplicate barcode captures: newest was selected by filesystem modification timestamp, then pathname as a deterministic tie-breaker; 199 barcodes had multiple captures.
- Each selected `rows` panel was replayed with `parse_nutrition_rows` followed by `parse_nutrition_numeric` from `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`. Mapping: `energyKcal?energy_kcal`, `fat?fat_g`, `satFat?fat_saturated_g`, `carbs?carbohydrates_g`, `sugar?sugars_g`, `fiber?dietary_fiber_g`, `protein?protein_g`, `sodium?sodium_mg`.
- Units: energy is compared as kcal; non-sodium nutrient fields as grams. Published sodium is normalized to mg per file/product value: values `<=1` are treated as grams and multiplied by 1,000; values `>1` are treated as mg. Replayed sodium is the parser?s `sodium_mg`.
- Buckets: MATCH `|delta| <= 0.05 g`, or `<=0.5 mg/kcal` for sodium/energy; ROUNDING up to `0.15 g`, or `2 mg/kcal`; MATERIAL above those limits. A one-sided field is FIELD_GAP, listed but excluded from damage counts. A product with no selected raw panel is NO_EVIDENCE.

## Published nutrition key mapping per shelf

| Shelf file | Published numeric keys observed |
|---|---|
| `bread_frontend_v3.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `bread_frontend_v4.json` | carbs, energyKcal, fat, fiber, protein, sodium, sugar |
| `brined_cheeses_frontend_v2.json` | carbs, energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `cakes_hard_cookies_frontend_v1.json` | carbs, energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `cereals_frontend_v2.json` | carbs, energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `cheese_frontend_v4.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `cheese_frontend_v5.json` | carbs, energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `chocolate_bars_frontend_v1.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `chocolate_tablets_frontend_v1.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `cookies_coffee_frontend_v2.json` | energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `crackers_frontend_v1.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `granola_frontend_v2.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `hard_cheeses_frontend_v4.json` | carbs, energyKcal, fat, protein, satFat, sodium, sugar |
| `hummus_frontend_v5.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `juices_frontend_v3.json` | energyKcal, fat, protein, sodium, sugar |
| `milk_frontend_v1.json` | carbs, energyKcal, fat, fiber, protein, satFat, sodium, sugar |
| `protein_combined_frontend_v2.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `snacks_frontend_v5.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `yogurt_drinkable_frontend_v1.json` | energyKcal, fat, fiber, protein, sodium, sugar |
| `yogurt_spoonable_frontend_v1.json` | energyKcal, fat, fiber, protein, sodium, sugar |

## Per-shelf damage table

| Shelf file | Products | With evidence | Fully MATCH | ROUNDING-only | ?1 MATERIAL | NO_EVIDENCE | Worst 3 MATERIAL examples |
|---|---:|---:|---:|---:|---:|---:|---|
| `bread_frontend_v3.json` | 29 | 0 | 0 | 0 | 0 | 29 | ? |
| `bread_frontend_v4.json` | 23 | 0 | 0 | 0 | 0 | 23 | ? |
| `brined_cheeses_frontend_v2.json` | 36 | 36 | 13 | 0 | 23 | 0 | bc-036: sodium 1628?1.628 (? 1626.37)<br>bc-002: sodium 1550?1.55 (? 1548.45)<br>bc-024: sodium 1500?1.5 (? 1498.5) |
| `cakes_hard_cookies_frontend_v1.json` | 62 | 55 | 55 | 0 | 0 | 7 | ? |
| `cereals_frontend_v2.json` | 20 | 20 | 5 | 0 | 15 | 0 | bsip1_cereal_7296073705574: fat 0.5?13.6 (? 13.1)<br>bsip1_cereal_7290112495433: fat 0.5?10.8 (? 10.3)<br>bsip1_cereal_72968: fat 0.5?9.4 (? 8.9) |
| `cheese_frontend_v4.json` | 47 | 0 | 0 | 0 | 0 | 47 | ? |
| `cheese_frontend_v5.json` | 47 | 0 | 0 | 0 | 0 | 47 | ? |
| `chocolate_bars_frontend_v1.json` | 23 | 0 | 0 | 0 | 0 | 23 | ? |
| `chocolate_tablets_frontend_v1.json` | 35 | 0 | 0 | 0 | 0 | 35 | ? |
| `cookies_coffee_frontend_v2.json` | 117 | 95 | 95 | 0 | 0 | 22 | ? |
| `crackers_frontend_v1.json` | 53 | 34 | 34 | 0 | 0 | 19 | ? |
| `granola_frontend_v2.json` | 22 | 22 | 22 | 0 | 0 | 0 | ? |
| `hard_cheeses_frontend_v4.json` | 31 | 0 | 0 | 0 | 0 | 31 | ? |
| `hummus_frontend_v5.json` | 57 | 57 | 57 | 0 | 0 | 0 | ? |
| `juices_frontend_v3.json` | 17 | 0 | 0 | 0 | 0 | 17 | ? |
| `milk_frontend_v1.json` | 18 | 0 | 0 | 0 | 0 | 18 | ? |
| `protein_combined_frontend_v2.json` | 32 | 15 | 15 | 0 | 0 | 17 | ? |
| `snacks_frontend_v5.json` | 21 | 21 | 20 | 0 | 1 | 0 | snk-018: sodium 200?0.2 (? 199.8) |
| `yogurt_drinkable_frontend_v1.json` | 17 | 0 | 0 | 0 | 0 | 17 | ? |
| `yogurt_spoonable_frontend_v1.json` | 50 | 4 | 4 | 0 | 0 | 46 | ? |

## Overall distribution summary

- Products: 757 total published records; 359/757 with evidence; 398/757 NO_EVIDENCE.
- Evidence-backed product disposition: FULLY_MATCH=320/359; ROUNDING_ONLY=0/359; MATERIAL_PRODUCT=39/359.
- Field-level MATERIAL differences: 39. FIELD_GAP entries: 5 (not counted as damage).
- Distribution marker: `product_disposition_histogram={FULLY_MATCH:320, ROUNDING_ONLY:0, MATERIAL_PRODUCT:39}; most_common=FULLY_MATCH (count=320)` (denominator: 359 evidence-backed products).
- Sanity anchors passed: cereals fat MATERIAL includes `5010029000061` published 0.5 vs replayed 2.0 and `7296073705574` published 0.5 vs replayed 13.6; cereal fat MATERIAL count=15. At least one evidence-rich shelf has a MATCH majority.

## Full MATERIAL-diff appendix

| Product id | Barcode | Shelf file | Field | Published | Replayed | Delta | Evidence file |
|---|---|---|---|---:|---:|---:|---|
| `bc-003` | `7296073641940` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-002` | `7290102397334` | `brined_cheeses_frontend_v2.json` | `sodium` | 1550 | 1.55 | 1548.45 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-007` | `2133162` | `brined_cheeses_frontend_v2.json` | `sodium` | 1300 | 1.3 | 1298.7 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-009` | `2133889` | `brined_cheeses_frontend_v2.json` | `sodium` | 1200 | 1.2 | 1198.8 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-010` | `7296073641964` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-006` | `7290011499129` | `brined_cheeses_frontend_v2.json` | `sodium` | 1010 | 1.01 | 1008.99 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-012` | `7290011499327` | `brined_cheeses_frontend_v2.json` | `sodium` | 1010 | 1.01 | 1008.99 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-011` | `7290011499105` | `brined_cheeses_frontend_v2.json` | `sodium` | 1200 | 1.2 | 1198.8 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-014` | `7290019790402` | `brined_cheeses_frontend_v2.json` | `sodium` | 1300 | 1.3 | 1298.7 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-037` | `48413` | `brined_cheeses_frontend_v2.json` | `sodium` | 1065 | 1.065 | 1063.93 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-038` | `7290108509755` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-016` | `2107798` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-025` | `7296073641957` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-027` | `7296073641902` | `brined_cheeses_frontend_v2.json` | `sodium` | 1100 | 1.1 | 1098.9 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-018` | `7290019790808` | `brined_cheeses_frontend_v2.json` | `sodium` | 1400 | 1.4 | 1398.6 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-036` | `3075805` | `brined_cheeses_frontend_v2.json` | `sodium` | 1628 | 1.628 | 1626.37 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-041` | `7296073641919` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-024` | `7290019790112` | `brined_cheeses_frontend_v2.json` | `sodium` | 1500 | 1.5 | 1498.5 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-017` | `7290114314015` | `brined_cheeses_frontend_v2.json` | `sodium` | 1400 | 1.4 | 1398.6 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-030` | `7290011499112` | `brined_cheeses_frontend_v2.json` | `sodium` | 1200 | 1.2 | 1198.8 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-032` | `7290019635222` | `brined_cheeses_frontend_v2.json` | `sodium` | 1010 | 1.01 | 1008.99 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-035` | `7290017065236` | `brined_cheeses_frontend_v2.json` | `sodium` | 1010 | 1.01 | 1008.99 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bc-044` | `7290011499365` | `brined_cheeses_frontend_v2.json` | `sodium` | 1000 | 1 | 999 | `02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json` |
| `bsip1_cereal_5010029000061` | `5010029000061` | `cereals_frontend_v2.json` | `fat` | 0.5 | 2 | 1.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_5900020012814` | `5900020012814` | `cereals_frontend_v2.json` | `fat` | 0.5 | 2.9 | 2.4 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_72968` | `72968` | `cereals_frontend_v2.json` | `fat` | 0.5 | 9.4 | 8.9 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_5900020036407` | `5900020036407` | `cereals_frontend_v2.json` | `fat` | 0.5 | 6.2 | 5.7 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7296073705550` | `7296073705550` | `cereals_frontend_v2.json` | `fat` | 0.5 | 4 | 3.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290017894911` | `7290017894911` | `cereals_frontend_v2.json` | `fat` | 0.5 | 4.7 | 4.2 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290112495433` | `7290112495433` | `cereals_frontend_v2.json` | `fat` | 0.5 | 10.8 | 10.3 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7296073705567` | `7296073705567` | `cereals_frontend_v2.json` | `fat` | 0.5 | 3.5 | 3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290017894928` | `7290017894928` | `cereals_frontend_v2.json` | `fat` | 0.5 | 6 | 5.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290017894904` | `7290017894904` | `cereals_frontend_v2.json` | `fat` | 0.5 | 6 | 5.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7296073642022` | `7296073642022` | `cereals_frontend_v2.json` | `fat` | 0.5 | 2.3 | 1.8 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_8445291638839` | `8445291638839` | `cereals_frontend_v2.json` | `fat` | 0.5 | 3.7 | 3.2 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7296073705574` | `7296073705574` | `cereals_frontend_v2.json` | `fat` | 0.5 | 13.6 | 13.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_3387390525960` | `3387390525960` | `cereals_frontend_v2.json` | `fat` | 0.5 | 7.4 | 6.9 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7613030979647` | `7613030979647` | `cereals_frontend_v2.json` | `fat` | 0.5 | 5.4 | 4.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-018` | `7290019297208` | `snacks_frontend_v5.json` | `sodium` | 200 | 0.2 | 199.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |

## FIELD_GAP appendix

| Product id | Barcode | Shelf file | Field | Published | Replayed | Evidence file |
|---|---|---|---|---|---|---|
| `ck-7290013453693` | `7290013453693` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 33.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013453068` | `7290013453068` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 53.8 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290119043149` | `7290119043149` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 60.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `bsip1_cookies_80083764` | `80083764` | `cookies_coffee_frontend_v2.json` | `satFat` | None | 2.3 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `bsip1_cookies_80083764` | `80083764` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 61.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290017962139` | `7290017962139` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 48.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740113` | `7290013740113` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 50.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-540160` | `540160` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740137` | `7290013740137` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 41.3 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740557` | `7290013740557` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 68.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119043743` | `7290119043743` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-960860015432` | `960860015432` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 67.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740472` | `7290013740472` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 59.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-311463` | `311463` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 71.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013453501` | `7290013453501` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 47.7 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740540` | `7290013740540` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 40.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740052` | `7290013740052` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 52.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740229` | `7290013740229` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 42.3 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740342` | `7290013740342` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 54.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740465` | `7290013740465` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 51.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290018371930` | `7290018371930` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 59.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290018371923` | `7290018371923` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-5317194` | `5317194` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 75.5 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290011489625` | `7290011489625` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 75.5 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290018371947` | `7290018371947` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 61.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119041053` | `7290119041053` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119041107` | `7290119041107` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119041152` | `7290119041152` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290018893845` | `7290018893845` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 78.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740014` | `7290013740014` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 52.3 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290017894317` | `7290017894317` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-2986065` | `2986065` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 71.2 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290017898506` | `7290017898506` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 48.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-2986058` | `2986058` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-313184` | `313184` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 76.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4823077614699` | `4823077614699` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 65.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7296073453857` | `7296073453857` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 57.8 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290019293804` | `7290019293804` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 35.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7296073453840` | `7296073453840` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.6 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290118426615` | `7290118426615` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290019816034` | `7290019816034` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 31.4 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-8410376075915` | `8410376075915` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-4820180816590` | `4820180816590` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 61.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-80083665` | `80083665` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4820180816576` | `4820180816576` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119043798` | `7290119043798` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 58.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290013740694` | `7290013740694` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 55.4 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290123330488` | `7290123330488` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 37.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4823077633317` | `4823077633317` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.1 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-313160` | `313160` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.2 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-311708` | `311708` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 67.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-8008698037171` | `8008698037171` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 59.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-74184` | `74184` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 76.5 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119041206` | `7290119041206` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 57.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119041350` | `7290119041350` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 57.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119043095` | `7290119043095` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 57.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7296073162001` | `7296073162001` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 56.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290018893036` | `7290018893036` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-311128` | `311128` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 69.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119040803` | `7290119040803` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 58.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119040858` | `7290119040858` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 58.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-5410126006049` | `5410126006049` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-5410126116168` | `5410126116168` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-5410126726244` | `5410126726244` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-5410126806250` | `5410126806250` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 72.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4823077614675` | `4823077614675` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 65.9 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4820180816552` | `4820180816552` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 67.4 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-8710502279010` | `8710502279010` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 59.4 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290112961754` | `7290112961754` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 66.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-4017100198151` | `4017100198151` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-99804` | `99804` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119043897` | `7290119043897` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.1 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7296073529019` | `7296073529019` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.1 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-46214731552` | `46214731552` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 59.9 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7296073529026` | `7296073529026` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.4 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-4017100364112` | `4017100364112` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-8000500366073` | `8000500366073` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-46214930207` | `46214930207` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 61.9 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7622300356767` | `7622300356767` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-61245` | `61245` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 62.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7296073161981` | `7296073161981` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 54.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290106656727` | `7290106656727` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 71.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290019816232` | `7290019816232` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 40.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-8710502470028` | `8710502470028` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 60.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290119040605` | `7290119040605` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 55.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290119040650` | `7290119040650` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 55.6 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290112340276` | `7290112340276` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 53.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290115206333` | `7290115206333` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7622201809188` | `7622201809188` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 67.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290101111986` | `7290101111986` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 35.8 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-8710502064814` | `8710502064814` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 61.3 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7290119040179` | `7290119040179` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 66.7 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290019816058` | `7290019816058` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 36.7 | `02_products/cakes_hard_cookies/bsip0_outputs/cakes_shufersal_bsip0_raw_20260614T125027.json` |
| `ck-7622210453327` | `7622210453327` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 63.0 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290109354996` | `7290109354996` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 83.8 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `ck-7290109354972` | `7290109354972` | `cookies_coffee_frontend_v2.json` | `carbs` | None | 85.2 | `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` |
| `bsip1_ricecakes_7296073343202` | `7296073343202` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073343202` | `7296073343202` | `crackers_frontend_v1.json` | `carbs` | None | 70.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073420323` | `7296073420323` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073420323` | `7296073420323` | `crackers_frontend_v1.json` | `carbs` | None | 70.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073420330` | `7296073420330` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073420330` | `7296073420330` | `crackers_frontend_v1.json` | `carbs` | None | 70.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290019431794` | `7290019431794` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290019431794` | `7290019431794` | `crackers_frontend_v1.json` | `carbs` | None | 78.2 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290020179043` | `7290020179043` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290020179043` | `7290020179043` | `crackers_frontend_v1.json` | `carbs` | None | 78.2 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000046` | `9322969000046` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000046` | `9322969000046` | `crackers_frontend_v1.json` | `carbs` | None | 69.9 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290018371275` | `7290018371275` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290018371275` | `7290018371275` | `crackers_frontend_v1.json` | `carbs` | None | 69.7 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000022` | `9322969000022` | `crackers_frontend_v1.json` | `satFat` | None | 1.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000022` | `9322969000022` | `crackers_frontend_v1.json` | `carbs` | None | 64.4 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000015` | `9322969000015` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000015` | `9322969000015` | `crackers_frontend_v1.json` | `carbs` | None | 70.9 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073106098` | `7296073106098` | `crackers_frontend_v1.json` | `satFat` | None | 0.7 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073106098` | `7296073106098` | `crackers_frontend_v1.json` | `carbs` | None | 80.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290110560317` | `7290110560317` | `crackers_frontend_v1.json` | `satFat` | None | 1.4 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290110560317` | `7290110560317` | `crackers_frontend_v1.json` | `carbs` | None | 65.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073592440` | `7296073592440` | `crackers_frontend_v1.json` | `satFat` | None | 1.4 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073592440` | `7296073592440` | `crackers_frontend_v1.json` | `carbs` | None | 65.1 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290017325422` | `7290017325422` | `crackers_frontend_v1.json` | `satFat` | None | 1.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290017325422` | `7290017325422` | `crackers_frontend_v1.json` | `carbs` | None | 79.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000039` | `9322969000039` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_9322969000039` | `9322969000039` | `crackers_frontend_v1.json` | `carbs` | None | 72.1 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073079019` | `7296073079019` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073079019` | `7296073079019` | `crackers_frontend_v1.json` | `carbs` | None | 79.6 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073195252` | `7296073195252` | `crackers_frontend_v1.json` | `satFat` | None | 0.7 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073195252` | `7296073195252` | `crackers_frontend_v1.json` | `carbs` | None | 79.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073195269` | `7296073195269` | `crackers_frontend_v1.json` | `satFat` | None | 0.9 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073195269` | `7296073195269` | `crackers_frontend_v1.json` | `carbs` | None | 79.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_4952792` | `4952792` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_4952792` | `4952792` | `crackers_frontend_v1.json` | `carbs` | None | 75.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073079002` | `7296073079002` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073079002` | `7296073079002` | `crackers_frontend_v1.json` | `carbs` | None | 82.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073151463` | `7296073151463` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073151463` | `7296073151463` | `crackers_frontend_v1.json` | `carbs` | None | 82.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073343219` | `7296073343219` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073343219` | `7296073343219` | `crackers_frontend_v1.json` | `carbs` | None | 82.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073441335` | `7296073441335` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073441335` | `7296073441335` | `crackers_frontend_v1.json` | `carbs` | None | 82.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290111564291` | `7290111564291` | `crackers_frontend_v1.json` | `satFat` | None | 0.7 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290111564291` | `7290111564291` | `crackers_frontend_v1.json` | `carbs` | None | 77.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290112340122` | `7290112340122` | `crackers_frontend_v1.json` | `satFat` | None | 0.8 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290112340122` | `7290112340122` | `crackers_frontend_v1.json` | `carbs` | None | 79.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290112348999` | `7290112348999` | `crackers_frontend_v1.json` | `satFat` | None | 0.4 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290112348999` | `7290112348999` | `crackers_frontend_v1.json` | `carbs` | None | 80.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073161479` | `7296073161479` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073161479` | `7296073161479` | `crackers_frontend_v1.json` | `carbs` | None | 80.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290110560300` | `7290110560300` | `crackers_frontend_v1.json` | `satFat` | None | 1.2 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290110560300` | `7290110560300` | `crackers_frontend_v1.json` | `carbs` | None | 66.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118426530` | `7290118426530` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118426530` | `7290118426530` | `crackers_frontend_v1.json` | `carbs` | None | 82.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118426516` | `7290118426516` | `crackers_frontend_v1.json` | `satFat` | None | 0.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118426516` | `7290118426516` | `crackers_frontend_v1.json` | `carbs` | None | 82.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_8423207208871` | `8423207208871` | `crackers_frontend_v1.json` | `satFat` | None | 0.3 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_8423207208871` | `8423207208871` | `crackers_frontend_v1.json` | `carbs` | None | 82.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073450740` | `7296073450740` | `crackers_frontend_v1.json` | `satFat` | None | 1.3 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7296073450740` | `7296073450740` | `crackers_frontend_v1.json` | `carbs` | None | 72.4 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290119373352` | `7290119373352` | `crackers_frontend_v1.json` | `satFat` | None | 0.9 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290119373352` | `7290119373352` | `crackers_frontend_v1.json` | `carbs` | None | 78.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118422129` | `7290118422129` | `crackers_frontend_v1.json` | `satFat` | None | 1.5 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_7290118422129` | `7290118422129` | `crackers_frontend_v1.json` | `carbs` | None | 64.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_4267230` | `4267230` | `crackers_frontend_v1.json` | `satFat` | None | 14.0 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_ricecakes_4267230` | `4267230` | `crackers_frontend_v1.json` | `carbs` | None | 69.1 | `02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json` |
| `bsip1_cereal_7290017962047` | `7290017962047` | `granola_frontend_v2.json` | `satFat` | None | 4.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290017962047` | `7290017962047` | `granola_frontend_v2.json` | `carbs` | None | 44.6 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290116534619` | `7290116534619` | `granola_frontend_v2.json` | `satFat` | None | 3.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290116534619` | `7290116534619` | `granola_frontend_v2.json` | `carbs` | None | 50.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290017962023` | `7290017962023` | `granola_frontend_v2.json` | `satFat` | None | 4.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290017962023` | `7290017962023` | `granola_frontend_v2.json` | `carbs` | None | 47.7 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290106771369` | `7290106771369` | `granola_frontend_v2.json` | `satFat` | None | 3.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290106771369` | `7290106771369` | `granola_frontend_v2.json` | `carbs` | None | 45.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290106773714` | `7290106773714` | `granola_frontend_v2.json` | `satFat` | None | 3.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290106773714` | `7290106773714` | `granola_frontend_v2.json` | `carbs` | None | 27.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290112498007` | `7290112498007` | `granola_frontend_v2.json` | `satFat` | None | 2.1 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290112498007` | `7290112498007` | `granola_frontend_v2.json` | `carbs` | None | 46.9 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290106771314` | `7290106771314` | `granola_frontend_v2.json` | `satFat` | None | 3.8 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290106771314` | `7290106771314` | `granola_frontend_v2.json` | `carbs` | None | 47.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290013433244` | `7290013433244` | `granola_frontend_v2.json` | `satFat` | None | 2.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290013433244` | `7290013433244` | `granola_frontend_v2.json` | `carbs` | None | 50.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290112497994` | `7290112497994` | `granola_frontend_v2.json` | `satFat` | None | 3.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290112497994` | `7290112497994` | `granola_frontend_v2.json` | `carbs` | None | 51.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290013433336` | `7290013433336` | `granola_frontend_v2.json` | `satFat` | None | 4.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290013433336` | `7290013433336` | `granola_frontend_v2.json` | `carbs` | None | 47.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290106771161` | `7290106771161` | `granola_frontend_v2.json` | `satFat` | None | 3.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290106771161` | `7290106771161` | `granola_frontend_v2.json` | `carbs` | None | 55.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290013433091` | `7290013433091` | `granola_frontend_v2.json` | `satFat` | None | 4.8 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290013433091` | `7290013433091` | `granola_frontend_v2.json` | `carbs` | None | 58.0 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290013433107` | `7290013433107` | `granola_frontend_v2.json` | `satFat` | None | 3.5 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7290013433107` | `7290013433107` | `granola_frontend_v2.json` | `carbs` | None | 48.0 | `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json` |
| `bsip1_cereal_7613035635845` | `7613035635845` | `granola_frontend_v2.json` | `satFat` | None | 2.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7613035635845` | `7613035635845` | `granola_frontend_v2.json` | `carbs` | None | 62.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7613037012095` | `7613037012095` | `granola_frontend_v2.json` | `satFat` | None | 2.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7613037012095` | `7613037012095` | `granola_frontend_v2.json` | `carbs` | None | 61.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7613035622623` | `7613035622623` | `granola_frontend_v2.json` | `satFat` | None | 1.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7613035622623` | `7613035622623` | `granola_frontend_v2.json` | `carbs` | None | 65.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131968` | `7290011131968` | `granola_frontend_v2.json` | `satFat` | None | 3.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131968` | `7290011131968` | `granola_frontend_v2.json` | `carbs` | None | 61.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131050` | `7290011131050` | `granola_frontend_v2.json` | `satFat` | None | 3.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131050` | `7290011131050` | `granola_frontend_v2.json` | `carbs` | None | 63.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011668587` | `7290011668587` | `granola_frontend_v2.json` | `satFat` | None | 3.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011668587` | `7290011668587` | `granola_frontend_v2.json` | `carbs` | None | 53.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290014471443` | `7290014471443` | `granola_frontend_v2.json` | `satFat` | None | 2.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290014471443` | `7290014471443` | `granola_frontend_v2.json` | `carbs` | None | 54.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131975` | `7290011131975` | `granola_frontend_v2.json` | `satFat` | None | 3.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_7290011131975` | `7290011131975` | `granola_frontend_v2.json` | `carbs` | None | 64.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_1343845` | `1343845` | `granola_frontend_v2.json` | `satFat` | None | 2.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_cereal_1343845` | `1343845` | `granola_frontend_v2.json` | `carbs` | None | 56.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_7296073725404` | `7296073725404` | `hummus_frontend_v5.json` | `satFat` | None | 3.2 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725404.json` |
| `bsip1_7296073725404` | `7296073725404` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725404.json` |
| `bsip1_6666307` | `6666307` | `hummus_frontend_v5.json` | `satFat` | None | 3.2 | `02_products/hummus/observations_bsip0/shufersal/P_6666307.json` |
| `bsip1_6666307` | `6666307` | `hummus_frontend_v5.json` | `carbs` | None | 12.4 | `02_products/hummus/observations_bsip0/shufersal/P_6666307.json` |
| `bsip1_6666444` | `6666444` | `hummus_frontend_v5.json` | `carbs` | None | 9.7 | `02_products/hummus/observations_bsip0/shufersal/P_6666444.json` |
| `bsip1_7296073725565` | `7296073725565` | `hummus_frontend_v5.json` | `satFat` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725565.json` |
| `bsip1_7296073725565` | `7296073725565` | `hummus_frontend_v5.json` | `carbs` | None | 11.7 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725565.json` |
| `bsip1_7296073725589` | `7296073725589` | `hummus_frontend_v5.json` | `satFat` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725589.json` |
| `bsip1_7296073725589` | `7296073725589` | `hummus_frontend_v5.json` | `carbs` | None | 11.7 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725589.json` |
| `bsip1_7290015858175` | `7290015858175` | `hummus_frontend_v5.json` | `satFat` | None | 1.2 | `02_products/hummus/observations_bsip0/shufersal/P_7290015858175.json` |
| `bsip1_7290015858175` | `7290015858175` | `hummus_frontend_v5.json` | `carbs` | None | 9.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290015858175.json` |
| `bsip1_7290110564360` | `7290110564360` | `hummus_frontend_v5.json` | `satFat` | None | 3.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290110564360.json` |
| `bsip1_7290110564360` | `7290110564360` | `hummus_frontend_v5.json` | `carbs` | None | 6.8 | `02_products/hummus/observations_bsip0/shufersal/P_7290110564360.json` |
| `bsip1_7290110579319` | `7290110579319` | `hummus_frontend_v5.json` | `satFat` | None | 2.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290110579319.json` |
| `bsip1_7290110579319` | `7290110579319` | `hummus_frontend_v5.json` | `carbs` | None | 10.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290110579319.json` |
| `bsip1_7290110557478` | `7290110557478` | `hummus_frontend_v5.json` | `satFat` | None | 2.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290110557478.json` |
| `bsip1_7290110557478` | `7290110557478` | `hummus_frontend_v5.json` | `carbs` | None | 10.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290110557478.json` |
| `bsip1_7290011800642` | `7290011800642` | `hummus_frontend_v5.json` | `satFat` | None | 0.3 | `02_products/hummus/observations_bsip0/shufersal/P_7290011800642.json` |
| `bsip1_7290011800642` | `7290011800642` | `hummus_frontend_v5.json` | `carbs` | None | 8.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290011800642.json` |
| `bsip1_7296073725381` | `7296073725381` | `hummus_frontend_v5.json` | `satFat` | None | 3.2 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725381.json` |
| `bsip1_7296073725381` | `7296073725381` | `hummus_frontend_v5.json` | `carbs` | None | 12.6 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725381.json` |
| `bsip1_3727667` | `3727667` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_3727667.json` |
| `bsip1_3727667` | `3727667` | `hummus_frontend_v5.json` | `carbs` | None | 14.0 | `02_products/hummus/observations_bsip0/shufersal/P_3727667.json` |
| `bsip1_7290106576513` | `7290106576513` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290106576513.json` |
| `bsip1_7290106576513` | `7290106576513` | `hummus_frontend_v5.json` | `carbs` | None | 14.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290106576513.json` |
| `bsip1_5174551` | `5174551` | `hummus_frontend_v5.json` | `satFat` | None | 1.5 | `02_products/hummus/observations_bsip0/shufersal/P_5174551.json` |
| `bsip1_5174551` | `5174551` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_5174551.json` |
| `bsip1_7290105964564` | `7290105964564` | `hummus_frontend_v5.json` | `satFat` | None | 1.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290105964564.json` |
| `bsip1_7290105964564` | `7290105964564` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290105964564.json` |
| `bsip1_2987963` | `2987963` | `hummus_frontend_v5.json` | `satFat` | None | 1.5 | `02_products/hummus/observations_bsip0/shufersal/P_2987963.json` |
| `bsip1_2987963` | `2987963` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_2987963.json` |
| `bsip1_8645935` | `8645935` | `hummus_frontend_v5.json` | `satFat` | None | 1.5 | `02_products/hummus/observations_bsip0/shufersal/P_8645935.json` |
| `bsip1_8645935` | `8645935` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_8645935.json` |
| `bsip1_7290119387434` | `7290119387434` | `hummus_frontend_v5.json` | `satFat` | None | 1.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290119387434.json` |
| `bsip1_7290119387434` | `7290119387434` | `hummus_frontend_v5.json` | `carbs` | None | 10.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290119387434.json` |
| `bsip1_7296073725497` | `7296073725497` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725497.json` |
| `bsip1_7296073725497` | `7296073725497` | `hummus_frontend_v5.json` | `carbs` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725497.json` |
| `bsip1_7296073725374` | `7296073725374` | `hummus_frontend_v5.json` | `satFat` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725374.json` |
| `bsip1_7296073725374` | `7296073725374` | `hummus_frontend_v5.json` | `carbs` | None | 11.2 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725374.json` |
| `bsip1_7290106573642` | `7290106573642` | `hummus_frontend_v5.json` | `satFat` | None | 2.1 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573642.json` |
| `bsip1_7290106573642` | `7290106573642` | `hummus_frontend_v5.json` | `carbs` | None | 13.8 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573642.json` |
| `bsip1_7296073725367` | `7296073725367` | `hummus_frontend_v5.json` | `satFat` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725367.json` |
| `bsip1_7296073725367` | `7296073725367` | `hummus_frontend_v5.json` | `carbs` | None | 11.6 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725367.json` |
| `bsip1_7290010931330` | `7290010931330` | `hummus_frontend_v5.json` | `satFat` | None | 0.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290010931330.json` |
| `bsip1_7290010931330` | `7290010931330` | `hummus_frontend_v5.json` | `carbs` | None | 8.1 | `02_products/hummus/observations_bsip0/shufersal/P_7290010931330.json` |
| `bsip1_8644112` | `8644112` | `hummus_frontend_v5.json` | `satFat` | None | 0.4 | `02_products/hummus/observations_bsip0/shufersal/P_8644112.json` |
| `bsip1_8644112` | `8644112` | `hummus_frontend_v5.json` | `carbs` | None | 8.1 | `02_products/hummus/observations_bsip0/shufersal/P_8644112.json` |
| `bsip1_7290107958639` | `7290107958639` | `hummus_frontend_v5.json` | `satFat` | None | 0.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290107958639.json` |
| `bsip1_7290107958639` | `7290107958639` | `hummus_frontend_v5.json` | `carbs` | None | 8.6 | `02_products/hummus/observations_bsip0/shufersal/P_7290107958639.json` |
| `bsip1_7290104721533` | `7290104721533` | `hummus_frontend_v5.json` | `carbs` | None | 6.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290104721533.json` |
| `bsip1_467320` | `467320` | `hummus_frontend_v5.json` | `satFat` | None | 3.4 | `02_products/hummus/observations_bsip0/shufersal/P_467320.json` |
| `bsip1_467320` | `467320` | `hummus_frontend_v5.json` | `carbs` | None | 15.0 | `02_products/hummus/observations_bsip0/shufersal/P_467320.json` |
| `bsip1_7290104061431` | `7290104061431` | `hummus_frontend_v5.json` | `satFat` | None | 1.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061431.json` |
| `bsip1_7290104061431` | `7290104061431` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061431.json` |
| `bsip1_7290106576537` | `7290106576537` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290106576537.json` |
| `bsip1_7290106576537` | `7290106576537` | `hummus_frontend_v5.json` | `carbs` | None | 14.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290106576537.json` |
| `bsip1_7290122780314` | `7290122780314` | `hummus_frontend_v5.json` | `satFat` | None | 2.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290122780314.json` |
| `bsip1_7290122780314` | `7290122780314` | `hummus_frontend_v5.json` | `carbs` | None | 13.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290122780314.json` |
| `bsip1_7290106573598` | `7290106573598` | `hummus_frontend_v5.json` | `satFat` | None | 3.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573598.json` |
| `bsip1_7290106573598` | `7290106573598` | `hummus_frontend_v5.json` | `carbs` | None | 15.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573598.json` |
| `bsip1_7290119373710` | `7290119373710` | `hummus_frontend_v5.json` | `satFat` | None | 3.6 | `02_products/hummus/observations_bsip0/shufersal/P_7290119373710.json` |
| `bsip1_7290119373710` | `7290119373710` | `hummus_frontend_v5.json` | `carbs` | None | 6.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290119373710.json` |
| `bsip1_7290104061424` | `7290104061424` | `hummus_frontend_v5.json` | `satFat` | None | 1.6 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061424.json` |
| `bsip1_7290104061424` | `7290104061424` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061424.json` |
| `bsip1_7290115202434` | `7290115202434` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290115202434.json` |
| `bsip1_7290115202434` | `7290115202434` | `hummus_frontend_v5.json` | `carbs` | None | 14.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290115202434.json` |
| `bsip1_467153` | `467153` | `hummus_frontend_v5.json` | `satFat` | None | 4.0 | `02_products/hummus/observations_bsip0/shufersal/P_467153.json` |
| `bsip1_467153` | `467153` | `hummus_frontend_v5.json` | `carbs` | None | 12.0 | `02_products/hummus/observations_bsip0/shufersal/P_467153.json` |
| `bsip1_7290106573819` | `7290106573819` | `hummus_frontend_v5.json` | `satFat` | None | 1.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573819.json` |
| `bsip1_7290106573819` | `7290106573819` | `hummus_frontend_v5.json` | `carbs` | None | 14.2 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573819.json` |
| `bsip1_7290119374892` | `7290119374892` | `hummus_frontend_v5.json` | `satFat` | None | 1.1 | `02_products/hummus/observations_bsip0/shufersal/P_7290119374892.json` |
| `bsip1_7290119374892` | `7290119374892` | `hummus_frontend_v5.json` | `carbs` | None | 9.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290119374892.json` |
| `bsip1_7290106573628` | `7290106573628` | `hummus_frontend_v5.json` | `satFat` | None | 2.1 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573628.json` |
| `bsip1_7290106573628` | `7290106573628` | `hummus_frontend_v5.json` | `carbs` | None | 13.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290106573628.json` |
| `bsip1_7290104061417` | `7290104061417` | `hummus_frontend_v5.json` | `satFat` | None | 1.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061417.json` |
| `bsip1_7290104061417` | `7290104061417` | `hummus_frontend_v5.json` | `carbs` | None | 9.9 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061417.json` |
| `bsip1_7290112968685` | `7290112968685` | `hummus_frontend_v5.json` | `satFat` | None | 3.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290112968685.json` |
| `bsip1_7290112968685` | `7290112968685` | `hummus_frontend_v5.json` | `carbs` | None | 13.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290112968685.json` |
| `bsip1_7296073725398` | `7296073725398` | `hummus_frontend_v5.json` | `satFat` | None | 3.1 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725398.json` |
| `bsip1_7296073725398` | `7296073725398` | `hummus_frontend_v5.json` | `carbs` | None | 12.6 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725398.json` |
| `bsip1_7290115207484` | `7290115207484` | `hummus_frontend_v5.json` | `satFat` | None | 0.8 | `02_products/hummus/observations_bsip0/shufersal/P_7290115207484.json` |
| `bsip1_7290115207484` | `7290115207484` | `hummus_frontend_v5.json` | `carbs` | None | 5.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290115207484.json` |
| `bsip1_7290104061448` | `7290104061448` | `hummus_frontend_v5.json` | `satFat` | None | 1.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061448.json` |
| `bsip1_7290104061448` | `7290104061448` | `hummus_frontend_v5.json` | `carbs` | None | 10.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290104061448.json` |
| `bsip1_7290115202687` | `7290115202687` | `hummus_frontend_v5.json` | `satFat` | None | 2.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290115202687.json` |
| `bsip1_7290115202687` | `7290115202687` | `hummus_frontend_v5.json` | `carbs` | None | 14.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290115202687.json` |
| `bsip1_7290111563492` | `7290111563492` | `hummus_frontend_v5.json` | `satFat` | None | 0.3 | `02_products/hummus/observations_bsip0/shufersal/P_7290111563492.json` |
| `bsip1_7290111563492` | `7290111563492` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290111563492.json` |
| `bsip1_7290106577572` | `7290106577572` | `hummus_frontend_v5.json` | `satFat` | None | 0.3 | `02_products/hummus/observations_bsip0/shufersal/P_7290106577572.json` |
| `bsip1_7290106577572` | `7290106577572` | `hummus_frontend_v5.json` | `carbs` | None | 10.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290106577572.json` |
| `bsip1_3989096` | `3989096` | `hummus_frontend_v5.json` | `satFat` | None | 0.8 | `02_products/hummus/observations_bsip0/shufersal/P_3989096.json` |
| `bsip1_3989096` | `3989096` | `hummus_frontend_v5.json` | `carbs` | None | 10.6 | `02_products/hummus/observations_bsip0/shufersal/P_3989096.json` |
| `bsip1_7296073725510` | `7296073725510` | `hummus_frontend_v5.json` | `satFat` | None | 0.9 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725510.json` |
| `bsip1_7296073725510` | `7296073725510` | `hummus_frontend_v5.json` | `carbs` | None | 7.1 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725510.json` |
| `bsip1_7296073725633` | `7296073725633` | `hummus_frontend_v5.json` | `satFat` | None | 0.9 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725633.json` |
| `bsip1_7296073725633` | `7296073725633` | `hummus_frontend_v5.json` | `carbs` | None | 7.1 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725633.json` |
| `bsip1_7290105366023` | `7290105366023` | `hummus_frontend_v5.json` | `satFat` | None | 1.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290105366023.json` |
| `bsip1_7290105366023` | `7290105366023` | `hummus_frontend_v5.json` | `carbs` | None | 8.2 | `02_products/hummus/observations_bsip0/shufersal/P_7290105366023.json` |
| `bsip1_7296073725640` | `7296073725640` | `hummus_frontend_v5.json` | `satFat` | None | 1.7 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725640.json` |
| `bsip1_7296073725640` | `7296073725640` | `hummus_frontend_v5.json` | `carbs` | None | 15.3 | `02_products/hummus/observations_bsip0/shufersal/P_7296073725640.json` |
| `bsip1_6724786` | `6724786` | `hummus_frontend_v5.json` | `satFat` | None | 2.4 | `02_products/hummus/observations_bsip0/shufersal/P_6724786.json` |
| `bsip1_6724786` | `6724786` | `hummus_frontend_v5.json` | `carbs` | None | 8.5 | `02_products/hummus/observations_bsip0/shufersal/P_6724786.json` |
| `bsip1_7290119374885` | `7290119374885` | `hummus_frontend_v5.json` | `satFat` | None | 1.2 | `02_products/hummus/observations_bsip0/shufersal/P_7290119374885.json` |
| `bsip1_7290119374885` | `7290119374885` | `hummus_frontend_v5.json` | `carbs` | None | 10.7 | `02_products/hummus/observations_bsip0/shufersal/P_7290119374885.json` |
| `bsip1_7290106520905` | `7290106520905` | `hummus_frontend_v5.json` | `satFat` | None | 0.6 | `02_products/hummus/observations_bsip0/shufersal/P_7290106520905.json` |
| `bsip1_7290106520905` | `7290106520905` | `hummus_frontend_v5.json` | `carbs` | None | 8.8 | `02_products/hummus/observations_bsip0/shufersal/P_7290106520905.json` |
| `bsip1_7296073451969` | `7296073451969` | `hummus_frontend_v5.json` | `satFat` | None | 1.0 | `02_products/hummus/observations_bsip0/shufersal/P_7296073451969.json` |
| `bsip1_7296073451969` | `7296073451969` | `hummus_frontend_v5.json` | `carbs` | None | 14.1 | `02_products/hummus/observations_bsip0/shufersal/P_7296073451969.json` |
| `bsip1_7290010154265` | `7290010154265` | `hummus_frontend_v5.json` | `satFat` | None | 3.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290010154265.json` |
| `bsip1_7290010154265` | `7290010154265` | `hummus_frontend_v5.json` | `carbs` | None | 19.0 | `02_products/hummus/observations_bsip0/shufersal/P_7290010154265.json` |
| `bsip1_7290106577480` | `7290106577480` | `hummus_frontend_v5.json` | `satFat` | None | 2.4 | `02_products/hummus/observations_bsip0/shufersal/P_7290106577480.json` |
| `bsip1_7290106577480` | `7290106577480` | `hummus_frontend_v5.json` | `carbs` | None | 6.5 | `02_products/hummus/observations_bsip0/shufersal/P_7290106577480.json` |
| `pb-002` | `7290017516295` | `protein_combined_frontend_v2.json` | `satFat` | None | 1.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-002` | `7290017516295` | `protein_combined_frontend_v2.json` | `carbs` | None | 31.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-003` | `7290121161886` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-003` | `7290121161886` | `protein_combined_frontend_v2.json` | `carbs` | None | 31.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-004` | `7290121166850` | `protein_combined_frontend_v2.json` | `satFat` | None | 3.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-004` | `7290121166850` | `protein_combined_frontend_v2.json` | `carbs` | None | 37.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-005` | `8410076610379` | `protein_combined_frontend_v2.json` | `satFat` | None | 7.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-005` | `8410076610379` | `protein_combined_frontend_v2.json` | `carbs` | None | 27.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-010` | `7290119371112` | `protein_combined_frontend_v2.json` | `satFat` | None | 8.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-010` | `7290119371112` | `protein_combined_frontend_v2.json` | `carbs` | None | 30.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-006` | `8410076610386` | `protein_combined_frontend_v2.json` | `satFat` | None | 7.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-006` | `8410076610386` | `protein_combined_frontend_v2.json` | `carbs` | None | 26.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-018` | `7290117384589` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-018` | `7290117384589` | `protein_combined_frontend_v2.json` | `carbs` | None | 34.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-019` | `7290117384596` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-019` | `7290117384596` | `protein_combined_frontend_v2.json` | `carbs` | None | 34.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-020` | `7290121160582` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-020` | `7290121160582` | `protein_combined_frontend_v2.json` | `carbs` | None | 31.6 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-021` | `7290121161916` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-021` | `7290121161916` | `protein_combined_frontend_v2.json` | `carbs` | None | 32.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-022` | `7290121161930` | `protein_combined_frontend_v2.json` | `satFat` | None | 4.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-022` | `7290121161930` | `protein_combined_frontend_v2.json` | `carbs` | None | 32.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-012` | `7290019401049` | `protein_combined_frontend_v2.json` | `satFat` | None | 5.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-012` | `7290019401049` | `protein_combined_frontend_v2.json` | `carbs` | None | 31.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-031` | `7290112915382` | `protein_combined_frontend_v2.json` | `satFat` | None | 9.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-031` | `7290112915382` | `protein_combined_frontend_v2.json` | `carbs` | None | 33.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-032` | `7290112913487` | `protein_combined_frontend_v2.json` | `satFat` | None | 11.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-032` | `7290112913487` | `protein_combined_frontend_v2.json` | `carbs` | None | 32.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-033` | `7290112915351` | `protein_combined_frontend_v2.json` | `satFat` | None | 9.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `pb-033` | `7290112915351` | `protein_combined_frontend_v2.json` | `carbs` | None | 36.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-001` | `7290100659090` | `snacks_frontend_v5.json` | `satFat` | None | 0.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-001` | `7290100659090` | `snacks_frontend_v5.json` | `carbs` | None | 49.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-002` | `7290011498894` | `snacks_frontend_v5.json` | `satFat` | None | 1.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-002` | `7290011498894` | `snacks_frontend_v5.json` | `carbs` | None | 61.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-004` | `7290011498948` | `snacks_frontend_v5.json` | `satFat` | None | 5.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-004` | `7290011498948` | `snacks_frontend_v5.json` | `carbs` | None | 64.6 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-003` | `7290105436382` | `snacks_frontend_v5.json` | `satFat` | None | 2.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-003` | `7290105436382` | `snacks_frontend_v5.json` | `carbs` | None | 47.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-010` | `7290011498900` | `snacks_frontend_v5.json` | `satFat` | None | 6.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-010` | `7290011498900` | `snacks_frontend_v5.json` | `carbs` | None | 55.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-005` | `7290105431516` | `snacks_frontend_v5.json` | `satFat` | None | 2.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-005` | `7290105431516` | `snacks_frontend_v5.json` | `carbs` | None | 45.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-008` | `7290011498986` | `snacks_frontend_v5.json` | `satFat` | None | 7.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-008` | `7290011498986` | `snacks_frontend_v5.json` | `carbs` | None | 57.6 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-006` | `16000548404` | `snacks_frontend_v5.json` | `satFat` | None | 2.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-006` | `16000548404` | `snacks_frontend_v5.json` | `carbs` | None | 64.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-007` | `16000548503` | `snacks_frontend_v5.json` | `satFat` | None | 2.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-007` | `16000548503` | `snacks_frontend_v5.json` | `carbs` | None | 64.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-009` | `7290011498917` | `snacks_frontend_v5.json` | `satFat` | None | 16.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-009` | `7290011498917` | `snacks_frontend_v5.json` | `carbs` | None | 55.9 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-013` | `6009684861000` | `snacks_frontend_v5.json` | `satFat` | None | 6.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-013` | `6009684861000` | `snacks_frontend_v5.json` | `carbs` | None | 69.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-011` | `16000423534` | `snacks_frontend_v5.json` | `satFat` | None | 3.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-011` | `16000423534` | `snacks_frontend_v5.json` | `carbs` | None | 61.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-012` | `7290107971522` | `snacks_frontend_v5.json` | `satFat` | None | 6.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-012` | `7290107971522` | `snacks_frontend_v5.json` | `carbs` | None | 43.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-014` | `8423207208703` | `snacks_frontend_v5.json` | `satFat` | None | 14.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-014` | `8423207208703` | `snacks_frontend_v5.json` | `carbs` | None | 60.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-015` | `8410076610508` | `snacks_frontend_v5.json` | `satFat` | None | 8.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-015` | `8410076610508` | `snacks_frontend_v5.json` | `carbs` | None | 50.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-017` | `8410076610492` | `snacks_frontend_v5.json` | `satFat` | None | 7.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-017` | `8410076610492` | `snacks_frontend_v5.json` | `carbs` | None | 47.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-016` | `8423207208680` | `snacks_frontend_v5.json` | `satFat` | None | 14.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-016` | `8423207208680` | `snacks_frontend_v5.json` | `carbs` | None | 60.0 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-018` | `7290019297208` | `snacks_frontend_v5.json` | `satFat` | None | 6.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-018` | `7290019297208` | `snacks_frontend_v5.json` | `carbs` | None | 69.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-019` | `4011800633516` | `snacks_frontend_v5.json` | `satFat` | None | 11.7 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-019` | `4011800633516` | `snacks_frontend_v5.json` | `carbs` | None | 65.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-020` | `4011800628512` | `snacks_frontend_v5.json` | `satFat` | None | 10.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-020` | `4011800628512` | `snacks_frontend_v5.json` | `carbs` | None | 65.8 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-021` | `4011800632519` | `snacks_frontend_v5.json` | `satFat` | None | 18.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `snk-021` | `4011800632519` | `snacks_frontend_v5.json` | `carbs` | None | 57.2 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_yogurt_7290112336712` | `7290112336712` | `yogurt_spoonable_frontend_v1.json` | `carbs` | None | 3.3 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_yogurt_7290110565527` | `7290110565527` | `yogurt_spoonable_frontend_v1.json` | `carbs` | None | 3.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_yogurt_7290114314596` | `7290114314596` | `yogurt_spoonable_frontend_v1.json` | `satFat` | None | 1.4 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_yogurt_7290114314596` | `7290114314596` | `yogurt_spoonable_frontend_v1.json` | `carbs` | None | 7.5 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |
| `bsip1_yogurt_7290119377411` | `7290119377411` | `yogurt_spoonable_frontend_v1.json` | `carbs` | None | 4.1 | `02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121703.json` |

This audit authorizes no correction. Any score-movement implications are tripwire-1 owner decisions.

---

# ORCHESTRATOR ADJUDICATION (2026-07-11, appended after independent verification — read this FIRST)

The scan's mechanics are correct, but 25 of its 39 MATERIAL rows are REPLAY-SIDE ARTIFACTS, not
published-data damage. Do NOT "correct" published values from this table without reading below.

1. **24 brined-cheeses sodium rows + snk-018: FALSE DAMAGE — published values are CORRECT.**
   Independently replayed by the orchestrator: bc-036's raw row is `{value: '1,628', unit: 'מג'}` —
   the label says 1,628 mg and the published 1628 is right. The REPLAY reads 1.628 because
   `_to_float` at 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py:555 does `.replace(",", ".")`
   (assumes decimal comma), so a THOUSANDS comma under-reads ×1000. All 24 brined rows are this bug.
   snk-018: raw row `{value: '0.2', unit: 'מג'}` — the unit token is implausible (0.2 mg sodium in a
   snack bar); published 200 mg (=0.2 g) is the plausible reading; classify EVIDENCE_AMBIGUOUS.
   → The genuine bug these rows expose is in the EVIDENCE parser, registered as a follow-up task
   (comma-thousands + unreliable small-value unit token). It affects Shelf Watch comparisons and any
   future rebuild that replays sodium; it does NOT affect what the site currently displays.

2. **15 cereals fat rows: REAL, CONFIRMED damage** (consistent with TASK-591; two rows independently
   re-replayed by the orchestrator). This is the fix scope.

3. **FIELD_GAP appendix (~95 rows: cookies-coffee carbs=None, ricecakes satFat/carbs=None):
   completeness gaps, not wrongness** — evidence exists for fields the page doesn't populate.
   Candidate backlog item, separate severity class.

4. **Coverage honesty: 398/757 products have NO in-repo raw panel** (all of bread, cheese,
   chocolate, juices, milk, yogurt-drinks + most yogurt). For those shelves this scan can prove
   nothing either way; "no damage found" ≠ "verified clean".

**Adjudicated damage total: 15 products, all on the cereals shelf.**
