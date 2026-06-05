---
name: bsip2_evidence_registry_v1
description: BSIP2 Evidence Registry v1 — 20 food findings, 20 guardrails, 20 deferred domains extracted from the Bari AI engineering specification PDF
metadata:
  type: project
  node_type: memory
---

**Registry location:** `C:\Bari\03_operations\bsip2\evidence_registry\`  
**Files:** `bsip2_evidence_registry_v1.md` + `bsip2_evidence_registry_v1.json`  
**Source document:** `C:\Bari\research\Engineering Architecture for AI.pdf` (78 pages)  
**Built:** 2026-05-30 — TASK-039

**Why:** Formal evidence registry grounding BSIP2 scoring decisions in the CNO's nutrition science research document. Governs which signals should be implemented, which must be blocked, and which are deferred pending better data.

**How to apply:** Before adding any new BSIP2 signal, check this registry. If a finding exists, use its recommended_action and should_affect_score_now flags. If no finding exists, the signal is not registered and requires a new evidence review.

## Registry Summary

- **20 primary findings** with full field extraction (finding_id, recommended_action, should_affect_score_now, required_input_fields)
- **20 guardrails** — misconceptions that must NOT be modeled (G-001 through G-020)
- **20 do-not-model-yet** — high-uncertainty domains deferred from algorithmic treatment

## Key counts

| Category | Count |
|---|---|
| implement_now | 17 |
| research_further | 3 |
| should_affect_score_now = true (label-ready today) | 9 |
| rejected signals | 3 |

## 9 Label-Ready Signals (can affect score now)

- **EV-003** `mucus_thinning_emulsifier_load` — CMC/P80/carrageenan vs lecithin vs gum arabic
- **EV-004** `allulose_adjusted_sugar_g` — allulose exemption from sugar scoring
- **EV-005** `polyol_laxative_potential` — polyol osmotic risk flag
- **EV-008** `matrix_state_factor` — liquid vs solid satiety discount
- **EV-010** `extrusion_matrix_penalty` — extruded product penalty
- **EV-012** `unsaturated_to_saturated_ratio` — fat ratio replaces absolute SFA (highest priority)
- **EV-015** `fermentation_quality_bonus` — fermentation markers already in BSIP1
- **EV-018** `reconstituted_matrix_flag` — milk powder detection
- **EV-019** `prebiotic_gum_exemption` — gum arabic exemption

## Recommended First 3 BSIP2 Upgrades

1. **EV-012** — Saturated-to-unsaturated fat ratio (zero new data required, 1 sprint)
2. **EV-003 + EV-019** — Emulsifier risk differentiation (Hebrew vocabulary + tiered logic, 1 sprint)
3. **EV-015** — Fermentation bonus activation (BSIP1 markers already exist, 0.5 sprint)

[[bari_governance_v1]] [[bsip2_v3_architecture]] [[governance_maturity_v1]]
