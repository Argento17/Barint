# P201 / Rehab the stale cheese-conform branch onto current master (route: C1-GEMINI)

➡️ OWNER: TASK-321I follow-up. The cheese frontend conform is correct, but its branch
`sweep/cheese-conform` was cut from an OLD master (before the yogurt + wave1 merges), so
merging it as-is would REVERT the yogurt conform. Gemini brings it up to date, keeping BOTH
the yogurt conform (from master) AND the cheese conform (from the branch). Orchestrator verifies before merge.

---

You are rehabilitating a stale git branch so it can merge cleanly. Work ENTIRELY in the
existing worktree `C:\bari-cheese` (it is checked out on branch `sweep/cheese-conform`).
Do NOT touch `C:\Bari` or any other worktree. This is git + build work only — do not change
scoring, data, or copy.

## The problem (precise)
- `origin/master` HEAD already contains: PR #10 (wave1 legacy route deletions) and PR #11
  (the YOGURT conform — `yogurts-page-data.ts`, `yogurts_frontend_v1.json`, conformed route + featured card).
- `sweep/cheese-conform` was branched BEFORE those merges. Its diff vs master therefore shows it
  *removing* the yogurt conform (re-adding the old `yogurts-comparison-page-data.ts`, deleting
  `yogurts-page-data.ts` and `yogurts_frontend_v1.json`). That is an artifact of the stale base — NOT intended.
- The cheese WORK on the branch is correct and must be preserved (`cheese-page-data.ts`,
  `cheese_frontend_v4.json`, conformed `cheese/page.tsx`, updated featured-cheese card, etc.).

## Tasks (do exactly these, in C:\bari-cheese)
1. `cd /c/bari-cheese` and confirm: `git status` clean, `git branch --show-current` = `sweep/cheese-conform`.
2. `git fetch origin`
3. `git merge origin/master`  (a merge commit; conflicts expected — resolve per the rule below).
4. **Conflict resolution rule:**
   - Any YOGURT file (`yogurts-page-data.ts`, `yogurts_frontend_v1.json`, `yogurts-shelf-filters.ts`,
     `yogurts-comparison-page.tsx`, `app/hashvaot/yogurts/page.tsx`, `featured-yogurts-intelligence-card.tsx`,
     `registry/categories/yogurts.ts`): take **MASTER's** version (the conform). If the old
     `yogurts-comparison-page-data.ts` reappears, DELETE it — master replaced it with `yogurts-page-data.ts`.
   - Any CHEESE file: keep the **branch's** version (the conform).
   - Shared files touched by both (`app/hashvaot/page.tsx`, registry index): take the UNION — keep BOTH the
     cheese-page-data import/usage AND the yogurts-page-data import/usage. Neither category may lose its import.
5. After resolving: `cd /c/bari-cheese/bari-web && npm install && npm run build` → must exit 0.
6. Grep-confirm zero references to deleted modules: `cheese-comparison-page-data`, `cheese-shelf-filters`,
   `yogurts-comparison-page-data` should return NOTHING under `bari-web/src`.
7. Commit the merge resolution and `git push origin sweep/cheese-conform`.

## Hard rules
- Do NOT lose the yogurt conform. After build, both `/hashvaot/cheese` and `/hashvaot/yogurts` must be present
  in the build output and both must use their `*-page-data.ts` loaders.
- Do not edit scoring, data JSON contents, or copy. No OFF anything.

## Return block (end with this — REAL values)
- Conflicted files + which side you took for each.
- `npm run build` exit code + total page count.
- Confirmation both `/hashvaot/cheese` and `/hashvaot/yogurts` are in the build output.
- Grep results for the three deleted-module names (must be empty).
- The merge commit SHA + confirmation of push to origin/sweep/cheese-conform.
