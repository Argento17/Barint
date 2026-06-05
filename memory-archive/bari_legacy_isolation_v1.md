---
name: bari_legacy_isolation_v1
description: "Legacy isolation policy — quarantines milk/bread/snack pages from canonical v1 build; defines additive vs destructive changes, migration eligibility (5 criteria), leave-as-is rules, canonical precedence table"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\legacy_isolation_policy_v1.md`

**Why:** Canonical component build (מעדנים) must not trigger refactors of live legacy pages. Legacy pages are quarantined.

**Legacy pages (leave as-is):**
- `milk-comparison-page.tsx` + `milk-editorial/` directory
- `bread-comparison-dashboard.tsx`
- `src/components/snack/` entire directory
- `bari-grade-badge.tsx`, `dimension-bars.tsx`, `bari-interpretation-panel.tsx`, `matrix-integrity-badge.tsx`

**Additive = permitted:** new exports, data content updates, crash fixes  
**Destructive = prohibited without migration approval:** replacing components, removing framework-term UI, altering types, changing behavior

**Token file rule:** `gradePalette` stays in `bari-comparison-tokens.ts` for legacy compatibility. Canonical components must not consume it.

**Migration eligibility (all 5 required):**
1. At least one canonical category in production
2. Canonical data shape stable through one content update cycle
3. No active editorial updates scheduled in next 2 weeks
4. Migration scope bounded to component swap only (no routing/data/URL changes)
5. Explicit approval

**Canonical precedence:** When canonical and legacy differ, canonical is always correct — regardless of build order or user count.

**Scope creep list (all prohibited during מעדנים build):** refactoring legacy files, updating bari-grade-badge, moving snack to shared/, removing DimensionBars/InterpretationPanel, deprecation comments, renaming legacy files, changing milk/bread types.

**Two trees that do not cross:** `src/components/shared/` (canonical) never imports from legacy; legacy never imports from canonical.

**Related:** [[bari_component_build_sequence_v1]] [[bari_frontend_integration_v1]]
