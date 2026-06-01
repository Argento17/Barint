# BSIP-S Principles v1
# Bari Supplement Intelligence Protocol — Foundational Architecture
**Date:** 2026-05-30
**Status:** Design Document v1
**Scope:** Architecture rationale, core principles, protocol boundaries

---

## Section 1 — Why BSIP-S Cannot Be BSIP2

BSIP2 was designed to evaluate food. Its entire scoring machinery assumes:

- **NOVA processing level** as a quality proxy (supplements have no meaningful NOVA level — all are industrially processed by definition)
- **Sugar, sodium, and saturated fat** as guardrail signals (irrelevant for capsule, tablet, and most powder formats)
- **Calorie density tables** per food category (caloric irrelevance in therapeutic supplement doses)
- **Ingredient count** as a complexity penalty (a supplement with 12 active ingredients may be more valuable than one with 2)
- **Israeli red label thresholds** (consumer food labeling law; does not govern supplements)
- **Fermentation as a quality signal** (the fermentation bonus in food is about microbial activity preserving the original food; in supplements, fermentation is strain-specific and requires separate treatment)

Forcing supplements through BSIP2 would produce numerically similar scores to food scores while measuring entirely different phenomena. A magnesium glycinate scored by BSIP2 would be penalized for being "ultra-processed" and rewarded for having no fiber — neither signal is meaningful.

**Verdict: BSIP-S is required. BSIP2 cannot be extended to serve this domain.**

---

## Section 2 — What BSIP-S Evaluates

BSIP-S answers one central consumer question:

> **"Is this product delivering what it claims to deliver, in a form and dose that has scientific support, with enough transparency to trust?"**

This question has four distinct components:
1. **Does the evidence support this supplement type for the intended use?** (Evidence Tier — category-level)
2. **Is the dose in the range where the evidence shows an effect?** (Dose Adequacy — product-level)
3. **Is the ingredient form the one that actually absorbs?** (Form Quality — product-level)
4. **Can we verify what's on the label?** (Transparency — product-level)

Everything else in BSIP-S serves these four components.

---

## Section 3 — What BSIP-S Cannot Evaluate

These are hard boundaries. Bari does not cross them.

| Cannot Evaluate | Reason |
|---|---|
| Whether this supplement will work for any individual | Individual pharmacokinetics, baseline levels, health status — all unknown |
| Whether a person needs this supplement | Requires blood work, clinical assessment |
| Disease treatment or prevention claims | Medical claim territory; regulatory prohibition |
| Long-term safety beyond known ULs | Insufficient evidence; individual variation |
| Supplement interactions with medications | Requires clinical knowledge of patient's drug regimen |
| Taste, texture, or sensory quality | Not a quality signal for therapeutic intent |
| Price-to-value optimization | Out of scope for scoring; may appear as supplementary consumer note |
| Bioavailability in the context of specific gut conditions | Individual clinical variation |

**Every BSIP-S output must include a transparency note clarifying that scores do not constitute medical advice and do not substitute for clinical assessment of individual need.**

---

## Section 4 — Core Principles

**P-01: Evidence Primacy**
The evidence base for a supplement category is assessed before any individual product. A product in a category with weak evidence cannot earn a high BSIP-S score regardless of formulation quality. A well-formulated product in a poorly-evidenced category is still a well-formulated product in a poorly-evidenced category.

**P-02: Dose Honesty**
A supplement that provides 10% of the dose used in clinical trials is not meaningfully different from a placebo for that use case. Dose adequacy is the single highest-weight scoring dimension. Underdosing is the most common form of supplement deception.

**P-03: Form Is Not Interchangeable**
Magnesium oxide and magnesium glycinate are not the same supplement at the same dose. Vitamin D2 and D3 are not equivalent. Creatine HCl and creatine monohydrate are not proven equivalent. Ingredient form determines actual bioavailability and must be evaluated independently of dose.

**P-04: Transparency as Quality Signal**
A proprietary blend that lists "Proprietary Mineral Complex 500mg" without individual ingredient amounts cannot be assessed for dose adequacy. The inability to verify is itself a quality failure. Opaque formulations receive structural penalties regardless of claimed benefits.

**P-05: Category Independence**
Magnesium is not evaluated like creatine. Probiotics are not evaluated like vitamin D. Each category has a distinct evidence tier, distinct reference dose range, distinct form hierarchy, and distinct common distortions. Cross-category score comparisons are not valid.

**P-06: Safety Is a Hard Override**
Doses exceeding established Upper Tolerable Intake Levels (ULs) trigger hard score caps regardless of formulation quality. A product that could cause harm cannot receive a high BSIP-S score. Safety flags are non-negotiable and mandatory disclosure items.

**P-07: Claim Integrity Is Evaluated Independently**
A product's label claims are assessed against its actual formula. A product may have an excellent formulation but make unsupported claims about it, or a weak formulation making technically accurate but misleading claims. Claim integrity is a separate scoring dimension, not collapsed into formulation quality.

**P-08: Framework Invisibility**
Consumer outputs never mention Evidence Tiers, dimension names, BSIP-S mechanics, or technical scoring terminology. The score and grade appear. Insights appear as observations. The framework is invisible.

**P-09: Confidence Levels Are Mandatory**
Every BSIP-S score carries a confidence designation:
- **Verified**: All key dimensions observable from label; third-party confirmation present
- **Partial**: Core dimensions assessable; some data missing (e.g., form not specified, no third-party test)
- **Insufficient**: Critical data unavailable (e.g., proprietary blend, no ingredient amounts)

Insufficient-confidence products display a floor score only, not a gradient assessment.

**P-10: Humility at Scale**
Supplement science is active and contested. Evidence tiers assigned in v1 will need revision as research evolves. Category frameworks include versioning. Scores should improve with evidence, not lock in at design time.

---

## Section 5 — Protocol Relationship to BSIP2

| Dimension | BSIP2 | BSIP-S |
|---|---|---|
| Primary quality signal | NOVA processing level | Evidence tier + dose adequacy |
| Worst-formulation signal | Ultra-processed (NOVA4) | Proprietary blend / insufficient dose |
| Guardrail system | Sugar, sodium, calorie, processing caps | Dose ceiling (UL), safety override |
| Category-specific tuning | Calorie density tables per food format | Form hierarchy + reference dose per category |
| Data source | Retailer nutritional panel + ingredients | Supplement facts panel + certifications |
| Label claims evaluation | Israeli red label compliance | Claim category × evidence × dose match |
| Score range | 0–100 → letter grade | 0–100 → letter grade (same display) |
| Consumer output | Insight line + expansion panel | Insight line + expansion panel (same format) |
| NOVA signal | Central | Absent |
| Fermentation | Direct score bonus | Strain-specific, probiotic category only |

The consumer output format is compatible. The scoring engine is entirely separate.

---

## Section 6 — Protocol Versioning

**BSIP-S v1 scope:** 8 categories (Magnesium, Vitamin D, Multivitamins, Fish Oil, Creatine, Protein Powder, Probiotics, Sleep Supplements).

**Evidence tier assignments** are locked at v1 for the 8 initial categories. Tier changes require a documented category review with evidence citations.

**Reference dose ranges** are sourced from: NIH Office of Dietary Supplements, Examine.com systematic synthesis, European EFSA opinions, and category-specific RCT literature. All ranges documented in `bsip_s_category_framework_v1.md`.

**Form hierarchies** are sourced from comparative bioavailability studies and pharmacokinetic literature. Form hierarchy changes require a documented evidence update.
