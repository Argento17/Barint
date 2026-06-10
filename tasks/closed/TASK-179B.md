---
id: TASK-179B
title: Glass Box W0 — six-dimension contract + scoring-philosophy reframe
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
close_reason: >
  Six-dimension contract accepted. CC close-readiness gate PASSED (verified against artifact);
  Product co-signed Q1/Q3/Q4 + D-SCO-1; owner ratified Q2 — D5 annotates-only, no standalone grade
  move (DEC-006, 2026-06-04). Foundational spine for Glass Box; doc-only, no score moved, no
  governance rewritten (deltas listed). W1 (D5 transparency + D6 confidence) cleared to build.
depends_on: [TASK-179A]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
cc_comments:
  - flag: fyi
    text: "CC close-readiness gate PASSED 2026-06-04 — contract verified against artifact (01_framework/glass_box/six_dimension_contract_v1.md): all 6 dims specified; D6 gate (unconstrained/demote/withhold→null) defined + mapped to uncertainty ladder; invariants preserved by construction (snk ceiling structurally safe — D6 only demotes/withholds + D4 asymmetric ⇒ no promotion path to A); deltas listed not applied; no code/score/governance rewrite."
  - flag: verify
    text: "Before CLOSE: Product co-sign on Q1–Q4 (D6 aggressiveness · D5 moves-grade-or-annotates · contested-additive ceiling weight · consumer drilldown exposure) + owner confirm D-SCO-1 (10 internal dims roll up into 6 public, not replaced). Dispatched to Product 2026-06-04 (TASK-179C)."
summary: >
  Wave 0 foundation of Glass Box (TASK-179): author the six-dimension contract (D1 nutrition ·
  D2 ingredient evidence · D3 de-moralized processing · D4 additive evidence · D5 transparency ·
  D6 confidence) and the scoring-philosophy reframe (grade = within-shelf ranking over OBSERVABLE
  data, not a health verdict; processing de-moralized to a population-level probabilistic signal).
  Doc only — NO engine code, NO score movement, NO rewriting of existing governance (list deltas).
  The contract must be precise enough that Data/Frontend can later build D5+D6 against it without
  re-deriving philosophy. Nutrition authors; Product co-signs (genuine judgment calls surfaced, not
  decided unilaterally). Proposes RETURNED for CC close-readiness gate → owner. Grounded by TASK-179A
  dossier. Spine for all later waves.
---

# TASK-179B — Glass Box W0: six-dimension contract + philosophy reframe

**Part of:** TASK-179 (Glass Box). **Wave 0 (foundation).** Doc only; no score movement.
Nutrition authors → Product co-sign → CC close-readiness gate → owner. Domain agent proposes RETURNED, never CLOSED.

## Deliverable
`01_framework/glass_box/six_dimension_contract_v1.md` (header `**Task:** TASK-179B`), containing:

1. **Scoring-philosophy reframe** — grade = within-shelf ranking over OBSERVABLE data, not truth/health verdict.
   De-moralize processing: D3 is a population-level probabilistic signal with stated uncertainty, not a moral
   penalty. List the reconciliation deltas against `.claude/scoring.md`, governance v1, and the uncertainty
   ladder — do NOT rewrite those docs in this task.
2. **The six-dimension contract** — per D1–D6: definition · inputs (data/signals) · output range/type ·
   contribution to the headline grade · confidence interaction. Specifically: how D1–D5 compose into one
   decisive grade; how **D6 gates** (demote/withhold — extend `INSUFFICIENT→null`, define thresholds
   conceptually); D5 disclosed-vs-hidden taxonomy penalized on its own axis and feeding D6; D4's 6-tier
   taxonomy → bounded score contribution (functional/neutral ≈ no penalty; contested/confirmed-negative =
   bounded signal), referencing the TASK-179A prototype.
3. **Two surfaces** — consumer (grade + confidence flag + drilldown) vs professional (full six-dim graph);
   the internal/external seam principle.
4. **Invariant-preservation statement** — how the contract preserves frozen invariants (milk run_004,
   snk 70/B ceiling, bread provenance); all behind flags, OFF = byte-identical.
5. **Open questions for Product co-sign** — the genuine judgment calls (e.g. how aggressively D6 demotes;
   whether D5 non-disclosure can move a grade or only annotate; weighting of contested additives).

## Constraints
Doc only. No engine/scoring/frontend code. No published score moves. No governance-doc rewrites (list deltas).
Cite TASK-179A for additive/nutrient grounding. Mark judgment calls for Product — do not decide them solo.
Evidence-registry discipline noted for any future rule (no rule without a source).

## Acceptance
Every dimension has defined inputs + output + grade-contribution + confidence-interaction; D6 gating defined;
two-surface seam explicit; invariant-preservation explicit; Product judgment-calls listed; precise enough to
build D5+D6 against without re-deriving philosophy.
