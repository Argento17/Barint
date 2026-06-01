# Bari Repository Map
**Last updated:** 2026-05-20  
**Architecture state:** Stabilization — Matrix Integrity v2 complete, Router v2 complete, Bread-Light stress test complete

This document is the authoritative navigation guide for the Bari repository.
For architectural philosophy, see `governance/target_architecture.md`.

---

## Active Pipeline Summary

```
Raw retail data
    ↓
BSIP0  (scraping + OCR + parsing)
    ↓
BSIP1  (canonical enrichment: ingredients, additives, protein, matrix, fermentation)
    ↓
BSIP2  (structural scoring: matrix integrity, NOVA proxy, 10 dimensions, grade)
    ↓
Intelligence outputs (traces, reports, comparison pages)
```

---

## 01_framework/ — Core Ontology and Design

| Path | Purpose | Status |
|------|---------|--------|
| `bsip2_framework/` | Active framework docs (scoring philosophy, signal taxonomy, UI language) | **Active** |
| `bsip2_framework/ui_language.md` | Hebrew grade labels, tone rules, dimension names — source of truth for UI | **Active** |
| `bsip2_framework/v3_architecture/` | V3 universal core + archetype system design | **Active** |
| `bsip2_framework/docs/` | Conceptual papers (beneficial processing, matrix integrity framework, etc.) | **Active reference** |
| `bsip2_framework/validation/` | Golden product suite, edge case catalog, failure mode catalog | **Active** |
| `bsip2_framework/validation/golden_corpus/golden_corpus_manifest.json` | **Regression corpus** — 12 structural class anchors (6 real products + 6 signal bundles) | **Active** |
| `bsip2_framework/architecture_v2/` | Older v2 architecture docs | **Superseded — reference only** |
| `freezes/bsip2_concept_v1_complete/` | Frozen snapshot of bsip2 framework at v1 milestone | **Archive (frozen)** |
| `shared/` | Cross-pipeline shared references | **Placeholder** |

---

## 02_products/ — Category Datasets and Intelligence

Each category follows this internal structure:
```
{category}/
  observations_bsip0/    raw scrape data (bsip0 outputs per product)
  canonical_bsip1/       canonical BSIP1 records (authoritative product source)
  intelligence_bsip2/    BSIP2 scored traces (run_XXX/products/{barcode}/bsip2_trace.json)
  reports/               category-level analysis docs
  raw_sources/           pre-scrape reference materials
```

### Active Categories

| Category | BSIP1 Source | BSIP2 Canonical Run | Notes |
|----------|-------------|---------------------|-------|
| `snack_bars/` | `03_operations/bsip1/run_001/output/` | `intelligence_bsip2/run_001/` | 53 products |
| `breakfast_cereals/` | `03_operations/bsip1/run_cereals_001/output/` | `intelligence_bsip2/run_cereals_001/` | 45 products |
| `yogurt_system/` | `03_operations/bsip1/run_yogurt_001/output/` | `intelligence_bsip2/run_yogurt_001/` | 45 products |
| `milk_and_alternatives/` | `03_operations/bsip1/run_milk_002/output/` | `intelligence_bsip2/run_004_recalibrated/` | 20 products |

### Stress Test Corpora (synthetic — not production datasets)

| Corpus | Source | Run | Purpose |
|--------|--------|-----|---------|
| `bread_light/` | `03_operations/bsip1/run_bread_light_001/output/` | `bsip2_outputs/run_bread_light_001/` | 32 synthetic products, 6 stress groups (A-F) — ontology pressure test |

### Key files
- `milk_and_alternatives/reports/run_003_final/website_candidates.md` — 6 curated milk comparison products with barcodes + scores
- `milk_and_alternatives/reports/cursor_handoff_milk_comparison.md` — frontend handoff for `/hashvaot/milk-comparison` page
- `{category}/intelligence_bsip2/latest_review/bsip2_master_products.csv` — flat export for review
- `bread_light/reports/bread_light_001_*.md` — 9 analysis outputs from bread-light stress test

---

## 03_operations/ — Active Pipelines and Runners

### BSIP0: Scraping + OCR

| Path | Purpose |
|------|---------|
| `bsip0/scrape/yohananof/` | Active Yohananof scraper (4 scripts: discover → approve → scrape → audit) |
| `bsip0/scrape/yohananof/outputs/yohananof/` | Scraped product data (HTML, JSON, images) |
| `bsip0/scrape/yohananof_milk/` | Milk-specific scraper + BSIP1 builder |
| `bsip0/pipeline/` | OCR pipeline (Azure-based extractor for physical label images) |

### BSIP1: Semantic Enrichment

| Path | Purpose |
|------|---------|
| `bsip1/core/ingredient_enricher.py` | **Active enrichment engine** — all Hebrew term detection |
| `bsip1/core/enrich_runner.py` | Batch enricher runner (runs across all product datasets) |
| `bsip1/core/test_enricher.py` | 64-check test suite (run with pytest) |
| `bsip1/run_001/output/` | Enriched snack bars (53 products) |
| `bsip1/run_cereals_001/output/` | Enriched cereals (45 products) |
| `bsip1/run_yogurt_001/output/` | Enriched yogurt (45 products) |
| `bsip1/run_milk_002/output/` | **Canonical enriched milk** (20 products, current) |

### BSIP2: Scoring Engine

| Path | Purpose |
|------|---------|
| `bsip2/proto_v0/src/score_engine.py` | Main scoring engine (10 dimensions, grade, trace) |
| `bsip2/proto_v0/src/signal_extractor.py` | L1-L6 signal extraction layer |
| `bsip2/proto_v0/src/matrix_integrity.py` | **Matrix Integrity Engine v2** (structural food interpretation) |
| `bsip2/proto_v0/src/structural_classifier.py` | **Structural Class Classifier v1** — A-F soft assignment from trace signals |
| `bsip2/proto_v0/src/nova_proxy.py` | NOVA proxy inference from Hebrew ingredient text |
| `bsip2/proto_v0/src/constants.py` | Shared constants (red label thresholds, grade bounds) |
| `bsip2/proto_v0/src/evaluation_scope.py` | Scope assignment (imported by all batch runners) |
| `bsip2/proto_v0/src/input_loader.py` | BSIP1 record loader |
| `bsip2/proto_v0/src/trace_writer.py` | BSIP2 trace JSON writer |
| `bsip2/proto_v0/src/router_v2.py` | **Router v2** — 3-stage routing (anchor → context-gated signals → resolution). Drop-in replacement for category_classifier. |
| `bsip2/proto_v0/src/category_classifier.py` | Product category classifier (v1 — superseded by router_v2) |

### Active Batch Runners

| Script | Runs scoring for |
|--------|----------------|
| `bsip2/proto_v0/src/batch_run_snack_bars_001.py` | snack_bars |
| `bsip2/proto_v0/src/batch_run_cereals_001.py` | breakfast_cereals |
| `bsip2/proto_v0/src/batch_run_yogurt_001.py` | yogurt |
| `bsip2/proto_v0/src/batch_run_milk_004.py` | milk (current canonical) |
| `bsip2/proto_v0/src/batch_run_bread_light_001.py` | bread_light stress corpus (32 synthetic products) |

### Active Validation / Report Runners

| Script | Purpose |
|--------|---------|
| `bsip2/proto_v0/src/run_matrix_validation_v2.py` | Matrix Integrity v1 vs v2 comparison |
| `bsip2/proto_v0/src/run_regression_check.py` | **Golden corpus regression check** — run after every engine change |
| `bsip2/proto_v0/src/run_router_regression.py` | **Router v2 regression suite** — 12-case corpus; run after any router_v2 change |
| `bsip2/proto_v0/src/router_regression_corpus.json` | 12-case router regression corpus (anchors, WFF gating, beverage gate, dairy suppression) |
| `bsip2/proto_v0/src/generate_structural_report.py` | Structural class coherence report across all categories |
| `bsip2/proto_v0/src/generate_router_validation.py` | **Router v2 validation** — 163-product analysis (anchor rate, suppression, instability, v1→v2 delta) |
| `bsip2/proto_v0/src/generate_router_anchor_audit.py` | **Router v2 anchor audit** — per-term activation counts, signal-anchor agreement, override legitimacy, routing change verdicts |
| `bsip2/proto_v0/src/generate_bread_light_analysis.py` | **Bread-light stress test** — 9 analysis outputs (routing, matrix, SC, deception, fiber, seed, fermentation) |
| `bsip2/proto_v0/src/create_bread_light_corpus.py` | Generator for 32-product bread-light synthetic BSIP1 corpus |
| `bsip2/proto_v0/src/generate_run_004_reports.py` | Milk run_004 report generation |
| `bsip2/proto_v0/src/generate_visuals.py` | Visual charts generation |
| `bsip2/reporting_dashboard/` | Streamlit dashboard (6 modules: app, anomaly, compare, data_loader, viz, ui_components) |

### Centralized Reports

```
03_operations/reports/
  matrix_integrity/
    matrix_integrity_validation_001.md    ← v1 baseline (163 products)
    matrix_integrity_calibration_v2.md   ← v1 vs v2 comparison
  enrichment/
    enrichment_validation_001.md          ← BSIP1 enrichment coverage report
  regression/
    regression_check_001.md              ← Golden corpus regression check (12 structural class anchors)
    router_regression_001.md             ← Router v2 regression check (12 routing cases)
  structural_class_report_001.md         ← Structural class coherence report (163 products)
  router_validation_001.md               ← Router v2 validation (163 products; 82 anchored, 23 changes, 6 unstable)
  router_anchor_audit_001.md            ← Anchor audit (87% signal-anchor agreement; 14 clear + 7 likely improvements; 0 regressions)
  validation/                             ← (future home for cross-category validation)

02_products/bread_light/reports/
  bread_light_001_corpus_summary.md      ← Group distribution, routing overview (32 products)
  bread_light_001_routing_ambiguity.md   ← WFF contamination, beverage FP, dairy-protein FP, missing bread archetype
  bread_light_001_matrix_integrity.md    ← WG detection limits, fermentation ambiguity, additive detection
  bread_light_001_structural_class.md    ← SC distribution by group (A-F), coherence assessment
  bread_light_001_deceptive_products.md  ← Wholegrain halo, fiber laundering, seed halo, sourdough theater
  bread_light_001_coherent_products.md   ← Structurally coherent products (reference anchors)
  bread_light_001_fiber_laundering.md    ← Isolated fiber cases, engine gap, recommended fix
  bread_light_001_seed_halo.md           ← Seed position analysis, WFF routing contamination
  bread_light_001_fermentation_ambiguity.md ← Sourdough spectrum (genuine→industrial→theater), engine gaps
```

---

## governance/ — Schemas and Architecture Decisions

| File | Purpose |
|------|---------|
| `target_architecture.md` | The intended target architecture (reference) |
| `freeze_inventory.md` | Registry of all frozen framework versions |
| `governance_recommendations.md` | Governance guidelines |
| `migration_cleanup_report.md` | Record of 2026-05-20 hygiene sprint |
| `migration_execution_report.md` | Prior migration tracking |

---

## 99_archive/ — Historical and Deprecated Work

Do not edit. Read only. Preserved for traceability.

| Path | Contents |
|------|---------|
| `legacy_bsip2/matrix_integrity_v1.py` | Matrix Integrity v1 engine (superseded by v2) |
| `old_batch_runners/` | Superseded batch runners (milk v1-v3, generic batch_run, run_matrix_validation_v1) |
| `old_batch_runners/generate_cereals_001_reports.py` | Category report generators (already run) |
| `old_reports/bsip2_pre_v4_runs/` | Batch reports from scoring runs before milk run_004 |
| `deprecated_logic/` | One-off experimental / diagnostic scripts |
| `bisp2_concept_prototype/` | Original BSIP2 v0 proof-of-concept (pre-rewrite) |
| `bisp0_placeholder/` | Legacy placeholder |

---

## Key Design Invariants

1. **BSIP1 is the cross-retailer canonical layer.** Never write BSIP2 traces into BSIP1 output directories.
2. **Matrix Integrity does NOT replace NOVA.** It adds structural composition signals that NOVA cannot see.
3. **Score formula:** `100 − deg×0.55 − eng×0.30 − hp×0.15 − assembly_drag`. No nutrition panel used.
4. **All Israeli product data is Hebrew-primary.** UI language rules: `01_framework/bsip2_framework/ui_language.md`.
5. **Fermentation protects traditional foods.** live_cultures → 0.40 factor cap on degradation reduction.
6. **No category-specific hacks.** All matrix integrity logic must generalize across all categories.

---

## What Does NOT Exist Yet

- `04_frontend/` — there is no `04_frontend/` directory; the website lives at `bari-web/` (folded in as a git subtree, TASK-134, 2026-06-01). Run/modify the site there (`npm run dev` from `C:\bari\bari-web`). Milk comparison page (`/hashvaot/milk-comparison`) was the first page; handoff doc at `02_products/milk_and_alternatives/reports/cursor_handoff_milk_comparison.md`.
- Bread/crackers router archetype — bread-light stress test identified 5 routing failure modes (WFF contamination, beverage FP, dairy-protein FP, snack-bar bleed, cereal overlap). Router expansion requires dedicated `bread` and `cracker` archetypes in router_v2.py. Stress test reports: `02_products/bread_light/reports/`.
- Fermentation quality scoring — stress test confirmed engine cannot distinguish genuine sourdough from industrial sourdough-powder. Enrichment fix: flag `fermentation_quality=mixed` when מחמצת + שמרים co-appear; `fermentation_role=flavor` when sourdough percentage <10%.
