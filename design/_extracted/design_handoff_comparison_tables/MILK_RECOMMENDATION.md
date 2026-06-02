# Milk page — recommendation

**Route:** `/hashvaot/milk-comparison`
**Files:** `src/components/comparisons/milk-comparison-page.tsx` (contains an inline,
bespoke `ProductShelfRow`), data in `src/lib/comparisons/milk-page-data.ts` +
`src/data/milk-comparison.json`.

---

## TL;DR — fold milk into the shared table; do not keep it bespoke

Milk is the single largest source of divergence in the audit (finding **D1**). It is a
**completely separate table**: its own page component, its own row, its own grade and
thumbnail usage, framer-motion animations, a unique 4-cell metric grid, and an
expansion taxonomy (`מה חשוב לדעת / מה מעלה / מה מוריד / בהשוואה` + a pillars panel)
that exists nowhere else.

**Recommendation: migrate milk onto the shared `ComparisonTable` (IMP-3).** Everything
that makes milk "special" is **data and configuration**, not layout — and the unified
component is explicitly designed to absorb it (category-configurable metric set +
optional expansion module). Keeping milk forked guarantees it keeps drifting: it has
already missed the v2 row, the promoted confidence, the aligned metric column, the band
rail, and the density toggle that the other categories are getting.

**Sequence it last** (after the six canonical categories are unified), so there's one
stable, fully-featured target to fold into — not a moving one.

---

## Why not keep it bespoke?

The case for "milk is genuinely different" rests on three things; none require a forked layout:

| "Milk is different because…" | Reality | Where it lives in the unified system |
|---|---|---|
| It shows per-100ml nutrition (protein, sugar) and a "main ingredient" | These are just **metrics + a chip** | Category-configurable `metrics` set (§7 data contract) + a type/ingredient chip under the name |
| Its expansion has its own sections | The sections **map 1:1** onto the shared taxonomy (table below) | One `Expansion` component, shared label strings |
| It has an "advanced — pillars" panel | A single **optional module**, gated by data | Optional pillars block at the foot of the shared expansion |

A forked layout costs: every shared fix (a11y, RTL, band rail, density, the next design
pass) has to be re-implemented in milk, or milk silently falls behind — which is exactly
the state the audit found.

---

## Migration mapping

### 1. Metrics (category-scoped set)

Milk's 4-cell grid → the shared fixed-width `MetricColumn`, configured for the dairy category:

| Milk cell (today) | Unified metric field | Scale / render |
|---|---|---|
| חלבון / 100 מ״ל | `protein_g` (per-100ml variant) | bar 0–? (set a dairy-appropriate max; protein-drinks run high) |
| סוכר / 100 מ״ל | `sugar_g` (**new category metric**) | bar; good low / poor high — tune thresholds for dairy |
| תוספים | `additive_count` | pips 0–5 (already shared) |
| רכיב עיקרי (main ingredient) | **not a metric** → render as a chip under the product name | small `Badge` (reuse `productTypeLabel` styling) |

> The shared `MetricColumn` takes a category metric list; milk passes
> `[protein, sugar, additives]` where hummus passes `[protein, additives, base]`.
> Same component, same alignment behavior, different columns.

### 2. Expansion taxonomy (relabel milk's content onto the shared sections)

| Milk section (today) | Shared expansion field (target) |
|---|---|
| `whatToKnow` (מה חשוב לדעת) | lead line of the expansion / `comparisonContext` intro |
| `raisesScore` (מה מעלה את הציון) | `positiveSignals` → **מה עובד לטובת המוצר?** |
| `lowersScore` (מה מוריד את הציון) | `limitingFactors` → **מה מגביל את הציון?** |
| `relativeToPeers` (בהשוואה למוצרים דומים) | `comparisonContext` → **הקשר במדף** |
| `takeawayLine` ("בקצרה: …") | `bottomLine` → **בשורה התחתונה** |
| `tradeoffNote` (עוד הקשר) | `caveats` (or appended to `bottomLine`) |
| pillars panel (advanced, `BariInterpretationPanel`) | **optional** module at foot of shared expansion, gated by `bariInterpretation?.length` |

This keeps every milk string verbatim (Invariant 3) while giving milk the shared
interpretive-before-technical order (Invariant 5).

### 3. Primitives & chrome

- Grade: already uses `BariGradeBadge` ✅ (matches the chosen shared primitive).
- Thumbnail: `ProductThumbnail` → the single shared thumbnail primitive.
- Hero: keep `ComparisonIntelligenceHero` (shared across categories) + the blog link.
- Drop the bespoke framer-motion row animation in favor of the shared CSS expand
  (240ms grid-rows) — and honor reduced-motion centrally.
- Milk's "main ingredient" + `productTypeLabel` become a chip row under the name.

### 4. Data work

- Extend the milk VM build to populate the shared `metrics` + `rowReason` fields
  (derive `rowReason.positive/limiting` from `raisesScore[0]` / `lowersScore[0]`).
- Add `sugar_g` to the dairy metric config; set dairy thresholds for protein & sugar
  (the hummus thresholds in §5 are category-scoped, not global).
- Apply the confidence accuracy-gate consistently (`verified/partial/insufficient`).

---

## Acceptance criteria

- `/hashvaot/milk-comparison` renders through the shared `ComparisonTable` — no
  milk-only row component remains; `milk-comparison-page.tsx` is reduced to data + hero + filters.
- Milk shows the aligned metric column (protein · sugar · additives), promoted
  confidence, band rail, dividers, and density toggle — same as every other category.
- All existing milk copy renders verbatim under the shared expansion labels.
- The pillars "advanced" view still works, as an optional module.
- Corpus order + filter-order invariants hold; no product is hidden.

---

## Risk / sequencing note

- **Do milk last.** Build IMP-1 (one row) and IMP-4 (metric set + rail) on the six
  canonical categories first; fold milk into the finished component.
- **Watch the metric scales.** Protein-fortified milk drinks exceed the hummus 0–20g
  scale — set dairy-specific maxes so bars stay meaningful (don't reuse hummus scales blindly).
- **Sugar coverage** is a real dairy signal (unlike hummus, where sugar is null/suppressed);
  make sure `sugar_g` is populated before relying on it as a metric column.
