# Comparison Architecture Audit v1

Scope: internal QA audit for rolling the current Maadanim comparison implementation to bread and snack categories. This document is audit-only and does not request UI, scoring, or content changes.

Canonical reference checked:
- `docs/comparison_ui_reference_v1.md`
- `src/app/hashvaot/maadanim/page.tsx`
- `src/components/comparisons/maadanim-comparison-page.tsx`
- `src/components/comparisons/comparison-shelf-page.tsx`
- `src/data/comparisons/maadanim_frontend_v2.json`

## Current Architecture Snapshot

The Maadanim production path now uses the reference component stack:

```text
/hashvaot/maadanim
  -> MaadanimComparisonPage
    -> ComparisonShelfPage
      -> CategoryHero
      -> CategoryPrologue
      -> CategoryShelfLenses
      -> ProductTable
        -> ProductRow
          -> ExpansionSection
      -> MethodologyFooter
```

The route shell is `src/app/hashvaot/maadanim/page.tsx`. It imports Maadanim-specific copy and products from `src/lib/comparisons/maadanim-page-data.ts` and passes them into `MaadanimComparisonPage`.

The reusable shell is `src/components/comparisons/comparison-shelf-page.tsx`. It owns filter state, first-row expansion selection, the phone-frame wrapper, and composition of shared primitives.

The shared row/table primitives are:
- `src/components/shared/category-hero.tsx`
- `src/components/shared/category-prologue.tsx`
- `src/components/shared/category-shelf-lenses.tsx`
- `src/components/shared/product-table.tsx`
- `src/components/shared/product-row.tsx`
- `src/components/shared/expansion-section.tsx`
- `src/components/shared/methodology-footer.tsx`
- `src/components/shared/score-chip.tsx`

## Reusable vs Category-Specific Boundaries

### Reusable and aligned

| Area | Files | Audit finding |
|---|---|---|
| Shelf page shell | `src/components/comparisons/comparison-shelf-page.tsx` | Generic over filter id and accepts `BariProductVM[]`, copy, metadata line, and category filters. Suitable as the rollout shell. |
| Product order | `src/components/shared/product-table.tsx` | Maps `products` in array order. No client-side sorting found. This matches the reference rule that corpus owns order. |
| Row rendering | `src/components/shared/product-row.tsx` | Consumes `BariProductVM`, keeps layout category-neutral, and delegates expansion to `ExpansionSection`. |
| v2 expansion rendering | `src/components/shared/expansion-section.tsx` | Renders `positiveSignals`, `limitingFactors`, `bottomLine`, and `comparisonContext` in the expected order. `comparisonContext` label is `הקשר במדף`. |
| Data loader | `src/lib/comparisons/corpus.ts` | Provides shared metadata shape and strips `_calibration` from product payloads before UI. |

### Category-specific and acceptable

| Area | Files | Audit finding |
|---|---|---|
| Maadanim copy and metadata line | `src/lib/comparisons/maadanim-page-data.ts` | Category copy is isolated outside shared components. This is acceptable for one category. |
| Maadanim filters | `src/lib/comparisons/maadanim-shelf-filters.ts` | Filter ids, labels, and match rules are isolated. This matches the reference's temporary filter-isolation rule. |
| Maadanim wrapper | `src/components/comparisons/maadanim-comparison-page.tsx` | Thin wrapper around `ComparisonShelfPage`. This is acceptable, but can create wrapper proliferation if repeated for every category. |

## Hidden Coupling to Maadanim

| Coupling | Location | Evidence | Rollout risk |
|---|---|---|---|
| Registry only supports one category id | `src/lib/comparisons/registry/types.ts` | `ComparisonCategoryId = "maadanim"` | Bread/snack cannot be registered without changing core registry types. This blocks clean use of `createComparisonCategoryRoute`. |
| Registry contains only Maadanim | `src/lib/comparisons/registry/index.ts` | `comparisonCategoryRegistry = { maadanim: maadanimCategoryDefinition }` | Any multi-category listing or dev API built on the registry is currently single-category. |
| Dev API hard-coded to Maadanim | `src/app/api/dev/maadanim/route.ts` | Calls `getComparisonCategoryCorpusPayload("maadanim")` | Useful for Maadanim smoke testing only. Not a category-generic QA path. |
| Dev preview hard-coded to Maadanim | `src/app/dev/preview/page.tsx` | Fetches `/api/dev/maadanim` and renders `MaadanimComparisonPage` | Old preview cannot validate bread/snacks without duplication or rework. |
| Route metadata duplicated | `src/app/hashvaot/maadanim/page.tsx`, `src/lib/comparisons/maadanim-page-data.ts` | Route defines metadata inline while `maadanimComparisonMetadata` also exists | Creates a small drift risk if title/description are changed in one place only. |
| Category wrapper names | `src/components/comparisons/maadanim-comparison-page.tsx` | Maadanim-specific wrapper around a generic shell | Acceptable now, but 10 categories could produce redundant wrappers unless route factory/registry is adopted consistently. |

## Route Assumptions

| Route | Current behavior | Audit finding |
|---|---|---|
| `/hashvaot/maadanim` | Production Maadanim route | Verified present. Uses repo-owned data. |
| `/dev/preview` | Client fetch preview for Maadanim | Still present. Useful as a dev smoke path, but not production architecture. |
| `/api/dev/maadanim` | Returns Maadanim corpus payload | Still present. Optional dev API only. |
| `/hashvaot/bread-comparison` | Redirects to `BREAD_COMPARISON_HREF` | Bread is not on the reference shelf route. |
| `/compare/bread-comparison` | Renders `BreadComparisonDashboard` | Bread currently uses a standalone dashboard, not `ComparisonShelfPage`. |
| `/hashvaot/snack-bars` | `notFound()` | Snack comparison is not production-routable on `/hashvaot`. |
| `/compare/snack-bars` | `notFound()` | Snack comparison engine exists but route is disabled. |

## Hardcoded Strings, Labels, and Category Names

| Area | Location | Audit finding |
|---|---|---|
| Shared expansion labels | `src/components/shared/expansion-section.tsx` | Labels are hard-coded in the shared component. They match Maadanim reference now, but changing label policy later affects all categories. |
| Confidence labels | `src/components/shared/expansion-section.tsx` | Shared component maps `verified`, `partial`, `insufficient` to Hebrew labels instead of always rendering `expansion.confidenceLabel`. This may override category/corpus wording. |
| Nutrient labels | `src/components/shared/expansion-section.tsx` | `energyKcal`, `protein`, `sugar`, `fat`, `sodium` are hard-coded; `fiber` exists in `BariNutritionVM` but is not displayed. This may matter for bread/snacks if fiber is expected. |
| Maadanim copy | `src/lib/comparisons/maadanim-page-data.ts` | Category copy is isolated, which is good. It is not represented as `BariCategoryPageVM`. |
| Maadanim filter labels | `src/lib/comparisons/maadanim-shelf-filters.ts` | Filter labels and thresholds are category-local. Good isolation, but not scalable through `BariCategoryPageVM.filters` yet. |

## Data-Shape Assumptions

| Assumption | Location | Risk |
|---|---|---|
| Product VM fields are present and valid | `src/lib/comparisons/corpus.ts` | Loader strips `_calibration` but does not validate required `BariProductVM` fields or expansion subfields. Malformed bread/snack corpora could fail at render time. |
| `expansion` always exists | `ProductRow` -> `ExpansionSection` | Matches `BariProductVM`, but no runtime guard exists for bad JSON. |
| Product ids are unique | `ProductTable` | `product.id` is used as React key and expansion identity. No uniqueness validation found. |
| Image URLs are Next-compatible | `ProductRow` and `next.config.ts` | Current remote patterns allow `api.yochananof.co.il` and `res.cloudinary.com/shufersal/**`. New category image hosts will require config changes. |
| `generated` is parseable as Date | `formatComparisonMetadataLine()` | Invalid date falls back to "updated recently"; no build failure. Acceptable but hides corpus metadata errors. |
| Positive signals may be empty | Maadanim corpus | Current Maadanim has `positiveSignals` populated on 58/90 products and empty/absent on the rest; renderer handles this. |
| `_calibration` may exist in repo data | `src/data/comparisons/maadanim_frontend_v2.json` | Current repo corpus contains `_calibration` on 1 product; loader strips it. |

## Scaling Risks for New Categories

| Category scale | Expected pressure point |
|---|---|
| 1 category | Current architecture works for Maadanim. Main risk is that reference implementation is still untracked in git status at audit time. |
| 3 categories | Registry type, route creation, category data modules, filter modules, and index page linking all need a repeatable pattern. Bread/snack currently do not use the Maadanim VM shelf path. |
| 10 categories | Wrapper modules, per-category filters, metadata duplication, image host config, and absent runtime validation become significant maintenance risks. A typed registry plus corpus validation becomes important before this scale. |

## Verification Notes

- Verified: production Maadanim route exists.
- Verified: repo-owned Maadanim data exists at `src/data/comparisons/maadanim_frontend_v2.json`.
- Verified: `ProductTable` no longer sorts client-side.
- Verified: `comparisonContext` uses label `הקשר במדף`.
- Verified: bread and snack are not currently on the reference VM shelf architecture.
- Not verified: `DISTORTION-001` implementation. The audit search found reference guidance and QA scripts, but no implementation or explicit `DISTORTION-001` marker in `src` or `docs` at audit time.
