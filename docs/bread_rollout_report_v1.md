# Bread Rollout Report v1

**Date:** 2026-05-29  
**Production route:** `/hashvaot/bread`  
**Reference:** `docs/comparison_ui_reference_v1.md` (מעadנים frozen)

---

## 1. CE-approved sources located

No file named `bread_frontend_v2.json` existed before this rollout. CE-approved Bread content in the repo was identified as:

| File | Role |
|------|------|
| `src/data/bread-retail-curated.json` | Curated shelf (`real_bread_retail_003_v1`): 24 displayable products, scores, grades, Hebrew copy, shelf order in `all_products`, cluster ids |
| `src/data/bread-retail-shufersal.json` | Governance (`dataset_meta`, framing rules) + `ingredient_architecture_summary` / `short_summary_he` per product id |
| `src/lib/comparisons/bread-page-data.ts` | CE-stabilized `BREAD_CLUSTER_FILTERS` and blog/dashboard data |
| `src/lib/blog/bread-analysis-content.ts` | Comparison SEO metadata (`breadComparisonMeta`) |
| `src/components/comparisons/bread-comparison-dashboard.tsx` | CE hero + methodology copy (Hebrew shelf framing) |

`bread_frontend_v2.json` was **generated** by `scripts/build-bread-frontend-v2.mjs` using only verbatim field mapping from the sources above (no new product copy, no re-sorting).

---

## 2. Files added

| Path | Purpose |
|------|---------|
| `src/data/comparisons/bread_frontend_v2.json` | Canonical `BariProductVM[]` corpus (24 products) |
| `scripts/build-bread-frontend-v2.mjs` | Regenerate corpus from CE-approved JSON sources |
| `src/lib/comparisons/bread-comparison-page-data.ts` | Loader, hero/prologue/methodology, registry getters |
| `src/lib/comparisons/bread-shelf-filters.ts` | CE cluster lenses + filter logic |
| `src/components/comparisons/bread-comparison-page.tsx` | Thin wrapper over `ComparisonShelfPage` |
| `src/app/hashvaot/bread/page.tsx` | Production route |
| `src/lib/comparisons/registry/categories/bread.ts` | Registry entry |
| `docs/bread_rollout_report_v1.md` | This report |

---

## 3. Files changed

| Path | Change |
|------|--------|
| `src/lib/comparisons/registry/types.ts` | `ComparisonCategoryId` → `"maadanim" \| "bread"` |
| `src/lib/comparisons/registry/index.ts` | Register `bread` in `comparisonCategoryRegistry` |

**Not changed:** `src/app/hashvaot/maadanim/page.tsx`, `maadanim-comparison-page.tsx`, `maadanim-page-data.ts`, shared shelf components, scoring modules.

**Canonical cutover (2026-05-29):** see §13 below.

---

## 4. What worked unchanged from the platform

- `ComparisonShelfPage` orchestration (375px frame, filter state, first-row expand)
- `CategoryHero`, `CategoryPrologue`, `CategoryShelfLenses`, `ProductTable`, `ProductRow`, `ExpansionSection`, `MethodologyFooter`, `ScoreChip`
- `loadComparisonCorpus` / `formatComparisonMetadataLine` from `src/lib/comparisons/corpus.ts`
- Registry pattern (`getComparisonCategory`, `getPageData`, `getCorpusPayload`)
- Static build-time corpus import (no client fetch on production route)

---

## 5. Category-specific adaptation

| Area | Adaptation |
|------|------------|
| **Corpus build** | Map `bread-retail-curated` → `BariProductVM`; merge `ingredient_architecture_summary` from shufersal index by `product_id`; split `structural_summary_he` on `\|` into `positiveSignals` (verbatim segments only) |
| **Shelf order** | Preserved `all_products` filter order for `display_score_boolean === true` (not score-sorted) |
| **Product count** | 24 scored shelf rows (31 curated total; transparency / non-displayable excluded per curated flags) |
| **Filters** | Reused `BREAD_CLUSTER_FILTERS` labels (minus `all`); match via `website_cluster` from curated JSON; empty selection = full shelf |
| **Copy** | Hero/prologue/methodology taken from CE-stabilized dashboard hero + methodology block (Hebrew); metadata from `breadComparisonMeta` |
| **Internal field** | `_website_cluster` stored in corpus JSON, stripped before UI (not shown) |
| **Nutrition** | Partial grid: `protein`, `fiber`, `sodium` from curated; `energyKcal` / `sugar` / `fat` null where absent in source |
| **Ingredients** | `ingredient_architecture_summary` when present in shufersal data; otherwise `null` |

---

## 6. Shared components changed?

**No.** No edits to `comparison-shelf-page.tsx`, `category-*`, `product-*`, `expansion-section.tsx`, or `score-chip.tsx`.

---

## 7. Did `/hashvaot/maadanim` remain unchanged?

**Yes.** Maadanim route, page component, page-data module, and corpus were not modified. Registry typing was extended to include `bread` only; maadanim behavior and rendering are unchanged.

---

## 8. Corpus mapping rules (for regeneration)

Run: `node scripts/build-bread-frontend-v2.mjs`

| Source field | Target |
|--------------|--------|
| `product_id` | `id` |
| `name_he` | `name` |
| `image_url` | `imageUrl` |
| `score` / `grade` | rounded score / grade |
| `suggested_card_blurb_he` | `insightLine`, `expansion.bottomLine` |
| `why_featured_he` | `expansion.comparisonContext` |
| `structural_summary_he` (split `\|`) | `expansion.positiveSignals[]` |
| `confidence_label_he` | `expansion.confidenceLabel` + mapped `confidence` |
| `fiber_g`, `protein_g`, `sodium_mg` | `expansion.nutrition` |
| shufersal `ingredient_architecture_summary` | `expansion.ingredients` |

---

## 9. Known gaps / follow-ups

| Item | Severity | Notes |
|------|----------|-------|
| `BreadComparisonDashboard` still in repo (unused by public routes) | LOW | Quarantine or remove after link audit; blog may still reference dashboard-era UX in copy |
| No `limitingFactors` in source corpus | LOW | Expansion shows positive + bottom + context only where authored |
| Many products lack `ingredients` string | LOW | Shufersal summary covers subset; null hides ingredients block cells |
| Filter semantics: multi-select OR across clusters | LOW | Dashboard was single-select; shelf template allows multiple chips (union of clusters) |
| Corpus validation CI | HIGH | Not yet wired (`comparison_corpus_validation_plan_v1.md`) |
| Dedicated CE `bread_frontend_v2` export from audit pipeline | MEDIUM | Repo build script is interim; prefer checked-in export from content pipeline when available |

---

## 10. Before category 3 (Snacks) — recommended improvements

| Priority | Item |
|----------|------|
| **HIGH** | Produce `snacks_frontend_v2.json` from real audit export (not `snack-page-data.ts` fixtures) |
| **HIGH** | Retire / disable `SnackComparisonEngine` on production paths; use `ComparisonShelfPage` only |
| **HIGH** | Remove NOVA/caps/runtime-generated detail copy from snack shelf surfaces |
| **HIGH** | Add corpus validation script + CI gate before snacks launch |
| **MEDIUM** | Generalize `/api/dev/comparison/[categoryId]` for maadanim + bread + snacks QA |
| **MEDIUM** | Registry-driven `/hashvaot` index cards (bread cutover done via `BREAD_COMPARISON_HREF`) |
| **MEDIUM** | Author snack shelf lenses in `{category}-shelf-filters.ts` from CE cluster definitions |
| **LOW** | Optional `BreadComparisonPage` → registry factory only (already thin wrapper) |
| **LOW** | Align `ExpansionSection` to prefer `expansion.confidenceLabel` verbatim over shared confidence map (cross-category) |

---

## 11. Verification

- `npm run lint` — pass (pre-existing warnings only)
- `npm run build` — pass; `/hashvaot/bread` listed as static route
- Stack: `BreadComparisonPage` → `ComparisonShelfPage` → shared reference components (same as מעadנים)

---

## 12. Acceptance checklist

- [x] `/hashvaot/bread` uses `ComparisonShelfPage` stack only
- [x] Corpus under `src/data/comparisons/bread_frontend_v2.json`
- [x] `bread` registered in comparison registry
- [x] Shelf filters from CE `BREAD_CLUSTER_FILTERS`
- [x] No shared UI component changes
- [x] מעadנים route untouched
- [x] Legacy compare route redirects to `/hashvaot/bread`
- [x] `/hashvaot` index bread card → `/hashvaot/bread`
- [ ] Production QA screenshots on `/hashvaot/bread` (recommended)
- [ ] External inbound link audit (analytics, sitemap, newsletters)

---

## 13. Canonical route cutover (2026-05-29)

### Canonical public route

| Role | URL |
|------|-----|
| **Production comparison (canonical)** | `/hashvaot/bread` |
| Shared link constant | `BREAD_COMPARISON_HREF` → `/hashvaot/bread` (`src/lib/blog/bread-analysis-content.ts`) |

### Index link update

- `/hashvaot` (`src/app/hashvaot/page.tsx`) uses `FeaturedBreadIntelligenceCardLite` with `href={BREAD_COMPARISON_HREF}` — now resolves to `/hashvaot/bread`.
- Home category grid (`src/components/home/home-category-intelligence.tsx`) bread tile updated to the same constant.

### Legacy route handling

| Legacy path | Behavior after cutover |
|-------------|------------------------|
| `/compare/bread-comparison` | `redirect()` → `/hashvaot/bread` (replaces dashboard render) |
| `/compare/bread-shufersal` | `redirect()` → `/hashvaot/bread` (via `BREAD_COMPARISON_HREF`) |
| `/hashvaot/bread-comparison` | `redirect()` → `/hashvaot/bread` (via `BREAD_COMPARISON_HREF`) |

Next.js `redirect()` issues a temporary redirect by default in App Router; acceptable for in-app legacy cleanup. Use `redirect(path, "permanent")` only if product requests explicit 308/301 policy.

### Files changed in cutover

| Path | Change |
|------|--------|
| `src/lib/blog/bread-analysis-content.ts` | `BREAD_COMPARISON_HREF` → `/hashvaot/bread` |
| `src/app/compare/bread-comparison/page.tsx` | Legacy redirect shell (no `BreadComparisonDashboard`) |
| `src/components/home/home-category-intelligence.tsx` | Bread tile uses `BREAD_COMPARISON_HREF` |

### Risks / follow-up

| Risk | Mitigation |
|------|------------|
| Bookmarks to `/compare/bread-comparison` | Redirect preserves access |
| Blog CTAs using `ctaHref: "/comparisons/bread"` | Unchanged (separate path); audit if that route exists |
| Dashboard component drift | `bread-comparison-dashboard.tsx` unused on public routes — document or retire |
| מעadנים regression | No maadanim files touched in cutover |
