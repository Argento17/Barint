# Bari Page Generator — Gate Report

**Input:** `C:/Bari/_g6_milk.json`
**Generated:** 2026-06-25T06:06:19Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |
| [SKIP] G9 INVERSION-INVARIANT | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[0]: additional property 'filterTags' not allowed
  FAIL: #.products[0]: additional property 'milkProductType' not allowed
  FAIL: #.products[0]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[1]: additional property 'filterTags' not allowed
  FAIL: #.products[1]: additional property 'milkProductType' not allowed
  FAIL: #.products[1]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[2]: additional property 'filterTags' not allowed
  FAIL: #.products[2]: additional property 'milkProductType' not allowed
  FAIL: #.products[2]: additional property 'milkProductTypeLabel' not allowed
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: ... and 88 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 18/18 non-null
  INFO: name: 18/18 non-null
  INFO: score: 18/18 non-null
  INFO: grade: 18/18 non-null
  INFO: insightLine: 5/18 non-null
  INFO: expansion: 18/18
  INFO: expansion.ingredients: 18/18
  INFO: expansion.nutrition.energyKcal: 18/18
  INFO: expansion.nutrition.protein: 18/18
  INFO: expansion.nutrition.sugar: 9/18
  INFO: expansion.nutrition.fat: 0/18
  INFO: expansion.nutrition.fiber: 0/18
  INFO: expansion.nutrition.sodium: 16/18
  INFO: expansion.confidenceLabel: 18/18
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 18
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290000051352: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019790259: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102392094: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114313865: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116936116: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110324926: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107932134: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014760141: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7394376620904: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119385560: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7394376619939: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7394376621451: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5411188124689: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8000215204554: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110325619: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8000215204219: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5411188112709: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5411188300328: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
