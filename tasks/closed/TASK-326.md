---
id: TASK-326
title: Salvage FDA Red-3/6-dye phase-out signal -> D4 azo-dye corroboration note (annotate-only, no score move)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified PASS. Nutrition Agent (C1-Sonnet) landed a no-score-change corroboration
  addendum at EV-059 (bsip2_evidence_registry_v1.md lines 1990-1998) on the existing contested
  Southampton-6 azo-dye tier. Verified against artifacts: git diff --stat HEAD on the registry =
  +26 insertions / 0 deletions / 1 file (purely additive, no existing content altered); no
  score_engine/constants/render_fields/config/page-JSON touched (only pre-existing dispatch.py in
  the tree, unrelated). FDA facts sourced to FDA.gov/HHS.gov primaries: Red 3 revocation (signed
  2025-01-15, erythrosine=E127, correctly flagged xanthene NOT azo + NOT one of the six) and the
  2025-04-22 HHS/FDA 6-dye phase-out (3/6 overlap with registry: E102/E110/E129). Firewall
  preserved (label-observable E-numbers; US jurisdiction does not move Israeli posture); contested
  tier confirmed-not-promoted; azo-dye cap future-action left gated (no D6/D7 opened). Return
  contract complete. SHA256 of artifact: E63E8E9C515A2EE9176918C7BE47E3A5EBF88F46C4B3AE5D71FEC4CB541DA35C.
summary: >
  Verify FDA facts (Red 3 revocation + 6 synthetic dyes phased out by 2027, dates/sources), map to existing contested azo-dye tier (E102/E110/E122/E124/E129/E104) + the standing azo-dye cap future-action; land a no-score-change corroboration addendum routed research/nutrition. Firewall preserved (dyes are label-observable E-numbers). No published-score movement (tripwire-1).
---

# TASK-326 — Salvage FDA Red-3/6-dye phase-out signal -> D4 azo-dye corroboration note (annotate-only, no score move)

Annotate-only corroboration addendum added at EV-059 of the BSIP2 evidence registry. FDA Red 3
revocation (2025-01-15) + HHS/FDA 6-dye phase-out (2025-04-22) corroborate keeping the six
Southampton azo dyes in the **contested** tier and strengthen the standing "azo-dye cap before any
children's-cereal launch" future-action. No published score, grade, tier, or cap changed; any
activation remains an owner-gated D6/D7 proposal (tripwire-1). Salvaged from the Project-Comp
baseline signal via the orchestrator.
