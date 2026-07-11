---
id: TASK-623
title: PD<->catalog<->comparison alignment: audit current agreement + build parity gate (always-aligned spine)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
summary: >
  Owner rule: PD must ALWAYS align with product catalog + comparison pages. Audit current agreement (PD publication_record score/grade/identity vs *_frontend_v*.json vs catalog) across all 687; build a parity gate (extend TASK-588 registry-parity pattern) that FAILS if the 3 surfaces diverge on score/grade/identity; wire to CI. Foundation for the re-score program.
---

# TASK-623 — PD<->catalog<->comparison alignment: audit current agreement + build parity gate (always-aligned spine)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
