# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v2.json`
**Generated:** 2026-07-01T15:26:09Z  |  **Elapsed:** 0.9s

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
  FAIL: #.products[0].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[3]: expected type string, got dict
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[2].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[3].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[3]: expected type string, got dict
  FAIL: #.products[3]: additional property 'brand' not allowed
  FAIL: #.products[4].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[4].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: ... and 69 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 20/20 non-null
  INFO: name: 20/20 non-null
  INFO: score: 20/20 non-null
  INFO: grade: 20/20 non-null
  INFO: insightLine: 20/20 non-null
  INFO: expansion: 20/20
  INFO: expansion.ingredients: 20/20
  INFO: expansion.nutrition.energyKcal: 20/20
  INFO: expansion.nutrition.protein: 20/20
  INFO: expansion.nutrition.sugar: 19/20
  INFO: expansion.nutrition.fat: 20/20
  INFO: expansion.nutrition.fiber: 19/20
  INFO: expansion.nutrition.sodium: 20/20
  INFO: expansion.confidenceLabel: 20/20
  INFO: Corpus barcodes with image in BSIP1: 63/63
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 20
  INFO: Scored products (trace dirs): 63
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 1164266 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 1164273 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 1343845 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5018357006731 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5018357006755 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 6582751 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131050 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131371 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131388 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131395 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131968 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131975 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011668587 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013433091 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013433107 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013433244 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013433336 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014471412 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014471429 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014471436 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014471443 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290016883176 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290016883183 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017325910 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017962023 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017962047 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106771161 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106771314 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106771369 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106773714 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112494351 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112495228 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112497994 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112498007 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116530482 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116534619 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116535371 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290118420811 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7613035622623 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7613035635845 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7613037012095 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8445290964595 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 884912126115 not in frontend and not explained in _meta exclusions

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
