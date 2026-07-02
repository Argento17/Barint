# Bari Page Generator — Gate Report

**Input:** `C:\bari\bari-web\src\data\comparisons\snacks_frontend_v3.json`
**Generated:** 2026-06-19T17:31:51Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [FAIL] G2 COVERAGE | FAIL |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0]: additional property '_internal_cluster' not allowed
  FAIL: #.products[0]: additional property 'rank' not allowed
  FAIL: #.products[0]: additional property 'categoryTotal' not allowed
  FAIL: #.products[1]: additional property '_internal_cluster' not allowed
  FAIL: #.products[1]: additional property 'rank' not allowed
  FAIL: #.products[1]: additional property 'categoryTotal' not allowed
  FAIL: #.products[2]: additional property '_internal_cluster' not allowed
  FAIL: #.products[2]: additional property 'rank' not allowed
  FAIL: #.products[2]: additional property 'categoryTotal' not allowed
  FAIL: #.products[3]: additional property '_internal_cluster' not allowed
  FAIL: #.products[3]: additional property 'rank' not allowed
  FAIL: #.products[3]: additional property 'categoryTotal' not allowed
  FAIL: #.products[4]: additional property '_internal_cluster' not allowed
  FAIL: #.products[4]: additional property 'rank' not allowed
  FAIL: #.products[4]: additional property 'categoryTotal' not allowed
  FAIL: #.products[5]: additional property '_internal_cluster' not allowed
  FAIL: #.products[5]: additional property 'rank' not allowed
  FAIL: #.products[5]: additional property 'categoryTotal' not allowed
  FAIL: #.products[6]: additional property '_internal_cluster' not allowed
  FAIL: #.products[6]: additional property 'rank' not allowed
  FAIL: ... and 34 more errors

### [FAIL] G2 COVERAGE
  INFO: imageUrl: 18/18 non-null
  INFO: name: 18/18 non-null
  INFO: score: 18/18 non-null
  INFO: grade: 18/18 non-null
  INFO: insightLine: 18/18 non-null
  INFO: expansion: 18/18
  INFO: expansion.ingredients: 18/18
  INFO: expansion.nutrition.energyKcal: 18/18
  INFO: expansion.nutrition.protein: 18/18
  INFO: expansion.nutrition.sugar: 18/18
  INFO: expansion.nutrition.fat: 18/18
  INFO: expansion.nutrition.fiber: 14/18
  INFO: expansion.nutrition.sodium: 16/18
  INFO: expansion.confidenceLabel: 18/18
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 0/18 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 0/18 authored (18 PENDING)
  FAIL: v3 consumerExplanation.whyRated: 18/18 products still PENDING_COPY
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 0/18 authored (18 PENDING)
  FAIL: v3 bestUseCases: 18/18 products still PENDING_COPY

### [WARN] G3 SCOPE
  INFO: Displayed products: 18
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290011498870: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207210287: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498894: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207206495: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498948: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000548404: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207210928: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610379: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900020039590: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610386: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076602251: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290111936784: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610508: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118427896: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290111937262: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014525306: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900020015174: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4011800633516: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
