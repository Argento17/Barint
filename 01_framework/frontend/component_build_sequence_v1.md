# Bari Comparison Component Build Sequence — v1

**Status:** Frozen  
**Date:** 2026-05-28  
**Applies to:** All Bari category comparison pages

---

## Canonical Build Order

| # | Component | File | Depends on |
|---|---|---|---|
| 1 | ScoreChip | `src/components/shared/score-chip.tsx` | nothing |
| 2 | ProductRow | `src/components/shared/product-row.tsx` | ScoreChip |
| 3 | ExpansionSection | `src/components/shared/expansion-section.tsx` | ProductRow |
| 4 | ProductTable | `src/components/shared/product-table.tsx` | ProductRow, ExpansionSection |
| 5 | CategoryHero | `src/components/shared/category-hero.tsx` | ScoreChip |
| 6 | CategoryPrologue | `src/components/shared/category-prologue.tsx` | nothing |
| 7 | MethodologyFooter | `src/components/shared/methodology-footer.tsx` | nothing |
| 8 | StickyFilterButton | `src/components/shared/sticky-filter-button.tsx` | nothing |
| 9 | ComparisonPage | `src/components/comparisons/[category]-comparison-page.tsx` | all of the above |

---

## Hard Gate

**No ComparisonPage assembly (step 9) before steps 1–3 are finalized and visually approved.**

Steps 4–8 may be built in parallel once steps 1–3 are approved. Step 9 requires all 8.

---

## Per-Component Completion Criteria

A component is **finalized** when:

1. It renders correctly with Hebrew content in `dir="rtl"` context
2. It passes its Section 3 audit table from `frontend_integration_checklist_v1.md`
3. It has been visually inspected at 375px viewport width
4. No forbidden patterns are present (see below)

A component is **visually approved** when it has been reviewed in browser at 375×812px emulation and explicitly confirmed.

---

## Forbidden Patterns — Enforced at Component Level

These conditions cause automatic rejection of any component, regardless of build stage:

| Component | Forbidden |
|---|---|
| ScoreChip | A hue outside the approved A–E `gradePalette` ramp, a fully saturated / solid-fill grade color, or a second per-product color axis (grade-coded tint via `gradePalette` is required, not forbidden — Gen 1.1) |
| ScoreChip | Chip geometry that varies by grade (geometry must be identical across grades — only the grade colors vary) |
| ScoreChip | A free-text interpretive label beside the grade beyond the approved tier word ("נמוך", "גבוה", "בינוני", "חזק") |
| ProductRow | Any `border` between rows (border on the row element itself) |
| ProductRow | Height > 80px collapsed |
| ProductRow | No insight line slot |
| ExpansionSection | Any heading tag (`h2`, `h3`, `h4`) inside expansion |
| ExpansionSection | Any reference to framework terms: NOVA, BSIP, cap, structural_class, matrix_integrity, pillar, dimension |
| ExpansionSection | "מה מעלה/מוריד את הציון" pattern — score attribution is not permitted |
| ExpansionSection | Modal, sheet, or overlay — must expand inline only |
| CategoryHero | Total height > 280px on 375px viewport |
| CategoryHero | More than one sentence in hero text |
| MethodologyFooter | Any `<h2>`, `<h3>`, or bold heading above text |
| MethodologyFooter | Any border, background, or card container |
| MethodologyFooter | Font larger than 12px or color darker than #AAAAAA |
| StickyFilterButton | Visible on initial page load (0px scroll) |
| StickyFilterButton | Any badge or count indicator |
| ComparisonPage | Any of the above present in assembled page |
| ComparisonPage | More than 1 comparison pair |
| ComparisonPage | Any section heading between prologue and first product row |

---

## Token Requirements Per Component

Each component must consume the following tokens from `src/lib/design/bari-comparison-tokens.ts`. If a token is missing from the file at build time, add it before building the component — do not hardcode values inline.

| Component | Required tokens |
|---|---|
| ScoreChip | `score.rowChip` (chip geometry/structure) + `gradePalette[grade]` for the grade-coded tint, accent border, and number/letter color (Gen 1.1) |
| ProductRow | `rows.oddBg`, `rows.evenBg`, `rows.zebraRowClass`, `rows.zebraContainerClass` |
| ProductRow | `typography.insightLine` (to be added: `font-size: 13px`, `color: #444444`) |
| ProductRow | `layout.rowHeight` (to be added: `72px`), `layout.imageSize` (to be added: `56px`) |
| CategoryHero | `score.hero` (hero score display; grade color via `gradePalette[grade]` consistent with the chip, Gen 1.1) |
| MethodologyFooter | `typography.methodology` (to be added: `font-size: 12px`, `color: #AAAAAA`) |

---

## Rationale

This sequence exists because:

- ScoreChip is the most constrained component (grade color must stay inside the approved A–E `gradePalette` ramp, tinted not saturated, no free-text interpretive label) and must be finalized before ProductRow consumes it
- ProductRow defines the visual rhythm of the entire page — its height, spacing, and insight line slot cannot be adjusted after ProductTable is built around it
- ExpansionSection inline behavior must be confirmed before page assembly, since a modal fallback is an auto-fail condition
- Steps 5–8 are independent of each other and can be built in parallel, but none of them can ship to the page until the row trio is approved

---

*This sequence governs all future Bari category builds, not only מעדנים. The file paths and component names are canonical.*

---

## Step 10 — Hashvaot Index Card + Background Photo

**Every new live category requires a featured card on `/hashvaot`.** This is the entry point users see first — skipping it means the category is invisible from the comparisons index.

### 10a. Source the background photo

- Search Pexels (pexels.com) for a free-license image that clearly depicts the category food.
- Use **firecrawl image search** with `site:pexels.com` to find candidates quickly.
- Pick an image with visual weight in the **bottom-left third** (the card mask bleeds from that corner).
- Download at 1200px width via Pexels' CDN parameter:
  ```
  https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1200
  ```
- Save to: `public/hashvaot/themes/<category-slug>.jpg`
- Target file size: 100–300 KB. If >500 KB, append `&q=80`.

### 10b. Create the featured card component

- File: `src/components/hashvaot/featured-<category-slug>-intelligence-card.tsx`
- Pattern: copy the closest existing card (e.g. `featured-butter-intelligence-card.tsx`), replace all content.
- Required props: `href: string`, `description: string`
- The `theme` object **must** include both `accent` and `photo`:
  ```ts
  theme={{
    accent: "<hex>",
    // photo: Pexels #<ID> — "<exact image title from the Pexels page>"
    // Free license: https://www.pexels.com/photo/<title-slug>-<ID>/
    // Downloaded <YYYY-MM-DD> via firecrawl image search → public/hashvaot/themes/
    photo: "/hashvaot/themes/<category-slug>.jpg",
  }}
  ```
- `INSIGHT_LINES`: 3–4 findings grounded in the **actual corpus** — not generic statements.
- `stats`: exactly 3 entries — products analyzed, a score/range, one category-specific metric.

### 10c. Wire into the `/hashvaot` index page (`src/app/hashvaot/page.tsx`)

1. Import the card component.
2. Import corpus meta + products from `<category>-page-data`.
3. Add `const <CATEGORY>_COMPARISON_HREF = "/hashvaot/<slug>"`.
4. Derive a `<category>Description` from the first prologue sentence + product count.
5. Render the card inside the **"ניתוח עדכני"** `<div>` — newest categories at the top of that section.

### 10d. Completion gate (do not mark Step 10 done until all pass)

- [ ] Photo file exists in `public/hashvaot/themes/` and is visible in browser
- [ ] Source comment in the card's `theme` block names the Pexels ID, full title, URL, and download date
- [ ] `photo` key is **not commented out** — image renders in the card
- [ ] Card appears in the correct position in the "ניתוח עדכני" section
- [ ] `tsc --noEmit` passes with 0 errors after adding the card
- [ ] Do NOT use bare `focus-visible:outline` — use `focus-visible:outline-2` instead (bare `outline` conflicts with `outline-2` in Tailwind v4; CSS conflict warning)
