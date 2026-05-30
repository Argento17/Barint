# Comparison UI Reference v1

**Frozen reference:** מעדנים production comparison (Codex audit corpus v2).  
**Status:** Documentation only — do not treat this file as a change request.  
**Date frozen:** 2026-05-29

Use this document when rolling out additional category comparison pages. Match structure and behavior; swap category-specific data and copy only.

---

## Route

| Purpose | Path |
|--------|------|
| **Production (reference)** | `/hashvaot/maadanim` |
| Dev smoke / API check | `/dev/preview` (client fetch via `/api/dev/maadanim`) |

Production route is a static server page: corpus is imported at build time, not fetched in the browser.

**Files**

- `src/app/hashvaot/maadanim/page.tsx` — route shell + metadata
- `src/components/comparisons/maadanim-comparison-page.tsx` — shelf UI composition

---

## Data source

| Item | Location |
|------|----------|
| Canonical corpus | `src/data/comparisons/maadanim_frontend_v2.json` |
| Loader / copy constants | `src/lib/comparisons/maadanim-page-data.ts` |
| Dev API (optional) | `src/app/api/dev/maadanim/route.ts` → `getMaadanimCorpusPayload()` |

**Rules**

- No runtime dependency on external paths (e.g. `C:\Bari\...`).
- `_calibration` and other internal fields are stripped in the loader before UI.
- UI consumes `BariProductVM[]` only (`src/lib/view-models/index.ts`).
- UI never imports BSIP, scoring engines, or raw audit traces.

**Corpus metadata** (`_meta`): `product_count`, `generated`, `version` (`v2-production`). Metadata line is derived from count + `generated` (Hebrew month/year).

---

## Component structure

Top-to-bottom inside the phone frame (single column, RTL):

```
MaadanimComparisonPage
├── CategoryHero          (eyebrow, title, metadata line)
├── CategoryPrologue      (2–3 sentences)
├── CategoryShelfLenses   (filter chips; lensOptions from category module)
├── ProductTable
│   └── ProductRow[]      (image, name, insightLine, chevron + ScoreChip)
│       └── ExpansionSection (when expanded)
└── MethodologyFooter     (methodology lines)
```

**Shared primitives** (reused across categories — change only with explicit design approval):

- `src/components/shared/category-hero.tsx`
- `src/components/shared/category-prologue.tsx`
- `src/components/shared/category-shelf-lenses.tsx`
- `src/components/shared/product-table.tsx`
- `src/components/shared/product-row.tsx`
- `src/components/shared/expansion-section.tsx`
- `src/components/shared/methodology-footer.tsx`
- `src/components/shared/score-chip.tsx`

**Category-specific wiring** lives in `maadanim-comparison-page.tsx` + `maadanim-page-data.ts` + `maadanim-shelf-filters.ts`, not inside shared row/table components.

---

## Product order ownership

**Order is owned by the JSON corpus**, not the client.

- Products appear in `maadanim_frontend_v2.json` in final shelf order (score-desc, insufficient last — pre-computed in corpus build).
- `ProductTable` maps `products` in array order **without re-sorting**.
- Filters subset the list but **preserve relative order** among visible rows.

Do not add client-side score sorting, grade sorting, or name sorting in `ProductTable` for reference-category pages.

---

## Expansion fields (interpretive v2)

Rendered by `ExpansionSection` from `BariExpansionVM`. Pre-authored Hebrew only; render verbatim.

| JSON field | UI section label | When shown |
|------------|------------------|------------|
| `positiveSignals[]` | מה עובד לטובת המוצר? | Non-empty array |
| `limitingFactors[]` | מה מגביל את הציון? | Non-empty array |
| `bottomLine` | בשורה התחתונה | Non-empty string |
| `comparisonContext` | **הקשר במדף** | Non-empty string |

**Section order (fixed):** positive → limiting → bottom line → shelf context → hairline → technical block.

**Technical block (secondary, below divider):**

- `expansion.nutrition` — per 100g/ml grid; hide null cells
- `expansion.ingredients` — clamped list + “הצג הכל”
- Confidence footer from `product.confidence` + `expansion.confidenceLabel`

**Must not appear in UI copy:** BSIP, NOVA, caps, dimensions, routing labels, score mechanics, internal audit terminology.

**Row header (collapsed):** `name`, `insightLine` (hidden slot if empty), `score`/`grade` chip, subtle chevron grouped with chip.

---

## Filter isolation

Filters are **not** yet driven by `BariCategoryPageVM.filters`.

| Concern | File |
|---------|------|
| Chip definitions + labels | `src/lib/comparisons/maadanim-shelf-filters.ts` (`MAADANIM_SHELF_LENS_OPTIONS`) |
| Match logic | `filterMaadanimProducts()` in same file |
| UI chips | `CategoryShelfLenses` with `lensOptions={MAADANIM_SHELF_LENS_OPTIONS}` |

**מעדנים lenses (v1):**

- `less-sweet` — סוכרים ≤ 10g per 100g
- `relatively-high-protein` — חלבון ≥ 8g
- `short-ingredient-list` — ≤ 6 comma-separated ingredients

Filters are **AND**-combined. Active state is client-only; corpus order unchanged.

Future: move definitions + counts into `BariCategoryPageVM.filters`; keep visual chip styling in `CategoryShelfLenses`.

---

## Mobile / desktop behavior

**Outer shell**

- Background: `#EFEFEB`, full viewport, centered.
- **Mobile:** `w-full`, no outer vertical padding on frame.
- **Desktop (`sm+`):** `max-w-[375px]`, `rounded-[2rem]`, `shadow-2xl`, `py-10` on outer wrapper.

**Phone frame:** 375px max width — editorial shelf prototype, not full-bleed desktop table.

**Row interaction**

- Tap row toggles expand/collapse.
- Chevron + score chip on the left (RTL); name + insight on the right.
- Expanded row scrolls into view (`scrollIntoView`, respects `prefers-reduced-motion`).
- First visible product opens expanded on load (`initialExpandedProductId` = first in filtered list).

**Images:** Next.js `Image` in `ProductRow`; lazy load except first two rows (`imagePriority`).

**Site chrome:** Production route renders inside root layout (`SiteHeader`). Shelf frame is unchanged; allow for global header when testing scroll/click at top of viewport.

---

## What must not change in future category rollouts

Unless there is an explicit new design pass, **preserve**:

1. **Information architecture** — Hero → Prologue → Lenses → Zebra product list → Methodology. No new sections above the shelf.
2. **Expansion section order and labels** — Especially **הקשר במדף** (not “בהשוואה לגרסה אחרת”).
3. **ProductRow / ProductTable layout** — Chevron beside score chip; no floating product orbit, no accordion chrome redesign.
4. **Client-side product reordering** — Order from corpus/VM only.
5. **Interpretive vs technical hierarchy** — Reasoning blocks first; nutrition/ingredients muted below hairline.
6. **No algorithm exposure** — No BSIP/NOVA/caps/dimension language in user-facing strings.
7. **Calm editorial tokens** — Off-white/graphite/emerald palette per Bari comparison rules; no neon/cyber/wellness-blog tone.
8. **Pre-authored strings** — UI displays VM fields verbatim; no LLM/runtime copy generation in components.
9. **Filter chip visual pattern** — Rounded pills, same active/inactive styling via `CategoryShelfLenses`.
10. **375px phone frame on desktop** — Do not expand shelf to full desktop grid without a new reference version.

**Safe to vary per category**

- JSON corpus path and loader module
- Hero/prologue/methodology Hebrew copy
- Shelf lens ids, labels, and match rules (isolated module)
- Product count and corpus `generated` date
- Route path under `/hashvaot/{category}`

---

## Reference checklist for new categories

- [ ] Corpus JSON under `src/data/comparisons/{category}_frontend_v2.json`
- [ ] Loader: strip internal fields → `BariProductVM[]`
- [ ] Page route: `src/app/hashvaot/{category}/page.tsx`
- [ ] Comparison page component mirroring `MaadanimComparisonPage`
- [ ] Shelf filters in dedicated `{category}-shelf-filters.ts` (not hard-coded in shared components)
- [ ] `ProductTable` receives pre-ordered products; no sort
- [ ] Expansion fields populated in corpus; UI unchanged
- [ ] `npm run lint` + `npm run build`

---

## Related QA assets

Screenshots and scripts (non-production): `public/qa/maadanim-v2/`, `scripts/qa-maadanim-production.mjs`.
