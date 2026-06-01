# Bari Platform — CE Direction Document v1.0
> CE = UX/UI Director, Editorial Systems Designer, Interaction Strategist  
> Cursor = Implementation only. No invention beyond what is specified here.  
> Reference aesthetic: `C:\Bari\03_operations\reports\bread_light_consumer_report_v1.html`

---

## Visual System Codification

### Color roles (do not deviate)

| Token | Value | Role |
|---|---|---|
| `bg-cream` | `#F7F7F2` | Page background, inner panels, pill badges |
| `bg-surface` | `#FFFFFF` | Cards, sections on cream |
| `text-primary` | `#111318` | Headlines, bold labels, active states |
| `text-secondary` | `#4E5663` | Body copy, descriptions |
| `text-muted` | `#7A817C` | Captions, metadata, footnotes |
| `accent-emerald` | `#1F8F6A` | CTAs, borders, eyebrow labels, score bars, active indicators |
| `accent-emerald-light` | `#2FAE82` | Trust icons, hover states, secondary accents |

### Three semantic uses of `#1F8F6A`

1. **Editorial signal** — eyebrow labels, section identifiers (`font-bold text-[#1F8F6A]`)  
2. **Data encoding** — score bars, grade indicators, scatter plot active states  
3. **Interactive affordance** — CTA button fill, hover border, active dot stroke

Never use emerald as a decorative fill. Only where it carries editorial or data meaning.

### Typography scale

```
Eyebrow:     text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]
Section H2:  text-3xl md:text-4xl font-extrabold tracking-[-0.045em] text-[#111318]
Article H2:  text-2xl md:text-3xl font-extrabold tracking-[-0.04em] text-[#111318]
Body:        text-base leading-relaxed text-[#4E5663]
Caption:     text-xs text-[#7A817C]
Stat value:  text-2xl font-extrabold tracking-[-0.04em] text-[#111318]
Stat label:  text-xs font-bold text-[#7A817C] uppercase tracking-[0.12em]
```

### Card pattern

```
rounded-[1.2rem] border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7
```

Interior sub-panels use `rounded-[1rem]` with the same border.

### What is forbidden going forward

- Animated radar charts, pulse animations on data points
- Drifting/oscillating benchmark bars
- SVG path networks as background decoration (`home-hero-signal-network`)
- Gradient blur blob divs (`blur-3xl` decorative fills)
- Gradient text effects (`bg-clip-text text-transparent`)
- Orbit/shelf arc decorative visuals (`MilkOrbitVisual`)
- English labels mixed into Hebrew-primary interfaces (`BSIP2 ANALYSIS PARAMETERS`, `CATEGORY-ADJUSTED PARAMETERS`)
- `max-h-[70vh]` constraints that clip editorial heroes

---

## HOME-01 — HomeHero: Remove decorative layer

**File:** `src/components/home/home-hero.tsx`

### Remove (delete entirely)

1. Lines 25–61: the `home-hero-signal-network` div containing the `<svg>` with `signal-network-group-a` and `signal-network-group-b` path/circle groups.

2. Lines 63–69: both gradient blob divs — the `-end-24` green blur and the `-start-16` cream blur.

### Modify

3. **Section height:** Change `min-h-[72vh] items-center md:min-h-[78vh]` to `min-h-[56vh] items-center md:min-h-[62vh]`. Editorial sections do not need massive padding.

4. **Gradient text headline:** Current:
   ```tsx
   className="... bg-gradient-to-l from-[#111318] via-[#111318] to-[#4E5663] bg-clip-text text-transparent ..."
   ```
   Replace with:
   ```tsx
   className="... text-[#111318] ..."
   ```
   Remove `bg-gradient-to-l from-[#111318] via-[#111318] to-[#4E5663] bg-clip-text text-transparent`. Flat `#111318`. The typography is strong enough without it.

5. **Section wrapper:** Add `border-b border-black/[0.06]` to the `<section>` element if not already present, for clear section separation.

### Keep unchanged

- Badge (eyebrow link to `/blog/milk-analysis`)
- `h1` text content
- `p` subtitle text
- Both CTA buttons and their labels
- `heroTrust` item row

### Acceptance criteria

- No animated SVG paths visible in hero area
- No green or cream blur blobs
- Headline renders as flat `#111318`, no gradient
- Hero vertical height reduced, content-proportionate
- All CTAs, badge, trust strip remain functional

---

## HOME-02 — HomeMethodology: Static signal evidence layout

**File:** `src/components/home/home-methodology.tsx`

This is a significant component rewrite. The outer section shell stays. Everything inside the main content card is replaced.

### Remove (delete entirely)

- `SignalRadar` component function (lines 175–353)
- `SignalBenchmarkRow` component function (lines 355–455)
- `SignalBenchmarkBars` component function (lines 458–472)
- `getPoint`, `pointsToString`, `clampPercent` utility functions (lines 156–171)
- `radarSignals` constant (lines 10–59)
- `benchmarkRows` constant (lines 61–86)
- All framer-motion `motion` usage
- `useEffect`, `useState`, `useMemo`, `useRef` imports (section becomes static)
- `useInView` and `usePrefersReducedMotion` hooks

### Keep

- `interpretationCards` constant (lines 88–104) — 3 cards with icons
- `HomeContainer` wrapper
- Section `id="methodology"`, `bg-[#F7F7F2] py-20 md:py-28`
- The thin horizontal rule decoration at top of section (line 501–504): `absolute inset-x-6 top-24 h-px bg-gradient-to-l from-transparent via-[#1F8F6A]/10 to-transparent`

### New section heading block

Replace the current heading (which has English "BSIP2 ANALYSIS PARAMETERS") with:

```tsx
<div className="mx-auto mb-12 max-w-3xl text-center">
  <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
    שיטת הניתוח
  </p>
  <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
    ניתוח רב-ממדי של מספר רב של פרמטרים.
  </h2>
  <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
    Bari מנתחת כל מוצר לפי פרמטרים תזונתיים, רכיביים ועיבודיים — כדי להבין לא רק אם מוצר
    "טוב" או "רע", אלא במה הוא חזק, איפה הוא חלש, ובאיזה הקשר הוא נבחן.
  </p>
</div>
```

### New main content card layout

Replace the current 2-column card with this structure:

```tsx
<div className="rounded-[2rem] border border-black/[0.08] bg-[#FFFFFF]/68 p-4 md:p-6 shadow-[0_36px_120px_-74px_rgba(17,19,24,0.78)]">

  {/* Top: signal grid */}
  <div className="rounded-[1.5rem] border border-black/[0.08] bg-[#FFFFFF]/72 p-5 md:p-7 mb-5">
    <p className="mb-5 text-xs font-bold uppercase tracking-[0.2em] text-[#7A817C]">
      8 אותות ניתוח
    </p>
    <div className="space-y-3">
      {SIGNAL_ROWS.map((signal) => (
        <div key={signal.axis} className="flex items-center gap-4">
          <span className="w-36 shrink-0 text-right text-sm font-bold text-[#111318]">
            {signal.axis}
          </span>
          <div className="relative h-2 flex-1 overflow-hidden rounded-full bg-[#F7F7F2]">
            <div
              className="absolute inset-y-0 right-0 rounded-full bg-[#1F8F6A]/70"
              style={{ width: `${signal.value}%` }}
            />
          </div>
          <span className="w-8 shrink-0 text-left text-xs font-bold text-[#1F8F6A]">
            {signal.value}
          </span>
        </div>
      ))}
    </div>
  </div>

  {/* Bottom: 3 interpretation cards */}
  <div className="grid gap-3 sm:grid-cols-3">
    {interpretationCards.map((card) => {
      const Icon = card.icon;
      return (
        <div
          key={card.title}
          className="rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/52 p-4"
        >
          <Icon className="mb-3 size-5 text-[#1F8F6A]" aria-hidden />
          <h4 className="text-sm font-extrabold text-[#111318]">{card.title}</h4>
          <p className="mt-2 text-xs leading-relaxed text-[#7A817C]">{card.text}</p>
        </div>
      );
    })}
  </div>
</div>
```

### New data constant replacing radarSignals

Add this constant at the top of the file (replaces both `radarSignals` and `benchmarkRows`):

```tsx
const SIGNAL_ROWS = [
  { axis: "איכות רכיבים",     value: 84 },
  { axis: "עומס סוכר ומלח",   value: 38 },
  { axis: "רמת עיבוד",         value: 76 },
  { axis: "ערך תזונתי",        value: 68 },
  { axis: "סיבים וחלבון",     value: 35 },
  { axis: "השוואה לקטגוריה", value: 79 },
  { axis: "אמינות הנתונים",  value: 64 },
  { axis: "פשטות המוצר",      value: 82 },
] as const;
```

### Reduced imports

After the rewrite, imports should be:

```tsx
import { Activity, CheckCircle2, Layers3 } from "lucide-react";
import { HomeContainer } from "./section-frame";
// Remove: motion, useEffect, useMemo, useRef, useState, Sparkles
// Remove: all animation-related code
```

### Acceptance criteria

- No animated radar chart
- No drifting benchmark bars, no Infinity animation loops
- No English labels ("BSIP2", "CATEGORY-ADJUSTED")
- 8 static signal rows visible with proportional bar widths
- 3 interpretation cards visible below
- Component is a server component (no "use client" needed if no state)
- Section still anchors to `#methodology`

---

## HOME-03 — HomeFlagshipAnalysis: Score overlays on product preview

**File:** `src/components/home/home-flagship-analysis.tsx`

### Modify product image grid

Check which score/grade field is available on `MilkComparisonProduct` type. If a `grade` or `score` field exists, add an overlay badge to each product card.

Current image div (lines 49–59):
```tsx
<div key={p.barcode} className="relative h-20 w-12 md:h-24 md:w-14">
  <Image src={p.image_url} alt="" fill ... />
</div>
```

Replace with:
```tsx
<div key={p.barcode} className="relative h-20 w-12 md:h-24 md:w-14">
  <Image src={p.image_url} alt="" fill className="object-contain drop-shadow-md" sizes="56px" />
  {p.grade ? (
    <span className="absolute bottom-0 left-1/2 -translate-x-1/2 rounded-full bg-[#111318] px-1.5 py-0.5 text-[0.55rem] font-extrabold text-[#F7F7F2] leading-none">
      {p.grade}
    </span>
  ) : null}
</div>
```

If `grade` is not on the type, check for `score` and derive grade tier from the score value using the standard Bari grade thresholds (A ≥ 75, B 60–74, C 45–59, D 30–44, E 15–29, F < 15).

### Strengthen the editorial pull quote

Current (line 62–64):
```tsx
<p className="mt-5 border-r-2 border-[#1F8F6A] pr-3 text-sm font-semibold leading-relaxed text-[#111318]">
  מוצרים שנראים דומים על המדף — מתפצלים ברכיבים, בעיבוד ובתזונה.
</p>
```

Replace with:
```tsx
<blockquote className="mt-5 border-r-2 border-[#1F8F6A] pr-4">
  <p className="text-base font-extrabold leading-snug tracking-[-0.02em] text-[#111318]">
    מוצרים שנראים דומים על המדף — מתפצלים ברכיבים, בעיבוד ובתזונה.
  </p>
  <p className="mt-1 text-xs text-[#7A817C]">מסקנה מניתוח 18 מוצרי חלב ושתייה צמחית</p>
</blockquote>
```

### Acceptance criteria

- 4 product images render with grade pill badges overlaid at the bottom
- Pull quote uses `<blockquote>` with caption line below
- No other changes to this component

---

## MILK-01 — MilkAnalysisHero: Replace orbit visual with typographic hero + KPI strip

**File:** `src/components/blog/milk-analysis-hero.tsx`

### Remove

- Import of `MilkOrbitVisual` (line 6)
- Import of `HomeContainer` if it becomes unused
- The `md:grid-cols-2` grid structure
- The right column div (lines 47–53) containing `<MilkOrbitVisual ...>`
- `max-h-[70vh]` constraint from both the `<header>` and the `<HomeContainer>`

### New hero structure

The hero becomes single-column, full-width, typographic. Replace the content div (lines 32–53) with:

```tsx
<div className="flex flex-col justify-center text-right max-w-3xl">
  <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
    {hero.eyebrow}
  </p>
  <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-5xl">
    {hero.title}
  </h1>
  <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
    {hero.subtitle}
  </p>
  <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>

  {/* KPI strip */}
  <div className="mt-6 flex gap-8 border-t border-black/[0.06] pt-5">
    <div>
      <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">18</p>
      <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">מוצרים נותחו</p>
    </div>
    <div>
      <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">5</p>
      <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">סוגי מוצר</p>
    </div>
    <div>
      <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">עשרות</p>
      <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">אותות תזונה</p>
    </div>
  </div>

  <p className="mt-4 max-w-xl text-xs leading-relaxed text-[#7A817C] md:text-sm">
    {disclaimer}
  </p>
</div>
```

### Section sizing

Remove `max-h-[70vh]` from both the `<header>` and `<HomeContainer>`. Section height should be determined by content, not a cap.

Change `HomeContainer` inner div from `flex max-h-[70vh] flex-col pt-3 pb-5 md:pt-4 md:pb-6` to `flex flex-col py-8 md:py-12`.

### Acceptance criteria

- No orbit arc visual, no floating product images
- Typographic-only hero with: eyebrow, H1, subtitle, meta date, KPI strip (3 numbers), disclaimer
- KPI strip: 18 products, 5 product types, "עשרות" signals — separated by top border
- No height cap — hero grows with content
- Back-to-blog link remains

---

## MILK-02 — MilkAnalysisScatter: Rounded container, click-to-pin, improved tooltip

**File:** `src/components/blog/milk-analysis-scatter.tsx`

### Fix 1 — Container rounding

Line 82 — outer div:
```tsx
// Before:
<div className="border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7">
// After:
<div className="rounded-[1.2rem] border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7">
```

### Fix 2 — Click-to-pin state

Add alongside `hovered` state:
```tsx
const [pinned, setPinned] = useState<string | null>(null);
```

Change `active` derivation (line 66):
```tsx
// Before:
const active = placed.find((p) => p.product.barcode === hovered);
// After:
const active = placed.find((p) => p.product.barcode === (pinned ?? hovered));
```

### Fix 3 — SVG group events (inside the `placed.map`)

Add `onClick` and `onTouchStart` to each `<g>` element alongside existing mouse events:
```tsx
onClick={() =>
  setPinned((prev) =>
    prev === p.product.barcode ? null : p.product.barcode
  )
}
onTouchStart={() =>
  setPinned((prev) =>
    prev === p.product.barcode ? null : p.product.barcode
  )
}
```

When `pinned` is set, show a small "pin" indicator on the active circle — add a second ring:
```tsx
{pinned === p.product.barcode ? (
  <circle
    cx={p.cx}
    cy={p.cy}
    r={p.r + 8}
    fill="none"
    stroke={color}
    strokeWidth={1.5}
    opacity={0.35}
    strokeDasharray="3 3"
  />
) : null}
```

### Fix 4 — Tooltip card styling

Current tooltip div (lines 222–231) — replace with:
```tsx
<div className="mt-4 rounded-[1.1rem] border border-black/[0.06] bg-[#F7F7F2]/60 px-4 py-3.5">
  <div className="flex items-start justify-between gap-3">
    <p className="text-sm font-extrabold text-[#111318]">{active.label}</p>
    <span className="shrink-0 rounded-full bg-[#1F8F6A] px-2.5 py-0.5 text-xs font-extrabold text-[#F7F7F2]">
      {active.product.score}
    </span>
  </div>
  <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">
    {active.placementInsight}
  </p>
  <p className="mt-2 text-xs text-[#7A817C]">
    {active.product.productTypeLabel} · {active.ingredientCount} רכיבים ברשימה
    {pinned ? " · לחצו שוב לביטול הנעיצה" : ""}
  </p>
</div>
```

### Fix 5 — Empty state text

Line 233–235 — change from generic Hebrew to:
```tsx
<p className="mt-4 text-xs text-[#7A817C]">
  העבירו את העכבר על נקודה — או לחצו לנעיצה — לפרטי המוצר
</p>
```

### Acceptance criteria

- Container has `rounded-[1.2rem]`
- Clicking a dot pins it (tooltip persists after mouse leaves)
- Clicking pinned dot unpins it
- Pinned dot shows dashed outer ring
- Touch works same as click
- Tooltip shows score as green pill badge in top-right corner
- Empty state describes both hover and click interactions

---

## MILK-03 — MilkAnalysisComparisons: Score delta callout + mobile divider fix

**File:** `src/components/blog/milk-analysis-comparisons.tsx`

### Find the "לעומת" badge divider

Locate the element that shows the "לעומת" text between the two products. Current implementation likely uses `absolute` positioning that breaks on mobile stacked layout.

Replace with a responsive divider:
```tsx
{/* Desktop: centered absolute badge. Mobile: horizontal rule with label */}
<div className="relative flex items-center justify-center py-3 md:absolute md:inset-y-0 md:left-1/2 md:flex md:-translate-x-1/2 md:py-0">
  <span className="relative z-10 rounded-full border border-black/[0.08] bg-[#F7F7F2] px-3 py-1 text-xs font-bold text-[#7A817C]">
    לעומת
  </span>
  <div className="absolute inset-x-0 top-1/2 h-px bg-black/[0.06] md:hidden" />
</div>
```

### Score delta

In each product panel, if the product score and the counterpart score are accessible in the data, add a score delta line below the score:
```tsx
<p className="mt-1 text-xs text-[#7A817C]">
  הפרש ציון: <span className="font-bold text-[#111318]">+{Math.abs(delta)}</span> לטובת {higherProductName}
</p>
```

This requires knowing both products' scores in the same render scope. Cursor should check how `ComparisonBlock` receives its data to determine if both scores are available and compute the delta there.

### Internal label cleanup

Replace the `<dt>` labels:
- `"הערת פורמולציה"` → `"מה ההבדל בהרכב"`
- `"מה השתנה?"` → `"מה משתנה כשבוחרים"`
- `"למה התפצלו"` — keep as-is, it reads naturally

### Acceptance criteria

- "לעומת" divider renders correctly on mobile (no overlap, not clipped)
- Score delta shown in at least one product panel
- No internal jargon labels visible

---

## MILK-04 — MilkAnalysisSimplicity: Ingredient chip pills

**File:** `src/components/blog/milk-analysis-simplicity.tsx`

### Replace truncated string display

Locate: `product.ingredients_display.slice(0, 48)` — remove this.

Replace with comma-split + pill array:

```tsx
const ingredientChips = useMemo(() => {
  const raw = product.ingredients_display ?? "";
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 10);
}, [product.ingredients_display]);

const totalCount = (product.ingredients_display ?? "").split(",").filter(Boolean).length;
```

Render:
```tsx
<div className="mt-3 flex flex-wrap gap-1.5">
  {ingredientChips.map((chip, i) => (
    <span
      key={i}
      className="rounded-full border border-black/[0.06] bg-[#F7F7F2] px-2.5 py-0.5 text-xs text-[#4E5663]"
    >
      {chip}
    </span>
  ))}
  {totalCount > 10 ? (
    <span className="rounded-full border border-black/[0.06] bg-[#F7F7F2] px-2.5 py-0.5 text-xs font-bold text-[#7A817C]">
      +{totalCount - 10} נוספים
    </span>
  ) : null}
</div>
```

### Acceptance criteria

- Each ingredient renders as a separate pill, no mid-word cuts
- Maximum 10 pills shown, remainder shown as "+N נוספים"
- Pills use cream background with light border
- If `ingredients_display` is null/empty, render nothing (no crash)

---

## Implementation order

Execute in this sequence — each ticket is independent except where noted:

1. **HOME-01** — quick, no logic changes (remove decorations)
2. **HOME-02** — significant rewrite, test that section still anchors correctly
3. **MILK-01** — remove orbit visual, add KPI strip
4. **MILK-04** — simplest, self-contained ingredient pills
5. **MILK-02** — scatter pin state + tooltip polish
6. **HOME-03** — depends on knowing `MilkComparisonProduct` field shape
7. **MILK-03** — depends on knowing `ComparisonBlock` data shape

---

## What Cursor must NOT do

- Do not add new animations or framer-motion usage to replace what was removed
- Do not add new decorative visuals, icons-as-decoration, or gradient fills
- Do not invent new data fields — use only what exists in the type definitions
- Do not change the routing, URL structure, or page meta
- Do not rename existing components — modify in-place
- Do not add new npm packages
- Do not add comments explaining what the code does — only if a constraint is non-obvious
