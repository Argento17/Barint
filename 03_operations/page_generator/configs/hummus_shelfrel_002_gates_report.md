# Bari Page Generator — Gate Report

**Input:** `03_operations/page_generator/configs/hummus_shelfrel_002.json`
**Generated:** 2026-06-25T05:22:54Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [FAIL] G2 COVERAGE | FAIL |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |
| [SKIP] G9 INVERSION-INVARIANT | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #: missing required field '_meta'
  FAIL: #: missing required field 'products'
  FAIL: #: additional property '_comment' not allowed
  FAIL: #: additional property 'category' not allowed
  FAIL: #: additional property 'corpus_dirs' not allowed
  FAIL: #: additional property 'run_products_dir' not allowed
  FAIL: #: additional property 'baseline_json' not allowed
  FAIL: #: additional property 'retailer_scope' not allowed
  FAIL: #: additional property 'subpool_filter' not allowed
  FAIL: #: additional property 'dedup' not allowed
  FAIL: #: additional property 'scoring' not allowed
  FAIL: #: additional property 'exclusions' not allowed
  FAIL: #: additional property 'extension_fields' not allowed
  FAIL: #: additional property 'render_fields' not allowed
  FAIL: #: additional property '_render_fields_note' not allowed
  FAIL: #: additional property 'boundary_policy' not allowed

### [FAIL] G2 COVERAGE
  FAIL: No products in frontend JSON

### [WARN] G3 SCOPE
  INFO: Displayed products: 0
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
