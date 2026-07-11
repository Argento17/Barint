# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/cheese_frontend_v4.json`
**Generated:** 2026-07-11T13:38:01Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 47/47 non-null
  INFO: name: 47/47 non-null
  INFO: score: 47/47 non-null
  INFO: grade: 47/47 non-null
  INFO: insightLine: 47/47 non-null
  INFO: expansion: 47/47
  INFO: expansion.ingredients: 47/47
  INFO: expansion.nutrition.energyKcal: 47/47
  INFO: expansion.nutrition.protein: 47/47
  INFO: expansion.nutrition.sugar: 28/47
  INFO: expansion.nutrition.fat: 47/47
  INFO: expansion.nutrition.fiber: 2/47
  INFO: expansion.nutrition.sodium: 47/47
  INFO: expansion.confidenceLabel: 47/47
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 47
  INFO: Scored products (trace dirs): 59
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 4127800 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4127817 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4127862 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 47942 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 48185 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 554969 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 554976 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 554983 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5992889 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014217492 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290108506624 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073453123 not in frontend and not explained in _meta exclusions

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=6040619: JSON score=81.2 vs trace score=81.3 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=7290108502541: JSON score=47.6 vs trace score=47.7 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=7622201139278: JSON score=45.5 vs trace score=45.6 (diff=0.100 > tolerance=0.05)

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=7290019635581 field=rowVerdict: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
