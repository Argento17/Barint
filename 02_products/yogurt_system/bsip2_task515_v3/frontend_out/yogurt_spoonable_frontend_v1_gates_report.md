# Bari Page Generator — Gate Report

**Input:** `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_spoonable_frontend_v1.json`
**Generated:** 2026-07-05T09:06:14Z  |  **Elapsed:** 0.3s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [FAIL] G8 DATA-SANITY | FAIL |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 90/94 non-null
  INFO: name: 94/94 non-null
  INFO: score: 94/94 non-null
  INFO: grade: 94/94 non-null
  INFO: insightLine: 94/94 non-null
  INFO: expansion: 94/94
  INFO: expansion.ingredients: 91/94
  INFO: expansion.nutrition.energyKcal: 94/94
  INFO: expansion.nutrition.protein: 94/94
  INFO: expansion.nutrition.sugar: 80/94
  INFO: expansion.nutrition.fat: 92/94
  INFO: expansion.nutrition.fiber: 38/94
  INFO: expansion.nutrition.sodium: 94/94
  INFO: expansion.confidenceLabel: 94/94
  INFO: Corpus barcodes with image in BSIP1: 117/122
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: Unauthored-copy check: SKIP (pre-copy generator output)
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 94/94 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 94
  INFO: Scored products (trace dirs): 94
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [FAIL] G8 DATA-SANITY
  FAIL: barcode=7290116936581: ingredients field contains nutrition panel text (2+ tokens)
  INFO: Data sanity violations: 1 across checked products
