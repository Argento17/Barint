# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v4.json`
**Generated:** 2026-07-10T08:45:08Z  |  **Elapsed:** 0.3s

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
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 31/31 non-null
  INFO: name: 31/31 non-null
  INFO: score: 31/31 non-null
  INFO: grade: 31/31 non-null
  INFO: insightLine: 31/31 non-null
  INFO: expansion: 31/31
  INFO: expansion.ingredients: 25/31
  INFO: expansion.nutrition.energyKcal: 31/31
  INFO: expansion.nutrition.protein: 31/31
  INFO: expansion.nutrition.sugar: 1/31
  INFO: expansion.nutrition.fat: 31/31
  INFO: expansion.nutrition.fiber: 0/31
  INFO: expansion.nutrition.sodium: 31/31
  INFO: expansion.confidenceLabel: 31/31
  INFO: Corpus barcodes with image in BSIP1: 79/94
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='v4', not v3)

### [PASS] G3 SCOPE
  INFO: Displayed products: 31
  INFO: Scored products (trace dirs): 76
  INFO: Declared exclusions in _meta: 45
  INFO:   missing barcode 2370246: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 4122348: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 4122683: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 4125776: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 4126674: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 474830: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 55350: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 57088: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 57118: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290000057088: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290000057118: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290004122270: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290004122683: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290004125776: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290004137311: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290014455252: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290014763395: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290016818642: excluded — contaminant: ravioli product (pasta, not a cheese); subpool misclassification
  INFO:   missing barcode 7290019635314: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102394463: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102394821: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102394845: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102395378: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102395408: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102395422: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102396672: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290102397204: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290108501346: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290108502725: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290110320867: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7290117265918: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073719786: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073731832: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073731849: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073731863: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073731870: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 7296073731887: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 8606615: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 8606622: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 8606950: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 9954234: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 9954241: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 9954258: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 9954357: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative
  INFO:   missing barcode 9955538: excluded — curation: dedup by (brand_group|cheese_type|fat_pct_bucket); this SKU is a form/packaging variant of the group representative

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
