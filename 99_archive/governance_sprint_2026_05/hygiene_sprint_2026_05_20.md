# Repository Hygiene Sprint — Cleanup Report
**Date:** 2026-05-20  
**Sprint:** Repository Cleanup + Structural Reorganization

## Actions Taken

### Files Archived to 99_archive/

**legacy_bsip2/**
- `matrix_integrity_v1_archive.py` → `legacy_bsip2/matrix_integrity_v1.py`

**old_batch_runners/**
- `batch_run.py` — original generic batch runner, superseded
- `batch_run_milk.py`, `_002.py`, `_003.py` — superseded by `batch_run_milk_004.py`
- `run_matrix_validation.py` — superseded by `run_matrix_validation_v2.py`
- `generate_run_003_reports.py` — superseded by run_004
- `generate_cereals_001_reports.py`, `generate_yogurt_001_reports.py` — one-off, already run

**deprecated_logic/**
- `diagnose_positive_structure.py` — one-off diagnostic
- `generate_review.py` — one-off review generator

**old_reports/bsip2_pre_v4_runs/**
- 8 batch summary/analysis reports from scoring runs prior to milk run_004 recalibration

### Reports Centralized

Created `03_operations/reports/` with `matrix_integrity/`, `enrichment/`, `validation/`, `regression/` subdirs.
Moved active matrix integrity reports and enrichment validation report to centralized location.
Removed now-empty `bsip2/reports/`, `proto_v0/reports/`, `bsip1/reports/` directories.

### Root-Level Placeholders Removed
- `bsip2_proto_v0/` — empty placeholder
- `bsip0_scrape/` — empty placeholder
- `02_products/golden_corpus/` — empty placeholder

### Path Updates
- `run_matrix_validation_v2.py` REPORT_PATH → `03_operations/reports/matrix_integrity/`

### Created
- `C:\Bari\REPO_MAP.md` — authoritative repository navigation guide

## Active src/ After Cleanup (17 files, no dead weight)

Core engine (9): score_engine, signal_extractor, matrix_integrity, nova_proxy, constants,
evaluation_scope, input_loader, trace_writer, category_classifier

Batch runners (4): snack_bars_001, cereals_001, yogurt_001, milk_004

Runners/generators (3): run_matrix_validation_v2, generate_run_004_reports, generate_visuals

Package: __init__.py

## Naming Conventions Going Forward
- Batch runners: `batch_run_{category}_{run_number}.py`
- Validation runners: `run_{system}_validation_v{N}.py`
- Engine versions: one canonical file; archive superseded to `99_archive/legacy_bsip2/`
