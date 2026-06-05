---
name: bari-view-model-v1
description: Bari Comparison View Model v1 — deterministic contract between BSIP backend and frontend UI; TypeScript interfaces at src/lib/view-models/index.ts; spec at 01_framework/comparison_view_model_v1.md
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

The View Model layer was established as the canonical interface between BSIP scoring outputs and the Bari frontend UI.

**Why:** After v0 prototype review, the architecture gap was identified: backend sophistication (BSIP routing, ontology, scoring internals) was bleeding into the frontend. The VM is the compression point where all interpretation terminates.

**Core rule:** UI components import from `@/lib/view-models` only. Never from `@/lib/comparisons/` or any scoring module.

**Key design decisions:**
- `confidence_level: "full"` → `confidence: "verified"` at the VM boundary (language shift)
- `nutrition` and `ingredients_he` moved from root product into `expansion` sub-object
- Field naming: snake_case → camelCase; `_he` suffix removed; `_g`/`_mg` unit suffixes removed (units are UI constants, not data)
- `expansion` is always present on BariProductVM; content fields inside are nullable
- `score` is always a pre-rounded integer from the backend; UI never rounds
- Products arrive pre-ordered (scored desc, insufficient last); UI never sorts
- `averageScore` is null if < 3 scored products; `topProduct` is null if best score < 60

**TypeScript interfaces:** `src/lib/view-models/index.ts`

**Spec document:** `C:\Bari\01_framework\frontend\comparison_view_model_v1.md`

**How to apply:** All new UI components must receive BariProductVM or BariCategoryPageVM. Existing components (score-chip, product-row, expansion-section) use the legacy ComparisonProduct type and must be migrated to BariProductVM before full page assembly (step 9 of build sequence).
