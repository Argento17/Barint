# Positive Structure Integration Options

**Status:** Design document — architecture decision analysis. No implementation decisions are made here.  
**Purpose:** Rigorously analyze four architectural options for integrating positive structure signals into the BSIP2 scoring pipeline.  
**Constraint:** The analysis must not weaken the low-end punishment architecture. Any option that materially lifts scores for highly engineered products at the bottom of the distribution is disqualified.

---

## The integration problem

Positive structure signals have been defined in companion documents. The architectural question is not what to measure but *where in the scoring pipeline* the measurement exerts influence — and whether that position produces genuine expressiveness for structurally strong products without creating side effects.

The current pipeline is:
```
Dimension scores → Weighted average (WDS) → Caps → Penalties → Floors → Confidence ceiling → Final score
```

Positive structure can, in principle, be inserted at:
1. **Within WDS** — as one or more scoring dimensions (Option A)
2. **At Floors** — as a floor condition based on structural signals (Option B)
3. **At Caps** — as a cap modifier that relaxes the binding cap based on structural quality (Option C)
4. **Hybrid** — combination of the above (Option D)

The diagnostic established the core problem: WDS contributions from structural dimensions are overwhelmed by cap magnitude. A 10-point positive structure ceiling (combining satiety_support + whole_food_integrity at max) cannot overcome a cap bite potential of 15–30 points. Any integration option must address this asymmetry, not just add more points to a pre-cap calculation.

---

## Option A: Dedicated weighted dimension

**Description:**  
Replace or augment the existing `satiety_support` and `whole_food_integrity` dimensions with a new `structural_integrity` dimension (or `matrix_coherence` dimension) carrying a weight of 0.10–0.15. This dimension receives a score based on the composite positive structure signals.

**Mechanism:**  
- Structural signals (intact matrix, structural fiber, source-quality protein, macro coherence) compute to a 0–100 dimension score
- The dimension is weighted into WDS alongside the existing 10 dimensions
- Products with high structural scores gain WDS points that flow through the cap layer

**Benefits:**
- Architecturally familiar — fits the existing dimension framework without structural changes
- Fully transparent in the trace — every product shows its structural dimension score and contribution
- Calibration is straightforward — the weight determines influence, and weight can be adjusted independently
- Explainable at the product level — "This product's structural quality score is X because of Y"

**Risks:**

*Risk 1: Pre-cap neutralization.* This is the fundamental flaw inherited from the current architecture. If a product's WDS rises by 8 points from a new structural dimension, but it is capped at 60, the 8-point improvement does nothing if the product's WDS was already below 60. The diagnostic showed that 46/48 products have WDS below their binding cap. For these products, a new weighted dimension provides zero upward expressiveness. It only helps the 2 products whose WDS already exceeds the cap — and for those products, a higher WDS is immediately shaved back to the cap.

*Risk 2: Gaming through individual signal optimization.* A dedicated dimension with a known weight creates a clear optimization target. Manufacturers can add isolated elements that score well on individual structural signals — add some inulin for "fiber context," use "concentrate" instead of "isolate" labeling, keep the ingredient count low — and capture scoring gains without genuine structural improvement. The compound signal design reduces but does not eliminate this risk.

*Risk 3: Calibration sensitivity.* If the weight is too low (<0.08), the dimension is decorative — it won't produce meaningful separation. If the weight is too high (>0.18), it may distort the overall scoring calibration and interact unpredictably with the cap system.

**Gaming resistance: Low-medium.** Individual signals within the dimension are gameable; the compound assessment reduces but doesn't eliminate gaming.

**Explainability: High.** The dimension score is a first-class output, visible in the trace.

**Calibration complexity: Low.** Weight is a single parameter; dimension formula can be adjusted independently.

**Interaction with existing architecture: Additive.** Does not change cap or penalty logic. Clean separation of concerns.

**Expressiveness for structurally strong products: Low.** Does not solve the pre-cap neutralization problem. Products already below their cap gain nothing from a higher WDS.

**Verdict:** Architecturally clean but fails the core expressiveness requirement. Does not address the root cause identified in the diagnostic.

---

## Option B: Structural floor system expansion

**Description:**  
Extend the existing SRC-01 floor mechanism to cover more product types, using positive structure signals as floor eligibility conditions. Instead of only protecting NOVA 1 single-ingredient products and `whole_food_fat` NOVA 1–2 products, define structural floors for additional product types when they meet compound structural integrity conditions.

**Mechanism:**  
Define new floor rules based on compound conditions. Hypothetical examples (for design illustration, not calibrated):

```
STRUCTURAL_INTEGRITY_FLOOR_SNACKBAR:
  Condition: category = snack_bar_granola
             AND nova_proxy <= 3
             AND structural_fiber_presence = True
             AND source_quality_protein IN (whole_food, mechanically_transformed)
             AND macro_coherence_index >= HIGH
             AND ingredient_simplicity >= 5 whole_food_primary_ingredients
  Floor value: 48
  Class: B (physiological caps can override)

STRUCTURAL_INTEGRITY_FLOOR_CEREAL:
  Condition: category = cereal
             AND nova_proxy <= 3
             AND structural_fiber_presence = True
             AND whole_grain_confirmed = True
             AND no_isolated_sweetener_system
  Floor value: 45
  Class: B
```

Products meeting these compound conditions would receive a minimum score guarantee, expressing structural quality as an explicit upward protection rather than an implicit absence-of-penalties benefit.

**Benefits:**
- Directly solves the expressiveness problem for eligible products — floor guarantees a minimum score regardless of pre-existing cap compression
- Compound eligibility conditions are substantially gaming-resistant — a product must satisfy all conditions simultaneously
- Architecturally coherent with the existing SRC-01 framework — extends rather than replaces
- Transparent and auditable — floor application is explicitly logged in the trace
- Self-limiting direction — only raises scores, never lowers them; cannot worsen the low end

**Risks:**

*Risk 1: Cliff effects.* Discrete floors create sharp score boundaries. A product scoring 47 that just barely misses the STRUCTURAL_INTEGRITY_FLOOR at 48 is rated below a product at 48.0 that just qualifies. This is the characteristic failure of threshold-based rules — continuous reality mapped to discrete gates.

*Risk 2: Eligibility misclassification.* Products near the boundary of eligibility conditions will produce borderline cases. Category instability (already observed in 9/53 products) means a product might qualify for the floor as snack_bar_granola but not as cereal. Mis-categorization creates unintended floor activation.

*Risk 3: Condition gaming requires understanding eligibility rules.* If the specific compound conditions become known, manufacturers can optimize to meet them — ensuring nova_proxy <= 3, adding enough structural fiber sources to trigger `structural_fiber_presence`, using whole-food protein sources in primary positions. This is harder than gaming a dimension score but not impossible with deep knowledge of the detection system.

*Risk 4: Floor values need calibration.* What should a `STRUCTURAL_INTEGRITY_FLOOR_SNACKBAR` floor value be? Too high (50) and it elevates too many products. Too low (40) and it provides no practical benefit since most qualifying products already score above that. Calibration requires dataset analysis.

**Gaming resistance: Medium-high.** Compound conditions are substantially harder to game than individual dimension signals. Each additional condition requirement narrows the gaming surface.

**Explainability: High.** "This product meets the criteria for a structural integrity floor because [condition list]." Discrete, auditable.

**Calibration complexity: Medium.** Condition thresholds and floor values require calibration against the full distribution. Addition of new product types requires new condition design.

**Interaction with existing architecture: Integrative.** Works within SRC-01 framework. New floor rules interact with the existing Class A/B classification (physiological caps can still override structural floors for products with genuine concerns).

**Expressiveness for structurally strong products: High.** Directly guarantees minimum scores for eligible products regardless of cap compression. This is the mechanism that could actually separate structurally strong snack bars upward.

**Verdict:** Most promising mechanism for achieving genuine expressiveness. High gaming resistance due to compound conditions. Cliff effects are a limitation but manageable.

---

## Option C: Cap moderation based on structural integrity

**Description:**  
Products with strong positive structural signals receive a cap relaxation — their binding cap is increased by some amount, allowing structurally superior products to express their WDS advantage in the final score.

**Mechanism:**  
Define a structural quality score (composite of positive structure signals) that, when it exceeds a threshold, modifies the cap value applied to the product.

Hypothetical mechanism (for design illustration):

```
IF structural_quality_score >= HIGH
   AND binding_cap comes from processing_load family (NOVA 3 or 4 cap)
   AND the binding_cap source is NOT a physiological concern cap (sugar, fat, sodium)
THEN
   relaxed_cap = binding_cap + cap_relaxation_amount
   (where cap_relaxation_amount might be 5–10 points)
```

The key design constraint: only processing-load caps should be subject to structural moderation. Sugar, sodium, and sat_fat caps represent genuine physiological concerns — those caps must remain unconditional. The NOVA 3 cap (75) and NOVA 4 cap (60) are processing proxies — they impose ceilings based on inferred processing level rather than specific nutritional concerns. These are the appropriate targets for structural quality moderation.

**Benefits:**
- Directly addresses the root cause identified in the diagnostic — cap application is currently blind to structural quality; this option specifically fixes that
- Self-limiting: only benefits products whose structural quality score is above the threshold AND whose binding cap is a processing-load cap AND whose WDS is above the relaxed cap — a very narrow window that only genuinely strong products reach
- Does not inflate the bottom: products with very low WDS (e.g., 22–35) are so far below any cap that cap relaxation has no effect on them
- Mechanically elegant: cap relaxation can be implemented as a single modification to the cap computation step

**Risks:**

*Risk 1: Explainability challenge.* "Your product received a cap exception because of its structural quality" is conceptually justifiable but architecturally complex to explain. A consumer or operator sees the final score without necessarily understanding why this product got a higher cap than a similarly-classified product. This is the most significant explainability risk.

*Risk 2: Cap structure dependency.* The mechanism depends on the processing_load cap being the binding cap. If the binding cap is a sugar cap (45–55) — which is common for high-sugar snack bars — cap relaxation on the processing-load cap does nothing because a different family's cap is binding. The mechanism only helps products where the processing cap is the sole or primary binding constraint.

*Risk 3: Gaming requires both structural signal gaming AND placing product in the processing-load cap range.* This is actually a gaming-resistance advantage — a product cannot reach this relaxation unless it is genuinely in the NOVA 3 range (processing cap is binding) AND genuinely has structural quality signals. Engineered products designed to score NOVA 3 specifically to get a 75 cap rather than a 60 cap are already exploiting NOVA, not this mechanism.

*Risk 4: Interaction with concern family coordination.* The concern family coordination framework assumes caps are fixed for each family. Modifying caps conditionally introduces complexity into the coordination logic — the binding cap determination must account for potential structural relaxations across families before resolving the final binding cap.

**Gaming resistance: Low individually, high in practice.**  
Gaming this mechanism requires: achieving structural signals that activate the relaxation, having a product whose binding cap is processing-load-derived, and having WDS above the relaxed cap. The intersection of these three requirements is narrow and difficult to engineer simultaneously. In practice: a protein bar manufacturer who adds structural signals will also likely trigger satiety quality detection that reveals the isolate-based construction; the signals needed to activate cap relaxation and the signals that expose reconstruction are partially the same.

**Explainability: Medium.**  
The relaxation can be surfaced in the trace explicitly ("processing cap relaxed from 75 to 83 due to structural quality signal"). But the reasoning — "why does structural quality change the cap?" — requires a conceptual framework to communicate.

**Calibration complexity: High.**  
The relaxation amount must be calibrated carefully. Too small (<5 pts) and it produces no meaningful separation. Too large (>15 pts) and it creates a scoring discontinuity between qualifying and non-qualifying products. Calibration requires analysis of where the NOVA 3 cap is binding for genuinely structured products vs. genuinely engineered ones.

**Interaction with existing architecture: Moderate disruption.**  
Requires modification to the cap evaluation step. The concern family coordination framework must be aware of conditional caps. This is a more invasive architectural change than Options A or B.

**Expressiveness for structurally strong products: Very high — when applicable.**  
For products where the processing cap is genuinely the binding constraint and structural quality is genuinely high, this mechanism provides the most direct path to upward score separation. But the eligibility criteria make it applicable to a narrower set of products than Option B.

**Verdict:** Architecturally the most targeted solution to the identified root cause. Explainability is the primary weakness. Gaming resistance is higher than it initially appears due to compound signal requirements.

---

## Option D: Hybrid architecture

**Description:**  
Combine elements of Options B and C, with a small supporting Option A component:

- **Primary mechanism:** Structural floor expansion (Option B) with compound eligibility conditions — provides guaranteed minimum scores for clearly-qualifying products
- **Secondary mechanism:** Processing-load cap moderation (Option C) for products with very strong structural signals — provides upward expressiveness beyond floor for the strongest products
- **Supporting mechanism:** A lightweight structural coherence indicator in the dimension layer (Option A, weight 0.06–0.08) — not the primary expressiveness vehicle but provides continuous signal visibility in the trace

**Mechanism sketch:**

```
Scoring pipeline with structural integration:

1. Compute structural quality signals (L3/L4): 
   structural_fiber_presence, source_quality_protein, 
   macro_coherence_index, fermentation_credit, ingredient_simplicity_positive

2. Compute structural quality grade:
   - STRONG: 4–5 signals active (compound)
   - MODERATE: 2–3 signals active
   - WEAK: 0–1 signals active

3. Dimension layer:
   - Replace whole_food_integrity (0.04) + satiety_support (0.06) 
     with structural_coherence (0.10) weighted dimension
   - structural_coherence score is source-aware (uses quality factors)

4. Cap layer:
   IF structural_quality_grade = STRONG
   AND binding_cap source = processing_load
   AND cap_value is NOVA_PROXY_3 or NOVA_PROXY_4
   THEN cap_relaxation = 8 (design-stage estimate)

5. Floor layer:
   IF structural_quality_grade = MODERATE or STRONG
   AND category = snack_bar_granola or cereal
   AND nova_proxy <= 3
   THEN structural_floor applies (value TBD in calibration)

6. Existing floor hierarchy (SRC-01) remains unchanged and takes precedence
```

**Benefits:**
- Three mechanisms operating at different pipeline positions provides defense in depth — even if one mechanism doesn't apply (e.g., processing cap isn't binding), another may
- The compound signal requirement for STRONG grade creates the most gaming-resistant path to structural benefit
- The supporting dimension layer provides continuous visibility for all products, not just those meeting the compound threshold
- The floor and cap mechanisms provide discrete step-changes for genuinely qualifying products that the dimension layer alone cannot deliver

**Risks:**

*Risk 1: Architectural complexity.* Three concurrent mechanisms interacting with the existing pipeline creates more potential for unexpected interactions. The trace must capture each mechanism's contribution separately.

*Risk 2: Calibration burden.* Three mechanisms with independent parameters require coordinated calibration. The floor value, the cap relaxation amount, and the dimension weight interact — the total structural quality uplift for a STRONG product could range from modest to large depending on how all three operate in combination.

*Risk 3: Overlapping mechanisms may double-credit the same signals.* If the same structural signals feed the dimension layer AND the floor trigger AND the cap relaxation, a product might gain points three times from the same underlying quality. The architecture must ensure that structural signals influence only one mechanism at a time, or that the combined effect is bounded.

*Risk 4: Calibration phasing.* The compound signals (L3/L4 level) are not yet implemented. Building a three-mechanism hybrid on unimplemented signals is premature. The architecture should be designed now but implemented incrementally.

**Gaming resistance: Low (WEAK grade), High (STRONG grade).**  
The tiered grade structure means that minor gaming (adding a few structural-looking signals) produces a WEAK grade that activates only the dimension layer — minimal benefit. Reaching STRONG grade requires satisfying 4–5 compound conditions simultaneously — high resistance.

**Explainability: Medium.**  
Three mechanisms operating together is harder to explain than any single mechanism. The trace must surface each mechanism's contribution clearly. Consumer-facing explanation should aggregate: "This product has strong structural integrity" rather than describing all three mechanisms.

**Calibration complexity: High.**  
Three-mechanism calibration requires coordination. Recommended approach: calibrate Option B first (floors), then add Option C (cap moderation) for the highest-integrity products, then assess whether Option A dimension layer adds value or just complexity.

**Interaction with existing architecture: Significant.**  
Replaces two existing dimensions (whole_food_integrity, satiety_support), modifies cap computation, and extends floor logic. This is the most invasive option architecturally.

**Expressiveness for structurally strong products: Highest.**  
Provides expressiveness at three pipeline stages. A STRONG product that fails the floor condition (e.g., it already scores above the floor naturally) still benefits from cap relaxation and the dimension layer.

**Verdict:** The most complete solution and the most complex. Appropriate as a design target for a mature implementation, but should be implemented in phases (B first, then C, then A replacement). Not a first-deployment architecture.

---

## Comparative summary

| | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| **Root cause addressed** | No — pre-cap neutralization persists | Yes — floor bypasses cap | Yes — cap relaxed | Yes — all three |
| **Gaming resistance** | Low-medium | Medium-high | Medium-high (in practice) | High for STRONG grade |
| **Explainability** | High | High | Medium | Medium |
| **Calibration complexity** | Low | Medium | High | High |
| **Architecture disruption** | Low | Medium | Moderate | High |
| **Expressiveness for strong products** | Low | High | Very high (conditional) | Highest |
| **Risk of lifting engineered bottom** | Low | Low | Very low | Low |
| **Implementation readiness** | High | Medium | Medium | Low |

---

## Key design principle for any option

The following constraint applies to all options and must be preserved:

**Structural quality signals must require compound satisfaction.**  
No single positive structural signal should independently trigger scoring benefits. Benefits should require 2–4 signals to fire simultaneously. This is the primary gaming-resistance mechanism — individual signals can be gamed; compound requirement sets are substantially harder to fake simultaneously.

**Processing-load caps and physiological concern caps must be treated differently.**  
NOVA processing caps (60, 75) are processing proxies — they can appropriately be subject to structural quality moderation. Sugar, sodium, and saturated fat caps are physiological concern responses — they must remain unconditional regardless of structural quality. A product with excellent matrix integrity but 30g sugar per 100g still has 30g sugar per 100g.

**Structural quality cannot neutralize concern signals; it can only provide upward expressiveness in their absence.**  
If a product has both strong structural quality AND strong concern signals (high sugar, high sodium), the concern signals take precedence. Structural quality is additive in the absence of concerns; it is not a concern override.

---

## Recommendation for next phase

**This decision document does not choose.** The choice requires:
1. A calibration dataset analysis to determine where current products fall relative to proposed thresholds
2. A golden product suite assessment (see `validation/golden_products_suite.md`) to verify that proposed options produce correct ranking behavior
3. A gaming stress test — deliberate analysis of which products a manufacturer could construct to exploit each option

**If forced to sequence:** Implement Option B first. The floor expansion is the most architecturally contained, most explainable, and most gaming-resistant option. It addresses the expressiveness problem for the most clearly-qualifying products. Option C (cap moderation) is the most powerful mechanism but requires more careful calibration. Option A (new dimension) is the least effective at solving the root cause and should only be implemented as a supporting signal layer after Options B or C are functioning.

**What must not happen:** Implementing Option A alone as the response to the positive structure diagnostic. The diagnostic identified that pre-cap neutralization is the root cause of weak expressiveness. Option A does not solve pre-cap neutralization. Implementing Option A alone would be a well-intentioned architectural non-answer.
