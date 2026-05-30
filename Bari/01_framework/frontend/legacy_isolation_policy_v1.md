# Bari Legacy Isolation Policy — v1

**Status:** Active  
**Date:** 2026-05-28  
**Scope:** All existing comparison pages prior to מעדנים canonical build  
**Authority:** This policy takes precedence over any general refactor impulse during canonical component implementation.

---

## Purpose

The canonical v1 component build (ScoreChip → ProductRow → … → ComparisonPage) must not trigger uncontrolled refactors of existing comparison pages. Legacy pages are live, user-facing, and their technical debt is known. Fixing them during the canonical build creates scope creep, introduces regression risk, and delays the first canonical category launch.

Legacy pages are **quarantined**. They run as-is until they individually meet migration eligibility criteria. They do not block, inform, or constrain the canonical build.

---

## Definition of Legacy Pages

The following files and their direct dependencies are legacy:

| File | Route | Status |
|---|---|---|
| `src/components/comparisons/milk-comparison-page.tsx` | `/hashvaot/milk-comparison` | Legacy |
| `src/components/comparisons/bread-comparison-dashboard.tsx` | `/compare/bread-comparison` | Legacy |
| `src/components/snack/` (entire directory) | `/compare/snack-bars`, `/categories/snacks` | Legacy |
| `src/components/comparisons/milk-editorial/` (entire directory) | Sub-components of milk page | Legacy |
| `src/lib/comparisons/milk-page-data.ts` | Data layer for milk | Legacy |
| `src/lib/comparisons/bread-page-data.ts` | Data layer for bread | Legacy |
| `src/lib/comparisons/snack-page-data.ts` | Data layer for snack | Legacy |
| `src/components/comparisons/bari-grade-badge.tsx` | Used by milk and snack | Legacy — do not extend |
| `src/components/comparisons/dimension-bars.tsx` | Used by milk | Legacy |
| `src/components/comparisons/bari-interpretation-panel.tsx` | Used by milk | Legacy |
| `src/components/comparisons/matrix-integrity-badge.tsx` | Used by milk | Legacy |

**Legacy status is file-level, not feature-level.** A file is either legacy or canonical. There is no hybrid state.

---

## Additive vs. Destructive Changes

### Permitted: Additive changes to legacy files

An additive change modifies a legacy file without altering its existing behavior. Permitted additive changes:

- Adding a new exported constant or type that does not change existing exports
- Adding a `console.warn` or dev-mode warning for a known violation
- Updating data content (product data, editorial copy) within existing data shape
- Fixing a crash-level bug that affects live users

Additive changes to legacy files require no review beyond standard code review.

### Prohibited: Destructive changes to legacy files

A destructive change alters the rendering, structure, or behavior of a legacy file. Prohibited without explicit migration approval (see below):

- Replacing `BariGradeBadge` with the canonical `ScoreChip` in a legacy page
- Removing `DimensionBars`, `BariInterpretationPanel`, or `MatrixIntegrityBadge` from milk
- Replacing the bread hero with the canonical `CategoryHero`
- Converting the bread methodology `<details>` to `MethodologyFooter`
- Replacing `ProductCardGrid` in snack with `ProductRow`
- Changing filter behavior in any legacy page
- Any change that would require updating the legacy page's TypeScript types

**The test:** If a change requires touching more than one file in the legacy page's component tree, it is a migration, not a patch. Treat it as such.

---

## Token File Rules

`src/lib/design/bari-comparison-tokens.ts` is shared between legacy and canonical pages.

| Operation | Rule |
|---|---|
| Adding new tokens | Permitted — additive |
| Modifying existing token values | **Prohibited** without audit of all legacy consumers |
| Removing existing tokens | **Prohibited** — legacy pages depend on them |
| Adding `gradePalette` usage in new components | **Prohibited** — canonical components must not consume `gradePalette` |
| Quarantining `gradePalette` from canonical components | Enforced by convention — canonical ScoreChip does not import it |

`gradePalette` remains in the token file for legacy page compatibility. Its presence does not constitute approval for use in canonical components.

---

## Migration Eligibility Criteria

A legacy page becomes eligible for migration to the canonical component architecture when **all five** of the following are true:

1. **Canonical precedent exists** — at least one category page (מעדנים or later) has been fully built, visually approved, and running in production using the canonical component set.
2. **Data contract is stable** — the canonical data shape (`maadanim-types.ts` or equivalent) has been in production without breaking changes for at least one full content update cycle.
3. **No active editorial dependency** — the legacy page has no scheduled editorial content updates in the next two weeks that could be disrupted by a migration.
4. **Migration scope is bounded** — the migration replaces the legacy page's component tree with canonical components without changing data, routing, or URL.
5. **Explicit approval** — migration is explicitly approved, not inferred from general cleanup intent.

Meeting eligibility criteria does not trigger migration automatically. It enables migration to be proposed.

---

## Leave-As-Is Governance Rules

The following conditions require the legacy page to be left as-is, regardless of how obviously wrong the pattern is:

| Condition | Rule |
|---|---|
| Pattern violates Bari spec but page is live | Leave as-is. Document the violation in the audit. Do not fix during canonical build. |
| Score chip shows color by grade in milk or snack | Leave as-is. Do not import canonical ScoreChip into legacy pages. |
| Expansion section contains framework terms | Leave as-is. Do not edit milk expansion during מעדנים build. |
| Bread hero exceeds 280px | Leave as-is. |
| Bread methodology is a collapsible card | Leave as-is. |
| Snack filter panel exposes NOVA options | Leave as-is. Document as legacy drift. |
| Legacy page uses `bari-grade-badge.tsx` | Leave as-is. The canonical ScoreChip replaces it in new pages only. |

**The principle:** The canonical build is the correction. It does not require the legacy pages to change before or during it. The presence of legacy violations does not lower the canonical standard — it defines what the canonical standard is correcting.

---

## Canonical-Page Precedence Rules

When a canonical component and a legacy component implement the same concept differently, the canonical implementation is authoritative and the legacy one is deprecated.

| Concept | Canonical file | Legacy equivalent | Legacy status |
|---|---|---|---|
| Score display | `src/components/shared/score-chip.tsx` | `bari-grade-badge.tsx`, `snack-score-chip.tsx` | Deprecated — new pages only use canonical |
| Product row | `src/components/shared/product-row.tsx` | `ProductShelfRow` (inline in milk) | Deprecated |
| Expansion | `src/components/shared/expansion-section.tsx` | Expansion block (inline in milk) | Deprecated |
| Hero | `src/components/shared/category-hero.tsx` | `ComparisonHero` (inline in bread) | Deprecated |
| Methodology | `src/components/shared/methodology-footer.tsx` | `<details>` block in bread | Deprecated |
| Filter | `src/components/shared/sticky-filter-button.tsx` | Pill buttons (bread), `FilterPanel` (snack) | Deprecated |

**Deprecation means:** the legacy component continues to function in existing pages, but is not used in any new page build, and is not the reference for design decisions.

When in doubt about which implementation is correct — a canonical component or a legacy one — the canonical component is always correct, regardless of which was built first or which has more users.

---

## Scope Creep Definition

The following actions constitute scope creep during the מעדנים canonical build and are prohibited:

- Refactoring a legacy file "while I'm in here"
- Updating `bari-grade-badge.tsx` to match canonical ScoreChip behavior
- Moving snack components to `src/components/shared/`
- Removing `DimensionBars` or `BariInterpretationPanel` from the codebase
- Renaming legacy files to indicate deprecation
- Adding deprecation comments to legacy components
- Updating milk data types to match canonical types
- Any change to bread or snack routes, routing config, or page metadata

If a scope creep action is identified mid-build, stop. Log it. Proceed with the canonical build. Address it in a separate, bounded task after מעדנים launches.

---

## Summary: Two Codebases in One Repo

During the canonical build phase, this repo contains two parallel implementations of the same concept:

```
Legacy (read-only, leave as-is):
  src/components/comparisons/milk-comparison-page.tsx
  src/components/comparisons/bread-comparison-dashboard.tsx
  src/components/snack/
  src/components/comparisons/bari-grade-badge.tsx
  src/components/comparisons/dimension-bars.tsx
  src/components/comparisons/bari-interpretation-panel.tsx
  src/components/comparisons/matrix-integrity-badge.tsx

Canonical (actively building):
  src/components/shared/score-chip.tsx
  src/components/shared/product-row.tsx
  src/components/shared/expansion-section.tsx
  src/components/shared/product-table.tsx
  src/components/shared/category-hero.tsx
  src/components/shared/category-prologue.tsx
  src/components/shared/methodology-footer.tsx
  src/components/shared/sticky-filter-button.tsx
  src/components/comparisons/maadanim-comparison-page.tsx
```

These two trees do not cross. A component in one tree does not import from the other. This is intentional and correct.

---

*This policy is in effect until all legacy pages have been migrated to canonical components or explicitly retired. Policy changes require the same approval level as a new exception registry entry.*
