# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`
**Generated:** 2026-07-01T19:23:12Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [PASS] G2 COVERAGE | PASS |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[4].expansion: missing required field 'comparisonContext'
  FAIL: #.products[4].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[5].expansion: missing required field 'comparisonContext'
  FAIL: #.products[5].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[6].expansion: missing required field 'comparisonContext'
  FAIL: #.products[6].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[7].expansion: missing required field 'comparisonContext'
  FAIL: #.products[7].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[8].expansion: missing required field 'comparisonContext'
  FAIL: #.products[8].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: ... and 58 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 36/36 non-null
  INFO: name: 36/36 non-null
  INFO: score: 36/36 non-null
  INFO: grade: 36/36 non-null
  INFO: insightLine: 36/36 non-null
  INFO: expansion: 36/36
  INFO: expansion.ingredients: 36/36
  INFO: expansion.nutrition.energyKcal: 36/36
  INFO: expansion.nutrition.protein: 36/36
  INFO: expansion.nutrition.sugar: 33/36
  INFO: expansion.nutrition.fat: 36/36
  INFO: expansion.nutrition.fiber: 3/36
  INFO: expansion.nutrition.sodium: 36/36
  INFO: expansion.confidenceLabel: 36/36
  INFO: Corpus barcodes with image in BSIP1: 48/48
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 36
  INFO: Scored products (trace dirs): 48
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 2107071 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 2385455 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 2511229 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 2511236 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 2511243 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4861056 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4861070 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5992872 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114310550 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073644996 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073730330 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8606370 not in frontend and not explained in _meta exclusions

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
