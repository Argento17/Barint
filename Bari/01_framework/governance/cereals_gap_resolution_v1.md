# Cereals Governance Gap Resolution Report v1

**Classification:** Governing Document — Internal  
**Issued:** 2026-05-29  
**Author:** CE Controller 1 — Chief Nutrition, Scoring & Content Architect  
**Status:** Active — governance resolutions to be applied before cereals category launch  
**Precondition:** Bari Governance Stress Test — Breakfast Cereals Category Audit v1 (`category_audit_cereals_v1.md`)  
**Governed by:** Bari Governance v1, Comparison Governance Constitution v1, Consumer Use-Case & Purpose Guardrails v2

---

## 1. Executive Summary

The Cereals Governance Stress Test (2026-05-29) returned a verdict of C: governance gaps block category launch. Four gaps were identified, two classified as critical.

This document resolves all four.

The resolutions are minimal. They do not create new frameworks. They amend two existing governance documents at specific, targeted locations. Three gaps are resolved by amendments to the Comparison Governance Constitution v1. One gap is resolved by an amendment to the Consumer Use-Case & Purpose Guardrails v2. The fourth gap, granola pool assignment, is resolved as a standing precedent derivable from rules already in the Constitution — no new document is required.

**Resolutions summary:**

| Gap | Type | Resolution | Document amended |
|---|---|---|---|
| Gap 1 — Children's cereal definition | Amendment | Operational definition added to Article II | Constitution v1 |
| Gap 2 — Endemic distortion disclosure | Amendment | Endemic Distortion Protocol added to Article VI | Constitution v1 |
| Gap 3 — Granola sub-category pool | Standing precedent | NOVA + macro divergence rule applied | Constitution v1 (Article II, Rule 2) |
| Gap 4 — Whole grain threshold | Amendment | Claim threshold table added to Section 5.2 | Guardrails v2 |

**Launch readiness reassessment:** If all four resolutions are adopted, cereals becomes **B — Launch Ready with Conditions**. The governance is resolved. Data pipeline conditions remain.

**Meta-finding:** All four gaps are generic, not cereals-specific. Each resolution should be applied universally across all future Bari categories. Bread, milk, cheese, and protein bars are all exposed to the same gaps in their current or anticipated form.

---

## 2. Gap Review

### Gap 1 — Children's Cereal Operational Definition

**Description:**  
The Comparison Governance Constitution v1, Article II, Section 2.7, explicitly prohibits comparing children's cereals against adult cereals ("different nutritional standards, different regulatory context, different target consumer — do not rank"). But no governance document defines what makes a product a "children's product." The prohibition exists; the trigger condition to activate it does not.

**Why it emerged:**  
The Constitution was written from the מעדנים category, where the children's product problem is minor (a children's yogurt is recognizable on sight). Cereals is the first category where the children's definition becomes operationally necessary — where a shelf contains Frosties, Kellogg's Coco Pops, Nesquik cereal, and granola alongside family and adult products, all in the same aisle. The definition gap was latent and was surfaced when cereals stress-tested the eligibility rules.

**Severity:** CRITICAL  
Without a definition, the absolute prohibition on children/adult comparison cannot be applied consistently. Products can slip in or out of the protected pool based on analyst judgment, creating comparison legitimacy risks and consumer trust failures.

**Which document failed:**  
Constitution v1, Article II, Section 2.3 (Absolute Restrictions), Section 2.7 (Purpose-Based Comparison Rules). Both sections reference children's products without defining them.

---

### Gap 2 — Category-Level Distortion Disclosure Format

**Description:**  
The Constitution v1, Article IV, Section 4.4, Principle 4 requires that "comparisons involving a distortion-flagged dimension must disclose that the scoring architecture has a known limitation in this area." This disclosure mechanism operates at the product level — it appears in the explanation for a specific comparison. In cereals, DISTORTION-004 (fortification) affects the majority of products in the category. When a distortion is endemic (applying to most products), product-level disclosure becomes informationally useless: every comparison carries the same footnote, consumers stop reading it, and the disclosure function degrades to noise.

No format exists for disclosing endemic distortions at the category or shelf level.

**Why it emerged:**  
The Constitution correctly anticipated per-product distortion disclosure. It did not anticipate the scenario where a registered distortion reaches category-critical prevalence. DISTORTION-004 is the first instance of a distortion that is not an edge case in a category — it is the default condition. The Constitution has no mechanism for this.

**Severity:** CRITICAL  
A distortion affecting the majority of products in a category is the highest-risk disclosure scenario. Individual-product disclosure is insufficient. Without a category-level format, the distortion registry produces no actionable output for the consumer in the categories where it matters most.

**Which document failed:**  
Constitution v1, Article VI (Category Launch Approval Framework). The launch checklist requires distortion review but specifies no output format for endemic distortions. Article IV (Explanation Governance) defines only product-level disclosure mechanisms.

---

### Gap 3 — Granola Sub-Category Pool Ruling

**Description:**  
Granola is architecturally distinct from the general breakfast cereals category: typically NOVA 3–4, high added sugar (10–30g/100g), high fat from added oils, nuts, and syrups. It simultaneously appears to qualify for Lens 2 (fiber and protein signals from nuts and oats) while being nutritionally closer to a confection than a cereal. The Consumer Use-Case Guardrails v2, Lens Application Rule 5 says "Ambiguous cases default to Lens 1." Applying this rule places granola in the general cereal comparison pool alongside flaked whole grain cereals and muesli — products with radically different nutritional architectures and consumer expectations. The Constitution's Article II, Rule 2 requires that "sub-category comparisons require sub-category definition" but no sub-category definition for granola exists.

**Why it emerged:**  
Granola is a product category that presents as a cereal but is architecturally a processed confection with wellness marketing. No existing governance document addresses the scenario where a product sub-category's architectural profile diverges so significantly from the parent category that inclusion in the same comparison pool distorts the comparison for all products in that pool.

**Severity:** SIGNIFICANT  
Without a ruling, granola is either improperly included in the general cereal pool (producing misleading comparisons) or arbitrarily excluded without a documented basis (violating the category definition requirement). Neither outcome satisfies governance integrity.

**Which document failed:**  
Constitution v1, Article II, Rule 2 (Sub-category comparisons require sub-category definition). The rule exists; the mechanism for resolving ambiguous sub-categories in real categories is not specified.

---

### Gap 4 — Whole Grain Marketing Divergence Threshold

**Description:**  
"Whole grain" is the most prevalent marketing claim in the breakfast cereals category. The Consumer Use-Case Guardrails v2, Section 5.2, Condition 2 states that a Marketing Divergence Finding is triggered when "the claim implies a specific nutritional standard in its ordinary meaning." For "whole grain," this condition cannot be evaluated without a quantitative threshold defining what "whole grain" implies. Without that threshold, the Marketing Divergence Finding — Bari's most powerful analytical output for claim verification — cannot be applied to the most common claim in the category.

**Why it emerged:**  
The Guardrails v2 framework is claim-agnostic by design. It requires that thresholds be defined at category launch. For claims where international consensus thresholds exist (protein, keto/carbohydrate, CFU for probiotics), the category-launch process would normally supply them. "Whole grain" has no Israeli regulatory threshold, and no international consensus threshold was imported at governance design time. The gap was not visible until a specific category was applied.

**Severity:** SIGNIFICANT  
Without a threshold, the Marketing Divergence Finding framework produces no outputs for the most prevalent claim type in cereals. The most common marketing lever in the category operates without any Bari analytical check.

**Which document failed:**  
Consumer Use-Case & Purpose Guardrails v2, Section 5.2 (Condition 2). The framework is correctly structured; the calibration constant for this specific claim type is absent.

---

## 3. Root Cause Analysis

### Gap 1 — Root Cause

**Type: Missing governance — complete absence, not ambiguity.**

The prohibition on children/adult comparisons in the Constitution was written as a categorical rule referencing a class of products that was never operationally defined. The rule assumed that "children's product" was self-evident. In simple categories (children's yogurt has a cartoon mascot, child-sized serving, and is on a shelf with adult yogurts) this assumption holds. In cereals (where adult products also have mascots, where family cereals blur the children's boundary, and where serving size varies from 25g to 55g depending on product type), the assumption fails.

This is a gap in the Constitution's eligibility framework, not in the prohibition rule itself. The rule is correct. The operationalization was not done.

**Not applicable:** No governance conflict. No category-specific limitation. The issue is simply a missing definition that the governance author assumed would be obvious.

---

### Gap 2 — Root Cause

**Type: Framework limitation — the per-product disclosure mechanism does not scale to endemic prevalence.**

The Constitution's distortion disclosure requirement was designed for the individual comparison case: "this specific comparison is affected by this specific distortion." That design is correct for distortions that affect a minority of products or a specific sub-category. It becomes structurally inadequate when a distortion is endemic.

The framework limitation is architectural: the disclosure mechanism has only one mode (per-product). A category-level mode was never built because no existing category had encountered a category-critical distortion before cereals. This is a genuine framework gap triggered by an edge case the framework was not designed to handle.

**Not applicable:** No governance conflict. No ambiguity — the rule is clear at the product level. The gap is in the absence of a parallel rule for the category level.

---

### Gap 3 — Root Cause

**Type: Category-specific edge case within an existing ambiguous governance rule.**

The Constitution's sub-category rule (Article II, Rule 2) correctly requires sub-category definitions. It does not specify how to generate those definitions or what to do when a product is simultaneously a plausible member of multiple sub-categories. The Guardrails v2 Lens 1 default correctly handles lens assignment (granola goes to Lens 1). But Lens assignment and sub-category pool assignment are distinct questions. Lens governs the type of consumer comparison; pool governs which products are ranked together.

The gap is that the Constitution addresses the existence of sub-category rules but not the process for creating them when a product's architecture places it at a category boundary. This is an ambiguous governance situation — the rules exist but produce no determinate answer for the edge case.

**Partially applicable:** Governance ambiguity (which pool does granola belong to given Article II, Rule 2's requirement for a definition?) + Category-specific edge case (granola's architecture is unusual in cereals in a way that no existing governance document anticipated).

---

### Gap 4 — Root Cause

**Type: Missing governance — calibration constant not supplied.**

The Guardrails v2 framework is structurally sound but its Condition 2 trigger requires category-specific threshold inputs. The framework correctly deferred threshold definition to category launch. The category launch governance (Constitution v1, Article VI) does not include a requirement to document claim thresholds as part of the launch checklist. The result: the governance framework assumed thresholds would be supplied at launch; the launch checklist did not mandate their documentation; no threshold was produced.

This is a missing governance gap distributed across two documents. The Guardrails v2 correctly implies that thresholds are needed; the Constitution's Article VI launch checklist doesn't mandate their creation.

---

## 4. Resolution Proposals

---

### Resolution 1 — Children's Product Operational Definition

**Recommended action: Amendment to Constitution v1, Article II.**

Add a new Section 2.8 — Developmental Product Definition. This section provides the operational definition missing from the absolute restrictions and purpose-based comparison rules.

---

**Exact governance change:**

Add the following as Section 2.8 to Article II of the Comparison Governance Constitution v1:

---

> **2.8 Developmental Product Definition**
>
> A product is classified as a developmental / children's product when it satisfies any **two or more** of the following four indicators. All indicators are observed from the product record; none rely on manufacturer self-declaration.
>
> **Indicator D1 — Visual targeting:**  
> Primary packaging features animated characters, anthropomorphized mascots, cartoon imagery, or child-directed visual language whose primary design audience is children under 12. Mascots used consistently by an adult-positioned brand do not qualify (e.g., a bear mascot on an adult granola brand is not a child-targeting signal if the product is marketed to adults).
>
> **Indicator D2 — Name or pack language:**  
> Product name or primary pack copy includes explicit child-targeting terms: "ילדים," "kids," "junior," "little," "mini" when referring to child-sized portions (not product dimensions), or developmental stage language ("toddler," "school age," or age ranges below 12).
>
> **Indicator D3 — Pediatric serving size:**  
> Declared serving size is ≤ 25g (breakfast cereal context) or ≤ 30g (snack context). Adult cereals typically declare 30–55g servings; pediatric products typically declare 20–30g.
>
> **Indicator D4 — Developmental marketing claim:**  
> Product carries an explicit developmental positioning claim: "supports growth," "for growing bodies," "school nutrition," or a comparable claim that refers to the developmental needs of children under 12 as the primary stated purpose.
>
> **Classification requires any two indicators concurrently present.**
>
> **Anti-gaming provision:** A product that historically qualified as a children's product (by any two indicators) does not escape classification by removing one indicator through packaging redesign while retaining the other. Classification history is retained.
>
> **Classification consequences:**
> - Classified developmental products are not ranked against non-developmental products under any lens
> - They are compared within a developmental-product sub-pool only
> - Score and architecture are reported honestly; the developmental context is stated before any score
> - Classification cannot improve a product's score (Anti-Immunity Rule applies)
>
> **Scope:** This definition applies to all Bari categories, not only to cereals. The indicators are calibrated for the cereal context (Indicator D3 serving size threshold); other categories may require category-specific threshold calibration for Indicator D3, documented at category launch.

---

**Risks:**
- The two-indicator requirement may produce false negatives for products that clearly target children but satisfy only one indicator. Mitigation: D1 is typically the most visible signal; a product with animated characters that lacks any other indicator is a genuine edge case and should be resolved by CE Controller 1 judgment on a case-by-case basis.
- The 25g pediatric serving threshold for cereals may require adjustment if cereal data reveals a different distribution. Mitigation: the serving size threshold is calibrated at BSIP time from the actual cereal corpus.

**Alternative options:**
- Single-indicator classification (only D1 or D2 required): higher recall, more false positives; gaming risk increases
- Manufacturer declaration: simpler but exploitable in both directions
- Regulatory reference: Israel does not have a formal regulatory definition of "children's food" for marketing purposes; a regulatory anchor is not currently available

---

### Resolution 2 — Endemic Distortion Protocol

**Recommended action: Amendment to Constitution v1, Article VI.**

Add a new Section 6.4 — Endemic Distortion Protocol. This section addresses the scenario where a distortion reaches category-critical prevalence and product-level disclosure is insufficient.

---

**Exact governance change:**

Add the following as Section 6.4 to Article VI of the Comparison Governance Constitution v1:

---

> **6.4 Endemic Distortion Protocol**
>
> **Definition:** A distortion is endemic within a category when it applies to ≥ 50% of products within that category's editorial scope.
>
> **Trigger:** When the Article VI Section C distortion review identifies a distortion as category-critical (applying to ≥ 50% of products), the Endemic Distortion Protocol is activated.
>
> **Required action:**
>
> A category-level distortion disclosure is required at the shelf/category page level. This disclosure is:
> - Persistent (visible on category page without requiring product expansion)
> - Single instance (appears once per category, not per product)
> - Not dismissable before reading
> - Supplementary (does not replace product-level disclosures where applicable)
>
> **Standard category-level distortion disclosure format:**
>
> ```
> CATEGORY NOTE — [Distortion Short Name]
> 
> [Category] products are subject to a known scoring limitation: [one sentence 
> describing the distortion in non-technical language].
> 
> This limitation applies to approximately [X]% of products in this category. 
> Scores reflect [what is measured]. Scores do not capture [what is missing]. 
> [One sentence on practical implication for the consumer's use of the score].
> ```
>
> **Example — DISTORTION-004 in Cereals:**
>
> ```
> CATEGORY NOTE — Fortification
> 
> Breakfast cereal products are frequently enriched with vitamins and minerals 
> (iron, B vitamins, calcium, vitamin D). Bari's current scores do not include 
> micronutrient contribution as a positive factor.
> 
> This limitation applies to the majority of products in this category. Scores 
> reflect macronutrient architecture, processing quality, and ingredient integrity. 
> Scores do not capture the nutritional value of added vitamins and minerals. 
> A fortified product may deliver meaningful micronutrient benefit not visible 
> in its score.
> ```
>
> **Graduated prevalence language:**
>
> | Affected proportion | Required language |
> |---|---|
> | 50–65% of products | "approximately half of products" |
> | 66–79% of products | "the majority of products" |
> | 80–100% of products | "most products in this category" |
>
> **Documentation requirement:** The category launch record must document which distortions triggered the Endemic Distortion Protocol, the prevalence estimate, and the exact disclosure text approved for production.
>
> **Scope:** This protocol applies to all Bari categories. When a category launches with an endemic distortion, the disclosure format is approved as part of the Article VI checklist Section C review.

---

Add to Article VI, Section 6.2, Section C — Distortion Review Requirements, the following criterion:

> | C5. Endemic distortion check | Identify any distortion with ≥ 50% category prevalence; if present, activate Section 6.4 | Pass only if endemic distortions identified and disclosure text approved |

---

**Risks:**
- Category-level disclosures may reduce consumer confidence in scores across the board, not only for fortification. Mitigation: the disclosure is precisely scoped ("scores do not capture micronutrient contribution") — it does not undermine the dimensions the score does capture.
- Over-triggering: multiple endemic distortions in a single category produce multiple category-level notices. Mitigation: if more than one distortion reaches endemic prevalence, consolidate into a single category note listing all applicable limitations.

**Alternative options:**
- No category-level disclosure: rely on product-level only. Rejected — this is the problem being solved.
- Suppress product-level disclosures when category-level notice exists: simpler UI, but reduces transparency at the specific product level where the distortion may affect that product's specific comparison.

---

### Resolution 3 — Granola Sub-Category Pool Ruling

**Recommended action: Standing precedent derivable from Constitution v1, Article II, Rule 2.**

No new document required. The resolution is documented here and established as a standing precedent for the cereals category and for all future categories encountering the same architectural divergence pattern.

---

**Exact governance change:**

Add the following as Article II, Rule 5 of the Comparison Governance Constitution v1:

---

> **Rule 5 — Architectural Divergence Sub-Category Rule**
>
> When a group of products within a category shares an architectural profile that diverges significantly from the parent category baseline across two or more scored dimensions, that group constitutes a distinct comparison sub-category and must be defined as a separate pool under Article II, Rule 2.
>
> **Divergence threshold:** A sub-group diverges significantly when its median value on two or more scored dimensions falls outside 1.5 standard deviations of the parent category's distribution on those dimensions.
>
> **Practical application where BSIP data is available:**  
> Sub-group divergence can be identified from BSIP2 category reports before pool assignment. If BSIP data is not yet available, the architectural divergence rule is applied using the following proxy indicators:
>
> - NOVA 3 or higher (processed or ultra-processed) when the category median is NOVA 1–2
> - Added sugar ≥ 10g/100g when the category median is ≤ 5g/100g
> - Fat ≥ 10g/100g from added fats/oils when the category median fat is < 5g/100g
>
> Products satisfying any two proxy indicators concurrently are presumed to belong to a distinct sub-category pool pending BSIP confirmation.
>
> **Granola standing precedent:**  
> Within the breakfast cereals category, products identified as granola-type (satisfying any two of the three proxy indicators above) constitute a distinct sub-category pool. This is the inaugural application of this rule. The granola precedent governs:
> - Granola-type products are ranked within the granola pool under Lens 1 (General Everyday Choice, default)
> - Cross-pool comparisons (granola vs. standard cereal) are permitted with a purpose divergence disclosure stating that granola and standard cereals serve different consumer occasions and represent meaningfully different nutritional architectures
> - Granola-type classification cannot protect a product from its score (Anti-Immunity Rule applies in full)
>
> **Standing precedent application:** This rule and its proxy indicators apply to all future Bari categories where a sub-group exhibits similar architectural divergence. Future applications do not require individual governance decisions provided the proxy indicators are satisfied.

---

**Risks:**
- The 10g/100g added sugar proxy requires ingredient-level data (distinguishing added sugar from natural sugar), which BSIP currently cannot reliably produce for all products. Mitigation: in the absence of added sugar data, total sugar ≥ 15g/100g is the proxy for the added sugar indicator.
- A product at exactly the boundary (e.g., 9.8g sugar, NOVA 3, 9.5g fat) may fall outside the granola pool by a narrow margin while being architecturally similar. Mitigation: boundary cases default to the granola pool (conservative interpretation — it is better to over-include in the separate pool than to distort the standard cereal pool).

**Alternative options:**
- Case-by-case CE Controller 1 ruling for each ambiguous sub-category product: more flexible, less systematic, creates reconsideration burden for every new category.
- Exclude granola from the category entirely: over-exclusion; loses valuable analytical output.

---

### Resolution 4 — Whole Grain Marketing Divergence Threshold

**Recommended action: Amendment to Consumer Use-Case & Purpose Guardrails v2, Section 5.2.**

Add a Claim Threshold Reference Table to Section 5.2, defining the "specific nutritional standard in its ordinary meaning" for the most prevalent claim types. Whole grain is the first entry; the table provides structure for future additions at category launch.

---

**Exact governance change:**

Add the following as Section 5.2.1 to the Consumer Use-Case & Purpose Guardrails v2, immediately after the three Condition descriptions in Section 5.2:

---

> **5.2.1 — Claim Threshold Reference Table**
>
> Condition 2 of the Marketing Divergence Finding requires that the claim implies a specific nutritional standard. Where that standard is not self-evident from the claim's ordinary meaning, it must be defined. This table provides the calibrated standard for each defined claim type.
>
> Thresholds not listed here must be documented in the category-specific governance addendum at category launch before any Marketing Divergence Findings are produced for that claim type.
>
> **Table: Defined Claim Thresholds (as of v2, 2026-05-29)**
>
> | Claim type | Claim forms covered | Threshold definition | Detection method |
> |---|---|---|---|
> | Whole grain — composition | "made with whole grain," "contains whole grain," "with whole grain goodness," or any claim implying presence without dominance | ≥ 30% of grain ingredients by weight are whole grain (i.e., a whole grain flour appears in the ingredient list and is not preceded by a refined flour of the same grain type) | Ingredient list: whole grain flour of the specified grain appears before refined flour of the same grain, OR only whole grain flour of that grain is present |
> | Whole grain — primary/dominant | "whole grain," "100% whole grain," "entirely whole grain," or any claim implying the product is predominantly whole grain | Whole grain flour is the first listed grain ingredient AND constitutes ≥ 51% of total grain ingredient weight. In absence of weight data: whole grain flour is first grain ingredient AND no refined flour of the same grain appears | Ingredient list: whole grain flour is listed before all refined grain ingredients. Presence of refined flour of the same grain immediately after disqualifies the dominant claim. |
> | Keto / ketogenic | "קטוגני," "keto-friendly," "ketogenic" | Net carbohydrates ≤ 5g per 100g (standard ketogenic formulation threshold) | Nutritional label: total carbohydrates minus fiber ≤ 5g/100g |
> | High protein (general food context) | "עשיר בחלבון," "high protein," "rich in protein" | Protein ≥ 20% of total calories, OR protein ≥ 15g/100g in solid products, OR protein ≥ 8g/100ml in beverages (Note: category-specific thresholds supersede this general default when defined) | Nutritional label: protein content per 100g/ml |
>
> **Application rule:**  
> When a claim is present and a threshold exists in this table, Conditions 1 and 2 of the Marketing Divergence Finding are automatically satisfied if the claim form matches. Condition 3 (architecture falls short) must still be evaluated against the listed threshold. All three conditions must be present for the Finding to be issued.
>
> **Absence of threshold:**  
> If a claim type is not listed and no category-specific threshold has been documented, Condition 2 cannot be evaluated. The finding cannot be issued. The claim is noted as "claim threshold undefined — Marketing Divergence Finding not applicable" in the category analysis record. This triggers a documentation requirement for the category launch checklist.

---

Add to Article VI, Section 6.2, Section D — Explanation Quality Requirements, the following criterion:

> | D6. Claim threshold table | Category-specific claim thresholds documented for all prevalent claim types in the category; thresholds validated against external references where available | Pass only if threshold table is written and filed |

---

**Risks:**
- The 51% whole grain threshold (FDA/WGC standard) may not match Israeli consumer expectation of what "whole grain" means. Israeli consumers may interpret "whole grain" more loosely. Mitigation: the threshold is used for Marketing Divergence Finding trigger purposes, not for consumer-facing judgment. The finding states the gap factually; it does not tell consumers whether the product is good or bad.
- Ingredient list-based detection cannot determine exact weight percentages. Mitigation: the "first grain ingredient" proxy is the operational detection method. It is conservative (may miss some products that technically meet the 51% threshold despite ordering) — false negatives are acceptable; false positives (finding issued when the claim is actually supported) are the failure mode to avoid.

**Alternative options:**
- No threshold — require per-claim CE Controller 1 judgment at analysis time: more flexible, produces inconsistent findings over time.
- Use Israeli Ministry of Health labeling guidelines as the reference: MOH has no specific whole grain percentage threshold; this option is not currently available.

---

## 5. Governance Impact Assessment

### Document 1 — Comparison Governance Constitution v1

**Impact: Material amendment required.**

Three resolutions directly amend this document:

**Amendment A — Article II, new Section 2.8:**  
Children's Product Operational Definition (Resolution 1). Adds specificity to the existing absolute prohibition. Does not change the philosophy of Article II; adds the missing operational trigger for the prohibition.

**Amendment B — Article II, new Rule 5:**  
Architectural Divergence Sub-Category Rule (Resolution 3). Extends the existing sub-category rule (Rule 2) with a mechanism for resolving ambiguous sub-category membership via proxy indicators. Does not change the existing rule; provides the determination process the rule required but did not supply.

**Amendment C — Article VI, new Section 6.4 and one new checklist criterion (C5):**  
Endemic Distortion Protocol (Resolution 2). Adds a category-level disclosure mechanism alongside (not replacing) the existing product-level distortion disclosure. The launch checklist gains one new criterion.

**Character of amendments:** All three are additive. No existing rules are revised, removed, or contradicted. The amendments fill gaps; they do not change the governance philosophy.

**Section requiring cross-reference update:**  
Article II, Section 2.3 and Section 2.7 both reference "children's products" without definition. Both sections should carry a cross-reference to new Section 2.8 after amendment.

---

### Document 2 — Consumer Use-Case & Purpose Guardrails v2

**Impact: Targeted calibration addition.**

One resolution amends this document:

**Amendment D — Section 5.2, new Section 5.2.1:**  
Claim Threshold Reference Table (Resolution 4). Adds a structured reference table for claim thresholds to the existing Marketing Divergence Finding standard. The finding standard (Conditions 1–3, evidence requirements, format) is unchanged. Section 5.2.1 provides the missing calibration constants for specific claim types.

**Character of amendment:** Additive. The framework is correct; the amendment supplies data inputs the framework required but did not contain.

**Note on table maintenance:**  
The Claim Threshold Reference Table must be treated as a living input — each new category launch must add claim thresholds for that category's prevalent claim types. Maintenance responsibility: CE Controller 1. The Constitution's Article VI checklist criterion D6 creates the governance requirement to keep the table current.

---

### Document 3 — Distortion Registry

**Impact: None.**

All four gaps are resolved through governance amendments. No new distortion entries are required. DISTORTION-004 (fortification) is already correctly registered. The resolution of Gap 2 creates the disclosure mechanism for endemic distortions; it does not change the distortion classification itself.

---

### Document 4 — Category Launch Framework (Constitution v1, Article VI)

**Impact: Two checklist criteria added.**

- **C5 — Endemic Distortion Check** (from Resolution 2): requires identification of endemic distortions and activation of Section 6.4 before launch.
- **D6 — Claim Threshold Table** (from Resolution 4): requires documentation of claim thresholds for all prevalent claim types in the category before explanation review.

The checklist grows from 25 criteria to 27 criteria. Both additions are mandatory hard gates consistent with the existing checklist governance model.

---

### Summary of Document Revision Requirements

| Document | Amendment required | Priority |
|---|---|---|
| Constitution v1 — Article II, Section 2.3 | Cross-reference to new Section 2.8 | Before cereals launch |
| Constitution v1 — Article II, Section 2.7 | Cross-reference to new Section 2.8 | Before cereals launch |
| Constitution v1 — Article II, new Section 2.8 | Full text addition (Resolution 1) | Before any category with children's products |
| Constitution v1 — Article II, new Rule 5 | Full text addition (Resolution 3) | Before cereals launch |
| Constitution v1 — Article VI, new Section 6.4 | Full text addition (Resolution 2) | Before any category with endemic distortions |
| Constitution v1 — Article VI, checklist criterion C5 | New row addition | Before cereals launch |
| Constitution v1 — Article VI, checklist criterion D6 | New row addition | Before cereals launch |
| Guardrails v2 — Section 5.2, new Section 5.2.1 | Full text addition + table (Resolution 4) | Before any Marketing Divergence Findings are produced for whole grain claims |

---

## 6. Launch Readiness Reassessment

**Assumed:** All four resolutions adopted as specified in Section 4.

### Governance Assessment — PASS

| Gap | Status after resolution |
|---|---|
| Gap 1 — Children's definition | RESOLVED — Section 2.8 provides unambiguous operational definition |
| Gap 2 — Endemic distortion disclosure | RESOLVED — Section 6.4 provides category-level format; C5 mandates activation |
| Gap 3 — Granola pool | RESOLVED — Article II, Rule 5 creates the standing precedent; granola assigned to separate pool under Lens 1 |
| Gap 4 — Whole grain threshold | RESOLVED — Section 5.2.1 defines the threshold; D6 mandates documentation at launch |

Governance gaps no longer block launch.

### Data Pipeline Assessment — NOT COMPLETE

Governance resolution does not resolve the data pipeline requirements. The following prerequisites remain before cereals is launch-ready:

| Prerequisite | Status | Governance reference |
|---|---|---|
| BSIP0 cereals scrape from real Israeli retailers | Not started | Article VI, Criteria A1–A2 |
| BSIP1 enrichment with children's classification field | Not started | Section 2.8 — requires D1–D4 enrichment fields |
| BSIP2 scoring with cereal archetype calibration | Not started | Article VI, Criteria A3–A4 |
| Serving size normalization protocol documented | Undefined | Article VI, Criterion B3 (Hybrid/variant policy) — serving size normalization is a variant of this requirement |
| Category launch checklist completed (all 27 criteria) | Not started | Article VI, Section 6.2 |

### Verdict

**B — Launch Ready with Conditions.**

The governance is resolved. The category cannot launch until the data pipeline conditions above are completed. Upon completion of data prerequisites and satisfaction of the 27-criterion checklist, cereals is approved for launch under the governance framework as amended by this document.

**Conditions that must be verified at launch:**
1. BSIP0 corpus contains ≥ 30 editorial-scope products traceable to real Israeli retailers
2. Children's products identified using Section 2.8 indicators and excluded from adult comparison pool
3. Granola-type products separated into distinct sub-category pool per Article II, Rule 5
4. DISTORTION-004 endemic disclosure text written and approved for the cereals category page
5. Whole grain claim thresholds applied to all products with whole grain claims in the corpus
6. Serving size normalization protocol documented (Gap 5 — moderate, not a governance gap but a methodology requirement)

---

## 7. Meta-Learning

Cereals was selected as the governance stress test precisely because it would expose weaknesses. It exposed four. The most important finding is that none of the four gaps are cereals-specific. They are generic. They will appear in every category Bari enters. The following documents the specific exposure in each upcoming category.

---

### Meta-Finding 1 — Children's Definition is Universal

Every category that could include products marketed to children under 12 will hit the Gap 1 problem. The new Section 2.8 definition is already scoped as universal ("applies to all Bari categories"). The Indicator D3 serving size threshold (≤25g) is calibrated for cereals specifically — other categories require recalibration.

**Bread:**  
Children's bread lines exist (smaller rolls, cartoon-branded loaves, sandwich bread marketed to school children). Indicators D1 and D2 are directly applicable. D3 requires a bread-context recalibration (≤30g slice weight, or single serving ≤ half a standard adult slice). The Gap 1 resolution applies immediately.

**Milk:**  
Growing-up milks and follow-on formulas for toddlers (18–36 months) carry children's indicators explicitly. These products occupy the dairy shelf alongside adult milk but belong to a different regulatory and nutritional context. The Gap 1 resolution applies; the developmental pool separation is the correct treatment. Note: toddler formulas approach the "medical nutrition" boundary — verify against Article II, Section 2.3 (absolute restriction on infant formula).

**Cheese:**  
Children's cheese snack lines (string cheese for kids, portion-sized children's cheese, cartoon-branded cheese) satisfy D1 and D3 concurrently in most cases. Indicator D3 calibration: ≤20g portion for cheese context. The Gap 1 resolution applies.

**Protein bars:**  
Children's-specific protein bars do not represent a significant segment. Gap 1 exposure is low for this category.

---

### Meta-Finding 2 — Endemic Distortion Disclosure will apply to Multiple Future Categories

DISTORTION-004 (fortification) is the first endemic distortion encountered. It will not be the last.

**Bread:**  
DISTORTION-002 (protein inflation) may reach endemic prevalence in the protein bread segment, which in Israel is a significant category subset. Most protein bread products have marginal protein concentration relative to protein claims. If ≥50% of bread products carry a protein claim that BSIP2 evaluates as architecturally weak, the Endemic Distortion Protocol activates for DISTORTION-002 in the bread category. Evaluate at BSIP2 run time.

**Milk (plant-based alternatives):**  
DISTORTION-004 is likely to be CATEGORY-CRITICAL in oat milk, almond milk, and soy milk — the fortification landscape in plant-based milks is nearly universal. The Endemic Distortion Protocol should be anticipated and the disclosure text prepared before the first plant-based milk BSIP2 run.

**Cheese:**  
DISTORTION-010 (macro obsession — protein + saturated fat tradeoff not captured in scoring) is likely to affect a significant proportion of hard cheese and processed cheese products. Evaluate at BSIP2 run time; Endemic Protocol may activate.

**Protein bars:**  
DISTORTION-002 (protein source quality) is effectively endemic in the protein bar category. Whey isolate and engineered protein blends are standard; whole-food protein sources are rare. The Endemic Distortion Protocol should be prepared for protein bars from day one of category launch planning.

---

### Meta-Finding 3 — Sub-Category Pool Decisions Occur in Every Category

The granola ruling established a mechanism (Article II, Rule 5 — Architectural Divergence Sub-Category Rule). That mechanism will be activated in every category Bari enters.

**Bread:**  
Crispbread / crackers occupy the same retail aisle as standard bread but are architecturally distinct (typically higher in fat, lower in water content, fundamentally different texture and serving role). The Rule 5 proxy indicators will identify these products as a distinct pool at BSIP2 run time. Keto bread and gluten-free bread are Lens 3 products that belong in their own restriction pool; the existing Lens 3 framework handles these without Rule 5.

**Milk:**  
Plant-based milk alternatives vs. dairy milk. These are already likely Lens 3 (dietary restriction) for vegan consumers and cross-lens for all others. The architectural divergence (fat type, protein source, micronutrient profile, fortification architecture) is extreme. Rule 5 will confirm what Lens 3 already implies: separate comparison pools with cross-pool disclosure.

**Cheese:**  
The hard cheese / soft cheese / processed cheese / cream cheese / labaneh architecture is fragmented enough that multiple sub-category pools are nearly certain. Rule 5 provides the formal mechanism. Labaneh (strained yogurt cheese, architecturally distinct from hard cheese) and processed cheese spreads (NOVA 4 baseline, architectural outlier) will be the highest-priority Rule 5 applications.

**Protein bars:**  
The date bar vs. engineered protein bar distinction was already identified in BSIP2 snack bars analysis. Rule 5 now provides the formal governance mechanism. Date bars are architecturally NOVA 2, high natural sugar, whole food matrix — against an engineered protein bar comparison pool where NOVA 3–4 and isolated protein are standard. The Rule 5 proxy indicators (NOVA, added sugar, fat) will separate these cleanly.

---

### Meta-Finding 4 — Claim Threshold Tables are a Category Launch Requirement

Gap 4 revealed that the Marketing Divergence Finding framework is analytically correct but calibration-incomplete. Every category has prevalent claim types. Every prevalent claim type needs a threshold before the Finding can be applied. The Claim Threshold Reference Table (Section 5.2.1 of Guardrails v2) is the mechanism. The Constitution's checklist criterion D6 creates the mandate.

**Bread:**  
"Sourdough" is the highest-value claim to threshold. The sourdough claim implies meaningful fermentation — but what constitutes meaningful fermentation? Options: (a) presence of sourdough starter as first ingredient before commercial yeast; (b) absence of commercial yeast; (c) declared fermentation time. This threshold requires food science input and is the most difficult to define from ingredient labels alone. Establish the "whole grain" threshold first (already done); sourdough threshold is the next priority for bread.

**Milk:**  
"Protein milk" threshold is the critical claim. Standard milk is approximately 3.2–3.5g protein/100ml. A "protein milk" claim implies meaningful concentration above this. Proposed threshold: ≥6g protein/100ml (roughly double the dairy baseline). This threshold requires validation against the Israeli protein milk market.

**Cheese:**  
"Light" / "lite" / "דל שומן" threshold for reduced-fat cheese. The EU standard requires 30% reduction from the reference product. Israel has no regulatory threshold. Proposed approach: ≥25% fat reduction from the category median for the same cheese type.

**Protein bars:**  
"High protein" threshold is existential for the category — without it, Marketing Divergence Findings cannot be applied to the most important claim type in the category. The general threshold in Section 5.2.1 (≥20% of calories from protein, or ≥15g/100g) provides a starting point. The category-specific threshold should be validated against the Israeli protein bar corpus at BSIP2 run time.

---

### Meta-Finding 5 — Governance Stress Testing Should be a Mandatory Pre-Launch Step

Cereals was selected as a voluntary stress test. The test found four blocking gaps. Had cereals launched without the stress test, all four gaps would have become production failures — inconsistent children's classification, undisclosed endemic distortions, granola in the wrong comparison pool, and unapplied Marketing Divergence Findings for the most prevalent claim type.

**Recommendation:** Add a Governance Stress Test as a mandatory step in the Category Launch Approval Checklist. Position it as a pre-launch requirement distinct from the 27 existing criteria — it is a process gate, not a data gate.

**Proposed criterion (to be added to Article VI):**

> **E6. Governance Stress Test:** A formal governance stress test has been applied to the category, evaluating the full governance stack against the category's specific characteristics. Verdict of B or higher required for launch. A verdict of C or lower blocks launch pending resolution documentation.

---

## 8. Recommendations

**Recommendation 1 — Apply all four amendments to their respective governance documents before any further category work.**  
Amendments A–D in Section 5 are the minimum required changes. These are additive amendments to existing documents. They should be written into Constitution v1 and Guardrails v2 before cereals data pipeline work begins, because both documents will be referenced by the BSIP2 cereals run.

**Recommendation 2 — Elevate Gap 1 (children's definition) and Gap 4 (claim thresholds) to all active categories immediately.**  
The bread and milk categories are in active pipeline stages. Both are exposed to the children's definition gap (Gap 1) and the claim threshold gap (Gap 4). The amendments resolve these at the framework level. Category-specific calibration (D3 serving size threshold for bread/milk/cheese, sourdough/protein milk/light cheese thresholds) must be documented at each category's next BSIP milestone.

**Recommendation 3 — Prepare the DISTORTION-004 endemic disclosure text for cereals before BSIP0 scrape begins.**  
The text should be drafted at pre-BSIP stage and refined when the corpus prevalence is known. Draft:  
*"Breakfast cereal products are frequently enriched with vitamins and minerals (iron, B vitamins, calcium, vitamin D). Bari's current scores do not include micronutrient contribution as a positive factor. Scores reflect macronutrient architecture, processing quality, and ingredient integrity. A fortified product may deliver meaningful micronutrient benefit not visible in its score."*  
This text satisfies the Section 6.4 format requirements.

**Recommendation 4 — Add Governance Stress Test as a mandatory Category Launch Approval criterion (E6).**  
The stress test process proved its value in cereals. It should not be voluntary. Add it to Article VI as a hard gate — verdict of B or higher required for launch approval. The mechanism already exists (this document is its output).

**Recommendation 5 — Maintain the Claim Threshold Reference Table (Section 5.2.1) as a living document under CE Controller 1 authority.**  
The table currently contains four claim types (whole grain composition, whole grain dominant, keto, high protein). Each new category will add entries. The table must be updated before Marketing Divergence Findings are produced for any claim type not yet listed. This is a maintenance obligation, not a one-time task.

---

*Cereals Governance Gap Resolution Report v1*  
*CE Controller 1 — Chief Nutrition, Scoring & Content Architect*  
*2026-05-29*  
*Resolves: category_audit_cereals_v1.md*  
*Amends: comparison_governance_v1.md (Articles II and VI), consumer_usecase_guardrails_v2.md (Section 5.2)*  
*Next action: Apply amendments to source documents before cereals data pipeline begins.*
