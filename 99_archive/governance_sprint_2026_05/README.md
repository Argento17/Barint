# Governance

This directory contains repository governance and migration planning documents for the Bari project.

## Documents

| File | Purpose |
|---|---|
| `migration_inventory.md` | Full audit of all source directories — status, classification, clutter, anomalies |
| `path_mapping.csv` | Row-by-row mapping of current paths to proposed new paths |
| `target_architecture.md` | Proposed directory tree, naming conventions, freeze/archive/outputs policies |
| `freeze_inventory.md` | All detected freezes with completeness assessment and creation recommendations |
| `governance_recommendations.md` | Two-phase migration plan, risk register, and what NOT to do |
| `post_migration_path_issues.md` | Hardcoded path references found in code after migration (populated by path safety check) |
| `migration_execution_report.md` | Final report: what was moved, frozen, archived, and any unresolved issues |

## Migration status

| Phase | Status |
|---|---|
| Phase 1 — Freeze and archive | Complete (2026-05-17) |
| Phase 2 — Move active directories | Complete (2026-05-17) |
| 02_products population | Pending — skeleton created; product data not yet reorganized |

## Governance principle

Framework documents live in `01_framework\`.  
Product data lives in `02_products\` organized category-first (not retailer-first).  
Operational code and run artifacts live in `03_operations\`.  
Superseded or inactive work lives in `99_archive\`.  

See `target_architecture.md` for full conventions.
