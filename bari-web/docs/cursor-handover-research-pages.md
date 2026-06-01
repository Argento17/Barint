# Cursor Handover — Bread & Milk Research Pages

This document tells you where to find all data, images, editorial content, and components for the two research/comparison experiences on the site.

---

## 1. Milk Comparison — `/hashvaot/milk-comparison`

### Route & entry component
```
src/app/hashvaot/milk-comparison/page.tsx   ← Next.js route (thin wrapper)
src/components/comparisons/milk-comparison-page.tsx   ← full page component
```

### Data file
```
src/data/milk-comparison.json
```
- **18 products** (real Israeli market products)
- Product key fields: `barcode`, `name_he`, `brand`, `productType`, `score`, `grade`, `image_url`, `nutrition`, `bariInterpretation[]`, `consumerExplanation`
- Product types: `dairy` | `soy` | `oat` | `almond` | `rice` | `coconut` | `protein_drink` | `other_plant`

### Images — all 18 have real photos
Every milk product has a live `image_url` pointing to the Yochananof product CDN:
```
https://api.yochananof.co.il/media/catalog/product/cache/.../{barcode}_s1_...jpg
```
The `<ProductThumbnail>` component handles loading + fallback:
```
src/components/comparisons/product-thumbnail.tsx
```
- Renders `<Image src={product.image_url} ... />` when available
- Falls back to a styled placeholder (gradient accent strip + brand text) if the URL errors or image_url is null
- Fallback accent color is keyed by `productType` — e.g. `dairy` → dark graphite, `oat` → amber, `soy` → emerald

**To show a milk product image anywhere, use `<ProductThumbnail product={p} size="md" />`.**

### TypeScript types & data accessors
```
src/lib/comparisons/milk-types.ts           ← MilkComparisonProduct, ComparisonFilterId, etc.
src/lib/comparisons/milk-page-data.ts       ← milkProducts[], GRADE_COLORS, comparisonFilters, filterBreadProducts(), sortBreadProducts()
src/lib/comparisons/milk-editorial-content.ts  ← structured editorial copy (sections, findings, etc.)
src/lib/comparisons/milk-product-insights.ts   ← per-product insight strings
```

### Blog post — `/blog/milk-analysis`
```
src/app/blog/milk-analysis/page.tsx         ← route
src/lib/blog/milk-analysis-content.ts       ← all article copy (hero, lead, editorialInsights, scatter metadata)
src/lib/blog/milk-analysis-chart-data.ts    ← scatter chart data + SCATTER_EDITORIAL_NOTES[]
```
The article embeds a scatter plot (`milk-analysis-scatter.tsx`) with axes:
- X: processing intensity (0 = minimal / 100 = heavily formulated)
- Y: protein level (0 = low / 100 = high)

### Milk editorial sub-components (inside `src/components/comparisons/milk-editorial/`)
| File | What it renders |
|------|----------------|
| `milk-cinematic-hero.tsx` | Dark hero section with score ring |
| `milk-editorial-intro.tsx` | Opening editorial paragraphs |
| `milk-dimension-story.tsx` | Dimension-by-dimension story |
| `milk-ingredient-structure.tsx` | Ingredient breakdown visual |
| `milk-processing-timeline.tsx` | Processing level timeline |
| `milk-matrix-integrity-visual.tsx` | Data confidence visual |
| `milk-comparison-bridge.tsx` | Transition block to the interactive comparison |
| `milk-product-strip.tsx` | Horizontal scrollable product strip |
| `animated-score-ring.tsx` | Animated SVG ring for score display |

---

## 2. Bread Comparison — `/hashvaot/bread-comparison`

### Route & entry component
```
src/app/hashvaot/bread-comparison/page.tsx   ← Next.js route (thin wrapper)
src/components/comparisons/bread-comparison-page.tsx   ← full page component (~900 lines)
```

### Data file
```
src/data/bread-comparison.json
```
- **20 representative products** (synthetic barcodes `9990001000001`–`9990001000032`, based on real BSIP2 analysis)
- Product key fields: `id`, `name_he`, `brand`, `category`, `archetype`, `score`, `grade`, `delta`, `gss`, `ferm_q`, `fiber_q`, `nutrition`, `ingredients_display`, `insight`, `finding`
- **`image_url` is `null` for all 20 products** — no real product photos available

### Images — no real photos, uses `BreadProductMark` instead
Because the bread corpus uses synthetic IDs, there are no CDN product images. The component renders a styled placeholder called `BreadProductMark` (defined inline in `bread-comparison-page.tsx`):
- A small card with a **colored top stripe** keyed by archetype
- Brand name + category label in text
- Archetype accent color from `ARCHETYPE_META` in `bread-page-data.ts`

**If you want to add real product images later:** add `image_url` strings to `bread-comparison.json` and update the product card rendering in `bread-comparison-page.tsx` to use `<Image>` when `image_url` is non-null (same pattern as `ProductThumbnail` for milk).

### Archetype system & colors
```
src/lib/comparisons/bread-page-data.ts
```
8 archetypes, each with a Tailwind class set:
| Archetype | Label | Color |
|-----------|-------|-------|
| `sourdough_traditional` | מחמצת מסורתית | amber (#92400E) |
| `nordic_whole_grain` | קריספ נורדי / דגן שלם | emerald (#1F8F6A) |
| `seeds_multigrain` | גרעינים ורב-דגן | yellow (#854D0E) |
| `sourdough_theater` | מחמצת כטעם | orange (#9A3412) |
| `fiber_inflation` | ניפוח סיבים | rose (#9F1239) |
| `engineered_functional` | הנדסה פונקציונלית | indigo (#3730A3) |
| `simple_white` | בסיס לבן / תעשייתי | slate (#374151) |
| `treat_salty` | פינוק / מלוח | stone (#6B3B2E) |

Access via:
```ts
import { ARCHETYPE_META } from "@/lib/comparisons/bread-page-data";
const { bgClass, textClass, borderClass, label } = ARCHETYPE_META["sourdough_traditional"];
```

### TypeScript types
```
src/lib/comparisons/bread-types.ts
```
Key types: `BreadProduct`, `BreadArchetype`, `BreadGrade`, `BreadFilterId`, `FermentationQuality`, `FiberSourceQuality`

### Data accessors
```
src/lib/comparisons/bread-page-data.ts
```
- `breadProducts: BreadProduct[]` — all 20 products
- `BREAD_GRADE_COLORS` — grade → `{ bg, text, border }` hex values
- `filterBreadProducts(products, filterId)` — filter by archetype / grade / fermentation / fiber type
- `sortBreadProducts(products, "score" | "fiber" | "protein" | "delta")` — sort helper

### Editorial content
```
src/lib/comparisons/bread-editorial-content.ts
```
All editorial copy in one `breadEditorial` export:
- `hero` — eyebrow, title, subtitle, KPIs (32 products / 6 patterns / 5 dimensions)
- `lead[]` — 4 opening paragraphs
- `dimensions[]` — 5 analytical dimensions (grain structure, processing, fiber source, sweeteners, balance)
- `archetypes[]` — 6 archetype cards (label, description, signals, tradeoff, examples)
- `lookalikes[]` — 4 look-alike pairs (products that look similar but score very differently)
- `fermentationZones[]` — 4 fermentation zones (traditional → none)
- `findings[]` — 3 surprising findings
- `grainStory` — closing editorial text on grain structure
- `conclusion` — CTA / closing block

---

## 3. Index page — `/hashvaot`

```
src/app/hashvaot/page.tsx
```
- Featured milk card → links to `/hashvaot/milk-comparison`
- Bread card → links to `/hashvaot/bread-comparison`
- Two "coming soon" cards (yogurts, energy bars)

The milk featured card uses `<FeaturedMilkIntelligenceCard>`:
```
src/components/hashvaot/featured-milk-intelligence-card.tsx
```

---

## 4. Shared design tokens (for both pages)

| Token | Value | Usage |
|-------|-------|-------|
| Page background | `#F7F7F2` | cream |
| Card background | `#FFFFFF` | white |
| Primary text | `#111318` | near-black |
| Secondary text | `#4E5663` | muted |
| Very muted text | `#7A817C` | labels |
| Accent green | `#1F8F6A` | Bari brand green |
| Grade A | `#2E7D32` | dark green |
| Grade B | `#558B2F` | olive green |
| Grade C | `#F9A825` | amber |
| Grade D | `#EF6C00` | orange |
| Grade E | `#C62828` | red |

Both pages are RTL (`dir="rtl"` is set on the root `<html>` in the layout). All Hebrew text flows right-to-left by default.

---

## 5. Quick reference — which file for what

| Need | Go here |
|------|---------|
| Milk product list + nutrition data | `src/data/milk-comparison.json` |
| Bread product list + scores | `src/data/bread-comparison.json` |
| Milk product images | `product.image_url` in the JSON (all present) |
| Bread product images | Not available — use `BreadProductMark` in `bread-comparison-page.tsx` |
| Render a milk product photo | `<ProductThumbnail product={p} />` from `src/components/comparisons/product-thumbnail.tsx` |
| Milk editorial copy | `src/lib/comparisons/milk-editorial-content.ts` |
| Bread editorial copy | `src/lib/comparisons/bread-editorial-content.ts` |
| Milk article copy + scatter | `src/lib/blog/milk-analysis-content.ts` + `milk-analysis-chart-data.ts` |
| Archetype color/label for bread | `ARCHETYPE_META` in `src/lib/comparisons/bread-page-data.ts` |
| Grade colors | `GRADE_COLORS` (milk) / `BREAD_GRADE_COLORS` (bread) in respective `*-page-data.ts` |
| TypeScript types — milk | `src/lib/comparisons/milk-types.ts` |
| TypeScript types — bread | `src/lib/comparisons/bread-types.ts` |
| Full milk page component | `src/components/comparisons/milk-comparison-page.tsx` |
| Full bread page component | `src/components/comparisons/bread-comparison-page.tsx` |
