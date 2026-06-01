---
id: TASK-075
title: Hummus content count reconciliation (resolve QA warning W-1)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on:
  - TASK-072
blocks: []
category_id: hummus
summary: >
  Reconciled hummus content counts after the TASK-069 NOVA-1 exclusion (69→63
  displayed, 67→61 scored). Corrected 8 stale fields from v2 into
  hummus_content_v3.json. Resolves QA warning W-1 from TASK-072.
  Deliverable: hummus_content_count_reconciliation.md.
---

# TASK-075 — Hummus Content Count Reconciliation

Backfilled into the registry per the Command Center v3 migration (TASK-084). The
work was complete (`hummus_content_count_reconciliation.md`: "W-1 is resolved in
hummus_content_v3.json") but had no registry record, so the v2 dashboard kept
showing TASK-073 as the Next Action. v3 detected this as a PHANTOM_TASK.
