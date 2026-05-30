# BSIP2 Concept v1 — Conceptual Architecture Freeze

**Freeze date:** 2026-05-17
**Status:** Conceptual architecture freeze — NOT production scoring
**Version:** bsip2_concept_v1

---

## What this freeze is

This freeze captures the BSIP2 analytical architecture at the point where its conceptual foundations are sufficiently developed to serve as a design and specification baseline. It documents how Bari evaluates food products across eleven analytical dimensions, how scoring is structured, how concern coordination prevents double-counting, and how the user interface should communicate results.

This is a **conceptual freeze**, not an implementation freeze. It means:

- The architectural decisions documented here are stable enough to build against
- The scoring formulas are defined but **thresholds remain experimental** — specific numeric cutoffs will be calibrated against real product data
- The dimension weights are directionally correct but subject to empirical adjustment
- No production scoring code is frozen here; only the conceptual specification

---

## What this freeze is NOT

- Not a production scoring system
- Not a validated nutritional assessment tool
- Not a clinical or regulatory instrument
- Not a final specification; it is the first stable design baseline

---

## Contents

| File | What it documents |
|------|------------------|
| `methodology.md` | Six-stage scoring pipeline; eleven dimensions with weights; grade table (A–E) |
| `signal_system.md` | Five signal groups; ingredient marker taxonomy; NOVA classification proxy |
| `processing_analysis.md` | NOVA level inference; additive burden rules; four hyper-palatability patterns |
| `category_analysis.md` | Eight product categories; category-specific calorie density threshold tables; whole-food floor rules |
| `confidence_framework.md` | Confidence calculation; data quality reductions; confidence bands; score ceilings by band |
| `comparison_logic.md` | How products are ranked; grade as comparison frame; where score gaps come from; tradeoff evaluation |
| `ui_language.md` | Signal labels; grade language; what not to say; hyper-palatability framing; tone guide |
| `docs/scoring/concern_coordination_contract.md` | How BSIP2 prevents the same root concern from reducing the score more than once; all concern families; family budget reference |

---

## Architectural decisions that are stable

The following design decisions are settled and should not be revisited without a documented rationale:

1. **Concern coordination before family budget clamping.** Caps and penalties are grouped by root concern and resolved (strictest cap wins; largest penalty wins at full value, others at supporting factor) before budget limits are applied. This ordering is intentional.

2. **SWEETENER_PRESENT is outside the CONCERNS graph.** Sweetener substitution is structurally independent of ultra-processing. A NOVA 1 product can carry a sweetener; coordination with NOVA caps would be architecturally incorrect.

3. **Confidence is a separate ceiling, not a concern family.** Data reliability and food quality are orthogonal. Confidence ceilings run after all guardrail coordination completes.

4. **Category-relative calorie evaluation.** A walnut and a snack bar are not evaluated against the same calorie density table. Category context is not optional.

5. **Whole-food floors protect single-ingredient NOVA 1 products.** The analytical engine cannot produce an absurd result for a plain walnut. The floor (75) is a philosophical commitment, not a numerical convenience.

6. **BSIP2 does not make personalised recommendations.** The score answers a structural analytical question about what a product contains and delivers. Suitability for any individual is out of scope.

---

## What remains experimental

- Specific numeric thresholds (e.g. the exact kcal cutoffs in the calorie interaction rules)
- Dimension weights (currently direction-correct; not empirically calibrated)
- Supporting evidence factors (0.4 and 0.5 values — reasonable but untested at scale)
- Category classification keyword lists and confidence scoring
- NOVA proxy classification reliability at scale
- Hyper-palatability pattern thresholds

---

## Intended use of this freeze

This freeze is the reference baseline for:
- Adversarial validation and edge-case testing (see `C:\Bari\bisp2_concept_v1\validation\`)
- Frontend and design language development
- BSIP2 implementation specification
- Future concept evolution — changes should be documented against this baseline

Anyone reviewing a future BSIP2 version should be able to read this freeze and understand what changed and why.

---

## Relationship to BSIP1

BSIP1 (canonicalization layer, frozen at `C:\Bari\bsip1_concept\freezes\bsip1_v0_1\`) produces compact product records that serve as the primary input to BSIP2. BSIP2 does not re-do BSIP1 work — it receives canonicalized nutritional fields, ingredient text, NOVA signals, and barcode trust metadata and applies the analytical scoring engine defined in this specification.

BSIP1 trust level is an input signal to BSIP2 analytical confidence. A BSIP1 low-trust product receives reduced analytical confidence in BSIP2.
