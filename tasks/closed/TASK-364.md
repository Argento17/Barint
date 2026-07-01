---
id: TASK-364
title: EV-101: NutriNet-Sante preservatives/antioxidants -> hypertension+CVD (gated annotate-only proposal)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-21
reopened_at: 2026-06-21  # owner "go ahead" → execute the two gated follow-ups (Research full-text HRs → Product D7)
closed_at: 2026-06-21
close_reason: >
  Full chain done + orchestrator-verified. (1) EV-101 registered (annotate-only, 0 score moves), then CORRECTED on
  primary-source verification: lead author fixed Srour/Sellem→Hasenböhler (I confirmed via ESC+ACC); the 8 HTN
  preservatives are named individually (ESC verbatim, incl. E300+E330) and E300 is the sole CVD-linked individual
  additive — but the per-additive HR magnitudes are NOT primary-verified (paywalled full text), so I refused to enter
  the Research Agent's web-synthesis numbers (1.39/1.25/1.14…) as fact; only class HRs (abstract) + identities (ESC)
  are recorded as verified. (2) Research Agent attempted full-text extraction — identities obtained, magnitudes
  paywalled (honest gap). (3) Product Agent D7 CO-SIGNED (EV-061/E460 parity): E300+E330 functional→contested, LOW
  confidence, 24-month replication-revert (2028-06-21), additive-preservative-use only. Verified: only 2 governance
  files changed (additive_tiered_library_v1.md +48, evidence_registry +48); rows 1/3 confirmed flipped to contested;
  EV-101 co_sign updated; 0 engine/score/JSON edits (constants.py etc. = pre-existing TASK-362). Tripwire-1 held
  throughout (no published score moved); activation into headline score remains owner-gated and not done.
depends_on: []
blocks: []
category_id: null
close_reason: >
  EV-101 authored and verified in the evidence registry (Nutrition Agent, orchestrator-verified). Paper independently
  verified REAL (DOI 10.1093/eurheartj/ehag308 resolves on Oxford Academic, published 2026-05-20, NutriNet-Sante,
  n=112,395) — my initial DOI skepticism was wrong. Entry sits at bsip2_evidence_registry_v1.md:2590-2636; registry diff
  is exactly +47 lines, ONE file, zero engine/score/JSON edits (constants.py/router_v2.py in the tree are pre-existing
  TASK-362 bars changes, confirmed unrelated). Gated, annotate-only, default-OFF (BARI_GLASSBOX_W2), should_affect_score_now=false,
  published_scores_moved=0. cosmetic_mup verdict: EV-059 field unchanged (function-class correct); the challenge is to the
  D4 *tier* (E330/E300 functional -> contested, EV-061/E460 rubric). Open downstream gates are tracked in EV-101's
  co_sign + future_actions fields (Product D7 co-sign; Research full-text per-additive HR extraction; 24-month
  replication-revert). Activation would be a published-score move = OWNER tripwire (not done; just registered).
summary: >
  Evidence-watch deferred item now actionable (paper published 2026-05-20). Register NutriNet-Sante preservative-additive -> HTN/CVD finding (EHJ, doi 10.1093/eurheartj/ehag308, n=112,395) as a GATED, annotate-only D4/D6 EV proposal. 0 published scores move; D7 + owner gate before any activation. Bears on EV-059 cosmetic_mup=False classification of preservatives/antioxidants/acidulants; sibling of EV-061/EV-051 NutriNet family.
---

# TASK-364 — EV-101: NutriNet-Sante preservatives/antioxidants -> hypertension+CVD (gated annotate-only proposal)

## Deliverable (DONE, orchestrator-verified)
- `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md:2590-2636` — new EV-101 entry, mirroring the
  EV-061 / EV-051 NutriNet-Sante annotate-only template (verified HRs from abstract, study_objects yaml tier B,
  anti-double-counting gate, EDPG/OFF firewall, risk-of-misuse health-claim prohibition).

## Verification (orchestrator)
- Source real: WebSearch + Oxford Academic confirm DOI/n/date. HRs in entry match abstract (non-antiox HTN 1.29
  [1.20-1.39], CVD 1.16 [1.04-1.29]; antiox HTN 1.22 [1.13-1.31]). Per-additive HRs flagged PENDING full-text (honest).
- 0 score/engine/JSON edits: `git diff --stat` = registry only, +47 lines. Grep of proto_v0/src for EV-101/ehag308 = none.

## Follow-ups STATUS
1. ✅ Research full-text extraction — DONE (identities verified via ESC; per-additive HR magnitudes paywalled/not-obtained, honestly flagged).
2. ✅ Product D7 co-sign — DONE (E300/E330 functional→contested, LOW conf, 24-month revert; applied to additive_tiered_library_v1.md §2.A rows 1/3 + §9).

## Still open (NOT blocking close — tracked in EV-101 + library)
- Consumer tooltip copy for E300/E330 at `contested` MUST go through Content Agent + Red-Team two-gate sign-off before any consumer string ships (must preserve: additive-use-only / observational-not-causal / LOW-confidence).
- Per-additive HRs/CIs for E300/E330 still paywalled — refresh if full text becomes accessible.
- 24-month replication-revert check (2028-06-21): if no independent cohort replicates the antioxidant-preservative HTN signal, revert both to `functional`. (Covered by the standing BSIP2 evidence-watch routine.)
- SCOPE NOTE: same paper names E202/E224/E250 (non-antioxidant preservatives) individually as HTN-associated; left `likely-neutral`. A separate tier review for those is a candidate follow-up — deliberately out of this proposal's antioxidant-subgroup scope.
- Activation of D4 into the headline score (if ever) = published-score move = OWNER tripwire + marginal-Δscore proof net of NOVA/additive signals.
