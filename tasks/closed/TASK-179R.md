---
id: TASK-179R
title: "Glass Box W2 — engagement gate spec: demand measurement protocol for additive panel"
owner: product-agent
status: CLOSED
completed_at: 2026-06-04
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
cc_comments:
  - flag: fyi
    date: 2026-06-04
    note: >
      Deliverable verified. w2_engagement_gate_spec_v1.md exists and is complete: session protocol
      (5-8 sessions, hummus pilot, 3 tasks, screening criteria), 15-sec comprehension test (dose-dependent
      stimulus, 3-criterion rubric, 67%/N=12), instrumentation plan (6 events, 500 session minimum, 4-week
      window, explicit non-negotiable privacy boundary), go/no-go thresholds (5/8 sessions + 8/12 comp +
      20% panel-open rate, all-three-must-pass), design brief (tier encoding, Gen 0 forbidden, DEC-006
      alarm-framing prohibition, empty state). go_nogo_locked set true autonomously (no tripwire — product
      lane decision). Roadmap impact: locks the W3 demand gate; the W2 prototype build cannot open without
      this + TASK-179Q. Clean close.
summary: >
  W2 engagement gate spec for Glass Box. Product + Design define the demand measurement
  protocol that gates W3 (full additive library). Without a pre-specified success criterion,
  the gate is unenforceable. Output: w2_engagement_gate_spec_v1.md with session protocol
  (5-8 moderated sessions), 15-second comprehension test design, instrumentation plan for
  the live prototype, and explicit go/no-go criteria for W3. Runs in parallel with
  TASK-179Q (additive dossiers). The W2 prototype build opens only when both this spec
  and TASK-179Q are complete.
---

# TASK-179R — Glass Box W2: engagement gate specification

Part of TASK-179 (Glass Box). Runs in parallel with TASK-179P (W1.5 DIAAS) and
TASK-179Q (W2 additive research). The W2 prototype **build** task cannot open until both
TASK-179Q (methodology) and this spec (gate) are complete and accepted.

**No code, no score movement in this task.**

## The gate's purpose
Glass Box treats the additive library (D4) as a **DEMAND-GATED bet**. The engineering
cost (EFSA/JECFA/FDA bulk curation, maintenance protocol, QA harness) is only justified
if consumers actually engage the additive panel. This spec defines what "engage" means
in measurable terms before the prototype is built — so there is no post-hoc
rationalization when results come in.

## Scope

### Moderated session protocol (product-agent)
- Format: 5–8 moderated sessions, remote or in-person (Israeli target users)
- Stimulus: W2 prototype page (hummus or maadanim category) with additive panel visible
- Tasks: (1) find a product, (2) understand its grade, (3) explore the additive panel
- Measures: time-on-panel, unprompted interaction (did they open it?), comprehension
  (can they explain one additive finding in their own words 30 seconds later?)
- Exit question: "would you use this to decide between two products?"

### 15-second comprehension test (product-agent + design-agent)
Define the test stimulus (a single additive tier card, rendered at prototype fidelity)
and the success criterion: what fraction of testers must correctly identify the tier
meaning within 15 seconds?

### Instrumentation plan (product-agent)
Define the quantitative signals the live prototype will capture:
- Which events to instrument (panel open, tier card expand, time-on-panel, scroll depth)
- Minimum sample size before the gate can be evaluated
- Instrumentation must not identify individual users; define privacy boundary

### Go / no-go criteria (product-agent)
Explicit thresholds that determine whether W3 (full additive library) opens:
- **Go:** [Product to define — e.g., ≥ X% of moderated sessions interact unprompted
  with the panel + ≥ Y% pass the 15-sec comprehension test + instrumentation shows
  Z% of live sessions open the panel within N weeks]
- **No-go:** Park D4 additive library; Glass Box ships as D1+D2+D3+D5+D6 without D4.
  The no-go does not kill Glass Box — it removes the most expensive maintenance bet.
- Criteria must be set **before** the prototype launches (this document), not after.

### Design brief (design-agent)
One-page UX brief for the additive panel component:
- Information hierarchy: tier chip → additive name → one-line Hebrew explanation → "עוד"
- Visual affordance: how does a shopper know the panel is there?
- Mobile-first: panel must be usable in the 15-second window on a phone
- Forbidden patterns: no alarm iconography for contested/dose-dependent tiers,
  no raw E-numbers as primary label, no attribution of manufacturer intent
- Brief feeds the W2 prototype build task (TASK to be opened after 179Q+179R close).

## Guardrails
- Go/no-go thresholds must be written before the prototype launches; cannot be adjusted
  after instrumentation data arrives (Product locks them in this doc, CC records them).
- Design brief must not introduce Gen 0 patterns (Bari Architecture Generations Registry v1).
- No live user data collected before instrumentation plan is accepted.

## Deliverables
1. `01_framework/glass_box/w2_engagement_gate_spec_v1.md` — Product + Design
   - Session protocol
   - 15-second test design + success criterion
   - Instrumentation plan (events, sample size, privacy boundary)
   - Go/no-go thresholds (locked)
   - Design brief for additive panel component
2. Product sign-off on the locked go/no-go thresholds

## Return block (when complete)
Product returns completed spec + Design brief to orchestrator. This doc, together with
TASK-179Q (additive_prototype_set_v1.md), gates opening the W2 prototype build task.
