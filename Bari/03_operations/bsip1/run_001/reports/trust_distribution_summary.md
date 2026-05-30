# BSIP1 Trust Distribution Summary

**Run date:** 2026-05-17 05:22 UTC  
**Products evaluated:** 53  
**Observations — total:** 66  
**Observations — trust-scored:** 63  
**Observations — excluded from scoring:** 3  
**Exclusion reason:** No-barcode observations are not canonicalized into products; they are queued in fuzzy_candidate_queue.json for manual matching and do not contribute to observation trust scoring.

---

## Canonical Trust Distribution

| Trust Level | Count | % |
|-------------|-------|---|
| **high** | 2 | 3.8% |
| **medium** | 46 | 86.8% |
| **low** | 5 | 9.4% |

Average canonical trust score: **0.765**  
Range: 0.03 – 1.0

---

## High Trust Products

2 products with canonical_trust_level = high

- `bsip1_4011800567613` — score 1.0
- `bsip1_5900020022325` — score 1.0

---

## Medium Trust Products

46 products with canonical_trust_level = medium

- `bsip1_7290107646154` — score 0.9 (nutrition_consistency_issue, high_conflict_count)
- `bsip1_7290118427896` — score 0.9 (nutrition_consistency_issue, high_conflict_count)
- `bsip1_8423207209885` — score 0.9 (nutrition_consistency_issue, high_conflict_count)
- `bsip1_4011800528416` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_4011800633516` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020015174` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020018908` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020020710` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020034021` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020039590` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_5900020039620` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290011498894` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290107646147` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290107646826` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290107947466` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290107947480` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290110563851` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290111936784` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_7290111937262` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8410076602251` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8410076610379` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8410076610508` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8423207207362` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8423207210287` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_8423207210928` — score 0.87 (inferred_barcode_only, single_source_only)
- `bsip1_4011800629519` — score 0.85 (inferred_barcode_only, single_source_only)
- `bsip1_5900020029669` — score 0.85 (inferred_barcode_only, single_source_only)
- `bsip1_7290118427858` — score 0.85 (inferred_barcode_only, single_source_only)
- `bsip1_8423207206501` — score 0.85 (inferred_barcode_only, single_source_only)
- `bsip1_16000423534` — score 0.81 (retailer_internal_id_barcode, single_source_only)
- `bsip1_16000548404` — score 0.81 (retailer_internal_id_barcode, single_source_only)
- `bsip1_16000548503` — score 0.81 (retailer_internal_id_barcode, single_source_only)
- `bsip1_7290011498870` — score 0.78 (inferred_barcode_only, single_source_only)
- `bsip1_4011800000349` — score 0.76 (malformed_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_8410076610386` — score 0.76 (malformed_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_8410076610492` — score 0.76 (malformed_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_8423207206488` — score 0.72 (nutrition_consistency_issue, corrupted_ingredient_text, high_conflict_count)
- `bsip1_4011800632519` — score 0.68
- `bsip1_8423207206495` — score 0.68
- `bsip1_7290014525290` — score 0.65 (corrupted_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_7290014525306` — score 0.65 (corrupted_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_8423207208260` — score 0.65 (corrupted_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_8423207208680` — score 0.65 (corrupted_ingredient_text, inferred_barcode_only, single_source_only)
- `bsip1_4011800628512` — score 0.61 (malformed_ingredient_text)
- `bsip1_4011800630515` — score 0.61 (malformed_ingredient_text)
- `bsip1_7290011498948` — score 0.61 (nutrition_consistency_issue, nutrition_suspicious, inferred_barcode_only, …)

---

## Low Trust Products

5 products with canonical_trust_level = low

- `bsip1_8423207208703` — score 0.03 (nutrition_data_absent, missing_ingredient_text, inferred_barcode_only, …)
- `bsip1_7290018333952` — score 0.27 (nutrition_data_absent, missing_ingredient_text, inferred_barcode_only, …)
- `bsip1_7290019545545` — score 0.27 (nutrition_data_absent, missing_ingredient_text, inferred_barcode_only, …)
- `bsip1_7290118427872` — score 0.27 (nutrition_data_absent, missing_ingredient_text, inferred_barcode_only, …)
- `bsip1_16000548909` — score 0.46 (nutrition_data_absent, retailer_internal_id_barcode, single_source_only)

---

## Top Causes of Trust Degradation

Canonical risk flag frequency across all products:

| Risk Flag | Products Affected |
|-----------|-------------------|
| `single_source_only` | 43 |
| `inferred_barcode_only` | 39 |
| `nutrition_data_absent` | 5 |
| `malformed_ingredient_text` | 5 |
| `nutrition_consistency_issue` | 5 |
| `corrupted_ingredient_text` | 5 |
| `retailer_internal_id_barcode` | 4 |
| `missing_ingredient_text` | 4 |
| `high_conflict_count` | 4 |
| `nutrition_suspicious` | 1 |

---

## Observation Quality Signal Frequency

Top positive and negative signals across all observations:

| Signal | Observations |
|--------|--------------|
| `has_price_data` | 63 |
| `full_product_page` | 58 |
| `has_allergen_data` | 54 |
| `full_nutrition_explicit_per_100g` | 52 |
| `inferred_barcode_1213` | 49 |
| `has_product_image` | 48 |
| `clean_ingredient_text` | 44 |
| `product_page_barcode_1213` | 10 |
| `energy_unit_ambiguous` | 10 |
| `absent_nutrition` | 9 |
| `absent_ingredient_text` | 8 |
| `malformed_ingredient_text` | 6 |
| `shelf_card_only` | 5 |
| `corrupted_ingredient_text` | 5 |
| `retailer_internal_barcode` | 4 |
| `partial_nutrition_explicit_per_100g` | 2 |