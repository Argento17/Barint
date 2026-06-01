# 03_operations — Execution Tools and Prototypes

Operations contains the execution machinery of the Bari system: scrapers, OCR pipelines, batch scripts, scoring prototypes, dashboards, and generated run artifacts.

## How operations relates to the rest of the repository

| Layer | Purpose | What it contains |
|---|---|---|
| `01_framework\` | *Why* — intelligence design | Design docs, architecture, scoring theory |
| `02_products\` | *What* — curated product data | Category-organized product observations, canonical records, scored outputs |
| `03_operations\` | *How* — execution machinery | Code, scripts, run artifacts, caches, generated files |
| `99_archive\` | *History* — superseded work | Old prototypes, abandoned experiments |

**Operations is not the source of truth for product data** — it is the factory that produces product data. Curated product data lives in `02_products\`. When you want to look at a product's score, go to `02_products\`. When you want to re-run the scoring pipeline, go to `03_operations\`.

## Structure

```
03_operations\
├── bsip0\
│   ├── pipeline\   OCR/image extraction prototype
│   │   ├── *.py               5 Python scripts (main, extractor, raw_ocr, evaluate_parser, azure_test)
│   │   ├── data\raw\          10-product test set (40 images + ground_truth.xlsx)
│   │   ├── outputs\           10 parsed JSON outputs
│   │   └── cache\             OCR API response cache (avoid re-billing on re-runs)
│   └── scrape\     Retailer web scraper
│       ├── carrefour\         Carrefour pipeline (empty outputs at migration time)
│       ├── yohananof\         Yohananof pipeline + 48-product outputs
│       └── retailer_capabilities\   Retailer capability YAML specs
│
├── bsip1\
│   └── run_001\    First BSIP1 cross-retailer consolidation run
│       ├── batch_test_001.py  Run script (paths updated post-migration)
│       ├── output\            53 bsip1_*.json + 53 bsip1_audit_*.json
│       └── reports\           Run report
│
└── bsip2\
    └── proto_v0\   Active BSIP2 scoring prototype
        ├── src\               13 Python source files
        │   ├── score_engine.py    Core scoring pipeline
        │   ├── batch_run.py       Batch processing entry point
        │   ├── generate_review.py Dashboard generator
        │   ├── generate_visuals.py Chart generator
        │   └── ...
        ├── outputs\products\  53 product bsip2_trace.json files (one per product)
        ├── reports\           8 markdown analysis reports
        ├── review\            CSV + XLSX + HTML review dashboard
        └── visuals\           PNG score charts + CSV summaries
```

## Running scripts

All scripts use absolute paths updated to the post-migration layout. Before running any script, ensure you are using the `.venv` at `C:\Bari\.venv`.

```powershell
# Activate venv (from C:\Bari)
.venv\Scripts\Activate.ps1

# Re-run BSIP2 scoring (all products)
python 03_operations\bsip2\proto_v0\src\batch_run.py

# Regenerate review dashboard
python 03_operations\bsip2\proto_v0\src\generate_review.py

# Regenerate visuals
python 03_operations\bsip2\proto_v0\src\generate_visuals.py
```

## Key path dependencies

| Script | Reads from | Writes to |
|---|---|---|
| `bsip2\proto_v0\src\batch_run.py` | `bsip1\run_001\output\` | `bsip2\proto_v0\outputs\`, `reports\` |
| `bsip2\proto_v0\src\generate_review.py` | `bsip2\proto_v0\outputs\products\` | `bsip2\proto_v0\review\` |
| `bsip2\proto_v0\src\generate_visuals.py` | `bsip2\proto_v0\outputs\products\` | `bsip2\proto_v0\visuals\` |
| `bsip1\run_001\batch_test_001.py` | `bsip0\scrape\` | `bsip1\run_001\output\` |
