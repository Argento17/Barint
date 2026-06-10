---
id: TASK-227
title: Salty Snacks comparison page — standards rebuild
status: CLOSED
owner: Frontend Agent
created: 2026-06-10
closed: 2026-06-10
renumber_note: >
  Originally filed as TASK-222 (untracked, in the live tasks/ dir); renumbered to TASK-227 on
  2026-06-10 to resolve an id collision. TASK-222 was already taken by a tracked governance task
  "BSIP2 Research-to-Implementation Decision Matrix" (2026-06-09, owner orchestrator, anchors the
  TASK-222A–F sub-family) in tasks/closed/. This salty-snacks rebuild is a distinct task that
  wrongly reused 222. The dependent comparison-cleanup task (TASK-226) had its depends_on updated
  from 222→227. The activation commit "Activate TASK-222 salty-snacks copy lock" (aba62523) was
  authored under the pre-renumber id; see commit history. Same root cause as the TASK-223 collision
  (see tasks/_README.md id-allocation rule).
close_reason: >
  All deliverables verified. salty_snacks_frontend_v3.json written with 54 interpretive
  insightLine verdicts (NOVA removed from public text, rowVerdict absent from JSON),
  expansion.positiveSignals/limitingFactors/bottomLine/comparisonContext added.
  salty-snacks-page-data.ts updated: v3 import, insightLine→rowVerdict enricher,
  new hero ("הבמבה מקבל C — חטיף עדשים של קרפור מקבל A."), updated prologue naming
  specific products. Category registered in registry/types.ts, registry/categories/salty-snacks.ts
  created, registry/index.ts updated. Build passes, /hashvaot/salty-snacks in static output.
---

## Scope

Rebuild the Salty Snacks comparison page (`/hashvaot/salty-snacks`) to meet Bari
comparison-page standards v1.

## Deliverables

- [x] `salty_snacks_frontend_v3.json` — 54 products, 2-line interpretive insightLine, no NOVA in public text, no rowVerdict in JSON, expansion enriched (positiveSignals, limitingFactors text, bottomLine, comparisonContext)
- [x] `salty-snacks-page-data.ts` — v3 import, insightLine→rowVerdict enricher, updated hero + prologue
- [x] `registry/types.ts` — "salty-snacks" added to ComparisonCategoryId union
- [x] `registry/categories/salty-snacks.ts` — created
- [x] `registry/index.ts` — salty-snacks registered
- [x] Build passes — /hashvaot/salty-snacks in static output

## Standards compliance

- NOVA not in any insightLine: confirmed (0 matches)
- rowVerdict not in JSON: confirmed
- positiveSignals/limitingFactors/bottomLine present on all 54 products: confirmed
- insightLine is 2-line interpretive verdict (standing→why→catch→grade): confirmed
