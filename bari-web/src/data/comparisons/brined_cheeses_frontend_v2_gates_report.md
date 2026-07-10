# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
**Generated:** 2026-07-10T08:45:03Z  |  **Elapsed:** 0.3s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [PASS] G2 COVERAGE | PASS |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
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

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=7290019635826: JSON score=83.3 vs trace score=85.4 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=554457: JSON score=82.7 vs trace score=84.8 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=554532: JSON score=82.7 vs trace score=84.8 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290102397334: JSON score=81.5 vs trace score=83.6 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290108509106: JSON score=78.6 vs trace score=80.5 (diff=1.900 > tolerance=0.05)
  FAIL: barcode=7290011499129: JSON score=78.0 vs trace score=80.1 (rounded trace=80, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290019790402: JSON score=74.3 vs trace score=76.4 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290017065663: JSON score=73.5 vs trace score=75.6 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290114314015: JSON score=70.3 vs trace score=72.4 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290019635222: JSON score=67.0 vs trace score=69.1 (rounded trace=69, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290017065236: JSON score=66.3 vs trace score=68.4 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=7290108509755: JSON score=64.6 vs trace score=66.7 (diff=2.100 > tolerance=0.05)
  FAIL: barcode=3075805: JSON score=62.5 vs trace score=64.7 (diff=2.200 > tolerance=0.05)
  FAIL: barcode=7290102393718: JSON score=62.5 vs trace score=64.6 (diff=2.100 > tolerance=0.05)

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
