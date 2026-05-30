# Comparison Registry Expansion Plan v1

**Status:** Planning only — no implementation.  
**Date:** 2026-05-29  
**Current registry:** `src/lib/comparisons/registry/` — `ComparisonCategoryId = "maadanim"` only.

---

## 1. Purpose

The registry is the **single registration point** for categories that use the frozen shelf comparison platform (`ComparisonShelfPage` + `BariProductVM` corpora). Expanding it to `maadanim`, `bread`, and `snacks` must not reintroduce legacy dashboard/engine types into shared contracts.

---

## 2. Current state

### 2.1 Files

```
src/lib/comparisons/registry/
  types.ts                 # ComparisonCategoryId, ComparisonCategoryDefinition
  index.ts                 # comparisonCategoryRegistry, getters
  categories/
    maadanim.ts            # wires maadanim-page-data
```

### 2.2 Contract (`ComparisonCategoryDefinition`)

Each category exposes:

| Member | Purpose |
|--------|---------|
| `id` | Registry key |
| `routePath` | Template literal `/hashvaot/${string}` |
| `metadata` | Next.js `Metadata` |
| `getPageData()` | Products, copy, metadata line, `shelfFilters` |
| `getCorpusPayload()` | `{ _meta, products }` for dev API |

### 2.3 Gaps

- Only `maadanim` is registered.
- `ComparisonCategoryId` is a single-literal union — TypeScript blocks other ids at compile time.
- Dev API (`/api/dev/maadanim`) is category-hardcoded in path and handler.
- `createComparisonCategoryRoute()` exists but cannot be used for bread/snacks until registry expands.
- `BariCategoryPageVM` in `view-models` is **not** the operational registry shape (filters, hero structure differ).

---

## 3. Target registry structure

### 3.1 Category ids and routes

| Category | Proposed `ComparisonCategoryId` | Canonical `routePath` | Notes |
|----------|--------------------------------|------------------------|-------|
| מעדנים | `maadanim` | `/hashvaot/maadanim` | **Frozen reference** — do not change behavior |
| לחם | `bread` | `/hashvaot/bread` | New; see `bread_migration_plan_v1.md` |
| חטיפים | `snacks` | `/hashvaot/snacks` | Align slug with product language; avoid `snack-bars` in canonical path |

**Slug rule:** One English slug per category under `/hashvaot/`, stable forever. Legacy paths redirect here.

### 3.2 Registry map (target)

```typescript
const comparisonCategoryRegistry = {
  maadanim: maadanimCategoryDefinition,
  bread: breadCategoryDefinition,
  snacks: snacksCategoryDefinition,
} as const satisfies Record<ComparisonCategoryId, ComparisonCategoryDefinition>;
```

Each definition file lives in `registry/categories/{id}.ts` and imports **only** from:

- `{category}-page-data.ts`
- `{category}-shelf-filters.ts` (indirectly via page data)

No imports from `bread-comparison-dashboard`, `snack-comparison-engine`, or milk modules.

### 3.3 Directory layout (target)

```
src/lib/comparisons/registry/
  types.ts
  index.ts
  categories/
    maadanim.ts
    bread.ts
    snacks.ts
```

Optional later:

```
registry/
  dev.ts                 # getDevCorpusPayload(id)
  list-public-categories.ts   # for /hashvaot index cards
```

---

## 4. Required type changes

### 4.1 `ComparisonCategoryId`

```typescript
export type ComparisonCategoryId = "maadanim" | "bread" | "snacks";
```

Use `as const` registry object so `keyof typeof comparisonCategoryRegistry` stays in sync.

### 4.2 Filter typing strategy

**Problem:** `MaadanimShelfFilterId` is a strict union; registry `getPageData()` is typed as `ComparisonCategoryPageData<string>` with a string guard wrapper for filters.

**Target approach (recommended):**

```typescript
export interface ComparisonCategoryDefinition<
  TFilterId extends string = string,
> {
  id: ComparisonCategoryId;
  routePath: `/hashvaot/${string}`;
  metadata: Metadata;
  getPageData: () => ComparisonCategoryPageData<TFilterId>;
  getCorpusPayload: () => { _meta: ComparisonCorpusMeta; products: BariProductVM[] };
}
```

Registry aggregate type:

```typescript
export type AnyComparisonCategoryDefinition =
  | ComparisonCategoryDefinition<MaadanimShelfFilterId>
  | ComparisonCategoryDefinition<BreadShelfFilterId>
  | ComparisonCategoryDefinition<SnacksShelfFilterId>;

const comparisonCategoryRegistry: Record<
  ComparisonCategoryId,
  AnyComparisonCategoryDefinition
>;
```

**Alternative (simpler):** Keep `TFilterId = string` everywhere in registry exports; category-specific unions stay in `{category}-shelf-filters.ts` only. Reduces type complexity; slightly weaker compile-time safety.

### 4.3 Optional metadata extensions

Add non-breaking optional fields to `ComparisonCorpusMeta`:

```typescript
interface ComparisonCorpusMeta {
  generated: string;
  category: string;
  product_count: number;
  // optional: retailer, scope_note, production_pass, version
}
```

No UI impact — documentation and validation only.

### 4.4 Public category listing type

For `/hashvaot` index and sitemaps:

```typescript
export interface ComparisonCategoryListing {
  id: ComparisonCategoryId;
  routePath: `/hashvaot/${string}`;
  title: string;           // from metadata.title
  description: string;     // from metadata.description
  productCount: number;    // from corpus meta
  status: "live" | "preview" | "planned";
}
```

`listComparisonCategories()` returns listings without calling heavy `getPageData()` if counts come from `_meta` only.

### 4.5 Alignment with `BariCategoryPageVM` (future)

| `BariCategoryPageVM` | `ComparisonCategoryPageData` today |
|----------------------|-----------------------------------|
| `hero: BariHeroVM` | `hero: { eyebrow, title }` + separate `metadataLine` |
| `filters: BariFilterVM[]` with counts | `shelfFilters` without counts |
| `methodology: BariMethodologyVM` | `methodologyLines: readonly string[]` |

**Plan:** Do not merge types in bread/snacks rollout. Add adapter `toCategoryPageVM(pageData)` only when migrating to VM-driven filters. Registry remains source of truth for rollout.

---

## 5. Route ownership model

### 5.1 Principles

1. **Registry owns** category id, canonical path, metadata, data getters.
2. **Route file owns** Next.js export (`metadata`, default page) — thin shell only.
3. **ComparisonShelfPage owns** client orchestration — never category names.
4. **Category modules own** corpus path, copy, filter rules.

### 5.2 Route implementation patterns

**Pattern A — Explicit route (מעadנים today, recommended for frozen reference)**

```text
src/app/hashvaot/maadanim/page.tsx
  imports maadanim-page-data + MaadanimComparisonPage
```

Stable, auditable, zero indirection for reference category.

**Pattern B — Registry factory (new categories)**

```text
src/app/hashvaot/bread/page.tsx
  export const { metadata, default } = createComparisonCategoryRoute("bread");
```

Or destructure `ComparisonCategoryRoute` + `metadata` from factory.

**Pattern C — Dynamic segment (defer)**

```text
src/app/hashvaot/[category]/page.tsx
```

Not recommended until ≥3 categories stable — risks accidental exposure of unlaunched ids and complicates static generation.

### 5.3 Ownership table

| Concern | Owner |
|---------|--------|
| URL | `ComparisonCategoryDefinition.routePath` |
| SEO metadata | `ComparisonCategoryDefinition.metadata` |
| Static generation | Route file imports corpus at build time via `getPageData()` |
| Client UI | `ComparisonShelfPage` + optional `{Category}ComparisonPage` wrapper |
| Dev corpus API | Registry `getCorpusPayload(id)` — path TBD: `/api/dev/comparison/[categoryId]` |

### 5.4 Wrapper components

| Category | Wrapper | Required? |
|----------|---------|-----------|
| maadanim | `MaadanimComparisonPage` | Keep for reference stability |
| bread | `BreadComparisonPage` | Optional thin wrapper; factory can use `ComparisonShelfPage` directly |
| snacks | `SnacksComparisonPage` | Same |

Avoid N duplicate wrappers if factory + registry suffice; wrappers only when stable export name needed for tests/QA.

---

## 6. Per-category registration checklist

### maadanim (existing)

- [x] `maadanimCategoryDefinition`
- [ ] Deduplicate metadata: route vs `maadanimComparisonMetadata` (drift risk)

### bread (planned)

- [ ] `bread_frontend_v2.json`
- [ ] `getBreadPageData()`, `getBreadCorpusPayload()`
- [ ] `breadCategoryDefinition` with `routePath: "/hashvaot/bread"`
- [ ] Register in `comparisonCategoryRegistry`

### snacks (planned)

- [ ] `snacks_frontend_v2.json` (replace hardcoded `snack-page-data.ts` fixtures)
- [ ] `getSnacksPageData()`, `getSnacksCorpusPayload()`
- [ ] `snacksCategoryDefinition` with `routePath: "/hashvaot/snacks"`
- [ ] Register in registry
- [ ] Retire `SnackComparisonEngine` from production path

---

## 7. Dev and QA integration

### 7.1 Generalize dev API

**Current:** `GET /api/dev/maadanim`  
**Target:** `GET /api/dev/comparison/[categoryId]` validating `categoryId` against registry.

Keep `/api/dev/maadanim` as permanent redirect or alias during transition.

### 7.2 Preview page

**Current:** `/dev/preview` — maadanim-only fetch.  
**Target:** Query param `?category=maadanim|bread|snacks` or category picker; render `ComparisonShelfPage` with registry payload.

### 7.3 QA scripts

Parameterize `scripts/qa-maadanim-production.mjs` → `qa-comparison-production.mjs --category=maadanim`.

---

## 8. Migration risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Registering bread/snacks before v2 corpora exist | Runtime empty or adapter hacks | Gate registry entries on validation CI |
| `ComparisonCategoryId` drift vs route folders | 404 or wrong category loaded | Single source: registry `routePath` + codegen check |
| Duplicate metadata (route + registry) | SEO drift | Export metadata only from `*-page-data.ts`; route re-exports |
| Legacy types imported into registry | Architecture drift | Lint rule: registry categories may not import `bread-types` / `snack-types` |
| Dynamic route premature | Unlaunched categories exposed | Stay with explicit routes until rollout complete |
| Filter type erasure (`string`) | Wrong filter id at runtime | Category shelf modules export const option tuples; validation in dev |

---

## 9. Implementation order (registry only)

1. Extend `ComparisonCategoryId` union + document slug table.
2. Add `bread` and `snacks` definition files **stubbed** (`status: planned`) behind feature flag — **or** wait until corpora validate (preferred: no stub in production registry).
3. Add `listComparisonCategories()` for index page.
4. Generalize dev API.
5. Register `bread` when `bread_migration_plan_v1` Phase 2 complete.
6. Register `snacks` when snack corpus + filters ready.

**Rule:** A category appears in `comparisonCategoryRegistry` only when its canonical route is ready for QA or production.

---

## 10. Non-goals

- Migrating milk into this registry (separate editorial architecture).
- Implementing `BariCategoryPageVM` end-to-end in UI.
- Auto-discovery of categories from filesystem without explicit registration.
