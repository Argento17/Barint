# Bari Design Token Governance Rules — v1

**Status:** Active  
**Date:** 2026-05-28  
**Token file:** `src/lib/design/bari-comparison-tokens.ts`  
**Secondary token surface:** `src/app/globals.css` (`@layer components` — Bari-prefixed CSS classes only)

---

## Purpose

Design tokens are the single source of truth for visual values across all Bari comparison pages. Token governance exists to prevent:

- Token proliferation (more tokens than there are decisions)
- Inline value duplication (hardcoded values that shadow tokens)
- Category-specific token drift (per-category overrides that fragment visual consistency)
- Orphaned tokens (values that accumulate in the token file but are used nowhere)

The token file is small by intention. Every token must earn its place.

---

## Section 1 — Allowed Token Categories

The token file is organized into named categories. Only the following categories are permitted. A new top-level category requires explicit approval.

| Category | Key in token file | Purpose | Status |
|---|---|---|---|
| `rows` | `BARI_COMPARISON_TOKENS.rows` | Row alternating background colors and CSS class names | Active |
| `score` | `BARI_COMPARISON_TOKENS.score` | Score chip geometry/structure values (grade color comes from `gradePalette`) | Active (see §7 for restrictions) |
| `typography` | `BARI_COMPARISON_TOKENS.typography` | Shared text style class strings | Active |
| `layout` | `BARI_COMPARISON_TOKENS.layout` | Pixel dimensions: row height, image size, chip size | **Must be added** — currently absent |
| `methodology` | `BARI_COMPARISON_TOKENS.methodology` | Methodology footer font size and color | **Must be added** — currently absent |
| `insightLine` | `BARI_COMPARISON_TOKENS.insightLine` | Insight line font size and color | **Must be added** — currently absent |
| `gradePalette` | `BARI_COMPARISON_TOKENS.gradePalette` | Grade-to-color mapping (A→E ramp) | **Active — canonical** (Gen 1.1, owner directive 2026-06-03). Source the canonical chip's grade tint/accent. Shared with legacy. See §7. |

No other top-level categories may be added without review.

---

## Section 2 — Required Tokens Not Yet Present

The following tokens are required by the canonical component spec but do not exist in the token file. They must be added before building the corresponding component.

Add under new top-level keys as follows:

```ts
layout: {
  rowHeightMobile: "72px",
  rowHeightMobileMax: "80px",
  rowImageSize: "56px",
  scoreChipSize: "28px",          // font-size for score numeral in row context
  heroMaxHeight: "280px",
  heroImageHeight: "160px",       // target; max 180px
},

insightLine: {
  fontSize: "13px",
  color: "#444444",
  lineHeight: "1.4",
  maxWords: 12,
},

methodology: {
  fontSize: "12px",
  color: "#AAAAAA",
  maxSentences: 4,
},
```

These values are not to be hardcoded inline in components. If a component needs `13px` for an insight line, it reads `BARI_COMPARISON_TOKENS.insightLine.fontSize`.

---

## Section 3 — Naming Conventions

### TypeScript keys

- camelCase throughout: `rowHeightMobile`, `scoreChipSize`, `backgroundColor`
- No abbreviations: `background` not `bg`, `border` not `bdr`, `fontSize` not `fs`
- Exception: existing keys `oddBg` / `evenBg` in `rows` are grandfathered — do not rename

### Value format

| Value type | Format | Example |
|---|---|---|
| Hex color | 6-digit uppercase hex | `"#444444"` |
| Hex color with opacity | 8-digit or `rgba()` | `"rgba(17,19,24,0.10)"` |
| Pixel dimension | String with px suffix | `"72px"` |
| Tailwind class string | Exact Tailwind utility | `"font-extrabold tabular-nums"` |
| Numeric constant | Number, no unit | `12` (maxWords, maxSentences) |

Do not mix formats within a category. Do not store raw numbers where a pixel string is needed.

### Key specificity

Token keys name the thing they control, not where they are used. 

- `rowHeightMobile` — names the constraint, not the component: PASS
- `productRowMobileHeight` — names the component: FAIL (the token may be reused elsewhere)
- `fontSize13` — names the value, not the thing: FAIL

---

## Section 4 — Override Rules

### Within canonical components

Canonical components (`src/components/shared/`) must consume token values. Hardcoded values that duplicate a token are prohibited.

**Permitted:**

```tsx
// Reading from token
<div style={{ height: BARI_COMPARISON_TOKENS.layout.rowHeightMobile }}>
```

```tsx
// Using a token-derived Tailwind class
<div className={BARI_COMPARISON_TOKENS.rows.zebraRowClass}>
```

**Prohibited:**

```tsx
// Hardcoded value that duplicates a token
<div style={{ height: "72px" }}>

// Inline color that duplicates a token
<span style={{ color: "#444444" }}>
```

The test: if the value appears in the token file, it must be read from there. If it does not appear in the token file, either add it (if it is a design decision that applies across pages) or use a Tailwind utility (if it is a local layout detail).

### Within legacy components

Legacy components (`milk-comparison-page.tsx`, `bread-comparison-dashboard.tsx`, `snack/`) are exempt from this rule. They are read-only quarantined code. Do not add token consumption to legacy components — that constitutes a destructive change under `legacy_isolation_policy_v1.md`.

### Tailwind inline values

Some local values — padding, margin, gap — are not design decisions; they are layout details. These are correctly expressed as inline Tailwind classes (`p-4`, `gap-3`) and do not require tokens.

A value requires a token when:
- It encodes a measurement that must be consistent across multiple components (row height, image size)
- It encodes a color that must not vary per category
- It encodes a typographic value that defines a named text role (insight line, methodology)

A value does not require a token when:
- It is internal spacing within a single component
- It is an animation timing value
- It is a border-radius on a card that only exists in that component

---

## Section 5 — Deprecation Policy

### When a token is deprecated

A token is deprecated when:
- The component that consumed it has been removed or replaced by a canonical equivalent
- The pattern it encoded has been declared Gen 0 (see `architecture_generations_registry_v1.md`)
- It has been replaced by a more specific token with a cleaner name

### Deprecation procedure

1. Add a JSDoc comment to the token in the file: `/** @deprecated — reason; do not use in canonical components */`
2. Do not remove the token until all legacy consumers are confirmed to be either removed or migrated
3. Update this document's deprecated token list (Section 6)
4. Removal happens as part of a legacy migration, not as standalone cleanup

### Deprecated tokens must not be used in new code

Once a token is marked deprecated, it must not appear in any new component, regardless of how convenient it would be. If a deprecated token holds a value you need, add a new token with the correct name.

---

## Section 6 — Deprecated Tokens

| Token path | Deprecated reason | Safe to remove when |
|---|---|---|
| `BARI_COMPARISON_TOKENS.score.hero.labelSize` | Used for the legacy free-text grade label — the canonical chip carries an approved tier word in its tier slot, not this legacy label token | All legacy consumers (`bari-grade-badge.tsx`, `snack-score-chip.tsx`) are removed or migrated |
| `BARI_COMPARISON_TOKENS.score.hero.labelClass` | Same — legacy grade-label styling, not used by the canonical chip | Same as above |
| `BARI_COMPARISON_TOKENS.score.comparisonChip` | Comparison chip uses a *saturated, solid-fill* rendering — that treatment is Gen 0; the canonical chip uses the tinted `gradePalette` accent instead | All consumers migrated |

These tokens remain in the file. They are quarantined from canonical component use.

> **Note:** `BARI_COMPARISON_TOKENS.gradePalette` is **no longer deprecated.** As of the Gen 1.1 directive (owner, 2026-06-03) it is the canonical source of the score chip's grade tint and accent color and is consumed by canonical components. It was previously listed here as deprecated under the original neutral-chip spec; that listing is superseded. The *legacy visual treatment* of grade color (saturated fill, free-text label) remains Gen 0 — only the grade-to-color mapping is shared and canonical.

---

## Section 7 — Category-Specific Token Prohibition

Tokens must be category-agnostic. The following are prohibited:

**Prohibited token patterns:**

```ts
// Category-specific token keys
breadRows: { ... }         // PROHIBITED — use rows for all categories
maadanimScoreSize: "28px"  // PROHIBITED — use layout.scoreChipSize
snackFilterColor: "..."    // PROHIBITED — filters use shared tokens
milkHeroHeight: "..."      // PROHIBITED — hero uses layout.heroMaxHeight
```

**Prohibited pattern: tokens that encode category editorial decisions**

Token values must be visual constants, not editorial ones. These are prohibited:

```ts
// Editorial decisions masquerading as tokens
insightLineMaxWordsForDairy: 12     // PROHIBITED — max is 12 for all categories
maadanimMethodologyColor: "#AAAAAA" // PROHIBITED — methodology color is universal
```

**Prohibited pattern: conditional tokens**

A token must have a single value. Conditional values by category, viewport, or context are not tokens — they are component logic.

```ts
// Conditional token — PROHIBITED
rowHeight: { mobile: "72px", desktop: "80px" }  // This is component logic, not a token
```

If a value varies by viewport, the variation is expressed in the component using Tailwind responsive prefixes (`sm:`, `md:`), not by creating multiple tokens.

---

## Section 8 — Additive-Token Review Process

Before adding a new token to `bari-comparison-tokens.ts`, answer these questions:

1. **Is this value used in more than one component?** If no — it is not a token. It is a local value. Keep it inline.
2. **Is this value a design decision that must be consistent across categories?** If no — it is not a token.
3. **Does this value already exist in the token file under a different key?** If yes — use the existing token. Do not add a duplicate.
4. **Does this value belong to a permitted category (Section 1)?** If no — a new category review is needed first.
5. **Is this value category-agnostic (Section 7)?** If no — it cannot be a token.

Only if all five checks pass: add the token.

**Process:**
- Add to `bari-comparison-tokens.ts` under the correct category key
- Add to the required-tokens table in `frontend_integration_checklist_v1.md` Section 4
- Consume immediately in the component that required it — do not add tokens speculatively

**What is not a token:**
- Animation durations and easing curves
- Z-index values
- Component-internal padding and margin
- Border-radius values that only apply within one component
- Breakpoint values (use Tailwind's built-in system)
- Shadow values that only appear on legacy card patterns

---

## Section 9 — Duplicate Token Prevention

Before adding any color, size, or font value to a component, run this check:

1. Search `bari-comparison-tokens.ts` for the value (`"#444444"`, `"72px"`, `"13px"`)
2. If found: use the existing token key — do not add a new key with the same value
3. If the value is close but not identical: confirm whether a token with the canonical value exists, and whether your component should use that canonical value instead of a slightly different one

**The hardcoded value problem:**

When a value is hardcoded in a component without checking the token file, it creates a silent duplicate. If the token is later updated, the hardcoded value does not update. This is the primary mechanism by which visual inconsistency spreads across categories.

Grep for any hardcoded color or size value before adding it to a component:

```
grep -r "#444444" src/components/shared/
grep -r "72px" src/components/shared/
grep -r "13px" src/components/shared/
```

If the grep finds the value in the token file, the component must read it from the token file. If the grep finds the value hardcoded in another shared component, that is a token missing from the token file — add the token and fix both locations.

---

## Current Token File State

For reference, the current token file contains:

| Key path | Value type | Status |
|---|---|---|
| `gradePalette.{A-E}.{bg,text,border}` | Hex colors | **Active — canonical** (Gen 1.1); grade tint/accent source for the chip, shared with legacy |
| `rows.oddBg` | `#FFFFFF` | Active |
| `rows.evenBg` | `#F9F9F9` | Active |
| `rows.zebraRowClass` | Tailwind class string | Active |
| `rows.zebraContainerClass` | Tailwind class string | Active |
| `typography.sectionEyebrow` | Tailwind class string | Active — legacy page typography |
| `typography.sectionTitle` | Tailwind class string | Active — legacy page typography |
| `typography.sectionMeta` | Tailwind class string | Active — legacy page typography |
| `score.hero.*` | Tailwind class strings + sizes | **Partially deprecated** — `labelSize`, `labelClass` deprecated |
| `score.rowChip.*` | Tailwind + hex values | Active — chip geometry/structure (grade color now from `gradePalette`) |
| `score.comparisonChip.*` | Tailwind class strings | **Deprecated** — saturated solid-fill comparison chip (Gen 0 treatment); canonical uses tinted `gradePalette` accent |
| `layout.*` | Pixel strings | **Missing — must add** |
| `insightLine.*` | Pixel/hex values | **Missing — must add** |
| `methodology.*` | Pixel/hex values | **Missing — must add** |

---

*Token governance applies to `bari-comparison-tokens.ts` and to any CSS custom property or class defined in `globals.css` under `@layer components` with a `bari-` prefix. Tailwind utility classes in components are not governed by this document — only named Bari tokens are.*
