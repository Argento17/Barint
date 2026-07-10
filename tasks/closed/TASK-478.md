---
id: TASK-478
title: Own product images: same-origin, blocker-proof serving (Level 2)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  Both phases shipped to origin/master and verified live. All 680 product images
  self-hosted under public/products/ (0 external image URLs remain, verified). Live
  acceptance test with ALL external image hosts blocked passed across cheese/milk/
  chocolate-tablets/hummus/magnesium (0 broken). Commits ebea9187, 5a11025f (Phase A),
  eae897ce (Phase B). DoD met.
depends_on: []
blocks: []
category_id: null
summary: >
  Re-host third-party-hotlinked product images to Bari-owned same-origin storage so images survive ad blockers/VPNs/DNS filters and stop depending on retailer hosts (Yochananof 502s via Vercel optimizer). Follow-up to reverted commit e9ab8171.
---

# TASK-478 — Own product images: same-origin, blocker-proof serving (Level 2)

## Goal / definition of done
Every comparison-page product image is served **same-origin** from `bari.digital`
(via `/_next/image`), so it survives ad blockers, VPNs, and private-DNS filters, and
no longer depends on a third-party host being reachable at request time.
DoD: on a 390px mobile viewport with all external image hosts blocked, every migrated
category still shows real product photos (not the ✦ fallback), and `next build` is green.

## Why (root cause, established 2026-07-03)
- All 663 distinct product images are hotlinked from third parties. **Bari owns no
  image storage** (no Cloudinary/Blob account, no creds, no upload tooling).
- The cheap fix (Level 1 = wrap in `next/image` for same-origin proxy) shipped as
  e9ab8171 and was **reverted (d6b0e252)**: the Vercel image optimizer returns **502**
  for `api.yochananof.co.il` (retailer blocks datacenter fetches), so milk images broke
  for everyone. Same-origin proxy only works for hosts the optimizer can reach.
- Therefore images must live on a **Bari-owned, globally-reachable** store.

## Image inventory (distinct URLs, 2026-07-03)
| Host | Count | Optimizes via Vercel? | Action |
|------|-------|-----------------------|--------|
| res.cloudinary.com (Shufersal's acct) | 588 | ✅ yes | Phase B (ownership hardening) |
| api.yochananof.co.il | 41 | ❌ 502 | **Phase A (must)** |
| yochananof.co.il | 33 | ❌ 502 | **Phase A (must)** |
| supplement hosts (vitamins4all/solgar/…) | ~17 | ❌ | **Phase A (must)** |
| media.shufersal.co.il | 1 | ✅ | Phase B |

Affected data files (retailer-hosted): `milk_frontend_v1.json`, `milk-comparison.json`,
`cakes_hard_cookies_frontend_v1.json`, `cookies_coffee_frontend_v2.json`,
`hard_cheeses_frontend_v4.json`, `juices_frontend_v3.json`, `magnesium-page-data.ts`,
`row-surface.ts`.

## Storage decision (the one real fork)
- **RECOMMENDED — commit optimized WebP to repo `/public/products/<barcode>.webp`.**
  Bari-owned, free, version-controlled, same-origin, **no external account, no spend,
  no remotePatterns needed**. Phase A footprint ≈ 3–5 MB (~91 small thumbnails).
- Alt — **Vercel Blob** (free ≤1 GB) keeps the repo lean; better if Phase B (all 663,
  ~30–40 MB) is in scope. **External store + eventual spend → owner tripwire #4.**
- Proceeding with `/public` unless owner picks Blob/Cloudinary.

## Feasibility (verified)
- This local machine fetches Yochananof images (HTTP 200) — the optimizer can't, but a
  **local ingestion script can**. Pipeline runs locally; no datacenter-block problem.

## Pipeline (deterministic, local, traceable)
1. **Extract** — enumerate each retailer image URL + owning product barcode + source
   file → `work_manifest.json`.
2. **Download** — fetch locally; validate real raster (content-type + magic bytes +
   decodes, naturalWidth>0). On failure → **DISCARD** per missing-data rule (no
   fabrication; page keeps ✦ fallback) and log the miss. Never substitute OFF/any source.
3. **Normalize** — convert to WebP, cap ~256px (displayed ≤128px), strip EXIF; write
   `/public/products/<barcode>.webp`; dedupe by barcode.
4. **Provenance** — write `public/products/_provenance.json`:
   `barcode → {localPath, sourceUrl, host, fetchedAt, bytes}` (traceability; see
   [[corpus_traceability_program]]).
5. **Rewrite data** — scripted replace of `imageUrl`/`image_url` fields in the affected
   files: retailer URL → `/products/<barcode>.webp`.
6. **Re-apply frontend** — restore the reverted `next/image` change in
   `BariProductThumbnail` (local `/public` images optimize same-origin, no remotePatterns
   needed). Keep `res.cloudinary.com` in `remotePatterns` for the still-remote Phase-B
   588 so cheese keeps optimizing.
7. **Verify (gates)** —
   - `npm run build` green.
   - Each affected category on 390px mobile: 0 broken, all product imgs from
     `/_next/image`, 0 external hotlinks for migrated hosts.
   - **Blocker simulation** (acceptance test): block `**.co.il` + `res.cloudinary.com`
     in the browser; migrated images still render from `/public`.
   - Consumer-facing → Adversarial QA render pass.
8. **Ship** — commit (images + data + component + provenance), push `origin/master`,
   confirm Vercel deploy green, re-verify live milk on mobile.

## Rollback
Single revert of the data+component commit restores hotlinks; committed `/public`
images remain harmlessly.

## Scope / phases
- **Phase A (the actual fix, ~91 images):** Yochananof + supplement hosts. After this,
  ALL categories are blocker-proof (Shufersal-cloudinary already optimizes). Achieves DoD.
- **Phase B (asset ownership, 588 images):** re-host Shufersal-Cloudinary too, so Bari
  depends on nothing third-party. Optional; consider Vercel Blob at this scale.

## Owner flags
- Storage choice (only if not `/public`) → tripwire #4 (external/spend).
- Image-rights note: re-hosting retailer product photos for display — the site already
  displays them; continuation, not new exposure. Surfaced, not a blocker.

## Progress
- **2026-07-03 — Phase A SHIPPED & verified live.** 91 optimizer-incompatible images
  (Yochananof + supplement hosts) self-hosted as WebP under `public/products/` (876KB,
  0 discarded); 7 data files repointed; provenance manifest written; same-origin
  `next/image` component re-applied. Commits `ebea9187` + `5a11025f` on `origin/master`;
  Vercel deploy green. **Live acceptance test passed:** milk 18/18 and magnesium 17/17
  render same-origin from `/products/` on a 390px mobile viewport AND survive a simulated
  block of ALL external image hosts (0 broken). Ingestion tools committed under
  `bari-web/scripts/migrate-images-{fetch,rewrite}.mjs` (reusable for Phase B).
- **2026-07-03 — Phase B SHIPPED & verified live.** Self-hosted the remaining 589
  Shufersal-Cloudinary + CDN product images. **Every product image site-wide is now
  same-origin** — 680 total under `public/products/` (7.9MB), 0 discarded, 928 data
  references repointed, verified 0 external image URLs remain. Fetch tool generalized to
  all hosts + merges manifests across phases. Commit `eae897ce` on `origin/master`;
  Vercel green. **Live acceptance test (all external hosts blocked, 390px mobile):**
  cheese 47, milk 18, chocolate-tablets 35, hummus 35, magnesium 17 — all render from
  `/products/`, 0 broken.
- **DoD MET for both phases.** Bari depends on no third-party image host at request time.

## Related
Reverted Level-1 commit e9ab8171; build-unblock commit 120b3689; revert d6b0e252.
Memories: [[featured_card_stock_image_rule]], [[missing_data_discard_rule]],
[[corpus_traceability_program]], [[hebrew_shell_corruption_and_verify_gotchas]].
