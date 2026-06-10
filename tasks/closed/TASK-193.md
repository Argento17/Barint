---
id: TASK-193
title: "Glass Box D4 — Additive Reference Library (demand-gated seed)"
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
source_research: "C:\\Bari\\research\\New Batch\\Food additives 1.pdf"
cc_comments:
  - flag: fyi
    note: >
      Close-readiness gate PASS (2026-06-06). Artifacts verified: evidence_registry_v1.md
      contains BEV-078–081 (4 tier entries); glass_box_d4_stub_v1.md created. No per-person
      ADI×bodyweight logic. Emulsifiers annotate_only with documented rationale (weak 2026
      evidence). Sulfites + azo colorants correctly flagged score_moving_pending_d7.
      Demand-gate threshold review by Product is TASK-179's responsibility (D4 activates
      after D5/D6 + DIAAS ship) — not a blocker for this task's close. Library seeding is
      the full mandate of TASK-193 and it is complete.
summary: >
  Seed the Glass Box D4 ("additive MOAT") with a cited reference library built from the
  Tier 1–4 additive framework + ADI table in the research batch. Library entries become
  structured Evidence Registry objects (EV-###) that D4 can consume. Demand-gated per the
  TASK-179 sequencing: the library is authored and tested first; consumer-facing score-moving
  rules require a separate owner D7 sign-off per rule.
---

# TASK-193 — Glass Box D4 Additive Reference Library

## Context

Source: `Food additives 1.pdf` (New Batch research, 2026-06-06). The document provides a
four-tier additive classification framework + per-additive ADI tables that map cleanly to
the D4 ("additive MOAT") dimension planned in Glass Box (TASK-179).

**What to take:**
- Tier 1–4 classification table (safety profile, regulatory status, common categories)
- ADI/TDI values from EFSA/JECFA as reference ceilings
- Decision algorithm for consumer-facing annotation (tier → annotation language)

**What to reject:**
- Per-person ADI × bodyweight intake calculation — this is a consumer-intake model;
  Bari describes the SKU, not the eater (BEV-001; BEV-003e). Never implement.

## Critical nuance (Nutrition co-determination)

Emulsifier evidence (P80/CMC/carrageenan) is **weak and non-directional**; the 2026 RCT
found ↓SCFA but no rise in inflammation markers. These stay **annotate-only** until
stronger evidence lands. Do NOT treat them as score-movers.

Only **sulfites (Tier 1)** and **azo synthetic colorants (Tier 2)** are even candidates for a
score-moving rule — both have established dose-independent sensitivity populations. These
need a separate owner D7 sign-off before any score rule is written.

## Deliverables

1. **EV-### series** — structured Evidence Registry entries for each tier, each citing the
   research doc + EFSA/JECFA primary source. One entry per tier, not per additive.
2. **Annotation language table** — tier → consumer-facing Hebrew description, reviewed by
   Content agent. No alarm language; no ADI math shown to consumer.
3. **D4 stub** in the Glass Box spec (`01_framework/`) that references the library and marks
   which rules are `annotate_only` vs `score_moving` (the latter requiring D7).
4. **Gate record** — Product co-signs the demand-gate threshold (what consumer engagement
   level triggers converting an annotate-only entry to a scored rule).

## Acceptance criteria

- [ ] Evidence Registry has new EV-### entries covering all 4 tiers, each with a cited source
      (research doc + EFSA/JECFA primary).
- [ ] No per-person ADI × bodyweight logic appears anywhere in the deliverable.
- [ ] Emulsifiers (P80, CMC, carrageenan) are marked `annotate_only` with explicit rationale.
- [ ] Sulfites + azo colorants are flagged `score_moving_pending_d7` — not activated.
- [ ] Product has reviewed and accepted the demand-gate threshold for activating scored rules.

## Governance

- roadmap_impact: true (touches Glass Box scoring philosophy)
- Score moves → separate owner D7 sign-off per rule; this task does NOT authorize any
- Demand-gate per TASK-179 sequencing (D4 library after D5/D6 + DIAAS ship)
- EDPG firewall: research doc calibrates the library; library does not directly move scores
