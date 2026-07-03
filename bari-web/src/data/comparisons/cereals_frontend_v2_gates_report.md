# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/cereals_frontend_v2.json`
**Generated:** 2026-07-03T15:17:44Z  |  **Elapsed:** 0.1s

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
  FAIL: #.products[0].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[3]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[4].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[4].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[4].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[4].expansion.limitingFactors[3]: expected type string, got dict
  FAIL: #.products[5].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[5].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[5].expansion.limitingFactors[2]: expected type string, got dict
  FAIL: #.products[6].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: ... and 49 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 20/20 non-null
  INFO: name: 20/20 non-null
  INFO: score: 20/20 non-null
  INFO: grade: 20/20 non-null
  INFO: insightLine: 20/20 non-null
  INFO: expansion: 20/20
  INFO: expansion.ingredients: 20/20
  INFO: expansion.nutrition.energyKcal: 20/20
  INFO: expansion.nutrition.protein: 20/20
  INFO: expansion.nutrition.sugar: 19/20
  INFO: expansion.nutrition.fat: 20/20
  INFO: expansion.nutrition.fiber: 19/20
  INFO: expansion.nutrition.sodium: 20/20
  INFO: expansion.confidenceLabel: 20/20
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 20
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=5010029000061: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7297488098688: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7297488199590: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900020012814: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073642046: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72968: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900020036407: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107647731: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073705550: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017894911: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112495433: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073705567: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107647854: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017894928: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017894904: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073642022: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8445291638839: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073705574: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3387390525960: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7613030979647: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=20 baseline=20
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=690  baseline=693  delta=-2
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               20          20          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          690         693          -2
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
