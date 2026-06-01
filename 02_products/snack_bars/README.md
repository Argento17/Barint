# Snack Bars — Product Workspace

This directory is the category workspace for snack bar products across all retailers.

## Directory structure

```
snack_bars\
├── raw_sources\             Raw retailer data (HTML, images) before any BSIP processing
│   ├── carrefour\           Carrefour raw product pages (not yet populated)
│   └── yohananof\           Yohananof raw product pages (not yet populated)
│
├── observations_bsip0\      BSIP0-parsed structured observations, one dir per barcode
│   ├── carrefour\           Carrefour (empty — no output at migration time)
│   └── yohananof\           48 barcode directories with parsed JSON + HTML; run artifacts
│
├── canonical_bsip1\         Cross-retailer consolidated canonical product records
│   └── run_001\             53 bsip1_*.json (canonical) + 53 bsip1_audit_*.json (trust)
│
├── intelligence_bsip2\      BSIP2 scored products and review artifacts
│   ├── latest_review\       Review dashboard: CSV, XLSX, HTML (53 products; copied from proto_v0)
│   └── latest_visuals\      Score charts, waterfall plots, CSV summaries (22 files)
│
├── reports\                 Analysis reports for this category (to be populated)
├── review\                  Additional review artifacts (to be populated)
└── README.md                This file
```

## Current dataset

| Stage | Source | Products | Status |
|---|---|---|---|
| BSIP0 (Yohananof) | `observations_bsip0\yohananof\` | 48 barcodes | Complete |
| BSIP0 (Carrefour) | `observations_bsip0\carrefour\` | 0 | Scraper output was empty |
| BSIP1 | `canonical_bsip1\run_001\` | 53 canonical + 53 audit | Complete |
| BSIP2 | `intelligence_bsip2\latest_review\` | 53 scored | Complete |

## Data flow

```
raw_sources\ → observations_bsip0\ → canonical_bsip1\ → intelligence_bsip2\
  (HTML/img)     (structured JSON)     (merged record)     (scored + graded)
```

## Notes

- `intelligence_bsip2\latest_review\` and `latest_visuals\` are copies of the current proto_v0 outputs. The originals remain in `03_operations\bsip2\proto_v0\review\` and `visuals\`. Update these by re-running generate_review.py and generate_visuals.py from the proto_v0 source.
- `canonical_bsip1\run_001\` is a copy of `03_operations\bsip1\run_001\output\`. The canonical source of truth for BSIP1 outputs is in `03_operations\`.
