# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/juices_frontend_v3.json`
**Generated:** 2026-07-10T09:16:48Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

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

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
