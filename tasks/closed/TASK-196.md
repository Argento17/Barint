---
id: TASK-196
title: "Evidence-Grading Tool — structured per-study registry objects (GRADE-style)"
owner: research-agent
status: CLOSED
closed_at: 2026-06-06
priority: LOW
created_at: 2026-06-06
depends_on: []
blocks: []
category_id: null
roadmap_impact: false
work_type: objective
source_research: "C:\\Bari\\research\\New Batch\\Bari Prioritized Research Program.pdf"
summary: >
  Build a lightweight evidence-grading tool that formalizes how studies enter the Bari
  Evidence Registry. Output is a structured per-study object (claim type, dose realism,
  population directness, risk-of-bias grade, overall A–D evidence tier) rather than a
  free-text note. Research leads; Nutrition defines the grading logic. Tooling only —
  no scoring system, no new dimensions, no score movements.
---

# TASK-196 — Evidence-Grading Tool

## Context

Source: `Bari Prioritized Research Program.pdf` (New Batch research, 2026-06-06). The
document proposes a GRADE-style evidence-grading layer. The valuable take is narrow:
a **structured per-study object** for the Evidence Registry so that every study backing
a scoring signal has a machine-readable quality record.

**What is adopted:**
- The structured object schema (claim, dose realism, population directness, risk-of-bias,
  overall tier A–D) — formalized as a Python dataclass or JSON schema
- The grading vocabulary (RoB2/ROBINS-I aligned conceptually; not requiring formal tools)

**What is explicitly rejected:**
- The 4-stream "platform reframe" — that's a strategic proposal for the owner, not tooling
- The "Outcome Fit" dimension — over-translation of clinical research concepts into a
  food-scoring dimension; does not survive Bari's "describe the food, not the eater" firewall
- Any sequencing that re-platforms finished work

## Deliverables

1. **Schema / dataclass** — `EvidenceStudy` object with fields:
   ```
   claim: str          # what the study claims (standardized vocabulary)
   dose_realistic: bool  # study dose ≤ 2× label dose of target product
   population_direct: bool  # study population matches Israeli consumer baseline
   rob_grade: Literal["low","moderate","high","very_high"]  # risk of bias
   evidence_tier: Literal["A","B","C","D"]  # A=Strong, B=Moderate, C=Weak, D=Insufficient
   source_doi: str
   notes: str
   ```
2. **Grading SOP** — 1-page doc: how Research uses the schema when evaluating a new study.
   Written in plain language; no GRADE jargon in the body (GRADE = inspiration, not the tool).
3. **Backfill** — apply the schema to the 5 existing SIE SUPP-EV entries and 3 highest-value
   food EV entries as a proof of concept. Not a full backfill of all EV entries.
4. **Evidence Registry v2 schema** — update the EV registry file header to reflect the new
   optional `study_objects:` block on each EV entry (backward-compatible; existing entries
   without it are valid).

## Acceptance criteria

- [ ] EvidenceStudy schema exists (Python dataclass or JSON Schema) with all 7 fields.
- [ ] Grading SOP is ≤1 page and uses no GRADE/RoB2 jargon in the body.
- [ ] 5 SIE + 3 food EV entries have a completed `study_objects:` block.
- [ ] Existing EV entries without `study_objects:` remain valid (no migration required).
- [ ] No new scoring rule or dimension is created by this task.

## Governance

- roadmap_impact: false (registry tooling; no scoring changes)
- Research leads; Nutrition co-signs the grading vocabulary and tier definitions
- No D7 required; no score-moving rules
