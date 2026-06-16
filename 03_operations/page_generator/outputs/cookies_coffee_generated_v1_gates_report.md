# Bari Page Generator — Gate Report

**Input:** `03_operations\page_generator\outputs\cookies_coffee_generated_v1.json`
**Generated:** 2026-06-16T07:06:35Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 118/118 non-null
  INFO: name: 118/118 non-null
  INFO: score: 118/118 non-null
  INFO: grade: 118/118 non-null
  INFO: insightLine: 118/118 non-null
  INFO: expansion: 118/118
  INFO: expansion.ingredients: 118/118
  INFO: expansion.nutrition.energyKcal: 118/118
  INFO: expansion.nutrition.protein: 117/118
  INFO: expansion.nutrition.sugar: 113/118
  INFO: expansion.nutrition.fat: 118/118
  INFO: expansion.nutrition.fiber: 74/118
  INFO: expansion.nutrition.sodium: 116/118
  INFO: expansion.confidenceLabel: 118/118
  INFO: Corpus barcodes with image in BSIP1: 61/61
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 118/118 insightLines still PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 118
  INFO: Scored products (trace dirs): 58
  INFO: Declared exclusions in _meta: 90
  INFO:   missing barcode 7290013453631: excluded — discard_wrong_ingredients
  INFO:   missing barcode 7290017962108: excluded — discard_wrong_scrape
  WARN: Displayed barcode 313184 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 4006529002170 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 4017100198151 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 4017100364112 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 46214731552 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 46214930207 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 4823077633317 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 5901414200411 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290000061245 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290000075143 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290013156006 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290013156921 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290013453068 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290013740014 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290017724171 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290018893036 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019293804 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019816034 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019816058 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019816232 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019870463 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019870470 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290020030184 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290101111986 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290105364784 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290106571921 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290106571945 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290106656727 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290112340276 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290112961754 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290115206333 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118422617 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118423904 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118426615 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119040605 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119040650 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119040858 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119043149 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119043897 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290122781359 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073161981 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073162001 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073453840 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073453857 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073529019 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073529026 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073659969 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622201401900 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622201809188 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622210137234 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622210453327 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622300356767 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622300489427 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7622300489434 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8000500366073 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8410376037784 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8410376075915 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8710502064814 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8710502139017 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8710502279010 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8710502405204 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8710502470028 has no BSIP2 trace in --run dir (ghost product)

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290020030184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290122781359: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013453068: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043149: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013156921: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000061245: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740014: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013156006: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=313184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118423904: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118422617: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019293804: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453840: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453857: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106571945: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410376037784: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816034: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118426615: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106571921: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410376075915: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019870470: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077633317: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017724171: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4006529002170: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073162001: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040858: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893036: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105364784: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502139017: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502405204: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502279010: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043897: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112961754: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=46214731552: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073529019: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073529026: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4017100364112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300489427: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8000500366073: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622210137234: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5901414200411: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073161981: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4017100198151: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502470028: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106656727: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=46214930207: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300489434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019870463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040605: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040650: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073659969: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201401900: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112340276: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300356767: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816232: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115206333: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201809188: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000075143: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816058: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290101111986: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622210453327: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502064814: no trace found in --run dir, cannot verify score vs trace

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=118 baseline=118
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=24  baseline=402  delta=-377
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                              118         118          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                           24         402        -377
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —
