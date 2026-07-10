# Bari Page Generator — Gate Report

**Input:** `C:\Bari\tasks\returns\TASK-461_juices_copy_overhaul.json`
**Generated:** 2026-07-03T01:18:59Z  |  **Elapsed:** 0.1s

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
  FAIL: #.products[0]: additional property 'volumeMl' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1]: additional property 'volumeMl' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2]: additional property 'volumeMl' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[3]: additional property 'volumeMl' not allowed
  FAIL: #.products[4].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[4]: additional property 'volumeMl' not allowed
  FAIL: #.products[5].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[5]: additional property 'volumeMl' not allowed
  FAIL: #.products[6].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[6]: additional property 'volumeMl' not allowed
  FAIL: #.products[7].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[7]: additional property 'volumeMl' not allowed
  FAIL: #.products[8].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[8]: additional property 'volumeMl' not allowed
  FAIL: #.products[8]: additional property '_d4_copy_flag' not allowed
  FAIL: #.products[9].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: ... and 19 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 17/17 non-null
  INFO: name: 17/17 non-null
  INFO: score: 17/17 non-null
  INFO: grade: 17/17 non-null
  INFO: insightLine: 17/17 non-null
  INFO: expansion: 17/17
  INFO: expansion.ingredients: 17/17
  INFO: expansion.nutrition.energyKcal: 17/17
  INFO: expansion.nutrition.protein: 16/17
  INFO: expansion.nutrition.sugar: 15/17
  INFO: expansion.nutrition.fat: 4/17
  INFO: expansion.nutrition.fiber: 0/17
  INFO: expansion.nutrition.sodium: 5/17
  INFO: expansion.confidenceLabel: 17/17
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 17
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290004030100: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013608260: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000525969: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013153395: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110114886: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290003009640: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290008690713: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290006822192: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019056720: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000136523: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290001247891: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290001247723: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290001247730: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019056355: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019056591: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019056737: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013153418: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=17 baseline=17
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=650  baseline=687  delta=-37
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               17          17          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          650         687         -37
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
