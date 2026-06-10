---
id: TASK-179E
title: Glass Box W1 — Product co-sign on D5/D6 binding numbers
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179D]
blocks: []
category_id: null
roadmap_impact: true
work_type: decision
close_reason: >
  Product D7 co-sign delivered + verified (01_framework/glass_box/w1_product_cosign_numbers_v1.md).
  All four numbers CO-SIGNED (DEMOTE=60 verified a no-op bound vs score_engine.py L143–154; NULL_FLOOR=30
  AND-severe; −10/−20; structural-only=0). No owner ratification needed (posture already ratified, numbers
  near-no-op). Key nuance: flag-ON is NOT byte-identical overall — the −10/−20 reduction + panel-absent→null
  flip move borderline products DOWN only (never promotion); Data/QA must prove this via the flag-ON pilot
  diff (separate D10 go-live gate, does not block this co-sign). EV-035…039 append AUTHORIZED conditional on:
  (1) Nutrition co-sign logged first + EV-038 wording fix + flip DRAFT→adopted-behind-flag (→ TASK-179F);
  (2) entries adopted-behind-flag (BARI_GLASSBOX_D5D6 OFF), revisitable after pilot. Decision only; no code.
summary: >
  Product D7 co-sign on the four binding numbers proposed in the D5/D6 rule spec (TASK-179D §2.3/§6):
  DEMOTE_CEILING_BOUND=60 (no-op on live behavior by design), NULL_FLOOR=30 gated on AND severe D5-band,
  and the D5→D6 confidence reductions (partial −10 / severe −20). Confirm they faithfully implement the
  already-owner-ratified Q1 posture (conservative-to-demote, reluctant-to-withhold; DEC-006) — owner
  re-ratification NOT expected since these numbers are near-no-op on live and implement a ratified posture;
  escalate only if Product judges a number changes the grade's meaning. On co-sign, authorize appending
  the controlling entries EV-035…039 to the live evidence registry, after which Data builds behind
  BARI_GLASSBOX_D5D6 (OFF = byte-identical). Decision deliverable; no code, no score movement.
---

# TASK-179E — Product co-sign: D5/D6 binding numbers

**Part of:** TASK-179 (Glass Box), Wave 1. **Gates:** Data build (179F). Spec = TASK-179D
(`01_framework/glass_box/d5_d6_rule_spec_v1.md` §2.3, §6). Rulings basis = DEC-006 (Q1/Q2).
Domain agent proposes RETURNED. On co-sign, EV-035…039 may be appended to the live registry.
