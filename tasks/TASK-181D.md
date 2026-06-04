---
id: TASK-181D
title: "Glass Box W3 — Data: wire expanded library into D4 detector + regenerate pilot JSONs (annotate-only, OFF byte-identical)"
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-04
blocker: "Waiting on TASK-181B (Nutrition tier assignments + registry). Cannot wire the detector before the expanded library is tiered."
depends_on: [TASK-181B]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
summary: >
  Replace the 24-entry GLASSBOX_W2_ADDITIVES table with the full tiered library from 181B; regenerate d4_additives + explanation_he across the pilot JSONs (hummus / maadanim / bread / veg-spreads). Guardrails: behind BARI_GLASSBOX_W2 flag; OFF = byte-identical (rerun verify_glassbox_w2_off_identical.py); published score / grade / gate / glassBox fields UNMODIFIED (annotate-only — D4 does not enter the grade in W3). QA confirms 0-diff on score fields + Hebrew copy coverage before close.
---

# TASK-181D — Glass Box W3 — Data: wire expanded library into D4 detector + regenerate pilot JSONs (annotate-only, OFF byte-identical)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
