# Bari Comparison Governance Constitution v1

**Classification:** Governing Framework — Internal  
**Issued:** 2026-05-29  
**Author:** CE Controller 1 — Chief Nutrition, Scoring & Content Architect  
**Status:** Active — applies to all current and future Bari comparison categories  
**Supersedes:** None (inaugural document)  
**Subject to:** Bari Governance v1 (constitutional layer)

---

## 1. Executive Summary

Bari's comparison experience is its most consequential consumer-facing output. When Bari places two products side by side and renders one superior to the other, it exercises editorial judgment that directly shapes consumer understanding. That judgment must be earned, not assumed.

This document exists because comparison is an inherently dangerous act. Done correctly, a comparison clarifies a genuinely opaque shelf. Done incorrectly, it misleads a consumer into a false binary, penalizes products for characteristics irrelevant to the consumer's actual purpose, or creates the impression of scientific certainty where only probabilistic interpretation is defensible.

The מעדנים category demonstrated the risks: protein-enriched products and traditional pleasure desserts occupy the same shelf but serve different consumer purposes. A comparison that ranks them together without acknowledgment of that divergence produces a number that appears precise but is epistemically dishonest.

This constitution establishes the intellectual rules that govern every comparison Bari produces across every category it will ever enter. It does not govern how comparisons are displayed. It governs what may be compared, how rankings are constructed and communicated, what constitutes a trustworthy explanation, and what must be true before a new category is approved for comparison.

**Core position:** Bari comparisons exist to reduce consumer confusion, not to create it. When the honest answer is "these products are not meaningfully different," that is a valid comparison outcome. When the honest answer is "these products serve different purposes," that is a valid reason to decline ranking.

**Six distortions registered in this document (DISTORTION-002 through DISTORTION-010).** None are implemented. All are reserved for BSIP3 review.

---

## 2. Findings

### 2.1 What the מעדנים Category Revealed

The inaugural comparison category exposed six structural tensions that recur across categories:

**Finding 1 — Purpose divergence is common, not exceptional.**  
In מעדנים, protein-enriched yogurts and traditional puddings share a shelf but differ in consumer intent. This pattern recurs in every category Bari will enter: protein bars vs. date bars, chocolate milk vs. protein milk, fortified cereals vs. whole-grain cereals. Purpose divergence is not an edge case. It is a default condition in the Israeli dairy, bakery, and snack aisle.

**Finding 2 — Marketing claims create artificial comparison clusters.**  
Products marketed as "diet," "protein," "light," or "natural" are positioned as superior within their category. The consumer has already been primed to compare these products against their standard counterparts. Bari's comparison layer enters a pre-existing frame. If Bari simply validates that frame without interrogating it, it becomes a marketing amplifier rather than an intelligence layer.

**Finding 3 — Score differences below threshold are routinely misinterpreted.**  
A 3-point score difference between two dairy desserts will appear meaningful to a consumer who sees 61 versus 58. In practice, at this precision level, ingredient variation between production batches, seasonal supplier changes, and incomplete nutritional label coverage can account for that entire delta. Without a meaningful difference threshold, Bari produces rankings that imply precision it does not possess.

**Finding 4 — The distortion registry is underbuilt.**  
DISTORTION-001 (fiber expectation in dairy) was the first documented instance of a systematic scoring bias that affects comparison validity. Analysis indicates at least nine additional distortions that operate across multiple categories. These are not bugs — they are structural tensions between a universal scoring framework and category-native reality. Each requires documentation before the categories it affects are launched.

**Finding 5 — Explanation quality determines consumer trust more than score accuracy.**  
A consumer who reads a clear, honest explanation of why two products differ — or why they do not differ meaningfully — walks away with accurate food intelligence regardless of whether the underlying score was off by two points. A consumer who reads a misleading explanation walks away misinformed even if the score was correct. Explanation governance is as important as scoring governance.

**Finding 6 — Category launch has no formal gate.**  
Prior to this document, no formal checklist existed specifying what must be true before a new comparison category could be approved. Each category was launched by judgment. This works when the category is well-understood; it creates compounding risk as Bari enters unfamiliar territory (beverages, frozen foods, cereals) where distortion patterns differ materially from bread and dairy.

---

## 3. Bari Comparison Governance Constitution v1

---

### ARTICLE I — COMPARISON PHILOSOPHY

#### 1.1 Why Bari Comparisons Exist

The Israeli retail food environment presents consumers with hundreds of products within any category, the majority of which are differentiated by marketing claim rather than nutritional substance. A consumer navigating the מעדנים shelf encounters: "protein," "light," "diet," "natural," "organic," "enriched," "bio," "pro," "kids." These claims signal positioning, not nutrition. The gap between what the packaging communicates and what the product delivers is where consumer confusion lives.

Bari comparisons exist to close that gap. They exist to answer the question that packaging will not: **when I pick up two products that appear to serve the same purpose, do they actually differ in nutritional quality — and if so, how materially?**

#### 1.2 What Consumer Problem Comparisons Solve

Comparisons solve three specific problems:

**Problem 1 — The false equivalence problem.**  
Two products occupy the same shelf position and carry similar prices. The consumer assumes they are roughly equivalent. One is NOVA 3 with 2 additives; the other is NOVA 4 with 12 additives and double the sugar. The packaging does not surface this gap. Bari does.

**Problem 2 — The wellness claim problem.**  
A product carries a "protein" or "diet" or "light" claim. The consumer assumes this claim correlates with superior nutrition. Often it does not, or the correlation is partial. Bari's comparison layer quantifies what the claim actually delivers versus what is implied.

**Problem 3 — The variant confusion problem.**  
A manufacturer produces 12 variants of the same product: flavors, fat percentages, sizes, fortified versions, reformulations. The consumer cannot tell which variant represents better nutritional value. Bari's comparison layer surfaces the within-brand nutritional architecture.

#### 1.3 What Bari Is Helping Users Understand

Bari comparisons help users understand:

- Whether a nutritional difference between two products is **material** (large enough to affect their decision) or **marginal** (within the noise of normal production variation)
- Whether a wellness claim translates to a **genuine nutritional advantage** or only to a marketing premium
- Whether two products that appear similar are **serving the same purpose** or are **fundamentally different** products that happen to share a shelf
- What the **specific nutritional basis** of any ranking difference is — not a label, but an observable fact about ingredients, processing, or macronutrient composition

#### 1.4 What Bari Comparisons Must Never Attempt

**Never recommend.** Bari does not tell consumers what to buy. Bari does not say "you should choose product A." Bari says "product A scores higher because of X, Y, Z." The consumer's decision involves factors Bari cannot observe: preference, budget, frequency of consumption, health goals, household composition.

**Never moralize.** Bari does not frame lower-scoring products as bad choices. A NOVA 4 dairy dessert consumed occasionally is not a health risk that Bari is positioned to evaluate. Bari describes. Bari does not judge consumption patterns.

**Never simplify irresolvable tradeoffs.** Some products present genuine tradeoffs that scoring cannot resolve. A product might be lower in sugar but higher in saturated fat. A product might have cleaner ingredients but lower protein coverage. When the tradeoff is irresolvable within BSIP's scoring architecture, Bari acknowledges the tradeoff rather than suppressing it.

**Never manufacture false precision.** A score of 61.3 is not meaningfully more precise than 61. BSIP produces estimates, not measurements. The output precision of the system should not exceed the input quality of the data.

**Never rank products whose purposes are incomparable.** A pleasure dessert and a post-workout protein product are not in competition for the same consumer decision. Ranking them together implies they are. That implication is false.

**Never attribute the score to a single driver.** A product does not score 72 "because of protein." It scores 72 because of the full weighted interaction of all scored dimensions. Single-driver attribution is a form of oversimplification that creates misleading consumer understanding.

#### 1.5 What a Successful Comparison Experience Looks Like

A comparison succeeds when a consumer who has read it:
- Can state the **specific nutritional basis** of any ranking difference
- Can understand whether the difference is **material or marginal**
- Can identify whether the two products **serve the same purpose** or whether purpose divergence explains part of the gap
- Has **not been told what to buy**
- Has **not been told the lower-scoring product is harmful**
- Leaves with a more accurate model of the shelf than they arrived with

A comparison fails when a consumer who has read it:
- Believes one product is "good" and another is "bad"
- Cannot identify the specific basis for the ranking
- Has made a purchase decision on the basis of a claim Bari cannot actually support
- Would make the same decision regardless of consumption purpose

---

### ARTICLE II — COMPARISON ELIGIBILITY FRAMEWORK

#### 2.1 Core Eligibility Principle

**Two products are eligible for comparison only if a consumer could reasonably purchase either product for the same primary purpose.**

"Primary purpose" is defined as the functional role the product plays in the consumer's diet: breakfast component, dessert, afternoon snack, meal replacement, or supplement. It is not defined by shelf placement, packaging similarity, or manufacturer category.

This principle overrides all secondary criteria. If two products fail the primary purpose test, they are not eligible for comparison regardless of similar nutritional profiles, similar branding, or shared shelf position.

#### 2.2 Products That May Be Compared

Products are eligible for direct ranking comparison when they satisfy all three of:

**Criterion A — Shared primary purpose.**  
The consumer is choosing between these products for the same eating occasion. Both products are reasonable answers to the same consumer decision.

**Criterion B — Comparable consumption unit.**  
The products are consumed in meaningfully similar quantities per occasion. Products with radically different serving sizes require normalization. Normalization must be documented and disclosed.

**Criterion C — Comparable category definition.**  
Both products fall within the same Bari category definition as governed by Article IV (Category Launch Approval).

#### 2.3 Products That Should Never Be Compared (Absolute Restrictions)

The following comparisons are prohibited regardless of nutritional similarity:

| Comparison | Reason |
|---|---|
| Meal replacement vs. snack | Caloric role divergence — different dietary function |
| Supplement (protein powder, collagen, creatine) vs. food product | One is a supplement; different regulatory standard, different dosing logic |
| Baby food / infant formula vs. adult food | Different regulatory framework, different nutritional standards |
| Medical nutrition product vs. retail food | Clinical vs. consumer context — incomparable purpose |
| Alcohol-containing product vs. non-alcohol product | Incomparable risk profile beyond nutrition |
| Children's / developmental product vs. adult product | Different nutritional standards, different regulatory context, different target consumer. See Section 2.8 for operational definition of "children's product." |

#### 2.4 Category Boundary Rules

**Rule 1 — Cross-category comparisons require explicit purpose alignment disclosure.**  
If two products from nominally different categories are compared (e.g., a bar and a dairy dessert both marketed as snacks), the comparison must explicitly acknowledge the cross-category nature and state the basis for inclusion.

**Rule 2 — Sub-category comparisons require sub-category definition.**  
If a comparison is within a sub-category (e.g., protein yogurt vs. protein yogurt, not protein yogurt vs. plain yogurt), the sub-category boundary must be defined and applied consistently. A comparison that includes some protein yogurts but not others without stated criteria is editorially arbitrary.

**Rule 3 — A product may not move between comparison groups within the same category.**  
Once a product is classified as belonging to a comparison group (e.g., "traditional dairy desserts"), it cannot be reclassified into a different group (e.g., "protein dairy desserts") within the same category analysis without documented justification.

#### 2.5 Product Variant Rules

**Variant eligibility:**  
Product variants (flavor variants, fat percentage variants, pack size variants) of the same base product are eligible for comparison with each other. They are not eligible for comparison with structurally different products from other brands unless the base product criterion is met.

**Variant selection:**  
When multiple variants exist, Bari selects the most nutritionally representative variant for cross-brand comparison purposes. This is typically the original/standard variant, not the enriched or light variant, unless the comparison is specifically about the enriched or light positioning.

**Variant comparison specific cases:**

| Comparison | Eligible? | Governance note |
|---|---|---|
| מילקי שוקולד vs. מילקי לייט | Yes | Same product, variant comparison. Fat reduction effect. |
| יופלה GO קלאסי vs. יופלה GO דובדבן | Yes | Same product, flavor variant. |
| מעדן חלבון ויטלה vs. מעדן חלבון לולה | Yes | Cross-brand within defined sub-category. |
| יופלה GO vs. מילקי שוקולד | Yes, with disclosure | Purpose divergence note required — different consumer intent. |
| עדנה 3% vs. עדנה 5% | Yes | Fat-level variant comparison. |

#### 2.6 Hybrid Product Rules

**Definition:** A hybrid product is a product marketed simultaneously under two positioning claims that belong to different comparison groups (e.g., "protein" + "dessert," "diet" + "indulgent," "organic" + "fortified").

**Governance principle:** Hybrid products must be classified by their **dominant nutritional reality**, not by their marketing claim.

Classification decision tree:
1. What does the consumer primarily consume this product for? (purpose test)
2. What is the dominant macronutrient architecture? (protein-forward vs. carbohydrate-forward vs. fat-forward)
3. What is the processing level? (NOVA class)
4. Where does the product physically appear on shelf?

If the marketing claim and the nutritional reality diverge, the nutritional reality governs classification. The divergence is surfaced in the explanation layer (Article V).

**Hybrid comparison rule:**  
A product classified by nutritional reality as a traditional dessert may not be placed in a protein comparison group simply because it carries a protein claim — unless its protein content meets the threshold that defines the protein sub-category (threshold defined per category at launch).

#### 2.7 Purpose-Based Comparison Rules

When a comparison involves products with partially overlapping but distinct purposes, the following rules apply:

**Rule 1 — Purpose divergence is information, not a disqualifier.**  
Two products with different purposes can still be compared, provided the purpose divergence is explicitly disclosed in the comparison output and its implications for the ranking are explained.

**Rule 2 — Purpose divergence statement triggers explanation requirement.**  
Any comparison where a purpose divergence is identified must include an explicit explanation of what the divergence means for the consumer — not a recommendation, but a statement of what the score difference reflects and what it does not.

**Specific case examples:**

| Comparison pair | Purpose status | Required disclosure |
|---|---|---|
| Protein pudding vs. regular pudding | Partial divergence | Protein enrichment changes the product's nutritional role. A higher score reflects protein concentration, not superior quality as a dessert experience. |
| Greek yogurt vs. protein yogurt | Minimal divergence | Protein yogurt is an evolution of the same category. Comparison is direct. Note protein source if relevant. |
| Chocolate milk vs. protein milk | Material divergence | Protein milk is a functional product. Chocolate milk is a flavored beverage. Different consumer purposes; ranking reflects different design goals. |
| Whole wheat bread vs. keto bread | Material divergence | Keto bread serves a specific dietary restriction. Standard bread comparison is not valid for keto consumers. Disclose before ranking. |
| Children's cereal vs. adult cereal | Absolute divergence | Different nutritional standards, different regulatory context, different target consumer. Do not rank. State separately. For the operational definition of "children's product," see Section 2.8. |
| Plain yogurt vs. flavored yogurt | Partial divergence | Flavoring adds sugar and typically additives. Comparison is valid; sugar delta is the primary driver. |

---

#### 2.8 Developmental Product Definition

*(Added: 2026-05-29. Source: Cereals Gap Resolution Report v1, Resolution 1.)*

A product is classified as a developmental / children's product when it satisfies any **two or more** of the following four indicators. All indicators are observed from the product record; none rely on manufacturer self-declaration.

**Indicator D1 — Visual targeting:**  
Primary packaging features animated characters, anthropomorphized mascots, cartoon imagery, or child-directed visual language whose primary design audience is children under 12. Mascots used consistently by an adult-positioned brand do not qualify (e.g., a bear mascot on an adult granola brand is not a child-targeting signal if the product is marketed to adults).

**Indicator D2 — Name or pack language:**  
Product name or primary pack copy includes explicit child-targeting terms: "ילדים," "kids," "junior," "little," "mini" when referring to child-sized portions (not product dimensions), or developmental stage language ("toddler," "school age," or age ranges below 12).

**Indicator D3 — Pediatric serving size:**  
Declared serving size is ≤ 25g (breakfast cereal context) or ≤ 30g (snack context). Adult cereals typically declare 30–55g servings; pediatric products typically declare 20–30g. Category-specific D3 thresholds for non-cereal categories must be documented at category launch.

**Indicator D4 — Developmental marketing claim:**  
Product carries an explicit developmental positioning claim: "supports growth," "for growing bodies," "school nutrition," or a comparable claim that refers to the developmental needs of children under 12 as the primary stated purpose.

**Classification requires any two indicators concurrently present.**

**Anti-gaming provision:** A product that historically qualified as a children's product (by any two indicators) does not escape classification by removing one indicator through packaging redesign while retaining the other. Classification history is retained.

**Classification consequences:**
- Classified developmental products are not ranked against non-developmental products under any lens
- They are compared within a developmental-product sub-pool only
- Score and architecture are reported honestly; the developmental context is stated before any score
- Classification cannot improve a product's score (Anti-Immunity Rule applies)

**Scope:** This definition applies to all Bari categories, not only to cereals. Indicator D3 serving size thresholds are calibrated for the cereal context; other categories must document their D3 threshold at launch.

---

#### 2.9 Architectural Divergence Sub-Category Rule

*(Added: 2026-05-29. Source: Cereals Gap Resolution Report v1, Resolution 3. Supplements Rule 2 of Section 2.4.)*

When a group of products within a category shares an architectural profile that diverges significantly from the parent category baseline across two or more scored dimensions, that group constitutes a distinct comparison sub-category and must be defined as a separate pool under Rule 2 of Section 2.4.

**Divergence threshold:** A sub-group diverges significantly when its median value on two or more scored dimensions falls outside 1.5 standard deviations of the parent category's distribution on those dimensions.

**Practical application where BSIP data is available:**  
Sub-group divergence is identified from BSIP2 category reports before pool assignment. If BSIP data is not yet available, the architectural divergence rule is applied using the following proxy indicators:

- NOVA 3 or higher (processed or ultra-processed) when the category median is NOVA 1–2
- Added sugar ≥ 10g/100g when the category median is ≤ 5g/100g (proxy: total sugar ≥ 15g/100g where added sugar data is unavailable)
- Fat ≥ 10g/100g from added fats/oils when the category median fat is < 5g/100g

Products satisfying any two proxy indicators concurrently are presumed to belong to a distinct sub-category pool pending BSIP confirmation.

**Boundary case rule:** Products at the edge of these thresholds default to the separate sub-category pool (conservative interpretation). It is preferable to over-include in the distinct pool than to distort the parent category pool.

**Granola standing precedent:**  
Within the breakfast cereals category, products identified as granola-type (satisfying any two of the three proxy indicators above) constitute a distinct sub-category pool. This is the inaugural application of this rule. Governance consequences:
- Granola-type products are ranked within the granola pool under Lens 1 (General Everyday Choice)
- Cross-pool comparisons (granola vs. standard cereal) are permitted with a purpose divergence disclosure
- Granola-type classification cannot protect a product from its score (Anti-Immunity Rule applies in full)

**Standing precedent application:** This rule and its proxy indicators apply to all future Bari categories. Future applications do not require individual governance decisions provided the proxy indicators are satisfied.

**Dairy / intrinsic-fat divergence axis**
*(Added: 2026-06-01. Source: Cheese-Spreads Stress Test v1, TASK-141, Resolution 1 — Product Owner approved 2026-06-01.)*

The proxy indicators above detect the *excess* pattern (granola-type: added sugar + added fat + NOVA 4). In categories where the differentiating fat is **intrinsic** (dairy), divergence is qualitative — set/structure, protein concentration, live fermentation, and intrinsic-fat tier — and the added-sugar / added-fat proxies under-fire (documented in `milk_production_simulation_v1.md` Sec 8.1). For such categories, sub-pool divergence is established by the **dairy structural axis**: (a) set/structure method, (b) protein concentration tier, (c) live-fermentation presence, (d) intrinsic-fat tier — confirmed by BSIP2 statistical divergence (≥ 1.5 SD on ≥ 2 of these dimensions) once data exists.

**Cheese-spreads standing precedent:** Within fresh cheese spreads, four sub-pools are defined — **Cottage**, **White-cheese / quark**, **Labaneh**, **Cream-cheese / spread**. Cream-cheese / spread also satisfies the original proxy indicators (NOVA 3–4 + high fat). Fat tiers (3 / 5 / 9%) within a pool are product *variants* (Section 2.5), not separate pools. Cross-pool comparisons require a purpose-divergence disclosure; the Anti-Immunity Rule applies in full.

---

### ARTICLE III — RANKING GOVERNANCE

#### 3.1 Why Product A Ranks Above Product B

A product ranks above another in Bari's system because its **weighted composite score across BSIP2 dimensions** is higher. That composite is the formal ranking basis. Nothing else constitutes a ranking basis — not price, not brand reputation, not consumer popularity, not packaging claims.

The BSIP2 dimensions that constitute the composite score are:
- Nutrient density (protein + fiber, weighted)
- Processing quality (NOVA proxy + additive load)
- Ingredient integrity (whole food proportion, engineering penalty)
- Sugar load (absolute + density-adjusted)
- Fat quality (saturated fat ratio where data available)
- Confidence modifier (data completeness adjustment)

A higher score means the product performed better across this specific multi-dimensional framework. It does not mean the product is categorically superior for all consumers in all contexts.

#### 3.2 What Constitutes a Meaningful Ranking Difference

**Threshold taxonomy:**

| Score delta | Classification | Consumer-facing treatment |
|---|---|---|
| 0–2 points | Noise | Products are effectively equivalent. Do not rank as better/worse. |
| 3–6 points | Marginal | One product has a modest advantage. Explain the specific driver. Note the limitation. |
| 7–14 points | Moderate | Meaningful difference. Specific driver explanation is sufficient. |
| 15–24 points | Material | Clear gap. Multiple drivers likely. Full explanation warranted. |
| 25+ points | Decisive | Products occupy different quality tiers. State clearly. |

**Threshold application rules:**
- Thresholds apply to the final composite score, not to individual dimension scores
- A product that scores significantly higher on one dimension but equivalently overall is not ranked higher overall
- Confidence modifiers can reduce the effective precision of a comparison (see 3.5)

#### 3.3 When Products Should Be Considered Effectively Equivalent

Products must be treated as effectively equivalent when:

1. Score delta is ≤ 2 points
2. Score delta is 3–6 points AND data confidence is partial or lower for either product
3. Score delta is 3–9 points AND the driver of the difference is a distortion-flagged dimension (see Article IV of the Distortion Registry)
4. Score delta is 3–10 points AND the products serve materially different purposes

**Treatment of effectively equivalent products:**  
Bari does not rank equivalent products. Bari states: "These products are nutritionally comparable on the dimensions we can observe." If one product has a specific advantage that the score does not capture (e.g., cleaner ingredient list at similar score levels), that advantage is surfaced in the explanation layer — not as a ranking, but as an observation.

#### 3.4 When Bari Must State "These Products Serve Different Purposes"

This statement is required — not discretionary — when any of the following conditions are met:

**Condition 1:** Products differ in primary consumer purpose as defined in Article II.2

**Condition 2:** The marketing positioning of one product is explicitly targeting a dietary restriction (keto, diabetic, allergen-free) that the other product does not address

**Condition 3:** One product is a functional food (high-protein, high-fiber, fortified, clinically positioned) and the other is a conventional food product

**Condition 4:** The caloric role of the products differs by more than 50% per serving (a 300-calorie meal component vs. a 150-calorie snack are not in direct competition)

**Condition 5:** One product is explicitly positioned as a children's product and the other is not

**Format of the statement:**  
The purpose divergence statement appears before the score comparison, not after. It frames the comparison. It reads as observation, not as caveat. Example: "מעדן חלבון is designed as a protein delivery vehicle; מילקי is a dessert product. Our score reflects what each product accomplishes within its own design goals."

#### 3.5 Ranking Confidence Principles

Ranking confidence is a function of:

1. **Data completeness** — What percentage of scored dimensions have observed data (vs. imputed or estimated)?
2. **Label reliability** — Is the product's nutritional label complete, consistent across sources, and free of known errors?
3. **Category specificity** — Is BSIP2's scoring architecture calibrated for this category, or is it applying bread/dairy logic to a different category type?

**Confidence levels for comparison:**

| Confidence | Definition | Ranking treatment |
|---|---|---|
| Full (both products verified) | Both products have complete, consistent data on all scored dimensions | Standard ranking applies |
| Mixed (one product verified, one partial) | One product has complete data; the other has partial coverage | Rank with disclosed confidence limitation |
| Partial (both products partial) | Both products have incomplete data | Score delta must be ≥10 points to produce a ranking. Below 10, declare equivalent. |
| Insufficient (either product insufficient) | Either product lacks enough data for reliable scoring | No ranking. Observations only. |

#### 3.6 Situations Where Ranking Should Be Avoided

Ranking must not be produced in any of the following situations:

1. **Absolute purpose divergence** — Products explicitly classified under Article II.3
2. **Insufficient data** — Either product has insufficient confidence level
3. **Active distortion involvement without resolution** — The ranking difference is primarily driven by a registered and unresolved distortion (DISTORTION-001 through DISTORTION-010 and any future entries)
4. **Cross-regulatory-category comparison** — One product is regulated as a supplement; the other is a food product
5. **Developmental food context** — Infant formula, baby food, clinical nutrition
6. **Score delta below meaningful threshold under partial confidence** — As defined in 3.5
7. **Category not yet formally approved** — Products from a category that has not cleared the launch approval framework (Article VI)

---

### ARTICLE IV — EXPLANATION GOVERNANCE

#### 4.1 What Makes an Explanation Trustworthy

An explanation is trustworthy when it satisfies all five of the following:

**T1 — It is grounded in an observed fact, not an inference.**  
"This product contains 9.3g of protein per 100g" is an observation. "This product is healthier" is an inference. Every claim in a Bari explanation must trace to an observable data point in the product's BSIP record.

**T2 — It acknowledges the limits of its own claim.**  
If a data point is absent (e.g., sugar was not available in the nutritional label), the explanation does not fill that gap with an assumption. It acknowledges the gap: "Sugar data was not available; this comparison reflects the dimensions we could observe."

**T3 — It is reversible.**  
An explanation written in a way that could describe any product in the category, or that contains no specific observations about this product, is not an explanation — it is a template. Every trustworthy explanation is specific to the product it describes.

**T4 — It separates observation from interpretation from consumer framing.**  
"This product has 12 additives" (observation). "This places it in the upper quartile of additive load for this category" (interpretation). "Some consumers prefer simpler ingredient lists" (framing). These three layers must not be collapsed into a single claim.

**T5 — It does not imply a recommendation.**  
A trustworthy explanation has no directional preference embedded in its language. It does not say "choose," "prefer," "better for you," or imply that the consumer should act on the information in any specific way.

#### 4.2 What Makes an Explanation Misleading

An explanation is misleading when it:

**M1 — Attributes intent to the manufacturer.**  
"This product was designed to maximize sugar craving" — attribution of intent is speculation. Bari cannot observe intent.

**M2 — Treats a single signal as determinative.**  
"This product is problematic because of its NOVA 4 status" treats processing level as if it overrides all other dimensions. No single dimension is determinative.

**M3 — Implies clinical significance.**  
"The higher sugar content in this product increases metabolic risk" — Bari is not a clinical instrument. It does not produce individual health assessments.

**M4 — Uses emotional language.**  
"This product is alarming" / "surprisingly clean" / "dangerously processed" — emotional registers undermine the evidential claim. They are also not falsifiable.

**M5 — Overstates confidence.**  
"This product definitively has less nutritional value" — "definitively" is a precision claim the data does not support.

**M6 — Makes a comparison without disclosing purpose divergence.**  
Any explanation that ranks two products without acknowledging a material purpose divergence between them is misleading by omission.

**M7 — Reproduces a marketing claim as if it were a Bari observation.**  
"This product, as advertised, provides superior protein" — Bari does not amplify manufacturer claims. Bari evaluates them.

#### 4.3 What Bari Should Explain

In a comparison context, Bari explains:

1. **The specific numerical basis for the score difference** — which dimensions drove the gap
2. **The magnitude of the difference** — is it material, moderate, or marginal?
3. **The data confidence behind each product's score** — what is known and what is estimated
4. **Any registered distortions that affect the comparison** — with a brief, non-technical disclosure
5. **Purpose divergence** — if applicable, stated before the score comparison
6. **What the score does not capture** — micronutrients, price, taste, consumer preference, individual health context

#### 4.4 What Bari Should Not Explain

Bari does not explain:

- Why the consumer should prefer one product
- What the score means for their personal health
- Whether the product is "worth" consuming
- What the manufacturer intended
- Whether the price differential is justified
- What any other nutrition expert, organization, or government body says about the product
- Anything that requires knowledge Bari does not possess from the product record

#### 4.5 Principles for Communicating Tradeoffs

Many products present genuine tradeoffs. A product may be higher in protein but also higher in processing. A product may have a cleaner ingredient list but lower nutritional density. BSIP2's composite score resolves tradeoffs through weighting — but the consumer may legitimately value dimensions differently from Bari's weights.

**Tradeoff communication principles:**

**Principle 1 — State the tradeoff explicitly if it is material.**  
If a product scores well on one dimension and poorly on another, and both dimensions are relevant to the comparison, both must be stated. Selective disclosure of only the favorable dimension is misleading.

**Principle 2 — Do not resolve tradeoffs the data does not resolve.**  
If the composite score reflects an architecturally controversial weighting (e.g., fiber in dairy products — DISTORTION-001), the explanation must acknowledge that reasonable people might weight the tradeoff differently.

**Principle 3 — The tradeoff statement is not a recommendation.**  
Stating "Product A has higher protein; Product B has fewer additives" is an observation. It does not conclude with "therefore you should prefer Product B if you care about processing." The consumer draws their own conclusion.

**Principle 4 — Tradeoffs involving distortion-flagged dimensions require a distortion disclosure.**  
If a tradeoff involves a dimension flagged in the distortion registry (e.g., fiber in dairy, added vs. natural protein, fortification), the comparison must disclose that the scoring architecture has a known limitation in this area.

#### 4.6 Principles for Handling Uncertainty

**Uncertainty is not failure. Uncertainty is information.**

**Principle 1 — Surface uncertainty at the level it exists.**  
If only sugar data is missing, the uncertainty statement targets sugar. It does not say "we are uncertain about this product's nutrition." It says "sugar data was not available; the score reflects the dimensions we could observe."

**Principle 2 — Calibrate language to data quality.**  
Full confidence → direct statements ("this product contains 8.2g protein per 100g").  
Partial confidence → hedged statements ("based on available label data, protein is approximately...").  
Insufficient confidence → no score comparison; observation only.

**Principle 3 — Uncertainty does not equal equivalence.**  
A product with high uncertainty may still be ranked if the data we do have produces a large enough score gap to exceed the confidence-adjusted threshold (Article III.5). Uncertainty reduces effective precision; it does not eliminate the comparison.

**Principle 4 — Asymmetric uncertainty must be disclosed.**  
If one product has full data confidence and the other has partial confidence, the comparison must note this asymmetry. The consumer should understand that they are comparing a fully characterized product with a partially characterized one.

#### 4.7 Reusable Explanation Framework

Every comparison explanation must follow this structure. Sections may be abbreviated or omitted only with documented justification.

```
LAYER 1 — PURPOSE STATEMENT (if divergence exists)
[State whether products serve the same purpose or diverge, before any score is shown]

LAYER 2 — SCORE DIFFERENCE
Product A: [score/grade]
Product B: [score/grade]
Delta: [X points] — [Noise / Marginal / Moderate / Material / Decisive]

LAYER 3 — SPECIFIC DRIVERS
The [X]-point difference is primarily driven by:
  · [Dimension 1]: Product A [observation]. Product B [observation].
  · [Dimension 2]: Product A [observation]. Product B [observation].
  · [Dimension 3 if applicable]

LAYER 4 — TRADEOFFS (if applicable)
On [dimension], Product B performs better than its overall score suggests: [observation].

LAYER 5 — KNOWN LIMITATIONS
  · [Distortion disclosure, if applicable]
  · [Data confidence statement, if applicable]
  · [Category-specific caveat, if applicable]

LAYER 6 — WHAT THIS SCORE DOES NOT CAPTURE
Score does not reflect: [price / taste / consumer preference / micronutrients / individual health context]
```

---

### ARTICLE V — DISTORTION REGISTRY EXPANSION

*(For registry entries DISTORTION-002 through DISTORTION-010. Full entry text follows in Section 4 of this document.)*

This constitution registers eight new distortions. DISTORTION-001 (dairy fiber, BSIP3) was registered in governance_v1.md on 2026-05-29. All entries below are documented only. None are implemented. All are reserved for BSIP3 review unless a higher-urgency escalation is triggered.

---

### ARTICLE VI — CATEGORY LAUNCH APPROVAL FRAMEWORK

#### 6.1 Purpose

No comparison category may be launched until it has cleared this formal approval checklist. "Category" here means any product group for which Bari will produce a scored, ranked comparison output accessible to consumers.

This checklist is not a suggestion. It is a hard gate.

#### 6.2 Category Launch Approval Checklist

**SECTION A — Dataset Requirements**

| Requirement | Minimum Standard | Pass Condition |
|---|---|---|
| A1. Product count | ≥ 30 products in editorial scope | Pass only if editorial scope ≥ 30 after corpus filter |
| A2. Barcode traceability | 100% of products traceable to a real retailer source | Pass only if zero invented products |
| A3. Nutritional label coverage | ≥ 80% of products have calories, protein, and carbohydrate data | Pass only if coverage ≥ 80% |
| A4. Ingredient list availability | ≥ 70% of products have ingredient list | Pass only if coverage ≥ 70% |
| A5. Image availability | ≥ 90% of editorial-scope products have a real product image | Pass only if coverage ≥ 90% |
| A6. Corpus filter documented | False positives identified and excluded with criteria stated | Pass only if filter logic is written |

**SECTION B — Category Definition Requirements**

| Requirement | Standard | Pass Condition |
|---|---|---|
| B1. Category boundary defined | Written definition of what is included and excluded | Pass only if definition exists in writing |
| B2. Sub-category structure | If multiple sub-categories exist, each has a written definition | Pass only if all sub-categories are defined |
| B3. Hybrid product protocol | Rules for hybrid products written (Article II.6) | Pass only if hybrid rules documented |
| B4. Variant policy | Rules for variant selection and inclusion written (Article II.5) | Pass only if variant rules documented |
| B5. Purpose alignment audit | All products checked against primary purpose test (Article II.1) | Pass only if purpose audit is on record |

**SECTION C — Distortion Review Requirements**

| Requirement | Standard | Pass Condition |
|---|---|---|
| C1. DISTORTION-001 review | Category reviewed for fiber-expectation applicability | Pass only if review is documented |
| C2. DISTORTION-002 through DISTORTION-010 review | Each distortion in the registry reviewed for applicability | Pass only if all 10 reviewed |
| C3. Category-specific distortion identification | Analysis performed to identify any distortions not yet in registry | Pass only if analysis documented |
| C4. Active distortion handling | Any applicable distortion either implemented, disclosed, or deferred with documented justification | Pass only if all active distortions are handled |
| C5. Endemic distortion check | Identify any distortion with ≥ 50% category prevalence; if present, activate Section 6.4 and approve disclosure text | Pass only if endemic distortions identified and disclosure text approved |

**SECTION D — Explanation Quality Requirements**

| Requirement | Standard | Pass Condition |
|---|---|---|
| D1. Representative product set reviewed | At least 5 products from the category reviewed against explanation framework (Article IV.7) | Pass only if 5 reviews documented |
| D2. No misleading explanations | No M1–M7 conditions (Article IV.2) present in reviewed explanations | Pass only if zero M-condition failures |
| D3. Tradeoff coverage | At least one material tradeoff in the category identified and explanation-tested | Pass only if tradeoff test documented |
| D4. Uncertainty language defined | Category-specific uncertainty phrasings written | Pass only if phrasings exist |
| D5. Purpose divergence pairs identified | Known purpose-divergence comparison pairs documented in advance | Pass only if pairs list exists |
| D6. Claim threshold table | Category-specific claim thresholds documented for all prevalent claim types; thresholds validated against external references where available | Pass only if threshold table is written and filed (see Guardrails v2, Section 5.2.1) |

**SECTION E — Consumer Trust Requirements**

| Requirement | Standard | Pass Condition |
|---|---|---|
| E1. Anti-drift test | Governance v1 10-question anti-drift test applied to a sample of category output | Pass only if test results documented |
| E2. No recommendation language | Sample review confirms zero recommendation-framed language in explanations | Pass only if sample is clean |
| E3. Framework invisibility test | No internal system terminology (FQC, GSS, BSIP, archetype, NOVA proxy) appears in consumer-facing output | Pass only if test passes |
| E4. Score specificity test | Each reviewed product has at minimum one specific, product-native insight (not a generic template) | Pass only if all reviewed products pass |
| E5. Governance review | At least one reviewer who did not build the category has read and signed off on sample output | Pass only if sign-off documented |

#### 6.3 Approval Decision

| Checklist result | Decision |
|---|---|
| All 27 criteria pass | Category approved for launch |
| Any B or C criterion fails | Category blocked — re-review after remediation |
| Any A criterion fails | Category blocked — data gap must be resolved |
| Any D or E criterion fails | Category conditionally blocked — explanation layer remediated and re-reviewed |

A category that is conditionally blocked may not produce public comparison output until the E criteria are re-reviewed. It may proceed to data pipeline work (BSIP0–BSIP2) during the remediation period.

---

#### 6.4 Endemic Distortion Protocol

*(Added: 2026-05-29. Source: Cereals Gap Resolution Report v1, Resolution 2.)*

**Definition:** A distortion is endemic within a category when it applies to ≥ 50% of products within that category's editorial scope.

**Trigger:** When the Section 6.2 Section C distortion review identifies a distortion as category-critical (applying to ≥ 50% of products), the Endemic Distortion Protocol is activated. A category may have more than one endemic distortion; each must be evaluated independently.

**Required action:**

A category-level distortion disclosure is required at the shelf/category page level. This disclosure is:
- Persistent (visible on category page without requiring product expansion)
- Single instance per endemic distortion (appears once per category, not per product)
- Not dismissable before reading
- Supplementary to product-level disclosures where applicable

If more than one distortion reaches endemic prevalence and both affect the same products, consolidate into a single category note listing all applicable limitations. If the endemic distortions affect distinct sub-pools within the category, pool-specific notes are preferred over consolidation — a note about plant-based fortification should not appear on dairy product cards, and vice versa.

**Standard category-level distortion disclosure format:**

```
CATEGORY NOTE — [Distortion Short Name]

[Category] products are subject to a known scoring limitation: [one sentence
describing the distortion in non-technical language].

This limitation applies to [prevalence language] of products in this category.
Scores reflect [what is measured]. Scores do not capture [what is missing].
[One sentence on practical implication for the consumer's use of the score.]
```

**Graduated prevalence language:**

| Affected proportion | Required language |
|---|---|
| 50–65% of products | "approximately half of products" |
| 66–79% of products | "the majority of products" |
| 80–100% of products | "most products in this category" |

**Reference example — DISTORTION-004 in Cereals:**

```
CATEGORY NOTE — Fortification

Breakfast cereal products are frequently enriched with vitamins and minerals
(iron, B vitamins, calcium, vitamin D). Bari's current scores do not include
micronutrient contribution as a positive factor.

This limitation applies to most products in this category. Scores reflect
macronutrient architecture, processing quality, and ingredient integrity.
Scores do not capture the nutritional value of added vitamins and minerals.
A fortified product may deliver meaningful micronutrient benefit not visible
in its score.
```

**Documentation requirement:** The category launch record must document which distortions triggered the Endemic Distortion Protocol, the prevalence estimate, and the exact disclosure text approved for production.

**Scope:** This protocol applies to all Bari categories. When a category launches with an endemic distortion, the disclosure format is approved as part of the Section 6.2 Section C checklist review (criterion C5).

---

## 4. Distortion Registry Expansion

**Registry format:** Each entry includes an ID, title, description, why it is dangerous, a category example, and a proposed governance response. No fixes are implemented here. All entries are deferred to BSIP3.

---

### DISTORTION-002 — Protein Inflation Distortion

**ID:** DISTORTION-002  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** מעדנים, יוגורט, חטיפים, משקאות, דגני בוקר

**Description:**  
BSIP2's protein score treats all protein sources as equivalent per gram. A product with 15g of protein from industrial whey isolate (NOVA 4 ingredient) receives the same protein_score as a product with 15g of protein from whole-food Greek yogurt. The score rewards protein quantity but does not distinguish protein source quality, bioavailability profile, or processing origin.

**Why it is dangerous:**  
In comparison contexts, products specifically engineered for protein content (using isolated proteins, concentrate blends, or amino acid fortification) can score alongside or above products whose protein is structurally integral to the food matrix. This creates the impression that an engineered protein product and a whole-food protein product are equivalent — or that the engineered product is superior — when the engineering itself is a NOVA-penalized attribute that the protein score does not offset.

Additionally, consumers who encounter a protein-forward comparison may conclude that any "protein" product outperforms conventional alternatives, regardless of the processing cost that produced the protein concentration.

**Example:**  
A protein pudding (מעדן חלבון) with 15g protein from whey concentrate, 8 additives, NOVA 4, scores comparably on protein_score to plain Greek yogurt (5% fat) with 10g naturally occurring milk protein, zero additives, NOVA 1. The protein dimension rewards the engineered product; the NOVA penalty partially corrects but does not fully offset.

**Proposed governance response (BSIP3):**  
Evaluate a protein source quality modifier: whole-food protein (dairy, legume, nut, egg matrix) vs. added isolated protein (whey isolate, casein, soy isolate, pea isolate). Modifier would reduce effective protein weight for isolated-protein products — not eliminate the credit, but reduce it by a calibrated factor. Gate: requires food science validation before implementation.

---

### DISTORTION-003 — Fiber Inflation Distortion

**ID:** DISTORTION-003  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** חטיפים, דגני בוקר, לחם, שתייה, מוצרי יוגורט עשירים

**Description:**  
BSIP2's fiber score treats all fiber sources as equivalent per gram. A product with 6g of fiber from added inulin (chicory root extract, a common industrial prebiotic added to processed foods) receives the same fiber_score as a product with 6g of fiber from oat bran, wheat germ, or whole grain matrix. The distinction matters: whole-food fiber is associated with established satiety and digestive effects; added isolated fiber (particularly inulin at high doses) has variable tolerability and a different fermentation profile.

**Why it is dangerous:**  
Products that add isolated fiber to achieve a "high fiber" claim can receive a substantial fiber_score boost. In a comparison, this inflates their score relative to whole-food alternatives whose fiber is nutritionally embedded but lower in absolute quantity. A consumer reading the comparison concludes that the industrial fiber-enriched product is nutritionally superior — an inference the current scoring architecture technically supports but which may not reflect nutritional reality.

**Example:**  
A snack bar with 8g fiber (7g from added inulin, 1g intrinsic) scores identically on fiber_score to a whole-grain bar with 8g fiber from oat matrix. The processing differences are captured partially by NOVA, but the fiber quality distinction is entirely absent from the score.

**Proposed governance response (BSIP3):**  
Evaluate a fiber source classification layer: intrinsic/matrix fiber (from whole grain, legume, vegetable, fruit) vs. added isolated fiber (inulin, chicory, polydextrose, FOS, pectin isolate). Apply a source quality multiplier that reduces effective fiber credit for isolated-fiber products below the whole-food equivalent. Gate: fiber classification requires ingredient parsing improvements (BSIP1 upgrade) and food science validation.

---

### DISTORTION-004 — Fortification Distortion

**ID:** DISTORTION-004  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** חלב, חלופות חלב, דגני בוקר, מוצרי לחם, שתייה

**Description:**  
Products enriched with vitamins and minerals (calcium, vitamin D, B12, iron, zinc) receive no positive credit in BSIP2's current scoring architecture — the micronutrient dimension does not exist. At the same time, the additives used to fortify (e.g., cholecalciferol, cyanocobalamin, ferric pyrophosphate) contribute to the additive count, which can influence NOVA classification and additive penalty. The result is a double-disadvantage: no benefit for the fortification, partial penalty for the additives used to deliver it.

**Why it is dangerous:**  
For product categories where fortification addresses a genuine public health need — calcium and vitamin D in dairy alternatives, B12 in plant-based products, iron in fortified cereals — this distortion systematically underscores products that have been designed to compensate for known dietary gaps. A comparison between fortified oat milk and unfortified oat milk, or between fortified cereal and whole-grain cereal, will not reflect the legitimate nutritional contribution of the fortification.

**Example:**  
Fortified oat milk (calcium, B12, vitamin D, vitamin E added) vs. plain oat milk (unfortified). The fortified version has additional additives from the fortification compounds; it may receive a higher additive count. The nutritional benefit of the fortification (addressing known deficiencies in plant-based diets) is entirely invisible to BSIP2.

**Proposed governance response (BSIP3):**  
Evaluate a fortification credit system: a small positive adjustment for products where fortification addresses documented category-specific nutrient gaps (e.g., B12 in plant-based, calcium in dairy alternatives, iron in complementary cereals). Gate: requires defining which nutrients qualify, which categories they apply to, and minimum fortification thresholds. Must not create a pathway for gaming via cosmetic over-fortification.

---

### DISTORTION-005 — Premium Product Distortion

**ID:** DISTORTION-005  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 editorial and methodology governance  
**Cross-category applicability:** Universal — all categories

**Description:**  
BSIP2 scores products on nutritional architecture only. It does not observe price, brand tier, or market positioning. A premium organic product and a budget conventional product with identical nutritional profiles will receive identical scores. This is architecturally correct — Bari evaluates nutrition, not value-for-money — but it creates a comparison output that can surprise consumers who expect Bari to affirm or challenge the premium pricing narrative.

The distortion operates in the reverse direction too: a premium product may carry a marketing story that implies nutritional superiority (organic, artisanal, heritage grain) and when that story is not reflected in the score, the consumer may lose trust in either Bari or the product, without understanding that the story was marketing, not nutrition.

**Why it is dangerous:**  
Not dangerous in scoring terms, but dangerous in consumer trust terms. When Bari assigns the same score to an expensive "clean label" product and a cheap conventional alternative, consumers may assume Bari made an error. If the explanation does not address this, consumer confidence in the comparison erodes.

**Example:**  
Organic plain yogurt at 18 NIS vs. conventional plain yogurt at 7 NIS, both NOVA 1, both with identical macro profiles. Bari scores them identically. The consumer who paid 11 NIS more for the organic product may experience this comparison as undermining rather than clarifying.

**Proposed governance response (BSIP3):**  
This is primarily an explanation governance issue, not a scoring issue. Develop a standard explanation protocol for premium product comparisons that explicitly addresses: "Bari's score reflects nutritional architecture only. Price, sourcing practices, environmental credentials, and brand values are not scored." No scoring changes required; explanation layer update needed.

---

### DISTORTION-006 — Low-Calorie Halo Distortion

**ID:** DISTORTION-006  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** שתייה, מוצרי דיאט, יוגורט דל שומן, חטיפי אוויר

**Description:**  
A very low calorie product can achieve a moderate score in BSIP2 because its absolute nutrient deficiencies are not penalized proportionally to its caloric contribution. A product with 15 calories per 100g, minimal protein, minimal fiber, and minimal sugar has very low absolute scores across all dimensions — but the composite score is not heavily penalized because the absolute values are all small. The consumer may interpret a score of 45/D for a flavored water or a diet gelatin as reasonable nutritional quality, when the product's actual nutritional contribution is near zero.

**Why it is dangerous:**  
In comparisons with low-calorie diet products, a product that delivers genuinely empty calories (water, artificial sweetener, flavoring, no nutritional contribution) can score in the same range as a product with moderate but real nutritional content. The comparison does not capture the distinction between "low nutritional cost" and "meaningful nutritional value."

**Example:**  
Diet fruit syrup (5 calories per 100ml, no macros, artificial sweeteners) vs. plain yogurt (80 calories per 100g, 10g protein). The syrup may score 38/E; the yogurt may score 52/C. The 14-point gap correctly places the yogurt higher, but the comparison frame implies the syrup has 38 units of nutritional value rather than approximately zero nutritional value with a low-calorie profile.

**Proposed governance response (BSIP3):**  
Evaluate a minimum caloric substance threshold: products below a defined caloric floor (e.g., <20 kcal per 100g/ml) are categorized as "condiments / caloric non-contributors" and excluded from direct nutritional comparison with whole-food products. They may have their own internal comparison tier. Gate: threshold definition and category boundary rules required.

---

### DISTORTION-007 — Natural Sugar Distortion

**ID:** DISTORTION-007  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** מוצרי חלב, פירות, מיצים טבעיים, יוגורט עם פירות

**Description:**  
BSIP2 applies a sugar penalty based on total sugar content per 100g/ml. This penalty does not distinguish between:
- Lactose (naturally occurring milk sugar, structurally integral to dairy matrix)
- Intrinsic fruit sugars (fructose in whole fruit matrix with fiber)
- Added sucrose or glucose-fructose syrup (refined, rapidly metabolized)

All three are captured in the "sugars" row of the nutritional label and treated equivalently by the scoring engine. This means a plain yogurt with significant lactose content is penalized identically to a yogurt with added sucrose — despite the fact that lactose and sucrose have meaningfully different metabolic and glycemic profiles.

**Why it is dangerous:**  
In dairy comparisons, naturally lactose-containing products receive the same sugar penalty as sugar-added products. In fruit comparisons, whole fruit products receive the same penalty as added-sugar products. The comparison systematically undervalues the nutritional difference between naturally occurring sugar matrices and refined added-sugar products.

**Example:**  
Plain 3% yogurt with 4.5g lactose per 100g vs. fruit yogurt with 4.5g sugar (2g lactose + 2.5g added sucrose). Both receive identical sugar penalties. The plain yogurt's lactose is nutritionally integral to the dairy matrix; the fruit yogurt's added sucrose is not. BSIP2 does not distinguish these.

**Proposed governance response (BSIP3):**  
Evaluate a sugar source modifier: if added sugars are explicitly declared on the label (as is increasingly required by Israeli labeling regulations), use added sugar rather than total sugar as the primary penalty driver. For categories where added sugar declaration is unavailable, maintain total sugar penalty with a category-calibrated floor that accounts for expected natural sugar content (e.g., dairy floor of 3.5g per 100g for lactose). Gate: requires ingredient parsing to identify sugar source from label language; Israeli labeling regulation review.

---

### DISTORTION-008 — Category Mismatch Distortion

**ID:** DISTORTION-008  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 editorial and methodology governance  
**Cross-category applicability:** Universal — comparison methodology

**Description:**  
When products from different true categories are placed in the same comparison group because of shared shelf position or shared marketing claim, BSIP2 applies a uniform scoring architecture that may not be appropriate for all products in the group. The score differences that emerge may reflect category-architectural incompatibility rather than genuine nutritional differences.

**Why it is dangerous:**  
In the snack bars category, comparing date bars (whole food, high natural sugar, minimal processing) to protein bars (engineered, isolated protein, complex additive list) using the same scoring architecture produces rankings that reflect the architecture's biases as much as the products' actual differences. A date bar may score lower on protein_score (correctly) and higher on NOVA (correctly) — but the composite score comparison implies the two products are in direct nutritional competition for the same consumer decision, which they may not be.

**Example:**  
Date-based energy ball (NOVA 2, 2g protein, 22g natural sugar from dates) vs. protein bar (NOVA 4, 20g whey protein, 5g added sugar). The protein bar scores higher on protein_score; the date ball scores higher on NOVA. The composite comparison produces a number. But the consumer who eats date balls and the consumer who eats protein bars are typically making different decisions, for different purposes, at different consumption occasions.

**Proposed governance response (BSIP3):**  
Strengthen the purpose alignment test (Article II.1) at category design time. Require explicit category architecture documents that identify internal sub-groups and apply the comparison eligibility framework (Article II) before including products in the same ranking pool. Sub-groups should be ranked internally; cross-sub-group comparisons should require purpose divergence disclosure.

---

### DISTORTION-009 — Additive Overreaction Distortion

**ID:** DISTORTION-009  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** Universal — all NOVA 4 products

**Description:**  
BSIP2 applies a uniform NOVA 4 penalty regardless of additive function or necessity. A product with three food-safety additives (preservatives required by regulation to prevent pathogen growth in ambient-shelf products) receives the same NOVA 4 classification and additive penalty as a product with eight cosmetic additives (artificial colors, flavor enhancers, sweeteners added for consumer appeal with no safety function). The penalty does not distinguish between additives that serve technical/safety functions and additives that serve commercial/cosmetic functions.

**Why it is dangerous:**  
In comparison contexts, a product that is NOVA 4 due to necessary food safety additives is penalized identically to a product that is NOVA 4 due to cosmetic over-engineering. This creates a comparison distortion where a technically necessary additive profile and a commercially driven additive profile produce equivalent scores. Consumers who value "clean label" products may be misled into believing a product is cosmetically over-processed when it is actually safety-processed.

**Example:**  
An ambient-shelf dessert product with sodium benzoate, potassium sorbate (two standard preservatives required for shelf stability without refrigeration) receives the same additive penalty contribution as a competing product with the same preservatives plus three artificial colors, two synthetic flavors, and a sweetener blend. Both are NOVA 4; both receive the same cap and penalty structure.

**Proposed governance response (BSIP3):**  
Evaluate an additive function classification layer: technical/safety additives (preservatives, antioxidants, pH regulators, emulsifiers required for food safety) vs. commercial additives (artificial colors, synthetic flavors, sweeteners, texture enhancers added for consumer appeal). Apply a reduced penalty for technical-only additive profiles within NOVA 4. Gate: requires additive classification database (E-number function mapping); significant BSIP1 enrichment upgrade.

---

### DISTORTION-010 — Macro Obsession Distortion

**ID:** DISTORTION-010  
**Status:** Documented. Not implemented. Reserved for BSIP3.  
**Owner:** BSIP3 scoring architecture  
**Cross-category applicability:** Universal — all categories

**Description:**  
BSIP2's nutrient density dimension is currently defined by protein and fiber, the two macronutrients most commonly correlated with satiety, muscle maintenance, and digestive health in the evidence base. This two-macro architecture means that products with excellent protein and fiber scores can achieve high nutrient density scores even when other nutritionally significant factors are absent or adverse: sodium content, saturated fat proportion, glycemic load, or micronutrient profile.

**Why it is dangerous:**  
A product scoring well on protein and fiber can achieve a B grade even if it is very high in sodium (relevant for cardiovascular health) or saturated fat (relevant for lipid health). In a comparison, the B-grade product appears to be the superior nutritional choice. The consumer takes away the conclusion that protein + fiber = good nutrition, which is an oversimplification that BSIP2's architecture inadvertently reinforces.

**Example:**  
A processed cheese product with 18g protein per 100g and 2g fiber (from added fiber) scores well on nutrient density. Its saturated fat content (12g per 100g) and sodium content (800mg per 100g) are not scored as adverse signals in BSIP2's current architecture. In comparison with a lower-protein but lower-saturated-fat product, the processed cheese may rank higher despite a nutritional profile that many dietitians would consider less favorable overall.

**Proposed governance response (BSIP3):**  
Evaluate expanding nutrient density to include: (a) a sodium penalty modifier for products exceeding a category-specific sodium threshold; (b) a saturated fat modifier for products in categories where saturated fat is a dominant risk signal (cheese, meat products, full-fat dairy); (c) potential for a net nutrient score that accounts for both positive macros and limiting macros simultaneously. Gate: requires category-specific threshold calibration; significant architecture change with regression risk across all scored categories.

---

## 5. Recommendations

**Recommendation 1 — Adopt this constitution as the governing document before any new category is launched.**  
The current pipeline has לחם and חלב queued. Both require a distortion review against the full registry (DISTORTION-001 through DISTORTION-010) before their comparison pages are considered production-ready. The Category Launch Approval Checklist (Article VI) must be applied to both.

**Recommendation 2 — Run DISTORTION-002 and DISTORTION-007 as priority BSIP3 investigations.**  
The protein source distortion (DISTORTION-002) and natural sugar distortion (DISTORTION-007) have the highest cross-category impact and the clearest implementation path. Both require ingredient parsing improvements, but the governance rule is conceptually straightforward. These should lead BSIP3 calibration work.

**Recommendation 3 — Formalize the "effectively equivalent" finding as a standard output type.**  
Currently, Bari's comparison output assumes that a score difference always justifies a ranking. This constitution establishes that products within 2 points — or within 6 points under partial confidence — should be declared equivalent. This needs to become a standard content pattern with editorial support, not an exception case.

**Recommendation 4 — Develop purpose divergence disclosure templates for the three highest-risk comparison pairs in each category.**  
For every category, there are two or three known high-stakes comparisons where purpose divergence is likely. For מעדנים: protein dessert vs. traditional dessert. For לחם: keto bread vs. whole grain bread. For חלב: plant-based alternatives vs. dairy milk. These templates should be written at category launch time, not ad hoc when the comparison surfaces.

**Recommendation 5 — Establish a distortion review sprint as part of BSIP3 planning.**  
The ten distortions documented in this constitution were identified through category analysis rather than dedicated investigation. A BSIP3 distortion review sprint — examining real product data for systematic scoring anomalies across categories — is likely to surface additional entries. This review should precede BSIP3 architecture decisions.

---

## 6. Risks

**Risk 1 — Effective equivalence frustrates engagement.**  
If Bari implements the equivalence threshold rigorously, a significant percentage of comparisons across all categories will conclude "these products are not meaningfully different." This is the honest answer. It is also potentially frustrating for consumers who came to a comparison expecting a clear winner. Risk of low consumer satisfaction with honest findings. Mitigation: invest in explanation quality that makes equivalence findings intellectually satisfying, not anticlimactic.

**Risk 2 — Purpose divergence disclosure is skipped under editorial time pressure.**  
The most easily violated rule in this constitution is the purpose divergence disclosure. It requires judgment about consumer intent, which is slower than reading a score differential. Under production pressure, it is the rule most likely to be abbreviated or omitted. Mitigation: build purpose divergence review into the category launch checklist (done — Section E, requirement E1/E2) and into the production pass QA protocol.

**Risk 3 — The distortion registry creates paralysis.**  
Ten documented distortions — none implemented — represents a catalog of known imperfections in the current scoring architecture. Stakeholders reviewing this list may conclude that Bari's scores are unreliable. The risk is a crisis of confidence rather than a governance improvement. Mitigation: the registry is a sign of epistemic honesty, not evidence of systematic failure. The distortions are bounded, documented, and have defined resolution paths. The answer to "Bari knows its scores have these limitations" is "that is exactly what a trustworthy scoring system looks like."

**Risk 4 — New category launches are delayed by the approval checklist.**  
The Category Launch Approval Checklist has 25 criteria across five sections. Some criteria require writing that currently doesn't exist (category boundary definition, purpose divergence pairs, uncertainty language). For categories that are data-ready but documentation-poor, the checklist will delay launch. Mitigation: the checklist is designed to prevent consumer trust failures, not to create bureaucracy. The criteria are proportionate. The cost of a failed comparison category is higher than the cost of a checklist.

**Risk 5 — Distortion-flagged comparisons are published before BSIP3 resolution.**  
The registry documents distortions but does not prevent their effects from appearing in comparison output. A protein pudding vs. plain yogurt comparison will proceed under DISTORTION-002 conditions regardless of its registry status. Mitigation: the explanation framework (Article IV.4, T4 principle, tradeoff communication Principle 4) requires disclosure when a comparison involves a distortion-flagged dimension. Disclosure does not eliminate the distortion; it makes it visible to the consumer.

---

## 7. Open Questions

**OQ-001 — What is the minimum score delta for a comparison to be worth publishing at all?**  
This constitution establishes that ≤2 points = noise. But it does not establish whether a comparison page should exist at all for products in the noise range. Should Bari produce comparison output for two products with a 1-point delta? The philosophical answer is yes — equivalence is a legitimate finding. The consumer experience question is unresolved.

**OQ-002 — How is the purpose test operationalized for products with ambiguous marketing?**  
The primary purpose test (Article II.1) requires judgment about what a consumer purchases a product for. For products with genuinely ambiguous positioning (a product marketed as both "breakfast option" and "afternoon snack"), the classification is not algorithmic. A documented decision process for ambiguous cases does not yet exist.

**OQ-003 — Does the equivalence threshold differ by grade tier?**  
A 3-point difference between two products at 68/B and 65/B crosses the grade boundary. A 3-point difference between 52/C and 49/D also crosses a grade boundary. Under the current framework, both are "marginal" differences. Should grade boundary crossings receive special treatment, given their consumer-facing significance? Unresolved.

**OQ-004 — How does the distortion registry interact with the comparison at consumer level?**  
This constitution specifies that distortion disclosures must appear in explanations (Article IV.4). It does not specify the format, length, or prominence of that disclosure. A one-line footnote and a prominent callout both technically satisfy the requirement. The appropriate consumer-facing format is an editorial question not resolved here.

**OQ-005 — What is the governance path for retiring a distortion from the registry?**  
Distortions are registered when documented. BSIP3 is designated as the resolution body. But what constitutes resolution? A partial mitigation (reducing the effect but not eliminating it), a full mitigation (eliminating the effect), or a documented acceptance that the distortion is structural and irreducible? The retirement criteria for each registry entry are not yet defined.

**OQ-006 — Does the comparison eligibility framework apply retroactively to the מעדנים comparison page?**  
The מעדנים comparison page was built before this constitution existed. Several comparisons on that page may require review under the purpose divergence rules (Article II.7). A formal retroactive review of מעדנים against this constitution is not yet scheduled.

---

*Bari Comparison Governance Constitution v1*  
*CE Controller 1 — Chief Nutrition, Scoring & Content Architect*  
*2026-05-29*  
*Governed by: Bari Governance v1*  
*All distortion entries reserved for BSIP3 review.*
