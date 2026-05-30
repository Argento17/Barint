# Repository Migration Inventory

**Status:** Planning document — no files have been moved.  
**Scan date:** 2026-05-17  
**Scope:** `C:\Bari\` top-level and all subdirectories

---

## Top-level directory inventory

| Directory | Status | Classification | Notes |
|---|---|---|---|
| `BISP0\` | Empty | Unknown | Uppercase inconsistency; no files inside; purpose unclear; likely abandoned placeholder |
| `bisp2_concept\` | Active (superseded) | Framework prototype | Pre-v1 Python scoring scripts + tests; superseded by `bisp2_concept_v1` + `bsip2_proto_v0` |
| `bisp2_concept_v1\` | Active | Framework documentation | Primary design document repository for BSIP2 scoring architecture |
| `bsip0_pipeline\` | Active (paused) | BSIP0 layer — OCR/image extraction | Prototype with 10 product test set; ground truth data present |
| `bsip0_scrape\` | Active (paused) | BSIP0 layer — web scraping | Two retailers (Carrefour 14+ products, Yohananof 50+ products); v0.2 freeze present |
| `bsip1_concept\` | Active | BSIP1 layer — cross-retailer consolidation | 53 BSIP1 output JSONs; trust scoring implemented |
| `bsip2_proto_v0\` | Active | BSIP2 prototype — scoring engine | 53 scored products, reports, review dashboard, visuals |
| `freezes\` | Incomplete | Freeze archive | Only one freeze present; missing docs/ subdirectory tree and validation/ |

---

## Detailed subdirectory inventory

### `BISP0\`

| Item | Status | Notes |
|---|---|---|
| *(empty)* | Empty directory | No contents; uppercase naming inconsistent with all other directories |

**Verdict:** Abandoned placeholder. Candidate for deletion or archive. The intended BISP0 content (OCR pipeline, web scrape) was developed under `bsip0_pipeline\` and `bsip0_scrape\` instead.

---

### `bisp2_concept\` (pre-v1 prototype)

| Item | Type | Notes |
|---|---|---|
| `bsip2_engine.py` | Python | Older scoring engine — superseded |
| `bsip2_score.py` | Python | Scoring entry point — superseded |
| `bsip2_dimensions.py` | Python | Dimension implementations — superseded |
| `bsip2_guardrails.py` | Python | Cap/penalty logic — superseded |
| `bsip2_nova.py` | Python | NOVA proxy — superseded |
| `bsip2_constants.py` | Python | Constants — superseded |
| `bsip2_trace.py` | Python | Trace generation — superseded |
| `bsip2_report.py` | Python | Report generation — superseded |
| `bsip2_classify.py` | Python | Category classifier — superseded |
| `bsip2_pipeline.py` | Python | Pipeline orchestration — superseded |
| `bsip2_batch.py` | Python | Batch runner — superseded |
| `tests/` | Test directory | 9 test files including golden products, concern coordinator; all superseded |
| `input.xlsx` | Data | Experiment input file |
| `outputv3.xlsx` | Data | Experiment output file |
| `sample_bsip1.csv` | Data | Sample BSIP1 input |
| `Barinew_v3.zip` | Archive | Archived zip of older version |
| `__pycache__/` | Artifact | Python bytecode cache — deletable |

**Verdict:** Superseded prototype. Python code is the direct ancestor of `bsip2_proto_v0\src\` but with significant divergence. `tests/` contains logic that may have research value. `Barinew_v3.zip` is a redundant archive of already-archived code. Archive entire directory to `99_archive\`.

---

### `bisp2_concept_v1\` (active framework docs)

| Item | Type | Notes |
|---|---|---|
| `*.md` (7 files) | Design docs | Top-level concept documents: architecture overview, NOVA proxy, signal taxonomy, etc. |
| `docs/scoring/` | Design docs | ~5 scoring-specific design documents |
| `docs/positive_structure_v1/` | Design docs | 6 new positive structure documents (created 2026-05-17) |
| `docs/` (other) | Design docs | ~6 additional docs covering fragmentation, beneficial processing, etc. |
| `validation/` | Validation docs | 6 validation documents covering score analysis |

**Verdict:** Active and primary. Move to `01_framework\` in target architecture. All content is documentation-only — no Python code.

---

### `bsip0_pipeline\` (OCR/image extraction)

| Item | Type | Notes |
|---|---|---|
| `main.py` | Python | Pipeline entry point |
| `extractor.py` | Python | Image/OCR extraction logic |
| `raw_ocr.py` | Python | Raw OCR output handling |
| `evaluate_parser.py` | Python | Parser evaluation |
| `azure_test.py` | Python | Azure API test script |
| `data/raw/snack_bars/` | Data | 10 products (product_001–010), 4 images each (40 total images) |
| `outputs/` | Data | product_001.json through product_010.json (10 parsed outputs) |
| `cache/ocr_cache.json` | Cache | OCR API response cache |
| `ground_truth.xlsx` | Data | Ground truth annotations for 10 products |

**Verdict:** Active prototype, currently paused. Part of the BSIP0 extraction layer (image path). Move to `03_operations\bsip0\pipeline\` in target architecture. Keep data and cache intact.

---

### `bsip0_scrape\` (web scraper)

| Item | Type | Notes |
|---|---|---|
| `carrefour/` | Python + outputs | 6 pipeline scripts (01–06); outputs with 14+ product JSONs |
| `yohananof/` | Python + outputs | 4 pipeline scripts (01–04); outputs with 50+ product JSONs |
| `bsip_freezes/bsip0_v0_2/` | Freeze | 7 files: freeze metadata, changelog, schema snapshot |
| `docs/CHANGELOG_BSIP0_v0_2.md` | Duplicate | Exact duplicate of `bsip_freezes/bsip0_v0_2/CHANGELOG_BSIP0_v0_2.md` |
| `retailer_capabilities/carrefour.yaml` | Config | Carrefour scraping capability spec |
| `schemas/` | Empty | Schemas directory — never populated |

**Verdict:** Active (paused). Move to `03_operations\bsip0\scrape\`. The `bsip_freezes/` subdirectory should be extracted to top-level `01_framework\freezes\bsip0_v0_2\`. Duplicate changelog should be removed. Empty `schemas/` directory should be removed or renamed to note it was never populated.

---

### `bsip1_concept\` (cross-retailer consolidation)

| Item | Type | Notes |
|---|---|---|
| `batch_test_001/batch_test_001.py` | Python | BSIP1 batch processing script |
| `batch_test_001/output/bsip1_*.json` | Data | 53 BSIP1 output JSONs (one per product) |
| `batch_test_001/output/bsip1_audit_*.json` | Data | 53 BSIP1 audit JSONs (trust scoring audit trail) |

**Verdict:** Active outputs. The `batch_test_001/` naming is operational (a specific run), not conceptual. Move to `03_operations\bsip1\` in target architecture.

---

### `bsip2_proto_v0\` (active BSIP2 prototype)

| Item | Type | Notes |
|---|---|---|
| `src/` | Python | 13 source files: score_engine.py, constants.py, dimensions.py, guardrails.py, classify.py, nova.py, trace.py, batch.py, report.py, generate_review.py, diagnose_positive_structure.py, + others |
| `outputs/products/` | Data | 53 product directories, each with bsip2_trace.json |
| `reports/` | Data | 8 markdown analysis reports |
| `review/` | Data | CSV, XLSX, HTML review dashboard |
| `visuals/` | Data | 11 PNGs, 5 waterfall PNGs, 6 CSVs |

**Verdict:** Active prototype. Primary home of all BSIP2 scoring code and outputs. Move to `03_operations\bsip2\proto_v0\` in target architecture.

---

### `freezes\` (top-level freeze archive)

| Item | Type | Notes |
|---|---|---|
| `bsip2_concept_v1/` | Partial freeze | MISSING: docs/ subdirectory structure (only has docs/scoring/); MISSING: validation/ directory entirely |

**Verdict:** Incomplete freeze. The freeze of `bisp2_concept_v1` was done before docs/positive_structure_v1/ and most of docs/ were written. This freeze snapshot is outdated and misleading. It should either be updated with a complete snapshot or labeled as a partial/superseded snapshot. See `freeze_inventory.md` for detailed recommendation.

---

## Clutter, duplicates, and anomalies

| Issue | Location | Severity | Action |
|---|---|---|---|
| Empty directory | `BISP0\` | Low | Archive or delete |
| Empty directory | `bsip0_scrape\schemas\` | Low | Delete (schemas never written) |
| Duplicate file | `bsip0_scrape\docs\CHANGELOG_BSIP0_v0_2.md` | Low | Delete; canonical copy is in `bsip_freezes\bsip0_v0_2\` |
| Naming inconsistency | `BISP0` (uppercase) vs all others (lowercase) | Low | Rename to `bsip0_placeholder` or delete |
| Naming inconsistency | `bisp2_concept` vs `bisp2_concept_v1` (different prefix style) | Low | Clarify by archiving `bisp2_concept` |
| Incomplete freeze | `freezes\bsip2_concept_v1\` | Medium | Update or label as partial |
| `__pycache__\` in prototype | `bisp2_concept\__pycache__\` | Low | Delete (regenerable) |
| Redundant archive zip | `bisp2_concept\Barinew_v3.zip` | Low | Archive with directory or delete |
| Operational naming | `bsip1_concept\batch_test_001\` | Low | Rename to reflect content (bsip1_run_001 or similar) |
| Diagnostic script | `bsip2_proto_v0\src\diagnose_positive_structure.py` | Low | Move to `reports/` or label as one-off |

---

## Summary counts

| Category | Count |
|---|---|
| Active directories | 5 (`bisp2_concept_v1`, `bsip0_pipeline`, `bsip0_scrape`, `bsip1_concept`, `bsip2_proto_v0`) |
| Archive candidates | 2 (`BISP0`, `bisp2_concept`) |
| Incomplete freeze | 1 (`freezes/bsip2_concept_v1`) |
| Duplicate files | 1 (CHANGELOG) |
| Empty directories | 2 (`BISP0`, `bsip0_scrape/schemas`) |
| Python source files (active) | 13 (in `bsip2_proto_v0/src/`) |
| Python source files (archived) | 11 (in `bisp2_concept/`) |
| Total products (BSIP2 scored) | 53 |
| Total BSIP0 OCR products | 10 |
| Total BSIP0 scrape products | ~64 (14 Carrefour + 50 Yohananof) |
