# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/bread_frontend_v3.json`
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
  FAIL: #.products[0]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[1]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[2]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[3]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[4]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[5]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[6]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[7]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[8]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[9]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[10]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[11]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[12]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[13]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[14]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[15]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[16]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[17]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[18]: additional property '_hash_no_rank' not allowed
  FAIL: #.products[19]: additional property '_hash_no_rank' not allowed
  FAIL: ... and 9 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 29/29 non-null
  INFO: name: 29/29 non-null
  INFO: score: 29/29 non-null
  INFO: grade: 29/29 non-null
  INFO: insightLine: 29/29 non-null
  INFO: expansion: 29/29
  INFO: expansion.ingredients: 29/29
  INFO: expansion.nutrition.energyKcal: 29/29
  INFO: expansion.nutrition.protein: 29/29
  INFO: expansion.nutrition.sugar: 1/29
  INFO: expansion.nutrition.fat: 29/29
  INFO: expansion.nutrition.fiber: 27/29
  INFO: expansion.nutrition.sodium: 29/29
  INFO: expansion.confidenceLabel: 29/29
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 29
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290016245325: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268429: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481203: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481197: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=574370: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3054183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079033: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079927: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=497044: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500316: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000966: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=96086000577: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018540329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079477: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9398281: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134459: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073134442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079217: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014321168: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8434165658523: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451484: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451507: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500460: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4685027: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016967074: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1902325: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=29 baseline=29
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=400  baseline=400  delta=+0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               29          29          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          400         400          +0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
