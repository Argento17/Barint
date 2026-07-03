# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/bread_frontend_v4.json`
**Generated:** 2026-07-03T09:45:07Z  |  **Elapsed:** 0.1s

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
  INFO: expansion.nutrition.sugar: 1/23
  INFO: expansion.nutrition.fat: 23/23
  INFO: expansion.nutrition.fiber: 22/23
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
  WARN: barcode=7290016245325: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268429: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481203: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3054183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=574370: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481197: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=497044: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500316: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018540329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079033: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079927: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079477: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9398281: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014321168: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451484: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451507: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500460: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016967074: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079217: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4685027: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1902325: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
