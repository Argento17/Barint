# Bari Page Generator — Gate Report

**Input:** `03_operations/page_generator/outputs/cereals_generated_v1.json`
**Generated:** 2026-06-16T06:43:54Z  |  **Elapsed:** 0.1s

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
  INFO: imageUrl: 20/20 non-null
  INFO: name: 20/20 non-null
  INFO: score: 20/20 non-null
  INFO: grade: 20/20 non-null
  INFO: insightLine: 20/20 non-null
  INFO: expansion: 20/20
  INFO: expansion.ingredients: 20/20
  INFO: expansion.nutrition.energyKcal: 20/20
  INFO: expansion.nutrition.protein: 20/20
  INFO: expansion.nutrition.sugar: 19/20
  INFO: expansion.nutrition.fat: 20/20
  INFO: expansion.nutrition.fiber: 19/20
  INFO: expansion.nutrition.sodium: 20/20
  INFO: expansion.confidenceLabel: 20/20
  INFO: Corpus barcodes with image in BSIP1: 63/63
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 20/20 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 20
  INFO: Scored products (trace dirs): 63
  INFO: Declared exclusions in _meta: 43
  INFO:   missing barcode 1164266: excluded — granola_subpool
  INFO:   missing barcode 1164273: excluded — granola_subpool
  INFO:   missing barcode 1343845: excluded — granola_subpool
  INFO:   missing barcode 5018357006731: excluded — granola_subpool
  INFO:   missing barcode 5018357006755: excluded — granola_subpool
  INFO:   missing barcode 6582751: excluded — granola_subpool
  INFO:   missing barcode 7290011131050: excluded — granola_subpool
  INFO:   missing barcode 7290011131371: excluded — granola_subpool
  INFO:   missing barcode 7290011131388: excluded — granola_subpool
  INFO:   missing barcode 7290011131395: excluded — granola_subpool
  INFO:   missing barcode 7290011131968: excluded — granola_subpool
  INFO:   missing barcode 7290011131975: excluded — granola_subpool
  INFO:   missing barcode 7290011668587: excluded — granola_subpool
  INFO:   missing barcode 7290013433091: excluded — granola_subpool
  INFO:   missing barcode 7290013433107: excluded — granola_subpool
  INFO:   missing barcode 7290013433244: excluded — granola_subpool
  INFO:   missing barcode 7290013433336: excluded — granola_subpool
  INFO:   missing barcode 7290014471412: excluded — granola_subpool
  INFO:   missing barcode 7290014471429: excluded — granola_subpool
  INFO:   missing barcode 7290014471436: excluded — granola_subpool
  INFO:   missing barcode 7290014471443: excluded — granola_subpool
  INFO:   missing barcode 7290016883176: excluded — granola_subpool
  INFO:   missing barcode 7290016883183: excluded — granola_subpool
  INFO:   missing barcode 7290017325910: excluded — off_banned
  INFO:   missing barcode 7290017962023: excluded — granola_subpool
  INFO:   missing barcode 7290017962047: excluded — granola_subpool
  INFO:   missing barcode 7290106771161: excluded — granola_subpool
  INFO:   missing barcode 7290106771314: excluded — granola_subpool
  INFO:   missing barcode 7290106771369: excluded — granola_subpool
  INFO:   missing barcode 7290106773714: excluded — granola_subpool
  INFO:   missing barcode 7290112494351: excluded — off_banned
  INFO:   missing barcode 7290112495228: excluded — off_banned
  INFO:   missing barcode 7290112497994: excluded — granola_subpool
  INFO:   missing barcode 7290112498007: excluded — granola_subpool
  INFO:   missing barcode 7290116530482: excluded — out_of_scope: bundle_pack
  INFO:   missing barcode 7290116534619: excluded — granola_subpool
  INFO:   missing barcode 7290116535371: excluded — off_banned
  INFO:   missing barcode 7290118420811: excluded — out_of_scope: crispbread
  INFO:   missing barcode 7613035622623: excluded — granola_subpool
  INFO:   missing barcode 7613035635845: excluded — granola_subpool
  INFO:   missing barcode 7613037012095: excluded — granola_subpool
  INFO:   missing barcode 8445290964595: excluded — granola_subpool
  INFO:   missing barcode 884912126115: excluded — granola_subpool

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=20 baseline=20
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=27  baseline=239  delta=-212
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               20          20          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                           27         239        -212
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —
