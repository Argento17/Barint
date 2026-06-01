# BSIP2 Revision Evaluation — Evidence Watch 2026-06-01

**Task:** TASK-132
**Owner:** Research Agent
**Date:** 2026-06-01
**Source under review:** [BSIP2_Evidence_Watch_20260601.md](BSIP2_Evidence_Watch_20260601.md)
**Framework reference:** `01_framework/bsip2_framework/` (algorithm v0.3.1; specification `bsip2_concept_v1`)

---

## Purpose

The Evidence Watch proposes scoring revisions from five recent findings. This document evaluates each proposed revision against three axes the Watch does not address:

1. **Architecture fit** — does the live BSIP2 spec already have a mechanism for this, and what would actually change?
2. **Gaming resistance** — does the revision close or open a manipulation path?
3. **Evidence-to-determinism fit** — BSIP2 is a deterministic, population-level scorer. Over-fitting it to individual fresh studies is itself a risk (see Tension 5, rule explosion).

Recommendation grades used: **ADOPT** / **ADAPT** (adopt with material changes) / **DEFER** / **WATCH** / **NO CHANGE**.

---

## Headline: three of five findings point at the *same* known gap

Findings 1, 2, and 3 are not five unrelated patches. F1 (emulsifier identity), F2 (protein-bar matrix), and F3 (fiber-source diversity) are all instances of the gap BSIP2's own design docs already name as the central unresolved problem:

> *"The current system cannot distinguish [a reconstructed protein bar] from a food that delivers the same macros through an intact matrix — because it is measuring components, not structure."* — `matrix_integrity_framework.md`

> *"Develop an Engineering Intensity metric derived directly from ingredient markers rather than mapped from NOVA."* — `current_architecture_tensions.md`, Tension 1

The single highest-leverage move is **not** to bolt on five rules. It is to build the **ingredient taxonomy with fragmentation + named-additive metadata** that `matrix_integrity_framework.md` already specifies as *Requirement 1*. That one piece of infrastructure unlocks F1 (per-additive penalty tiering), F2 (source-aware protein discount), and a gaming-resistant version of F3. Treating these findings as empirical *prioritization signal* for that infrastructure is worth more than treating them as five independent tweaks — and it respects the rule-budget constraint in Tension 5 ("Bari should not become NOVA with more math").

---

## Finding 1 — Emulsifier-specific gut effects → tiered emulsifier penalty

**Recommendation: ADAPT (Medium-High priority, gated on named-additive metadata)**

**What BSIP2 does today.** `emulsifier` and `stabilizer` are *generic* markers (`signal_system.md`). Both feed the additive-burden count (caps at 3–4 markers → 65; 5+ → 55) and the additive-quality dimension (−12 per marker type). The processing dimension applies a flat **−6 for any emulsifier** regardless of identity. Carrageenan (E407) and CMC (E466) are not distinguished from soy lecithin (E322).

**Why the revision is directionally right — in both directions.** The Watch frames this as *raising* penalties for carrageenan/CMC. The more important consequence is the *opposite*: the finding reports soy lecithin and native rice starch as near-neutral at dietary doses, which means **the current flat −6 over-penalizes lecithin.** A tiered scheme improves accuracy at both ends — it is not purely additive severity. That makes it a calibration correction, not a new punitive layer, which is the right kind of change for this architecture.

**Cautions:**
- **Single RCT (n=60).** The carrageenan-permeability and CMC-SCFA results are *consistent with prior literature* (Chassaing et al. on CMC; long-standing carrageenan debate) but should not be over-weighted. Keep penalty deltas modest.
- **Food-grade vs. degraded.** Carrageenan toxicity literature is muddied by degraded carrageenan (poligeenan); food-grade is the relevant species. Note this in the rule rationale.
- **Native vs. modified starch.** "Native rice starch → functional ingredient" is defensible (aligns with the concentration/culinary distinction in `beneficial_processing.md`), but only for *unmodified* starch. Modified starches remain stabilizers. And the study still showed a *sub-significant* SCFA trend for native starch — so the target is "near-neutral," not "positive credit."

**Implementation (rule-budget-neutral):** Do **not** add new caps. Replace the flat emulsifier/stabilizer penalty weights with identity-modulated weights driven by a named-additive lookup (carrageenan, CMC → higher; lecithin → lower/near-zero; native starch → excluded from additive burden). This rides on the same named-additive metadata F2 and F4 want, so build it once.

---

## Finding 2 — Protein-bar matrix degrades DIAAS to 47–81% → matrix discount on bar protein

**Recommendation: ADOPT (High priority — strongest evidence + strongest architectural fit)**

**This is the flagship finding.** `matrix_integrity_framework.md` already names the protein isolate bar as *the* canonical gaming vulnerability (its §"Protein isolate bar" and §"Gaming vulnerability"). This study supplies exactly what the design doc lacked: **empirical quantification** (n=1,641 bars; in-vitro INFOGEST DIAAS at 47–81% of label) of a structural problem BSIP2 already knows it cannot currently see.

**What BSIP2 does today.** Protein Quality is a 9%-weight dimension measuring "protein quantity and sourcing method." A `protein_isolate` marker exists; a `snack_bar_granola` category exists. But there is **no matrix/format discount** — a reconstructed bar's protein counts at near-face value, which is precisely the "wins the score without delivering the structure" hole the framework warns about.

**Why adopt with confidence:** highest evidence grade (large n, validated methodology), closes a *documented* gaming hole, and serves the architecture's stated direction (Engineering Intensity / matrix integrity). Unlike F3 it is a *penalty*, so it fits the current penalty-avoidance architecture (Tension 4) without requiring the not-yet-decided "positive signal" machinery.

**Implementation guidance:**
- Apply the discount inside the **Protein Quality dimension** for bar-format + `protein_isolate`/reconstructed-source products, not as a blanket cut to `protein_g` (other dimensions like satiety still legitimately see the protein mass).
- Use the empirical range as a **band, conservatively** (lean toward the larger discount given the data are in-vitro DIAAS, not in-vivo): discount the protein-quality contribution rather than asserting a precise per-product DIAAS.
- **Collagen:** add a `collagen` marker (new) and an additional discount — justified independently by incomplete amino-acid profile and the study's lowest measured matrix digestibility. This is squarely "sourcing method," already in the dimension's remit.
- **Coordinate via the PROCESSING_LOAD concern family** so the matrix discount does not double-count with NOVA-4 / additive caps that already bind on the same bars (`methodology.md` Stage 5; `score_resolution_contract.md` concern coordination).
- New signals required: `collagen` marker; protein-source granularity (isolate vs. intact). Bar-format detection already exists via category.

---

## Finding 3 — Fiber-diversity SCFA synergy (+32.8%) → fiber-diversity bonus

**Recommendation: DEFER (evidence + gaming + architectural-novelty concerns; lower priority than the Watch assigns)**

The Watch rates this Medium priority "implement." I rate it lower, for three independent reasons:

1. **Evidence is in-vitro only.** n=33 fecal fermentation, no in-vivo RCT. The Watch itself grades it Medium. A deterministic scorer should not encode an in-vitro synergy figure as a live bonus.

2. **Direct gaming exposure.** A naive "3+ distinct fiber types → bonus" is *exactly* the manipulation `matrix_integrity_framework.md` Requirement 5 warns against: a reconstructed bar can add small amounts of three *isolated* fibers (inulin + chicory + cellulose) and claim the synergy halo. The 32.8% synergy was observed across *whole-food-derived* diverse fibers in fecal inocula; isolated-added-fiber synergy in vivo is not established. So the bonus, as written, would **reward the very gaming pattern F2 is trying to penalize** — the two findings pull against each other if F3 is implemented naively.

3. **It is an architecturally novel mechanism, not a tweak.** BSIP2 has **no guardrail bonuses** — by deliberate design (Tension 4: "no structural positive caps that lift a score"). Introducing a positive lift is a philosophy-level decision that belongs to the unresolved "nourishment markers" question, not to a single evidence-watch cycle.

**If pursued later:** credit fiber diversity *only* when it arises from multiple distinct **whole-food sources** (e.g., whole grain + legume + vegetable), gated on matrix integrity and Requirement-5 gaming resistance, and only after the positive-architecture direction (Tension 4) is decided. Until then: **defer.**

---

## Finding 4 — FDA reassessing BHA → precautionary penalty

**Recommendation: WATCH (Low priority; optional cheap add only if the F1 named-additive taxonomy is built)**

**Scope tension is the core issue.** BSIP2 is explicitly a *food-structure / nutritional-architecture* framework, not a toxicology engine (`matrix_integrity_framework.md` "What matrix integrity is not"; `beneficial_processing.md`). Single-chemical precautionary safety flags sit at the edge of its remit. The current additive taxonomy has **no preservative/antioxidant category at all** — BHA is invisible today.

**Other concerns:**
- **Evidence is regulatory, not outcome.** NTP animal designation; human carcinogenicity not established; dietary-dose extrapolation contested (Watch grade: Medium).
- **Maintenance/rule-budget cost.** "Escalate the penalty if GRAS is revoked post-2026" implies a *regulatory-status-tracking subsystem* — recurring maintenance and a slippery slope toward per-chemical rules (Tension 5 rule explosion).
- **The finding is already partly stale.** As of today (2026-06-01) the FDA comment deadline (Apr 13 2026) has passed, and the "GRAS overhaul proposed rule expected spring 2026" should be checked for an actual outcome before any rule work. Re-verify status before acting.

**If acted on:** the *cheap* path is to piggyback on the named-additive lookup built for F1 — add BHA (and explicitly differentiate BHT, which is **not** under reassessment) as a small named-additive penalty within the existing additive/processing dimension. Do **not** build regulatory-status tracking. Otherwise, hold as a monitoring item and revisit when the GRAS rule lands.

---

## Finding 5 — Sucralose vs. stevia transgenerational mouse study

**Recommendation: NO CHANGE (agree with the Watch)**

The Watch correctly self-classifies this as monitoring-only. Mouse model, supra-physiological doses, unclear transgenerational mechanism, contradicted by human RCTs at physiological doses. BSIP2 already treats sweeteners as high-signal-weight (−8 to additive quality + an independent SWEETENER_PRESENT cap of 70, listed as an *architectural commitment* in `score_resolution_contract.md`). No calibration change is warranted. Re-evaluate only on a human RCT with consistent findings.

---

## Regulatory note — EFSA mandatory FAIM tool (effective July 2026)

**No BSIP2 scoring action.** FAIM governs *exposure-assessment methodology in EU additive authorization dossiers* — it is not an input to product-level scoring. It is a useful **leading indicator** that EFSA is tightening additive scrutiny (which may surface future findings), but it changes nothing in the scorer today. Monitoring only.

---

## Summary & recommended sequencing

| Finding | Watch priority | **This eval** | Rationale |
|---|---|---|---|
| F2 — Protein-bar matrix discount | High | **ADOPT (High)** | Best evidence (n=1,641, validated DIAAS) + best fit; closes a *documented* gaming hole; fits penalty architecture |
| F1 — Emulsifier tiering | High | **ADAPT (Med-High)** | Directionally right *both ways* (also fixes lecithin over-penalty); single RCT → modest deltas; needs named-additive metadata |
| F4 — BHA flag | Medium | **WATCH (Low)** | Toxicology = scope edge; regulatory-only evidence; partly stale; cheap only if F1 taxonomy exists |
| F3 — Fiber-diversity bonus | Medium | **DEFER** | In-vitro only; **opens** a gaming path F2 closes; requires not-yet-decided positive-signal architecture |
| F5 — Sucralose mouse study | No change | **NO CHANGE** | Agree — monitoring only |
| EFSA FAIM note | — | **NO ACTION** | Methodology change for EU dossiers, not a scoring input |

**Recommended sequencing:**
1. **Build the named-additive + ingredient-fragmentation taxonomy** (`matrix_integrity_framework.md` Requirement 1). This is the enabling infrastructure, not a finding-specific patch.
2. On that base, ship **F2 (protein-bar matrix discount + collagen marker)** — highest payoff, closes the canonical gaming hole.
3. Then ship **F1 (identity-modulated emulsifier/stabilizer weights)**, reusing the taxonomy; optionally fold in **F4 (BHA named penalty)** at near-zero marginal cost.
4. **Defer F3**; revisit only with whole-food-source gating + a decision on positive signals (Tension 4).

**Two cross-cutting guardrails for whoever implements this:**
- **Respect the rule budget (Tension 5).** Prefer modulating *existing* dimension/penalty weights over adding standalone caps. F1, F2, and F4 can all be expressed as weight modulations on existing mechanisms.
- **Watch the F2↔F3 interaction.** They pull in opposite directions on the same product class (reconstructed bars). Implementing F3 naively would partially undo F2. This is the strongest reason to defer F3 until it can be made matrix-aware.
