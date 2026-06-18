---
id: TASK-261
title: "EV-051 additive-cocktail cluster — calibrate + Product D7 co-sign"
owner: nutrition-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-12
depends_on: []
blocks: []
category_id: null
co_sign_required: [nutrition-agent, product-agent]
summary: >
  Nutrition-initiated D6 scoring-rule proposal (EV-051) extending EV-045 with a bounded
  emulsifier-gum-modified-starch co-occurrence interaction term, anchored on the NutriNet-Santé
  2025 PLOS Medicine T2D-mixtures cohort. Evidence entry + proposal spec filed; activation is
  gated on a marginal-discrimination calibration (net of EV-045/EV-003/NOVA) and Product D7
  co-sign. should_affect_score_now = false until both clear. No engine change in this filing.
---

# TASK-261 — EV-051 additive-cocktail cluster: calibrate + Product D7 co-sign

## Origin
Owner asked (2026-06-12) whether external research findings could enrich the BSIP2 model.
Of 7 candidates, only the additive-cocktail finding (NutriNet-Santé 2025) was both
implementable from the direct-scrape ingredient text and net-additive over existing rules —
and even that is an **extension of EV-045**, not a new dimension.

## Filed in this task (DONE)
- **EV-051** evidence entry — `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
  (human-cohort anchor for EV-045 + bounded co-occurrence-cluster proposal; `should_affect_score_now: false`).
- **D6 proposal spec** — `01_framework/bsip2_framework/docs/scoring/additive_cocktail_cluster_proposal_v1.md`
  (signal definition, four activation gates, calibration plan, bounded −3 penalty inside EV-045's −6 cap, rollback).

## Open (DoD to activate — none done yet)
1. **Research Agent** — confirm DOIs `10.1371/journal.pmed.1004570` + `10.1016/S2213-8587(24)00086-X`;
   extract the mixture-2 additive list verbatim into an evidence sheet.
2. **Data Agent** — run `cocktail_flag` over golden corpus + each live category; report cluster-positive
   frequency + **marginal Δscore net of EV-045/EV-003/NOVA** + any clean whole-food false positives.
3. **Nutrition Agent** — set bounded penalty (≤ −3, within EV-045 cap) **only if** marginal
   discrimination is demonstrated; otherwise recommend no-activation (evidence upgrade to EV-045 stands alone).
4. **Product Agent** — **D7 co-sign go/no-go** (frozen-invariant tripwire #1).
5. Frozen invariants re-verified unmoved (milk run_005_headpin, snk-001 70/B, bread retail_003)
   before any flag flip.

## Guardrails
- No engine code in this filing; activation behind `BARI_ADDITIVE_COCKTAIL` (default OFF = byte-identical).
- Anti-double-counting is the load-bearing gate; if marginal discrimination ≈ 0, do not activate.
- Consumer copy stays architecture-framed; no health-outcome claims (Hard Rule #5).
- Detection is from the direct-scrape ingredient panel only (EDPG firewall; OFF not used).
