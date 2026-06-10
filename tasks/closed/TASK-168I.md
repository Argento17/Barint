---
id: TASK-168I
title: Rollout verdicts — yogurts + snacks + bread
owner: content-agent
status: CLOSED
priority: HIGH
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "53 verdicts rewritten to v2 model across yogurts(11)/snacks(18)/bread(24), insightLine-only (QA pass each). Grounding held: snacks cite ZERO invented panel numbers (only trace figures), yogurts cite no sugar where null + ceiling B, bread no energy/sugar/fat + מחמצת only where signal asserts. Nutrition: 1 bread contradiction (shufersal_3268429 verdict affirmed whole-grain vs its own refined-base signals) — CC reworded the verdict to lead on undisputed protein/fiber/A standing without claiming the base; the deeper expansion contradiction (bottomLine/limitingFactors) remains tied to OPEN TASK-164 (human grade/signal decision). Live + tsc clean."
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
summary: >
  Rewrite insightLine to verdict model in yogurts_frontend_v2 (§4, ceiling B), snacks_frontend_v2 (§6, ALL nutrition null - only trace ingredient figures, ceiling B), bread_frontend_v2 (§5, no energy/sugar/fat, sourdough only where signal asserts). Routed via rowVerdict.
---

# TASK-168I — Rollout verdicts — yogurts + snacks + bread

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
