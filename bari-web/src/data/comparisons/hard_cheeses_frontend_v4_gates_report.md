# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json`
**Generated:** 2026-07-03T15:17:45Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 31/31 non-null
  INFO: name: 31/31 non-null
  INFO: score: 31/31 non-null
  INFO: grade: 31/31 non-null
  INFO: insightLine: 31/31 non-null
  INFO: expansion: 31/31
  INFO: expansion.ingredients: 25/31
  INFO: expansion.nutrition.energyKcal: 31/31
  INFO: expansion.nutrition.protein: 31/31
  INFO: expansion.nutrition.sugar: 1/31
  INFO: expansion.nutrition.fat: 31/31
  INFO: expansion.nutrition.fiber: 0/31
  INFO: expansion.nutrition.sodium: 31/31
  INFO: expansion.confidenceLabel: 31/31
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='v4', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 31
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290110324872: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122348: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4137311: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=52311: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014760448: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117265888: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073731856: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5384356: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9150162: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931524: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3073781199918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5079658: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5079665: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5079672: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290004122195: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014455245: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017065434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635192: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020467393: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114311601: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114312813: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8606974: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8711528211138: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014760912: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4122270: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110320850: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073735151: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8606608: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=53219: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110323301: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453482: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=31 baseline=31
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=588  baseline=589  delta=-0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               31          31          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          588         589          -0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
