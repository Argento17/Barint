# Rollout Risk Assessment v1

Scope: risks when scaling the current Maadanim comparison implementation from 1 category to 3 categories and then 10 categories.

## Current Baseline

Verified baseline:
- Maadanim production route exists at `src/app/hashvaot/maadanim/page.tsx`.
- Maadanim data exists at `src/data/comparisons/maadanim_frontend_v2.json`.
- `ProductTable` preserves corpus order.
- v2 expansion fields render through `ExpansionSection`.
- `comparisonContext` is integrated with the shared label `הקשר במדף`.

Important baseline caveat:
- At audit time, the Maadanim reference implementation, data, docs, registry, and QA assets appear as untracked files in `git status --short`. This is a rollout risk because the reference may not yet be committed/merged.

## Scale: 1 Category

| Risk | Class | Severity | Evidence | Assessment |
|---|---|---:|---|---|
| Reference implementation not committed | Regression risk | HIGH | `git status --short` lists `docs/comparison_ui_reference_v1.md`, `src/app/hashvaot/maadanim/`, shared components, `src/data/comparisons/`, and registry files as untracked | A clean checkout may not contain the reference. Rollout work could branch from an incomplete baseline. |
| Dev preview still exists beside production route | Architecture | LOW | `src/app/dev/preview/page.tsx` | Acceptable for smoke testing, but must not be treated as canonical. |
| `_calibration` remains in repo JSON | Data/model compatibility | LOW | Current corpus has `_calibration` on 1 product; loader strips it | Not user-facing, but indicates data export still includes internal fields. |
| Runtime validation absent | Data/model compatibility | MEDIUM | `loadComparisonCorpus()` strips fields but does not validate shape | Current corpus works; malformed future corpus can fail at render time. |

## Scale: 3 Categories

Target categories implied by rollout:
- Maadanim
- Bread
- Snacks

| Risk | Class | Severity | Evidence | Assessment |
|---|---|---:|---|---|
| Registry blocks additional ids | Architecture | HIGH | `ComparisonCategoryId = "maadanim"` in `src/lib/comparisons/registry/types.ts` | Bread/snack cannot join the registry or route factory without core type changes. |
| Bread still uses a standalone dashboard | Architecture | HIGH | `src/app/compare/bread-comparison/page.tsx` renders `BreadComparisonDashboard` | Bread rollout requires a data adapter and route migration; otherwise it will not match the reference IA or mobile shelf layout. |
| Snack production routes are disabled | Architecture | HIGH | `src/app/hashvaot/snack-bars/page.tsx` and `src/app/compare/snack-bars/page.tsx` call `notFound()` | Snack has no active production comparison route. |
| Snack engine exposes algorithm vocabulary | Data/model compatibility | HIGH | `src/lib/comparisons/snack-product-detail.ts`, `src/components/snack/product-card-grid.tsx`, `src/components/snack/map-section.tsx` expose NOVA/caps/score drivers | Reference says these terms must not appear in comparison UI copy. |
| Bread/snack are not `BariProductVM` | Data/model compatibility | HIGH | `BreadProduct` and `SnackProduct` are separate types | Shared Maadanim shelf cannot consume current bread/snack data directly. |
| Route families compete | Maintenance | MEDIUM | Maadanim is `/hashvaot/maadanim`; bread is `/compare/bread-comparison`; snack routes are disabled | QA, links, redirects, and navigation need one canonical route policy. |
| Filter model not page-VM driven | Maintenance | MEDIUM | Maadanim filters are in `maadanim-shelf-filters.ts`; `BariCategoryPageVM.filters` is unused | Manageable at 3 categories, but duplicated filter logic is likely. |
| `next.config.ts` image hosts may not cover new corpora | Regression risk | MEDIUM | Only Yochananof and Cloudinary Shufersal patterns are configured | Bread/snack image hosts need verification before build/deploy. |

## Scale: 10 Categories

| Risk | Class | Severity | Evidence | Assessment |
|---|---|---:|---|---|
| Category wrappers and page-data modules proliferate | Maintenance | HIGH | `MaadanimComparisonPage`, `maadanim-page-data.ts`, `maadanim-shelf-filters.ts` pattern | Without registry/factory discipline, each category may drift in shell, metadata, filters, and route behavior. |
| No runtime schema validation | Data/model compatibility | HIGH | `loadComparisonCorpus()` trusts JSON | With 10 corpora, a single missing `expansion`, bad `confidence`, duplicate id, or unsupported image host can break a route late. |
| Multiple comparison systems remain active | Architecture | HIGH | Bread, milk, snack, Maadanim all have separate systems | The team may maintain four product-row/score/expansion paradigms indefinitely. |
| Shared labels are hard-coded globally | Maintenance | MEDIUM | `ExpansionSection` owns labels/confidence/nutrients | Any category-specific label variation requires shared component changes or ad hoc branching. |
| Performance on long corpora is only partially verified | Performance | MEDIUM | `content-visibility` exists for collapsed rows; no virtualization found | 90 products works for Maadanim. Larger categories may need measurement, especially with Next `Image` rows and expansion state resets. |
| `ProductTable` remounts on filter changes | Regression risk | MEDIUM | `ComparisonShelfPage` passes `key={expandedProductId ?? "none"}` | This intentionally resets expansion, but at larger scale it may cause scroll/state churn. Needs QA with long lists. |
| Navigation/index not registry-driven | Maintenance | MEDIUM | `/hashvaot/page.tsx` manually imports milk/bread data/cards | Adding 10 categories manually increases stale card/link risk. |

## Risk Classification

### Architecture

High:
- Registry currently accepts only `"maadanim"`.
- Bread and snack are not on the reference shelf architecture.
- Snack routes are disabled; bread route is in `/compare`.

Medium:
- Route factory exists but is unused by Maadanim route and unusable for other ids until registry widens.
- Dev preview/API are Maadanim-only.

### Performance

Medium:
- Current row strategy probably handles 90 Maadanim products, but 200+ product categories are not verified.
- Images rely on Next remote config; new hosts can break optimized rendering.

Low:
- `content-visibility` helps collapsed rows.
- First two images are prioritized only, which is appropriate for the current shelf.

### Maintenance

High:
- Duplicate category systems make the canonical reference hard to enforce.

Medium:
- Filter logic is category-local and not `BariCategoryPageVM.filters`.
- Metadata/copy can drift between route files and page-data modules.
- Multiple score components exist.

### Data / Model Compatibility

High:
- Bread/snack data do not currently match `BariProductVM`.
- Snack current model and UI expose terms banned by the reference.

Medium:
- Loader lacks runtime validation.
- `BariCategoryPageVM` is defined but not the operational page shape.

### Regression Risk

High:
- Reference implementation is untracked at audit time.

Medium:
- Legacy routes and disabled routes can mislead QA.
- No verified bread/snack smoke tests on the reference shelf path.

## Rollout Gates Recommended Before Bread/Snack

These are cleanup/QA gates, not feature or UX redesign requests:

1. Commit or otherwise stabilize the Maadanim reference files before using them as rollout baseline.
2. Decide canonical route policy for bread/snacks (`/hashvaot/{category}`) and document redirects/notFound retirement.
3. Add bread/snack category ids to registry only when their data adapters output `BariProductVM[]`.
4. Verify bread/snack corpora contain v2 expansion fields or explicitly mark fields unavailable.
5. Run a production-route smoke test per category, not only `/dev/preview`.
6. Confirm no reference comparison route exposes NOVA, caps, BSIP, score drivers, or internal audit terminology.

## Not Verified

- No bread `src/data/comparisons/bread*_frontend_v2.json` found in repo.
- No snack `src/data/comparisons/snack*_frontend_v2.json` found in repo.
- No working snack production comparison route found.
- `DISTORTION-001` implementation not found in searched source/docs; status remains not verified.
