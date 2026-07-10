# Bari Page Generator — Gate Report

**Input:** `C:\Bari\tasks\returns\TASK-461_granola_copy_overhaul.json`
**Generated:** 2026-07-03T01:19:51Z  |  **Elapsed:** 0.0s

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
  INFO: imageUrl: 22/22 non-null
  INFO: name: 22/22 non-null
  INFO: score: 22/22 non-null
  INFO: grade: 22/22 non-null
  INFO: insightLine: 22/22 non-null
  INFO: expansion: 22/22
  INFO: expansion.ingredients: 22/22
  INFO: expansion.nutrition.energyKcal: 22/22
  INFO: expansion.nutrition.protein: 22/22
  INFO: expansion.nutrition.sugar: 22/22
  INFO: expansion.nutrition.fat: 22/22
  INFO: expansion.nutrition.fiber: 22/22
  INFO: expansion.nutrition.sodium: 22/22
  INFO: expansion.confidenceLabel: 22/22
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 22
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290017962047: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116534619: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017962023: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106771369: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106773714: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112498007: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106771314: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013433244: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112497994: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013433336: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106771161: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013433091: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013433107: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7613035635845: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7613037012095: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7613035622623: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011131968: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011131050: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011668587: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014471443: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011131975: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1343845: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=22 baseline=22
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=745  baseline=740  delta=+5
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               22          22          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          745         740          +5
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
