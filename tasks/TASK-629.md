---
id: TASK-629
title: Re-score bread/crackers/cheese on corrected engine (apply |delta|<=30 autonomously, surface >30) + keep PD/catalog/comparison aligned
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-614
summary: >
  Owner mandate: score moves <=30 are autonomous, don't defer. Establish the re-enrich->re-score->generate path on the MAIN tree (Codex-worktree can't; C:\Bari hardcoded) for bread/crackers/cheese with the corrected parser (comma TASK-621 + fat). Produce per-product |delta|; APPLY <=30 (write corrected comparison JSON + rebuild PD so all 3 surfaces stay aligned + parity gate green); >30 = defect, STOP+surface. Exclude 7290016967074. Consumer deploy = owner merge.
---

# TASK-629 — Re-score bread/crackers/cheese on corrected engine (apply |delta|<=30 autonomously, surface >30) + keep PD/catalog/comparison aligned

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
