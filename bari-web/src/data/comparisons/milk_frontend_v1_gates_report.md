# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/milk_frontend_v1.json`
**Generated:** 2026-07-01T19:18:12Z  |  **Elapsed:** 0.1s

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

### [WARN] G2 COVERAGE
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

### [PASS] G7 PARITY
  INFO: Product count: current=18 baseline=18
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=820  baseline=820  delta=+0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               18          18          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          820         820          +0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
