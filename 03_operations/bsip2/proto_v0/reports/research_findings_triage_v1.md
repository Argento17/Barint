# BSIP2 Coverage Triage — 10 Research Findings

**Date:** 2026-06-10  
**Reviewer:** Scoring Governance Lead  
**Method:** Finding-by-finding mapping against existing BSIP2 signal extraction, dimension scoring, constants, and evidence registry.

---

## Triage Table

| # | Finding | Existing BSIP2 coverage | Verdict | Recommended action | Demolition risk |
|---|---------|------------------------|---------|-------------------|-----------------|
| 1 | Food Matrix Collapse as Primary Satiety Mechanism | **Partial.** NOVA proxy (processing_quality, WFI) captures ultra-processing degree. Fragmentation captures structural form (intact→reconstructed). HP patterns capture unhealthy combos. Satiety_support uses protein+fiber/kcal. **Not covered:** soft/homogenized/paste-like matrices that reduce oro-sensory satiety independent of nutrient composition; liquid-calorie bypass mechanism beyond beverage calorie_density category defaults. | Already covered (partial) | No action. The satiety gap is acknowledged but not label-detectable in current data (no "homogenized" / "pasteurized" / "texture-modified" indicator reliably available). If oro-sensory texture markers become label-observable (e.g., "smooth", "creamy", "paste"), create a future scoring task. | Low — no existing rule would be contradicted. Fragmentation already captures extreme cases (reconstructed). The gap is granularity, not contradiction. |
| 2 | CMC Individualized Dysbiosis Response | **Full.** CMC is penalised through: (a) F1 identity delta −3 on additive_quality (TASK-222A, line score_engine.py:1235); (b) ECS-v1 high weight −5 (TASK-224, line score_engine.py:1280); (c) marker_count contribution if text matches emulsifier/stabilizer patterns (signal_extractor.py:116–139). The evidence base (EV-003, EV-043, BEV-081) is registered. Individual variability is noted but not actionable from labels — no microbiome marker is label-observable. | Already covered | No action. Individual susceptibility is acknowledged in evidence registry (BEV-081 annotate_only) but not implementable from labels. Maintain current penalties. | None — CMC is already a named concern. Adding a new rule would duplicate existing F1 + ECS coverage. |
| 3 | HPP Preserves Micronutrient / Bioactive Integrity | **Zero.** HPP is not mentioned anywhere in signal_extractor.py, constants.py, or score_engine.py. It is not label-detectable in current Israeli retail data: no mandatory "high-pressure processed" declaration exists on Israeli labels. | Not implementable from labels | Backlog/monitoring only. If HPP labelling becomes mandatory or reliably detectable (e.g., via retailer-supplied processing metadata), revisit. No methodology work warranted. | None — no existing rule to contradict. |
| 4 | Fiber Quality: Viscous/Gel-Forming Drives Satiety | **Covered but gated.** EV-006 is accepted. FFV-v1 vocabulary (fiber_functional_vocabulary_v1.md) is complete: maps beta-glucan, psyllium, native guar, pectin → viscous; inulin, FOS, GOS, resistant dextrin, PHGG → non-viscous. **Scoring path is NOT wired** — score_engine.py uses total_fiber_g (flat 2.0× multiplier in glycemic_quality, 5.0× in satiety_support, line 1202 and 1375). No viscous/non-viscous differentiation. | Covered but gated | Amend existing spec. Wire viscous fiber weighting into glycemic_quality and satiety_support dimensions. Use presence-only detection (FFV-v1 vocabulary) with credit-capped bonus per EV-006's risk_of_misuse constraint. Constants design: `VISCOUS_FIBER_MULTIPLIER` (+2× bonus relative to non-viscous), `VISCOUS_FIBER_PRESENCE_CAP`. | Low — viscous fiber bonus would sit inside the existing fiber scoring path. No existing rule contradicted; the total_fiber_g path already has capacity for refinement. |
| 5 | Resistant Starch / Inulin as Prebiotic Multipliers | **Covered but gated.** FFV-v1 vocabulary covers: resistant starch (עמילן עמיד), resistant dextrin (דקסטרין עמיד), inulin (אינולין), FOS (FOS/אוליגופרוקטוז/פרוקטטו-אוליגו-סכריד), GOS (GOS/גלקטו-אוליגו-סכריד), acacia/gum arabic (גומי ערבי/E414). **Scoring path is NOT wired** — no prebiotic multiplier exists beyond the flat fiber bonus. | Covered but gated | Future scoring task — group with Finding 4 (viscous fiber). EV-006 and FFV-v1 provide the vocabulary; scoring requires a separate design + implementation phase. Not a priority until viscous fiber scoring is wired first (Finding 4 is more impactful). | Low — prebiotic credit would be additive to fiber bonus. No existing rule contradicted. |
| 6 | Polyphenol Bioavailability: Processing Method and Matrix Interaction | **Zero.** No polyphenol detection, no processing-method detection, no bioavailability scoring. Polyphenols are not label-detectable in current Israeli data (mo quantity column; processing method is not reliably declared). | Not implementable from labels | Backlog/monitoring only. If polyphenol data becomes available (e.g., USDA FDC extended fields for Israeli imports), revisit. No methodology work warranted. | None — no existing rule. |
| 7 | FDA 2026 Regulatory Changes: GRAS Reform / Synthetic Dye Phase-Out | **Partially tracked.** D4 additive framework exists in evidence_registry_v1.md (BEV-078–BEV-081): sulfites (score_moving_pending_d7), azo synthetic dyes (score_moving_pending_d7), neutral additives (annotate_only). **No active watchlist for FDA GRAS reform** or for phase-out timelines. Synthetic dye E-numbers (E102, E110, E122, E124, E129) are label-observable but no scoring rule is active — all D4 entries are pre-activation pending D7 sign-off. "No artificial colors" claims are not validated. | Already covered (partial) | Registry note only. Add a BEV entry to track FDA GRAS reform + dye phase-out as monitoring signals. Do not create scoring rules until D7 co-sign is obtained (per D4 governance). No code change — evidence registry update only. | Low — D4 entries are pre-activation; no active scoring rule to duplicate. |
| 8 | Protein Quality: DIAAS vs PDCAAS for Plant Protein Reassessment | **Partial.** DIAAS detector exists (detect_diaas_signal, TASK-179P, BARI_GLASSBOX_W15 flag, score_engine.py:2510). R1 protein rules with category-relative scales exist (constants.py:388–397). F2 matrix discounts exist (protein_quality, PROTEIN_QUALITY_MATRIX_DISCOUNT). **Not covered:** sprouting logic (sprouted grains get no bonus), complementary protein blend logic (rice+pea → no completeness credit). | Already covered (partial) | Future scoring task — sprouting and complement are label-detectable (sprouted grains in ingredient list, legume+grain patterns) but require vocabulary + scoring design. The DIAAS path (Glass Box W1.5) already covers the amino-acid-completeness dimension. | Low — sprouting/complement would add to existing protein_quality dimension. No contradiction with DIAAS (which targets completeness, not processing benefit). |
| 9 | CMC Non-Finding: Dose and Microbiota Variability Context | **Full.** CMC is penalised via F1 (−3) + ECS-v1 (−5). The evidence registry (BEV-081) already acknowledges the 2026 RCT showing no acute inflammation markers alongside lowered SCFA. The nuance (short-term non-findings do not override CMC-specific mechanistic/susceptibility evidence) is consistent with the current treatment — the penalty is based on EV-003 mechanistic evidence, not acute null studies. | Already covered | Registry note only. Add a clarification to BEV-081 or EV-003 stating that short-term average-effect non-findings are reconciled with and do not override CMC-specific mechanistic/susceptibility evidence. No scoring change. | Low — evidence clarification only. Current penalties remain. |
| 10 | Limonene Bioavailability and Citrus Processing | **Zero.** D-limonene and citrus flavonoids are not tracked. Not relevant to supermarket food scoring at current data resolution — no limonene quantity, no citrus-processing method, no bioavailability data on Israeli labels. | Not implementable from labels | Backlog/monitoring only. Low priority. | None — no existing rule. |

---

## Verdict Summary

| Verdict | Count | Findings |
|---------|-------|----------|
| Already covered | 3 | #2 (CMC), #4 (Fiber quality — vocab exists), #9 (CMC non-finding) |
| Already covered (partial) | 3 | #1 (Matrix collapse), #7 (FDA regulatory), #8 (DIAAS protein) |
| Not implementable from labels | 3 | #3 (HPP), #6 (Polyphenols), #10 (Limonene) |
| Covered but gated (scoring absent) | 2 | #4 (Viscous fiber scoring not wired), #5 (Prebiotic scoring not wired) |
| Missing | 0 | None — every finding maps to at least partial existing coverage |

---

## Required Actions

### No action (6 findings)
- #1 Food Matrix Collapse — satiety gap is acknowledged but not label-detectable
- #2 CMC Individualized Dysbiosis — fully covered by F1 + ECS-v1
- #3 HPP — not label-detectable; monitoring only
- #6 Polyphenols — not label-detectable; monitoring only
- #9 CMC Non-Finding — covered by existing evidence registry entries
- #10 Limonene — not relevant; monitoring only

### Registry note only (2 findings)
- #7 FDA 2026 Regulatory Changes — add BEV entry tracking FDA GRAS reform + dye phase-out as monitoring signals. No scoring change.
- #9 CMC Non-Finding — add clarification to BEV-081 that short-term average-effect non-findings are reconciled with and do not override CMC-specific mechanistic evidence.

### Amend existing spec (1 finding)
- #4 Fiber Quality: Viscous/Gel-Forming — wire FFV-v1 vocabulary into glycemic_quality and satiety_support dimensions. Design constants: `VISCOUS_FIBER_MULTIPLIER`, `VISCOUS_FIBER_PRESENCE_CAP`. Implementation follows the precedent of ECS-v1 (TASK-224): vocabulary exists separately from scoring; scoring is a separate implementation phase.

### Future scoring task (2 findings)
- #5 Resistant Starch / Inulin — group with Finding 4 implementation. Prebiotic multiplier logically follows viscous fiber scoring.
- #8 Sprouting + Protein Complement — requires vocabulary + scoring design. DIAAS path (Glass Box W1.5) already covers amino-acid completeness.

### No methodology amendment required (10/10 findings)
No finding requires a new methodology spec. Finding 4 (viscous fiber) requires a scoring implementation on top of existing vocabulary, not a new methodology. All other findings are either already covered, not implementable, or require only registry notes.

---

## Demolition Risk Summary

| Risk level | Count | Details |
|------------|-------|---------|
| None | 10 | No finding would duplicate or contradict existing BSIP2 logic if implemented. |
| High | 0 | — |

Every finding that could potentially be implemented (viscous fiber, prebiotic, sprouting) would add to existing scoring paths rather than replace or shadow them. No demolition risk exists.
