# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v1.json`
**Generated:** 2026-06-13T18:14:46Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].score: expected type ['integer', 'null'], got float
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[0]: additional property 'novaGroup' not allowed
  FAIL: #.products[0]: additional property 'consumerTakeaway' not allowed
  FAIL: #.products[0]: additional property 'consumerExplanation' not allowed
  FAIL: #.products[0]: additional property 'bariInterpretation' not allowed
  FAIL: #.products[0]: additional property 'bestUseCases' not allowed
  FAIL: #.products[1].score: expected type ['integer', 'null'], got float
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[1]: additional property 'novaGroup' not allowed
  FAIL: #.products[1]: additional property 'consumerTakeaway' not allowed
  FAIL: #.products[1]: additional property 'consumerExplanation' not allowed
  FAIL: #.products[1]: additional property 'bariInterpretation' not allowed
  FAIL: #.products[1]: additional property 'bestUseCases' not allowed
  FAIL: #.products[2].score: expected type ['integer', 'null'], got float
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: ... and 501 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 61/61 non-null
  INFO: name: 61/61 non-null
  INFO: score: 61/61 non-null
  INFO: grade: 61/61 non-null
  INFO: insightLine: 61/61 non-null
  INFO: expansion: 61/61
  INFO: expansion.ingredients: 61/61
  INFO: expansion.nutrition.energyKcal: 61/61
  INFO: expansion.nutrition.protein: 61/61
  INFO: expansion.nutrition.sugar: 59/61
  INFO: expansion.nutrition.fat: 61/61
  INFO: expansion.nutrition.fiber: 44/61
  INFO: expansion.nutrition.sodium: 61/61
  INFO: expansion.confidenceLabel: 61/61
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [PASS] G3 SCOPE
  INFO: Displayed products: 61
  INFO: Scored products (trace dirs): 61
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=7290119043743 field=expansion.limitingFactors[0]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=960860015432 field=expansion.limitingFactors[0]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=311463 field=expansion.limitingFactors[0]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290013453501 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290011489625 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119041152 field=expansion.limitingFactors[0]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119041053 field=expansion.limitingFactors[0]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=2986065 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=2986058 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290013740694 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119043798 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290123330488 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119041350 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119043095 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119041206 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290119040803 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290106656727 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290109354996 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'
  FAIL: barcode=7290109354972 field=expansion.limitingFactors[1]: framework vocabulary leaked: 'NOVA'

### [SKIP] G7 PARITY
  SKIP: No baseline provided
