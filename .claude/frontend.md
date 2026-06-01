# Bari Frontend â€” Architecture Reference

**Frontend repo:** `C:\bari-web`  
**Framework:** Next.js (App Router)  
**Language:** TypeScript  
**Styling:** Tailwind CSS  
**Last verified:** 2026-05-30

---

## Bari Repository Map â€” TWO SEPARATE LOCATIONS

This file describes the **website repo**: `C:\bari-web`. All implementation in this document happens there.

| Repo | Path | Use for |
|------|------|---------|
| **Website repo** | `C:\bari-web` | Next.js app, React components, Tailwind, routes, `src/`, `package.json`, frontend JSON, `npm run lint`, `npm run build` |
| **Product / data workspace** | `C:\Bari` | BSIP assets, scoring research, CE reports, nutrition docs, category rollout, Python pipelines |

- All frontend work (routes, components, UI, build, lint) â†’ **`C:\bari-web`**.
- **Never assume `C:\Bari` is the website repo** â€” no Next.js source lives there.
- **Never modify website source files under `C:\Bari`.** The frontend JSON the site renders lives in `C:\bari-web\src\data\comparisons\` (generated from BSIP2 outputs in `C:\Bari`, then copied over).
- Before implementing, **confirm the working directory is `C:\bari-web`**.

---

## Two Component Generations

| Generation | Status | Files |
|---|---|---|
| Gen 0 (deprecated) | Legacy â€” quarantined, do not modify | `src/components/comparisons/milk-comparison-page.tsx`, `bread-comparison-dashboard.tsx`, `src/components/snack/` |
| Gen 1 (canonical) | Active â€” all new builds use these | `src/components/shared/` |

**Do not cross the tree boundary.** Canonical components never import from legacy files.

---

## Route Structure

All category comparison pages live under `/hashvaot/`:

| Route | Component | Data source |
|-------|-----------|-------------|
| `/hashvaot/maadanim` | `maadanim-comparison-page.tsx` | `maadanim_frontend_v2.json` |
| `/hashvaot/bread` | bread comparison page | `bread_frontend_v2.json` |
| `/hashvaot/snack-bars` | snacks comparison page | `snacks_frontend_v2.json` |
| `/hashvaot/yogurts` | yogurts comparison page | `yogurts_frontend_v1.json` |
| `/hashvaot/milk-comparison` | `milk-comparison-page.tsx` (legacy) | `milk-comparison.json` |

Category pages are registered in `src/lib/comparisons/registry/index.ts` via `ComparisonCategoryDefinition`.

---

## Canonical Component Tree (`src/components/shared/`)

Build order is enforced. Each component depends on the one above it being visually approved before proceeding.

| # | Component | File | Depends on |
|---|---|---|---|
| 1 | ScoreChip | `score-chip.tsx` | nothing |
| 2 | ProductRow | `product-row.tsx` | ScoreChip |
| 3 | ExpansionSection | `expansion-section.tsx` | ProductRow |
| 4 | ProductTable | `product-table.tsx` | ProductRow, ExpansionSection |
| 5 | CategoryHero | `category-hero.tsx` | ScoreChip |
| 6 | CategoryPrologue | `category-prologue.tsx` | nothing |
| 7 | MethodologyFooter | `methodology-footer.tsx` | nothing |
| 8 | StickyFilterButton | (sticky-filter-button.tsx, planned) | nothing |
| 9 | ComparisonPage | `comparisons/[category]-comparison-page.tsx` | all above |

---

## View Model Contract

**Source:** `src/lib/view-models/index.ts`

The View Model is the **only** interface between backend outputs and the UI. The UI never imports from `lib/comparisons/`, never reads BSIP fields directly, and never contains scoring logic.

```typescript
BariCategoryPageVM
  â”œâ”€â”€ hero: BariHeroVM         // tagline, productCount, scoredCount, topProduct
  â”œâ”€â”€ prologue: BariPrologueVM // sentences: string[] (2â€“3 pre-authored)
  â”œâ”€â”€ products: BariProductVM[]
  â”‚     â”œâ”€â”€ id, name, imageUrl
  â”‚     â”œâ”€â”€ score: number | null
  â”‚     â”œâ”€â”€ grade: "A"|"B"|"C"|"D"|"E" | null
  â”‚     â”œâ”€â”€ insightLine: string  // "" = no slot rendered
  â”‚     â”œâ”€â”€ confidence: "verified"|"partial"|"insufficient"
  â”‚     â””â”€â”€ expansion: BariExpansionVM
  â”‚           â”œâ”€â”€ nutrition: BariNutritionVM | null
  â”‚           â”œâ”€â”€ ingredients: string | null
  â”‚           â”œâ”€â”€ confidenceLabel: string  // pre-rendered Hebrew
  â”‚           â”œâ”€â”€ servingNote: string      // "×œ-100 ×’×¨×"
  â”‚           â”œâ”€â”€ positiveSignals?: string[]   // optional v2 field
  â”‚           â”œâ”€â”€ limitingFactors?: string[]   // optional v2 field
  â”‚           â”œâ”€â”€ bottomLine?: string          // optional v2 field
  â”‚           â””â”€â”€ comparisonContext?: string   // optional v2 field
  â”œâ”€â”€ filters: BariFilterVM[]  // first entry is always "all"
  â””â”€â”€ methodology: BariMethodologyVM
```

**Transformation layer** (`src/lib/comparisons/`) maps BSIP JSON â†’ BariProductVM. This is the only place where BSIP field names appear.

---

## Category Registry Pattern

Each category has a definition file:

```
src/lib/comparisons/registry/
  index.ts                  getComparisonCategory(), listComparisonCategoryIds()
  types.ts                  ComparisonCategoryDefinition, ComparisonCategoryId
  categories/
    maadanim.ts
    bread.ts
    snacks.ts
    yogurts.ts
```

`ComparisonCategoryDefinition` provides:
- `id: ComparisonCategoryId`
- `routePath: /hashvaot/â€¦`
- `metadata: Metadata` (Next.js page metadata)
- `getPageData()` â†’ full page payload
- `getCorpusPayload()` â†’ raw products + meta

Adding a new category requires a new file in `registry/categories/` and a registration entry in `registry/index.ts`.

---

## Page Structure (Gen 1 Frozen)

Exactly 4 sections, in this order. No additions.

```
[1] CategoryHero      â€” compact, single sentence, max 280px mobile
[2] CategoryPrologue  â€” 2â€“3 prose sentences
[3] ProductTable      â€” sorted by score descending
[4] MethodologyFooter â€” 2â€“4 sentences, 12px/#AAAAAA, no card container
```

---

## Design Tokens

**File:** `src/lib/design/bari-comparison-tokens.ts`

Active tokens:

| Key path | Value | Purpose |
|---|---|---|
| `rows.oddBg` | `#FFFFFF` | Odd-row background |
| `rows.evenBg` | `#F9F9F9` | Even-row background |
| `rows.zebraRowClass` | Tailwind class string | Applied per row |
| `rows.zebraContainerClass` | Tailwind class string | Applied to table container |
| `score.rowChip.*` | bg `#F7F7F2`, border `rgba(17,19,24,0.10)` | Score chip (neutral, grade-agnostic) |
| `layout.*` | `rowHeightMobile: 72px`, `imageSize: 56px`, `scoreChipSize: 28px`, `heroMaxHeight: 280px` | (must be added if missing) |
| `insightLine.*` | `fontSize: 13px`, `color: #444444` | (must be added if missing) |
| `methodology.*` | `fontSize: 12px`, `color: #AAAAAA` | (must be added if missing) |

**Deprecated tokens** (legacy use only, never import in canonical components):
- `gradePalette` â€” grade-to-color mapping (forbidden in Gen 1)
- `score.comparisonChip` â€” color-coded chip
- `score.hero.labelSize`, `score.hero.labelClass` â€” grade label text

---

## RTL Rules

- All content is Hebrew, `dir="rtl"`.
- Product names: right-aligned.
- Insight lines: right-aligned.
- Score chip: positioned top-right of row.
- Nutrition grid labels and values: right-aligned.
- "×”×¦×’ ×”×›×œ" link: right-aligned.
- Sticky filter button: fixed **bottom-right** (not bottom-left).
- Ingredient list: right-aligned, RTL.

---

## Mobile / Desktop Behavior

Mobile is the **primary design target**. Desktop adapts from mobile.

| Element | Mobile | Desktop |
|---|---|---|
| Collapsed row height | 72px (max 80px) | Same |
| Product image | 48px (mobile) / 56px | 56px |
| Hero max height | 280px | â€” |
| Pre-table max height | 480px | â€” |
| Filter default | Collapsed, sticky FAB after 300px scroll | Same |
| Filter panel | Full-screen modal | Same or sidebar |
| Expansion | Inline below row, no overlay | Inline |
| Table layout | Single-column full-width | Two-column (desktop layout via `BariComparisonDesktopPage`) |

**Desktop split:** `maadanim-comparison-page.tsx` renders `ComparisonShelfPage` on mobile (`max-lg:block`) and `BariComparisonDesktopPage` on desktop (`hidden lg:block`).

---

## Legacy Components (Quarantined)

Do not import these into canonical components. Do not modify them during a canonical build.

| File | Route | Gen 0 violations present |
|---|---|---|
| `milk-comparison-page.tsx` | `/hashvaot/milk-comparison` | Dimension bars, score attribution, matrix integrity badge |
| `bread-comparison-dashboard.tsx` | `/hashvaot/bread-comparison` | Full-viewport hero, collapsible methodology card, 3 comparison pairs |
| `src/components/snack/` | `/hashvaot/snack-bars` | Sheet expansion, NOVA label, card grid layout |
| `bari-grade-badge.tsx` | Used by milk + snack | Grade-to-color mapping |
| `dimension-bars.tsx` | Used by milk | Dimension breakdown (framework exposure) |
| `bari-interpretation-panel.tsx` | Used by milk | Score attribution |
| `matrix-integrity-badge.tsx` | Used by milk | Framework vocabulary in UI |

---

## Forbidden Patterns in Any UI Component

- Framework vocabulary in rendered text: NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, dimension
- Score chip background/border that varies by grade value
- Grade letter accompanied by label text ("D Â· × ×ž×•×š", "B Â· ×’×‘×•×”")
- Expansion that opens as sheet, modal, or overlay
- "×ž×” ×ž×¢×œ×”/×ž×•×¨×™×“ ××ª ×”×¦×™×•×Ÿ" pattern (score attribution)
- Heading tags inside expansion section
- Methodology wrapped in a card, border, or `<details>`
- Filter visible at 0px scroll
- More than 3 filter dimensions
- More than 1 highlighted comparison pair per page

---

## Sources

- `C:\bari-web\src\lib\view-models\index.ts`
- `C:\bari-web\src\lib\comparisons\registry\`
- `C:\bari-web\src\components\comparisons\maadanim-comparison-page.tsx`
- `C:\Bari\01_framework\frontend\component_build_sequence_v1.md`
- `C:\Bari\01_framework\frontend\cursor_handoff_protocol_v1.md`
- `C:\Bari\01_framework\frontend\comparison_view_model_v1.md`
- `C:\Bari\01_framework\frontend\design_token_governance_v1.md`
- `C:\Bari\01_framework\frontend\legacy_isolation_policy_v1.md`
- `C:\Bari\01_framework\frontend\architecture_generations_registry_v1.md`
