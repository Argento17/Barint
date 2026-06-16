# Bari Page Generator — Gate Report

**Input:** `C:\Bari\03_operations\page_generator\outputs\granola_generated_v1.json`
**Generated:** 2026-06-12T14:19:06Z  |  **Elapsed:** 0.1s

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
  INFO: imageUrl: 25/25 non-null
  INFO: name: 25/25 non-null
  INFO: score: 25/25 non-null
  INFO: grade: 25/25 non-null
  INFO: insightLine: 25/25 non-null
  INFO: expansion: 25/25
  INFO: expansion.ingredients: 25/25
  INFO: expansion.nutrition.energyKcal: 25/25
  INFO: expansion.nutrition.protein: 25/25
  INFO: expansion.nutrition.sugar: 0/25
  INFO: expansion.nutrition.fat: 25/25
  INFO: expansion.nutrition.fiber: 24/25
  INFO: expansion.nutrition.sodium: 25/25
  INFO: expansion.confidenceLabel: 25/25
  INFO: Corpus barcodes with image in BSIP1: 66/66
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name

### [PASS] G3 SCOPE
  INFO: Displayed products: 25
  INFO: Scored products (trace dirs): 63
  INFO: Declared exclusions in _meta: 75
  INFO:   missing barcode 3387390525960: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 5010029000061: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 5018357006731: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 5018357006755: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 5900020012814: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'childrens_character' does not match required 'granola'
  INFO:   missing barcode 5900020036407: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 7290011131371: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290011131388: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290011131395: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290014471412: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290014471429: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290014471436: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290016883176: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290016883183: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'muesli' does not match required 'granola'
  INFO:   missing barcode 7290017325910: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cornflakes' does not match required 'granola'
  INFO:   missing barcode 7290017894904: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7290017894911: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7290017894928: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7290107647731: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 7290107647854: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cereal_other' does not match required 'granola'
  INFO:   missing barcode 7290112494351: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cornflakes' does not match required 'granola'
  INFO:   missing barcode 7290112495228: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cornflakes' does not match required 'granola'
  INFO:   missing barcode 7290112495433: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7290116530482: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cornflakes' does not match required 'granola'
  INFO:   missing barcode 7290116535371: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 7290118420811: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7296073642022: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cereal_other' does not match required 'granola'
  INFO:   missing barcode 7296073642046: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'cornflakes' does not match required 'granola'
  INFO:   missing barcode 7296073705550: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7296073705567: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 7296073705574: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 72968: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 7297488098688: excluded — no_corpus_record: barcode not found in any corpus_dir
  INFO:   missing barcode 7297488199590: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'puffed_extruded' does not match required 'granola'
  INFO:   missing barcode 7613030979647: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'childrens_character' does not match required 'granola'
  INFO:   missing barcode 8445290964595: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'whole_grain_flakes' does not match required 'granola'
  INFO:   missing barcode 8445291638839: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'
  INFO:   missing barcode 884912126115: excluded — subpool_filter: field 'bsip_cereal_subtype' = 'oat_cereal' does not match required 'granola'

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=25 baseline=42
  INFO: Products added vs baseline (1): 7290014471443
  INFO: Products removed vs baseline (18): 3560070826186, 5010026515919, 5010026521149, 5018357006731, 5018357006755, 7290011131371, 7290011131388, 7290011131395, 7290011668570, 7290014471412, 7290014471429, 7290014471436, 7290016883183, 7290019603634, 7290114603034, 7290120871069, 7297488099821, 7613035758834
  INFO: Image coverage: current=100.0%  baseline=78.6%  delta=+21.4%
  INFO: Avg consumer-text chars/product: current=59  baseline=333  delta=-274
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               25          42         -17
  INFO:   Image coverage %                         100.0        78.6       +21.4
  INFO:   Avg chars/product                           59         333        -274
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               1           —           —
  INFO:   Products removed                            18           —           —
