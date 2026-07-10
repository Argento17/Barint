---
id: TASK-427
title: Internal Inventory Dashboard (cross-category corpus rollup)
owner: orchestrator
status: CLOSED
priority: MEDIUM
final_audit: >
  2026-07-01 Design-Agent comprehensive audit (both pages, desktop+mobile): 18 checks PASS —
  zero horizontal overflow on mobile (incl. sidebar + open expansion), zero algorithm-vocab
  leakage in the reused ExpansionSection, brand green #167A58 5.29:1 AA, "עודכן השבוע" 5.75:1 AA,
  name-link/chevron independent, admin unchanged, zero console errors, sort works. Minor findings
  triaged: fixed sidebar sticky offset (header-relative) + added mobile category-strip scroll fade;
  dismissed false positives (RTL chevron direction is correct/matches reference; 1px header var).
  Residual optional follow-ups: bread/hummus brand enrichment (data re-scrape, no fabrication);
  per-product anchor deep-link on comparison pages; sitemap entry for /catalog. Deploy is owner-gated
  (consumer-facing, tripwire #2) — build complete + audited locally, not yet published.
reopened_note: >
  2026-07-01: owner reclassified /catalog to carry the FULL navy reference shell (header search +
  right sidebar), public, in the site nav — upgrading it from consumer chrome. Admin dashboard shares
  the same shell. Also corrected: live product count is 174 (not 196) — hummus's published corpus
  excludes 22 vegetable-spread items via getHummusCorpusPayload; the data agent's "196" was a raw-JSON
  count, the live registry-curated count of 174 is correct and matches the hummus comparison page.
  Local dev admin login enabled (.env.local ADMIN_PASSWORD=bari-dev, gitignored, dev-only).
close_reason: >
  Delivered + verified. Public /catalog (Server Component, no-auth, indexable) + internal /admin/inventory
  (auth-gated navy shell) both build clean (npm run build exit 0, tsc exit 0, all routes present, no /hashvaot
  regression). Data reconciles 196===196===196; snacks retailer recovered from real BSIP0 (0% "other"); nameHe
  self-contained per category. Design-Agent vision audit run: 2 CRITICAL WCAG failures (C1 buy-text, C2 green
  accent) + 11 geometry/token items fixed and RE-VERIFIED by orchestrator contrast computation (C1 5.99:1 white /
  5.78:1 zebra; C2 5.69:1 — all ≥4.5). Boundary clean (no scoring imports in client components). Residuals noted
  below (admin live-render, latent active-buy green, sitemap) are non-blocking follow-ups.
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Internal /admin dashboard + PUBLIC /catalog: total counts, retailer donut, top categories, browsable product table with grade chips. Data: retailer normalization + InventorySummaryVM/InventoryProductRowVM contract + 2 auth-gated endpoints + public-safe loader + self-contained category nameHe. Frontend: shared donut/top-categories/table components, navy admin shell (gated) + consumer /catalog (public), consumer nav change, dormant buy affordance. Display-only aggregation; no scoring change; additive/non-breaking.
---

# TASK-427 — Inventory Dashboard + Public Catalog (cross-category corpus rollup)

## Scope (evolved by owner during build)
- **Internal ops dashboard** at `/admin/inventory` (auth-gated, navy "Food Intelligence" shell) — the original brief.
- **Public consumer catalog** at `/catalog` (owner reclassified mid-build) — public Server Component, consumer chrome, reads the loader directly; 4 visible columns (מוצר · קטגוריה · ציון · רשת), SKU hidden, barcode retained as hidden scan-resolution key.
- **Consumer nav change** (`site-header.tsx`): killed מדריכים; order now `[קטלוג המוצרים→/catalog, בלוג→/blog, השוואות→/hashvaot]`.
- **Dormant buy affordance** per public row (`buyUrl` slot; inactive "לרכישה · בקרוב" now, future affiliate links).

## Verified (orchestrator, against artifacts)
- `npx tsc --noEmit` exit 0 (whole repo); `npm run build` exit 0, all routes generated, no regression to `/hashvaot/*`.
- Boundary clean: no scoring/registry/bsip imports in any client component; loader calls are server-only.
- Auth posture: `/catalog` public (no auth), `/admin/inventory` gated (session → redirect), both endpoints 401 without session.
- Reconciliation: Σ retailerBreakdown === Σ topCategories === totalProducts === 196; snacks retailer recovered from real BSIP0 (0% "other"); nameHe co-located per category (required field → new category can't ship unnamed).
- Fixed inline: admin dashboard was rendering only 100/196 products (pageSize cap) → now fetches all pages.

## Remaining before go-live close
- **Visual render audit** vs `bari-web/_design-ref/Bari Dashboard.dc.html` (Design-Agent vision pass) — code verified, live DOM/pixels not yet.
- `/catalog` not in `sitemap.ts` (add on public go-live).
- Note: current corpus is 100% Shufersal → donut is a single ring (truthful; diversifies with new chains).

## New-category onboarding path (owner asked)
Register the scraped category in the comparison registry (id + routePath + nameHe + corpus payload) — it appears in the catalog automatically (totals, donut, top-categories, table). Only extra possible touch: one line in the retailer map if a brand-new chain appears (else falls to "אחר" gracefully).
