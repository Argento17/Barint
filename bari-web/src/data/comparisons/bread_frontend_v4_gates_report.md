# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/bread_frontend_v4.json`
**Generated:** 2026-07-11T13:38:00Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [FAIL] G2 COVERAGE | FAIL |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [FAIL] G2 COVERAGE
  INFO: imageUrl: 23/23 non-null
  INFO: name: 23/23 non-null
  INFO: score: 23/23 non-null
  INFO: grade: 23/23 non-null
  INFO: insightLine: 23/23 non-null
  INFO: expansion: 23/23
  INFO: expansion.ingredients: 23/23
  INFO: expansion.nutrition.energyKcal: 23/23
  INFO: expansion.nutrition.protein: 23/23
  INFO: expansion.nutrition.sugar: 21/23
  INFO: expansion.nutrition.fat: 23/23
  INFO: expansion.nutrition.fiber: 22/23
  INFO: expansion.nutrition.sodium: 23/23
  INFO: expansion.confidenceLabel: 23/23
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  FAIL: insightLine: 6/23 products still PENDING_COPY (page authored but incomplete)
  FAIL: rowVerdict: 6/23 products still PENDING_COPY (page authored but incomplete)
  FAIL: 6/23 products render NO verdict — both insightLine and rowVerdict are unauthored (PENDING/null/empty/missing) after the copy stage ran — barcodes: 3268429, 2079927, 2079033, 2079996, 7290014321168, 4685027
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 23
  INFO: Scored products (trace dirs): 31
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 2026 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073134442 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073134459 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073641568 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 74252 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8434165658523 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 96086000577 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 96086000966 not in frontend and not explained in _meta exclusions

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=7290016967074: JSON score=66.0 vs trace score=69.0 (rounded trace=69, diff=3.000 > tolerance=0.05)

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
