---
id: TASK-542
title: Live brined-cheeses page carries banned mechanism phrases on 4 rows (caught by new copy gate)
owner: content-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  The new validate_copy_authored.py gate (TASK-541) flagged live copy: brined_cheeses_frontend_v2.json
  carries banned score-mechanism narration (owner ruling 2026-07-08) on 4 rowVerdicts, not 1 — orchestrator
  re-ran the gate 2026-07-09 (exit 1): 7290108509755 'הגורם המגביל', 7296073641964 'מוריד את הציון',
  7290114314015 'מוריד את הציון', 4861360 'מגביל את הציון'. Fix via Content Agent per Hard Rules 9-11,
  two-gate, then the brined page passes the new gate clean. Live-site copy — reversible, no score change,
  but shipping the fix is a consumer-facing deploy (tripwire 2 — owner-gated). QUEUED for supervised
  morning: needs Content authoring + Adversarial-QA gate + owner merge.
---

# TASK-542 — Live brined-cheeses row 7290108509755 carries banned mechanism phrase (caught by new copy gate day-one)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
