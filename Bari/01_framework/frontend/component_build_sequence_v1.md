# Bari Comparison Component Build Sequence — v1

**Status:** Frozen  
**Date:** 2026-05-28  
**Applies to:** All Bari category comparison pages

---

## Canonical Build Order

| # | Component | File | Depends on |
|---|---|---|---|
| 1 | ScoreChip | `src/components/shared/score-chip.tsx` | nothing |
| 2 | ProductRow | `src/components/shared/product-row.tsx` | ScoreChip |
| 3 | ExpansionSection | `src/components/shared/expansion-section.tsx` | ProductRow |
| 4 | ProductTable | `src/components/shared/product-table.tsx` | ProductRow, ExpansionSection |
| 5 | CategoryHero | `src/components/shared/category-hero.tsx` | ScoreChip |
| 6 | CategoryPrologue | `src/components/shared/category-prologue.tsx` | nothing |
| 7 | MethodologyFooter | `src/components/shared/methodology-footer.tsx` | nothing |
| 8 | StickyFilterButton | `src/components/shared/sticky-filter-button.tsx` | nothing |
| 9 | ComparisonPage | `src/components/comparisons/[category]-comparison-page.tsx` | all of the above |

---

## Hard Gate

**No ComparisonPage assembly (step 9) before steps 1–3 are finalized and visually approved.**

Steps 4–8 may be built in parallel once steps 1–3 are approved. Step 9 requires all 8.

---

## Per-Component Completion Criteria

A component is **finalized** when:

1. It renders correctly with Hebrew content in `dir="rtl"` context
2. It passes its Section 3 audit table from `frontend_integration_checklist_v1.md`
3. It has been visually inspected at 375px viewport width
4. No forbidden patterns are present (see below)

A component is **visually approved** when it has been reviewed in browser at 375×812px emulation and explicitly confirmed.

---

## Forbidden Patterns — Enforced at Component Level

These conditions cause automatic rejection of any component, regardless of build stage:

| Component | Forbidden |
|---|---|
| ScoreChip | Any `backgroundColor`, `color`, or `borderColor` that varies by grade value |
| ScoreChip | Any label text beside the grade letter ("נמוך", "גבוה", "בינוני", "חזק") |
| ScoreChip | Any container with `rounded-xl border` if border color encodes grade |
| ProductRow | Any `border` between rows (border on the row element itself) |
| ProductRow | Height > 80px collapsed |
| ProductRow | No insight line slot |
| ExpansionSection | Any heading tag (`h2`, `h3`, `h4`) inside expansion |
| ExpansionSection | Any reference to framework terms: NOVA, BSIP, cap, structural_class, matrix_integrity, pillar, dimension |
| ExpansionSection | "מה מעלה/מוריד את הציון" pattern — score attribution is not permitted |
| ExpansionSection | Modal, sheet, or overlay — must expand inline only |
| CategoryHero | Total height > 280px on 375px viewport |
| CategoryHero | More than one sentence in hero text |
| MethodologyFooter | Any `<h2>`, `<h3>`, or bold heading above text |
| MethodologyFooter | Any border, background, or card container |
| MethodologyFooter | Font larger than 12px or color darker than #AAAAAA |
| StickyFilterButton | Visible on initial page load (0px scroll) |
| StickyFilterButton | Any badge or count indicator |
| ComparisonPage | Any of the above present in assembled page |
| ComparisonPage | More than 1 comparison pair |
| ComparisonPage | Any section heading between prologue and first product row |

---

## Token Requirements Per Component

Each component must consume the following tokens from `src/lib/design/bari-comparison-tokens.ts`. If a token is missing from the file at build time, add it before building the component — do not hardcode values inline.

| Component | Required tokens |
|---|---|
| ScoreChip | `score.rowChip` (neutral only — no gradePalette) |
| ProductRow | `rows.oddBg`, `rows.evenBg`, `rows.zebraRowClass`, `rows.zebraContainerClass` |
| ProductRow | `typography.insightLine` (to be added: `font-size: 13px`, `color: #444444`) |
| ProductRow | `layout.rowHeight` (to be added: `72px`), `layout.imageSize` (to be added: `56px`) |
| CategoryHero | `score.hero` (neutral — no gradePalette color application) |
| MethodologyFooter | `typography.methodology` (to be added: `font-size: 12px`, `color: #AAAAAA`) |

---

## Rationale

This sequence exists because:

- ScoreChip is the most constrained component (no color encoding, no label text) and must be finalized before ProductRow consumes it
- ProductRow defines the visual rhythm of the entire page — its height, spacing, and insight line slot cannot be adjusted after ProductTable is built around it
- ExpansionSection inline behavior must be confirmed before page assembly, since a modal fallback is an auto-fail condition
- Steps 5–8 are independent of each other and can be built in parallel, but none of them can ship to the page until the row trio is approved

---

*This sequence governs all future Bari category builds, not only מעדנים. The file paths and component names are canonical.*
