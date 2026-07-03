# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/protein_combined_frontend_v2.json`
**Generated:** 2026-07-03T13:58:41Z  |  **Elapsed:** 0.1s

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
  FAIL: #.products[0]: additional property 'name_he' not allowed
  FAIL: #.products[0]: additional property 'format' not allowed
  FAIL: #.products[0]: additional property 'image_url' not allowed
  FAIL: #.products[0]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[0]: additional property 'protein_per_100g' not allowed
  FAIL: #.products[0]: additional property 'protein_per_bar' not allowed
  FAIL: #.products[0]: additional property 'bar_weight_g' not allowed
  FAIL: #.products[0]: additional property 'show_per_bar' not allowed
  FAIL: #.products[0]: additional property '_scoring_trace' not allowed
  FAIL: #.products[0]: additional property 'displayTitle' not allowed
  FAIL: #.products[1]: additional property 'name_he' not allowed
  FAIL: #.products[1]: additional property 'format' not allowed
  FAIL: #.products[1]: additional property 'image_url' not allowed
  FAIL: #.products[1]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[1]: additional property 'protein_per_100g' not allowed
  FAIL: #.products[1]: additional property 'protein_per_bar' not allowed
  FAIL: #.products[1]: additional property 'bar_weight_g' not allowed
  FAIL: #.products[1]: additional property 'show_per_bar' not allowed
  FAIL: #.products[1]: additional property '_scoring_trace' not allowed
  FAIL: #.products[1]: additional property 'displayTitle' not allowed
  FAIL: ... and 300 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 32/32 non-null
  INFO: name: 32/32 non-null
  INFO: score: 32/32 non-null
  INFO: grade: 32/32 non-null
  INFO: insightLine: 32/32 non-null
  INFO: expansion: 32/32
  INFO: expansion.ingredients: 32/32
  INFO: expansion.nutrition.energyKcal: 32/32
  INFO: expansion.nutrition.protein: 32/32
  INFO: expansion.nutrition.sugar: 32/32
  INFO: expansion.nutrition.fat: 32/32
  INFO: expansion.nutrition.fiber: 31/32
  INFO: expansion.nutrition.sodium: 32/32
  INFO: expansion.confidenceLabel: 32/32
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 32
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290017516295: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019766025: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290121161886: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290121166850: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119371129: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610379: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119371112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018703991: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018703984: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610386: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015130042: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015130035: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117384572: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117384589: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290117384596: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290121160582: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290121161916: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290121161930: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019766018: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018703304: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018703076: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018043899: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018043134: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019310235: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015130028: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019401049: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019401018: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019766230: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112915382: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112913487: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112915351: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019401544: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=32 baseline=32
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=637  baseline=631  delta=+7
  INFO: Per-barcode grade changes (3):
  INFO:   barcode=7290015130028 [WIN חטיף חלבון קרם חלב]: C -> D
  INFO:   barcode=7290019401018 [חטיף קרם עוגיות]: C -> D
  INFO:   barcode=7290019401049 [חטיף שוקולד קרמל]: C -> D
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               32          32          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          637         631          +7
  INFO:   Grade changes                                3           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
