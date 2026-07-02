# P463 Contract — catalog branch merge resolution (origin/master into golive/catalog-task458)

**Worktree:** `C:\bari_wt_t458` (branch `golive/catalog-task458`)
**Status proposed:** RETURNED
**Merge commit:** `99576c32fcbda9fe54e608184d1db7d07f79b4c4`

## Resolution rule applied

Master Hebrew copy wins; branch OG/metadata helper structure wins (`withComparisonOpenGraph` / `*ComparisonMetadata` exports).

## Per-file resolution

| File | OG structure (branch) | Hebrew copy (master) |
|------|----------------------|----------------------|
| `bari-web/src/app/hashvaot/breakfast-cereals/page.tsx` | `export const metadata = cerealsComparisonMetadata` (helper from page-data) | Strings live in auto-merged `cereals-page-data.ts` (`20 מוצרי דגני בוקר`) |
| `bari-web/src/app/hashvaot/cakes/page.tsx` | `withComparisonOpenGraph({...})` inline | `62 עוגות` description (was 65 on branch) |
| `bari-web/src/app/hashvaot/juices/page.tsx` | `export const metadata = juicesComparisonMetadata` (helper from page-data) | Strings live in auto-merged `juices-page-data.ts` (`17 מיצים`) |
| `bari-web/src/lib/comparisons/crackers-page-data.ts` | `crackersComparisonMetadata = withComparisonOpenGraph({...})` | `19 קרקרים` description (was עשרים on branch) |

## Verification outputs

1. **Conflict markers:** `git grep -l "<<<<<<<" -- bari-web/src` → empty (no markers in source).
2. **Banned strings:** `38 פרמטרים` → 0 hits repo-wide in `bari-web/src`. Literal spec grep `38 פרמטרים\|655` on full `bari-web/src` → 11 hits, all hash/barcode/id false positives (e.g. `_hash_no_rank`, barcode `4820180816552`); **0/4 hits in the four resolved conflict files**.
3. **OG helpers:** all four files import/use branch helpers — breakfast-cereals `cerealsComparisonMetadata`, cakes `withComparisonOpenGraph`, juices `juicesComparisonMetadata`, crackers `withComparisonOpenGraph`.
4. **TypeScript:** `npx tsc --noEmit` in `bari-web/` → exit 0.
5. **Build:** `npm run build` in `bari-web/` → exit 0; `/catalog` route present (`.next/server/app/catalog/page.js`).
6. **Push:** branch pushed to `origin/golive/catalog-task458` (updates PR).

```json
{
  "task": "P463",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/app/hashvaot/breakfast-cereals/page.tsx", "action": "modified", "sha256": "857d04e27c3aa1fa270ba90cc2bb4052eaff7248011d9938864afa799fa330e3"},
    {"path": "bari-web/src/app/hashvaot/cakes/page.tsx", "action": "modified", "sha256": "1d644c8e78cacd07391d028ca41771229a35b98d01bf3c7ed2f91945a3a996db"},
    {"path": "bari-web/src/app/hashvaot/juices/page.tsx", "action": "modified", "sha256": "e9f9eb223f788d062ccf3b473705e19fa0d1213a86aa3db0936ddeedec932159"},
    {"path": "bari-web/src/lib/comparisons/crackers-page-data.ts", "action": "modified", "sha256": "7a2afc98dfd900bccf812f001d42bfae7c1b5d2cfbc0b959e4ede7bbb854049a"}
  ],
  "counts": {
    "merge_conflicts_resolved": "4/4 (git merge origin/master content conflicts in P463 file list)",
    "conflict_markers_in_bari_web_src": "0/4 (git grep <<<<<<< -- bari-web/src; 4 conflict files checked)",
    "banned_38_parametrim_in_bari_web_src": "0/N (git grep 38 פרמטרים -- bari-web/src; N=consumer-facing ts/tsx/json corpus)",
    "banned_pattern_hits_in_4_resolved_files": "0/4 (git grep 38 פרמטרים|655 on 4 resolved paths only)",
    "og_helper_usage_in_resolved_files": "4/4 (cerealsComparisonMetadata, withComparisonOpenGraph x2, juicesComparisonMetadata)",
    "tsc_no_emit": "0/0 (npx tsc --noEmit exit 0; no errors reported)",
    "npm_build": "0/0 (npm run build exit 0; catalog route in .next/server/app/catalog)"
  },
  "commands_run": [
    {"cmd": "git fetch origin", "exit_code": 0},
    {"cmd": "git merge origin/master", "exit_code": 1},
    {"cmd": "git grep -l \"<<<<<<<\" -- bari-web/src", "exit_code": 1},
    {"cmd": "git grep -n \"38 פרמטרים\" -- bari-web/src", "exit_code": 1},
    {"cmd": "cd bari-web && npx tsc --noEmit", "exit_code": 0},
    {"cmd": "cd bari-web && npm run build", "exit_code": 0},
    {"cmd": "git commit -m \"Merge origin/master into golive/catalog-task458\"", "exit_code": 0},
    {"cmd": "python 03_operations/validators/validate_return.py --md tasks/returns/P463_contract.md --root C:\bari_wt_t458", "exit_code": 0},
    {"cmd": "git push origin golive/catalog-task458", "exit_code": 0}
  ],
  "not_done": [
    "PR merge (owner clicks)"
  ],
  "self_check": "4/4 merge conflicts resolved under master-copy/branch-OG rule; tsc and build exit 0; validate_return.py --md tasks/returns/P463_contract.md exits 0"
}
```

**Proposed RETURNED.** Orchestrator: verify merge commit `99576c32`, artifact sha256s, re-run tsc/build, confirm PR is mergeable.
