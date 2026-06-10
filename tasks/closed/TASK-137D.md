---
id: TASK-137D
title: "Data: implement 'סלט' exclusions per Nutrition ruling + wire rowVerdict through the corpus/builder, re-derive counts, sync to bari-web"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Not necessary"
depends_on: [TASK-137A, TASK-137B, TASK-137C]
blocks: [TASK-137E]
category_id: hummus
summary: >
  Apply Nutrition's exclude/keep ruling for the 'סלט' items (audit record like excluded_products_hummus_v1.md; re-derive product count + grade tally + the 37/A-count hero stats and prologue counts). Add the authored rowVerdict to hummus_frontend_v3.json via the builder and sync the copy into bari-web/src/data/comparisons/.
---

# TASK-137D — Data: implement 'סלט' exclusions per Nutrition ruling + wire rowVerdict through the corpus/builder, re-derive counts, sync to bari-web

## Scope (updated 2026-06-01)
Boundary fix DONE in `hummus-comparison-page-data.ts` (`EXCLUDED_RAW_CHICKPEA_IDS` =
`bsip1_1990261`, `bsip1_3643714` — raw/dry chickpeas; 37→35 displayed, grade-A unchanged at 1).
Counts auto-derive — no hardcoded edits. Prepared tahini-based salads/spreads (incl. סלט חומוס)
kept per Product ruling. Remaining 137D scope: **wire the authored `rowVerdict` through the
builder → `hummus_frontend_v3.json` → sync into `bari-web/src/data/comparisons/`**, then QA
re-baseline (the exclusion drops 2 rows the mobile+lg snapshots must be refreshed for).
