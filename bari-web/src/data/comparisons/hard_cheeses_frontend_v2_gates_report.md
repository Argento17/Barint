# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json`
**Generated:** 2026-06-18T15:16:30Z  |  **Elapsed:** 0.0s

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

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
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
  FAIL: #.products[9].expansion: missing required field 'comparisonContext'
  FAIL: #.products[9].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: ... and 36 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 28/28 non-null
  INFO: name: 28/28 non-null
  INFO: score: 28/28 non-null
  INFO: grade: 28/28 non-null
  INFO: insightLine: 28/28 non-null
  INFO: expansion: 28/28
  INFO: expansion.ingredients: 28/28
  INFO: expansion.nutrition.energyKcal: 28/28
  INFO: expansion.nutrition.protein: 28/28
  INFO: expansion.nutrition.sugar: 2/28
  INFO: expansion.nutrition.fat: 28/28
  INFO: expansion.nutrition.fiber: 0/28
  INFO: expansion.nutrition.sodium: 28/28
  INFO: expansion.confidenceLabel: 28/28
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 28
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290110324872: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110323301: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931524: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122348: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004137311: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122195: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014760912: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108503999: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3073781199918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000057088: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000057118: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122270: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122683: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004125776: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014763395: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017065434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635192: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102394463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102394845: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102396672: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102397204: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108501346: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108502725: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110320850: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110320867: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117265888: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117265918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8711528211138: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
