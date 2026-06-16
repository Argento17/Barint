# Bari Page Generator — Gate Report

**Input:** `_e2e_out/page/e2e_page_throwaway_final.json`
**Generated:** 2026-06-13T04:29:11Z  |  **Elapsed:** 0.0s

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

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 3/3 non-null
  INFO: name: 3/3 non-null
  INFO: score: 3/3 non-null
  INFO: grade: 3/3 non-null
  INFO: insightLine: 3/3 non-null
  INFO: expansion: 3/3
  INFO: expansion.ingredients: 3/3
  INFO: expansion.nutrition.energyKcal: 3/3
  INFO: expansion.nutrition.protein: 3/3
  INFO: expansion.nutrition.sugar: 3/3
  INFO: expansion.nutrition.fat: 3/3
  INFO: expansion.nutrition.fiber: 3/3
  INFO: expansion.nutrition.sodium: 3/3
  INFO: expansion.confidenceLabel: 3/3
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: v3 consumerTakeaway: 3/3 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 3/3 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 30/30 authored (0 PENDING)
  INFO: v3 bestUseCases: 3/3 authored (0 PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 3
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=9990000000003: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9990000000001: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9990000000002: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided
