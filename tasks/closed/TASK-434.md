---
id: TASK-434
title: Bread #1 product score is stale vs current engine: REQ-362 Rule2 (added 2026-06-20) reroutes 7290016245325 high-protein tahini bread to snack_bar_granola, -0.8
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: bread
summary: >
  Latent router-version drift surfaced by TASK-433 bread re-derive. Rule 2 (whole_food_fat->snack_bar_granola when protein>=20 & ingredient_count>=15) added 2 days after bread published; would change published 94.8/S to 94.0/S if bread re-scored. NOT crackers-caused, NOT shipped. Nutrition/Product to rule: is routing a high-protein seed bread to snack_bar_granola correct? If yes, bread carries a stale #1 score to correct on next re-score (owner-gated). If no, Rule 2 needs a bread guard.
---

# TASK-434 — Bread #1 product score is stale vs current engine: REQ-362 Rule2 (added 2026-06-20) reroutes 7290016245325 high-protein tahini bread to snack_bar_granola, -0.8

## Ruling (Nutrition Agent, 2026-07-01) — CLOSED by orchestrator

**Verdict: Rule 2 correctly reclassifies; accept the correction. No engine change, no D6/D7 needed.**

- The discriminator is NOT "protein≥20 & ingredients≥15" alone — that's the second gate. The first gate is Stage-1 anchoring: this SKU's name anchors on **טחינה (tahini, conf 0.93) which beats לחם (bread, conf 0.90)**, routing it to `whole_food_fat`; only then does Rule 2 re-lens a 192-kcal engineered multi-ingredient product out of a table built for dense raw tahini. `calorie_density` 90→75, score 94.8→94.0, **grade unchanged (S), still #1 bread**.
- **Blast radius: 1/31 bread products today.** Full corpus trace-scan confirmed. The keto seed bread 7290014321168 (23.7g protein) routes via `hard_anchor:לחם`, `req362_override_trace=null` — never reaches Rule 2. Ordinary high-protein breads are unaffected. Only a bread *named/marketed* primarily as tahini/nut-butter/oil could trip it — a narrow, self-selecting set. No guard needed.
- Rule 2 (REQ-362-R1) was **D6+D7 co-signed** (commit fa80cd47, 2026-06-20) with generic `whole_food_fat` scope — intentional cross-category application, not a bars-only patch bread accidentally fell outside.

**close_reason:** Ruling delivered + verified against code (router_v2.py:908 gate), traces (tahini anchor 0.93 vs bread 0.90), and a full 31-product corpus scan (1/31 affected). This is corpus-staleness (bread published 2 days before the rule existed, never re-scored), not a defect. The 94.0 correction lands whenever bread is next re-scored (owner-gated re-flow; nothing auto-deploys). Footnote-level, non-blocking. Folded into owner digest. No follow-up task required.
