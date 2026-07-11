---
id: TASK-321H
title: Yogurt frontend wiring — conform /hashvaot/yogurts to the uniform comparison page
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "SUPERSEDED - TASK-515/543 split replaced the 321H conformance approach; live yogurt served via the new architecture (asserted). Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  Parallel chat: on branch sweep/yogurt-conform-data (has yogurts_frontend_v1.json, 83 products+copy), replace the bespoke/stale /hashvaot/yogurts route with the standard conforming comparison page (model on brined-cheeses), reading the new JSON. Remove orphaned bespoke yogurt page-data/component. Build green, push, owner merges. No scoring/data edits.
---

# TASK-321H — Yogurt frontend wiring — conform /hashvaot/yogurts to the uniform comparison page

## Execution log (2026-06-17)

**Branch:** `sweep/yogurt-conform` (off `origin/sweep/yogurt-conform-data` @ `ce02095d9`, pushed to `Argento17/Barint`)
**Worktree:** `C:\bari-yogurt` — isolated.
**Commit:** `2d05f9ea` — 7 files changed, 102 insertions(+), 179 deletions(-)

---

## What was done

Replaced the bespoke `yogurts-comparison-page-data.ts` + `yogurts-shelf-filters.ts` pipeline with the
standard uniform pattern (modeled on brined-cheeses / cookies-coffee). The route now reads from
`yogurts_frontend_v1.json` (83 products, `run_yogurt_shelfrel_v2`) via `loadComparisonCorpus`.

---

## Files changed

| Action | Path | Notes |
|---|---|---|
| **CREATED** | `src/lib/comparisons/yogurts-page-data.ts` | New conforming page-data; reads `yogurts_frontend_v1.json`; page_copy extracted from JSON (no hardcoded Hebrew) |
| **DELETED** | `src/lib/comparisons/yogurts-comparison-page-data.ts` | Was reading `yogurts_frontend_v4.json` with stale run_yogurt_006 corpus + hardcoded copy strings |
| **DELETED** | `src/lib/comparisons/yogurts-shelf-filters.ts` | Was `_cluster`-based filter tightly coupled to v4.json; v1 products carry no filterTags |
| **UPDATED** | `src/components/comparisons/yogurts-comparison-page.tsx` | Stripped `yogurts-shelf-filters` import; replaced with empty `lensOptions: []` (matches brined-cheeses pattern) |
| **UPDATED** | `src/app/hashvaot/yogurts/page.tsx` | Import switched from `yogurts-comparison-page-data` → `yogurts-page-data` |
| **UPDATED** | `src/lib/comparisons/registry/categories/yogurts.ts` | Import switched to `yogurts-page-data` |
| **UPDATED** | `src/components/hashvaot/featured-yogurts-intelligence-card.tsx` | Import switched to `yogurts-page-data` |

---

## Key decisions

**`prologue` shape mismatch:** `yogurts_frontend_v1.json` ships `page_copy.prologue` as a single string, not `{ sentences: [] }`. Wrapped in single-element array `[_pageCopy.prologue]` to satisfy `prologueSentences: readonly string[]`. CategoryPrologue renders each element — the paragraph renders correctly.

**`category_caveat` key:** JSON uses `category_caveat` (not `caveat`). Formatted as `${title}\n\n${body}` → `yogurtsCategoryNote` string. Matches the standard yellow-box pattern.

**Shelf filters:** `yogurts-shelf-filters.ts` used `_cluster` field from v4 products; v1 products have no `filterTags`/`_cluster`. Using empty `lensOptions: []` (identical to brined-cheeses). This drops the shelf lens UI — consistent with the uniform pattern.

**`consumerTakeaway` decision:** Field is NOT present in `yogurts_frontend_v1.json` (intentionally stripped per dispatch). `ComparisonPage` renders `rowVerdict` and `insightLine` — not `consumerTakeaway`. **Dropped — no copy invented.** All 83 products carry `rowVerdict` and `insightLine` in the JSON.

**No data value changed:** Zero edits to any score/grade/barcode/copy in the JSON. Only route/component/loader files changed.

---

## Grep-clean proof

Zero remaining references to deleted files:
- `yogurts-comparison-page-data` — 0 hits
- `yogurts-shelf-filters` — 0 hits

---

## Build result

```
Next.js 16.2.6 (Turbopack)
✓ Compiled successfully in 6.3s
✓ TypeScript: 0 errors
✓ 43 pages generated
EXIT: 0

/hashvaot/yogurts → PRESENT (83 products, uniform ComparisonPage) ✓
All other canonical routes PRESENT and unchanged ✓
```

Note: build is on `sweep/yogurt-conform-data` base (predates Wave 1 branch), so the legacy redirect shims
(`/compare/bread-comparison` etc.) still appear in this build's route list. They are deleted in `sweep/wave1-legacy-routes`
(TASK-321G, owner-gated). After both PRs merge (Wave 1 first), the combined result will be clean.

---

## Return block

**Status:** RETURNED
**DoD claims:**
- [x] Branch `sweep/yogurt-conform` pushed to `origin` (Argento17/Barint)
- [x] `yogurts-page-data.ts` created — reads `yogurts_frontend_v1.json` via `loadComparisonCorpus`
- [x] `yogurts-comparison-page-data.ts` deleted (orphaned bespoke)
- [x] `yogurts-shelf-filters.ts` deleted (v4-coupled, orphaned)
- [x] `yogurts-comparison-page.tsx` updated — empty shelf filters, no `yogurts-shelf-filters` import
- [x] `page.tsx`, `registry/categories/yogurts.ts`, `featured-yogurts-intelligence-card.tsx` all switched to `yogurts-page-data`
- [x] Zero dangling refs — grep-clean across `src/**/*.{ts,tsx}`
- [x] `npm run build`: exit 0, 43 pages, 0 TypeScript errors
- [x] `/hashvaot/yogurts` present and rendering the 83-product uniform page
- [x] Zero score/grade/barcode/copy values changed
- [x] `consumerTakeaway`: NOT rendered — not present in v1.json, not present in `ComparisonPage` props — **dropped cleanly, no copy invented**
- [x] `off_used`: false (source = `yogurts_frontend_v1.json`, run_yogurt_shelfrel_v2, Shufersal direct scrape)

```json
{
  "task_id": "TASK-321H",
  "status": "RETURNED",
  "agent": "frontend-agent",
  "branch": "sweep/yogurt-conform",
  "base_branch": "sweep/yogurt-conform-data",
  "commit": "2d05f9ea",
  "build_exit_code": 0,
  "build_pages": 43,
  "typescript_errors": 0,
  "files_created": ["src/lib/comparisons/yogurts-page-data.ts"],
  "files_deleted": [
    "src/lib/comparisons/yogurts-comparison-page-data.ts",
    "src/lib/comparisons/yogurts-shelf-filters.ts"
  ],
  "files_updated": [
    "src/components/comparisons/yogurts-comparison-page.tsx",
    "src/app/hashvaot/yogurts/page.tsx",
    "src/lib/comparisons/registry/categories/yogurts.ts",
    "src/components/hashvaot/featured-yogurts-intelligence-card.tsx"
  ],
  "yogurts_route_present": true,
  "product_count": 83,
  "run_id": "run_yogurt_shelfrel_v2",
  "off_used": false,
  "consumer_takeaway_decision": "DROPPED — field absent from v1.json; ComparisonPage renders rowVerdict/insightLine; no copy invented",
  "live_data_values_modified": 0,
  "grep_clean": true,
  "propose": "RETURNED"
}
```

## ORCHESTRATOR VERIFIED 2026-06-17 — yogurt fully conformed
Branch sweep/yogurt-conform (2d05f9ea, based on yogurt-conform-data). Verified: yogurts_frontend_v1.json present,
/hashvaot/yogurts route conformed to standard ComparisonPage, orphaned bespoke modules deleted (yogurts-comparison-page-data,
yogurts-shelf-filters), 0 dangling refs, consumerTakeaway dropped (not rendered). Build green (43 pages, accepted on
agent evidence + clean structural verification). YOGURT END-TO-END CONFORMED (config+copy+frontend). Branch = deploy-ready, owner merges.
