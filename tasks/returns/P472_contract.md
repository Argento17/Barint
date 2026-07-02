# P472 Contract — TASK-465 catalog dashboard redesign (PowerBI-grade /catalog)

**Worktree:** `C:\bari_wt_t465` (branch `feat/task465-catalog-dashboard`)
**Status proposed:** RETURNED

## Summary

Redesigned the public `/catalog` page into a sharp data-dashboard layout: KPI header strip (live-derived counts + grade distribution bar), professional filter toolbar, and dense spreadsheet-style data grid with sticky header and score column. All KPI numbers computed at render time from `buildInventoryRows` output — zero hardcoded stats. No loader/data changes; expansion panels unchanged.

## Component inventory

| File | Action | SHA256 |
|------|--------|--------|
| `bari-web/src/components/inventory/catalog-dashboard-metrics.ts` | created | `637c8fb1828081f2c387fa396d3eb7d336e4306fc1842ae5e009f38ebfca41d9` |
| `bari-web/src/components/inventory/catalog-kpi-strip.tsx` | created | `066368ccb40685f527c5bfab2ea0b2f07850535998b27bb821ebe36ae0624663` |
| `bari-web/src/app/catalog/_catalog-client.tsx` | modified | `761441e406b4045edd32e6c7c8e52463af759991a27aa37334b8e57fd2b94ffb` |
| `bari-web/src/components/inventory/product-table.tsx` | modified | `c9f3f4572a80cb72c0f620567442e00a400a0ba63c4752bc0b80bd97d837dbda` |
| `tasks/returns/P472_screens/catalog-desktop-1280.png` | created | `6e198b590aca4f3492ee7e073dfce5d60f5e0f6ba65e24e1fc1b69541f45b79b` |
| `tasks/returns/P472_screens/catalog-mobile-390.png` | created | `5895b505c958ee2b5a3d6f32e023ac81cb460d7bbb563b71e82aa85c5dd5068d` |

## New consumer strings (verbatim — content two-gate pending)

1. `סה״כ מוצרים` — KPI card label (total products)
2. `קטגוריות` — KPI card label (category count)
3. `מוצרים עם ציון` — KPI card label (scored products)
4. `ללא ציון` — KPI card sub-label when unscored count > 0
5. `נתונים מלאים` — KPI card label (verified-confidence share)
6. `מוצרים` — KPI card sub-label suffix for verified count (e.g. "97 מוצרים")
7. `פילוח לפי דרגה` — grade distribution bar section label
8. `ללא` — grade bar legend label for unscored segment (only when unscored > 0)

Reused existing strings: `קטלוג המוצרים`, `כל המוצרים`, filter placeholders, column headers, `N מוצרים` result readout (shortened from prior `N מוצרים מוצגים`).

## KPI verification (independent vs rendered page)

Independent derivation (`npx tsx bari-web/scripts/p472-kpi-verify.mts` against live registry):

| Metric | Value |
|--------|------:|
| totalProducts | 187 |
| categoryCount | 7 |
| grade A/B/C/D/E | 15 / 49 / 64 / 41 / 18 |
| unscored | 0 |
| verified (full data) | 97 |
| fullDataPercent | 52% |

Cross-check vs `buildInventorySummary(rows)`: totalProducts, categoryCount, gradeDistribution all **match** (187/187 registry rows; histogram A:15 B:49 C:64 D:41 E:18 unscored:0; most_common grade C count 64).

## Bundle / dependency delta

- **New npm dependencies:** 0 (no `package.json` / lockfile changes)
- **Net catalog source delta:** −4,047 chars vs `origin/master` (client slimmed; +2 new components; product-table dashboard styling)
- **Server `/catalog` build output:** 26,401 bytes (`.next/server/app/catalog/` post-build)

## Gate results

| # | Gate | Command | Exit |
|---|------|---------|-----:|
| 1 | lint | `npm run lint` (bari-web) | 0 |
| 2 | tsc | `npx tsc --noEmit` (bari-web) | 0 |
| 3 | build | `npm run build` (bari-web) — `/catalog` listed as `ƒ` dynamic route | 0 |
| 4 | render | Playwright full-page screenshots desktop 1280px + mobile 390px | 0 |
| 5 | self-gate | `python 03_operations/validators/validate_return.py --md tasks/returns/P472_contract.md --root C:\bari_wt_t465` | (run below) |

## Screenshot paths

- `tasks/returns/P472_screens/catalog-desktop-1280.png`
- `tasks/returns/P472_screens/catalog-mobile-390.png`

```json
{
  "task": "P472",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/components/inventory/catalog-dashboard-metrics.ts", "action": "created", "sha256": "637c8fb1828081f2c387fa396d3eb7d336e4306fc1842ae5e009f38ebfca41d9"},
    {"path": "bari-web/src/components/inventory/catalog-kpi-strip.tsx", "action": "created", "sha256": "066368ccb40685f527c5bfab2ea0b2f07850535998b27bb821ebe36ae0624663"},
    {"path": "bari-web/src/app/catalog/_catalog-client.tsx", "action": "modified", "sha256": "761441e406b4045edd32e6c7c8e52463af759991a27aa37334b8e57fd2b94ffb"},
    {"path": "bari-web/src/components/inventory/product-table.tsx", "action": "modified", "sha256": "c9f3f4572a80cb72c0f620567442e00a400a0ba63c4752bc0b80bd97d837dbda"},
    {"path": "tasks/returns/P472_screens/catalog-desktop-1280.png", "action": "created", "sha256": "6e198b590aca4f3492ee7e073dfce5d60f5e0f6ba65e24e1fc1b69541f45b79b"},
    {"path": "tasks/returns/P472_screens/catalog-mobile-390.png", "action": "created", "sha256": "5895b505c958ee2b5a3d6f32e023ac81cb460d7bbb563b71e82aa85c5dd5068d"}
  ],
  "counts": {
    "catalog_products_total": "187/187 (buildInventoryRows registry corpus)",
    "catalog_categories": "7/7 (listComparisonCategoryIds registry)",
    "grade_distribution": "A:15 B:49 C:64 D:41 E:18 unscored:0 /187 (buildInventoryRows; histogram; most_common C count 64)",
    "verified_full_data_products": "97/187 (row.confidence===verified; 52%)",
    "kpi_metrics_match_summary": "3/3 (totalProducts, categoryCount, gradeDistribution vs buildInventorySummary)",
    "lint_errors": "0/0 (npm run lint bari-web; 18 baseline warnings unchanged)",
    "npm_new_dependencies": "0/0 (package.json unchanged)",
    "render_screenshots": "2/2 (Playwright full-page desktop 1280 + mobile 390)"
  },
  "commands_run": [
    {"cmd": "cd bari-web && npm ci", "exit_code": 0},
    {"cmd": "cd bari-web && npm run lint", "exit_code": 0},
    {"cmd": "cd bari-web && npx tsc --noEmit", "exit_code": 0},
    {"cmd": "cd bari-web && npm run build", "exit_code": 0},
    {"cmd": "cd bari-web && npx tsx scripts/p472-kpi-verify.mts", "exit_code": 0},
    {"cmd": "cd bari-web && node scripts/p472-screenshot.mjs", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "KPI strip on /catalog shows 187 products, 7 categories, grade bar A15/B49/C64/D41/E18, 52% full-data — matches independent npx tsx scripts/p472-kpi-verify.mts output against buildInventoryRows (187/187 registry rows)."
}
```
