# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\hummus_frontend_v5.json`
**Generated:** 2026-06-16T04:51:16Z  |  **Elapsed:** 0.3s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 69/69 non-null
  INFO: name: 69/69 non-null
  INFO: score: 69/69 non-null
  INFO: grade: 69/69 non-null
  INFO: insightLine: 69/69 non-null
  INFO: expansion: 69/69
  INFO: expansion.ingredients: 65/69
  INFO: expansion.nutrition.energyKcal: 69/69
  INFO: expansion.nutrition.protein: 69/69
  INFO: expansion.nutrition.sugar: 64/69
  INFO: expansion.nutrition.fat: 69/69
  INFO: expansion.nutrition.fiber: 23/69
  INFO: expansion.nutrition.sodium: 69/69
  INFO: expansion.confidenceLabel: 69/69
  INFO: Corpus barcodes with image in BSIP1: 69/69
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 5/69 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 69
  INFO: Scored products (trace dirs): 69
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=3643820 field=insightLine: sodium causally framed: 'כיב יחיד — 17.2 גרם חלבון ונתרן'
  FAIL: barcode=6666444 field=insightLine: sodium causally framed: 'כי ההרכב פשוט יחסית, אך הנתרן'
  FAIL: barcode=7290015858175 field=insightLine: sodium causally framed: 'כי בסיס הפלפל דומיננטי והנתרן'
  FAIL: barcode=7296073725381 field=insightLine: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7296073725381 field=rowVerdict: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290119374892 field=insightLine: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290119374892 field=rowVerdict: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7296073725510 field=insightLine: sodium causally framed: 'בגלל הנתרן'
  FAIL: barcode=7290119374885 field=insightLine: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided
