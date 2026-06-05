---
name: bari_architecture_generations_v1
description: Architecture generations registry — Gen 0 (deprecated dashboard/exploratory) vs Gen 1 (frozen comparison template); 10 known Gen 0 weaknesses; generation comparison table; usage rule for pattern identification
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\architecture_generations_registry_v1.md`

**Why:** Prevents accidental reuse of Gen 0 patterns during Gen 1 build. When a pattern is proposed, identify its generation first.

**Gen 0 — Exploratory/Dashboard (Deprecated)**
- Files: `bread-comparison-dashboard.tsx`, `snack-comparison-engine.tsx`, `milk-comparison-page.tsx`, `milk-editorial/`, `snack/`
- Key patterns: color-coded score chips, grade label text (נמוך/גבוה), card grid layout, NOVA labels in UI, dimension bars, MatrixIntegrityBadge, score attribution (מה מעלה/מוריד), full-viewport stats hero, 5–7 page sections, collapsible methodology card, snack sheet/modal expansion
- Status: Deprecated — quarantined under Legacy Isolation Policy v1

**Gen 1 — Frozen Comparison Template (Active)**
- First implementation: מעדנים
- Key patterns: neutral score chip (same bg all grades, no label text), 72px row with insight line, sticky FAB filter, inline expansion (nutrition+ingredients only, no framework terms), compact hero (280px, one sentence), plain methodology footer (12px/#AAAAAA), exactly 4 page sections
- Governed by: comparison_template_v1.md + component_build_sequence_v1.md + exception_registry_v1.md

**Usage rule:** If a proposed pattern belongs to Gen 0 → do not use. Document Gen 1 alternative.  
**If generation unclear → treat as Gen 0** until confirmed.

**Gen 0 known weaknesses (top 5):**
1. Score color encoding trains users to read color, not number
2. Grade label text interprets score as verdict
3. NOVA in consumer UI exposes framework without context
4. "מה מעלה/מוריד" is direct ontology leakage
5. Card layout creates analytics-software feel, not shelf investigation

**Related:** [[bari_legacy_isolation_v1]] [[bari_component_build_sequence_v1]] [[bari_comparison_template_v1]]
