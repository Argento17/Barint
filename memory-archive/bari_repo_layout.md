---
name: bari-repo-layout
description: "Canonical Bari repository directory structure after 2026-05-20 hygiene sprint — active paths, archive locations, report centralization"
metadata:
  node_type: memory
  type: project
  originSessionId: 88339fa2-f552-455b-8eed-95c12c9cad01
---

Hygiene sprint completed 2026-05-20. Repository now has clean structural separation.
Authoritative navigation guide: `C:\Bari\REPO_MAP.md`

## Active Pipeline Paths

**BSIP0 scraping:**
- `C:\Bari\03_operations\bsip0\scrape\yohananof\` — active Yohananof scraper (4 scripts)
- `C:\Bari\03_operations\bsip0\scrape\yohananof_milk\` — milk-specific scraper

**BSIP1 enrichment:**
- `C:\Bari\03_operations\bsip1\core\ingredient_enricher.py` — active enrichment engine
- `C:\Bari\03_operations\bsip1\core\enrich_runner.py` — batch runner
- `C:\Bari\03_operations\bsip1\run_001\output\` — snack bars (53 products)
- `C:\Bari\03_operations\bsip1\run_cereals_001\output\` — cereals (45 products)
- `C:\Bari\03_operations\bsip1\run_yogurt_001\output\` — yogurt (45 products)
- `C:\Bari\03_operations\bsip1\run_milk_002\output\` — milk (20 products, canonical)

**BSIP2 scoring engine (all in proto_v0/src/):**
- `score_engine.py` — main scorer
- `signal_extractor.py` — L1-L6 signals
- `matrix_integrity.py` — Matrix Integrity v2 (current)
- `nova_proxy.py`, `constants.py`, `evaluation_scope.py` (imported by all runners)
- `input_loader.py`, `trace_writer.py`, `category_classifier.py`

**Active batch runners:**
- `batch_run_snack_bars_001.py`, `batch_run_cereals_001.py`, `batch_run_yogurt_001.py`, `batch_run_milk_004.py`

**Active validation runners:**
- `run_matrix_validation_v2.py` — imports v2 from src/ AND v1 from `99_archive/legacy_bsip2/matrix_integrity_v1.py`
- `generate_run_004_reports.py` — milk run_004 report generator
- `generate_visuals.py` — chart generation

## Centralized Reports (all live here after hygiene sprint)
- `C:\Bari\03_operations\reports\matrix_integrity\` — matrix integrity validation and calibration
- `C:\Bari\03_operations\reports\enrichment\` — enrichment validation
- `C:\Bari\03_operations\reports\validation\` — (reserved for future)
- `C:\Bari\03_operations\reports\regression\` — (reserved for future)

## Archive
- `C:\Bari\99_archive\legacy_bsip2\matrix_integrity_v1.py` — v1 engine (imported by comparison runner)
- `C:\Bari\99_archive\old_batch_runners\` — batch_run.py, batch_run_milk v1-v3, run_matrix_validation_v1, old generators
- `C:\Bari\99_archive\old_reports\bsip2_pre_v4_runs\` — batch reports from scoring runs before milk run_004
- `C:\Bari\99_archive\deprecated_logic\` — one-off scripts (diagnose_positive_structure, generate_review)
- `C:\Bari\99_archive\bisp2_concept_prototype\` — original BSIP2 v0 prototype (pre-rewrite)

## Key Structural Rules
- `99_archive/` = read-only, no editing
- `03_operations/reports/` = only writes from runner scripts, not hand-edited
- `proto_v0/src/` = active engine code only (17 .py files, no dead weight after sprint)
- Category product data: `02_products/{category}/intelligence_bsip2/run_XXX/`
- BSIP1 records: `03_operations/bsip1/run_{category}/output/bsip1_{barcode}.json`

## Root Dirs (after sprint)
```
C:\Bari\
  01_framework/   framework docs + ontology
  02_products/    category datasets + analysis
  03_operations/  active pipelines + centralized reports
  governance/     architecture decisions + freeze inventory
  99_archive/     historical/deprecated (read-only)
  REPO_MAP.md     authoritative navigation guide
```

## What Doesn't Exist
- `04_frontend/` — no frontend built yet; cursor handoff at `02_products/milk_and_alternatives/reports/cursor_handoff_milk_comparison.md`
- Root-level `bsip0_scrape/` and `bsip2_proto_v0/` — removed (were empty placeholders)
- `02_products/golden_corpus/` — removed (was empty)
