---
id: TASK-194
title: "Glass Box D1 — Energy Density signal evaluation (EV-### + D7 gate)"
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-06
closed_at: 2026-06-06
cc_reviewed: 2026-06-06
depends_on: [TASK-179]
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
source_research: "C:\\Bari\\research\\New Batch\\Beyond Nutrients.pdf"
cc_comments:
  - flag: fyi
    note: >
      Close-readiness gate PASS (2026-06-06). Artifacts verified: evidence_registry_v1.md
      contains BEV-082 (DED signal, score_moving_pending_d7); review memo at
      glass_box_d1_energy_density_review_v1.md (≥3 primary citations confirmed);
      D7 brief at glass_box_d1_ded_d7_brief_v1.md ready for owner sign-off. No published
      score changed. Fermentation/intact-grain marked annotate_only. D7 sign-off is the
      owner's next action — not this task's mandate. Task delivered everything it was scoped
      to deliver.
summary: >
  Evaluate Dietary Energy Density (DED <1.5 kcal/g as the evidence-anchored threshold) as
  a new D1 signal. DED is fully label-observable (kcal ÷ serving mass), has robust evidence
  in the Beyond Nutrients doc, and keeps Bari's de-moralized stance (density, not calories).
  This is the cleanest new score-mover candidate in the New Batch research. Touches scoring
  philosophy → D7 review path required before any score rule is activated.
---

# TASK-194 — Glass Box D1 Energy Density Signal Evaluation

## Context

Source: `Beyond Nutrients.pdf` (New Batch research, 2026-06-06). The document cites a robust
evidence base for Dietary Energy Density (DED) as a diet-quality signal distinct from raw
calorie counts — the <1.5 kcal/g threshold is well-anchored in epidemiological literature
and is directly computable from a nutrition panel without any per-person parameters.

This is fully consistent with Bari's existing stance (score the food architecture, not the
eater) because DED describes the food's energy concentration, not the consumer's intake.

**Also in the doc — handle separately:**
- Fermentation / live cultures → hardens EV-024; do NOT broaden to dry "fermented" claims
  (annotation-only, no new signal needed here)
- Intact-grain protein kinetics → annotate-only; evidence too mechanistic for a BSIP2 rule
- UPF classification overlap with NOVA → already governed; no change

## Deliverables

1. **Evidence review memo** — Nutrition documents the DED evidence base (citation quality,
   threshold robustness, cross-category applicability). Target: a 1–2 page structured review
   citing ≥3 primary sources from the research doc + EFSA/WHO literature.
2. **EV-### Evidence Registry entry** — formal entry for DED as a candidate D1 signal:
   evidence tier, proposed threshold (≤1.5 kcal/g = positive, >2.5 kcal/g = penalized),
   category applicability notes, and `score_moving_pending_d7` status flag.
3. **D7 brief** — a concise scoring-philosophy sign-off doc for the owner: what the rule
   would do, which categories it touches, expected score-distribution shift, and the
   single recommended threshold. This is the gate deliverable before activation.

## Acceptance criteria

- [ ] Evidence review memo exists with ≥3 primary citations supporting the <1.5 kcal/g anchor.
- [ ] EV-### entry in the Evidence Registry, flagged `score_moving_pending_d7`.
- [ ] D7 brief drafted and routed to owner for sign-off.
- [ ] No existing published score is changed by this task — evaluation only.
- [ ] Fermentation/intact-grain signals explicitly noted as `annotate_only` (not new rules).

## Governance

- roadmap_impact: true (proposes a new score signal in D1)
- **Score activation requires owner D7 sign-off** (scoring-philosophy tripwire) — this task
  delivers the D7 brief, not the activation
- EDPG firewall: research doc calibrates the evaluation; Nutrition makes the recommendation;
  owner decides
- Cross-category impact: DED affects all food categories differently (snacks vs milk vs bread);
  category impact table required in the D7 brief
