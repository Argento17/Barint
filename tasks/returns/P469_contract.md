# P469 Contract — TASK-463 empty-state mitigation (expansion-section)

**Worktree:** `C:\bari_wt_t463` (branch `fix/task463-empty-state-mitigation`)
**Status proposed:** RETURNED

## Change summary

Uniform display rule in `expansion-section.tsx`: absent `limitingFactors` / `positiveSignals` data renders **nothing** — no green-check false positive, no orphan panel headers, no assessment section when both sides are empty.

- **Limiting-factors panel:** wrapped in `hasLimits`; removed empty-state branch (`CheckGlyph` + banned string).
- **Positive panel:** already gated on `hasPositives` (unchanged — no false empty-state copy existed).
- **`hasAssessment`:** now `positiveSignals.length > 0 || limitingFactors.length > 0` (was `|| expansion.limitingFactors !== undefined`, which showed the section for `[]`).
- **Grid:** `twoCol = hasPositives && hasLimits` for sane 1-col layout when only one side has items.

## Render verification (Playwright `e2e/p469-verify.spec.ts`, desktop 1280×900, fresh dev server)

| Case | Route / product | DOM assertions |
|------|-----------------|---------------|
| 1 Bread all-empty | `/hashvaot/bread` → לחם טחינה פרוס | `אין גורמים מגבילים מהותיים` count **0**; `מה מגביל את הציון?` count **0**; `הערכת המוצר` count **0** |
| 2 Cheese D all-empty | `/hashvaot/cheese` → גבינת שמנת זיתים (grade D) | banned string count **0**; limits heading count **0** |
| 3 Hummus with factors (unchanged) | `/hashvaot/hummus` → חומוס מסעדות (auto-expanded rank-1) | `מה מגביל את הציון?` count **1**; banned string count **0** |
| 4 Catalog bread | `/catalog` search → לחם טחינה פרוס expand | banned string count **0**; limits heading count **0** in expansion panel |

Command: `cd bari-web && npx playwright test e2e/p469-verify.spec.ts --project=desktop` → **exit 0** (1 passed).

## Corpus counts (trace-derived)

`npx tsx -e "import { buildInventoryProductDetails } from './src/lib/inventory/loader.ts'; …"` in `bari-web/`:

- `empty_limitingFactors`: **83/187** (catalog corpus via `buildInventoryProductDetails`)
- `empty_positiveSignals`: **84/187** (same source)
- `bread_empty_limitingFactors`: **23/23** (product id contains `bread`)
- `cheese_empty_limiting_factors`: **47/47** (product id contains `cheese`)

## Gates

| Gate | Result |
|------|--------|
| `npx eslint src/components/shared/expansion-section.tsx` | exit 0 |
| `npx tsc --noEmit` | exit 0 |
| `npm run build` | exit 0 |
| `npm run lint` (full repo) | exit 1 — **12 pre-existing errors** in unrelated files (`public/hero/tweaks-panel.jsx`, `privacy/page.tsx`, etc.); **0 errors in touched file** |

```json
{
  "task": "P469",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/components/shared/expansion-section.tsx", "action": "modified", "sha256": "e99e86b91b0eaa3e2f4c99ab8f5f23ade39884ffa48b9be6b228b5903dd4f498"}
  ],
  "counts": {
    "empty_limitingFactors_catalog_corpus": "83/187 (buildInventoryProductDetails via npx tsx loader.ts)",
    "empty_positiveSignals_catalog_corpus": "84/187 (buildInventoryProductDetails via npx tsx loader.ts)",
    "bread_empty_limitingFactors": "23/23 (buildInventoryProductDetails bread id subset; histogram: 23 empty, 0 populated)",
    "cheese_empty_limitingFactors": "47/47 (buildInventoryProductDetails cheese id subset; histogram: 47 empty, 0 populated)",
    "banned_empty_limiting_string_in_expansion_section": "0/1 (grep אין גורמים in expansion-section.tsx)",
    "render_verification_cases_pass": "4/4 (playwright e2e/p469-verify.spec.ts desktop)",
    "eslint_touched_file": "0/0 (npx eslint expansion-section.tsx exit 0)",
    "tsc_no_emit": "0/0 (npx tsc --noEmit exit 0)",
    "npm_build": "0/0 (npm run build exit 0)"
  },
  "commands_run": [
    {"cmd": "cd bari-web && npm ci", "exit_code": 0},
    {"cmd": "cd bari-web && npx eslint src/components/shared/expansion-section.tsx", "exit_code": 0},
    {"cmd": "cd bari-web && npx tsc --noEmit", "exit_code": 0},
    {"cmd": "cd bari-web && npm run build", "exit_code": 0},
    {"cmd": "cd bari-web && npm run lint", "exit_code": 1},
    {"cmd": "cd bari-web && npx tsx -e import buildInventoryProductDetails counts", "exit_code": 0},
    {"cmd": "cd bari-web && npx playwright test e2e/p469-verify.spec.ts --project=desktop", "exit_code": 0},
    {"cmd": "python 03_operations/validators/validate_return.py --md tasks/returns/P469_contract.md --root C:\\bari_wt_t463", "exit_code": 0}
  ],
  "not_done": [
    "Full-repo npm run lint exit 0 blocked by 12 pre-existing ESLint errors outside expansion-section.tsx (unchanged by this task)"
  ],
  "self_check": "Playwright 4/4 render cases pass: empty bread/cheese/catalog expansions show no banned string and no limits heading; hummus rank-1 still shows limits heading (count 1); tsc + build exit 0"
}
```

**Proposed RETURNED.** Orchestrator: verify artifact sha256, re-run playwright spot-check, confirm bread 23/23 + cheese 47/47 empty-LF counts unchanged (data fix is post-freeze).
