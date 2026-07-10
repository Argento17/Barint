# TASK-464 Stage-1 Report — White Tile Default (site-wide blend fix)

**Date:** 2026-07-03  
**Worktree:** `C:\bari_wt_t461x_a`  
**Branch:** `fix/task464-thumbnail-blend`  
**Commit SHA:** `9d8bf49c`  
**Base commit:** `06f85de4` (Merge PR #49 — task467-share-community)

---

## What changed (file:line)

### 1. `bari-web/src/components/comparisons/bari-product-thumbnail.tsx:13`
```
- blendWhite = false,
+ blendWhite = true,
```
Changed the default parameter from `false` to `true`. The JSDoc comment was updated to reflect the new semantic: white tile is now the site-wide default; pass `false` explicitly if a specific context requires the cream `#F7F7F2` tile back.

### 2. `bari-web/src/components/shared/comparison-row.tsx:189` (line removed)
```
- blendWhite={category === "magnesium"}
```
Removed the explicit prop that was previously overriding the default to `false` for all non-magnesium categories. Without this line, all categories inherit `blendWhite=true` from the default. Magnesium continues to receive `true` (no regression — it was already `true` explicitly; now it gets `true` from the default).

**Net diff:** 2 files changed, 6 insertions, 7 deletions. No data/JSON changes. No other files touched.

---

## Call-site audit (complete)

| Call-site | File | Before | After | Notes |
|---|---|---|---|---|
| `BariProductThumbnail` in comparison row | `src/components/shared/comparison-row.tsx:186-190` | `blendWhite={category === "magnesium"}` → `false` for 16 live categories, `true` for magnesium | no explicit prop → inherits `true` default for ALL categories incl. magnesium | Only call-site |
| Export definition | `src/components/comparisons/bari-product-thumbnail.tsx:13` | `blendWhite = false` | `blendWhite = true` | Default changed |

Confirmed via grep across `bari-web/src/`: `BariProductThumbnail` is imported and used in exactly **one** file (`comparison-row.tsx`). No other call-sites exist. The `/hashvaot` hub page uses category feature cards (not `BariProductThumbnail`); confirmed 0 `.bari-cmp-thumbcell` elements on that page.

---

## Screenshot index

All screenshots saved to `C:\Bari\tasks\returns\TASK-464_render_verify\`.

| Filename | Category | Viewport | What it proves |
|---|---|---|---|
| `milk_desktop_shelf.png` | milk (78% white-box, worst) | 1280×900 desktop | Hero + first product row visible; first row expanded, thumbnail shows milk carton on white tile |
| `milk_desktop_multirow.png` | milk | 1280×900 desktop | Multiple collapsed rows; milk carton thumbnails uniform on white tiles, no cream vs white mismatch |
| `milk_mobile390_rows.png` | milk | 390×844 mobile | 3 milk/alt-milk rows; carton images blend into white tile; uniform across rows |
| `granola_desktop_rows.png` | granola (4.5% defect, cleanest control) | 1280×900 desktop | Multiple granola rows; transparent cutout bags on white tile; clean and unchanged vs pre-fix (granola was already mostly clean — control confirmed) |
| `granola_mobile390_rows.png` | granola | 390×844 mobile | 3 granola rows; transparent bags on white tiles; no regression |
| `hummus_desktop_rows.png` | hummus (70% white-box, worst mixed) | 1280×900 desktop | 5 hummus rows; hummus containers with baked-in white backgrounds now dissolve into white tile; shelf visually uniform |
| `hummus_mobile390_rows.png` | hummus | 390×844 mobile | 4 hummus rows; same result at mobile viewport |
| `magnesium_mobile390_regression.png` | magnesium (was the only blendWhite=true category) | 390×844 mobile | Supplement bottles on white tiles; previously explicit `blendWhite={category === "magnesium"}`; now via default — behavior identical, no regression |
| `hashvaot_hub_desktop.png` | /hashvaot hub | 1280×900 desktop | Category card hub — no BariProductThumbnail present; confirms hub is unaffected by change |

**Visual findings:**
- Milk shelf (78% WHITE_BOX before): all carton images now sit on white tiles. The previously jarring "cream tile frame around a white-box product photo" is gone. Shelf is visually uniform.
- Hummus shelf (70% WHITE_BOX, worst mixed category before): hummus tubs with baked-in white studio backgrounds now dissolve into the white tile. The mixed look (some products floating, others boxed) is eliminated for the WHITE_BOX class.
- Granola (cleanest control, 95.5% transparent): no change in appearance — transparent cutouts on white look identical to transparent cutouts on near-white cream. Control confirmed.
- Magnesium (the one prior explicit `blendWhite=true` user): no regression — same appearance.
- Note: `OTHER_OPAQUE` products (gray/tan/colored studio backdrops, 61 total, 10.5% of corpus) remain as a visible box on any background color. Stage-1 was never designed to fix these — they are the Stage-2 rembg scope.

---

## TypeScript / Build results

| Check | Command | Exit code |
|---|---|---|
| TypeScript typecheck | `npx tsc --noEmit` | **0** |
| Next.js production build | `npm run build` | **0** |

Build ran in `C:\bari_wt_t461x_a\bari-web`. All 16 comparison routes compiled successfully.

---

## Magnesium regression check

The magnesium page previously received `blendWhite={category === "magnesium"}` — an explicit `true`. After the change, it receives `blendWhite` default (`true`). Behavior is identical. Screenshot `magnesium_mobile390_regression.png` confirms supplement bottles render on white tiles, same as before.

---

## Residual after Stage-1

- **Resolved:** 201/262 opaque-background defects (WHITE_BOX class — all baked-in white/near-white backgrounds). These dissolve into the white tile.
- **Residual:** 61/262 OTHER_OPAQUE products (gray/tan/colored studio backdrops — mostly Yochananof-sourced milk/juices). White tile does not help these; they still show a colored box. Stage-2 rembg cutout regen is the fix path (see `TASK-464_handover.md`).
- **Stage-2 scope:** propose as own task; requires Data+Design pipeline (self-hosted cutout images, imageUrl repointing in 16 JSONs), owner-gated per handover.

---

## Return Contract

```json
{
  "task_id": "TASK-464",
  "stage": "stage-1",
  "status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/src/components/comparisons/bari-product-thumbnail.tsx",
      "sha256": "changed",
      "change": "blendWhite default false→true; JSDoc updated"
    },
    {
      "path": "bari-web/src/components/shared/comparison-row.tsx",
      "sha256": "changed",
      "change": "removed blendWhite={category === 'magnesium'} prop"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/TASK-464_stage1_report.md",
      "sha256": "this file",
      "change": "new — stage-1 report"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/milk_desktop_shelf.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/milk_desktop_multirow.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/milk_mobile390_rows.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/granola_desktop_rows.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/granola_mobile390_rows.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/hummus_desktop_rows.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/hummus_mobile390_rows.png",
      "sha256": "screenshot",
      "change": "new — render verify"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/magnesium_mobile390_regression.png",
      "sha256": "screenshot",
      "change": "new — regression check"
    },
    {
      "path": "tasks/returns/TASK-464_render_verify/hashvaot_hub_desktop.png",
      "sha256": "screenshot",
      "change": "new — hub call-site audit"
    }
  ],
  "counts": {
    "files_changed": 2,
    "lines_added": 6,
    "lines_removed": 7,
    "call_sites_audited": 1,
    "call_sites_total": 1,
    "defects_addressed_by_stage1": 201,
    "defects_total_corpus": 262,
    "stage1_coverage_pct": 76.7,
    "residual_other_opaque": 61,
    "screenshots_taken": 9,
    "categories_screenshotted": 4,
    "tsc_exit_code": 0,
    "build_exit_code": 0
  },
  "commands_run": [
    {"cmd": "git checkout -b fix/task464-thumbnail-blend 06f85de4", "exit": 0},
    {"cmd": "npx tsc --noEmit", "exit": 0},
    {"cmd": "npm run build", "exit": 0},
    {"cmd": "npm run start (port 3099, killed after screenshots)", "exit": 0},
    {"cmd": "git commit", "exit": 0, "sha": "9d8bf49c"}
  ],
  "not_done": [
    "Stage-2: rembg cutout regen for 61 OTHER_OPAQUE products (Yochananof milk/juices — colored studio backdrops; requires Data+Design pipeline + owner gate; propose as separate task)",
    "PR creation (owner reviews branch fix/task464-thumbnail-blend before merge; this is a site-wide visual change per the handover spec)"
  ],
  "acceptance_test": {
    "tsc": "PASS (exit 0)",
    "build": "PASS (exit 0)",
    "render_verify_milk": "PASS — white tile uniform on 78%-defect category; carton photos dissolve",
    "render_verify_granola": "PASS (control) — transparent cutouts unchanged on white tile",
    "render_verify_hummus": "PASS — 70%-white-box mixed category now visually uniform",
    "magnesium_regression": "PASS — supplement bottles unchanged on white tile",
    "hub_call_site": "PASS — BariProductThumbnail not present on /hashvaot hub; unaffected"
  }
}
```
