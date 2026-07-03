# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/crackers_frontend_v1.json`
**Generated:** 2026-07-03T09:45:07Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
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

### [WARN] G3 SCOPE
  INFO: Displayed products: 19
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=96086000966: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000577: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740823: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740809: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073659945: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134459: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112963918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073659952: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112968821: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115205176: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8434165658523: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073398875: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740083: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011489595: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74375: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018790328: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000396021202: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
