# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`
**Generated:** 2026-07-03T14:59:42Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.limitingFactors: expected type array, got NoneType
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[4].expansion: missing required field 'comparisonContext'
  FAIL: #.products[5].expansion: missing required field 'comparisonContext'
  FAIL: #.products[6].expansion: missing required field 'comparisonContext'
  FAIL: #.products[7].expansion: missing required field 'comparisonContext'
  FAIL: #.products[8].expansion: missing required field 'comparisonContext'
  FAIL: #.products[9].expansion: missing required field 'comparisonContext'
  FAIL: #.products[10].expansion: missing required field 'comparisonContext'
  FAIL: #.products[11].expansion: missing required field 'comparisonContext'
  FAIL: #.products[12].expansion: missing required field 'comparisonContext'
  FAIL: #.products[13].expansion: missing required field 'comparisonContext'
  FAIL: #.products[14].expansion: missing required field 'comparisonContext'
  FAIL: #.products[15].expansion: missing required field 'comparisonContext'
  FAIL: #.products[16].expansion: missing required field 'comparisonContext'
  FAIL: ... and 22 more errors

### [WARN] G2 COVERAGE
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
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 36
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=554457: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=554532: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108509106: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635826: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073641940: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4861360: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102397334: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499303: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2133162: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2133889: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073641964: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499129: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499327: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499358: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499105: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019790402: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=48413: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017065663: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108509755: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2107798: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073641957: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073641902: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499051: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019790808: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3075805: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393718: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073641919: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019790112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114314015: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635222: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017065236: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499365: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=369617: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114312707: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114312486: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=36 baseline=36
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=344  baseline=344  delta=+0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               36          36          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          344         344          +0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
