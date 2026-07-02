# P463 / TASK-458 catalog branch: merge origin/master + resolve 4 conflicts (route: C1-CURSOR)

## 1. Context / baseline
- You are ALREADY in isolated worktree `C:\bari_wt_t458`, branch `golive/catalog-task458` (the fully two-gated catalog package). The owner cannot merge its PR: origin/master has moved (merges #38/#39/#40) and `git merge-tree` shows exactly 4 content conflicts. Never touch `C:\Bari`. `bari-web\node_modules` already installed here.
- The conflicts are between THIS branch's per-page OpenGraph metadata refactor (commit bd1e3a80: pages now call `blogOpenGraph()`/`withComparisonOpenGraph()` helpers) and master's TASK-460 prose fixes (commits d57eae3b/cef964d4/9e17a35b: corrected Hebrew copy strings in the same files).

## 2. Objective
```
git fetch origin
git merge origin/master
```
Resolve the 4 conflicted files — `bari-web/src/app/hashvaot/breakfast-cereals/page.tsx`, `bari-web/src/app/hashvaot/cakes/page.tsx`, `bari-web/src/app/hashvaot/juices/page.tsx`, `bari-web/src/lib/comparisons/crackers-page-data.ts` — with this exact rule:
- **Hebrew copy strings: origin/master's version wins, always** (those strings passed five adversarial gates on TASK-460; do not resurrect any older text — specifically no "38 פרמטרים", no stale counts).
- **OG/metadata structure: this branch's version wins** (the `withComparisonOpenGraph(...)`/helper-based metadata export), applied AROUND master's strings — i.e., the final file has master's copy inside this branch's metadata structure.
- Nothing else: no new copy, no refactors beyond the conflict hunks.

After resolution:
1. Verify NO conflict markers remain (`git grep -l "<<<<<<<"` = empty).
2. Belt-and-braces: `git grep -n "38 פרמטרים\|655" -- bari-web/src` must return ZERO hits; and confirm the four resolved files import/use the OG helpers exactly as this branch had them.
3. `npx tsc --noEmit` exit 0 and `npm run build` exit 0 in `bari-web\` (the /catalog route must appear in build output).
4. Commit the merge (standard merge commit message is fine, mention the resolution rule), then `git push` the branch (it has an upstream; pushing updates the PR — this is expected and required so the owner can merge).

## 3. Boundaries
- OFF ban absolute. No consumer-string authoring (the rule above only selects between two already-gated versions). No other files modified beyond the merge itself. No PR open/merge (owner clicks).
- If a conflict cannot be resolved under the rule (e.g., master deleted something this branch needs), STOP, describe it precisely, propose BLOCKED.

## 4. Return
Write to `tasks\returns\P463_contract.md` (not P463_return.md): per-file resolution description (which side won what), the three verification outputs (no markers, zero banned strings, tsc/build exit codes), merge commit SHA, push confirmation. Full Return Contract v1 JSON (real sha256s for the 4 resolved files, counts with denominators, commands_run with exit codes). Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P463_contract.md --root C:\bari_wt_t458` exit 0 (PowerShell). Commit the contract, include it in the push. Propose RETURNED.
