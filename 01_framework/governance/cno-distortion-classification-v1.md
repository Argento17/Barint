# CNO Distortion Classification — v1

**Role:** Chief Nutrition Officer  
**Task:** TASK-004 — Impact classification of all known distortions  
**Source document:** `distortion-backlog-v1.md`  
**Date:** 2026-05-30  

This document classifies each distortion in the Bari Distortion Backlog v1 by severity (Critical / Significant / Moderate / Minor) and assesses impact across four dimensions: scientific validity, consumer trust, score accuracy, and category calibration. No solutions are proposed. No scores are modified. No new rulings are created.

---

## Classification Scale

| Level | Definition |
|---|---|
| **Critical** | Produces analytically invalid results today, in production. May mislead consumers or operators with no visible signal that the score is wrong. Requires active attention before the next category promotion or corpus expansion. |
| **Significant** | Produces systematically distorted results with confirmed direction or confirmed mechanism. May or may not be grade-determinative in the current corpus. Should be in the active BSIP2 development queue. |
| **Moderate** | Real structural vulnerability or contextual mismatch. May affect specific product types or is currently prospective. Does not render scores analytically invalid in general, but creates specific failure cases. |
| **Minor** | Scientifically identifiable but empirically low-impact in the current corpus. Other caps or signals typically mask the distortion. Worth monitoring; not worth interrupting planned work. |

---

## DIST-001 — Dairy Fiber Penalty

**CNO Classification: SIGNIFICANT**

### Why it matters

Applying a 35% fiber weight to products that are biologically fiber-free is a category-level analytical error. It is not that dairy products fail to deliver fiber — it is that the question does not apply. The nutrient density dimension formula (`0.65 × protein_score + 0.35 × fiber_score`) was designed for products where fiber is a meaningful compositional variable. Dairy products are excluded from fiber by biology, not by formulation weakness.

The distortion worsens with higher protein content: the products most deserving of nutritional credit — high-protein yogurts, skyr, quark — are penalised the most. This inverts the intended relationship between protein quality and nutritional score.

### Scope of impact

Every scored dairy product in the `dairy_protein` category, without exception. Quantified range: 0.84–4.46 final score points of systematic underscoring. The yogurt corpus (45 products planned) will be uniformly affected when launched. The distortion is direction-certain — it always runs negative.

### Dimension assessments

**Scientific validity:** Affected. Applying a fiber penalty to fiber-free foods is not defensible analytically. The formula encodes an assumption — that all food categories should contribute fiber — that is false for dairy as a product class. Evidence strength for the scientific objection: Strong.

**Consumer trust:** Affected. A consumer comparing plain yogurt to a snack bar will see the yogurt scored lower in part because it contains no fiber, which is a normal property of yogurt, not a flaw. If this mechanism became visible, it would undermine confidence in the system's design.

**Score accuracy:** Affected. The distortion is quantified, systematic, and directionally certain. At the B/C grade boundary (score 70), a 2-point distortion is grade-determinative. Any dairy product currently scoring 68–70 may be incorrectly assigned a C instead of its analytically correct B.

**Category calibration:** Affected. The entire `dairy_protein` category is uniformly downscored relative to its analytical reality. Within-category rankings are preserved (all products are penalised by the same formula), but cross-category comparisons between dairy and non-dairy categories are biased against dairy.

### Disposition

**Prioritized for future BSIP2 work.** The fix mechanism is known and bounded. The impact is quantified. The direction is certain. This should be resolved before the yogurt corpus is published, as the yogurt category will be the first category where this distortion materially affects a substantial product corpus.

---

## DIST-002 — Date Sugar Halo

**CNO Classification: SIGNIFICANT**

### Why it matters

The question this distortion raises is a genuine nutritional science question: is the glycemic impact of 60–70% sugar from whole dates equivalent to 60–70% sugar from refined cane syrup? The architecture's implicit answer is no — and that answer has partial scientific support. Whole dates consumed as fruit produce a meaningfully different glycemic trajectory than equivalent sugar from glucose syrup, primarily due to the intact fiber matrix, polyphenol content, and slower mastication rate.

However, date bars and date-paste products are not whole dates. Date paste, date syrup, and date concentrate all have reduced matrix integrity compared to whole fruit. The fiber is present but the structural matrix that moderates the glycemic response is partially disrupted. The degree to which the glycemic equivalence applies to date-derived ingredients in processed bars is not empirically established in the Bari corpus.

The distortion is therefore not that the architectural position is wrong — it may be right — but that it is unverified for the specific product forms in the Bari corpus, and it is silently embedded. Consumers see a date bar score well and have no way to understand that the score reflects a structural philosophy about natural sugar, not a finding that date bars have a low glycemic effect.

### Scope of impact

`snack_bar_granola` primarily. The Israeli snack market has a significant segment of date-based bars (אנרגיה בר, תמר חלון, etc.). Within this category, the score gap between date-dominant bars and equivalent-sugar cane-sweetened bars is potentially large but not yet quantified.

### Dimension assessments

**Scientific validity:** Partially affected. The whole-food natural sugar position has scientific basis for whole-food forms. Its extension to date paste and date concentrate in processed products is not empirically validated. The distortion is an overgeneralisation of a scientifically defensible principle to product forms where the evidence is weaker. Evidence strength for the boundary claim (date paste ≈ whole date in glycemic terms): Weak to Moderate.

**Consumer trust:** Significantly affected. A consumer comparing a date bar (high score) to a sugar-syrup snack bar (lower score) will reasonably conclude the date bar is nutritionally superior in all dimensions. If the glycemic equivalence of the products is real, this is a trust-damaging conclusion to draw from the scores.

**Score accuracy:** Unknown magnitude. The score difference between an equivalent date-sugar and refined-sugar product has not been measured. Until the comparison is quantified, the distortion scale is characterised only by direction (date products score higher), not by magnitude.

**Category calibration:** Affected within `snack_bar_granola`. Date-dominant products are systematically over-ranked relative to their refined-sugar equivalents. The within-category ordering reflects the structural scoring philosophy but may not reflect metabolic equivalence.

### Disposition

**Researched.** The primary research question is: for the specific product forms present in the Bari corpus (date paste bars, date-nut balls, date-and-oat bars), what is the evidence for a meaningful glycemic differential compared to refined-sugar products at equivalent total sugar concentrations? This question should be answered before the snack bar category is promoted to consumers.

---

## DIST-003 — Router v2 Missing Archetypes (Bread / Cracker)

**CNO Classification: CRITICAL**

### Why it matters

Category misassignment is the most structurally severe distortion in the system. A seed-topped sourdough bread evaluated under `whole_food_fat` rules is not receiving a lower score than it deserves — it is receiving the wrong score from a wrong analytical frame. The score is internally consistent and plausible, but it answers a different question than the one Bari is supposed to answer for that product.

The confirmed failure mode is directionally known: seed-topped breads routed to `whole_food_fat` face more lenient calorie density rules. They receive a score optimistic relative to bread category norms. A consumer comparing this bread to other breads is comparing an inflated score to correctly categorized scores — the ranking is corrupted.

The bread category is currently live in production with 24+ products. The Israeli retail bread market contains numerous seed-topped varieties: sesame challah, sunflower-topped whole grain, multi-seed sourdough. If any of these are in the current corpus and were routed through the WFF contamination path, their published scores are wrong today.

### Scope of impact

`bread` (production), with contamination into `whole_food_fat`. Crackers fall to `default`. The scope within the production corpus is not measured but is likely non-trivial given the prevalence of seed-topped breads in Israeli retail.

### Dimension assessments

**Scientific validity:** Severely affected. There is no scientifically defensible justification for evaluating a bread product using whole-food fat calorie density tables. The caloric context of a 480 kcal/100g tahini (consumed at 20g portions) is completely different from a 480 kcal/100g bread (consumed at 80–100g portions). Routing bread into the WFF frame produces an analytically invalid result regardless of how precisely the scoring engine executes.

**Consumer trust:** Severely affected. A seed-topped sourdough bread that scores higher than a plain whole grain bread due to routing — not due to composition — is a credibility failure. The score implies the seeded bread is nutritionally superior; the reality may be the opposite for specific products.

**Score accuracy:** Severely affected for affected products. The quantified worst case (30-point swing) is large enough to change a product's grade from D to B. In a category with 24+ products, even a handful of misrouted products corrupts the integrity of the entire comparison.

**Category calibration:** Severely affected. Misrouted products are calibrated against the wrong reference group. Their scores do not represent their standing within the bread category; they represent their standing within a different category using different rules.

### Disposition

**Prioritized for future BSIP2 work.** This is operationally urgent because the bread category is live. The next bread scoring cycle must include router v2 updates with bread and cracker archetypes before any scores are treated as valid for new products. An audit of the current corpus against the routing output is also needed to identify which currently published bread scores may be contaminated.

---

## DIST-004 — Prototype Weight Divergence

**CNO Classification: SIGNIFICANT**

### Why it matters

The 10 dimension weights determine the relative analytical importance of processing quality, nutritional contribution, calorie density, glycemic quality, protein, additives, satiety, fat quality, regulatory signals, and whole food integrity. These weights encode a scientific judgment about which aspects of food structure matter most in the Bari framework. If the weights in `constants.py` diverge from the methodology document, the engine is executing a different scientific judgment than the one that has been defined, reviewed, and published.

This creates a documentation integrity problem. Bari's methodology transparency — the claim that "this is how we score" — is undermined if the published weights are not the weights being used.

From a nutritional science standpoint, the specific weights matter. If Processing Quality should carry 18% weight but actually carries a different weight, the engine over- or under-penalises processing-related signals relative to the design intent. The direction of this divergence is unknown, which means the sign of the error is unknown.

### Scope of impact

All categories. All 10 dimensions. Every scored product. This is the broadest-scope distortion in the backlog, but its severity is unknown because the magnitude of divergence has not been measured.

### Dimension assessments

**Scientific validity:** Affected. Publishing a methodology that describes weights different from the implemented weights is a scientific integrity breach. The scores cannot be traced to the published methodology. Evidence strength for the divergence: Moderate (the divergence is confirmed; the magnitude is unknown).

**Consumer trust:** Affected — but conditionally. Consumers do not typically inspect the methodology weights. The trust impact is most acute if Bari publishes the weights and a technically informed consumer compares them to the engine output.

**Score accuracy:** Unknown. The distortion could be negligible (weights are close to intended) or significant (weights diverge substantially). The range estimate (5–15 points) is speculative and not anchored to a measurement.

**Category calibration:** Affected. If certain dimensions are over- or under-weighted, products that score primarily on those dimensions will be systematically biased relative to the intended calibration. The direction is unknown.

### Disposition

**Researched.** A calibration corpus study is required before this distortion can be properly classified. The research question is: what are the actual weights in `constants.py`, what are the intended weights in the methodology, and what is the score difference for a representative set of golden products between the two weight sets? Until this comparison exists, the severity of DIST-004 cannot be determined precisely.

---

## DIST-005 — Inactive Scoring Layers (Snacks)

**CNO Classification: CRITICAL**

### Why it matters

This distortion contains a data integrity violation: 11 products are currently labelled `confidence: verified` in the live snacks corpus despite having no verified nutritional content. This is not a subtle analytical gap — it is a factually incorrect label being displayed to users (or available to operators) in the current production system.

Beyond the label error, the scoring consequence is severe. Snack bar scores currently reflect only structural integrity (Layer 1) and consumption engineering signals (Layer 4). The two nutritional layers — Nutritional Contribution (Layer 2) and Metabolic Stability (Layer 3) — are inactive. For snack bars specifically, these layers are analytically essential: a date bar and a chocolate-coated wafer should produce dramatically different nutritional layer scores. The fact that snacks score a category mean of 43.50 — virtually identical to maadanim at 43.78 — is the empirical signature of a system scoring without its nutritional instruments.

Snack bars are the category most susceptible to the health-halo problem. They are marketed as healthy and purchased for their apparent nutritional value. Scoring them without nutritional data is scoring the category where nutritional data matters most without that data.

### Scope of impact

All 18 products in the snacks corpus. 11 products with incorrect confidence labels. Potentially grade-affecting for most of the corpus (10–20 point shift expected when nutritional data is ingested).

### Dimension assessments

**Scientific validity:** Severely affected. Scoring Layer 2 (Nutritional Contribution) and Layer 3 (Metabolic Stability) with null data is equivalent to not having a nutritional assessment. The current snack scores cannot be described as nutritionally validated scores. They are structural-and-processing assessments presented as complete product assessments. The confidence label error compounds this: "verified" is a scientific claim about data quality that is factually false for 11 products.

**Consumer trust:** Severely affected. A consumer making a purchasing decision based on a snack bar's Bari score is relying on an assessment that is incomplete in its two nutritional dimensions. The confidence label "verified" is the most direct trust violation: the system explicitly claims data quality it does not have.

**Score accuracy:** Severely affected. The 10–20 point potential shift means some products are currently scored in a grade that may change by one full grade when nutritional data is incorporated. A snack bar currently at 72 (grade B) could drop to 52 (grade D) if its nutritional profile is poor. The current ranking within the category may not survive full scoring.

**Category calibration:** Severely affected. Within-category rankings are based on incomplete analytical data. The relative ordering of snack bars in the current corpus cannot be trusted to reflect nutritional reality until Layer 2 and Layer 3 are activated.

### Disposition

**Prioritized for future BSIP2 work — immediate.** The confidence label error is not a future work item; it is a current production error. The snack bar corpus should not be promoted to users or used in comparative content until: (1) nutritional data is ingested, (2) BSIP2 is re-run with complete data, (3) confidence labels are corrected, (4) the new scores are validated against the CE Advisory criteria.

---

## DIST-006 — Classification Instability

**CNO Classification: CRITICAL**

### Why it matters

A confident-but-wrong category classification produces a score that is internally consistent, plausible in appearance, and completely invalid analytically. Nothing in the output signals that the category assignment may be wrong. The consumer, the operator, and the scoring system itself have no way to distinguish a correctly categorised score from an incorrectly categorised one.

This distortion is unique in the registry because it does not affect a dimension or a threshold — it corrupts the foundational frame within which all other analytical decisions are made. No amount of dimension calibration or cap refinement addresses the risk that the entire analytical frame is wrong for a given product.

The confirmed example is instructive. A date-almond-oat ball at 480 kcal/100g scores B (70–80) in `whole_food_fat` and D (45–55) in `snack_bar_granola` — a 30-point difference from category assignment alone. A 30-point difference corresponds to two full grades. The consumer who sees this product graded D when its correct analytical grade is B has been significantly misled.

The four failure modes identified are all highly relevant to the Israeli retail context: Hebrew-only product names are the rule rather than the exception; ambiguous form factors (date-nut balls, granola-style snacks, protein-oat bars) are a large and growing market segment; novel product formats (functional beverages, high-protein dairy innovations) are entering the market continuously.

Classification instability is correctly described as "the single biggest practical scoring risk in BSIP2." No other distortion has equivalent worst-case impact combined with no output visibility.

### Scope of impact

All categories. All products at category boundaries. The failure modes are not edge cases — they are properties of the Israeli retail environment (Hebrew labels, diverse product formats, innovation pace) that will produce mis-classifications at meaningful frequency.

### Dimension assessments

**Scientific validity:** Severely affected. A score computed within the wrong analytical frame is not a scientific result for that product — it is a scientific result for a different product class. The score of ~50 for the date-nut ball in `snack_bar_granola` is a scientifically valid answer to the question "how does this product compare to snack bars?" It is not a valid answer to the question "what is the nutritional quality of this product?" The system currently cannot make this distinction visible.

**Consumer trust:** Severely affected. The worst-case trust scenario is a misclassified product where the consumer knows the correct category and sees a score that reflects a different one. A consumer who buys a date-nut ball from the nuts section and sees it scored as a snack bar with a D grade has been given a wrong answer with no indication it is wrong.

**Score accuracy:** Severely affected. The 20–40 point worst-case swing spans multiple grade boundaries. For any product at a category boundary, the score is effectively a function of the classifier's confidence — and that confidence is not currently surfaced or used to moderate score severity.

**Category calibration:** Severely affected. A misrouted product contaminating a category corrupts that category's rankings by introducing a product scored on alien rules. The `whole_food_fat` category, for example, is contaminated by any bread product routed there — its rankings include a product that is not analytically a whole-food fat product.

### Disposition

**Prioritized for future BSIP2 work.** Classification instability is the highest-priority architectural problem in the system. The minimum viable mitigation — surfacing `category_confidence` as a first-class output field and applying a confidence ceiling for low-confidence classifications — is achievable before full architectural redesign and should be treated as a near-term deliverable.

---

## DIST-007 — Structural Emptiness Blind Spot

**CNO Classification: SIGNIFICANT**

### Why it matters

The current scoring architecture evaluates food primarily by what it fails to do. A product scores well not because the system recognises its nutritional quality but because nothing fires against it. For most product types this is adequate — the penalty system catches the relevant concerns. For a specific class of products — those engineered to be inoffensive to the scoring system rather than genuinely nourishing — the architecture is blind.

The calorie density dimension inversion is the clearest manifestation. The dimension is calibrated to penalise caloric density excess. But at the low end of the caloric scale, it rewards products for being calorically absent, even when that absence is produced by removing all nutritional structure along with the calories. A diet mousse at 40 kcal/100g receives a high calorie density score — not because it delivers nutritional value at a low caloric cost, but because it delivers essentially nothing at all.

This is a scientific validity problem, not a calibration problem. The dimension is measuring the right thing for some products (caloric excess) and the wrong thing for others (it rewards the absence of food structure). No amount of threshold adjustment resolves this.

From a nutritional science standpoint, the asymmetry between penalising presence and failing to reward absence produces scores that are directionally misleading for engineered-empty products. A score of 62–68 means something to a consumer. That meaning implies nutritional acceptability. If the 62 is earned by a product that delivers no meaningful nutritional structure, the score is misleading.

### Scope of impact

`dessert` and `beverage` categories are most affected, particularly their diet product segments. The Israeli dairy dessert market (maadanim) includes diet variants that may exhibit this pattern. The beverage category, when it is scored, will likely contain many products where low calorie density is achieved through nutritional vacancy. Empirical prevalence in the current production corpus is not measured.

### Dimension assessments

**Scientific validity:** Affected. The claim that a product has a score of 62 implies that 62 represents something analytically meaningful about its nutritional structure. For structurally empty products, this is false. The score is produced by the absence of penalties, not by the presence of nutritional merit. Evidence strength for the mechanism: Moderate-Strong (canonical examples are well-documented). Evidence strength for the empirical prevalence: Weak (unmeasured).

**Consumer trust:** Affected. The most damaging scenario is a direct comparison between a diet variant (scores 65 due to structural emptiness) and a genuine whole-food product in the same category (scores 65 due to positive nutritional structure). Both scores are 65, but they represent fundamentally different nutritional realities. A consumer treating the scores as equivalent has been misled.

**Score accuracy:** Affected at 5–15 points of positive distortion for affected products. The calorie density dimension inversion quantifies as the key mechanism. The scale is bounded — the sweetener cap (70 ceiling) and NOVA 4 cap (60 ceiling) catch many engineered-empty products, limiting how high their scores can go.

**Category calibration:** Affected within `dessert` and `beverage`. Diet variants of products rank higher than their nutritional contribution warrants relative to whole-food alternatives in the same category.

### Disposition

**Prioritized for future BSIP2 work.** The positive architecture framework is the designed resolution, and it is already in the planning documents. This distortion is a direct argument for the priority of that work. The minimum viable partial resolution — a matrix poverty flag that removes calorie density credit when a product is simultaneously very low in calories, protein, fiber, and fat — should be scoped as a near-term deliverable that does not require the full positive architecture.

---

## DIST-008 — Cliff-Edge Cap Gaming Surfaces

**CNO Classification: MODERATE**

### Why it matters

The four cliff-edge caps (HIGH_SUGAR_25G_PLUS, HIGH_SODIUM_700MG_PLUS, ADDITIVE_MARKERS_3_PLUS, NOVA_PROXY_4) are binary implementations of what are, in nutritional reality, continuous quality gradients. Sugar concentration does not become meaningfully more harmful at exactly 25.0g/100g. Sodium does not become meaningfully more problematic at exactly 700mg/100g. The threshold is a practical implementation choice, not a scientifically sharp boundary.

This matters because a product reformulated from 25.2g to 24.8g sugar has made no nutritional improvement, but its score improves significantly as a cap is escaped. The scoring system thus rewards minimal cosmetic reformulation and does not reward genuine nutritional improvement near the threshold.

This is currently a prospective risk, not a current scoring error. No evidence exists that any product in the Bari corpus has been reformulated to a threshold. The distortion is in the system design, not in current published scores.

### Scope of impact

All categories for the sugar and sodium caps. `snack_bar_granola` for the three category-specific heuristic caps. `sauce_spread` is disproportionately affected by sodium cap in a context (condiment evaluation) that also creates a separate distortion (DIST-009). The gaming risk is highest for categories where cap thresholds are well-known and products are commercially competitive.

### Dimension assessments

**Scientific validity:** Partially affected. The caps themselves encode scientifically defensible concerns. The threshold values (25g sugar, 700mg sodium) are reasonable structural markers. The binary implementation — a product is either capped or uncapped — is not scientifically defensible as a hard boundary, because nutritional quality is continuous near these thresholds.

**Consumer trust:** Conditionally affected. If a consumer discovers that a product at 24.9g sugar and one at 25.1g sugar have substantially different Bari scores, and that the 24.9g product was reformulated specifically to escape the threshold, Bari's credibility is damaged. This is currently hypothetical but is a credible risk as Bari becomes more visible.

**Score accuracy:** Not currently affected. The distortion is structural vulnerability, not current error. Scores for products near thresholds are correct given current formulations.

**Category calibration:** Not currently affected. Within-category rankings are accurate for current product formulations.

### Disposition

**Monitored.** The gradient cap architecture is already in the planning documents (BEV-053). The risk is prospective and the structural issue is documented. Active research is not needed until either: (a) evidence emerges of threshold-based reformulation in the Bari corpus, or (b) the gradient cap work moves into active development.

---

## DIST-009 — Condiment Per-100g Evaluation

**CNO Classification: MODERATE**

### Why it matters

The per-100g analytical frame is the correct standard for foods consumed in amounts where 100g is a meaningful reference quantity. For condiments consumed at 5–15g per use — miso, soy sauce, fish sauce, preserved vegetables, capers — the per-100g frame produces a score that implies a dietary sodium load that no consumer actually receives.

Miso paste scoring near zero on the sodium dimension when consumed at one tablespoon per meal is not a nutritional assessment of miso — it is a nutritional assessment of eating 100g of miso at a sitting, which no consumer does. The score is analytically correct and contextually misleading simultaneously.

This matters from a nutritional science standpoint because miso is a fermented product with genuine nutritional value (B vitamins, beneficial microorganisms, protein from fermented soy). A score that flags it as a sodium problem when used as a condiment is not capturing its nutritional role in context.

### Scope of impact

`sauce_spread` primarily. The scope within the production corpus is unknown — the proportion of the sauce_spread category that consists of small-quantity condiments vs. spread-quantity foods is not characterised. The distortion is bounded to a specific product class and a specific category.

### Dimension assessments

**Scientific validity:** Technically accurate but contextually misleading. The per-100g evaluation is analytically precise. The contextual mismatch — that the analytical frame does not correspond to how the product is consumed — is a scope limitation, not a methodological error. Evidence strength for the mismatch: Moderate (the mechanism is understood; the product-specific prevalence in the corpus is not measured).

**Consumer trust:** Affected for condiment users. A consumer who avoids miso because of its Bari score — reasoning that the score reflects something about miso's dietary contribution — has drawn the wrong conclusion from a technically correct score. The consumer is not wrong to trust the score; the score fails to communicate its own contextual limitation.

**Score accuracy:** Severely affected for specific condiment products. A miso paste or soy sauce score is not an accurate representation of its dietary impact. But the distortion is category-contained and does not affect the majority of `sauce_spread` products, which are consumed at closer to 100g quantities (hummus, tahini, jam).

**Category calibration:** Affected within `sauce_spread`. Small-quantity condiments rank artificially low relative to spread-quantity products, even when both are nutritionally comparable at realistic serving sizes. The category comparison is misleading for the condiment subset.

### Disposition

**Researched.** The primary research question is: within the current and planned `sauce_spread` corpus, what fraction of products are small-quantity condiments (≤20g per typical use)? If the fraction is small, monitoring is sufficient. If it is substantial, a `context_limited` flag and UI note should be planned before the sauce_spread category is launched.

---

## DIST-010 — Incomplete Protein Credit

**CNO Classification: MINOR**

### Why it matters

Gelatin protein is nutritionally incomplete. Gelatin is a hydrolysed collagen protein — it contains all amino acids present in collagen but is deficient in tryptophan, an essential amino acid that humans cannot synthesise. A product relying on gelatin as its primary protein source cannot support complete protein synthesis in the human body. BSIP2 currently credits gelatin protein identically to complete protein from egg, dairy, or whole legume sources.

This is a scientifically established distinction. The tryptophan deficiency of gelatin protein is well-characterised in nutritional biochemistry (evidence strength: Strong for the basic science). The question is whether this matters in the current corpus.

For gelatin-based desserts, the answer is: probably not grade-determinative. Gelatin desserts typically carry other scoring penalties — sweetener presence (70 ceiling), NOVA 4 processing (60 ceiling), additive burden — that limit their scores below the range where a 3–7 point protein credit correction would change the grade. The protein credit distortion exists, but it is largely masked by overlapping caps.

The secondary form — protein isolates receiving the same credit as whole-food protein — is more prevalent (protein bars commonly use whey or pea isolate) but scientifically less clear-cut. Protein isolates contain all essential amino acids. Their lower bioavailability and reduced satiety effect are real but not of the magnitude to constitute a fundamental analytical error.

### Scope of impact

`dessert` (gelatin-based products, typically score low anyway), `dairy_protein` (isolate-containing products), `snack_bar_granola` (protein bars). Low product count in the current production corpus for the gelatin case. Isolate-containing products are more prevalent but the analytical distortion is smaller.

### Dimension assessments

**Scientific validity:** Affected for the gelatin case (tryptophan deficiency is established science). Partially affected for the isolate case (bioavailability differences are real but the magnitude of the analytical error is not established). Overall evidence strength: Moderate.

**Consumer trust:** Low-moderate. Most gelatin-containing products score low due to overlapping caps. A consumer comparing a protein bar that uses whey isolate to one that uses whole dairy protein may not understand why the scores are close if the isolate product is analytically inferior in protein quality. But this is a nuanced comparison unlikely to produce visible consumer confusion.

**Score accuracy:** Low-moderate. The distortion (3–7 points for gelatin products) is real but typically masked. For isolate-protein products, the score difference from correct attribution has not been measured and is likely small.

**Category calibration:** Minimally affected in the current corpus. The low product count and masking by overlapping caps mean within-category rankings are not materially distorted by this specific mechanism.

### Disposition

**Monitored.** The scientific basis for distinguishing protein completeness is established and should be implemented in BSIP1 enrichment at some point. The appropriate trigger for elevated priority is: expansion of the corpus into product classes where gelatin or isolate protein is the primary nutritional claim and where overlapping caps are absent.

---

## Classification Summary

| ID | Distortion | Classification | Priority Disposition |
|---|---|---|---|
| DIST-001 | Dairy fiber penalty | **Significant** | Prioritized for future BSIP2 work |
| DIST-002 | Date sugar halo | **Significant** | Researched |
| DIST-003 | Router v2 missing archetypes | **Critical** | Prioritized for future BSIP2 work |
| DIST-004 | Prototype weight divergence | **Significant** | Researched |
| DIST-005 | Inactive scoring layers (snacks) | **Critical** | Prioritized for future BSIP2 work — immediate |
| DIST-006 | Classification instability | **Critical** | Prioritized for future BSIP2 work |
| DIST-007 | Structural emptiness blind spot | **Significant** | Prioritized for future BSIP2 work |
| DIST-008 | Cliff-edge cap gaming | **Moderate** | Monitored |
| DIST-009 | Condiment per-100g evaluation | **Moderate** | Researched |
| DIST-010 | Incomplete protein credit | **Minor** | Monitored |

---

## Dimension Impact Matrix

| ID | Scientific Validity | Consumer Trust | Score Accuracy | Category Calibration |
|---|---|---|---|---|
| DIST-001 | Affected | Affected | Affected (0.84–4.46pts, direction certain) | Affected (uniform downscoring of dairy) |
| DIST-002 | Partially affected | Significantly affected | Unknown magnitude | Affected (within snack_bar_granola) |
| DIST-003 | Severely affected | Severely affected | Severely affected (up to 30pts) | Severely affected (wrong reference frame) |
| DIST-004 | Affected | Conditionally affected | Unknown magnitude | Affected (all categories, direction unknown) |
| DIST-005 | Severely affected | Severely affected | Severely affected (10–20pts, 11 incorrect labels) | Severely affected (rankings based on partial data) |
| DIST-006 | Severely affected | Severely affected | Severely affected (up to 40pts) | Severely affected (wrong category entirely) |
| DIST-007 | Affected | Affected | Affected (5–15pts positive distortion) | Affected (diet variants over-ranked) |
| DIST-008 | Partially affected | Conditionally affected | Not currently affected | Not currently affected |
| DIST-009 | Technically accurate, contextually misleading | Affected for condiment users | Severely affected for specific products | Affected within sauce_spread |
| DIST-010 | Affected (gelatin: strong evidence) | Low-moderate | Low-moderate (3–7pts, typically masked) | Minimally affected |

---

## CNO Prioritization Assessment

Three distortions require action before the next category expansion or corpus promotion:

1. **DIST-005** — Confidence labels are factually wrong in production today. This is a data integrity issue with no analytical justification for delay. Should be resolved before snacks is promoted.

2. **DIST-003** — The bread category is live with known router gaps that produce analytically invalid scores for seed-topped products. The bread corpus should be audited against router output before any new bread scoring cycles run.

3. **DIST-006** — Classification instability is the highest single-instance risk in the system. The minimum viable mitigation (surfacing `category_confidence` as a first-class output field) should be implemented as soon as technically feasible.

Three distortions require active research before classification can be finalised:

4. **DIST-002** — The date sugar position needs empirical quantification for the specific product forms in the corpus before a final classification can be made.

5. **DIST-004** — The weight divergence magnitude is unknown. A calibration corpus study is required to determine whether this distortion is Minor or Critical.

6. **DIST-009** — The condiment prevalence in the sauce_spread corpus needs measurement before deciding whether monitoring is sufficient.

Four distortions are correctly in the monitoring queue:

7. **DIST-001** — Real, quantified, should be fixed before yogurt launch. Planning queue.
8. **DIST-007** — Architectural gap acknowledged; positive architecture is the resolution. Planning queue.
9. **DIST-008** — Prospective. Monitor for threshold reformulation evidence.
10. **DIST-010** — Minor. Monitor for corpus expansion into gelatin-primary products.

---

*End of CNO Distortion Classification v1.*
