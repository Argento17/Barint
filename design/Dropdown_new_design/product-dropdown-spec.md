# Product Dropdown (expansion) — implementation spec

**Status:** Accepted direction. Engineering + design handoff for the redesigned
product **expansion** (the dropdown that opens under each comparison row).
**Source of truth:** `Bari Product Dropdown.html` (prototype, milk shelf). This doc
translates it into build decisions. Pairs with `handoff/comparison-v2-spec.md` (row +
shelf chrome) — this spec covers **only the expansion body**; the collapsed row,
band rail, and density toggle are unchanged from v2.

**Scope:** one expansion component, identical for **every category** (milk, hummus,
bread, …). Differences between categories are **data + metric config**, never layout.

---

## Where this lives in the repo

**Repo:** `bari-web` (Next.js App Router · package name `bari`). All paths below are
relative to `bari-web/`.

| What | File | Action |
|---|---|---|
| **The shared expansion component** (primary target) | `src/components/shared/expansion-section.tsx` | Re-skin the body to this spec. Labels already exist as constants `LABEL_POSITIVE` / `LABEL_LIMITING` / `LABEL_COMPARISON` / `LABEL_BOTTOM` — **keep them verbatim** (note: canonical strings end in `?`: `"מה עובד לטובת המוצר?"`, `"מה מגביל את הציון?"`). |
| Row that mounts the expansion | `src/components/shared/comparison-row.tsx` (`<ExpansionSection expansion={product.expansion} … />`, ~L240) | No change beyond passing existing props. |
| **Additives sub-dropdown** | `src/components/shared/AdditivePanel.tsx` | Restyle into the collapsible §3.5; wire its clean/has states. |
| Older positive/limiting block (if still referenced) | `src/components/shared/deep-dive-section.tsx` (L125 `מה עובד לטובת המוצר?`) | Reconcile — single source of truth should be `expansion-section.tsx`. |
| **VM types** | `src/lib/view-models/index.ts` — `BariExpansionVM` (~L32), `BariProductVM` (~L225) | Confirm/extend per §2: `limitingFactors` magnitude, `nutrition.*`, `rank`/`categoryTotal`. Most fields already exist. |
| Per-category data wiring | `src/lib/comparisons/<category>-page-data.ts` (e.g. `milk-page-data.ts`, `hummus-comparison-page-data.ts`) + `src/data/<category>-comparison.json` | Populate the metric scales/thresholds and `rank`/`categoryTotal`. |
| Milk page (matches the prototype) | `src/components/comparisons/milk-comparison-page.tsx` | Currently bespoke — fold onto the shared expansion (see `MILK_RECOMMENDATION.md`). |
| Primitives reused as-is | `bari-grade-badge.tsx`, `bari-product-thumbnail.tsx`, `confidence-marker.tsx` | No change. |

> The expansion is **already shared** across categories via `ExpansionSection` — this is
> a re-skin of an existing component, not a new one. Hold the order/label/VM invariants
> in §0–§2 and the existing per-category data wiring keeps working.

---

## 0. Non-negotiables (carried from v1/v2)

1. **Pre-authored Hebrew, verbatim.** No runtime copy generation. Every string renders
   from the VM. Keep the exact section labels below.
2. **Interpretive-before-technical.** Fixed order: assessment → context → bottom line →
   nutrition/ingredients → additives. Never reorder.
3. **Limits are information, not alarms.** Limiting factors render in **neutral ink**,
   never red. The only color in the expansion is rationed Bari-green on the positive side.
4. **Every product gets the full taxonomy.** A product with zero limits and zero
   additives still renders both sections, in their resolved empty states (below).
5. **No algorithm exposure** (no NOVA/BSIP/caps language in user-facing strings).

---

## 1. Section order (one taxonomy, every product)

| # | Section | Label string (verbatim) | Source field |
|---|---|---|---|
| 1 | Assessment — two panels | `מה עובד לטובת המוצר` / `מה מגביל את הציון` | `positiveSignals` / `limitingFactors` |
| 2 | Shelf context | `הקשר במדף` | `rank`, `categoryTotal`, `comparisonContext` |
| 3 | Bottom line | `בשורה התחתונה` | `bottomLine` |
| 4 | Nutrition + ingredients | `ערכים תזונתיים · ל-100 מ״ל` | `nutrition` + `ingredients` |
| 5 | Additives (separate sub-dropdown) | `תוספי מזון` | `additives[]` |
| — | Footer | confidence tag + source line | `confidence`, `sourceLine` |

Each section is preceded by a **section header**: a mono uppercase label
(`var(--font-mono)`, 10.5px, `letter-spacing:0.16em`, `color:var(--fg3)`) followed by a
1px hairline rule filling the remaining width (`var(--hairline-faint)`).

---

## 2. Data contract (`BariProductVM` — additions to the v2 contract)

```ts
expansion: {
  positiveSignals: string[];          // "מה עובד" bullets (1–n)
  limitingFactors: { text: string; magnitude: number }[]; // magnitude 0–1, display-only weight
  comparisonContext: string;          // "הקשר במדף" prose (one short paragraph)
  bottomLine: string;                 // "בשורה התחתונה" one sentence
  ingredients: string | null;         // ingredient sentence; null → "רשימת רכיבים מלאה לא אומתה במקור."
  additives: { name: string; function: string }[]; // [] when none verified
}
nutrition: {                          // per-100ml (or per-100g); display-only
  protein_g: number | null;
  sugar_g:   number | null;
  energy_kcal: number | null;
  sodium_mg: number | null;
}
rank: number;                         // position within the full category corpus
categoryTotal: number;                // size of the category corpus
confidence: "verified" | "partial" | "insufficient";
sourceLine: string;                   // e.g. "מקור: שופרסל · עודכן השבוע"
```

- `magnitude` is **display-only** (derived from existing label data; bar width). It is
  **not** a score input. Never surface a number for it — it is a relative bar only.
- Null nutrition cells render `—`, never `0`.
- `additives` and `limitingFactors` empty arrays are valid and have defined empty states.

---

## 3. Section specs

### 3.1 Assessment — two panels (`wlGrid`, 2-col → 1-col < 640px)

**Positive panel** (`.panel.works`): background `#F1F8F4`, border `rgba(31,143,106,0.16)`,
radius `--radius-xl`. Title `מה עובד לטובת המוצר` in `--bari-green-deep`, with a count
pill (`positiveSignals.length`). Each item: green ring-check glyph + text (`--fg2`,
13px). Items separated by a 4%-ink hairline.

**Limits panel** (`.panel.limits`): background `#FAFAF7`, neutral. Title
`מה מגביל את הציון` in `--fg1`, count pill only when `length > 0`. Each item: neutral
dash glyph + text, **plus a magnitude bar** under the text (4px track `#E7E7E0`, fill
`#B9BEB7`, width = `magnitude * 100%`).
- **Empty state** (`limitingFactors.length === 0`): single row, green check glyph +
  `אין גורמים מגבילים מהותיים` in `--bari-green-deep`. No count pill.

### 3.2 Shelf context (`.shelfCtx`)

Panel: `#F6F7F4`, border `--hairline-soft`, radius `--radius-xl`.
- Top row: `מדורג <rank> מתוך <categoryTotal>` (rank emphasized in `--bari-green-deep`)
  on the start side; category meta (`חלב ומשקאות · לכל המדף`) mono on the end side.
- **Position track:** 6px bar with a left→right grade gradient
  (`#C77F5A → #C49A4A → #9A9A5E → #3FA07E → #1F8F6A`) at `opacity:0.5`. A 13px ring
  marker sits at `inset-inline-start = 100% − (rank−1)/(categoryTotal−1) × 100%`
  (RTL: best rank = end/right). Marker = white fill, 2.5px `--fg1` border.
- `comparisonContext` prose below (13px, `--fg2`, line-height 1.6).

### 3.3 Bottom line (`.bottomLine`)

White card, `border-inline-start: 3px solid var(--bari-green)`, radius `--radius-md`.
Mono kicker `בשורה התחתונה` (`--bari-green-deep`) + the sentence (`--fg1`, 13.5px).

### 3.4 Nutrition + ingredients

4-up grid (`repeat(4,1fr)` → `repeat(2,1fr)` < 640px). Each cell: mono label, big
extrabold tabular value with a small unit (`חלבון/סוכר` → `ג׳`, `אנרגיה` → `קק״ל`,
`נתרן` → `מ״ג`), and a 4px mini-bar.
- **Scales (category-scoped, dairy shown):** protein 0–8 g, sugar 0–8 g, energy 0–80
  kcal, sodium 0–80 mg. **Set per category** — do not reuse dairy scales for hummus
  (protein runs 0–22 there). Bars are display-only; the numeral is the source of truth.
- **Tone:** protein good ≥5 → green, <3 → amber; sugar good ≤1 → green, ≥6 → amber;
  otherwise neutral grey. Energy/sodium stay neutral grey.
- Ingredients line below the grid: mono `רכיבים` label + the sentence. If `null`, show
  `רשימת רכיבים מלאה לא אומתה במקור.` in `--fg3`.

### 3.5 Additives — **separate sub-dropdown** (`.addBox`)

A self-contained collapsible inside the expansion (own open state, independent of the
row). Header: a 30px rounded icon tile + title `תוספי מזון` + subtitle + count pill +
chevron.
- **Has additives** (`length > 0`): amber-tinted icon/pill, count = `length`, subtitle
  `לחצו לפירוט התוספים ותפקידם`, **expandable**. Open body lists each additive:
  `name` (start) + `function` chip (end, mono, `#F6F6F1`), rows split by hairline.
- **Clean** (`length === 0`): green-tinted icon, pill reads `ללא`, subtitle
  `לא זוהו תוספים — רכיבים מזוהים בלבד`. **Not clickable**, no chevron (`.addHead.static`).

### 3.6 Footer (`.expFoot`)

Top hairline, then: confidence tag (dot + `נתונים מלאים / חלקיים / חסרים`, color per
`confidence`) on the start side, `sourceLine` mono in `--fg4` pushed to the end.

---

## 4. Interaction / motion

- **Row expand:** CSS grid-rows `0fr → 1fr` over `--dur-fast` (280ms) `--ease-out-soft`.
  Multiple rows may be open. **Never `scrollIntoView`** on expand (yanks long lists).
- **Additives sub-dropdown:** same grid-rows technique, independent state, default
  **closed**.
- Chevrons rotate 180° on open over `--dur-fast`.
- **Reduced motion:** disable all expand/rotate transitions under
  `prefers-reduced-motion: reduce` (content shows instantly, never stuck at height 0).

## 5. Responsive

- `< 640px`: assessment panels stack to 1 column; nutrition grid → 2 columns; collapsed
  row hides the mini-metrics column (full metrics live in the expansion). Expansion
  padding tightens to 13px inline.
- The expansion never introduces horizontal scroll; all panels are fluid.

## 6. Accessibility / RTL

- Row + additives toggles are `<button aria-expanded>`; the clean additives header is a
  non-interactive `<div>` (no button role).
- All logical properties (`inset-inline`, `ms/me`, `border-inline-start`). The position
  marker is computed from `inset-inline-start` so it flips correctly in RTL.
- Magnitude bars and mini-bars are **decorative** — every value they encode is also
  present as text/numeral. Add `aria-hidden` to the bars; `aria-label` the metric cells
  (`"חלבון 3.3 גרם"`).
- Grade letter **and** number both announced in the badge.

## 7. Tokens (all from `colors_and_type.css` — no new values)

Green `--bari-green` / `--bari-green-deep`; ink scale `--fg1..4`; surfaces `--surface`,
`--surface-3`; hairlines `--hairline`, `--hairline-soft`, `--hairline-faint`; radii
`--radius-md/-xl/-2xl`; motion `--dur-fast`, `--ease-out-soft`; grade palette
`--grade-*`. Panel tints (`#F1F8F4`, `#FAFAF7`, `#F6F7F4`) and bar greys (`#E7E7E0`,
`#B9BEB7`, `#EEEEE8`) are the only literals — promote to tokens if reused elsewhere.

## 8. Acceptance criteria

- Every product renders all five sections in the fixed order, including resolved empty
  states for zero limits and zero additives.
- Section labels match the verbatim strings in §1; no runtime-generated copy.
- Limits render in neutral ink with magnitude bars; positives in green. No red anywhere.
- Additives is an independently-collapsible sub-dropdown; clean products show the
  non-clickable `ללא` state.
- Nutrition bars use **category-scoped** scales; null cells show `—`.
- Position marker lands at the correct rank in RTL; best rank sits at the end (right).
- Multiple rows open simultaneously; no `scrollIntoView`; reduced-motion safe.
- Copy is wired from the VM (this prototype's milk strings are illustrative — replace
  with corpus `expansion.*`).

## 9. Open items for design/data

- **Copy:** prototype prose (works/limits/context/bottomLine) is authored illustratively
  in Bari voice. Wire the real corpus strings; confirm `magnitude` derivation rule with
  data (suggest: normalized severity rank of each limiting factor, 0–1).
- **Thumbnails:** prototype uses one placeholder packshot — wire `ProductThumbnail`.
- **Scales per category:** define dairy/hummus/bread metric maxes + good/poor thresholds
  in the category metric config (don't hardcode dairy).
