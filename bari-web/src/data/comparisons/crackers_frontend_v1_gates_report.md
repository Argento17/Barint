# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/crackers_frontend_v1.json`
**Generated:** 2026-07-01T19:47:29Z  |  **Elapsed:** 0.1s

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
  INFO: imageUrl: 19/19 non-null
  INFO: name: 19/19 non-null
  INFO: score: 19/19 non-null
  INFO: grade: 19/19 non-null
  INFO: insightLine: 19/19 non-null
  INFO: expansion: 19/19
  INFO: expansion.ingredients: 19/19
  INFO: expansion.nutrition.energyKcal: 19/19
  INFO: expansion.nutrition.protein: 19/19
  INFO: expansion.nutrition.sugar: 2/19
  INFO: expansion.nutrition.fat: 19/19
  INFO: expansion.nutrition.fiber: 17/19
  INFO: expansion.nutrition.sodium: 19/19
  INFO: expansion.confidenceLabel: 19/19
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 19/19 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 19/19 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 190/190 authored (0 PENDING)
  INFO: v3 bestUseCases: 19/19 authored (0 PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 19
  INFO: Scored products (trace dirs): 20
  INFO: Declared exclusions in _meta: 1
  INFO:   missing barcode 7290112968807: excluded — insufficient_data: unrecoverable per-serving/per-100g nutrition corruption, discard-rule. Full nutrition block (kcal/protein/carbs/fiber/sodium) was ~1/4.6 of near-identical sibling 'פיטנס' products with no clean unit/parse scaling factor -> nulled at BSIP1 source (TASK-433 FIX2b, missing-data-discard rule) -> engine returns insufficient_data/neutral score -> a gradeless row does not belong on a comparison page. Same rule as the existing BSIP1-stage discard of 5317200 (total data blackout), applied one stage later because this product's corruption was found and nulled during the TASK-433 rework, not at initial scrape.

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
