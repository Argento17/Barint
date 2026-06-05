---
name: bari_component_build_sequence_v1
description: "Frozen canonical component build order for all Bari comparison pages — 9-step sequence with hard gate at step 3, per-component forbidden patterns, and token requirements"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\component_build_sequence_v1.md`

**Why:** Sequence exists to prevent page assembly before the row trio is visually approved. ScoreChip constraints must be locked before ProductRow consumes it; ProductRow height/spacing must be fixed before ProductTable builds around it.

**Canonical order:**
1. ScoreChip → `src/components/shared/score-chip.tsx`
2. ProductRow → `src/components/shared/product-row.tsx`
3. ExpansionSection → `src/components/shared/expansion-section.tsx`
4. ProductTable → `src/components/shared/product-table.tsx`
5. CategoryHero → `src/components/shared/category-hero.tsx`
6. CategoryPrologue → `src/components/shared/category-prologue.tsx`
7. MethodologyFooter → `src/components/shared/methodology-footer.tsx`
8. StickyFilterButton → `src/components/shared/sticky-filter-button.tsx`
9. ComparisonPage → `src/components/comparisons/[category]-comparison-page.tsx`

**Hard gate:** No step 9 before steps 1–3 are finalized and visually approved. Steps 4–8 may run in parallel after gate passes.

**All new components go in `src/components/shared/`** — not in category-specific folders.

**Key forbidden patterns (per component):**
- ScoreChip: no color by grade, no label text (נמוך/גבוה/בינוני/חזק)
- ProductRow: no row borders, height ≤ 80px, must have insight line slot
- ExpansionSection: no headings, no framework terms, no "מה מעלה/מוריד את הציון", inline only
- CategoryHero: ≤ 280px total, one sentence
- MethodologyFooter: no heading, no card, 12px/#AAAAAA
- StickyFilterButton: invisible at 0px scroll, no count badge

**Related:** [[bari_frontend_integration_v1]] [[bari_comparison_template_v1]]
