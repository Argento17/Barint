# Bari Page Generator — Gate Report

**Input:** `C:\Bari\03_operations\spine\_e2e_out\page\e2e_page_throwaway.json`
**Generated:** 2026-06-12T17:32:03Z  |  **Elapsed:** 0.0s

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

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 3/3 non-null
  INFO: name: 3/3 non-null
  INFO: score: 3/3 non-null
  INFO: grade: 3/3 non-null
  INFO: insightLine: 3/3 non-null
  INFO: expansion: 3/3
  INFO: expansion.ingredients: 3/3
  INFO: expansion.nutrition.energyKcal: 3/3
  INFO: expansion.nutrition.protein: 3/3
  INFO: expansion.nutrition.sugar: 3/3
  INFO: expansion.nutrition.fat: 3/3
  INFO: expansion.nutrition.fiber: 3/3
  INFO: expansion.nutrition.sodium: 3/3
  INFO: expansion.confidenceLabel: 3/3
  INFO: Corpus barcodes with image in BSIP1: 3/3
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 3/3 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 3
  INFO: Scored products (trace dirs): 3
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
