# Bari Repository Architecture

**Last updated:** 2026-05-17

---

## Mental model

```
01_framework   =  Bari Intelligence Framework
                  Design docs, architecture, scoring theory, concept definitions.
                  Describes what the system does and why.

02_products    =  Product Category Workspaces
                  Category-organized product data: raw sources, parsed observations,
                  canonical records, scored outputs, review dashboards.
                  This is where you go to look at a product or category.

03_operations  =  Execution Tools and Prototypes
                  Scrapers, OCR pipelines, batch scripts, scoring engines.
                  This is where you go to run or modify a process.

99_archive     =  Historical and Superseded Assets
                  Old prototypes and abandoned experiments. Read-only reference.
```

---

## Top-level structure

```
C:\Bari\
├── 01_framework\       Bari Intelligence Framework
├── 02_products\        Category-first product workspaces
├── 03_operations\      Execution tools and prototypes
├── 99_archive\         Historical/superseded assets
├── governance\         Repository governance and migration documents
├── ARCHITECTURE.md     This file
│
│   ── Development environment folders (do not delete without explicit approval) ──
├── .claude\            Claude Code project state
├── .idea\              JetBrains IDE project files
└── .venv\              Python virtual environment (C:\Bari\.venv)
```

`.claude\`, `.idea\`, and `.venv\` are development environment folders, not part of Bari data architecture. They should not be deleted, moved, or reorganized unless explicitly approved. The `.venv\` Python environment is shared by all operational scripts.

---

## 01_framework — Bari Intelligence Framework

Design documents, architecture decisions, and scoring theory for all BSIP pipeline stages. No code, no run artifacts.

```
01_framework\
├── README.md
├── bsip0_framework\    Extraction layer design (early — see README for what to write)
├── bsip1_framework\    Consolidation layer design (early — see README for what to write)
├── bsip2_framework\    Scoring layer design (developed — 30 documents)
│   ├── docs\
│   │   ├── scoring\               Core scoring design
│   │   └── positive_structure_v1\ Positive structure architecture (6 docs)
│   └── validation\                Validation documents
├── shared\             Cross-cutting concepts (signal taxonomy, category taxonomy, glossary)
└── freezes\            Immutable point-in-time snapshots
    ├── bsip0_v0_2\                        BSIP0 scraper v0.2 milestone
    ├── bsip2_concept_v1_complete\         Full framework snapshot (pre-migration 2026-05-17)
    └── bsip2_concept_v1_partial_early\    Superseded early partial snapshot
```

---

## 02_products — Product Category Workspaces

Products are organized **category-first, retailer-second.** Each category is a self-contained workspace with its own pipeline stages: raw sources → BSIP0 observations → BSIP1 canonical records → BSIP2 intelligence.

```
02_products\
├── README.md
├── snack_bars\                      Current active category (53 products, fully scored)
│   ├── raw_sources\carrefour\       Raw HTML/images from Carrefour (not yet populated)
│   ├── raw_sources\yohananof\       Raw HTML/images from Yohananof (not yet populated)
│   ├── observations_bsip0\carrefour\ BSIP0-parsed Carrefour observations (empty)
│   ├── observations_bsip0\yohananof\ BSIP0-parsed Yohananof: 48 barcodes, 391 files
│   ├── canonical_bsip1\run_001\     53 canonical + 53 audit JSONs from BSIP1 run 001
│   ├── intelligence_bsip2\
│   │   ├── latest_review\           Review dashboard (CSV + XLSX + HTML, 53 products)
│   │   └── latest_visuals\          Score charts + waterfall plots (22 files)
│   ├── reports\                     (to be populated)
│   ├── review\                      (to be populated)
│   └── README.md
└── golden_corpus\                   Hand-curated validation products (skeleton)
```

**Category-first principle:** When adding a new category (e.g., chocolates), create `02_products\chocolates\` before organizing by retailer.

---

## 03_operations — Execution Tools and Prototypes

Code, scripts, run artifacts, caches. The factory that produces product data. See `03_operations\README.md` for runbook.

```
03_operations\
├── README.md
├── bsip0\
│   ├── pipeline\   OCR/image extraction prototype (10-product test set)
│   └── scrape\     Web scraper — Carrefour + Yohananof (48 Yohananof products)
├── bsip1\
│   └── run_001\    First BSIP1 run — 53 products consolidated and trust-scored
└── bsip2\
    └── proto_v0\   Active BSIP2 scoring prototype — 53 products graded
        ├── src\    13 Python source files
        ├── outputs\products\   53 bsip2_trace.json files
        ├── reports\
        ├── review\
        └── visuals\
```

---

## 99_archive — Historical and Superseded Assets

Read-only. Do not modify. Copy to `03_operations\` if archived code needs to be resumed.

```
99_archive\
├── bisp0_placeholder\          Empty BISP0 dir (uppercase naming, abandoned)
└── bisp2_concept_prototype\    Pre-v1 Python scoring prototype (superseded by proto_v0)
    ├── bsip2_*.py              11 Python modules
    ├── tests\                  9 test files (golden products, concern coordinator)
    └── ...
```

---

## Pipeline flow

```
BSIP0                BSIP1                    BSIP2
Extraction  ──────►  Cross-retailer  ──────►  Scoring + Grading
(scrape/OCR)         consolidation            + Explanation
     │                    │                        │
03_operations\       03_operations\           03_operations\
bsip0\               bsip1\                   bsip2\
     │                    │                        │
     ▼                    ▼                        ▼
02_products\         02_products\             02_products\
observations_bsip0\  canonical_bsip1\         intelligence_bsip2\
```

---

## Conventions

- **Lowercase underscores** for all directory names
- **Version suffix** on versioned dirs (`proto_v0`, `bsip0_v0_2`, `positive_structure_v1`)
- **Category-first** in `02_products\` — never retailer-first
- **Freezes** are immutable; live in `01_framework\freezes\`; always include `freeze_metadata.md`
- **Copies in `02_products`** are derived from `03_operations` originals — regenerate by re-running the relevant script
- **Do not delete `.claude\`, `.idea\`, `.venv\`** without explicit approval

See `governance\target_architecture.md` for full naming and policy details.
