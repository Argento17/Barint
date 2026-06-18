# Bari Page Generator — Gate Report

**Input:** `C:\Bari\03_operations\page_generator\outputs\juices_generated_v1.json`
**Generated:** 2026-06-16T06:50:56Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 0/20 non-null
  INFO: name: 20/20 non-null
  INFO: score: 20/20 non-null
  INFO: grade: 20/20 non-null
  INFO: insightLine: 20/20 non-null
  INFO: expansion: 20/20
  INFO: expansion.ingredients: 20/20
  INFO: expansion.nutrition.energyKcal: 20/20
  INFO: expansion.nutrition.protein: 19/20
  INFO: expansion.nutrition.sugar: 18/20
  INFO: expansion.nutrition.fat: 6/20
  INFO: expansion.nutrition.fiber: 0/20
  INFO: expansion.nutrition.sodium: 5/20
  INFO: expansion.confidenceLabel: 20/20
  INFO: Corpus barcodes with image in BSIP1: 0/32
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 20/20 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 20
  INFO: Scored products (trace dirs): 28
  INFO: Declared exclusions in _meta: 8
  INFO:   missing barcode 7290000272696: excluded — removed_from_display: lemon_juice subpool
  INFO:   missing barcode 7290004030148: excluded — removed_from_display: lemon_juice subpool
  INFO:   missing barcode 7290018940761: excluded — removed_from_display: tirosh subpool
  INFO:   missing barcode 7290019398516: excluded — removed_from_display: tirosh subpool
  INFO:   missing barcode 7290106668577: excluded — removed_from_display: lemon_juice subpool
  INFO:   missing barcode 7290117034774: excluded — removed_from_display: lemon_juice subpool
  INFO:   missing barcode 7290117765630: excluded — removed_from_display: tirosh subpool
  INFO:   missing barcode 7290119385034: excluded — removed_from_display: lemon_juice subpool

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=20 baseline=20
  INFO: Image coverage: current=0.0%  baseline=100.0%  delta=-100.0%
  INFO: Avg consumer-text chars/product: current=30  baseline=153  delta=-123
  INFO: Per-barcode grade changes (1):
  INFO:   barcode=7290019056737 [קריסטל מיץ אשכולית 2 ליטר]: E -> D
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               20          20          +0
  INFO:   Image coverage %                           0.0       100.0      -100.0
  INFO:   Avg chars/product                           30         153        -123
  INFO:   Grade changes                                1           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —
