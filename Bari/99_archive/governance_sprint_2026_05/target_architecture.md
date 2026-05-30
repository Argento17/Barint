# Target Repository Architecture

**Status:** Planning document — proposed structure, not yet implemented.  
**Scope:** `C:\Bari\` complete repository reorganization.  
**Principle:** Framework documents and operational artifacts are separated. Products are organized category-first, not retailer-first.

---

## Proposed directory tree

```
C:\Bari\
├── 01_framework\                        # Design documents, architecture, theory
│   ├── bsip0_framework\                 # BSIP0 OCR and scraping design docs
│   ├── bsip1_framework\                 # BSIP1 consolidation and trust layer design
│   ├── bsip2_framework\                 # Primary BSIP2 scoring framework (from bisp2_concept_v1)
│   │   ├── *.md                         # Top-level concept documents (7 files)
│   │   ├── docs\
│   │   │   ├── scoring\                 # Scoring design documents
│   │   │   ├── positive_structure_v1\   # Positive structure architecture documents
│   │   │   └── *.md                     # Other design documents
│   │   └── validation\                  # Validation documents
│   └── freezes\                         # Immutable point-in-time snapshots
│       ├── bsip0_v0_2\                  # BSIP0 v0.2 freeze (from bsip0_scrape\bsip_freezes\)
│       └── bsip2_concept_v1_complete\   # Complete freeze of bsip2_concept_v1 (to be done)
│
├── 02_products\                         # Product data organized category-first
│   ├── snack_bars\
│   │   ├── carrefour\                   # Carrefour snack bar raw + processed data
│   │   ├── yohananof\                   # Yohananof snack bar raw + processed data
│   │   └── _consolidated\              # Cross-retailer BSIP1 outputs for snack bars
│   ├── chocolates\
│   │   ├── carrefour\
│   │   └── yohananof\
│   ├── [other_categories]\
│   └── _all_retailers\                 # Products not yet categorized or cross-category
│
├── 03_operations\                       # Operational code, scripts, run artifacts
│   ├── bsip0\
│   │   ├── pipeline\                    # OCR/image extraction (from bsip0_pipeline\)
│   │   │   ├── main.py
│   │   │   ├── extractor.py
│   │   │   ├── raw_ocr.py
│   │   │   ├── evaluate_parser.py
│   │   │   ├── azure_test.py
│   │   │   ├── data\raw\               # 10-product image test set
│   │   │   ├── outputs\                # Parsed JSON outputs
│   │   │   ├── cache\                  # OCR API response cache
│   │   │   └── ground_truth.xlsx
│   │   └── scrape\                     # Web scraper (from bsip0_scrape\)
│   │       ├── carrefour\              # Carrefour scripts + outputs
│   │       ├── yohananof\              # Yohananof scripts + outputs
│   │       └── retailer_capabilities\ # Retailer capability specs
│   ├── bsip1\
│   │   └── run_001\                    # First batch run (from bsip1_concept\batch_test_001)
│   │       ├── batch_test_001.py
│   │       └── output\                 # 53 bsip1_*.json + 53 bsip1_audit_*.json
│   └── bsip2\
│       └── proto_v0\                   # Active BSIP2 prototype (from bsip2_proto_v0\)
│           ├── src\                    # 13 Python source files
│           ├── outputs\products\       # 53 product bsip2_trace.json files
│           ├── reports\                # 8 markdown reports + diagnostic scripts
│           ├── review\                 # CSV, XLSX, HTML dashboard
│           └── visuals\               # PNG charts, CSV summaries
│
└── 99_archive\                         # Superseded work; read-only reference
    ├── bisp0_placeholder\              # The empty BISP0 directory (with note)
    └── bisp2_concept_prototype\        # Pre-v1 Python prototype (from bisp2_concept\)
        ├── *.py                        # 11 Python modules
        ├── tests\
        ├── input.xlsx
        ├── outputv3.xlsx
        ├── sample_bsip1.csv
        └── Barinew_v3.zip
```

---

## Naming conventions

### Directory naming

| Rule | Example |
|---|---|
| All lowercase | `bsip2_framework` not `BISP2_Framework` |
| Underscores, no hyphens | `proto_v0` not `proto-v0` |
| Version suffix when versioned | `proto_v0`, `bsip0_v0_2` |
| Operational runs named `run_NNN` | `run_001`, `run_002` |
| No trailing numbers on non-versioned directories | `pipeline` not `pipeline1` |

### Products: category-first organization

Products must be organized **category first, retailer second** at all levels:

```
02_products\snack_bars\carrefour\      ✓ correct
02_products\carrefour\snack_bars\      ✗ wrong — retailer-first
```

**Why category-first:** Cross-retailer analysis (BSIP1) is the primary analytical operation. When exploring a category (e.g., all snack bars), the category should be the top-level grouping. Retailer is a secondary attribute.

### Freeze naming

Freezes are named `{system}_{version}` using the system's own versioning:

```
bsip0_v0_2          ← correct (matches BSIP0's internal version label)
bsip2_concept_v1    ← correct (matches the directory being frozen)
```

---

## Freeze policy

**What a freeze is:** An immutable point-in-time snapshot of a system or framework layer. Once created, files in a freeze directory are never modified.

**What gets frozen:**
- Framework design documents at a stable milestone
- Scoring schema and constants at a release point
- BSIP0 scraper outputs at a run boundary

**What does NOT get frozen:**
- Operational run outputs (these are already immutable by virtue of being outputs)
- Active working copies
- Archive directories

**Freeze location:** All freezes live in `01_framework\freezes\`. Not inside the operational directory that generated them (the current `bsip0_scrape\bsip_freezes\` pattern is incorrect).

**Freeze completeness requirement:** A freeze must capture the complete state of the system being frozen. Partial freezes (like the current `freezes\bsip2_concept_v1\` which is missing `docs\` subdirectories and `validation\`) should be either completed or labeled `_partial` with a note explaining what is missing.

**Freeze update policy:** Freezes are never updated. If the system state changes and a new freeze is needed, create a new freeze directory with an incremented version.

---

## Archive policy

**What goes in `99_archive\`:**
- Superseded code that has been replaced by a newer implementation
- Empty directories with historical placeholders
- Work that is complete and will never be extended

**What does NOT go in `99_archive\`:**
- Paused active work (goes in `03_operations\`)
- Documents that are still referenced by active framework docs (keep in `01_framework\`)
- Freeze snapshots (go in `01_framework\freezes\`)

**Archive immutability:** Archive directories should be treated as read-only. If archived code needs to be resumed, copy it to `03_operations\` rather than extracting from archive.

---

## Outputs policy

Generated artifacts (CSVs, PNGs, HTML, XLSX) live with their generating operational system, not in a separate `outputs\` top-level directory.

```
03_operations\bsip2\proto_v0\outputs\    ← correct
03_operations\bsip2\proto_v0\visuals\    ← correct
02_outputs\bsip2\                        ← wrong — outputs separated from code
```

**Why:** When regenerating outputs, the code and its outputs should cohere. Separating them creates confusion about which outputs correspond to which code version.

---

## Run naming convention

Operational batch runs are named `run_NNN` with zero-padded integers:

```
03_operations\bsip1\run_001\    ← first BSIP1 run
03_operations\bsip1\run_002\    ← second BSIP1 run (when it happens)
```

Each run directory contains:
- The script used for that run (pinned version)
- All outputs from that run
- A `run_metadata.json` or `run_notes.md` with date, input set, and key results

---

## Framework vs Operations distinction

| Dimension | `01_framework\` | `03_operations\` |
|---|---|---|
| Content type | Design docs, architecture, theory | Code, scripts, data, run outputs |
| Audience | Anyone reasoning about the system | Anyone running or debugging the system |
| Stability | Changes slowly; major changes create freezes | Changes frequently with each run or fix |
| Version control | Document versioning (v1, v2 suffixes on directories) | Git or run-numbered directories |
| Deletion policy | Never delete; archive if superseded | Output runs can be cleaned after freeze |

---

## Current state → target state mapping summary

| Current | Target | Action |
|---|---|---|
| `bisp2_concept_v1\` | `01_framework\bsip2_framework\` | Move |
| `bsip0_scrape\bsip_freezes\bsip0_v0_2\` | `01_framework\freezes\bsip0_v0_2\` | Extract and move |
| `freezes\bsip2_concept_v1\` | `01_framework\freezes\bsip2_concept_v1_partial\` | Rename to flag as partial; create complete freeze separately |
| `bsip0_pipeline\` | `03_operations\bsip0\pipeline\` | Move |
| `bsip0_scrape\` (minus freeze) | `03_operations\bsip0\scrape\` | Move |
| `bsip1_concept\batch_test_001\` | `03_operations\bsip1\run_001\` | Move and rename |
| `bsip2_proto_v0\` | `03_operations\bsip2\proto_v0\` | Move |
| `BISP0\` | `99_archive\bisp0_placeholder\` | Move |
| `bisp2_concept\` | `99_archive\bisp2_concept_prototype\` | Move |
| `02_products\` | `02_products\` (new structure) | Create; populate from scrape outputs |
