---
id: TASK-132
title: Review BSIP2 Evidence Watch 2026-06-01 and evaluate potential BSIP2 revisions
owner: research
status: DONE
priority: MEDIUM
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Review BSIP2 Evidence Watch 2026-06-01 and evaluate potential BSIP2 revisions
---

# TASK-132 — Review BSIP2 Evidence Watch 2026-06-01 and evaluate potential BSIP2 revisions

## Scope

Review `research/BSIP2_Evidence_Watch_20260601.md` (5 findings + EFSA regulatory note) and
evaluate the proposed BSIP2 revisions against the live framework
(`01_framework/bsip2_framework/`, algo v0.3.1).

## Deliverable

[BSIP2_Evidence_Watch_20260601_EVALUATION.md](../research/BSIP2_Evidence_Watch_20260601_EVALUATION.md)

## Conclusions

- **F2 (protein-bar matrix discount): ADOPT, High.** Best evidence (n=1,641, validated DIAAS)
  and best fit — directly closes the protein-isolate-bar gaming hole already named in
  `matrix_integrity_framework.md`.
- **F1 (emulsifier tiering): ADAPT, Med-High.** Directionally right *both ways* — also corrects
  the current flat over-penalty of soy lecithin. Single RCT → keep deltas modest. Needs
  named-additive metadata.
- **F4 (BHA flag): WATCH, Low.** Toxicology is a scope edge for a structure-based scorer;
  regulatory-only evidence; partly stale (Apr-2026 comment window closed). Cheap only if the
  F1 named-additive taxonomy is built anyway.
- **F3 (fiber-diversity bonus): DEFER.** In-vitro only and, as written, *opens* a gaming path
  that F2 closes; also requires the not-yet-decided positive-signal architecture (Tension 4).
- **F5 (sucralose mouse study) + EFSA FAIM note: NO CHANGE / NO ACTION.** Agree with the Watch.

**Cross-cutting:** F1/F2/F3 all point at the documented "components vs. structure" gap. Highest
leverage = build the ingredient-fragmentation + named-additive taxonomy
(`matrix_integrity_framework.md` Req 1) once; it unlocks F1, F2, and a gaming-resistant F3.
Respect the Tension-5 rule budget (modulate existing weights, don't add caps).

## Decision (2026-06-01)

Owner approved **F2, F1, F4** for implementation; **F3 deferred**; F5 / EFSA note no action.
Implementation work registered under objective **TASK-133** (taxonomy-first sequencing per the
evaluation). This review task is complete.
