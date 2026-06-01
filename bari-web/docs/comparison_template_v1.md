# Comparison Template v1

**Status:** Approved MVP framework (2026-05-30)  
**Reference routes:** `/hashvaot/milk-comparison`, `/hashvaot/snacks`, `/hashvaot/bread`, `/hashvaot/yogurts`

Four-category MVP rollout uses one shared comparison experience. Milk retains a custom data schema but matches the same desktop visual pattern.

---

## Reusable (shared framework)

### Layout & responsive split

| Viewport | Component | Behavior |
|---|---|---|
| `< lg` (mobile) | `ComparisonShelfPage` | 375px phone-frame shelf; filters, hero, zebra rows, expansion |
| `lg+` (desktop) | `BariComparisonDesktopPage` | `HomeContainer` / `max-w-7xl`; intelligence hero; lens filters; zebra rows |

Category pages wrap both in a split container:

```tsx
<div className="max-lg:block lg:hidden"><ComparisonShelfPage … /></div>
<div className="hidden lg:block"><BariComparisonDesktopPage … /></div>
```

### Core components

| File | Role |
|---|---|
| `src/components/comparisons/bari-comparison-desktop-page.tsx` | Desktop orchestrator: hero, prologue, filters, ranked list, methodology |
| `src/components/comparisons/comparison-shelf-page.tsx` | Mobile shelf orchestrator |
| `src/components/comparisons/bari-product-shelf-row.tsx` | Zebra row: rank, thumbnail, name, score/grade, `בקצרה`, expansion panel |
| `src/components/comparisons/bari-product-thumbnail.tsx` | Product image (null-safe) |
| `src/components/comparisons/comparison-intelligence-hero.tsx` | Hero card: badge, tags, title, insight rotation, stats, updated line |
| `src/components/comparisons/comparison-intelligence-backdrop.tsx` | Grid/wave backdrop |

### Styling & rhythm

- Tokens: `src/lib/design/bari-comparison-tokens.ts` (`BARI_COMPARISON_TOKENS`)
- Zebra row alternation on desktop and mobile
- Expansion: nutrition tiles, positive signals, limiting factors, bottom line, comparison context
- Methodology block at page foot (desktop and mobile)

### Data loading pattern

1. JSON corpus in `src/data/comparisons/*_frontend_v*.json` with `_meta` + `products[]`
2. Page-data module loads via `loadComparisonCorpus`, strips internal fields (`_cluster`, `_website_cluster`, etc.)
3. Shelf filters module: lens options + `filterProducts(products, activeFilters)`
4. Route `page.tsx` passes props to category `*ComparisonPage` client component

### Registry (optional, for programmatic access)

`src/lib/comparisons/registry/` — `ComparisonCategoryId`, `getComparisonCategoryPageData(id)`

---

## Category-specific (per comparison)

Each category supplies only:

| Concern | Location pattern |
|---|---|
| Corpus JSON | `src/data/comparisons/{category}_frontend_v*.json` |
| Page data | `src/lib/comparisons/{category}-comparison-page-data.ts` |
| Filters / lenses | `src/lib/comparisons/{category}-shelf-filters.ts` |
| Page component | `src/components/comparisons/{category}-comparison-page.tsx` |
| Route | `src/app/hashvaot/{category}/page.tsx` |
| Index card | `src/components/hashvaot/featured-{category}-intelligence-card*.tsx` |

### Category matrix (MVP)

| Category | Route | Corpus | Filters | Notes |
|---|---|---|---|---|
| Milk | `/hashvaot/milk-comparison` | `milk-comparison.json` | Custom in page | Custom schema; same desktop hero/row visual |
| Snacks | `/hashvaot/snacks` | `snacks_frontend_v2.json` | `_internal_cluster` map | 18 products; Yochananof |
| Bread | `/hashvaot/bread` | `bread_frontend_v2.json` | `bread-retail-curated.json` clusters | 24 products; Shufersal |
| Yogurts | `/hashvaot/yogurts` | `yogurts_frontend_v1.json` | `_cluster` on products | 14 products; manual MVP corpus |

### Editorial content (per category)

- `hero.eyebrow`, `hero.title`
- `prologueSentences[]` (2–3 sentences)
- `methodologyLines[]` (disclosure)
- `metadataLine` (product count, scope, sort order)
- Desktop hero stats (scraped / scored / displayed counts where applicable)
- Optional `blogLink` on desktop

### Internal JSON fields (stripped before render)

- Snacks: `_internal_cluster`
- Bread: `_website_cluster` (filter uses separate curated map)
- Yogurts: `_cluster`

---

## Milk exception

Milk uses `MilkComparisonProduct` and `ProductShelfRow` in `milk-comparison-page.tsx` — not `BariProductVM` / `BariProductShelfRow`. Desktop layout, hero, zebra rhythm, and expansion structure match the approved template. Do not migrate milk data schema without explicit approval.

---

## Deprecated

- `ComparisonShelfPage` with `layout="web"` (4-column table) — retired
- Per-category `*-comparison-desktop-page.tsx` — merged into `BariComparisonDesktopPage`

See also: `docs/comparison_web_template_v1.md` (historical note).
