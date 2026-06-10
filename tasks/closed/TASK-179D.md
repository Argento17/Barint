---
id: TASK-179D
title: Glass Box W1 — D5/D6 rule spec + evidence entries (Nutrition)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179B]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  D5/D6 rule spec delivered + verified against the artifact (488-line spec) and the live code. CC gate
  PASSED. Honors DEC-006 (Q2 D5 profile-only — feeds D6 + annotates, never docks the grade; Q1
  conservative — demote band is a no-op on live behavior, null floor is AND-gated on thin+severe).
  Caught + corrected a stale contract constant (live CONFIDENCE_LOW_CEILING=75, contract said 70 —
  contract fixed). Five panel-reality guards encoded (nutrition-table bleed truncation, Hebrew
  normalization per EV-029, endemic-flavoring exclusion EV-036 [prevents ~70% maadanim mis-demote],
  single-ingredient protection, G5 double-count prohibition). Proposed binding numbers (DEMOTE=60,
  NULL_FLOOR=30 AND severe, D5 −10/−20) + draft EV-035…039 carried to Product D7 co-sign (TASK-179E)
  before Data builds. Spec + draft EV only; no code; no score moved.
cc_comments:
  - flag: verify
    text: "Data: build against LIVE constants (CONFIDENCE_LOW_CEILING=75, CONFIDENCE_INSUFFICIENT_CEILING=50), not any doc number. The contract's stale '70' was corrected 2026-06-04."
  - flag: verify
    text: "Data: G5 must NOT double-count — D5 names missing legacy fields for the profile but adds NO new deduction for the six fields compute_confidence already handles; only new sat-fat/sugar red-label omissions feed the D5-band, once (spec §1.2 G5 / §2.1)."
summary: >
  Wave 1 step 1: Nutrition authors the precise D5 (transparency) + D6 (confidence) rule spec against
  the six-dimension contract (TASK-179B) + DEC-006 rulings, with draft evidence-registry entries.
  D5 = disclosure-gap taxonomy + detector spec over the raw BSIP0 panel, scored on its OWN axis but
  (per DEC-006/Q2) NEVER moving the grade — it feeds D6 + annotates. D6 = extend confidence_framework
  with D5 as an input + add the gate state machine (unconstrained · demote · withhold→null), extending
  today's INSUFFICIENT cap-50; PROPOSE the binding Q1 numbers (null-vs-cap + demote band, conservative-
  to-demote/reluctant-to-withhold) for Product D7 co-sign. Spec + draft EV-### only — NO engine code
  (Data implements in 179E), NO score movement (flag OFF = byte-identical). Pilot sanity-check on
  hummus + maadanim. Surfaces the one Product co-sign item before Data builds.
---

# TASK-179D — Glass Box W1: D5/D6 rule spec (Nutrition)

**Part of:** TASK-179 (Glass Box), Wave 1. **Chain:** 179D (this, rule spec) → Product co-sign on the
binding Q1 numbers → 179E (Data: implement behind flag, OFF=byte-identical) → 179F (Frontend: surface
flag + confidence state) → 179G (QA: byte-identity + invariant re-verify). Domain agent proposes RETURNED.

Builds against `01_framework/glass_box/six_dimension_contract_v1.md` (§D5, §D6, §2.6, §5.0 RESOLUTIONS)
and DEC-006. Deliverable: `01_framework/glass_box/d5_d6_rule_spec_v1.md` (header `**Task:** TASK-179D`).
Spec + draft EV entries only; no code; no score movement; respect DEC-006 exactly (esp. Q2 = D5 annotates,
never docks the grade). Surface the Q1 binding threshold as the single Product co-sign item.
