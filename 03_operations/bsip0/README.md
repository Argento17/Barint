# BSIP0 — Data Acquisition Layer

BSIP0 is the raw-data acquisition stage of the Bari pipeline. It produces one
JSON file per retailer per category run, containing the scraped product records
(barcode, Hebrew name, nutrition panel, ingredients, image URL, provenance tags).
These raw files feed BSIP1 enrichment and are never modified after the gate is
declared.

## Active acquisition sources (3)

Every new category run targets all three sources. See full retailer status in
`01_framework/operations/bsip0_retailer_coverage_standard_v1.md`.

| # | Retailer | Chain ID | Method | Status |
|---|---|---|---|---|
| 1 | יוחננוף (Yohananof) | 7290455000004 | Playwright storefront — product modal, "ערכים תזונתיים" tab | ✅ PRIMARY |
| 2 | ויקטורי (Victory) | 7290696200003 | Playwright storefront — same SaaS as Yohananof (CDN retailer 1470); scraper at `scrape/victory/01_acquire_victory.py` | ✅ SECONDARY |
| 3 | OFF + il_prices | — | il_prices identity feed (barcodes + names) paired with Open Food Facts nutrition panel — covers products not on Yohananof/Victory shelves or with empty modals (imported goods) | ✅ ENRICHMENT |

**Scraping stack — no Firecrawl in any production path.**
- Storefront panels: local Playwright (headless=False), no proxy needed for Yohananof/Victory
- Identity: `il_prices` feeds via laibcatalog (Yohananof/Victory/Carrefour) or chain self-hosted JSON (Shufersal)
- Nutrition enrichment: OFF API per barcode — supplements where the storefront modal is empty
- Blocked retailers (Shufersal, Carrefour, Rami-Levi): il_prices identity available; storefront blocked by WAF/TLS fingerprinting; documented in category READMEs, never silently skipped

## Directory structure

```
bsip0/
├── acquisition_v2/          Prototype acquisition scripts (v2)
├── acquisition_v3/          Active multi-retailer acquisition + composition gate
├── pipeline/                OCR/image-extraction prototype (Azure Vision)
├── scrape/                  Per-category retailer scrapers
│   ├── _shared/             Shared modules (bsip0_nutrition.py, grade_governance.py)
│   ├── multiretailer_*/     Multi-retailer acquisition pipelines (il_prices + OFF)
│   ├── victory/             Victory storefront scraper (source 2)
│   ├── shufersal_*/         Shufersal-specific scrapers by category
│   ├── yohananof_*/         Yohananof-specific scrapers by category
│   └── ...
├── tests/                   Legacy test files
└── validators/              QA gate validator module (TASK-218)
    ├── bsip0_qa_validator.py   THE single source of truth for BSIP0 gate checks
    └── test_bsip0_qa_validator.py
```

## Gate Contract

Every BSIP0 run must pass all six quality checks defined in
`validators/bsip0_qa_validator.py` before the gate is declared PASS: (1) no
fabrication signatures — round-hour timestamps spanning multiple retailers or
byte-identical nutrition dicts across retailers both constitute hard FAILs;
(2) portal availability confirmed for all scrape targets before the run starts
— if any target is DOWN or MAINTENANCE the run aborts, no data is written, and
no gate status is recorded; (3) every scraped product page must pass a barcode
or keyword identity check before its record is accepted, preventing wrong-card
captures; (4) every product must match the category's positive-type list and
match none of its negative-type list, with all boundary-rejected products
logged explicitly; (5) the packaged frontend JSON must be scanned for forbidden
framework terms (NOVA, BSIP, cap, floor, structural_class, matrix_integrity,
pillar, dimension, nova_level, nova_proxy) in the `positiveSignals`,
`limitingFactors`, and `insightLine` fields — any hit is a hard FAIL and the
file must not be deployed; (6) the run summary must include all five mandatory
fields (`scrape_success_rate`, `source_verified`, `null_imageUrl_rate`,
`scope_rejected_count`, `portal_availability`) and must meet the threshold rules
(`scrape_success_rate >= 0.70`, `source_verified = true`). An acknowledged W001
warning does not constitute a conditional pass — a warning that is acknowledged
and then ignored is treated as a FAIL. The validator module at
`validators/bsip0_qa_validator.py` is the single source of truth; scrapers
import and call it, they do not re-implement checks locally. Scrapers that
attempt to record a PASS status with unresolved FAILs must raise
`GateSelfPassError`.

## Running the tests

```powershell
# From C:\Bari — activate venv first
.venv\Scripts\Activate.ps1
$env:PYTHONIOENCODING = "utf-8"
python 03_operations\bsip0\validators\test_bsip0_qa_validator.py
```

All 22 tests should pass in under 1 second (no network calls in the test suite).
