---
id: TASK-303
title: Light methodology re-confirm of post-data-fix deltas — cereals/granola/hummus (deltas shifted after TASK-300 corrected the source data)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Nutrition re-confirm = CONFIRM-GO for cereals (D->C sound, phantom-ingredient de-contamination) + granola (5/5 moves sound
  on corrected sodium/ingredients). Orchestrator-verified + caught one thing the agent waved through: HUMMUS is NOT clean to
  deploy — post-fix, the shelf's TOP 5 (all 5 A-grades: 7296073733324/733331/005889/006015/705505) are RAW/DRIED CHICKPEAS,
  not prepared hummus dip (real dips start at B/76.8). Scores honest, but shelf mis-curated → HUMMUS HELD ON CURATION (exclude
  the raw-chickpea class -> re-run -> re-gate). Granola tracked note: 7290106773714 fat_g=0.5 implausible (pre-existing BSIP1
  scrape error, not TASK-300) -> separate re-scrape data ticket, non-blocking. Net: cereals+granola CONFIRM-GO; hummus -> held.
depends_on: [TASK-300]
blocks: []
category_id: null
summary: >
  The TASK-300 data corrections shifted the re-baseline deltas on 3 shelves AFTER the TASK-299 review (cereals 0->1 grade move, granola 8->5, hummus now data-clean). Nutrition re-confirms ONLY these 3 shelves' current deltas in _rescore_staging/rebaseline_delta_report.md are methodologically sound on the corrected data + invariants hold. Read-only; gates the clean-set deploy-prep. Other 6 shelves stand as previously reviewed.
---

# TASK-303 — Light methodology re-confirm of post-data-fix deltas — cereals/granola/hummus (deltas shifted after TASK-300 corrected the source data)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
