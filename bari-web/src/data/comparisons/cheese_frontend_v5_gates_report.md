# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/cheese_frontend_v5.json`
**Generated:** 2026-07-03T15:17:44Z  |  **Elapsed:** 0.1s

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
  INFO: imageUrl: 47/47 non-null
  INFO: name: 47/47 non-null
  INFO: score: 47/47 non-null
  INFO: grade: 47/47 non-null
  INFO: insightLine: 47/47 non-null
  INFO: expansion: 47/47
  INFO: expansion.ingredients: 47/47
  INFO: expansion.nutrition.energyKcal: 47/47
  INFO: expansion.nutrition.protein: 47/47
  INFO: expansion.nutrition.sugar: 28/47
  INFO: expansion.nutrition.fat: 47/47
  INFO: expansion.nutrition.fiber: 2/47
  INFO: expansion.nutrition.sodium: 47/47
  INFO: expansion.confidenceLabel: 47/47
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 47
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290014758681: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6040619: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127077: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=41445: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110321277: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=474502: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290010945481: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393268: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114311472: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114310918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116934280: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2868996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127336: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=41452: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2824183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2824640: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3523230065467: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=56272: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931241: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011194246: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3075850: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201798154: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116934365: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635369: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119375219: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635376: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6492852: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108504378: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014759084: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635116: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201521493: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108502541: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201139278: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014762831: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116935409: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116936604: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112342102: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129118: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129101: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116933078: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129156: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931982: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116932644: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635581: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499624: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635383: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=47 baseline=47
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=312  baseline=312  delta=-0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               47          47          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          312         312          -0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
