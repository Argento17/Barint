---
name: bari_canonical_reference_v1
description: "מעדנים declared canonical comparison reference — all future pages inherit from it, not from bread/snack/milk; shared component extraction rules; deviation documentation requirements; 9-level reference hierarchy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\canonical_reference_declaration_v1.md`

**Why:** Establishes a single authoritative reference so future implementers have a clear answer to "how does Bari do X?" — not a choice between bread, milk, snack, and spec docs.

**The declaration:** מעדנים comparison page is the canonical Bari comparison reference. All future pages inherit from it. No future page inherits from bread-comparison-dashboard, snack/*, or milk-comparison-page.

**Inheritance means:** using shared components from src/components/shared/, conforming to those component interfaces, following 4-section structure, passing the geometry checklist with the same pixel targets.

**14 prohibited Gen 0 patterns** — explicitly listed in the declaration (color chip, grade label text, dimension bars, score attribution, NOVA labels, card grid, sheet expansion, stats hero, collapsible methodology, insight blocks, inline nutrition panels, stats bar, NOVA filter).

**Shared component extraction rules:**
- Extract only from finalized (visually approved) מעדנים code — not speculatively
- Interface defined by what מעדנים needs — no hypothetical props
- Never extract from legacy pages — reimplement from spec

**Deviation requirements:** 5 questions must be answered before any deviation is implemented. Gen 0 pattern as "deviation" = rejected always.

**Reference hierarchy (9 levels):**
1. This declaration
2. מעדנים implementation (code)
3. comparison_template_v1.md
4. component_build_sequence_v1.md
5. mobile_geometry_checklist_v1.md
6. insight_line_spec_v1.md
7. exception_registry_v1.md
8. legacy_isolation_policy_v1.md
9. architecture_generations_registry_v1.md

If not covered by any → do not build until specified.

**Related:** [[bari_legacy_isolation_v1]] [[bari_architecture_generations_v1]] [[bari_component_build_sequence_v1]] [[bari_comparison_template_v1]]
