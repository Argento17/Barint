# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/crackers_frontend_v1.json`
**Generated:** 2026-07-03T08:34:49Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [FAIL] G2 COVERAGE | FAIL |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [FAIL] G2 COVERAGE
  INFO: imageUrl: 19/19 non-null
  INFO: name: 19/19 non-null
  INFO: score: 19/19 non-null
  INFO: grade: 19/19 non-null
  INFO: insightLine: 19/19 non-null
  INFO: expansion: 19/19
  INFO: expansion.ingredients: 19/19
  INFO: expansion.nutrition.energyKcal: 19/19
  INFO: expansion.nutrition.protein: 19/19
  INFO: expansion.nutrition.sugar: 2/19
  INFO: expansion.nutrition.fat: 19/19
  INFO: expansion.nutrition.fiber: 17/19
  INFO: expansion.nutrition.sodium: 19/19
  INFO: expansion.confidenceLabel: 19/19
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  FAIL: insightLine: 1/19 products still PENDING_COPY (page authored but incomplete)
  FAIL: rowVerdict: 1/19 products still PENDING_COPY (page authored but incomplete)
  FAIL: 1/19 products render NO verdict — both insightLine and rowVerdict are unauthored (PENDING/null/empty/missing) after the copy stage ran — barcodes: 7290018790328
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 1/19 insightLines still PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 19
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=96086000966: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000577: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740823: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740809: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073659945: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134459: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112963918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073659952: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112968821: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115205176: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8434165658523: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073398875: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740083: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011489595: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74375: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018790328: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000396021202: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=19 baseline=19
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=1430  baseline=1615  delta=-185
  INFO: Per-barcode grade changes (1):
  INFO:   barcode=7290018790328 [קרקר מרובע מלוח]: C -> D
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               19          19          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                         1430        1615        -185
  INFO:   Grade changes                                1           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
