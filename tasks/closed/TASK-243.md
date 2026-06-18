---
id: TASK-243
title: Retailer image backfill for the 32 nulled OFF images (cereals/granola/hard_cheeses)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-11
closed_at: 2026-06-11
cc_reviewed: 2026-06-11
depends_on: [TASK-242]
blocks: []
category_id: null
branch: task-243-image-backfill
commit: 7cac6086
deployed:
  repo: Argento17/Barint
  commit: 6b4a6e8b
  url: https://bari.digital
  verified_at: 2026-06-11
close_reason: >
  CC verification before close: diff = exactly 64 imageUrl lines across 3 JSONs, nothing
  else; EAN-in-URL identity 0 mismatches across all 47 yochananof images on the branch;
  all 47 GET-verified by CC as 200 + image/* + real file sizes (the Yochananof server stubs
  HEAD requests at 2447B — GET is authoritative; smallest real image decoded as a genuine
  220x272 product PNG); branch cut from current master. EAN-named files on the retailer's
  own catalog host = harvested identity, not synthesized guesses. Merged as PR #3
  (6b4a6e8b); live-verified on bari.digital post-deploy: 0 null imageUrls remain on
  /hashvaot/breakfast-cereals, /granola, /hard-cheeses.
summary: >
  TASK-242 de-OFF'd categories by nulling OFF image URLs (honest placeholder). Backfill REAL
  retailer images (Yochananof catalog harvester; HTTP-200 verified; no OFF, no guessed URLs).
  Yogurts excluded per orchestrator scope change (replaced by TASK-249 run_yogurt_006).
---

# TASK-243 — Retailer image backfill for the 32 nulled OFF images (cereals/granola/hard_cheeses)

## Scope (final)

- cereals_frontend_v2.json: 8 nulls
- granola_frontend_v1.json: 9 nulls
- hard_cheeses_frontend_v2.json: 15 nulls
- yogurts: OUT OF SCOPE — replaced wholesale by TASK-249 run_yogurt_006
- Total: 32 nulls targeted

## Return block

**Branch:** `task-243-image-backfill`
**Commit:** `7cac6086`
**PR / Compare:** https://github.com/Argento17/Barint/compare/master...task-243-image-backfill

**Verification log:** `C:\Bari\03_operations\bsip0\scrape\image_backfill_task243\apply_report.json`

### Results

| Category | Nulls before | Backfilled | Still null | Source |
|---|---|---|---|---|
| cereals | 8 | 8 | 0 | Yochananof (api.yochananof.co.il) |
| granola | 9 | 9 | 0 | Yochananof (api.yochananof.co.il) |
| hard_cheeses | 15 | 15 | 0 | Yochananof (api.yochananof.co.il) |
| **Total** | **32** | **32** | **0** | |

### HTTP-200 verification

All 32 URLs verified HTTP 200 + `image/*` Content-Type before entering JSON:
- 19 via prior Yochananof cache-path (EAN in filename, re-verified this run)
- 13 via Yochananof direct pattern `api.yochananof.co.il/media/catalog/product/{d1}/{d2}/{EAN}.jpg`

No Shufersal CDN URLs (cloudfront 403 for all attempts). All from api.yochananof.co.il.

### Build

- `tsc --noEmit`: clean
- `next build`: 47/47 static pages, 0 errors

### Hard guards satisfied

- Only `imageUrl` field changed — no scores, no copy, no other fields
- Zero OFF URLs in any patched file
- All URLs contain EAN in filename (identity confirmed)
- No guessed/synthesized URLs
- Worktree: `C:\Bari\Bari-task243` from `origin/master`, isolated from main working tree

### DoD checklist

- [x] 32/32 nulls backfilled (0 still-null)
- [x] All URLs HTTP-200 verified with image/* Content-Type
- [x] Zero OFF domains in any JSON
- [x] Only imageUrl field modified
- [x] tsc --noEmit clean
- [x] next build green (47/47)
- [x] Branch pushed, compare URL returned
- [x] Worktree isolated from C:\Bari main tree
</content>
</invoke>