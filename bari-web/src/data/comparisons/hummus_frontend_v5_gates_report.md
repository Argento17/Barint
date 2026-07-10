# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\hummus_frontend_v5.json`
**Generated:** 2026-07-10T08:45:09Z  |  **Elapsed:** 0.4s

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
  FAIL: #.products[0].d3_processing_signal: expected type null, got dict
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].d3_processing_signal: expected type null, got dict
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].d3_processing_signal: expected type null, got dict
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[3].d3_processing_signal: expected type null, got dict
  FAIL: #.products[4].expansion: missing required field 'comparisonContext'
  FAIL: #.products[4].d3_processing_signal: expected type null, got dict
  FAIL: #.products[5].expansion: missing required field 'comparisonContext'
  FAIL: #.products[5].d3_processing_signal: expected type null, got dict
  FAIL: #.products[6].expansion: missing required field 'comparisonContext'
  FAIL: #.products[6].d3_processing_signal: expected type null, got dict
  FAIL: #.products[7].expansion: missing required field 'comparisonContext'
  FAIL: #.products[7].d3_processing_signal: expected type null, got dict
  FAIL: #.products[8].expansion: missing required field 'comparisonContext'
  FAIL: #.products[8].d3_processing_signal: expected type null, got dict
  FAIL: #.products[9].expansion: missing required field 'comparisonContext'
  FAIL: #.products[9].d3_processing_signal: expected type null, got dict
  FAIL: ... and 94 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 57/57 non-null
  INFO: name: 57/57 non-null
  INFO: score: 57/57 non-null
  INFO: grade: 57/57 non-null
  INFO: insightLine: 57/57 non-null
  INFO: expansion: 57/57
  INFO: expansion.ingredients: 57/57
  INFO: expansion.nutrition.energyKcal: 57/57
  INFO: expansion.nutrition.protein: 57/57
  INFO: expansion.nutrition.sugar: 55/57
  INFO: expansion.nutrition.fat: 57/57
  INFO: expansion.nutrition.fiber: 14/57
  INFO: expansion.nutrition.sodium: 57/57
  INFO: expansion.confidenceLabel: 57/57
  INFO: Corpus barcodes with image in BSIP1: 69/69
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 57
  INFO: Scored products (trace dirs): 69
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 1990261 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 208428 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 3643714 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 3643820 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290018359686 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073005889 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073006015 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073705505 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073733317 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073733324 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073733331 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073733348 not in frontend and not explained in _meta exclusions

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
