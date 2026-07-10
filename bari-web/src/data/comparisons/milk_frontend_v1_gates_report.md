# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\milk_frontend_v1.json`
**Generated:** 2026-07-10T08:45:10Z  |  **Elapsed:** 0.2s

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
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[0]: additional property 'filterTags' not allowed
  FAIL: #.products[0]: additional property 'milkProductType' not allowed
  FAIL: #.products[0]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[1]: additional property 'filterTags' not allowed
  FAIL: #.products[1]: additional property 'milkProductType' not allowed
  FAIL: #.products[1]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[2]: additional property 'filterTags' not allowed
  FAIL: #.products[2]: additional property 'milkProductType' not allowed
  FAIL: #.products[2]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[3]: additional property 'filterTags' not allowed
  FAIL: #.products[3]: additional property 'milkProductType' not allowed
  FAIL: #.products[3]: additional property 'milkProductTypeLabel' not allowed
  FAIL: ... and 70 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 18/18 non-null
  INFO: name: 18/18 non-null
  INFO: score: 18/18 non-null
  INFO: grade: 18/18 non-null
  INFO: insightLine: 18/18 non-null
  INFO: expansion: 18/18
  INFO: expansion.ingredients: 18/18
  INFO: expansion.nutrition.energyKcal: 18/18
  INFO: expansion.nutrition.protein: 18/18
  INFO: expansion.nutrition.sugar: 9/18
  INFO: expansion.nutrition.fat: 0/18
  INFO: expansion.nutrition.fiber: 0/18
  INFO: expansion.nutrition.sodium: 16/18
  INFO: expansion.confidenceLabel: 18/18
  INFO: Corpus barcodes with image in BSIP1: 0/20
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 18
  INFO: Scored products (trace dirs): 20
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 7290110324773 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114313285 not in frontend and not explained in _meta exclusions

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
