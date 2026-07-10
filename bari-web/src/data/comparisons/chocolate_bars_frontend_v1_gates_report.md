# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json`
**Generated:** 2026-07-10T09:16:47Z  |  **Elapsed:** 0.1s

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
  INFO: imageUrl: 23/23 non-null
  INFO: name: 23/23 non-null
  INFO: score: 23/23 non-null
  INFO: grade: 23/23 non-null
  INFO: insightLine: 23/23 non-null
  INFO: expansion: 23/23
  INFO: expansion.ingredients: 23/23
  INFO: expansion.nutrition.energyKcal: 23/23
  INFO: expansion.nutrition.protein: 23/23
  INFO: expansion.nutrition.sugar: 23/23
  INFO: expansion.nutrition.fat: 23/23
  INFO: expansion.nutrition.fiber: 4/23
  INFO: expansion.nutrition.sodium: 23/23
  INFO: expansion.confidenceLabel: 23/23
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 23
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=5000159560511: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72991008: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106651265: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116536781: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116536774: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900951310379: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116532011: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110571405: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290100249086: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116537375: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116532042: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116531748: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3800020401552: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112494283: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000159559485: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105362377: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72917367: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000159561976: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72917329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077617041: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116534442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72918388: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=34000250103: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
