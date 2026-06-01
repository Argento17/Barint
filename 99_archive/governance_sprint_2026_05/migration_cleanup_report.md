# Migration Cleanup Report

**Executed:** 2026-05-17 (cleanup pass following initial migration)  
**Status:** Complete — one outstanding item requires IDE close (see below)

---

## What was fixed in this pass

### 1. Ghost directory verification and disposition

**`C:\Bari\bsip0_scrape\`** and **`C:\Bari\bsip2_proto_v0\`** were confirmed as **empty ghost directories**, not failed moves:

| Directory | Files at source | Files at destination | Verdict |
|---|---|---|---|
| `bsip0_scrape\` | 0 (only empty `carrefour\` subdir) | 403 at `03_operations\bsip0\scrape\` | All files moved; container held by IDE |
| `bsip2_proto_v0\` | 0 | 107 at `03_operations\bsip2\proto_v0\` | All files moved; container held by IDE |

Removal was attempted via `cmd /c rmdir /s /q` and `Remove-Item -Recurse -Force`. Both failed with "The process cannot access the file because it is being used by another process." The `.idea\` directory confirms a JetBrains IDE has these directories in its project index and holds kernel-level handles on the directory objects even though the files inside were moved.

**No data loss. No duplication. The top-level ghost dirs are 100% empty containers.**

**Resolution (requires human action):** Close JetBrains IDE (or any application with these directories open), then run:
```powershell
Remove-Item "C:\Bari\bsip0_scrape" -Recurse -Force
Remove-Item "C:\Bari\bsip2_proto_v0" -Recurse -Force
```

### 2. Framework placeholders created

Created the missing framework stage directories and READMEs:

| Directory | Status | README contents |
|---|---|---|
| `01_framework\bsip0_framework\` | Created | Purpose, what belongs here, priority docs to write |
| `01_framework\bsip1_framework\` | Created | Trust layer overview, what belongs here, current implementation state |
| `01_framework\shared\` | Created | Cross-cutting concepts, cross-stage docs to eventually promote |
| `01_framework\README.md` | Created | Maturity table, relationship to operations |

### 3. 02_products snack_bars structure built and populated

Created full category workspace for snack bars with data populated at all available pipeline stages:

| Directory | Files | Source | Notes |
|---|---|---|---|
| `snack_bars\observations_bsip0\yohananof\` | 391 | `03_operations\bsip0\scrape\yohananof\outputs\yohananof\` | 48 barcode dirs; run artifacts |
| `snack_bars\observations_bsip0\carrefour\` | 1 (README) | — | No source data; placeholder |
| `snack_bars\canonical_bsip1\run_001\` | 108 | `03_operations\bsip1\run_001\output\` | 53 canonical + 53 audit JSONs + 2 other |
| `snack_bars\intelligence_bsip2\latest_review\` | 3 | `03_operations\bsip2\proto_v0\review\` | CSV + XLSX + HTML dashboard |
| `snack_bars\intelligence_bsip2\latest_visuals\` | 22 | `03_operations\bsip2\proto_v0\visuals\` | PNGs + CSVs |

**Note on copy vs. move:** These are copies, not moves. The operational originals remain in `03_operations\` as the canonical source. `02_products\` copies are for browsing and analysis; regenerate them by re-running the relevant scripts.

**Note on yohananof structure:** The first copy attempt produced an extra nesting level (copied `outputs\*` which included a `yohananof\` subdirectory). This was corrected: the final structure copies from `outputs\yohananof\*`, placing the 48 barcode directories directly under `observations_bsip0\yohananof\`.

### 4. 03_operations README created

`03_operations\README.md` explains the operations/products/framework distinction, directory structure, and a runbook with the correct paths for all scripts.

### 5. ARCHITECTURE.md updated

Rewrote with the four-layer mental model:
- `01_framework` = Bari Intelligence Framework
- `02_products` = Product category workspaces
- `03_operations` = Execution tools and prototypes
- `99_archive` = Historical/superseded assets

Added notes on `.claude\`, `.idea\`, `.venv\` (do not delete without explicit approval). Added full pipeline flow diagram showing BSIP0 → BSIP1 → BSIP2 and their mapping to `03_operations\` → `02_products\`.

---

## Outstanding item

| Issue | Location | Action Required | By |
|---|---|---|---|
| Ghost dirs: `bsip0_scrape\` and `bsip2_proto_v0\` | `C:\Bari\` top level | Close IDE; run `Remove-Item -Recurse -Force` on both | Human — requires IDE close |

---

## Final top-level tree

```
C:\Bari\
├── .claude\                    Claude Code project state (dev env — do not delete)
├── .idea\                      JetBrains IDE project (dev env — do not delete)
├── .venv\                      Python virtual environment (dev env — do not delete)
│
├── 01_framework\               Bari Intelligence Framework
│   ├── README.md
│   ├── bsip0_framework\        Extraction layer design (early — 1 doc)
│   ├── bsip1_framework\        Consolidation layer design (early — 1 doc)
│   ├── bsip2_framework\        Scoring layer design (developed — 30 docs)
│   ├── shared\                 Cross-cutting concepts (1 placeholder)
│   └── freezes\
│       ├── bsip0_v0_2\                      BSIP0 v0.2 milestone (10 files)
│       ├── bsip2_concept_v1_complete\        Full pre-migration snapshot (31 files)
│       └── bsip2_concept_v1_partial_early\   Historic partial freeze (10 files)
│
├── 02_products\                Category-first product workspaces (527 files)
│   ├── README.md
│   ├── golden_corpus\          (empty skeleton)
│   └── snack_bars\
│       ├── README.md
│       ├── raw_sources\carrefour\            (empty)
│       ├── raw_sources\yohananof\            (empty)
│       ├── observations_bsip0\carrefour\     (1 file — README placeholder)
│       ├── observations_bsip0\yohananof\     48 barcodes, 391 files
│       ├── canonical_bsip1\run_001\          108 files (53 canonical + 53 audit)
│       ├── intelligence_bsip2\latest_review\ 3 files (CSV + XLSX + HTML)
│       ├── intelligence_bsip2\latest_visuals\ 22 files
│       ├── reports\                          (empty)
│       └── review\                           (empty)
│
├── 03_operations\              Execution tools and prototypes (692 files)
│   ├── README.md
│   ├── bsip0\pipeline\         OCR prototype (62 files, 10 test products)
│   ├── bsip0\scrape\           Web scraper (403 files — 48 Yohananof products)
│   ├── bsip1\run_001\          First BSIP1 run (119 files)
│   └── bsip2\proto_v0\         Active scoring prototype (107 files)
│
├── 99_archive\                 Historical assets (48 files)
│   ├── bisp0_placeholder\      Empty BISP0 dir + README
│   └── bisp2_concept_prototype\ Pre-v1 Python prototype (46 files + 2 READMEs)
│
├── governance\                 Governance and migration documents (8 files)
│   ├── README.md
│   ├── migration_inventory.md
│   ├── path_mapping.csv
│   ├── target_architecture.md
│   ├── freeze_inventory.md
│   ├── governance_recommendations.md
│   ├── post_migration_path_issues.md
│   └── migration_execution_report.md
│   └── migration_cleanup_report.md  ← this file
│
├── ARCHITECTURE.md             Repository orientation document
│
│   ── Ghost dirs: empty, IDE-locked, safe to delete after IDE close ──
├── bsip0_scrape\carrefour\     EMPTY — all 403 files at 03_operations\bsip0\scrape\
└── bsip2_proto_v0\             EMPTY — all 107 files at 03_operations\bsip2\proto_v0\
```

---

## Final snack_bars product tree

```
02_products\snack_bars\
├── README.md
├── raw_sources\
│   ├── carrefour\              (empty — raw HTML not yet stored here)
│   └── yohananof\              (empty — raw HTML not yet stored here)
├── observations_bsip0\
│   ├── carrefour\              README.md explaining no data at migration time
│   └── yohananof\              48 barcode directories (391 files total)
│       ├── 7290107646826\      per-product: HTML pages + product_parsed.json
│       ├── ... (47 more)
│       ├── all_products.json
│       ├── approved_candidates.json
│       ├── audit_report.csv / .json
│       ├── candidate_review.csv / candidate_review_approved.csv
│       └── run_report.json
├── canonical_bsip1\
│   └── run_001\                108 files
│       ├── bsip1_*.json        53 canonical product records
│       └── bsip1_audit_*.json  53 trust-scoring audit trails
├── intelligence_bsip2\
│   ├── latest_review\          3 files
│   │   ├── bsip2_master_products.csv
│   │   ├── bsip2_master_products.xlsx
│   │   └── review_dashboard.html
│   └── latest_visuals\         22 files
│       ├── *.png               11 score distribution charts
│       ├── data\*.csv          6 CSV summaries
│       └── product_waterfall_examples\*.png  5 waterfall charts
├── reports\                    (empty — to be populated)
└── review\                     (empty — to be populated)
```
