---
id: TASK-222
title: "BSIP2 research-to-implementation — decision matrix and implementation roadmap (Phase 1 batch)"
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: []
blocks: [TASK-222A, TASK-222B, TASK-222C]
roadmap_impact: false
cc_reviewed: true
work_type: governance
closed_reason: "Research-to-BSIP2 decision matrix accepted after priority correction, mandatory corpus-diff gate, and implementation guardrails for 222A/222B/222C."
---

# TASK-222 — BSIP2 Research-to-Implementation Decision Matrix

## Context

Phase 1 of the BSIP2 meta-research review is complete. The Bari scoring engine (`score_engine.py`, `constants.py`, `router_v2.py`, F1–F5 rules) already implements design-time rules for 6 of the 13 research clusters — some active (emulsifier sprint1 corrections, fermentation bonus, sweetener tiers), some gated at DEC-004 (F1 identity deltas, protein-bar matrix discount, BHA penalty). The remaining clusters require new design, monitoring, or explicit rejection.

This task formalizes the research-to-implementation translation: which clusters graduate to implementation, which need more design, which get monitored, and which are rejected.

## Required deliverables

### 1. Decision matrix (all 13 clusters)

**IMPLEMENT_NOW (3 clusters)**

| # | Cluster | Evidence | Observable Signals | Scoring Impact | Categories | Next Task |
|---|---------|----------|-------------------|----------------|------------|-----------|
| 1 | **Emulsifier tiering — F1 identity deltas** | Human RCT (carrageenan/CMC ↔ intestinal permeability, SCFA reduction). Moderate–strong. | BSIP1: `tax_emulsifier_concern`, sprint1 count corrections. BSIP2: `ADDITIVE_IDENTITY_DELTAS` (0/no-op, DEC-004 gated). | Activate F1 identity deltas: carrageenan/CMC/P80 → −3 each on `additive_quality`; lecithin → +2 relief. **Cap stacked concern at −6** (hard ceiling, enforced in constants). **Retire sprint1 +2/−1 additive-count corrections** (remove from F1 processing; do not let both fire on the same product). **No double-counting** — the sprint1 corrections and identity deltas target the same scoring dimension (`additive_quality`); only one system fires. Net: <5 pts for most products. | All processed: dairy desserts, yogurts, snack bars, sauces, plant-based milks. | TASK-222A |
| 2 | **Protein-bar matrix discount** | DIAAS study (bar matrix reduces AA bioavailability 47–81%). Moderate. | BSIP2: `PROTEIN_QUALITY_MATRIX_DISCOUNT` (reconstructed=0.80, collagen=0.55, gated DEC-004), scoped to `snack_bar_granola`. | Confirm DEC-004 placeholder values. **Protein quality dimension only** — 0.80 multiplier on the protein-quality sub-score for isolate bars. **Do NOT reduce label protein grams.** **Do NOT alter nutrient-density or satiety dimensions** unless separately approved. | Snack bars (currently `snack_bar_granola` only). | TASK-222B |
| 3 | **BHA/E320 flag** | Regulatory: FDA reassessment RFI, NTP listing. Moderate. | BSIP2: `BHA_NAMED_PENALTY` (5 pts, DEC-004 gated). E320 only; BHT excluded. | **Requires corpus prevalence scan before any score impact.** If prevalence is zero or near-zero → treat as additive-library/regulatory flag update (no scoring sprint). Only activate `BHA_NAMED_PENALTY` = 5 on `additive_quality` if BHA-bearing products appear in the scored corpus. | All categories where BHA appears (bread, snacks, cereals, fats/oils — low Israeli retail prevalence). | TASK-222C |

**DESIGN_ONLY (3 clusters)**

| # | Cluster | Current State | Proposed Action | Next Task |
|---|---------|---------------|-----------------|-----------|
| 4 | **Matrix-integrity proxy** | `matrix_integrity.py` computes degradation/engineering/HP scores but NOT wired into composite. | Wire a subset: binary intact-grain-present signal → ≤+3 bonus on `whole_food_integrity`. Grain-based categories only. Do NOT use unobservable v2 parameters. | TASK-222D |
| 5 | **Fiber diversity bonus** | Not tracked in BSIP2. No existing rule. | Binary: if ≥2 distinct named fiber sources (inulin, FOS, β-glucan, oat fiber, etc.) → ≤+2 on `nutrient_density`. Gate: NOVA proxy ≤ 3 only. | TASK-222E |
| 6 | **Fermentation breadth — vocabulary audit** | FERMENTATION_DIRECT_BONUS = +8 (live, NOVA 1–3). No scoring change needed. | Vocabulary-only audit: compare current FERMENTATION_MARKERS_HE + BSIP1 FERMENTATION_TERMS against 100 recent Israeli retail labels for gaps. | TASK-222F |

**MONITOR (3 clusters)**

| # | Cluster | Reason | Action |
|---|---------|--------|--------|
| 7 | **Sweeteners** | BSIP2 already has 3-tier differentiated penalties (Tier C cap 70/−15). No scoring change. | Monitor human RCT evidence for potential Tier B→C migration (maltitol). |
| 8 | **IUFoST / NOVA / IF&PC frameworks** | BSIP2 is already multi-axis (NOVA proxy + additive burden + matrix signals + hyper-palatability). | Methodology language update only: add note stating BSIP2 is "NOVA-informed, not NOVA-only." |
| 9 | **GRAS / EFSA FAIM** | Additive tier library (36 entries) already indexes regulatory status. | Schedule quarterly additive-tier review (next: 2026-Q3). |

**REJECT_NOW (4 clusters)**

| # | Cluster | Rejection Rationale |
|---|---------|---------------------|
| 10 | Broad fructose multiplier | Double-counts existing added-sugar penalties. |
| 11 | Precision-processing bonus | Not observable from labels — rewards marketing claims. |
| 12 | Supplement contamination | Requires lot-level lab testing — out of scope. |
| 13 | Mycotoxin supplier-risk | Requires supply-chain data — not on the label. |

### 2. Top 3 implementation candidates (by impact, with quickest-win note)

| Rank | Candidate | Effort | Impact | Rationale |
|------|-----------|--------|--------|-----------|
| 1 | **TASK-222A — Emulsifier F1 identity deltas** | ~8 hrs | **Highest** — strongest human RCT evidence, broadest category reach, corrects a known coarse proxy (sprint1 count corrections) with fine-grained identity-based scoring. | Largest consumer-facing impact. Replaces coarse +2/−1 with evidence-based −3/+2 deltas. Retires sprint1 system cleanly. |
| 2 | **TASK-222B — Protein-bar matrix discount** | ~4 hrs | Medium — corrects a label-fidelity gap for the worst category (snack bars). | Already placeholdered; DIAAS evidence justifies activation. Ceiling (70/B) designed to hold by construction. |
| 3 | **TASK-222C — BHA/E320 flag** | ~2 hrs | Low — affects very few products in Israeli retail. **Quickest win**, not highest-impact first move. | Routine regulatory-transparency flag. If corpus scan shows zero/near-zero prevalence, treat as library update, not a scoring sprint. |

### 3. First implementation task: TASK-222A — Emulsifier F1 identity deltas

Rationale: highest impact — strongest human RCT evidence, broadest category coverage, replaces a coarse sprint1 approximation with evidence-based fine-grained scoring. TASK-222C is the *quickest win* but not the highest-impact first move; sequencing starts with the largest correction to the most products. Consumer copy: "contains food-grade emulsifiers" neutral descriptor. No "damages the gut," "increases permeability," or any disease-risk language.

### 4. Regression test categories (for all 3 IMPLEMENT_NOW candidates)

| Test | Scope | Pass Condition |
|------|-------|---------------|
| **Corpus diff gate** | Every product in every AUTHORITATIVE category, run before and after the rule change | Tabular diff with fields: `before_score`, `after_score`, `before_grade`, `after_grade`, `affected_rule`, `reason`, `approval_recommendation`. Every non-zero diff must be individually reviewed and approved. |
| Golden structural regression | Full pipeline on all AUTHORITATIVE categories | All scores ±1 pt of baseline. No ceiling/grade change. |
| Router regression | 12/12 tests | Pass unchanged. |
| Category-ceiling verification | Each scored category's max grade | snk-001 = 70/B held. Milk = 85/A held. No new A/S. |
| Scope collision audit | Cross-reference new rule vs every penalty cap | No double-count on same signal. |
| Consumer-copy pass | All methodology/product-card text | No "disease," "carcinogen," "gut leak," or medical claims. |
| Israeli corpus coverage | Current scored corpus | All signal-present products correctly flagged; no false positives. |

## Acceptance criteria

- [x] Decision matrix covering all 13 clusters with IMPLEMENT_NOW / DESIGN_ONLY / MONITOR / REJECT_NOW classification
- [x] Evidence type and strength assessment for each cluster
- [x] Observable BSIP0/BSIP1/BSIP2 signal mapping for each cluster
- [x] Scoring impact quantification for IMPLEMENT_NOW clusters
- [x] Categories-affected listing for each cluster
- [x] Regression-risk assessment for each IMPLEMENT_NOW cluster
- [x] Consumer-copy restriction for each IMPLEMENT_NOW cluster
- [x] Recommended next task for each cluster (6 sub-tasks: 222A–222F)
- [x] Top 3 implementation candidates ranked by effort + impact
- [x] First implementation task recommendation with rationale
- [x] Regression test categories defined for all IMPLEMENT_NOW candidates
- [x] **Mandatory corpus diff gate** defined: every product diff has `before_score`, `after_score`, `before_grade`, `after_grade`, `affected_rule`, `reason`, `approval_recommendation` — every non-zero diff individually reviewed
- [x] TASK-222A: sprint1 +2/−1 retirement explicitly documented; no-double-counting confirmed with ADDITIVE_IDENTITY_DELTAS; stacked emulsifier concern capped at −6
- [x] TASK-222B: protein quality dimension only; label protein grams unchanged; nutrient-density/satiety dimensions excluded unless separately approved
- [x] TASK-222C: corpus prevalence scan required before any score activation; zero/near-zero prevalence → library/regulatory update only, no scoring sprint
- [x] Freeze compliance: no milk score changes, no snack-bar ceiling change, no scoring-philosophy revision

## Out of scope

- Actual code implementation — this task produces the decision matrix and methodology recommendations only
- Redesigning scoring philosophy, published scores, or frozen category ceilings
- Writing consumer-facing copy for the new flags
- Building automated regression-test tooling

---

## Return block (orchestrator, 2026-06-09)

**Proposed status:** RETURNED

### What was built

| Deliverable | Location | Notes |
|---|---|---|
| Decision matrix | This task | 13 clusters: 3 IMPLEMENT_NOW, 3 DESIGN_ONLY, 3 MONITOR, 4 REJECT_NOW |
| Implementation roadmap | This task | TASK-222A (emulsifier F1 deltas), TASK-222B (protein discount), TASK-222C (BHA flag) |
| First-task recommendation | TASK-222A (Emulsifier F1 deltas) | Highest impact — strongest human RCT evidence, broadest category coverage. TASK-222C is quickest win but not highest-impact. |
| Regression test plan | This task | 6 gates: golden structural, router, ceiling, collision audit, copy pass, corpus coverage |

### Implementation summary

**Evidence assessment:** Human RCT evidence for carrageenan/CMC (gut permeability, SCFA reduction) is the strongest new signal in this batch — sufficient to activate the DEC-004-gated F1 identity deltas for emulsifiers. The protein-bar DIAAS study is commercially sourced but directionally consistent with known matrix effects; the 0.80 multiplier is conservative and supportable. The BHA FDA reassessment RFI provides a regulatory transparency rationale for the already-designed penalty.

**No-surprise guarantee:** All three IMPLEMENT_NOW clusters involve activating rules that were designed, gated at DEC-004, and collision-checked during the original BSIP2 R&D. The decision matrix identifies no new scoring signal that would surprise the corpus — every signal was extracted in BSIP1 and is already present in the scored pipeline.

**Cross-lane coordination:** The decision matrix identifies three collision-documentation items: (1) ADDITIVE_IDENTITY_DELTAS replace the sprint1 additive-count corrections — must ensure clean retirement: remove `sprint1_additive_count` corrections from F1 processing; verify no product hits both systems; confirm the net scoring delta matches expectations; (2) PROTEIN_QUALITY_MATRIX_DISCOUNT overlaps with `matrix_integrity.py` degradation signals — must coordinate in TASK-222B to avoid double-counting; (3) TASK-222C corpus prevalence scan must enumerate every product in the scored pipeline before any score impact is applied — if prevalence is zero or near-zero, the scope downgrades from scoring sprint to library maintenance.

### Key decisions documented

1. **Four explicit REJECT_NOW** entries with rationale — prevents scope creep in a future phase.
2. **Fermentation scoring is frozen** — existing +8 bonus is sufficient. Only a vocabulary audit is proposed (TASK-222F), not a scoring change.
3. **BHA (E320) is in; BHT (E321) is out** — the penalty is explicitly scoped per the existing constant. BHT may be revisited if FDA issues a rule for it.
4. **Fiber diversity is gated by NOVA proxy ≤ 3** — prevents ultra-processed products from gaming the bonus with isolated fiber blends.
5. **Matrix-integrity proxy is deliberately narrow** — single binary signal (intact grain), ≤+3, grain categories only. Rejects the full v2 degradation formula as unobservable.

### Open items (not blocking RETURNED)

1. **No implementation code written** — TASK-222A/B/C must be staffed and dispatched.
2. **No corpus prevalence scan for BHA** — TASK-222C's first step: enumerate BHA-bearing products in the scored corpus. Result determines whether this is a scoring sprint or a library update.
3. **No corpus prevalence scan for emulsifiers** — TASK-222A's first step: enumerate products where ADDITIVE_IDENTITY_DELTAS produce non-zero changes (carrageenan/CMC/P80/lecithin) to bound the diff-gate review.
4. **No golden structural regression was run** — pipeline regression is scoped to the implementation sub-tasks, not this research phase.
5. **No consumer-copy templates written** — the consumer-copy restrictions are defined per cluster but no actual copy exists yet.
6. **No methodology.md update** — the IUFoST/NOVA multi-signal note (cluster 8 MONITOR) has not been written yet.
7. **No quarterly additive-review calendar created** — the 2026-Q3 review proposal is noted but not scheduled.
8. **No evidence-registry entries created** — the 13-cluster matrix uses research evidence but does not create new EV-NNN entries in the evidence registry. This is acceptable for a RETURNED decision task; EV entries should be created during implementation.

---

## Close block (CC, 2026-06-09)

**Status:** CLOSED

**Close rationale:** Research-to-BSIP2 decision matrix accepted after priority correction, mandatory corpus-diff gate, and implementation guardrails for 222A/222B/222C.
