---
id: TASK-321A
title: Wave 0 — /hashvaot index reconciliation + 6 route deletions (frontend only)
owner: frontend-agent
status: CLOSED
priority: HIGH
closed_at: 2026-06-17
close_reason: >
  Wave 0 shipped + orchestrator-verified live. Merged as PR #9 (master tip ed53b858c), Vercel Ready. Live smoke GREEN
  (WebFetch, cache-busted ?w0=ed53): butter/salty-snacks/maadanim/vegetable-spreads/cakes-hard-cookies all 404; /hashvaot
  index shows brined-cheeses/cakes/cookies-coffee and no longer shows the 4 deleted categories; hummus still 200 (top 71·B)
  so deleting vegetable-spreads didn't break the shared dataset. Orphan-JSON follow-up (1e532806) verified: 5 orphan JSONs
  + stale comment gone, 0 OFF refs. Butter + salty-snacks takedown (possible OFF/fabricated data) now off production.
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  Frontend-only Wave 0 of the zero-different sweep: on a clean branch off origin/master, delete 6 routes (butter, salty-snacks, maadanim, vegetable-spreads, bread-comparison, cakes-hard-cookies) page+route+orphaned components/page-data, and reconcile the /hashvaot index card set (add brined-cheeses/cakes/cookies-coffee cards; remove the 4 deleted-category cards; keep bread/cheese/yogurts as rebuild-pending). No scoring/data edits. npm run build must pass. New branch, PR, owner merges. Runs in a PARALLEL chat.
---

# TASK-321A — Wave 0 — /hashvaot index reconciliation + 6 route deletions (frontend only)

## Execution log (2026-06-17)

**Branch:** `sweep/wave0-index-deletions` (off `origin/master`, pushed to `Argento17/Barint`)
**Worktree:** `/c/bari-wave0` — isolated, never touches the main checkout.
**Commit:** `c1ebbe77` — 34 files changed, 229 insertions(+), 1680 deletions(−)

---

## (A) Routes deleted — all 6

| Route | Path | Type |
|---|---|---|
| butter | `bari-web/src/app/hashvaot/butter/page.tsx` | full category page |
| salty-snacks | `bari-web/src/app/hashvaot/salty-snacks/page.tsx` | full category page |
| maadanim | `bari-web/src/app/hashvaot/maadanim/page.tsx` | full category page |
| vegetable-spreads | `bari-web/src/app/hashvaot/vegetable-spreads/page.tsx` | full category page |
| bread-comparison | `bari-web/src/app/hashvaot/bread-comparison/page.tsx` | legacy redirect shim |
| cakes-hard-cookies | `bari-web/src/app/hashvaot/cakes-hard-cookies/page.tsx` | redirect shim (→ /hashvaot/cakes) |

## Orphaned files deleted (cascade)

**Hashvaot card components (4):**
- `bari-web/src/components/hashvaot/featured-butter-intelligence-card.tsx`
- `bari-web/src/components/hashvaot/featured-maadanim-intelligence-card.tsx`
- `bari-web/src/components/hashvaot/featured-salty-snacks-intelligence-card.tsx`
- `bari-web/src/components/hashvaot/featured-vegetable-spreads-intelligence-card.tsx`

**Comparison page components (4):**
- `bari-web/src/components/comparisons/butter-comparison-page.tsx`
- `bari-web/src/components/comparisons/maadanim-comparison-page.tsx`
- `bari-web/src/components/comparisons/salty-snacks-comparison-page.tsx`
- `bari-web/src/components/comparisons/vegetable-spreads-comparison-page.tsx`

**Page-data libs (4):**
- `bari-web/src/lib/comparisons/butter-page-data.ts`
- `bari-web/src/lib/comparisons/maadanim-page-data.ts`
- `bari-web/src/lib/comparisons/salty-snacks-page-data.ts`
- `bari-web/src/lib/comparisons/vegetable-spreads-comparison-page-data.ts`

**Shelf-filter libs (4):**
- `bari-web/src/lib/comparisons/butter-shelf-filters.ts`
- `bari-web/src/lib/comparisons/maadanim-shelf-filters.ts`
- `bari-web/src/lib/comparisons/salty-snacks-shelf-filters.ts`
- `bari-web/src/lib/comparisons/vegetable-spreads-shelf-filters.ts`

**Registry category files (4):**
- `bari-web/src/lib/comparisons/registry/categories/butter.ts`
- `bari-web/src/lib/comparisons/registry/categories/maadanim.ts`
- `bari-web/src/lib/comparisons/registry/categories/salty-snacks.ts`
- `bari-web/src/lib/comparisons/registry/categories/vegetable-spreads.ts`

**Dev routes (orphaned by maadanim deletion, 2 files):**
- `bari-web/src/app/dev/preview/page.tsx` (exclusively used maadanim-comparison-page + maadanim-page-data)
- `bari-web/src/app/api/dev/maadanim/route.ts` (exclusively used registry "maadanim" entry)

**Registry updates (2 files modified):**
- `bari-web/src/lib/comparisons/registry/index.ts` — removed butter/maadanim/salty-snacks/vegetable-spreads imports and registry entries
- `bari-web/src/lib/comparisons/registry/types.ts` — removed "butter" | "maadanim" | "salty-snacks" | "vegetable-spreads" from `ComparisonCategoryId`

---

## (B) /hashvaot index reconciled

**File:** `bari-web/src/app/hashvaot/page.tsx`

| Action | Card | href |
|---|---|---|
| REMOVED | FeaturedButterIntelligenceCard | /hashvaot/butter |
| REMOVED | FeaturedMaadanimIntelligenceCard | /hashvaot/maadanim |
| REMOVED | FeaturedSaltySnacksIntelligenceCard | /hashvaot/salty-snacks |
| REMOVED | FeaturedVegetableSpreadsIntelligenceCard | /hashvaot/vegetable-spreads |
| ADDED | FeaturedBrinedCheesesIntelligenceCard | /hashvaot/brined-cheeses |
| ADDED | FeaturedCakesHardCookiesIntelligenceCard | /hashvaot/cakes |
| ADDED | FeaturedCookiesCoffeeIntelligenceCard | /hashvaot/cookies-coffee |
| KEPT | FeaturedMilkIntelligenceCard | /hashvaot/milk-comparison |
| KEPT | FeaturedBreakfastCerealsIntelligenceCard | /hashvaot/breakfast-cereals |
| KEPT | FeaturedGranolaIntelligenceCard | /hashvaot/granola |
| KEPT | FeaturedBreadIntelligenceCardLite | /hashvaot/bread (rebuild-pending) |
| KEPT | FeaturedCheeseIntelligenceCard | /hashvaot/cheese (rebuild-pending) |
| KEPT | FeaturedHardCheesesIntelligenceCard | /hashvaot/hard-cheeses |
| KEPT | FeaturedHummusIntelligenceCard | /hashvaot/hummus |
| KEPT | FeaturedJuicesIntelligenceCard | /hashvaot/juices |
| KEPT | FeaturedSnacksIntelligenceCard | SNACK_COMPARISON_HREF |

**New card components added (3):**
- `bari-web/src/components/hashvaot/featured-brined-cheeses-intelligence-card.tsx`
- `bari-web/src/components/hashvaot/featured-cakes-hard-cookies-intelligence-card.tsx`
- `bari-web/src/components/hashvaot/featured-cookies-coffee-intelligence-card.tsx`

All use stock CATEGORY theme images (`/hashvaot/themes/{cat}.jpg`) per the featured_card_stock_image_rule.

---

## Grep-clean proof (no dangling refs)

```
grep -rn "butter-page-data|salty-snacks-page-data|maadanim-page-data|vegetable-spreads-comparison-page-data|
butter-shelf-filters|maadanim-shelf-filters|salty-snacks-shelf-filters|vegetable-spreads-shelf-filters|
butter-comparison-page|maadanim-comparison-page|salty-snacks-comparison-page|vegetable-spreads-comparison-page|
featured-butter-intelligence|featured-salty-snacks-intelligence|featured-maadanim-intelligence|featured-vegetable-spreads-intelligence"
/c/bari-wave0/bari-web/src → 0 matches
```

Registry grep for "butter"|"maadanim"|"salty-snacks"|"vegetable-spreads" in `src/lib/comparisons/registry/` → 0 matches.

---

## Build result

```
EXIT_CODE: 0
Next.js 16.2.6 (Turbopack)
✓ Compiled successfully in 8.3s
✓ TypeScript — 0 errors
✓ 43 pages generated
```

**Route list — deleted routes ABSENT:**
- /hashvaot/butter → NOT in build ✓
- /hashvaot/salty-snacks → NOT in build ✓
- /hashvaot/maadanim → NOT in build ✓
- /hashvaot/vegetable-spreads → NOT in build ✓
- /hashvaot/bread-comparison → NOT in build ✓
- /hashvaot/cakes-hard-cookies → NOT in build ✓

**New routes PRESENT:**
- /hashvaot/brined-cheeses ✓
- /hashvaot/cakes ✓
- /hashvaot/cookies-coffee ✓

---

## Return block

**Status:** RETURNED
**DoD claims verified:**
- [x] Branch `sweep/wave0-index-deletions` pushed to `origin` (Argento17/Barint)
- [x] 6 routes deleted (page+route dir)
- [x] All orphaned components, page-data, shelf-filters, registry entries removed
- [x] 3 new card components added (brined-cheeses, cakes, cookies-coffee) — stock category images
- [x] 4 card removals from index (butter, maadanim, salty-snacks, vegetable-spreads)
- [x] bread + cheese kept as rebuild-pending cards
- [x] No scoring/data/BSIP files touched
- [x] npm run build: exit 0, 43 pages, 0 TypeScript errors
- [x] Zero dangling refs (grep-clean)

**NOT done (out of scope / owner decision):**
- `compare/bread-comparison` route at `bari-web/src/app/compare/bread-comparison/page.tsx` — this is a separate legacy redirect (→ /hashvaot/bread via BREAD_COMPARISON_HREF). It compiled fine and was NOT in the 6-route deletion list. Flagged for Wave 1 or separate cleanup.
- Worktree `/c/bari-wave0` left in place — owner removes after PR merges.
- No PR opened — owner opens/merges (go-live gate).

## ORCHESTRATOR VERIFICATION (2026-06-17, against pushed branch origin/sweep/wave0-index-deletions)
Independently verified — NOT taken on the agent's word:
- ✅ Clean fast-forward (0 behind / 1 ahead of master); all 6 route `page.tsx` confirmed absent on the branch.
- ✅ Index card set on the branch = 9 KEPT (milk, cereals, granola, bread, cheese, hard-cheeses, hummus, juices, snacks)
  + 3 ADDED (brined, cakes, cookies) = 12 rendered cards; 4 deleted-category cards gone. (Agent's prose "kept 11" was a
  miscount; the actual composition is correct.)
- ✅ No dangling CODE references; `glass-box-copy.ts` hit is only a stale COMMENT (inert, build-consistent).
- ✅ Cascade deletions sound; good catch on the maadanim dev-route + api/dev/maadanim runtime bug.
- ⚠️ **GAP (agent missed): orphaned data JSONs not deleted** — `butter_frontend_v2.json`, `maadanim_frontend_v3.json`,
  `salty_snacks_frontend_v4.json` (+ archived butter_v1, maadanim_v2) remain. No route imports them (no build/runtime
  risk), but the butter JSON still carries external image URLs → "delete the category entirely" isn't complete while
  they're in the repo. Follow-up sent to the parallel chat to delete them on the same branch before merge.
- Build (exit 0 / 43 pages / 0 TS errors) accepted on the agent's evidence + clean-FF structural verification (not re-run here).
**Verdict: branch is correct for the routes+index ask; merge-ready AFTER the orphan-JSON follow-up lands. Owner merges; then live-smoke.**

### Follow-up verified 2026-06-17 (commit 1e532806, branch tip; clean FF 2 ahead of master)
- ✅ All 5 orphan JSONs deleted (butter_frontend_v2, maadanim_frontend_v3, salty_snacks_frontend_v4, archive/butter_frontend_v1, archive/maadanim_frontend_v2).
- ✅ glass-box-copy.ts stale maadanim comment removed.
- ✅ Zero remaining OFF-host refs in any deleted-category data anywhere on the branch.
**WAVE 0 COMPLETE + ORCHESTRATOR-VERIFIED → MERGE-READY.** Owner merges to master (auto-deploys); then orchestrator live-smokes:
6 routes → 404, /hashvaot index shows brined/cakes/cookies + not butter/maadanim/salty-snacks/veg-spreads, kept pages still load.

```json
{
  "task_id": "TASK-321A",
  "status": "RETURNED",
  "agent": "frontend-agent",
  "branch": "sweep/wave0-index-deletions",
  "commit": "c1ebbe77",
  "build_exit_code": 0,
  "build_pages": 43,
  "typescript_errors": 0,
  "routes_deleted": ["hashvaot/butter","hashvaot/salty-snacks","hashvaot/maadanim","hashvaot/vegetable-spreads","hashvaot/bread-comparison","hashvaot/cakes-hard-cookies"],
  "orphans_deleted": 20,
  "cards_added": ["brined-cheeses","cakes","cookies-coffee"],
  "cards_removed": ["butter","maadanim","salty-snacks","vegetable-spreads"],
  "dangling_refs": 0,
  "off_dependencies": 0,
  "scoring_files_touched": 0,
  "propose": "RETURNED"
}
```
