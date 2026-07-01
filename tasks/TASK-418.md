---
id: TASK-418
title: Repro repair: granola + hard_cheeses baselines don't reproduce (blocks de-chain activation)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  De-chain activation eval (2026-07-01) found granola (2 products off +16/+20 vs committed) and hard_cheeses (matched=0 + conformance path bug 'C:\Bariari-web' + granola manifest still points v1 not v2) do NOT cleanly reproduce their published scores. Score-NEUTRAL repair (patch to committed-trace like TASK-409; fix conformance path concat; repoint granola live_manifest v1->v2). No new score move. Precondition for any future de-chain activation.
---

# TASK-418 — Repro repair: granola + hard_cheeses baselines don't reproduce (blocks de-chain activation)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
