# Bari Comparison Template Standard v1

**Type:** Design standard — frozen approved state  
**Status:** **Single authoritative comparison template.** Supersedes and absorbs `comparison_template_v1.md` (consolidated 2026-06-03, owner-approved).  
**Authority:** Design Director  
**Source of truth:** Live component source in `C:\bari\bari-web\src\components\shared\` and `bari-comparison-tokens.ts`  
**Canonical reference implementation:** `maadanim-comparison-page.tsx`  
**Last verified against live source:** 2026-05-30  

This document records the current approved visual and structural state of Bari comparison pages, and the editorial/UX principles that govern them. It is the reference for future category rollouts. Sections 1–19 are the live design standard (verified against component source). Sections 20–26 are the conceptual layer (Core Principle, public-language and copy rules, leakage/drift checklists, the rollout workflow, and the governing UX principles) folded in from the former `comparison_template_v1.md` so nothing useful was lost in the consolidation.

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
| Score chip colour rule | Color-coded by grade via `gradePalette` (owner directive 2026-06-03): one distinct hue family per grade A→E (green → olive → gold → orange → red). Tinted background + accent left-border + accent number/letter only — never a fully saturated fill. Each grade's accent ≥3:1 and label ≥4.5:1 on its own bg. Same chip geometry for all grades. |
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
| Fully saturated / solid-fill score chips | Reads as a warning badge. Grade color is allowed (owner directive 2026-06-03) but only as a tinted bg + accent border/number — never a saturated block fill. |
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

---

## 20. Core Principle

The user should feel:  
**"Someone carefully investigated this supermarket shelf for me."**

Not:  
"I am using food analytics software."

Every rule in this document — geometry, typography, copy, leakage prevention — serves that distinction. When a design choice is ambiguous, resolve it toward "investigated shelf," away from "analytics dashboard."

The product table is the main experience. Hero, prologue, and methodology are support. No maps, dashboards, cluster visualizations, insight systems, decomposition panels, or glossary sections.

---

## 21. Section Copy Rules

The geometry of each section is specified in Sections 10 (Hero), the Prologue typography in Section 4, and Section 9 (Methodology Footer). This section governs the *copy* that goes inside them.

### Hero copy

- One sentence. Maximum 12 words in Hebrew.
- Names a real product and a real observation. It does not explain anything.
- Not a thesis, summary of findings, invitation to a journey, or a hook. A moment of orientation: "you are about to see products from this shelf."
- Example: `ב-95 מוצרים ממדף המעדנים של שופרסל, הגביע הכי מוכר מקבל את הציון הכי נמוך.`

### Prologue copy

- 3–5 sentences. Hard limit. Calm declarative tone. Continuous prose, no bullets/subheadings.
- Every sentence is a shelf observation verifiable from the data. No nutrition lecture, no framework language, no "here is how we score."
- Does not repeat the hero sentence. Does not preview the findings — it names what is on the shelf, not what to think about it.
- Example: `מדף המעדנים של שופרסל כולל מוצרי חלב קלאסיים, אלטרנטיבות חלבון, ומוצרים שמציגים תוויות 'דיאט' ו'ללא סוכר'. בדקנו 95 מוצרים. לא כל מוצר שמרגיש בריא יותר מקבל ציון גבוה יותר.`

### Methodology copy

- 2–4 sentences. What to include: products reviewed from Israeli retail shelves; that ingredients, nutrition, and processing context were considered (not only calories/macros); that scores are relative to the category; one linked line to full methodology.
- What not to include: score mechanics, NOVA explanation, cap/floor logic, dimension names or weights, framework architecture, confidence computation.
- Example: `בדקנו 95 מוצרים ממדף המעדנים בשופרסל. הציון מבוסס על רכיבים, ערכי תזונה ורמת עיבוד — לא רק על קלוריות. הציונים יחסיים לקטגוריה. [המתודולוגיה המלאה →]`

### Highlighted pair driver line (optional)

- If a clearly strongest pair exists: one driver line, ≤15 Hebrew words, observational, no framework language. It is a table annotation, not a story beat — no side-by-side layout, no separate narrative scene.
- Maximum one highlighted pair per page. If no pair is clearly strongest, omit it. Absence is better than a forced comparison.

---

## 22. Public Language Rules

Apply to all public-facing text: hero, prologue, row insights, methodology, filter labels, any UI microcopy.

### Approved terms

| Concept | Public language |
|---|---|
| Score | ציון (number + grade letter; tier word permitted only in the chip tier slot) |
| High processing | "רמת עיבוד גבוהה" / "מוצר מעובד" |
| Additives | "תוספים" / "תוספים מזוניים" |
| Short ingredient list | "רשימת רכיבים קצרה" |
| Protein | "חלבון" (g amount, not a quality classification) |
| Sugar | "סוכר" (g amount from label) |
| Confidence | "נתונים מלאים" / "נתונים חלקיים" |

### Forbidden terms (never appear publicly)

BSIP / BSIP0 / BSIP1 / BSIP2 · NOVA (name or number) · cap / binding cap / floor · routing / category routing · dimension (processing_quality, glycemic_quality, etc.) · structural class · anchor / hard anchor · confidence band or numeric confidence score · framework / pipeline / ontology · any explanation of how scores are computed.

### Score display rules (reconciled with Gen 1.1, owner directive 2026-06-03)

- Chip format: `72 · B · טוב` — numeric + grade letter + tier word. Grade is conveyed by **both** the letter and the color (per `gradePalette`, see Section 5).
- The chip tier slot (`טוב` / `בינוני` / etc.) is the **only** place a grade adjective may appear. Do **not** write free-floating verbal verdicts elsewhere ("ציון גבוה" / "ציון בינוני" / "ציון נמוך" in prose) — the chip carries the interpretation.
- Grade color stays within the approved A–E ramp as a subtle tint + accent border/number — never a saturated fill, never a second per-product color axis.

> Note: the former v1 constraint "no color, no grade adjectives" is **superseded**. The chip is color-coded by grade and the tier word is permitted in the tier slot. Section 5 is the operative chip spec.

### Insight line rules

The insight line is an observation, not a verdict. (Full grammar in `insight_line_spec_v1.md`; interpretive verdict-row model in `row_description_standard_v1.md`.)

- Approved: `רשימת רכיבים קצרה מ-5 מרכיבים` · `10 גרם חלבון ל-100 גרם` · `מוצר הדיאט עם יותר תוספים מהגרסה הרגילה` · `המוצר הנמכר ביותר בקטגוריה`
- Forbidden: `מוצר לא בריא` · `כדאי להימנע` · `עדיף על` · `הציון נמוך כי...` · any causal explanation of the score.

---

## 23. Ontology Leakage Prevention

A leakage event occurs when the internal framework becomes visible through any surface: a filter label, tooltip, row annotation, or data note.

**Detection checklist — run before every category launch:**

- [ ] Does any filter label contain a framework term?
- [ ] Does any row insight explain the score mechanism?
- [ ] Does the methodology section name any framework dimension?
- [ ] Does the hero or prologue contain NOVA, cap, or routing language?
- [ ] Does the expanded row show anything other than interpretive content, nutrition, ingredients, data note, confidence?
- [ ] Does the highlighted-pair driver line reference framework logic?

If any checkbox is YES: fix before launch.

---

## 24. Dashboard Drift Prevention

A drift event occurs when the page starts to feel like analytics software rather than shelf exploration.

**Drift warning signs:**

- A chart or visualization appears above the first product row.
- The user must make a choice (filter, select, configure) before seeing any product.
- A summary statistic ("67% of products are NOVA4") appears before product rows.
- An aggregate view (brand ranking, category average) is surfaced as primary content.
- Multiple filter dimensions are visible and open by default.
- Comparison moments multiply beyond one.
- A score appears with a free-floating verbal interpretation beside it (outside the chip tier slot).
- A heading appears inside the expansion section.

Note: per Gen 1.1, grade-based color on the score chip is **not** drift — it is the approved chip treatment (Section 5). Drift is a saturated red/green warning-badge fill, or a *second* color axis beyond the A–E ramp.

**Response to drift pressure:** Do not add the element. If a stakeholder requests one of the above, the answer is the methodology page or framework documentation — not the product table.

---

## 25. Category Rollout Workflow

For each new category, in order:

1. **Data prerequisites** — BSIP2 run complete; batch summary reviewed; editorial scope filtered (false positives removed); minimum 30 scored products.
2. **Hero identification** — from scored data, find the single most surprising product (known brand with unexpected low score, OR "healthy"-positioned product below category average). Write one Hebrew sentence naming product + observation.
3. **Prologue writing** — answer in 3–5 sentences total: what products are on this shelf; what we looked at; what is not obvious from the front of the package. One sentence each, max.
4. **Highlighted pair (optional)** — identify the single clearest score gap between two comparable products. Write one driver line (≤15 Hebrew words, observational). If no pair is clearly strongest, omit.
5. **Row insight writing** — one insight line per in-scope product (≤12 Hebrew words). Sources: ingredient count, dominant ingredient, notable claim vs. score, protein amount, additive presence. The insight must be independently observable without knowing the score.
6. **Filter configuration** — name the 1–3 filter dimensions; write Hebrew consumer labels for each value; confirm no label exposes a framework term.
7. **Methodology line** — 2–4 sentences using the methodology copy rules (Section 21). Confirm no framework terms.
8. **Leakage + drift checklist** — run both (Sections 23 and 24). Fix any failure before launch. Then proceed through the Build Gate Sequence (Section 18).

---

## 26. Governing UX Principles

Every design decision is evaluated against these, in order.

1. **Products first.** The user's first visual interaction is with a product, not a system. No filter wall, chart, or summary box before the first product row.
2. **Calm by default.** Nothing pulses or competes for attention. Interactions are quiet: expand/collapse, filter toggle. No hover state changes layout.
3. **One discovery at a time.** The table is sorted by score. Contradictions emerge through scrolling, not annotation.
4. **Invisible scaffolding.** The system that produced the scores does not appear. The user sees products, scores, and observations — not the pipeline.
5. **Mobile is not a reduction.** The mobile experience is complete. Collapsed rows hold everything a browsing user needs; expanded rows hold everything an investigating user needs.
6. **Restraint is the feature.** When in doubt, remove. Fewer elements at higher quality beats more elements at lower quality. The absence of a comparison moment is a decision to let the table speak.

---

*End of Comparison Template Standard v1.*
