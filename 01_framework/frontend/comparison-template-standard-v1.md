# Bari Comparison Template Standard v1

**Type:** Design standard — frozen approved state  
**Authority:** Design Director  
**Source of truth:** Live component source in `C:\bari-web\src\components\shared\` and `bari-comparison-tokens.ts`  
**Canonical reference implementation:** `maadanim-comparison-page.tsx`  
**Last verified against live source:** 2026-05-30  

This document records the current approved visual and structural state of Bari comparison pages. It is a reference for future category rollouts. It does not propose changes.

---

## 1. Required Page Sections

Every comparison page contains exactly four sections, in this order. No additions are permitted without explicit re-approval.

| Order | Section | Component file |
|---|---|---|
| 1 | Category Hero | `src/components/shared/category-hero.tsx` |
| 2 | Category Prologue | `src/components/shared/category-prologue.tsx` |
| 3 | Product Table | `src/components/shared/product-table.tsx` |
| 4 | Methodology Footer | `src/components/shared/methodology-footer.tsx` |

The filter control (`CategoryShelfLenses`) is positioned between Section 2 and Section 3. It is not counted as a standalone section — it is part of the table display system.

---

## 2. Section Order

```
┌─────────────────────────────────┐
│  [1] Category Hero              │  px-4 pt-4 pb-2
│      eyebrow / title / metadata │
├─────────────────────────────────┤
│  [2] Category Prologue          │  px-4
│      3–5 declarative sentences  │
├─────────────────────────────────┤
│  [FILTER] Shelf Lenses          │  px-4
│      filter pill group          │
├─────────────────────────────────┤
│  [3] Product Table              │  no additional padding
│      table header (desktop)     │
│      product rows               │
├─────────────────────────────────┤
│  [4] Methodology Footer         │  px-4 pt-4 pb-6
│      2–4 plain-text sentences   │
└─────────────────────────────────┘
```

On desktop (`lg+`), the shell gains horizontal inset padding: `lg:px-8 xl:px-10 2xl:px-12`. The four sections and the filter group all share this inset class. The product rows use the same inset so columns align with section headers.

---

## 3. Visual Hierarchy

### Surface colours

| Surface | Colour | Notes |
|---|---|---|
| Page background (mobile) | `#EFEFEB` | Warm grey canvas |
| Page background (desktop) | `#F7F7F2` | Slightly lighter warm off-white |
| Content card (mobile) | `#FFFFFF` | White, max-width 375px, `rounded-[2rem]` on sm+ |
| Desktop shell surface | `#FFFFFF` | `lg:rounded-none lg:border-0 lg:shadow-none` |
| Product row — odd rank | `#FFFFFF` | Rank 1, 3, 5 … |
| Product row — even rank | `#F9F9F9` | Rank 2, 4, 6 … |
| Table header (desktop) | `#FAFAF8` | Header row only |
| Image frame | `#F8F7F3` | Fallback and frame background |
| Image frame (missing) | `#F3F3EE` | Darker fallback when no image |

### Stripe logic

Stripe is determined by rank, not by DOM position. Rank 1 = white, rank 2 = grey, rank 3 = white. The table header on desktop is not counted as a rank; it does not disrupt the odd/even sequence.

Container class: `bari-zebra-rows overflow-hidden`  
Row utility: `comparisonRowStripeClass(rank)` → returns `bg-[#FFFFFF]` or `bg-[#F9F9F9]`

### Elevation and borders

No box shadows on product rows. No borders on individual rows. Separation between rows is achieved entirely through alternating surface colour.

The only visible divider is the desktop table header bottom border: `lg:border-b lg:border-[rgba(17,19,24,0.06)]`.

The expansion panel technical details section has a top border: `border-t border-[rgba(17,19,24,0.06)]`.

On desktop, the expansion panel top has: `border-t border-[rgba(17,19,24,0.06)]`.

---

## 4. Typography Hierarchy

All text is Hebrew (RTL). The root layout container carries `dir="rtl"`.

### Section-level typography (Category Hero)

| Element | Specification |
|---|---|
| Eyebrow | `font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80` |
| H1 title (mobile) | `mt-1 text-[1.35rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318]` |
| H1 title (desktop) | `lg:text-[1.75rem]` — scale only, all other properties same |
| Metadata line | `mt-1 text-[12px] leading-snug text-[#6A716E]` |
| Metadata line (desktop) | `lg:text-[13px]` — scale only |

### Row-level typography (Product Row)

| Element | Mobile | Desktop |
|---|---|---|
| Product name | `font-semibold text-[15px] line-clamp-1 leading-snug tracking-[-0.012em] text-[#111318]` | `text-[16px] leading-snug` (same weight, tracking, colour) |
| Insight line | `text-[13px] leading-[1.5] text-[#353D39] line-clamp-2` | `text-[14px] leading-[1.55] line-clamp-3` |
| Rank number (desktop only) | — | `text-[12px] font-semibold tabular-nums text-[#9A9FA6]` |

The insight line reserves a fixed minimum height of `2.9375rem` on mobile even when the string is empty (an NBSP is rendered to hold the space). This prevents layout shift between products.

### Expansion panel typography

| Element | Specification |
|---|---|
| Section label | `text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]` |
| Positive signal line | `text-[12px] leading-relaxed text-[#4E5663]` |
| Limiting factor line | `text-[12px] leading-relaxed text-[#6E756F]` |
| Bottom line | `text-[13px] leading-[1.55] text-[#2F3531]` |
| Comparison context | `text-[12px] leading-relaxed text-[#7A817C]` |
| Nutrition label | `text-[10px] font-medium leading-none text-[#9A9FA6]` |
| Nutrition value | `text-[12px] font-semibold tabular-nums leading-none text-[#6E756F]` |
| Nutrition unit | `text-[9px] font-medium text-[#9A9FA6]` |
| Serving note | `text-[10px] font-medium leading-none text-[#AAAAAA]` |
| Ingredients text | `text-[11px] leading-relaxed text-[#7A817C]` |
| "הצג הכל" button | `text-[11px] font-semibold text-[#1F8F6A]` |
| Confidence label | `text-[10px] text-[#AAAAAA]` |
| Close button ("סגור") | `text-[11px] text-[#AAAAAA]` |

### Prologue typography

`text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]`  
Items are `space-y-2`. No bullet points.

### Methodology footer typography

`text-[11px] leading-relaxed text-[#8A908B]`  
Items are `space-y-1.5`. Note: the design token file specifies `12px` for methodology but the component renders `text-[11px]`. The component is the source of truth.

### Filter pill typography

| State | Specification |
|---|---|
| Inactive | `text-[12px] font-medium color: #4E5663; bg: #FAFAF7; border: #D9DDD7` |
| Active | `text-[12px] font-medium color: #295C49; bg: #EEF5F1; border: #C9D8CF` |

Both states: `rounded-full border px-3 py-1.5 transition-colors duration-150`

---

## 5. Score Chip Standard

The ScoreChip (`score-chip.tsx`) is the only element that communicates a product score and grade together. Its visual treatment is fully standardised.

### Chip anatomy

```
┌──────────────┐
│  left border │
│     72       │  ← score, 22px, font-extrabold, tabular-nums
│      B       │  ← grade, 10px, font-bold
│              │
└──────────────┘
```

- Container: `inline-flex shrink-0 flex-col items-center justify-center rounded-lg text-center`
- Size: `minWidth: 2.75rem`, `padding: 5px 8px`
- Left border: `4px solid {accentColor}` — grade-specific
- Right/top/bottom border: `1px solid rgba(17,19,24,0.10)`
- Score font size: `22px` (from token `layout.scoreChipSize`)
- Grade font size: `10px`

### Grade-specific colours

Every grade produces a distinct but very subtle tint. Saturation is intentionally low.

| Grade | Background tint | Accent colour (left border + text) |
|---|---|---|
| A | `#F3F7F5` | `#3E6B57` |
| B | `#F1F7F6` | `#2F6E69` |
| C | `#F8F4EB` | `#9A6D25` |
| D | `#F8F1EA` | `#9A5A24` |
| E | `#F7EFED` | `#8A4338` |

**Critical rule:** The chip is never saturated. Grade A does not render a vivid green; Grade E does not render a vivid red. The tint backgrounds are barely visible; the accent lives only on the left border and on the two text elements.

### Null / no-score state

When `score` or `grade` is `null`:
- Background: `#EEEEEA`
- Border: `1px solid rgba(17,19,24,0.07)`, left border `3px solid #9A9FA6`
- Content: `—` at `text-[11px] font-semibold text-[#9A9FA6]`
- ARIA label: `ללא ציון`

### Chevron

A `ChevronDown` icon (`size-3.5`) sits to the right of the chip (RTL: left side of the row, visually). Colour `#B5BBB6` at rest, rotates 180° when expanded, colour shifts to `#9A9FA6`. Transition: `duration-200 ease-[cubic-bezier(0.22,1,0.36,1)]`.

---

## 6. Product Row Standard

### Collapsed row

| Property | Value |
|---|---|
| Minimum height (mobile) | `72px` |
| Horizontal padding | `px-4` |
| Image size (mobile) | `56px` (rendered at `66px` after ×1.18 scale factor) |
| Image size (desktop) | `64px` (rendered at `75px`) |
| Image container | `rounded-md`, `bg: #F8F7F3`, inner shadow `inset 0 0 0 1px rgba(17,19,24,0.04)` |
| Gap between elements | `gap-2.5` |
| Row class | `bari-shelf-row` + `bari-shelf-row--idle` when closed |

The entire row is a tap/click target (`role="button"`, `tabIndex={0}`, `aria-expanded`). Keyboard: Enter and Space activate toggle.

Scroll behaviour on expand: `scrollIntoView({ block: "nearest" })` with `scrollMarginBlock: 8px`. Respects `prefers-reduced-motion`.

### Expanded row — panel content order

1. **Interpretive content** (conditional — omitted when absent)
   - "מה עובד לטובת המוצר?" — positive signal bullet list
   - "מה מגביל את הציון?" — limiting factor bullet list
   - "בשורה התחתונה" — bottom line prose
   - "הקשר במדף" — shelf context prose
2. **Technical details** (conditional — omitted when absent)
   - Separator: `border-t border-[rgba(17,19,24,0.06)]`
   - Nutrition grid (per-100g)
   - Ingredient list (clipped at 4 lines)
3. **Footer row** (always present)
   - Confidence label (left)
   - "סגור" close button (right)

On `confidence === "insufficient"`: only the brief message "אין מספיק נתונים לאריזה זו כדי להציג פירוט." plus the footer row. No interpretive or technical content.

### Expansion animation

CSS grid-template-rows collapse: `gridTemplateRows: "0fr"` → `"1fr"`. Transition: `duration-200 ease-[cubic-bezier(0.22,1,0.36,1)]`. Motion reduction respected via `motion-reduce:transition-none`.

Only one row is expanded at a time. ProductTable manages the single-expanded-ID state.

### Desktop layout (lg+)

The row switches to a four-column CSS grid:

```
Columns:  [2.25rem]  [4.5rem]  [minmax(0,1fr)]  [5.25rem]
           rank       image     product+insight    score
Gap:       lg:gap-x-5
```

Expansion panel spans `lg:col-start-3 lg:col-end-4` (product column only). Rank and image columns do not expand.

Desktop inset matches section inset: `lg:px-8 xl:px-10 2xl:px-12`.

---

## 7. Nutrition Grid Standard

Located inside the expansion panel, separated from interpretive content by a border.

- Per-100g basis only. Label: `ל-100 גרם` (from `servingNote` field).
- Five fields in fixed order: `קק"ל`, `חלבון ג'`, `סוכרים ג'`, `שומן ג'`, `נתרן מ"ג`
- `null` field: cell is hidden entirely
- `0` value: displayed as `0` — zero is a valid and meaningful value
- Grid: `grid grid-cols-1 gap-y-1` — single column on all viewports in the expansion panel

### Desktop (wide mode) nutrition

On desktop, if both positive signals and limiting factors exist, the signal lists display in a two-column grid: `lg:grid-cols-2 lg:gap-x-12`. The nutrition grid remains single-column.

---

## 8. Table Desktop Header Standard

Visible only at `lg+` (`hidden lg:grid`).

- Grid matches product row column definition exactly
- Background: `lg:bg-[#FAFAF8]`
- Bottom border: `lg:border-b lg:border-[rgba(17,19,24,0.06)]`
- Padding: `lg:py-2.5`
- Column eyebrow text: `text-[10px] font-bold tracking-[0.06em] text-[#9A9FA6]`
- Inset matches product rows: `lg:px-8 xl:px-10 2xl:px-12`

The table header does not count as a ranked product row; it does not disturb the rank-based stripe sequence.

---

## 9. Methodology Footer Standard

- Container: `<footer>`, not a card, no border, no background colour
- Padding: `px-4 pt-4 pb-6` / `lg:pb-8 lg:pt-3` (wide)
- Text: `text-[11px] leading-relaxed text-[#8A908B]`
- Item spacing: `space-y-1.5`
- Length: 2–4 sentences maximum
- Required content: product count, data source, statement that scores are relative to category
- Forbidden content: scoring mechanics, NOVA, dimension names, cap or floor logic, any framework term

The methodology footer is plain prose rendered as `<p>` tags. No heading tags, no links, no icons.

---

## 10. Category Hero Standard

Container: `<header>`, padding `px-4 pt-4 pb-2`.

Three elements in fixed vertical order:

1. **Eyebrow** — `<p>` — monospace, 0.62rem, bold, uppercase, teal (`#1F8F6A` at 80% opacity)
2. **Title** — `<h1>` — the only `<h1>` on the page
3. **Metadata line** — `<p>` — product count and scan date

The hero contains no images, no charts, no animated elements. The eyebrow is the category label. The title is a shelf observation. Neither element explains the scoring system.

---

## 11. Filter Control Standard

Positioned between Section 2 and the table header. Renders as a horizontal scrollable row of pill buttons.

| Property | Value |
|---|---|
| Container padding | `px-4` |
| Pill shape | `rounded-full border` |
| Pill padding | `px-3 py-1.5` |
| Font | `text-[12px] font-medium` |
| Transition | `transition-colors duration-150` |
| Inactive bg | `#FAFAF7` |
| Inactive border | `#D9DDD7` |
| Inactive text | `#4E5663` |
| Active bg | `#EEF5F1` |
| Active border | `#C9D8CF` |
| Active text | `#295C49` |

Filter pills are single-select (radio semantics). The first option is always "הכל". Grade filter values are B / C / D / E only — no numeric ranges, no verbal descriptors.

The filter reduces visible rows without a page reload. Filtered-out rows are not shown; no animation on hide.

Maximum 2–3 filter dimensions per category. Labels are consumer-facing Hebrew, not internal cluster names.

---

## 12. Mobile Layout Behaviour

**Viewport reference:** 375px width.

| Behaviour | Specification |
|---|---|
| Base background | `#EFEFEB` warm grey |
| Content card | `w-full bg-white overflow-hidden` |
| Content card (sm+) | `sm:max-w-[375px] sm:rounded-[2rem] sm:shadow-2xl` |
| Min-height | `min-h-screen` |
| Centring (sm+) | `flex justify-center sm:py-10` |
| Scroll | Natural document scroll; no custom scroll container |

At 375px, 3 or more product rows must be fully visible without scrolling. The hero, prologue, and filter group appear above the first product row.

Expansion opens inline below the tapped row. The page scrolls to bring the expanded row into view (`scrollIntoView: nearest`).

No fixed or sticky elements at 375px except the optional `StickyFilterButton` which appears only after 300px scroll.

No horizontal overflow at any width from 375px upward.

---

## 13. Desktop Shell Layout

Reference breakpoint: `lg` (1024px+).

| Property | Value |
|---|---|
| Shell max width | `1600px` |
| Shell alignment | `mx-auto` within viewport |
| Canvas background | `#F7F7F2` |
| Shell surface | `bg-white`, no border, no shadow, no rounding |
| Section horizontal inset (sm/md) | `px-4` |
| Section horizontal inset (lg) | `lg:px-8` |
| Section horizontal inset (xl) | `xl:px-10` |
| Section horizontal inset (2xl) | `2xl:px-12` |

The mobile shelf layout and the desktop layout are rendered in the same React tree. The mobile version (`max-lg`) and desktop version (`lg+`) both read from `ComparisonLayoutProvider`. Context value is `"shelf"` (mobile) or `"web"` (desktop).

---

## 14. Elements That Must Remain Consistent

These are non-negotiable across all categories. Any deviation requires explicit re-approval.

| Element | Rule |
|---|---|
| Section count | Always exactly 4. No additions. |
| Section order | Hero → Prologue → Table → Footer. Fixed. |
| Score chip colour rule | Tint background only. Left border accent. Never saturated by grade. |
| Score chip null state | `—` on `#EEEEEA`, grey border, no score text. |
| Row height minimum | 72px collapsed. |
| Row image size | 56px mobile / 64px desktop (token-defined). |
| Stripe logic | Rank-based. Rank 1 = white. No exceptions. |
| Expansion type | Inline only. No sheet, modal, overlay, or portal. |
| Single-expand | One row at a time. Expanding a second row collapses the first. |
| Close button label | "סגור" — no alternatives. |
| Nutrition basis | Per 100g only. |
| Nutrition zero display | `0` displayed, not hidden. |
| Nutrition null display | Cell hidden entirely. |
| Desktop column grid | `[2.25rem_4.5rem_minmax(0,1fr)_5.25rem]` with `gap-x-5`. Fixed. |
| `dir` attribute | `dir="rtl"` on root container. |
| Ingredient clip | 4 lines, "הצג הכל" to expand. |
| Methodology container | `<footer>`, plain text, no card. |
| H1 usage | One per page, in CategoryHero only. |
| Token import | All visual values from `bari-comparison-tokens.ts`. No hardcoded duplicates. |
| View model boundary | Components receive `BariProductVM` only. No raw BSIP fields reach the UI. |
| Forbidden rendered terms | NOVA, BSIP, BSIP2, cap, floor, structural_class, matrix_integrity, pillar, dimension — never in rendered strings. |

---

## 15. Elements Allowed to Vary by Category

These may differ across categories without re-approval.

| Element | What varies |
|---|---|
| Eyebrow text | Category name in Hebrew |
| H1 title | Shelf observation specific to the category |
| Metadata line | Product count, scan count, data source, update date |
| Prologue sentences | 3–5 sentences — unique per category |
| Methodology lines | 2–4 sentences — unique per category |
| Filter dimensions | 1–3 filters; labels are category-specific |
| Filter values | Options within each filter dimension |
| Product count | No minimum beyond 3 visible at 0px scroll on mobile |
| Product JSON source | `src/data/comparisons/{category}_frontend_vN.json` |
| Highlighted product pair | Optional; one maximum; omit if no clear pair exists |
| Page route | `/hashvaot/{category}` |
| Component file name | `{category}-comparison-page.tsx` |
| Page data module | `{category}-page-data.ts` |
| Shelf filters module | `{category}-shelf-filters.ts` |

---

## 16. Excluded Elements

These were evaluated and excluded from the template. They require explicit re-approval before introduction.

| Element | Why excluded |
|---|---|
| Score distribution chart | Analytics register, no consumer utility |
| Colour-coded score chips (saturated) | Creates good/bad framing, contradicts structural neutrality |
| Dimension bars per product | Exposes internal framework architecture |
| "Understanding the score" modal | Framework exposure risk |
| Radar or spider charts | Exposes dimension architecture |
| Category average benchmark | Requires explanation that pulls from framework |
| Animated score reveal | Disconnected from shelf-native feeling |
| Multiple comparison scenes | Hard to scale; theatrical |
| "Recommended" / "Best" labels | Editorial claim too strong |
| Percentile scoring | Not implemented; cross-category comparison risks |
| Summary statistics above first row | Delays product access; adds framework framing |

---

## 17. Canonical Implementation Reference

The maadanim category is the canonical Gen 1 reference. When building a new category, derive from:

| Artifact | Path |
|---|---|
| Page component | `src/components/comparisons/maadanim-comparison-page.tsx` |
| Page data | `src/lib/comparisons/maadanim-page-data.ts` |
| Shelf filters | `src/lib/comparisons/maadanim-shelf-filters.ts` |
| Registry entry | `src/lib/comparisons/registry/categories/maadanim.ts` |
| Frontend data | `src/data/comparisons/maadanim_frontend_v2.json` |

The milk-comparison page is a legacy implementation. It uses custom components (`BariProductShelfRow`, `BariGradeBadge`, custom layout) that do not reflect the Gen 1 standard. Do not use milk as a template for new categories.

---

## 18. Build Gate Sequence

Five checkpoints must be passed in order before a new category launches. Each is a hard stop.

| Gate | Component | Condition to proceed |
|---|---|---|
| 1 | ScoreChip | Visual approval of chip colour, null state, and grade accent |
| 2 | ProductRow | Visual approval of collapsed row at 375px and 1280px |
| 3 | ExpansionSection | Visual approval of all four interpretive sections and technical details |
| 4 | ProductTable | Visual approval of stripe, header, and single-expand behaviour |
| 5 | Full page | Mobile QA at 375px, leakage sweep, forbidden-term check, no console errors |

---

## 19. Token File as Ground Truth

`src/lib/design/bari-comparison-tokens.ts` is the single source of all visual constants. Any implementation that hardcodes a colour or dimension that exists in the token file is in violation. The file exposes a dev-mode warning via `warnComparisonImplementationDeviation()` — this should never fire in production.

Where the token file and an implemented component appear to differ, the component implementation is the operative value and the token file should be updated to match.

---

*End of Comparison Template Standard v1.*
