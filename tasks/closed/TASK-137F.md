---
id: TASK-137F
title: Standardize maadanim to the hummus reference (verdict-first rows, why-metric prologue, kill hero+insight boxes)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: []
category_id: maadanim
summary: >
  Apply the validated hummus reference pattern to the maadanim comparison page: Nutrition picks the headline row metric + rationale; Content rewrites the prologue (what/how/why-metric) and authors a 2-3 sentence rowVerdict per displayed product grounded in the current (post-TASK-136, engine 0.4.0) traces; Frontend sets showHeroCard=false + showInsights=false and injects verdicts into maadanim_frontend_v2.json (already on v2 row infra); QA gate. Scores are NOT touched (TASK-136 owns the rescore).
---

# TASK-137F — Standardize maadanim to the hummus reference (verdict-first rows, why-metric prologue, kill hero+insight boxes)

## Done (2026-06-01) — maadanim now matches the hummus reference
- **Nutrition:** headline metric = **protein** (present 87/87; sugar only 29/87 and unreliable —
  same logic as hummus fat). Rationale + guardrail: `02_products/maadanim/maadanim_metric_137F.md`.
- **Content:** prologue rewritten (what / how / why-protein + guardrail + sugar caveat) in
  `maadanim-page-data.ts`. **87 rowVerdicts authored** (2–3 sentences, grounded in each current
  trace), injected into `maadanim_frontend_v2.json` (coverage-checked 87/87).
- **Frontend:** `showHeroCard={false}` (kills the hero card that duplicated the /hashvaot featured
  card; lightweight H1 instead) + `showInsights={false}`; full prologue now passed (sentence[0] no
  longer dropped). Typecheck green.
- **No score changes** — 87 products, grades 1B/19C/55D/12E, GO 70/B, מילקי 40/D all intact
  (TASK-136 owns scores).

## Follow-up fixes (Product review 2026-06-01)
- **Category-boundary sweep:** removed 11 off-category items → **87 → 76 displayed** (counts auto-derive;
  card + metadata line updated). Excluded: eggplant spread (חצילים), 2 non-dairy fruit preserves
  (משמש, תפוז), 2 non-dairy jellies (ג'לי פטל, לימבו פטל), 6 instant-pudding **powders**.
  `EXCLUDED_MAADANIM_IDS` in `maadanim-page-data.ts`. Scores untouched.
- **GO factual fix:** `יופלה GO מועשר בחלבון` has **no added sugar** (ingredients = milk/milk-protein/
  milk-powder; sugar=None). Removed the false "מתוק" framing from the verdict + limiting factor; verdict
  now reconciles **10 g/100 g (20 g per 200 g cup)**.
- **Protein metric:** label now **"חלבון ל-100ג׳"** (per-100g basis explicit) so it isn't misread as the
  package's per-cup figure. Shared component → also clarifies hummus.

## Open (Product decisions — not actioned unilaterally)
- **GO = 70/B challenge:** it's the cleanest product on the shelf yet capped at B. Score is a **frozen
  launch invariant** (TASK-136) — needs a governed Nutrition/Product rescore to change, not an edit here.
- **Protein basis:** kept per-100g (comparability). If Product wants per-serving or both, that's a
  systemic metric change across all categories.

## Pending
Design sign-off on row density; QA gate (mobile + lg baselines) — folded into 137E.
