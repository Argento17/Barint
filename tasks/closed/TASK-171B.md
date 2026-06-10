---
id: TASK-171B
title: Phase 1 - Build 5 SIE Evidence Dossiers + lifecycle instantiation
owner: research-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Build the 5 MVP Evidence Dossiers (creatine, magnesium, vitamin D3, caffeine, omega-3 EPA/DHA) from the live reference layer (literature, dsld, pubchem, NIH ODS/EFSA), per methodology_v1.md schema + lifecycle fields. All verification_status=candidate / should_affect_score_now=false. Capture per-dossier build/maintenance cost metrics for Product's go/no-go gate. Nutrition co-signs tiers (D6/D7).
---

# TASK-171B — Phase 1 - Build 5 SIE Evidence Dossiers + lifecycle instantiation

## Return block (2026-06-03, research-agent) — proposing RETURNED

**Delivered** (`03_operations/supplement_engine/proto_v0/evidence_dossiers/`):
- 5 Evidence Dossier YAMLs: `creatine_monohydrate.yaml`, `magnesium.yaml`, `vitamin_d3.yaml`, `caffeine.yaml`, `omega3_epa_dha.yaml` — §5 schema + §5.1 lifecycle fields, all `verification_status: candidate`, `should_affect_score_now: false`, real cited values. All parse as valid YAML.
- `_build_cost_report.md` — measured build/maintenance cost for Product's go/no-go gate.

**Tiers are PROPOSALS** (claim-specific) pending Nutrition D6/D7 co-sign. CV-events claim flagged `contested`, NOT tiered.

**Clients smoke-tested LIVE:** pubchem, literature (PubMed), dsld. 21 literature queries, ~118 papers screened. No client failed.

**Fields flagged `NEEDS-ENV-VERIFY`** (5 dossiers): all UL/safety primary-source numbers (NIH ODS / EFSA / FDA sheets) — client retrieved evidence but the regulatory UL values must be confirmed against primary fact-sheets in the owner network before promotion. Omega-3 effective-dose (2-4 g/day TG) and EE-vs-TG bioavailability magnitude also flagged.

## Nutrition D6/D7 co-sign (2026-06-03, nutrition-agent)
- **All 12 claim tiers ratified** (no value changed): creatine strength=Strong/fat-loss=Insufficient; magnesium BP=Moderate/sleep=Weak; D3 status=Strong/bone-fracture=Moderate/broad=Weak; caffeine ergogenic=Strong/alertness=Moderate; omega-3 TG=Strong/brain&mood=Weak/CV-events=**contested→deferred** (Hard Rule 7).
- **3 scrutiny rulings:** omega-3 broad brain/mood held Weak with a built `conflation_firewall` (does NOT inherit clinical-MDD evidence; MDD claim untiered/provenance-only, out of MVP scope); magnesium sleep held Weak (directional low-certainty signal, re-adjudicate next sweep); D3 bone/fracture held Moderate (conditional — with-calcium/at-risk = strong end, broad = weak end).
- **UL governance meta-rule (D7):** veto at the most-credible *tolerance/hazard* threshold; higher number tracked as a note. → Magnesium **EFSA 250** governs (NIH 350 noted); omega-3 **EFSA 5 g no-concern** governs the veto, **FDA 3 g = Safety NOTE band** (FDA 3g is GRAS/labeling, not a tolerance ceiling); caffeine 400/200-preg confirmed; D3 4,000 IU adult confirmed (never apply adult UL to a children's SKU).
- Dossiers updated (finalized `evidence_tier`+`tier_rationale`, `ul_governing_decision`, `nutrition_cosign: true`); **SUPP-EV registry created** (`evidence_registry/supp_evidence_registry_v1.md`, SUPP-EV-001–005, omega-3 at 005, ashwagandha = deferred Phase-2 note). All stay `candidate` / `should_affect_score_now: false`. NEEDS-ENV-VERIFY flags on primary UL numbers retained.

## Build-cost finding (Product gate)
`_build_cost_report.md` → **conditional GO for Phase-2 scale-up**: (a) tiered sweep cadence (annual default, semi-annual for live-debate claims), (b) UL/safety via NIH ODS/EFSA re-sync not hand-derivation, (c) hard staleness alarm on any `contested` claim. Authority-leverage ≈ 0.375 of drift fields delegable; tier+form-ladder adjudication irreducibly in-house (correct — that's what the firewall protects). Dominant risk = **silent staleness on a contested active** (omega-3 = the canary), not build cost.

## CLOSED 2026-06-03 — orchestrator close-readiness gate
Artifacts verified on disk: 5 dossier YAMLs + `_build_cost_report.md` + `supp_evidence_registry_v1.md`; co-sign markers (`nutrition_cosign`, `ul_governing_decision`, `evidence_tier`, omega-3 `conflation_firewall`) confirmed present via grep (41 matches across 5 files). D6/D7 CO-SIGNED (Research built, Nutrition tiered). Candidate/non-score-affecting; no food artifact touched. `cc_reviewed: true`.

## Next
Phase 2 (TASK-171C, pending owner go) — engine prototype + 12-anchor golden-corpus validation; calibrates the §3 weights/caps/vetoes against the constructed PASS/FAIL fixtures. First point at which numbers move (still pre-launch).
