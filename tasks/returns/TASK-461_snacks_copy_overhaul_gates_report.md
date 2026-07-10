# Bari Page Generator — Gate Report

**Input:** `C:\Bari\tasks\returns\TASK-461_snacks_copy_overhaul.json`
**Generated:** 2026-07-03T01:16:45Z  |  **Elapsed:** 0.1s

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
  FAIL: #.products[0]: additional property 'name_he' not allowed
  FAIL: #.products[0]: additional property 'image_url' not allowed
  FAIL: #.products[0]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[0]: additional property '_scoring_trace' not allowed
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1]: additional property 'name_he' not allowed
  FAIL: #.products[1]: additional property 'image_url' not allowed
  FAIL: #.products[1]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[1]: additional property '_scoring_trace' not allowed
  FAIL: #.products[2].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[2]: additional property 'name_he' not allowed
  FAIL: #.products[2]: additional property 'image_url' not allowed
  FAIL: #.products[2]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[2]: additional property '_scoring_trace' not allowed
  FAIL: #.products[3].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[3].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: ... and 135 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 21/21 non-null
  INFO: name: 21/21 non-null
  INFO: score: 21/21 non-null
  INFO: grade: 21/21 non-null
  INFO: insightLine: 21/21 non-null
  INFO: expansion: 21/21
  INFO: expansion.ingredients: 21/21
  INFO: expansion.nutrition.energyKcal: 21/21
  INFO: expansion.nutrition.protein: 21/21
  INFO: expansion.nutrition.sugar: 21/21
  INFO: expansion.nutrition.fat: 21/21
  INFO: expansion.nutrition.fiber: 20/21
  INFO: expansion.nutrition.sodium: 21/21
  INFO: expansion.confidenceLabel: 21/21
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 21
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290100659090: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498894: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498948: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105436382: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498900: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105431516: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498986: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000548404: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000548503: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498917: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6009684861000: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000423534: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107971522: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207208703: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610508: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610492: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207208680: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019297208: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4011800633516: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4011800628512: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4011800632519: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=21 baseline=21
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=598  baseline=587  delta=+11
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               21          21          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          598         587         +11
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
