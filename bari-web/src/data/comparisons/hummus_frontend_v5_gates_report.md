# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/hummus_frontend_v5.json`
**Generated:** 2026-07-01T16:29:23Z  |  **Elapsed:** 0.1s

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

### [WARN] G2 COVERAGE
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
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 57
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7296073725404: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6666307: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725565: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725589: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6666444: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015858175: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110564360: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110579319: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110557478: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011800642: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725381: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3727667: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106576513: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5174551: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105964564: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2987963: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8645935: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119387434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725497: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725374: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106573642: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725367: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290010931330: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8644112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107958639: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290104721533: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=467320: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290104061431: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106576537: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290122780314: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106573598: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119373710: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290104061424: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115202434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=467153: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106573819: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119374892: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106573628: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290104061417: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112968685: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725398: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115207484: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290104061448: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115202687: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290111563492: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106577572: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3989096: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725510: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725633: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105366023: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073725640: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6724786: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119374885: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106520905: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073451969: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290010154265: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106577480: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=57 baseline=57
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=467  baseline=467  delta=+0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               57          57          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          467         467          +0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
