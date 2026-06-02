# Bari Consumer Use-Case & Purpose Guardrails v2

**Classification:** Governing Framework — Internal  
**Issued:** 2026-05-29  
**Author:** CE Controller 1 — Chief Nutrition, Scoring & Content Architect  
**Status:** Active — replaces Purpose Framework v1 in all applications  
**Supersedes:** Product Purpose Framework v1 (`product_purpose_framework_v1.md`) — rejected  
**Governed by:** Bari Governance v1, Bari Comparison Governance Constitution v1

---

## 1. Executive Summary

Purpose Framework v1 was built around a category error: it treated purpose as a stable, detectable property of a product. Purpose is not a product property. It is a relational property between a product and a consumer. That error invalidated the seven-class taxonomy, the detection methodology, and the upstream classification architecture built on top of it.

This document does not rebuild what failed. It establishes a smaller, more defensible set of guardrails that do the work purpose reasoning is actually needed for: protecting comparison validity, enabling marketing divergence findings, and ensuring that contextualizing a score never becomes excusing a score.

**What this document is:**  
A set of comparison-time guardrails. Three broad comparison lenses. One standard finding type. One hard anti-immunity rule.

**What this document is not:**  
A product classification system. A taxonomy. A BSIP layer. An architecture.

**Core position:** Consumer use-case reasoning belongs at the moment of comparison, applied to the specific decision between two specific products in front of a specific consumer. It does not belong upstream, attached to every product, as a permanent classification.

The one provision that Framework v1 produced that survives fully: the marketing divergence finding. When a product's claims exceed what its architecture can support, Bari should say so. That finding requires no taxonomy. It requires evidence and editorial will.

---

## 2. Findings

**Finding 1 — The failure of v1 was not in the insight. It was in the architecture.**  
The insight behind Framework v1 was correct: consumers on the same shelf may be making different decisions, and Bari's comparisons must respect that. The error was operationalizing this insight as an upstream product classification system. The insight survives. The architecture is abandoned.

**Finding 2 — Consumer use-case is genuinely unknowable from product data alone.**  
No combination of protein content, ingredient list, and brand name reliably predicts why a specific consumer bought a product. The same plain yogurt is a protein source for one consumer and a cooking ingredient for another. A framework built on detecting consumer use-case from product data was always inferring something the data cannot fully contain.

**Finding 3 — Three things can be known. One cannot.**  
From product data, Bari can observe: the product's nutritional architecture (what is in it), the manufacturer's claimed purpose (what they say it is), and the comparison context (what products it is being placed alongside). What Bari cannot observe is the consumer's actual use-case. This document governs how to use the three observable things while acknowledging the limits of the fourth.

**Finding 4 — The Comparison Governance Constitution already solved most of the problem.**  
The Constitution's eligibility framework already prohibits comparing meal replacements against snacks, supplements against food, children's products against adult products, and clinical nutrition against retail food. These absolute restrictions handle the cases where purpose divergence is so material that no comparison is valid. The remaining cases — protein pudding vs. regular pudding, keto bread vs. whole wheat — are better handled by comparison-time caveats than by upstream classification.

**Finding 5 — Marketing divergence is the highest-value analytical output.**  
The most useful thing purpose reasoning produces is not a classification label. It is a finding: this product claims something its architecture cannot support. That finding is editorially tractable, independently valuable, and does not require a taxonomy to produce.

---

## 3. Why Purpose Framework v1 Failed

### 3.1 The Category Error

Framework v1 defined product purpose as "the primary dietary job a product is designed to do." The phrase "designed to do" reveals the error: the framework was analyzing designer intent, not consumer behavior.

A product's nutritional architecture reflects the manufacturer's design decisions. It does not determine what consumers use the product for. Plain yogurt is consumed as breakfast nutrition, as a cooking ingredient, as a post-workout protein source, and as a dessert substitute — by different consumers, in different contexts, for different reasons. The framework assigned it to Everyday Nutrition and called the classification ground truth. It was designer intent, presented as consumer reality.

**Lesson:** Bari must not conflate "what the product's composition implies" with "what consumers do with it." These are different claims with different evidentiary standards. Framework v1 collapsed them.

### 3.2 Taxonomy Instability

Seven classes at precise definitional boundaries produced instability exactly where it was most consequential. Greek yogurt (10g protein/100g) fell below the 15g/100g Macro Delivery threshold and was classified Everyday Nutrition — ignoring that Greek yogurt exists because of protein concentration via straining. Peanut butter simultaneously satisfied three purpose classes with equal evidence. Granola's marketing signaled Everyday Nutrition while its architecture signaled Indulgence. Eggs had no applicable classification at all because the framework's premise — that products are designed for purposes — breaks down for agricultural outputs.

In every unstable classification case, the product generating the instability was exactly the type of product that most needed purpose governance. The taxonomy was precise where products were simple and indeterminate where products were complex.

**Lesson:** A taxonomy that fails at its most important cases is not a useful taxonomy. A broader, coarser classification with fewer boundaries is more defensible than a fine-grained one with unstable edges.

### 3.3 Detection Circularity

The framework's detection methodology used threshold signals — "protein ≥15g/100g implies Macro Delivery" — derived from the taxonomy's own definitions. The detection validated the taxonomy and the taxonomy validated the detection. There was no external reference: no consumer research, no regulatory nutritional claim thresholds, no independent nutritional science basis for the specific thresholds chosen.

A detection system that can only produce the categories it was designed to produce is not detecting reality. It is applying a predetermined schema and reporting that it found what it was looking for.

**Lesson:** Detection thresholds require external validation to be meaningful. In the absence of external validation, stated thresholds are assertions, not findings.

### 3.4 Indulgence Immunity Risk

The framework's Indulgence class (Purpose Class 2) carried the provision that scoring an indulgence product poorly on protein and fiber would be "epistemological overreach." This reasoning, internally coherent, created a governance risk: any product with indulgent architecture could claim the Indulgence classification and receive editorial normalization of its low score.

The risk was not hypothetical. The logic of the framework — "evaluate a product within its purpose context" — is available to any manufacturer whose product genuinely qualifies as indulgent. The classification protects them from the comparison that would most accurately reveal their nutritional shortfall.

**Lesson:** A framework that can be legitimately exploited to produce the result a manufacturer would want is not a governance framework. It is a rationalization engine.

### 3.5 Overgeneralization from מעדנים

The Comparison Governance Constitution's finding — "purpose divergence is the default condition" — was generalized from the מעדנים category, where protein puddings, traditional chocolate desserts, children's snacks, and plant-based alternatives genuinely cohabit a highly heterogeneous shelf. That heterogeneity is real in מעדנים. It is not the default in bread (where most products compete for the same everyday consumer), in plain dairy (similarly homogeneous), or in fresh produce.

Framework v1 built a seven-class universal classification system to address a problem that is severe in some categories and minor in others. The architecture was calibrated to the hardest case.

**Lesson:** Frameworks designed for the exception case will be overcomplicated for the majority case. Build for the majority; add handling for exceptions. Do not invert the hierarchy.

---

## 4. Bari Consumer Use-Case & Purpose Guardrails v2

---

### SECTION 1 — The Corrected Conceptual Model

#### 1.1 Four Distinct Things

When Bari engages with the question of what a product is and what it is for, four distinct inputs are in play. These must not be conflated.

**Product architecture:**  
The observable nutritional reality of the product. What is in it. Protein content, sugar content, fiber content, processing level (NOVA proxy), ingredient list, additive count, serving size. This is Bari's primary data source. It is factual, quantifiable, and stable. It is what BSIP measures.

**Manufacturer claim:**  
What the producer states, implies, or markets about the product's purpose, function, or quality. This is observable (from product name, pack copy, claims). It is not factual — it is a commercial assertion. It is data to be evaluated against architecture, not an authority to be accepted.

**Consumer use-case:**  
What a specific consumer, in a specific moment, is using the product for. This is the actual purpose being served. It is relational: it depends on who the consumer is, what occasion they are planning for, what alternatives they considered, what nutritional intent they bring. It cannot be fully inferred from product data. Bari observes product architecture; it does not observe the consumer.

**Comparison context:**  
The decision frame in which two products are placed alongside each other. This is the specific context in which use-case reasoning is most relevant: not "what is this product for in general?" but "are these two specific products competing for the same consumer decision in this specific comparison?"

#### 1.2 Why Consumer Use-Case Is Relational

Consumer use-case is not a property of a product the way protein content is a property of a product. Protein content is the same regardless of who buys the product, when, or why. Consumer use-case changes with the consumer.

This is not a gap in Bari's data. It is a structural feature of the concept. A framework that treats consumer use-case as stably inferable from product architecture is not filling a data gap — it is making a category error.

**The consequence for governance:** Bari cannot classify products into consumer use-case buckets and treat those classifications as ground truth. Bari can observe architecture, evaluate claims against architecture, and identify — at comparison time — whether two products are plausibly serving the same consumer decision. That is all that use-case reasoning can defensibly support.

#### 1.3 Architecture Is Not Ground Truth of Purpose

Framework v1 elevated product architecture to the status of "ground truth" for purpose: "Nutritional purpose (what the product actually does) — GROUND TRUTH."

This was wrong for two reasons.

First, architecture reveals designer intent, not consumer reality. A protein yogurt engineered for macro delivery may be consumed as a dessert by consumers who purchase it for taste, not protein. The architecture is designed for one purpose; the consumer is using it for another. Neither is more "true" than the other for the consumer's decision.

Second, treating architecture as ground truth of purpose makes the marketing divergence finding circular. If architecture is ground truth, then any product whose architecture diverges from its claim is, by definition, making a false claim. But a product with 12g protein can legitimately claim to be "rich in protein" in some regulatory contexts even if it does not reach Bari's Macro Delivery threshold. Calling this a false claim requires an external standard, not an internally defined taxonomy.

**The corrected position:** Architecture is Bari's evidence base. Manufacturer claims are assertions to be evaluated. Consumer use-case is the relational context that governs comparison validity. No single one of these is ground truth. All three are inputs to interpretation.

---

### SECTION 2 — Comparison-Time Use-Case Framework

#### 2.1 When Bari Applies Use-Case Reasoning

Use-case reasoning is permitted in four specific situations and prohibited in all others.

**Permitted situation 1 — Comparison eligibility determination.**  
When constructing a comparison, Bari asks: are these two products plausibly competing for the same consumer decision? If a consumer choosing between Product A and Product B is making a single decision — "which of these do I want?" — the products are comparison-eligible. If a consumer would not rationally choose between these two products in a single decision moment, they are not comparison-eligible regardless of shelf co-location.

**Permitted situation 2 — Explaining divergent consumer decisions.**  
When a comparison involves products that are technically in the same category but serve different consumer decisions, use-case reasoning governs the disclosure. The disclosure states what decision each product is designed for, before any score is presented.

**Permitted situation 3 — Identifying marketing divergence findings.**  
When a product's manufacturer claim suggests one use-case and the product's architecture supports a different use-case, this divergence is a Bari finding. Use-case reasoning is used to identify and articulate the gap.

**Permitted situation 4 — Adding comparison caveats.**  
When a comparison is valid but carries a use-case qualification (products in the comparison serve partially overlapping but not identical decisions), use-case reasoning governs the caveat text.

#### 2.2 When Use-Case Reasoning Is Prohibited

Use-case reasoning is not permitted in the following situations:

**Prohibited 1 — To protect a product from its score.**  
A product's use-case does not reduce, normalize, or excuse its nutritional score. A product that scores 35/E in its category scores 35/E regardless of what it is designed for. The score is a statement about nutritional architecture. Use-case contextualizes what the score means; it does not change what the score is.

**Prohibited 2 — Before scoring.**  
Use-case reasoning happens at comparison time, after products have been scored. It is not an input to the scoring process. Scores are computed on a uniform basis; use-case reasoning governs how they are presented and compared, not how they are calculated.

**Prohibited 3 — To assign comparison immunity.**  
No use-case classification removes a product from all comparison. A keto bread is compared against other keto breads. A children's yogurt is compared against other children's yogurts. Use-case reasoning narrows the appropriate comparison pool; it does not eliminate the product from comparative analysis.

**Prohibited 4 — To rationalize a counterintuitive score.**  
If a product scores unexpectedly low or high, the response is to verify the score through the data and scoring architecture. It is not to apply a use-case classification that explains why the score is "correct given its purpose." That reasoning is post-hoc rationalization, which the critique identified as a critical failure mode.

---

### SECTION 3 — Three Comparison Lenses

These are not product identities. They are not permanent classifications. They are comparison-time lenses applied to specific pairs or groups of products at the moment a comparison is constructed.

A product does not "belong to" a lens. A comparison "uses" a lens.

---

**LENS 1 — GENERAL EVERYDAY CHOICE**

*The consumer decision:* The consumer is making a routine purchase for regular consumption in a standard eating context. They are not bringing a specific functional intent or a binding dietary restriction to the decision. They are choosing between products that they could reasonably substitute for each other in their normal eating pattern.

*Comparison behavior under this lens:*  
- Products are compared directly on nutritional architecture
- Score differences are interpreted as-is, using the standard meaningful threshold table from the Comparison Governance Constitution
- No use-case caveats are required unless a marketing divergence finding applies

*When this lens applies:*  
Default. If no evidence suggests that either product in a comparison is serving a targeted function or a binding restriction, this lens applies.

*Products that typically fall under this lens:*  
Plain dairy, standard bread, whole-food products, conventional snacks evaluated against each other, standard cereals, basic beverages. This lens covers the majority of comparisons in most categories.

*What this lens is not:*  
An endorsement that these products are nutritionally equivalent. Products under this lens still have meaningfully different scores. The lens only means they are competing for the same consumer decision.

---

**LENS 2 — TARGETED NUTRITIONAL FUNCTION**

*The consumer decision:* The consumer is seeking a specific nutritional outcome as the primary reason for purchase. The decision is not "which of these do I want for lunch?" but "which of these delivers the protein / fiber / probiotic function I came for?" The functional intent is the governing criterion for the purchase.

*Comparison behavior under this lens:*  
- Products are compared against each other within the targeted function, not against general-purpose alternatives
- The specific functional dimension is surfaced explicitly in the explanation
- Cross-lens comparisons (Targeted vs. General) require a use-case disclosure before the score

*When this lens applies:*  
When both products in a comparison share a clear, architecturally supported functional positioning. The function must be observable in the nutritional architecture — not only claimed.

*Indicators:*  
- Both products have protein above the category's functional threshold (to be defined at category launch)
- Both products declare a specific probiotic function at documented CFU
- Both products are explicitly marketed toward a common functional outcome and their architecture confirms the claim

*What this lens is not:*  
A protection against comparison with general-purpose products. When a Targeted product is placed in a General comparison, use-case disclosure is required — but the comparison is not invalid. A protein pudding placed in a general מעדנים comparison receives a use-case disclosure, not an exemption.

*Critical constraint:*  
This lens applies only when the architecture supports the function. A product with a protein claim and 8g protein/100g in a category where functional protein is ≥15g/100g does not qualify for this lens. It is a General Everyday Choice product with a marketing divergence finding.

---

**LENS 3 — DIETARY AND RESTRICTION-DRIVEN CHOICE**

*The consumer decision:* The consumer has a binding constraint — medical, metabolic, or value-system — that eliminates the general product from their eligibility set. They are not choosing between this product and its conventional equivalent; the conventional equivalent is not available to them.

*Comparison behavior under this lens:*  
- Products in this lens are compared within their restriction group, not against conventional alternatives
- Cross-lens comparisons (Restriction vs. General) require an explicit lens disclosure that identifies the restriction and explains why the score difference reflects formulation constraints, not nutritional failure
- No ranking is produced between a Lens 3 product and a Lens 1 product without the disclosure

*When this lens applies:*  
- Product is marketed for and formulated to comply with a specific restriction (gluten-free, keto, vegan, lactose-free, kosher-specific)
- The restriction drives observable formulation differences (absent gluten ingredients, severely reduced carbohydrates, absent animal products)
- The restriction is verifiable from the ingredient list or certification

*What this lens is not:*  
A nutritional immunity shield. A gluten-free bread that scores 38/D scores 38/D. The restriction disclosure explains why the formulation constraint affected the score; it does not improve the score. A consumer with celiac disease who reads a 38/D for a gluten-free bread deserves to know it scores 38/D — and also to know that this score reflects the formulation constraints of restriction compliance.

*When this lens does not apply:*  
When a restriction claim is incidental rather than defining. A product that is naturally free of an ingredient (e.g., a dairy product that incidentally contains no gluten) does not qualify for Lens 3. Lens 3 requires that the restriction drove formulation decisions.

---

### SECTION 4 — Lens Application Rules

**Rule 1 — Lenses are assigned at comparison time, not at product classification time.**  
A product does not have a lens. A comparison uses a lens. The same product can be involved in a Lens 1 comparison (evaluated against other plain dairy) and a Lens 2 comparison (evaluated against protein dairy) at different moments.

**Rule 2 — Cross-lens comparisons are permitted with disclosure.**  
Two products from different lenses can be placed in a comparison provided the lens disclosure appears before the scores. Lens 1 vs. Lens 2 comparisons produce: "Product A is an everyday nutrition choice. Product B is a targeted protein product. What follows is a direct comparison with this context noted." The consumer receives accurate information; the comparison proceeds.

**Rule 3 — Lens 1 is the default. Lenses 2 and 3 require positive evidence.**  
When in doubt, Lens 1 applies. Assigning Lens 2 or Lens 3 requires observable, specific evidence from the product's architecture. A claim alone is insufficient for Lens 2; architectural support is required. A restriction claim alone is insufficient for Lens 3; formulation evidence is required.

**Rule 4 — Lens assignment cannot improve a product's score.**  
Being assigned to Lens 2 or Lens 3 does not create a different scoring baseline. The score remains the same. The lens only governs the comparison group and the disclosure text.

**Rule 5 — Ambiguous cases default to Lens 1.**  
This is the conservative interpretation principle applied to lens assignment. Bari does not grant restrictive-lens protection based on ambiguous evidence. If the architecture is unclear, the product competes in the general pool with the appropriate disclosure.

---

## 5. Marketing Divergence Finding Standard

### 5.1 Definition

A Marketing Divergence Finding is issued when a product's manufacturer claim implies a use-case or nutritional function that the product's observable architecture does not support at a meaningful level.

This is a formal Bari output type. It is not a rhetorical observation in editorial prose. It has a defined trigger condition, an evidence standard, and a standard format.

It is distinct from a low score. A low score reflects performance on nutritional criteria. A Marketing Divergence Finding reflects a gap between what the product claims to be and what it is.

### 5.2 When the Finding Applies

A Marketing Divergence Finding is triggered when all three of the following conditions are met:

**Condition 1 — A specific claim is present.**  
The product carries a specific purposive claim: "high protein," "protein," "probiotic," "keto," "natural," "organic," "enriched," "diet," "light," "for athletes," or a comparable functional declaration. Generic marketing language ("delicious," "quality," "authentic") does not trigger the finding.

**Condition 2 — The claim implies a specific nutritional standard.**  
The claim, in its ordinary meaning, implies that the product delivers a specific nutritional function at a meaningful level. "High protein" implies protein concentration above the category norm at a level that creates a genuine nutritional advantage. "Probiotic" implies live cultures at a dose that supports gut health. "Keto" implies carbohydrate restriction below ketogenic thresholds.

**Condition 3 — The architecture does not support the implied standard.**  
Measured against the specific nutritional dimension implied by the claim, the product's observable architecture falls materially short of what the claim implies. "High protein" with protein at or below the category average. "Probiotic" with no declared CFU count and no verifiable culture information. "Keto" with carbohydrates above ketogenic threshold.

All three conditions must be present. A low-protein product without a protein claim does not generate this finding. A protein claim that is architecturally supported at the implied level does not generate this finding.

### 5.2.1 Claim Threshold Reference Table

*(Added: 2026-05-29. Source: Cereals Gap Resolution Report v1, Resolution 4.)*

Condition 2 of the Marketing Divergence Finding requires that the claim "implies a specific nutritional standard in its ordinary meaning." For claim types where that standard is not self-evident, a calibrated threshold must be defined. This table provides the calibrated standard for each defined claim type.

Thresholds not listed here must be documented in the category-specific governance addendum at category launch before any Marketing Divergence Findings are produced for that claim type. When no threshold exists and none has been documented, Condition 2 cannot be evaluated — the finding cannot be issued for that claim type.

**Table: Defined Claim Thresholds (as of v2 amendment, 2026-05-29)**

| Claim type | Claim forms covered | Threshold definition | Detection method |
|---|---|---|---|
| Whole grain — composition | "made with whole grain," "contains whole grain," "with whole grain goodness," or any claim implying presence without dominance | ≥ 30% of grain ingredients by weight are whole grain — operationally: a whole grain flour of the specified grain appears in the ingredient list and is not preceded by a refined flour of the same grain | Ingredient list: whole grain flour appears before refined flour of the same grain; or only whole grain flour of that grain is listed |
| Whole grain — primary/dominant | "whole grain," "100% whole grain," "entirely whole grain," or any claim implying the product is predominantly whole grain | Whole grain flour is the first listed grain ingredient AND constitutes ≥ 51% of total grain weight (FDA/WGC standard). In absence of weight data: whole grain flour is first grain ingredient AND no refined flour of the same grain appears at all | Ingredient list: whole grain flour is listed before all refined grain ingredients; presence of refined flour of the same grain immediately after disqualifies the dominant claim |
| Keto / ketogenic | "קטוגני," "keto-friendly," "ketogenic" | Net carbohydrates ≤ 5g per 100g | Nutritional label: total carbohydrates minus fiber ≤ 5g/100g |
| High protein (general food context) | "עשיר בחלבון," "high protein," "rich in protein" | Protein ≥ 20% of total calories, OR ≥ 15g/100g in solid products, OR ≥ 8g/100ml in beverages | Nutritional label protein content per 100g/ml. Note: category-specific thresholds supersede this general default when documented |
| Reduced-fat / light (dairy) *(added 2026-06-01, Source: Cheese-Spreads Stress Test v1, TASK-141, Resolution 2 — ratified 2026-06-01)* | "דל שומן," "light," "לайт," "חצי שומן," "reduced fat," a stated low fat % positioned as light | **≥ 25% fat reduction vs. the standard-fat reference product of the *same sub-pool***. The pool standard-fat reference is the pool's full-fat / standard tier (or pool median where no single reference exists). A lower-fat tier that is itself the category default (e.g., 5% white cheese) is NOT "light" relative to itself. Relative reduction is the sole eligibility test — an absolute fat cutoff is not used, as fat baselines differ across dairy sub-pools. | Nutritional label fat/100g vs. same-sub-pool standard reference |

**Application rule:**  
When a claim is present and a threshold exists in this table, Conditions 1 and 2 of the Marketing Divergence Finding are automatically satisfied if the claim form matches. Condition 3 (architecture falls short of the threshold) must still be evaluated. All three conditions must be present for the Finding to be issued.

**Absence of threshold:**  
If a claim type is not listed and no category-specific threshold has been documented, Condition 2 cannot be evaluated. The claim is noted as "claim threshold undefined — Marketing Divergence Finding not applicable" in the category analysis record. This triggers a documentation requirement under Constitution v1, Article VI, criterion D6.

**Table maintenance:** CE Controller 1 is responsible for updating this table when new category thresholds are established. Each new threshold entry must include the claim forms covered, the threshold definition, and the detection method.

---

### 5.3 Evidence Required

The finding must be supported by a specific, quantitative observation:

- For macro claims: the specific nutrient value per 100g/ml, the category average or threshold against which it falls short, and the delta
- For functional claims: the declared or estimated dose of the active component and the established functional threshold (if available)
- For restriction claims: the specific ingredient or nutrient that the claim excludes, and whether the exclusion is architecturally confirmed

Evidence of absence is not sufficient. If a product claims "probiotic" and no CFU information is available, the finding is "CFU data unavailable — functional claim cannot be verified" rather than "claim is not supported." The distinction matters: the product may have a legitimate probiotic culture at adequate dose that is simply not disclosed on the label.

### 5.4 Standard Finding Format

```
MARKETING DIVERGENCE FINDING

Claim: [exact claim text from product]
Observed: [specific nutritional value from product record]
Expected: [value implied by claim / threshold / category standard]
Gap: [quantified delta]
Finding: [claim] is [not supported / partially supported / unverifiable] 
         by the product's nutritional architecture.

[Optional: one sentence on what the product does deliver that is accurate]
```

### 5.5 Example Findings

**Example 1 — Weak protein claim:**

```
MARKETING DIVERGENCE FINDING

Claim: "עשיר בחלבון" (rich in protein)
Observed: 5.8g protein / 100ml
Expected: Products with credible protein claims in this category 
          deliver ≥10g protein / 100g (dairy context)
Gap: −4.2g / 100g below meaningful protein-forward threshold
Finding: The "protein" claim is not supported by the product's 
         nutritional architecture. The product contains above-average 
         protein for standard chocolate milk but does not deliver 
         meaningful protein concentration.

The product does contain more protein than standard variants.
This is an incremental improvement, not a protein delivery claim.
```

**Example 2 — Cosmetic functional claim:**

```
MARKETING DIVERGENCE FINDING

Claim: "עם פרוביוטיקה" (with probiotics)
Observed: Live cultures declared; no CFU count available
Expected: Functional probiotic effect requires documented CFU 
          (typical range: 1–10 billion CFU per serving)
Gap: CFU count not declared — functional claim cannot be verified
Finding: The probiotic claim cannot be assessed from available data. 
         Bari cannot confirm the product delivers probiotics at a 
         functionally relevant dose.

The presence of live cultures is observable; their quantity is not.
```

**Example 3 — Keto health halo:**

```
MARKETING DIVERGENCE FINDING

Claim: "קטוגני" (ketogenic)
Observed: 12g net carbohydrates / 100g
Expected: Ketogenic formulation typically requires ≤5g net carbs / 100g
Gap: +7g / 100g above standard ketogenic threshold
Finding: The ketogenic claim is not supported by this product's 
         carbohydrate content. The product has reduced carbohydrates 
         compared to conventional alternatives but does not meet 
         standard ketogenic dietary requirements.
```

**Example 4 — Children's product health halo:**

```
MARKETING DIVERGENCE FINDING

Claim: Product marketed as "healthier choice for kids" 
       with imagery implying nutritional superiority
Observed: 19g sugar / 100g; 8 additives including artificial colors
Expected: A "healthier choice" positioning implies meaningful 
          improvement over the category benchmark
Gap: The product's sugar content (19g/100g) and additive load 
     are at or above the category median
Finding: The "healthier choice" positioning is not supported by 
         the product's nutritional architecture relative to 
         the category. The claim appears to be marketing 
         language rather than a nutritional distinction.
```

### 5.6 What Bari Should Not Say in a Marketing Divergence Finding

- **Do not attribute intent.** "The manufacturer is misleading consumers" — Bari cannot observe intent. The finding states the gap; it does not explain why the gap exists.
- **Do not call the product defective.** The finding concerns the claim, not the product. The product may be entirely appropriate as a General Everyday Choice product; the finding is about the claim's accuracy, not the product's worth.
- **Do not produce the finding without quantitative evidence.** "The protein claim seems overstated" is not a finding. "The protein content (5.8g/100ml) is below the threshold for a credible protein positioning in this category (10g/100g)" is a finding.
- **Do not use the finding to imply the product should not exist.** The finding is informational. It does not recommend against purchasing the product.

---

## 6. Anti-Immunity Rule

### 6.1 The Rule

> **Purpose, use-case, and lens assignment can contextualize a score. They cannot excuse poor nutritional architecture. They cannot lower the bar for what constitutes a good score. They cannot be used to suppress or soften a score that reflects genuine nutritional limitations.**

This rule is not advisory. It is a hard constraint that governs every application of use-case reasoning in Bari's output.

### 6.2 Why Indulgence Is Not a Protective Category

The rejected Framework v1 proposed an Indulgence classification that effectively normalized low scores for products with high-sugar, high-fat, low-protein architecture. The reasoning was that evaluating such products against protein and fiber criteria was "epistemological overreach."

That reasoning fails for three reasons.

**First:** Consumers who consume indulgent products still benefit from accurate nutritional information. A consumer who regularly eats a milk chocolate dessert may not experience it as a health product — but they are still better served by accurate nutritional data than by a score softened through purpose normalization. Indulgence is not a reason to reduce the quality of Bari's nutritional finding.

**Second:** "Indulgence" is not a nutritional category with its own nutritional standards. It is a description of the experience a product prioritizes. The nutritional criteria that Bari applies — protein, fiber, sugar, processing quality — are relevant to all food products regardless of the hedonic experience they deliver. An indulgent product can be well-formulated (real chocolate, minimal additives, no artificial ingredients) or poorly formulated (artificial flavors, 12 additives, industrial sugar). BSIP's architecture correctly distinguishes these. Indulgence classification would collapse that distinction.

**Third:** Indulgence classification is commercially exploitable. Any manufacturer of a high-sugar, high-additive product can claim Indulgence and receive normalized scoring. The classification is available to everyone in the D/E range with no gating criterion that isn't also available to every poor-quality product on the shelf. A protection that is equally available to all low-quality products is not a protection — it is a suppression system for the scoring signal.

**The correct treatment of indulgent products:** A traditional milk chocolate dessert that scores 38/E receives 38/E. The explanation notes: "This product is designed primarily for pleasure rather than nutrition. Its score reflects that architecture against general nutritional criteria." That context is useful to the consumer. It is an honest observation. It is not a score reduction. It is not a normalized baseline for the product's category.

### 6.3 Restriction Products Still Receive Honest Scoring

A dietary restriction product — keto bread, gluten-free pasta, vegan cheese — that scores poorly on general nutritional criteria receives that score. The lens disclosure contextualizes the score: "This product is formulated for [restriction context]. Its score reflects the nutritional architecture within that constraint." This is honest and useful.

What the lens does not do:
- It does not produce a different score for the product
- It does not establish a separate scoring baseline for restriction products
- It does not imply the product is nutritionally adequate for a consumer without the restriction

A consumer with celiac disease who reads that a gluten-free bread scores 40/D should know it scores 40/D. That information is relevant: it tells them that among gluten-free products, this one is in the lower tier. They should seek a higher-scoring gluten-free bread if one is available. The restriction lens provides context; it does not eliminate the consumer's interest in comparative quality.

### 6.4 Functional Products Still Need Dose Evidence

A product with a functional claim receives no score adjustment for the claim. If its architecture supports the claim at a meaningful dose, the functional contribution may appear in the explanation layer as a positive observation. It does not add score points because the score does not measure functional claims — it measures nutritional architecture.

If the functional claim is not supported (Marketing Divergence Finding triggered), the claim is surfaced as a finding. The product's score is unchanged. The finding adds information; it does not subtract score points.

Neither condition — claim supported or claim unsupported — results in a score change. Score changes result only from changes to the underlying nutritional data or from scoring architecture revisions at BSIP level.

### 6.5 Different Purpose Does Not Mean Nutritionally Fine

"These products serve different purposes" is a comparison disclosure. It is not an evaluation of either product's nutritional quality.

When Bari states that a protein pudding and a traditional dessert serve different consumer decisions, it is saying: the score difference partially reflects architectural differences that reflect those different decisions. It is not saying: the traditional dessert is nutritionally fine for its purpose.

A product that scores 32/E serves its consumer poorly on nutritional criteria regardless of whether it is categorized as indulgence, convenience, or any other use-case. The score is the score. The use-case is context.

---

## 7. Recommendations

**Recommendation 1 — Adopt Consumer Use-Case & Purpose Guardrails v2 as the governing framework. Retire Purpose Framework v1.**  
Framework v1 is not salvageable through modification. Its foundational category error invalidates the architecture. This document supersedes it entirely. References to "purpose class" or "seven-class taxonomy" in any downstream document should be updated to reference the three comparison lenses in this document.

**Recommendation 2 — Apply the three comparison lenses at the comparison construction stage only.**  
No lens is assigned to a product at the BSIP level. No lens field is added to BSIP1 enrichment. Lenses are editorial tools applied when two specific products are placed alongside each other. The comparison output records which lens was applied and why.

**Recommendation 3 — Establish the Marketing Divergence Finding as a standard editorial output type with defined format.**  
The finding format defined in Section 5 should be treated as a named output type in Bari's editorial system, alongside insight lines, positive signals, and limiting factors. It should have a consistent format, an evidence requirement, and a named field in the product record when applicable.

**Recommendation 4 — Amend the Comparison Governance Constitution v1 to reference this document.**  
The Constitution's Article II (Eligibility) and Article III (Ranking) reference "primary consumer purpose" without defining the term. This document provides the operational definition. The Constitution should be updated with a cross-reference to Section 1.1 of this document and to the three comparison lenses.

**Recommendation 5 — Issue the Anti-Immunity Rule as a named governance provision.**  
The Anti-Immunity Rule in Section 6.1 should be named, numbered, and referenced as a hard constraint in all future category editorial protocols. It should appear in the Category Launch Approval Checklist (Comparison Governance Constitution v1, Article VI) as a required verification item.

**Revised Answer to the Governance Question:**  

> **C — Comparison-time guardrail.** Not a core BSIP layer. Not a category taxonomy. Not an editorial caveat only (too weak for systematic application). A comparison-time guardrail: applied at the specific moment two products are placed in comparison, governed by three broad lenses, enforced by the Anti-Immunity Rule, and supported by the Marketing Divergence Finding as a systematic output type.

---

## 8. Risks

**Risk 1 — "Comparison-time" is poorly bounded without a product-level anchor.**  
If use-case reasoning is applied only at comparison time, every analyst who constructs a comparison must independently determine the applicable lens. Without a product-level anchor, two analysts may assign different lenses to the same product in different comparisons. Over time, the same product accumulates inconsistent lens assignments across the category. Mitigation: maintain a category-level lens-assignment log that records the lens applied to each product in each comparison, with the specific architectural evidence that justified the assignment. The log creates consistency without requiring upstream product classification.

**Risk 2 — The Marketing Divergence Finding can be perceived as accusatory.**  
Publishing a named finding that says "this claim is not supported by this product's architecture" is a strong editorial act. Manufacturers will object. Consumers may read it as an accusation of deception. Mitigation: the finding format specified in Section 5.6 prohibits attribution of intent and restricts the finding to the factual gap. The finding states the gap; it does not explain the manufacturer's motivation for the gap.

**Risk 3 — Lens 2 (Targeted Function) becomes a new Indulgence-style immunity vector.**  
If Lens 2 is applied loosely — if any product with a functional claim gets comparison-pool protection — it becomes the replacement for the Indulgence immunity risk that was specifically rejected. A protein pudding that barely crosses a protein threshold could claim Lens 2 and be removed from comparison with traditional puddings. Mitigation: Rule 5 (Lens 1 is default; Lenses 2 and 3 require positive architectural evidence) is the key safeguard. Apply it strictly. If the architectural evidence is ambiguous, Lens 1 applies.

**Risk 4 — The three lenses are insufficient for highly heterogeneous categories.**  
In beverages, the range from plain water to probiotic functional shots to energy drinks to sports recovery drinks is extreme. Three lenses may not provide enough granularity to construct valid comparison groups. A comparison between flavored water and a probiotic drink may be assigned to Lens 1 by default (neither is clearly Targeted or Restriction), producing a comparison that no consumer would make. Mitigation: the Comparison Governance Constitution's eligibility rules (Article II.3 — absolute restrictions) handle the most extreme cases independently of the lens system. The lenses govern the middle ground.

**Risk 5 — The framework is too minimal for categories Bari hasn't entered yet.**  
For categories with genuinely complex use-case architecture — clinical nutrition adjacencies, meal kits, fermented foods — three lenses and comparison-time application may provide insufficient governance. Mitigation: this framework is the floor. As Bari enters complex categories, category-specific use-case addenda can supplement the three-lens framework without requiring a new general architecture.

---

## 9. Open Questions

**OQ-001 — Does the "comparison-time only" rule create a gap for individual product presentations?**  
When Bari presents a single product — not in comparison — there is no comparison context in which to apply lens reasoning. But use-case context might still be relevant: explaining a low score for a restriction product, or surfacing a Marketing Divergence Finding for a product presented alone. The framework currently provides no guidance for use-case reasoning in solo product presentations. Is this a gap that needs filling, or is the explanation framework (Comparison Governance Constitution v1, Article IV) sufficient?

**OQ-002 — What is the category-specific protein threshold for Lens 2 eligibility?**  
The framework requires architectural support for Lens 2 assignment. For protein-targeted function, this requires a threshold: protein at or above X per 100g. The framework does not set X — it correctly defers to category launch. But without thresholds, Lens 2 cannot be consistently applied. Each category launch must produce a documented threshold decision, and the threshold must be externally validated (not derived from the framework's own definitions).

**OQ-003 — How does the Anti-Immunity Rule interact with the partial confidence situation?**  
When a product has partial data confidence and a low score, is the score still "what the score is" in the Anti-Immunity sense? A product with 55% data coverage that scores 40/D may have a "true" score anywhere in a range around 40/D. The Anti-Immunity Rule prohibits use-case from excusing the score, but incomplete data may be a legitimate reason to caveat it. These are different caveats — purpose-based vs. data-quality-based — and the framework should be explicit that the Anti-Immunity Rule governs only purpose-based caveats.

**OQ-004 — Should the Marketing Divergence Finding be produced proactively or reactively?**  
The finding could be produced proactively (Bari audits all products in a category for marketing claim / architecture gaps at category launch) or reactively (the finding is produced when a product with a divergent claim is placed in a comparison). Proactive production maximizes consumer value. Reactive production is more manageable. The framework currently implies reactive production; a proactive audit protocol would require additional governance.

**OQ-005 — What happens when a product migrates between lenses due to reformulation?**  
A product that qualifies for Lens 2 at launch (architecturally supported protein claim) may be reformulated to reduce protein below threshold. Its lens assignment is now incorrect. Without upstream product classification, lens assignments are not tracked at the product level and reformulation changes are invisible to the lens framework. This is an operational gap that becomes consequential as categories age and products evolve.

---

*Bari Consumer Use-Case & Purpose Guardrails v2*  
*CE Controller 1 — Chief Nutrition, Scoring & Content Architect*  
*2026-05-29*  
*Supersedes: Product Purpose Framework v1*  
*Governed by: Bari Governance v1, Comparison Governance Constitution v1*
