# Snacks Post-Rollout Architecture Audit v1

Audit date: 2026-05-29  
Scope: `/hashvaot/maadanim` compared with `/hashvaot/snacks` in `C:\bari-web`  
Mode: audit only. No UI, scoring, or content changes.

## Verdict

Snacks successfully scaled the core comparison shelf architecture without changing the shared shelf UI. The live Snacks route uses the same canonical shell as Maadanim:

`CategoryHero -> CategoryPrologue -> CategoryShelfLenses -> ProductTable -> ProductRow -> ExpansionSection -> MethodologyFooter`

The main architecture drift is not in the visible UI. It is in category data sourcing and operational coupling: Snacks still imports filter, hero, and methodology inputs from older snack/blog modules, and a deprecated generator still targets the canonical Snacks JSON path.

## Evidence Map

| Area | Maadanim | Snacks | Finding |
|---|---|---|---|
| Production route | `src/app/hashvaot/maadanim/page.tsx` | `src/app/hashvaot/snacks/page.tsx` | Both routes render a category wrapper page. |
| Category wrapper | `src/components/comparisons/maadanim-comparison-page.tsx` | `src/components/comparisons/snacks-comparison-page.tsx` | Both wrappers are thin adapters over `ComparisonShelfPage`. |
| Shared shell | `src/components/comparisons/comparison-shelf-page.tsx` | `src/components/comparisons/comparison-shelf-page.tsx` | Same shared component tree used by both categories. |
| Product table | `src/components/shared/product-table.tsx` | `src/components/shared/product-table.tsx` | Shared table. Display order remains corpus-owned. |
| Product row | `src/components/shared/product-row.tsx` | `src/components/shared/product-row.tsx` | Shared row UI. |
| Expansion | `src/components/shared/expansion-section.tsx` | `src/components/shared/expansion-section.tsx` | Shared v2 expansion UI. |
| Data file | `src/data/comparisons/maadanim_frontend_v2.json` | `src/data/comparisons/snacks_frontend_v2.json` | Both use repo-owned v2 JSON through category page-data modules. |
| Data loader | `src/lib/comparisons/maadanim-page-data.ts` | `src/lib/comparisons/snacks-comparison-page-data.ts` | Both call `loadComparisonCorpus`. |
| Registry | `src/lib/comparisons/registry/categories/maadanim.ts` | `src/lib/comparisons/registry/categories/snacks.ts` | Both are present in the comparison registry. |
| Legacy route handling | N/A in this audit | `src/app/hashvaot/snack-bars/page.tsx`, `src/app/compare/snack-bars/page.tsx` | Legacy snack-bar routes redirect to `/hashvaot/snacks`. |

## Shared Components Used

- `src/components/comparisons/comparison-shelf-page.tsx`
- `src/components/shared/category-hero.tsx`
- `src/components/shared/category-prologue.tsx`
- `src/components/shared/category-shelf-lenses.tsx`
- `src/components/shared/product-table.tsx`
- `src/components/shared/product-row.tsx`
- `src/components/shared/expansion-section.tsx`
- `src/components/shared/methodology-footer.tsx`
- `src/lib/comparisons/load-comparison-corpus.ts`
- `src/lib/comparisons/types.ts`
- `src/lib/comparisons/registry/index.ts`
- `src/lib/comparisons/registry/types.ts`

## Confirmed Parity

- Snacks route uses `SnacksComparisonPage -> ComparisonShelfPage`.
- Maadanim route uses `MaadanimComparisonPage -> ComparisonShelfPage`.
- Both category wrappers pass products, hero copy, prologue copy, methodology copy, and shelf filters into the shared shell.
- `ProductTable` does not own ranking or sorting. Snacks product order was verified as score-descending/non-increasing across all 18 products in `snacks_frontend_v2.json`.
- The shared `ExpansionSection` renders the v2 reasoning fields:
  - `positiveSignals`
  - `limitingFactors`
  - `bottomLine`
  - `comparisonContext`
- Snacks product-level corpus scan found no product-level forbidden vocabulary exposure for `BSIP`, `NOVA`, `cap`, `caps`, `dimension`, `GSS`, `ferm_q`, `fiber_q`, `routing`, `audit trace`, or `scoring engine`.

## Deviations

| Deviation | Location | Impact |
|---|---|---|
| Snacks page metadata is exported from the category data module, while Maadanim defines metadata inline in the route. | `src/app/hashvaot/snacks/page.tsx`, `src/app/hashvaot/maadanim/page.tsx` | Low architecture drift. The Snacks pattern is cleaner and registry-aligned. |
| Snacks strips `_internal_cluster` in the category page-data module after loading the corpus. | `src/lib/comparisons/snacks-comparison-page-data.ts` | Category-specific internal-field handling is still local, not standardized. |
| Snacks has no ingredients and no populated nutrition values in the visible technical block, although every product has a nutrition object. | `src/data/comparisons/snacks_frontend_v2.json` | Shared UI handles this, but category parity with Maadanim is lower. |
| Snacks prologue and metadata expose a selected display cohort of 18 products from 53 scanned and 48 scored products. | `src/lib/comparisons/snacks-comparison-page-data.ts` | Governance depends on keeping selected-cohort language explicit. |
| Snacks rollout documentation still contains stale 14-row language. | `docs/snacks_rollout_report_v1.md` | Documentation drift can mislead QA and future rollout work. |

## Hidden Coupling

| Coupling | Location | Risk |
|---|---|---|
| Shelf filters are derived from legacy snack filters and product objects. | `src/lib/comparisons/snacks-shelf-filters.ts`, `src/lib/comparisons/snack-page-data.ts` | If CE corpus product IDs diverge from legacy `snackProducts`, filtered views silently omit products. |
| Snacks hero copy imports `snackHeroLine` from the legacy snack page data module. | `src/lib/comparisons/snacks-comparison-page-data.ts`, `src/lib/comparisons/snack-page-data.ts` | Category comparison copy is not fully self-contained. |
| Snacks methodology copy imports from blog analysis content. | `src/lib/comparisons/snacks-comparison-page-data.ts`, `src/lib/blog/snack-analysis-content.ts` | Shelf methodology depends on a blog module that also owns non-shelf analysis copy. |
| Deprecated Snacks generator still writes to the canonical v2 JSON path if run. | `scripts/build-snacks-frontend-v2.ts` | High operational risk. It can overwrite the CE v2 corpus with deprecated mapping behavior. |

## Duplicated Logic

| Duplicate pattern | Files | Assessment |
|---|---|---|
| Thin category wrappers over `ComparisonShelfPage`. | `maadanim-comparison-page.tsx`, `snacks-comparison-page.tsx`, `bread-comparison-page.tsx` | Acceptable at 2 categories, likely repetitive by 5 to 10 categories. |
| Category page-data loaders. | `maadanim-page-data.ts`, `snacks-comparison-page-data.ts`, `bread-comparison-page-data.ts` | Useful boundary, but internal-field stripping, metadata-line construction, and filter guards are repeated. |
| Category shelf filters. | `maadanim-shelf-filters.ts`, `snacks-shelf-filters.ts`, `bread-shelf-filters.ts` | The pattern is valid, but Snacks specifically depends on legacy product data. |
| Legacy and canonical comparison route systems. | `src/app/compare/*`, `src/app/hashvaot/*` | Legacy routes redirect for Snacks and Bread, but old code paths still add review burden. |

## Architecture Compliance Result

Snacks is compliant with the frozen comparison shelf architecture at the UI-shell level. The platform did not fork into a separate Snacks UI. The readiness issue before additional categories is operational standardization: category modules need to become self-contained, deprecated corpus writers need to be neutralized, and validation needs to move from manual audit to repeatable script.
