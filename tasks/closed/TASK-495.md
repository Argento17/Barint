---
id: TASK-495
title: EV-017 flag-vs-score review: reconcile population-RCT meta vs class-not-tier evidence
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-05
close_reason: >
  PROPOSE-only review complete + orchestrator-verified (2026-07-05 unattended run). Recommendation:
  KEEP should_affect_score_now=false — NO score change. Crux resolved: the 2026 Tufts/Mozaffarian 21-RCT
  meta (PMID 42347889, verified) clears the population-signal gate but is CLASS-level and explicitly
  tier-silent, so it cannot license EV-017's tier-level (sucralose/saccharin-flag vs stevia/monk-fruit-neutral)
  move; scoring the class would wrongly penalize stevia/monk-fruit equally (Frontiers mouse data even shows
  divergent tier effects, supporting the current split). No tripwire tripped (status quo maintained). Memo:
  03_operations/reports/nutrition/task495_ev017_flag_vs_score_recommendation_v1.md; C0 PASS. One within-lane
  follow-up (no D7, no score): retire the now-inaccurate "high inter-individual variability" grounds-language
  in the EV-017 registry entry → spun off as TASK-514. Any future score-active conversion = tripwire-1 (owner+Product).
depends_on: []
blocks: []
category_id: null
summary: >
  D6/D7 review teed up by the 2026-07-03 EV-017 REFINES addendum (Tufts/Mozaffarian 21-RCT meta). Question: is 'high inter-individual variability' still valid grounds for should_affect_score_now=false now that a population-level RCT-meta counterexample exists? Crux to resolve: the meta operates at the NNS *class* level while EV-017's actionable content is a *tier* (sucralose/saccharin flag vs stevia/monk-fruit neutral). Requires Nutrition + Product co-sign; trips published-scores tripwire only if it proceeds to a live change. PROPOSE-only until then. DOIs pending Research Agent.
---

# TASK-495 — EV-017 flag-vs-score review: reconcile population-RCT meta vs class-not-tier evidence

## Dependency: Research DOI verification — SATISFIED + orchestrator-verified (2026-07-05)
Report: `03_operations/reports/research/task495_ev017_doi_verification_v1.md`. C0 validate_return PASS.
3/3 citations resolve, 0 retractions. Primary: PMID 42347889 / DOI 10.1007/s11883-026-01429-9 (Wang, Wu,
Wallen, Mozaffarian — *Current Atherosclerosis Reports* 28:65, 2026-06-25; 21 RCTs). CRUX RESULT: the meta
pools ALL non-nutritive sweeteners as a single **class** and is explicitly silent on **tier** structure
(paper's own stated limitation: "grouping them together may obscure the full picture"). It can neither
confirm nor refute EV-017's sucralose/saccharin-flag-vs-stevia-neutral tier split. Supporting: Frontiers mouse
study (weak) + UK Biobank cohort n=133,285 (moderate, observational).

## Nutrition review DISPATCHED 2026-07-05 3AM run (PROPOSE-only — no score change unattended)
Nutrition Agent (Sonnet) synthesizes: does the class-level RCT-meta counterexample invalidate
`should_affect_score_now=false` for EV-017, given the meta is tier-agnostic? Output = written recommendation
only. Any proposal to move a live score is tripwire-1 → parks for owner + Product co-sign; NOT executed here.
