# Duplicate Systems Audit v1

Scope: duplicated or competing systems that overlap with the current Maadanim comparison-template reference before rollout to bread and snacks.

## Summary

Maadanim is the only category currently implemented on the new `BariProductVM` shelf path. Bread, milk, and snacks still have category-specific comparison/product systems. Some are active production routes, some are disabled/not-found routes, and some are support/blog systems. Left untouched, these systems create architectural drift and make it unclear which comparison implementation is canonical.

## Duplicates and Overlaps

| File/path | Overlaps with | Keep / consolidate / retire | Risk if left untouched |
|---|---|---|---|
| `src/components/comparisons/bread-comparison-dashboard.tsx` | `ComparisonShelfPage`, `ProductTable`, `ProductRow`, `ScoreChip`, `ExpansionSection` | Consolidate for bread rollout. Keep only as legacy/reference until bread is migrated. | Bread will ship with a different IA, route pattern, data model, score display, and row behavior than Maadanim. |
| `src/app/compare/bread-comparison/page.tsx` | `/hashvaot/{category}` route pattern | Consolidate route to reference pattern or document as legacy redirect target. | Users and links may continue to treat `/compare/...` as canonical while Maadanim uses `/hashvaot/...`. |
| `src/app/hashvaot/bread-comparison/page.tsx` | Production comparison route path | Retire or replace after bread migration. | Redirect layer hides actual canonical route ownership. |
| `src/app/compare/bread-shufersal/page.tsx` | Bread comparison route | Retire after link audit if unused. | Extra legacy route increases QA matrix and broken-link risk. |
| `src/lib/comparisons/bread-types.ts` | `BariProductVM` / `BariExpansionVM` | Consolidate via adapter/export to `BariProductVM` for rollout. | Bread-specific raw model prevents direct use of shared row/table/expansion components. |
| `src/lib/comparisons/bread-page-data.ts` | `maadanim-page-data.ts`, `corpus.ts`, category registry | Consolidate data loading pattern. | Bread data transforms, filters, score observations, and copy remain bespoke and difficult to compare against reference. |
| `src/components/bread/bread-shelf-product-image.tsx` | `ProductRow` image rendering | Keep only if needed as adapter input or retire after migration. | Duplicate image behavior and fallback styling. |
| `src/components/bread/bread-confidence-pill.tsx` | `ExpansionSection` confidence footer | Consolidate if bread migrates to `BariProductVM.confidence`. | Different confidence vocabulary and styling may remain. |
| `src/components/comparisons/snack-comparison-engine.tsx` | `ComparisonShelfPage`, `CategoryShelfLenses`, `ProductTable`, `ExpansionSection` | Retire or quarantine unless snack rollout intentionally keeps it as non-reference legacy. | Snack rollout may accidentally revive a non-reference engine with search, maps, modal details, exposed NOVA/caps, and client sorting. |
| `src/app/hashvaot/snack-bars/page.tsx` | Production comparison route path | Replace for rollout; currently disabled with `notFound()`. | Route appears present but is not usable. |
| `src/app/compare/snack-bars/page.tsx` | Legacy comparison route path | Retire or redirect after rollout decision. Currently disabled with `notFound()`. | Route confusion and QA ambiguity. |
| `src/components/snack/product-card-grid.tsx` | `ProductTable` / `ProductRow` | Retire from comparison route or keep as blog-only if explicitly scoped. | Competing product presentation model; not mobile phone-frame shelf table. |
| `src/components/snack/snack-product-detail-panel.tsx` | `ExpansionSection` | Retire from comparison route or keep as blog-only if explicitly scoped. | Competing expansion/detail model; exposes score drivers and algorithm terms. |
| `src/components/snack/snack-score-chip.tsx` | `src/components/shared/score-chip.tsx` and `src/components/comparisons/bari-grade-badge.tsx` | Consolidate score display for comparison routes. | Multiple grade styles and null-score language. |
| `src/components/snack/why-this-landed-here.tsx` | `ExpansionSection` v2 interpretive sections | Retire from comparison route or map to v2 fields. | Uses snack-specific sections and can diverge from positive/limiting/bottom/context order. |
| `src/lib/comparisons/snack-types.ts` | `BariProductVM` / `BariExpansionVM` | Consolidate through a snack VM export before rollout. | Snack remains coupled to NOVA/caps fields not allowed in reference UI copy. |
| `src/lib/comparisons/snack-page-data.ts` | Repo-owned v2 comparison JSON pattern | Retire or replace with `src/data/comparisons/snack-bars_frontend_v2.json` equivalent. | Hard-coded product fixture data and algorithm vocabulary can leak into production. |
| `src/lib/comparisons/snack-product-detail.ts` | v2 pre-authored expansion text | Retire from comparison route. | Generates UI explanations from model fields at runtime and exposes caps/NOVA/score mechanics. |
| `src/components/comparisons/milk-comparison-page.tsx` | Reference shelf page and shared row components | Keep as existing legacy until explicitly migrated; not in this bread/snack rollout. | Continued third comparison architecture increases drift and maintenance overhead. |
| `src/lib/comparisons/milk-types.ts` and `src/lib/comparisons/milk-page-data.ts` | `BariProductVM` / registry pattern | Keep as legacy unless milk migration is planned. | Multiple data contracts coexist. |
| `src/components/comparisons/bari-grade-badge.tsx` | `ScoreChip`, `SnackScoreChip` | Consolidate for comparison routes or scope to legacy milk/blog views. | Three score-display systems can diverge visually and semantically. |
| `src/lib/comparisons/comparison-product.ts` | `BariProductVM`, `BreadProduct`, `SnackProduct`, `MilkComparisonProduct` | Retire if unused. | Adds another generic-sounding product type that is not the canonical VM. |
| `src/app/dev/preview/page.tsx` | Production `/hashvaot/maadanim` and route factory | Keep only as dev QA if documented; do not use for rollout architecture. | Client-fetch path can mask static route/build-time issues. |
| `src/app/api/dev/maadanim/route.ts` | Static import production data path | Keep only as dev API if documented. | Single-category dev API can be mistaken for production data path. |
| `scripts/capture-maadanim-expansions.mjs` | `scripts/qa-maadanim-production.mjs` | Update or retire after QA path consolidation. | Still defaults to `/dev/preview`, so screenshots may test old preview rather than production route. |

## Old Preview / Dev Implementations

| File/path | Status | Audit note |
|---|---|---|
| `src/app/dev/preview/page.tsx` | Active dev route | Now reuses `MaadanimComparisonPage` and `/api/dev/maadanim`, but remains Maadanim-only. |
| `src/app/api/dev/maadanim/route.ts` | Active dev API | Uses registry payload rather than external `C:\Bari` file. Good cleanup, but still hard-coded to Maadanim. |
| `scripts/capture-maadanim-expansions.mjs` | QA helper | Defaults to `http://localhost:3000/dev/preview`; this can miss production-route regressions. |
| `scripts/qa-maadanim-production.mjs` | QA helper | Production-specific script exists, but audit did not validate its latest output. |

## Competing Data Types

| Type | Location | Relationship to canonical VM |
|---|---|---|
| `BariProductVM` | `src/lib/view-models/index.ts` | Canonical product row contract. |
| `BariCategoryPageVM` | `src/lib/view-models/index.ts` | Defined but not used by Maadanim page data or `ComparisonShelfPage`. |
| `ComparisonCategoryPageData` | `src/lib/comparisons/registry/types.ts` | Current operational category page shape. Similar to but not the same as `BariCategoryPageVM`. |
| `BreadProduct` | `src/lib/comparisons/bread-types.ts` | Legacy bread-specific model. |
| `SnackProduct` | `src/lib/comparisons/snack-types.ts` | Legacy snack-specific model with NOVA/caps fields. |
| `MilkComparisonProduct` | `src/lib/comparisons/milk-types.ts` | Legacy milk-specific model. |
| `ComparisonProduct` | `src/lib/comparisons/comparison-product.ts` | Generic-looking type; no active runtime use found in audit search. |

## Keep / Consolidate / Retire Recommendation

| Recommendation | Items |
|---|---|
| Keep as canonical | `ComparisonShelfPage`, shared category/product components, `BariProductVM`, `corpus.ts`, Maadanim production route/data. |
| Consolidate before bread rollout | Bread route, bread data adapter, bread filters, bread product row/table/score display. |
| Consolidate before snack rollout | Snack data source, snack route, snack filters, snack score display, snack detail/expansion logic. |
| Retire or quarantine | Disabled snack routes if not part of rollout, old `/compare` routes after canonical redirects are set, unused `ComparisonProduct`, dev preview scripts that test `/dev/preview` instead of production. |

## Not Verified

- Whether any external links or analytics depend on `/compare/snack-bars`, `/hashvaot/snack-bars`, `/compare/bread-shufersal`, or `/compare/bread-comparison`.
- Whether `DISTORTION-001` is documented outside the files searched by this audit.
- Whether snack/bread v2 JSON corpora already exist outside `src/data`.
