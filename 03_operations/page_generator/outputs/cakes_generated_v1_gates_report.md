# Bari Page Generator — Gate Report

**Input:** `03_operations/page_generator/outputs/cakes_generated_v1.json`
**Generated:** 2026-06-16T06:57:22Z  |  **Elapsed:** 0.3s

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
  INFO: imageUrl: 65/65 non-null
  INFO: name: 65/65 non-null
  INFO: score: 65/65 non-null
  INFO: grade: 65/65 non-null
  INFO: insightLine: 65/65 non-null
  INFO: expansion: 65/65
  INFO: expansion.ingredients: 65/65
  INFO: expansion.nutrition.energyKcal: 65/65
  INFO: expansion.nutrition.protein: 65/65
  INFO: expansion.nutrition.sugar: 64/65
  INFO: expansion.nutrition.fat: 65/65
  INFO: expansion.nutrition.fiber: 11/65
  INFO: expansion.nutrition.sodium: 65/65
  INFO: expansion.confidenceLabel: 65/65
  INFO: Corpus barcodes with image in BSIP1: 167/167
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 65/65 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 65
  INFO: Scored products (trace dirs): 149
  INFO: Declared exclusions in _meta: 84
  INFO:   missing barcode 313184: excluded — not_in_live_curation
  INFO:   missing barcode 4006529002170: excluded — not_in_live_curation
  INFO:   missing barcode 4017100198151: excluded — not_in_live_curation
  INFO:   missing barcode 4017100364112: excluded — not_in_live_curation
  INFO:   missing barcode 46214731552: excluded — not_in_live_curation
  INFO:   missing barcode 46214930207: excluded — not_in_live_curation
  INFO:   missing barcode 4820180816552: excluded — not_in_live_curation
  INFO:   missing barcode 4820180816576: excluded — not_in_live_curation
  INFO:   missing barcode 4820180816590: excluded — not_in_live_curation
  INFO:   missing barcode 4823077633317: excluded — not_in_live_curation
  INFO:   missing barcode 5317194: excluded — not_in_live_curation
  INFO:   missing barcode 5410126006049: excluded — not_in_live_curation
  INFO:   missing barcode 5410126116168: excluded — not_in_live_curation
  INFO:   missing barcode 5410126726244: excluded — not_in_live_curation
  INFO:   missing barcode 5410126806250: excluded — not_in_live_curation
  INFO:   missing barcode 5901414200411: excluded — not_in_live_curation
  INFO:   missing barcode 7290000061245: excluded — not_in_live_curation
  INFO:   missing barcode 7290000075143: excluded — not_in_live_curation
  INFO:   missing barcode 7290011489625: excluded — not_in_live_curation
  INFO:   missing barcode 7290013145406: excluded — not_in_live_curation
  INFO:   missing barcode 7290013156006: excluded — not_in_live_curation
  INFO:   missing barcode 7290013156921: excluded — not_in_live_curation
  INFO:   missing barcode 7290013453068: excluded — not_in_live_curation
  INFO:   missing barcode 7290013740014: excluded — not_in_live_curation
  INFO:   missing barcode 7290017724171: excluded — not_in_live_curation
  INFO:   missing barcode 7290017962139: excluded — not_in_live_curation
  INFO:   missing barcode 7290018893036: excluded — not_in_live_curation
  INFO:   missing barcode 7290019293804: excluded — not_in_live_curation
  INFO:   missing barcode 7290019816034: excluded — not_in_live_curation
  INFO:   missing barcode 7290019816058: excluded — not_in_live_curation
  INFO:   missing barcode 7290019816232: excluded — not_in_live_curation
  INFO:   missing barcode 7290019870463: excluded — not_in_live_curation
  INFO:   missing barcode 7290019870470: excluded — not_in_live_curation
  INFO:   missing barcode 7290020030184: excluded — not_in_live_curation
  INFO:   missing barcode 7290101111986: excluded — not_in_live_curation
  INFO:   missing barcode 7290105364784: excluded — not_in_live_curation
  INFO:   missing barcode 7290106571921: excluded — not_in_live_curation
  INFO:   missing barcode 7290106571945: excluded — not_in_live_curation
  INFO:   missing barcode 7290106656727: excluded — not_in_live_curation
  INFO:   missing barcode 7290112340276: excluded — not_in_live_curation
  INFO:   missing barcode 7290112961754: excluded — not_in_live_curation
  INFO:   missing barcode 7290115206333: excluded — not_in_live_curation
  INFO:   missing barcode 7290118422617: excluded — not_in_live_curation
  INFO:   missing barcode 7290118423904: excluded — not_in_live_curation
  INFO:   missing barcode 7290118426615: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040513: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040568: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040605: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040612: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040650: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040667: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040803: excluded — not_in_live_curation
  INFO:   missing barcode 7290119040858: excluded — not_in_live_curation
  INFO:   missing barcode 7290119041053: excluded — not_in_live_curation
  INFO:   missing barcode 7290119041107: excluded — not_in_live_curation
  INFO:   missing barcode 7290119041152: excluded — not_in_live_curation
  INFO:   missing barcode 7290119043095: excluded — not_in_live_curation
  INFO:   missing barcode 7290119043149: excluded — not_in_live_curation
  INFO:   missing barcode 7290119043743: excluded — not_in_live_curation
  INFO:   missing barcode 7290119043897: excluded — not_in_live_curation
  INFO:   missing barcode 7290122781359: excluded — not_in_live_curation
  INFO:   missing barcode 7290123330488: excluded — not_in_live_curation
  INFO:   missing barcode 7296073161981: excluded — not_in_live_curation
  INFO:   missing barcode 7296073162001: excluded — not_in_live_curation
  INFO:   missing barcode 7296073453840: excluded — not_in_live_curation
  INFO:   missing barcode 7296073453857: excluded — not_in_live_curation
  INFO:   missing barcode 7296073529019: excluded — not_in_live_curation
  INFO:   missing barcode 7296073529026: excluded — not_in_live_curation
  INFO:   missing barcode 7296073659969: excluded — not_in_live_curation
  INFO:   missing barcode 7622201401900: excluded — not_in_live_curation
  INFO:   missing barcode 7622201809188: excluded — not_in_live_curation
  INFO:   missing barcode 7622210137234: excluded — not_in_live_curation
  INFO:   missing barcode 7622210453327: excluded — not_in_live_curation
  INFO:   missing barcode 7622300356767: excluded — not_in_live_curation
  INFO:   missing barcode 7622300489427: excluded — not_in_live_curation
  INFO:   missing barcode 7622300489434: excluded — not_in_live_curation
  INFO:   missing barcode 8000500366073: excluded — not_in_live_curation
  INFO:   missing barcode 8410376037784: excluded — not_in_live_curation
  INFO:   missing barcode 8410376075915: excluded — not_in_live_curation
  INFO:   missing barcode 8710502064814: excluded — not_in_live_curation
  INFO:   missing barcode 8710502139017: excluded — not_in_live_curation
  INFO:   missing barcode 8710502279010: excluded — not_in_live_curation
  INFO:   missing barcode 8710502405204: excluded — not_in_live_curation
  INFO:   missing barcode 8710502470028: excluded — not_in_live_curation

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=65 baseline=65
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=22  baseline=354  delta=-331
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               65          65          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                           22         354        -331
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —
