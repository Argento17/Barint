# Bari Page Generator — Gate Report

**Input:** `C:/Bari/_g6_bread.json`
**Generated:** 2026-06-25T06:06:16Z  |  **Elapsed:** 0.1s

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
| [SKIP] G9 INVERSION-INVARIANT | SKIP |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 29/29 non-null
  INFO: name: 29/29 non-null
  INFO: score: 29/29 non-null
  INFO: grade: 29/29 non-null
  INFO: insightLine: 29/29 non-null
  INFO: expansion: 29/29
  INFO: expansion.ingredients: 29/29
  INFO: expansion.nutrition.energyKcal: 29/29
  INFO: expansion.nutrition.protein: 29/29
  INFO: expansion.nutrition.sugar: 1/29
  INFO: expansion.nutrition.fat: 29/29
  INFO: expansion.nutrition.fiber: 27/29
  INFO: expansion.nutrition.sodium: 29/29
  INFO: expansion.confidenceLabel: 29/29
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 29/29 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 29/29 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 29/29 authored (0 PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 29
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290016245325: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268429: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481203: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481197: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=574370: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3054183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079033: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500316: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000966: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079927: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=497044: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000577: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018540329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9398281: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134459: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079477: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079217: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014321168: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451484: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451507: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500460: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4685027: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8434165658523: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016967074: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1902325: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74252: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
