# Bari Page Generator — Gate Report

**Input:** `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_drinkable_FINAL_v3.json`
**Generated:** 2026-07-08T19:52:18Z  |  **Elapsed:** 0.1s

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

### [WARN] G3 SCOPE
  INFO: Displayed products: 20
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290102393299: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4068035: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115676051: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020711090: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020711007: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110573737: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110552244: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107937542: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105364678: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105965738: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635567: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110325114: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119380923: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107938396: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110325121: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102031276: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55336: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55343: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=58030: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55329: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
