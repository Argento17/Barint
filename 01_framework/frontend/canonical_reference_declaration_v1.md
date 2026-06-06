# Bari Canonical Comparison Reference Declaration — v1

**Status:** Active  
**Date:** 2026-05-28  
**Authority:** This declaration supersedes any prior implicit reference. When a future implementation question references "how Bari does X," the answer is derived from this document and the מעדנים implementation — not from bread, snack, or milk.

---

## Declaration

The מעדנים comparison page is declared the canonical Bari comparison reference.

All future category comparison pages inherit component behavior, visual rhythm, data patterns, and interaction rules from the finalized מעדנים implementation. No future page inherits from `bread-comparison-dashboard.tsx`, any file in `src/components/snack/`, or `milk-comparison-page.tsx`.

---

## What "Inherit From מעדנים" Means

Inheritance is behavioral and structural, not code-copy.

A future category page inherits from מעדנים when:

1. It uses the canonical components from `src/components/shared/` — the same components built for מעדנים, unchanged
2. Its data adapter (`[category]-page-data.ts`) produces props that conform to the same component interfaces defined in the מעדנים build
3. Its page structure follows the 4-section template: CategoryHero → CategoryPrologue → ProductTable → MethodologyFooter
4. Its insight lines follow the T1/T2/T3 spec validated by `validate_insight_lines.py`
5. Its mobile geometry passes `mobile_geometry_checklist_v1.md` using the same pixel targets

A future category page does **not** need to copy מעדנים's editorial content, data shape, or category-specific decisions. Those are category-level concerns. It inherits the components and the interaction rules.

---

## What Future Pages Must Not Inherit

The following patterns exist in bread, snack, or milk. They are Gen 0. Future pages must not reproduce them, regardless of how they appear in the codebase.

| Pattern | Found in | Status |
|---|---|---|
| Saturated / solid-fill grade chip (legacy `gradePalette` treatment) | `bari-grade-badge.tsx`, `snack-score-chip.tsx` | Prohibited — *treatment only.* Grade color via `gradePalette` is canonical (Gen 1.1, 2026-06-03); what is prohibited is the legacy saturated/solid-fill rendering, not grade color itself. The canonical chip uses a subtle tint + accent border/number within the A–E ramp. |
| Free-text grade label beside grade letter | `bari-grade-badge.tsx` | Prohibited — the canonical chip carries only the approved tier word ("72 · B · טוב"), not a free-text interpretive label |
| Dimension bars (`DimensionBars`) | `dimension-bars.tsx` | Prohibited |
| Score attribution ("מה מעלה/מוריד את הציון") | `milk-comparison-page.tsx` | Prohibited |
| `BariInterpretationPanel` with pillar strength labels | `bari-interpretation-panel.tsx` | Prohibited |
| `MatrixIntegrityBadge` | `matrix-integrity-badge.tsx` | Prohibited |
| NOVA label in consumer UI | `product-card-grid.tsx`, `snack-shelf-stat-bar.tsx` | Prohibited |
| Card-grid product layout | `product-card-grid.tsx` | Prohibited |
| Sheet or modal product expansion | `snack-product-detail-panel.tsx` | Prohibited |
| Full-viewport stats hero | `bread-comparison-dashboard.tsx` | Prohibited |
| Collapsible methodology card | `bread-comparison-dashboard.tsx` | Prohibited |
| InsightBlocks section | `bread-comparison-dashboard.tsx` | Prohibited |
| Always-visible inline nutrition panels per row | `milk-comparison-page.tsx` | Prohibited |
| Aggregate statistics bar (NOVA%, score range) | `snack-shelf-stat-bar.tsx` | Prohibited |
| Filter with NOVA or grade dimensions | `filter-panel.tsx` | Prohibited |

If a future implementation proposes any of these patterns, the response is: "this pattern is Gen 0 — see `architecture_generations_registry_v1.md` and the מעדנים implementation for the correct approach."

---

## Shared Component Extraction Rules

Shared components in `src/components/shared/` are extracted from the finalized מעדנים implementation only.

**Finalized** means: the component has been visually approved in the context of a live or staging מעדנים page. A component that exists in code but has not been visually approved is not finalized and cannot be declared canonical.

| Rule | Detail |
|---|---|
| No pre-extraction | A shared component is not extracted speculatively. It is extracted from working, approved מעדנים code. |
| Interface before generalization | The component interface is defined by what מעדנים needs. Generalization for a second category happens when that category is being built — not before. |
| No props added for hypothetical categories | If מעדנים does not need a prop, the prop does not exist in the shared component, even if a future category might need it. |
| No extraction from legacy pages | A component that exists in `milk-comparison-page.tsx` or `bread-comparison-dashboard.tsx` is not extracted into `src/components/shared/` — it is reimplemented from the מעדנים spec. |

When a second category is built, its component needs may differ from מעדנים in some details. Those differences are handled by:

1. Extending the shared component's props with a new optional prop, if the extension does not alter existing behavior
2. Creating a category-level override only if the shared component genuinely cannot accommodate the difference without mutation
3. Filing an exception registry entry if the difference constitutes a template deviation

---

## Deviation Documentation Requirements

A deviation is any future category page behavior that differs from the מעדנים canonical implementation.

**Deviations require a documented justification before implementation.** The justification must answer:

1. What is the specific behavior in מעדנים that this category cannot replicate?
2. Why can't the shared component accommodate the difference through a prop?
3. What is the proposed alternative behavior?
4. Does the alternative violate any condition in `comparison-template-standard-v1.md` or `mobile_geometry_checklist_v1.md`?
5. Is this deviation category-specific (acceptable if justified) or a template change (requires broader review)?

Deviations that do not violate template rules can be approved at the implementation level with a documented rationale in the category's data file or page component.

Deviations that violate template rules require an entry in `exception_registry_v1.md` before implementation.

Deviations that reproduce a Gen 0 pattern are rejected regardless of justification. A Gen 0 pattern is not a "deviation from מעדנים" — it is a regression.

---

## Reference Hierarchy

When any implementation question arises about how to build a Bari comparison page, consult in this order:

| Priority | Document | What it answers |
|---|---|---|
| 1 | This declaration | Which reference to use |
| 2 | מעדנים implementation | How the canonical behavior looks in code |
| 3 | `comparison-template-standard-v1.md` | What the architecture requires |
| 4 | `component_build_sequence_v1.md` | Build order and component completion criteria |
| 5 | `mobile_geometry_checklist_v1.md` | Pixel targets and viewport behavior |
| 6 | `insight_line_spec_v1.md` | Editorial content rules |
| 7 | `exception_registry_v1.md` | Approved deviations |
| 8 | `legacy_isolation_policy_v1.md` | What not to touch |
| 9 | `architecture_generations_registry_v1.md` | Pattern identification |

If a question is not answered by any document in this hierarchy, the answer is: do not build it until it is specified.

---

## Effect on Prior Documents

This declaration does not replace any prior document. It establishes precedence.

| Document | Effect |
|---|---|
| `legacy_isolation_policy_v1.md` | Unchanged — legacy pages remain quarantined |
| `architecture_generations_registry_v1.md` | Unchanged — Gen 0 patterns remain prohibited |
| `component_build_sequence_v1.md` | Unchanged — build order and gate remain in force |
| `exception_registry_v1.md` | Unchanged — EXCEPTION-001 remains the only approved exception |
| `comparison-template-standard-v1.md` | Unchanged — מעדנים implements this template; the template does not change because מעדנים implements it |

---

*This declaration is updated when a new canonical reference is formally designated. A new canonical reference is only designated after the previous one has been live in production and its shared components have been validated across at least one subsequent category build.*
