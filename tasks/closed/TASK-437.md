---
id: TASK-437
title: Nutrition rulings: EV-045 juice emulsifier penalty (real D->E driver) + Stage-2 BARI_PROC_CONTINUOUS_V1 activation brief
owner: nutrition-agent
status: CLOSED
closed_at: 2026-07-01
close_reason: Both rulings delivered + orchestrator-verified. OWNER RULED 2026-07-01: EV-045 refine BACKLOGGED (1-product latent defect, no flag built until it goes live); Stage-2 PARKED (dormant scaffold retained on branch p277, full-corpus shadow audit deferred). Nothing activated, nothing deployed. Spec BARI_ECS_TIER_GATED_COMPLEXITY_V1 preserved in the report for future pickup.
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-419, TASK-432]
blocks: []
category_id: null
summary: >
  Two owner-gated rulings, analysis only. (1) Is the flat -4 for 3+ trace emulsifiers correct for juices vs the differentiated CMC/P80 vs lecithin scale? KEEP/REFINE. (2) Stage-2 continuous-processing flag activation D6/D7 decision brief: ACTIVATE/DORMANT/more-shadow. Dispatched to Nutrition Agent.
---

# TASK-437 — Nutrition rulings: EV-045 juice emulsifier penalty (real D->E driver) + Stage-2 BARI_PROC_CONTINUOUS_V1 activation brief

<!-- opened with new_task.py; fill in context / scope / the deliverable -->


## RESOLUTION (2026-07-01, Nutrition Agent ruling — orchestrator-VERIFIED)
Nutrition Agent traced all 29 live juice records (worktree, real engine). Orchestrator independently verified the two load-bearing claims (ECS-v1 commit 117e7021 = 2026-06-10; published run_juices_yohananof_002 traces carry NO emulsifier_complexity_penalty field = predate ECS-v1; `_emulsifier_complexity()` score_engine.py:1845 IS tiered high/med/low). The agent's single grade-mover (7290019056737 grapefruit D->E) independently MATCHES the orchestrator's own per-category census (TASK-436) — strong cross-check.
Report: `03_operations/bsip2/proto_v0/reports/nutrition_ev045_and_stage2_ruling_v1.md` (sha256 e7fe03e8...).

**PREMISE CORRECTED:** EV-045 is NOT the live juice-drop mechanism. The published juice scores predate ECS-v1 entirely; the actual shipped D->E moves were D4/sulphites (build_juices_d4.py explicitly stubbed ECS to 0). EV-045 has never moved a published juice score.

**Ruling 1 — EV-045: REFINE (latent defect, not a live one).** Exactly 1/29 juices would grade-move from ECS-v1 (grapefruit D->E), driven entirely by the count-based complexity surcharge (-3 for 3+ distinct agents), which is agent-identity-BLIND. All 5 firing juice products use only low-tier GRAS thickeners (pectin/gum arabic/guar) — zero CMC/P80/carrageenan. This contradicts Bari's own differentiated emulsifier doctrine (EV-003: CMC/P80 -5 vs gums -1) and EV-045's own risk_of_misuse #3. Specced fix (NOT implemented): new default-off flag `BARI_ECS_TIER_GATED_COMPLEXITY_V1` gating the count surcharge behind ">=1 medium/high agent present"; reverts grapefruit -4->-1 -> D, everything else unchanged. Score-moving on activation -> Product co-sign (D7) + owner gate. Shared function -> full-corpus shadow needed before any flip.

**Ruling 2 — Stage-2 (BARI_PROC_CONTINUOUS_V1): KEEP DORMANT / needs-more-shadow.** Flag-gate verified real + byte-identical off. The plain+additive-light free-pass defect is real & worth fixing, BUT: 700/1119 scores move on a 15%-weight dimension; the NOVA-band clamp means it's proven to MOVE plausibly, not proven better-CALIBRATED; and even uncapped it couldn't flip its own motivating pair. Not a fair owner go/no-go until a fresh full-corpus shadow + per-product audit of every one of the ~51 grade moves exists (the rescore_full_reaudit standard, not a spot check). That audit is the concrete next step, not activation.

**Status -> BLOCKED on owner/Product routing.** EV-045 refine = optional (1-product latent defect); Stage-2 = keep dormant pending shadow audit. Neither activated; nothing deployed.
