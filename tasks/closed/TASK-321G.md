---
id: TASK-321G
title: Wave 1 frontend — purge remaining legacy/duplicate routes (compare/bread-comparison + audit)
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - 4 legacy routes deleted (commit beabcef8 per task body); /compare/bread-comparison asserted absent. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: MEDIUM
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  Parallel chat: audit the full route tree for legacy/duplicate/orphan routes that violate uniformity; delete compare/bread-comparison (flagged in Wave 0) + any others; clean branch off origin/master, build green, push, owner merges. No scoring/data edits.
---

# TASK-321G — Wave 1 frontend — purge remaining legacy/duplicate routes (compare/bread-comparison + audit)

## Execution log (2026-06-17)

**Branch:** `sweep/wave1-legacy-routes` (off `origin/master` @ `ed53b858c`, pushed to `Argento17/Barint`)
**Worktree:** `C:\bari-wave1` — isolated.
**Commit:** `beabcef8` — 4 files changed, 35 deletions(-)

---

## Route audit — full disposition

**All routes under `bari-web/src/app/` audited (origin/master post Wave 0 merge):**

| Route | Nature | Decision |
|---|---|---|
| `/compare/bread-comparison` | Legacy redirect shim → `/hashvaot/bread` | **DELETED** |
| `/compare/bread-shufersal` | Legacy redirect shim → `/hashvaot/bread` | **DELETED** |
| `/compare/snack-bars` | Legacy redirect shim → `/hashvaot/snacks` | **DELETED** |
| `/categories/snacks` | Dead stub — `return notFound()` | **DELETED** |
| `/hashvaot/yogurts` | Bespoke component (Wave 2 rebuild/delete target) | **LEFT — Wave 2 scope** |
| `/hashvaot/cheese` | Bespoke component (Wave 2 rebuild/delete target) | **LEFT — Wave 2 scope** |
| `/products/demo` | Ambiguous — no deletion mandate | **LEFT — not in delete batch** |
| `/research/*` | Content pages — not in delete batch | **LEFT — not in delete batch** |
| All `/hashvaot/` canonical routes (14) | Conforming or scheduled | **UNTOUCHED** |

**Why each deleted route qualified:**
- `compare/bread-comparison`: redirect shim was in the Wave 0 DELETE batch but not caught; `LegacyCompareBreadComparisonRoute()` body is a single `redirect(BREAD_COMPARISON_HREF)` — pure legacy.
- `compare/bread-shufersal`: same pattern, also redirected to `/hashvaot/bread`.
- `compare/snack-bars`: redirect to `/hashvaot/snacks`; no canonical function.
- `categories/snacks`: single `notFound()` call; no linked content, no imports, dead stub.

**Ambiguous routes left for owner review:**
- `/hashvaot/yogurts` — Wave 2 target (rebuild or delete per TASK-321 plan); live on master, out of Wave 1 scope.
- `/hashvaot/cheese` — Wave 2 target; same.

---

## Files changed

| Action | Path |
|---|---|
| Deleted | `bari-web/src/app/compare/bread-comparison/page.tsx` |
| Deleted | `bari-web/src/app/compare/bread-shufersal/page.tsx` |
| Deleted | `bari-web/src/app/compare/snack-bars/page.tsx` |
| Deleted | `bari-web/src/app/categories/snacks/page.tsx` |

Parent dirs `/compare/` and `/categories/` removed entirely (both only contained the deleted subdirs).

---

## Grep-clean proof

No remaining references to deleted route paths in `src/**/*.{ts,tsx}`:
- `bread-comparison` (route) — 0 hits (only data-module hits: `bread-comparison-page-data.ts` + component `bread-comparison-page.tsx` — these are NOT routes; they belong to `/hashvaot/bread`)
- `bread-shufersal` (route) — 0 hits
- `compare/snack-bars` (route) — 0 hits
- `categories/snacks` (route) — 0 hits (only hit: `registry/index.ts` imports `./categories/snacks.ts` data file — unrelated to the deleted route)

---

## Build result

```
Next.js 16.2.6 (Turbopack)
✓ Compiled successfully in 6.3s
✓ TypeScript: 0 errors
✓ 39 pages generated (was 43 on master; delta = 4 deleted routes)
EXIT: 0

Routes ABSENT (deleted): /compare/bread-comparison, /compare/bread-shufersal,
  /compare/snack-bars, /categories/snacks ✓
All canonical /hashvaot/* routes PRESENT ✓
```

---

## Return block

**Status:** RETURNED
**DoD claims:**
- [x] Branch `sweep/wave1-legacy-routes` pushed to `origin` (Argento17/Barint)
- [x] `compare/bread-comparison` deleted (confirmed legacy redirect, Wave 0 gap)
- [x] `compare/bread-shufersal` deleted (confirmed legacy redirect)
- [x] `compare/snack-bars` deleted (confirmed legacy redirect)
- [x] `categories/snacks` deleted (confirmed dead stub)
- [x] `compare/` and `categories/` parent dirs removed entirely
- [x] Zero dangling refs — grep-clean across `src/**/*.{ts,tsx}`
- [x] `npm run build`: exit 0, 39 pages, 0 TypeScript errors
- [x] All canonical `/hashvaot/*` routes present and unmodified
- [x] Zero scoring/data/component edits — routes only

**Ambiguous routes surfaced for owner:**
- `/hashvaot/yogurts` — Wave 2 target, not deleted in Wave 1
- `/hashvaot/cheese` — Wave 2 target, not deleted in Wave 1

```json
{
  "task_id": "TASK-321G",
  "status": "RETURNED",
  "agent": "frontend-agent",
  "branch": "sweep/wave1-legacy-routes",
  "commit": "beabcef8",
  "build_exit_code": 0,
  "build_pages": 39,
  "build_pages_before": 43,
  "typescript_errors": 0,
  "routes_deleted": [
    "compare/bread-comparison",
    "compare/bread-shufersal",
    "compare/snack-bars",
    "categories/snacks"
  ],
  "routes_deleted_count": 4,
  "files_deleted_count": 4,
  "grep_clean": true,
  "live_files_modified": 0,
  "ambiguous_left_for_owner": ["hashvaot/yogurts", "hashvaot/cheese"],
  "off_used": false,
  "propose": "RETURNED"
}
```

## ORCHESTRATOR VERIFIED 2026-06-17 — merge-ready
Branch sweep/wave1-legacy-routes (beabcef81), clean FF (0 behind/1 ahead). Verified: 4 routes DELETED
(categories/snacks, compare/bread-comparison, compare/bread-shufersal, compare/snack-bars — all redirect
shims/dead stubs); all 13 canonical /hashvaot routes present & unmodified. bread/cheese/yogurts correctly
retained for Wave 2. Owner merges. CONFIG/DELETION side of the sweep verified.
