# 02_products — Bari Product Dataset

This directory is the category-first product data store for the Bari project.

## Organization principle

Products are organized **category-first, then retailer**:

```
02_products\
├── snack_bars\
│   ├── carrefour\      ← Carrefour snack bar data
│   ├── yohananof\      ← Yohananof snack bar data
│   └── _consolidated\  ← Cross-retailer BSIP1 outputs
├── golden_corpus\      ← Hand-curated reference products for scoring validation
└── [other_categories]\ ← Added as categories are scraped
```

**Why category-first:** Cross-retailer analysis (BSIP1) is the primary analytical operation. When exploring a category, the category is the natural top-level grouping. Retailer is a secondary attribute.

## Current status

Skeleton created 2026-05-17. Not yet populated.

Product scrape outputs currently live in:
- `03_operations\bsip0\scrape\yohananof\outputs\` — Yohananof product data (50+ products)
- `03_operations\bsip0\scrape\carrefour\` — Carrefour product data (empty at migration time)

Scored product traces live in:
- `03_operations\bsip2\proto_v0\outputs\products\` — 53 BSIP2-scored product directories

## Population plan

When populating `02_products`, copy (do not move) from the scrape outputs, organizing by category first. Categories should be determined from the product data or the `bsip2_proto_v0` category classifier.

Do not reorganize product data here until the category classification is stable.
