# Handoff: Unify the `/hashvaot` comparison tables

> **Task type — refactor/consolidation, not greenfield.** This package documents a
> consolidation of the existing Bari comparison-table code (Next.js + React +
> Tailwind, the `bari-web` repo). The goal is to collapse **four divergent table
> renderers into one responsive component** that every product category inherits.
> The HTML files in this bundle are **design references** — prototypes showing the
> intended look and behavior. Recreate them using the repo's existing patterns
> (the shared `@/components/shared/*` and `@/lib/design/bari-comparison-tokens`
> primitives), not by pasting the prototype HTML.

---

## 1. Overview

`bari.digital/hashvaot/*` hosts seven product comparison tables (hummus, maadanim,
yogurts, vegetable-spreads, snacks, bread, milk). A code-level audit found they do
**not** share one table experience — they've drifted into three. This handoff
delivers:

1. **The audit** — what diverged and why (`Bari Comparison Table Consistency Audit.html`).
2. **The target** — a working prototype of the single unified table
   (`Bari One-Table Prototype.html`).
3. **This README** — the migration plan, component spec, design tokens, and data
   contract, keyed to the real files in the repo.
4. **`MILK_RECOMMENDATION.md`** — a standalone decision + field-mapping for the milk page.
5. **`comparison-v2-spec.md`** — the previously-accepted v2 direction (the prototype implements it).

## 2. Fidelity

**High-fidelity.** The prototype uses final Bari tokens (colors, type, spacing,
metric scales, motion). Recreate the visual result pixel-faithfully using the
repo's Tailwind setup and `BARI_COMPARISON_TOKENS`. Copy values from `colors_and_type.css`
(the canonical token source, mirrored in the app's `next/font` + tokens module).

---

## 3. The problem (audit summary)

Three kinds of divergence exist today. There should be **none** — categories should
differ only in **data**, never in **layout**.

| # | Divergence | Affected | Severity |
|---|---|---|---|
| **D1** | **Milk is a parallel table** — own `MilkComparisonPage` + `ProductShelfRow`; shares no row/grade/thumbnail/expansion. Unique metric model (sugar/100ml, main ingredient) + unique expansion taxonomy. | Milk | High |
| **D2** | **Mobile and desktop are different components** — desktop = `BariProductShelfRow`, mobile = `ProductRow`. Different grade UI, thumbnail, expansion markup; the "בקצרה:" prefix is desktop-only. | All 6 canonical | High |
| **D3** | **The v2 row ships to only 2 of 6** — `v2Slice` is `true` for Hummus + Maadanim, `false` for Yogurts/Spreads/Snacks/Bread. v2 = RowReason +/−, promoted confidence, protein metric, single disclosure; v1 = `insightLine`, buried confidence, double "advanced" toggle. | Hummus/Maadanim vs rest | Medium |
| **D4** | **A whole desktop table path ships dead** — `ProductRow`'s `isWeb` web-grid branch + `ProductTableHeader` + `ComparisonShelfPage` `layout="web"` are never invoked in production. | shared components | Low |

---

## 4. Target architecture

```
ComparisonPage (per category — thin: data + hero copy + filters only)
└── ComparisonTable (shared)
    ├── ColumnHeader            (desktop only; one definition)
    ├── BandRail                (side, ≥680px container; scroll-only jumps)
    └── ComparisonRow  ← ONE responsive component, mobile + desktop via CSS
        ├── GradeBadge          (one primitive — replaces ScoreChip + BariGradeBadge)
        ├── ProductThumbnail    (one primitive — replaces ProductImage + BariProductThumbnail + ProductThumbnail)
        ├── MetricColumn        (protein bar · additive pips · base % — fixed widths, aligned)
        ├── ConfidenceIndicator (promoted onto the row)
        └── Expansion           (one taxonomy; one disclosure)
```

**Key principle proven by the prototype:** the phone vs desktop difference is **pure
CSS** (a container query on the list wrapper), not a second component. The DOM is
identical at both widths; only `grid-template-areas`, column visibility, and the
rail's presence change. See `proto/proto-components.jsx` (`ComparisonRow`) and the
`@container cmptable` rules in `Bari One-Table Prototype.html`.

---

## 5. Component spec — the unified `ComparisonRow`

### Layout grid

**Desktop (container ≥ 680px)** — single aligned line:
```
grid-template-columns: 30px 56px minmax(0,1fr) 232px 156px;
grid-template-areas:    "rank thumb name metric grade";
align-items: center;  padding: 13px 22px;
```

**Mobile (container < 680px)** — stacked, rank + rail hidden, metrics wrap below:
```
grid-template-columns: auto 1fr auto;
grid-template-areas:    "thumb name grade"
                        "metric metric metric";
padding: 14px 16px;  gap: 12px 14px;
```

Implement the breakpoint with a **container query** on the scroll wrapper
(`container-type: inline-size`), **not** a viewport media query — this is what lets
the same component sit in a 375px shell or a 1140px workspace and Just Work, and it
is what ends the "hummus-vs-others 375px drift" called out in `comparison-v2-spec.md` §9.

### MetricColumn (the differentiator — v2 spec §2/§4)

Three fixed-width (62px) metrics so they align column-to-column down the list:

| Metric | Scale | Good | Poor | Render |
|---|---|---|---|---|
| Protein | 0–20 g | ≥10 (`#1F8F6A`) | <5 (`#B5882F`) | label + value + 3px bar |
| Additives | 0–5 | ≤1 (`#1F8F6A`) | ≥4 (`#B5882F`) | label + count + 5 pips |
| % grain (`base`) | 0–100 % | ≥80 | <55 | label + value + 3px bar |

Neutral grey `#9AA09B`/`#B5BBB6` otherwise — **limits are information, not alarms; no red.**
Null renders `—`, never `0` (§2.3). The numeric value is the source of truth; bars/pips
are decorative and `aria-hidden`, with the group carrying an `aria-label`
(e.g. `חלבון 22 גרם`, `0 תוספי מזון`). Metric **set is category-configurable** — see §7 data contract and `MILK_RECOMMENDATION.md`.

### BandRail (v2 spec §3)

Sticky side affordance (inline-end → left in RTL), **hidden < 680px**. Bands:
`80+ · 70–79 · 60–69 · 50–59 · <50`, derived from `score`, contiguous in corpus order.
Each shows label + count + a proportion bar tinted green→amber as the band drops.
**Click = scroll only** — `scrollContainer.scrollTo({top: rowEl.offsetTop - 8})`.
**Never `scrollIntoView`** (it yanks long lists — §7). Honor `prefers-reduced-motion`.

### In-list band dividers (v2 spec §4)

Pure visual separators inserted when the score band changes between rows. They **do
not** regroup or reorder — corpus order is law (§Invariant 1).

### Expansion (one taxonomy — v2 spec §7)

Sections, in order: **מה עובד לטובת המוצר?** (positive) → **מה מגביל את הציון?**
(limiting) → **בשורה התחתונה** (bottomLine) → **הקשר במדף** (comparisonContext) →
technical (ingredients + serving) **inline, no second "advanced" toggle**. Multiple
rows may be open at once. Keep the exact Hebrew label strings.

### Confidence (promoted — v2 spec §5/§6)

`verified` → `נתונים מלאים` (`#1F8F6A`), `partial` → `נתונים חלקיים` (`#B5882F`),
`insufficient` → `נתונים חסרים` (`#B5BBB6`). On the **row** beside the grade — dot+label
on mobile, bordered pill on desktop. **Removed** from the 10px expansion footnote (de-dup).

---

## 6. Interactions & behavior

- **Expand/collapse:** click/Enter/Space on the row button; `aria-expanded`; animate
  `grid-template-rows: 0fr → 1fr` (240ms `cubic-bezier(.22,1,.36,1)`); reduced-motion → instant.
- **Multiple rows open** simultaneously is allowed.
- **Rail jump:** scrolls the list container only (see §5).
- **Filters:** subset the list and **preserve relative corpus order** (§Invariant 1). No client re-sort.
- **Insufficient-data products** render with a `—` no-score state — never hidden (§Invariant 2).
- **Density toggle** (compact/comfortable, §1): comfortable widens the thumb (52→60px) and relaxes row padding.

### Non-negotiable invariants (from `comparison-v2-spec.md`)

1. **Corpus owns order** — render in `BariProductVM[]` array order; filters preserve it.
2. **Every product individually visible** — no clustering, collapse-by-default, or pagination.
3. **Pre-authored Hebrew, verbatim** — no runtime copy generation.
4. **No algorithm exposure** — no BSIP/NOVA/caps/dimension language in user strings.
5. **Interpretive-before-technical** hierarchy inside the expansion.

---

## 7. Data contract additions (`BariProductVM`)

The aligned metric block + collapsed-row reason need structured fields (display-only,
derived deterministically from existing label data — **never** new score inputs):

```ts
metrics: {
  protein_g:      number | null,   // bar 0–20
  additive_count: number | null,   // pips 0–5
  base_pct:       number | null,   // main-ingredient %, bar 0–100
  sodium_mg:      number | null,   // expansion only
  energy_kcal:    number | null,   // expansion only
  // category-configurable extras (e.g. milk): sugar_g, per-100ml variants
}
rowReason: { positive: string | null, limiting: string | null }  // short, collapsed row
confidence: "verified" | "partial" | "insufficient"   // accuracy-gated per confidence_label_audit_v1
```

The **metric set rendered is category-scoped** — define it where the category's
filters/lens options live so milk can show sugar where hummus shows % grain, without
forking the component.

---

## 8. File-by-file migration plan (real repo paths)

### Edit / merge
- `src/components/shared/product-row.tsx` — make this the **single** responsive row.
  Port the desktop affordances from `BariProductShelfRow` into its `@container` rules.
- `src/components/shared/product-table.tsx` — keep as the list container; add
  `BandRail` + band dividers + `ColumnHeader`.
- `src/components/comparisons/bari-comparison-desktop-page.tsx` — stop rendering its own
  `BariProductShelfRow` list; render the shared `ProductTable`. Keep its hero/filters chrome.
- The 6 page wrappers (`hummus-`, `maadanim-`, `yogurts-`, `vegetable-spreads-`,
  `snacks-`, `bread-comparison-page.tsx`) — drop the `max-lg:block lg:hidden` /
  `lg:block` split; render **one** `ComparisonPage`. Remove per-page `v2Slice`.

### Delete (after merge)
- `src/components/comparisons/bari-product-shelf-row.tsx` (folded into `ProductRow`).
- `ProductRow`'s dead `isWeb` web-grid branch + `src/components/shared/product-table-header.tsx`
  if unused after the merge, + `ComparisonShelfPage` `layout="web"` mode (**D4**).
- `HUMMUS_V2_SLICE` / `MAADANIM_V2_SLICE` flags and all `v2Slice` props (**D3** — v2 becomes the only path).

### Consolidate primitives
- Grade: keep **`BariGradeBadge`**, remove `ScoreChip` usage.
- Thumbnail: pick one of `ProductImage` / `BariProductThumbnail` / `ProductThumbnail`; remove the others.

### Milk
- `src/components/comparisons/milk-comparison-page.tsx` + its inline `ProductShelfRow`
  → fold into the shared system per **`MILK_RECOMMENDATION.md`** (**D1**).

---

## 9. Tasks & acceptance criteria

| ID | Task | Done when |
|---|---|---|
| **IMP-1** | One responsive `ProductRow`; delete `BariProductShelfRow` | Both breakpoints render from one component; grade+thumbnail are single primitives; no `isWeb` branch remains |
| **IMP-2** | Make v2 default, remove `v2Slice` | All 6 categories show RowReason + promoted confidence + metric column; flag deleted |
| **IMP-3** | Fold Milk in | Milk renders via shared `ComparisonTable`; see `MILK_RECOMMENDATION.md` mapping; `MilkComparisonPage` row deleted |
| **IMP-4** | Finish v2 spec uniformly | Aligned metric column, band rail (scroll-only), in-list dividers, density toggle live for all |
| **IMP-5** | Delete dead web-grid path | `ProductTableHeader` + `layout="web"` gone or wired; no dead branches |
| **IMP-6** | Category notes once | Category-wide caveats (e.g. hummus fat note) in header/methodology, not per-row `unknowns` |

**Suggested order:** IMP-2 + IMP-6 (quick, ship now) → IMP-1 + IMP-5 (the structural fix) → IMP-3 + IMP-4 (one system, fully). Detail in the audit's §04.

### QA (per `comparison-v2-spec.md`)
- Re-capture baselines at **mobile + lg** (old 375px-only snapshots are invalid).
- Assert: filtered views preserve corpus order; rail jump lands on the band's first row;
  null metrics render `—`; no control removes a product from the DOM; RTL logical props
  (`inset-inline`, `ms/me`); grade letter + number both announced.

---

## 10. Design tokens

Canonical source: **`colors_and_type.css`** (in this bundle; mirrors the app tokens).
Highlights — **Brand** `--bari-green #1F8F6A`; **Ink** `#111318 / #4E5663 / #7A817C / #AAAAAA`;
**Canvas** `#F7F7F2`, surfaces `#FFFFFF / #F9F9F9 / #FAFAF8`; **Grades** A/B green
`#176F53`, C amber `#8F6600`, D/E red `#A63F2A / #8B2E2E`; **Signals** positive `#1F8F6A`,
limiting neutral ink (never red); **Type** Inter (Latin) + Heebo (Hebrew), Geist Mono
(numerals/labels); **Radii** 6–18px; **Motion** `cubic-bezier(.22,1,.36,1)`, 240–280ms.
Metric/confidence color thresholds are in §5.

---

## 11. Files in this bundle

| File | What it is |
|---|---|
| `README.md` | This document |
| `MILK_RECOMMENDATION.md` | Milk-page decision + field mapping |
| `Bari Comparison Table Consistency Audit.html` | The audit (findings + improvement plan) |
| `Bari One-Table Prototype.html` | **Target design** — the unified responsive table (interactive) |
| `proto/proto-components.jsx` | Prototype components (`ComparisonRow`, `MetricColumn`, `BandRail`, `Expansion`) |
| `proto/proto-data.jsx` | Real hummus sample data + band helpers |
| `colors_and_type.css` | Design tokens |
| `comparison-v2-spec.md` | Accepted v2 direction (the prototype implements it) |

> Open the two HTML files in a browser. In the prototype, the **Frame** control
> (Phone/Desktop) demonstrates the single-component reflow; **Layout** (v1/v2) shows
> the before/after; **Density** shows compact/comfortable.

### Illustrative-data caveat
In `proto/proto-data.jsx`, product **names, scores, grades, protein, sodium, energy,
ingredients, and confidence are real** (from `hummus_frontend_v2.json`). The
**`additive_count` and `base_pct`** values are **authored placeholders** — the live
corpus does not yet expose those structured fields (that's the §7 data-contract work).
Wire them to derived label data during implementation.
