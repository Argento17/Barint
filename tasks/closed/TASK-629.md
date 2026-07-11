---
id: TASK-629
title: Re-score bread/crackers/cheese on corrected engine (apply |delta|<=30 autonomously, surface >30) + keep PD/catalog/comparison aligned
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-614
lesson_trigger: none
close_reason: "VERIFIED + committed 8bfe41bb. Re-score bread/crackers/cheese, |delta|<=30 (max 24, 0 defects>30), applied autonomously per owner mandate. Semantic by-barcode diff CLEAN (score/grade/nutrition/confidence only; copy->PENDING_COPY x10, 0 fabricated; ingredients+excluded untouched); parity diverge=0. Caught+fixed a 2nd comma path (task616_type_b, crackers 7290018790328) + a false superlative. FOLLOW-UPS: TASK-630 wires the new traces (calc currently fails, trace-wiring gap not bad scores); 10 PENDING_COPY need Content Agent+two-gate; task616_type_b needs corpus-wide comma audit; consumer deploy=owner merge."
summary: >
  Owner mandate: score moves <=30 are autonomous, don't defer. Establish the re-enrich->re-score->generate path on the MAIN tree (Codex-worktree can't; C:\Bari hardcoded) for bread/crackers/cheese with the corrected parser (comma TASK-621 + fat). Produce per-product |delta|; APPLY <=30 (write corrected comparison JSON + rebuild PD so all 3 surfaces stay aligned + parity gate green); >30 = defect, STOP+surface. Exclude 7290016967074. Consumer deploy = owner merge.
---

# TASK-629 — Re-score bread/crackers/cheese on corrected engine (apply |delta|<=30 autonomously, surface >30) + keep PD/catalog/comparison aligned

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
