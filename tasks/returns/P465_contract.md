# P465 Contract — TASK-462 CI green sweep, part 2: ESLint exit 0 in bari-web

**Worktree:** `C:\bari_wt_t462b` (branch `ci/task462-green-eslint`)
**Status proposed:** RETURNED

## Summary

Fixed all 12 ESLint errors blocking `npm run lint` in `bari-web/` with minimal, behavior-preserving changes. No global eslint config edits, no dependency changes, no eslint-disable debt added. Warnings (17) remain and do not fail the gate.

## Error census (before)

| rule | count |
|------|------:|
| `@typescript-eslint/no-explicit-any` | 1 |
| `@typescript-eslint/no-this-alias` | 1 |
| `react-hooks/refs` | 4 |
| `react/no-unescaped-entities` | 4 |
| `react-hooks/set-state-in-effect` | 2 |
| **total errors** | **12** |

Source: `npm run lint` in `bari-web/` (captured to `tasks/returns/P465_lint_before.txt`).

## Fix census by strategy

| strategy | fixed | denominator |
|----------|------:|-------------|
| typed (`GeometryEntry` union) | 1 | 1 `@typescript-eslint/no-explicit-any` |
| escaped (`&apos;` / `&quot;`) | 4 | 4 `react/no-unescaped-entities` |
| refactored (arrow fns, lazy `useState`, remove ref-from-render, `useLayoutEffect` sync) | 7 | 7 remaining errors (1 alias + 4 refs + 2 set-state-in-effect) |
| disabled-with-tag | 0 | 0 |

## eslint-disable additions

None.

## Gate outputs

| # | command | exit |
|---|---------|-----:|
| 1 | `npm run lint` (in `bari-web/`) | 0 |
| 2 | `npx tsc --noEmit` (in `bari-web/`) | 0 |
| 3 | `npm run build` (in `bari-web/`) | 0 |
| 4 | `git diff --stat` (repo root) | touches only 8 lint-error files |

Build route list: **unchanged** vs pre-change capture (`tasks/returns/P465_routes_before.txt` vs `P465_routes_after.txt`, byte-identical).

## Files changed

| file | action |
|------|--------|
| `bari-web/e2e/vision-probe.spec.ts` | modified — typed geometry entry |
| `bari-web/public/hero/plant.js` | modified — arrow handlers (no-this-alias) |
| `bari-web/public/hero/tweaks-panel.jsx` | modified — refs-during-render fixes |
| `bari-web/src/app/privacy/page.tsx` | modified — entity escape x2 |
| `bari-web/src/app/terms/page.tsx` | modified — entity escape x1 |
| `bari-web/src/components/blog/olive-oil-transparency-matrix.tsx` | modified — entity escape x1 |
| `bari-web/src/components/shared/consent-manager.tsx` | modified — lazy init banner view |
| `bari-web/src/components/shared/ga4-script.tsx` | modified — lazy init granted state |

```json
{
  "task": "P465",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/e2e/vision-probe.spec.ts", "action": "modified", "sha256": "538114f15ebb0ef6a920da800908e4e494b1908ad67a1d73deb599290c0b254d"},
    {"path": "bari-web/public/hero/plant.js", "action": "modified", "sha256": "89c2aad180d0541603efab6bceb00ba01c5042c0a6530ac621e214e15859754e"},
    {"path": "bari-web/public/hero/tweaks-panel.jsx", "action": "modified", "sha256": "3cafec30e10387ac8644e382b8bbe22501829beba9a24f28ef725553531cd8b7"},
    {"path": "bari-web/src/app/privacy/page.tsx", "action": "modified", "sha256": "6d5e61cc10bfa73469b478174e13ea5bdc4649abaa7d4ef907f29b29b8d71570"},
    {"path": "bari-web/src/app/terms/page.tsx", "action": "modified", "sha256": "59b23e1ef4ef0353e3cd7df4f8a24dc0b9669b5870038779081a5ced0492b858"},
    {"path": "bari-web/src/components/blog/olive-oil-transparency-matrix.tsx", "action": "modified", "sha256": "56f75dfb0c42143cb6debed853180346ff7422a17479b4f14f6ba494de07b6b0"},
    {"path": "bari-web/src/components/shared/consent-manager.tsx", "action": "modified", "sha256": "d9a46655595a38dadf26ec1976e18dfb13235046bf11993abe06e3354e605f94"},
    {"path": "bari-web/src/components/shared/ga4-script.tsx", "action": "modified", "sha256": "399d1521a5c4b061acbbf82edefc5c6b3622fb924c297ab53b97bee10af35e44"}
  ],
  "counts": {
    "eslint_errors_before": "12/12 (npm run lint in bari-web/; histogram: no-explicit-any(1), no-this-alias(1), react-hooks/refs(4), no-unescaped-entities(4), set-state-in-effect(2); most_common react-hooks/refs(4))",
    "eslint_errors_after": "0/12 (npm run lint in bari-web/; 17 warnings remain, 0 errors)",
    "fixes_typed": "1/1 (no-explicit-any in e2e/vision-probe.spec.ts)",
    "fixes_escaped": "4/4 (react/no-unescaped-entities in privacy, terms, olive-oil-transparency-matrix)",
    "fixes_refactored": "7/7 (plant.js, tweaks-panel.jsx, consent-manager.tsx, ga4-script.tsx)",
    "fixes_disabled_with_tag": "0/0 (no eslint-disable additions)",
    "build_routes_unchanged": "1/1 (P465_routes_before.txt vs P465_routes_after.txt byte-identical)",
    "git_diff_scope": "8/8 (git diff --stat files all had lint errors)"
  },
  "commands_run": [
    {"cmd": "npm ci (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run lint (in bari-web/)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run build (in bari-web/)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P465_contract.md --root C:\\bari_wt_t462b", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "npm run lint in bari-web/ exits 0 with 0 errors (12/12 prior errors fixed); build route list unchanged"
}
```
