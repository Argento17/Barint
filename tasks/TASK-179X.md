---
id: TASK-179X
title: "Glass Box W2 — engagement gate: run moderated sessions"
owner: product-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179R, TASK-179V]
blocks: []
category_id: null
roadmap_impact: true
work_type: research
summary: >
  Critical path to W3. Recruit 5–8 Israeli users and run moderated sessions per
  w2_engagement_gate_spec_v1.md §1–3. Deliverable: session recordings + scored results
  against 3 thresholds (5/8 unprompted opens + 8/12 comprehension + 20% live panel-open
  rate). Without this result, W3 is indefinitely blocked.
---

# TASK-179X — Glass Box W2: engagement gate — run moderated sessions

Part of TASK-179 (Glass Box), Wave 2 gate. **This is the critical path to W3.**

## Prerequisites (both CLOSED)

- `TASK-179R` (CLOSED 2026-06-04) — `w2_engagement_gate_spec_v1.md` with the 3 thresholds
  and go/no-go criteria. `go_nogo_locked = true`.
- `TASK-179V` (CLOSED 2026-06-04) — W2 QA pass. Prototype is live on hummus + maadanim pages.

## What to do

Run the engagement gate as specified in `01_framework/glass_box/w2_engagement_gate_spec_v1.md`.

**Recruit:** 5–8 Israeli users (target: mobile, ages 25–45, self-described health-curious
food buyers; see spec §1 for screener criteria).

**Sessions:** Moderated, per spec §2:
- Show the live comparison page (hummus or maadanim) on mobile.
- Do not prompt the user to find the additive panel.
- Record screen + audio.
- Ask the 3 comprehension questions from spec §3 after the session.

**Scoring:** Against the 3 thresholds from spec §3.2:
1. **Unprompted opens:** ≥5 of 8 users open the additive panel without being told to.
2. **Comprehension:** ≥8 of 12 question-responses answered correctly.
3. **Live rate (instrumentation):** ≥20% panel-open rate across live sessions (see spec §3.3
   — minimum 500 sessions for statistical confidence; moderated sessions count separately
   from the live-traffic gate; see spec for clarification on threshold interaction).

**Co-owner:** Research Agent assists with recruiting, screener, and session facilitation.
Product owns go/no-go call and final gate verdict.

## Gate outcome

- **PASS (all 3 thresholds met):** Product records gate = PASS in this task's return block.
  W3 is unblocked — CC opens W3 sub-tasks per the Glass Box roadmap.
- **FAIL (any threshold missed):** Product records gate = FAIL with specific threshold data.
  W3 remains blocked. Product and Nutrition review the failure and propose a W2.1 iteration
  (per spec §4 remediation protocol) before re-running the gate.
- **Partial data (fewer than 5 sessions complete):** Record partial result only — do NOT
  extrapolate. State which thresholds are inconclusive.

## Guardrails

- Do NOT open W3 tasks until gate PASS is recorded and CC verifies.
- Do NOT modify the gate thresholds — `go_nogo_locked = true` (TASK-179R).
- Frozen invariants (milk/snack/bread scores) are not in scope of this research task.
- No PII in session notes delivered to the registry.

## Deliverable

1. Session log summary: N sessions completed, date range, user profile summary (no PII).
2. Threshold scoring table: threshold / target / result for each of the 3 criteria.
3. Gate verdict: PASS or FAIL, with explicit per-threshold results.
4. If FAIL: specific threshold delta and proposed remediation (which W2 element to iterate).

## Return block

Product returns with the gate verdict (PASS/FAIL), threshold table, and session log summary.
If PASS: explicitly state "Gate PASS — W3 is unblocked."
CC closes this task and updates TASK-179 umbrella status only after verifying gate verdict
is complete and evidenced.
