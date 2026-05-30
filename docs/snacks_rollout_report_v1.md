# Snacks Rollout Report v1

**Date:** 2026-05-29  
**Production route:** `/hashvaot/snacks`  
**Reference:** `docs/comparison_ui_reference_v1.md` (מעadנים frozen)

---

## 1. CE-approved sources located

No dedicated `snacks_frontend_v2.json` or standalone snacks retail JSON export existed before this rollout. CE-approved Snacks content in the repo was identified as:

| File | Role |
|------|------|
| `src/lib/comparisons/snack-page-data.ts` | Product fixtures (`snk-001`…`snk-016`), scores, Hebrew observations, cluster ids, `SNACK_FILTERS`, `SNACK_REPORT_STATS` |
| `src/lib/comparisons/snack-types.ts` | Product / filter types |
| `src/lib/blog/snack-editorial-content.ts` | Shelf intro, hero line, flagship editorial (blog only) |
| `src/lib/blog/snack-analysis-content.ts` | Comparison href, SEO metadata, shelf methodology lines (NOVA-free) |

`snacks_frontend_v2.json` was **generated** by `scripts/build-snacks-frontend-v2.ts` using only field mapping from `snack-page-data.ts` displayable rows (array order preserved; NOVA/cap tags stripped from `positiveSignals`).

**Corpus gap:** `SNACK_REPORT_STATS` documents 53 scraped / 48 scored products, but `snack-page-data.ts` currently contains **16 products (14 displayable)**. A full CE retail JSON export (analogous to `bread-retail-curated.json`) was **not found** in the repo.

---

## 2. Files added

| Path | Purpose |
|------|---------|
| `src/data/comparisons/snacks_frontend_v2.json` | Canonical `BariProductVM[]` corpus (14 displayable products at generation) |
| `scripts/build-snacks-frontend-v2.ts` | Regenerate corpus from `snack-page-data.ts` |
| `src/lib/comparisons/snacks-comparison-page-data.ts` | Loader, hero/prologue/methodology, registry getters |
| `src/lib/comparisons/snacks-shelf-filters.ts` | CE lens labels (NOVA/insufficient excluded) + `snackMatchesFilter` logic |
| `src/components/comparisons/snacks-comparison-page.tsx` | Thin wrapper over `ComparisonShelfPage` |
| `src/app/hashvaot/snacks/page.tsx` | Production route |
| `src/lib/comparisons/registry/categories/snacks.ts` | Registry entry |
| `docs/snacks_rollout_report_v1.md` | This report |

---

## 3. Files changed

| Path | Change |
|------|--------|
| `src/lib/comparisons/registry/types.ts` | `ComparisonCategoryId` → `"maadanim" \| "bread" \| "snacks"` |
| `src/lib/comparisons/registry/index.ts` | Register `snacks` |
| `src/lib/blog/snack-analysis-content.ts` | `SNACK_COMPARISON_HREF`, shelf methodology, flagship exports |
| `src/lib/comparisons/snack-page-data.ts` | Re-export comparison href/meta from snack-analysis |
| `src/app/hashvaot/snack-bars/page.tsx` | Redirect → `/hashvaot/snacks` |
| `src/app/compare/snack-bars/page.tsx` | Redirect → `/hashvaot/snacks` |
| `src/app/hashvaot/page.tsx` | Snacks link card in ניתוח עדכני |
| `src/components/home/home-category-intelligence.tsx` | Bars tile → זמין, `/hashvaot/snacks` |

**Not changed:** `/hashvaot/maadanim`, `/hashvaot/bread` routes and page modules, shared shelf components, maadanim/bread corpora.

---

## 4. Shared components changed?

**No.** No edits to `comparison-shelf-page.tsx`, `category-*`, `product-*`, `expansion-section.tsx`, or `score-chip.tsx`.

---

## 5. Maadanim and bread unchanged?

**Yes.** Maadanim and bread routes, page components, page-data modules, and corpora were not modified. Registry typing was extended to include `snacks` only.

---

## 6. Shelf architecture

- Route uses `SnacksComparisonPage` → `ComparisonShelfPage` (same orchestrator as מעadנים / bread).
- Filters: CE `SNACK_FILTERS` minus `all`, `nova2`/`nova3`/`nova4`, `insufficient` (reference UI: no NOVA chip labels).
- Filter matching reuses `snackMatchesFilter` from `snack-page-data.ts`.

---

## 7. Corpus mapping (regeneration)

Run: `npx tsx scripts/build-snacks-frontend-v2.ts`

| Source field | Target |
|--------------|--------|
| `id` | `id` |
| `name_he` | `name` |
| `image_url` | `imageUrl` |
| `score` / `grade` | rounded score / grade |
| `key_observation_he` | `insightLine`, `expansion.bottomLine` |
| `explainability_tags` (NOVA/cap filtered) | `expansion.positiveSignals` |
| `segment` | `expansion.comparisonContext` |
| `confidence_level` | `confidence` |
| `confidence_label_he` | `expansion.confidenceLabel` |
| `cluster_id` | `_internal_cluster` (stripped before UI) |

Nutrition and ingredients: `null` (not present in snack fixtures).

---

## 8. Legacy redirects

| Legacy path | Target |
|-------------|--------|
| `/hashvaot/snack-bars` | `/hashvaot/snacks` |
| `/compare/snack-bars` | `/hashvaot/snacks` |

---

## 9. Lint / build

- **`npm run lint`:** pass (0 errors, 9 pre-existing warnings)
- **`npm run build`:** pass after `servingNote` aligned to `BariProductVM` (`ל-100 גרם`)

---

## 10. Blockers before product-live

| Priority | Blocker |
|----------|---------|
| **HIGH** | Full CE snacks retail corpus (53 / 48 scored products) not in repo — shelf shows **14** displayable rows until `snack-page-data` or a dedicated JSON export is completed |
| **HIGH** | Stats copy (`SNACK_REPORT_STATS`, prologue “53 מוצרים”) vs shelf row count mismatch until corpus is complete |
| **MEDIUM** | No per-product `ingredients` / nutrition grid in source — expansion panels are observation-only |
| **MEDIUM** | Legacy `snack-comparison-engine.tsx` and blog flagship still reference NOVA in editorial; shelf route does not |
| **LOW** | No dedicated `FeaturedSnacksIntelligenceCardLite` on `/hashvaot` (text link card only) |

---

## 11. Verdict

**Route and platform wiring:** shipped at `/hashvaot/snacks` on frozen comparison shelf architecture.

**Full CE shelf parity:** blocked on missing full product export; partial `snack-page-data.ts` fixtures are not equivalent to `bread-retail-curated.json` completeness.
