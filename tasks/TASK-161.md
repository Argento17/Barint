---
id: TASK-161
title: Unify all comparison rows to hummus rich-row format (+/- reason + headline metric)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
cc_reviewed: 2026-06-02
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
close_reason: "CC gate PASS (cc_reviewed set). Objective met + QA-verified across 5 sub-tasks: ALL comparison rows now render the hummus rich-row format — green + (positiveSignals[0]) / amber - (limitingFactors[0]) rowReason + a per-category headline metric bar. 161A (Nutrition) chose metrics: protein for cheese/yogurts/veg-spreads/bread, NO bar for snacks (nutrition all-null), milk as-is. 161B (Data) regenerated +/- signals from BSIP2 traces (cheese 42+/44-, yogurts 10+/4-, bread 24+/19-), scores id-matched unchanged, 0 banned phrases. 161C (Frontend) wired metricSpecs+rowReason via shared row-surface.ts; tsc/build/lint/corpus all exit 0. 161E (Content) scrubbed bread false-positives (0 remain). 161D (QA) confirmed parity + score-neutrality. Display-only; no scores changed by 161."
follow_ups: "Non-blocking, carved out (not part of 161 scope): (1) bread headline switch protein->fiber (needs fiber_g wired into BariProductMetricsVM); (2) vegetable-spreads per-100g protein preset (aria-unit); (3) ESCALATION bread shufersal_3268429 — A-vs-B grade divergence + name/signal grain-base inconsistency, frozen-invariant -> Product/Nutrition; (4) OWNER commit-bundle decision: hummus/maadanim/yogurts rescores are co-resident uncommitted (TASK-149/150/143)."
summary: >
  ALL comparison pages adopt the hummus row anatomy: green + (top positiveSignal) / amber - (top limitingFactor) under the name + a headline metric bar. Outliers: cheese/yogurts (no signals), bread (no limitingFactors), snacks (no protein), milk (no rowReason). Cross-agent: Nutrition metric decision + Data signal regen gate Frontend wiring.
---

# TASK-161 — Unify all comparison rows to hummus rich-row format (+/- reason + headline metric)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
