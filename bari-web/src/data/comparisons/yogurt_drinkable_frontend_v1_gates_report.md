# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/yogurt_drinkable_frontend_v1.json`
**Generated:** 2026-07-08T12:24:16Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 20/20 non-null
  INFO: name: 20/20 non-null
  INFO: score: 20/20 non-null
  INFO: grade: 20/20 non-null
  INFO: insightLine: 20/20 non-null
  INFO: expansion: 20/20
  INFO: expansion.ingredients: 20/20
  INFO: expansion.nutrition.energyKcal: 20/20
  INFO: expansion.nutrition.protein: 20/20
  INFO: expansion.nutrition.sugar: 20/20
  INFO: expansion.nutrition.fat: 20/20
  INFO: expansion.nutrition.fiber: 8/20
  INFO: expansion.nutrition.sodium: 20/20
  INFO: expansion.confidenceLabel: 20/20
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 20/20 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 20/20 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 200/200 authored (0 PENDING)
  INFO: v3 bestUseCases: 20/20 authored (0 PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 20
  INFO: Scored products (trace dirs): 23
  INFO: Declared exclusions in _meta: 3
  INFO:   missing barcode 6664655: excluded — TASK-515 dedup-drop (unchanged from HIGH-2 ruling): אקטימל לבן מארז -- byte-identical duplicate SKU of barcode 7290119380923 (KEPT, canonical EAN-13).
  INFO:   missing barcode 7290116932774: excluded — TASK-515 owner-directed dump (superseding the prior HIGH-1 discard ruling): גו בננה-קרמל -- fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac), not just this retailer panel. missing_data_discard_rule.
  INFO:   missing barcode 7290116934228: excluded — TASK-515 owner-directed dump (superseding the prior HIGH-1 discard ruling): משקה יוגורט גו מלון תות -- sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac), not just this retailer panel. missing_data_discard_rule.

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
